#!/usr/bin/env bash
# Apply branch rulesets from .github/rulesets/*.json to the current repo.
# Run once after creating a new repo from this template. Idempotent: a
# ruleset whose `name` already exists on the repo is updated in place rather
# than duplicated.
#
# Requires: gh CLI authenticated with admin access to the repo.
# Usage:    .github/scripts/apply-rulesets.sh [owner/repo]
#           Defaults to the gh-detected current repo.

set -euo pipefail

repo="${1:-$(gh repo view --json nameWithOwner -q .nameWithOwner)}"
ruleset_dir="$(cd "$(dirname "$0")/../rulesets" && pwd)"

shopt -s nullglob
files=("$ruleset_dir"/*.json)
if [ ${#files[@]} -eq 0 ]; then
  echo "no rulesets found in $ruleset_dir" >&2
  exit 0
fi

# Map of existing ruleset name -> id, so we can PUT updates instead of
# creating duplicates.
existing=$(gh api "repos/$repo/rulesets" --jq '[.[] | {name, id}]')

for f in "${files[@]}"; do
  name=$(jq -r .name "$f")
  id=$(jq -r --arg n "$name" 'map(select(.name == $n)) | .[0].id // empty' <<<"$existing")
  if [ -n "$id" ]; then
    echo "updating ruleset '$name' (id $id) on $repo"
    gh api -X PUT "repos/$repo/rulesets/$id" --input "$f" >/dev/null
  else
    echo "creating ruleset '$name' on $repo"
    gh api -X POST "repos/$repo/rulesets" --input "$f" >/dev/null
  fi
done

echo "done."
