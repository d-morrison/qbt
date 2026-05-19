# Branch rulesets

Each JSON file here is a GitHub branch ruleset exported from the template's
canonical configuration. Apply them to a new repo (after creating it from
the template) with:

```sh
.github/scripts/apply-rulesets.sh                 # current repo
.github/scripts/apply-rulesets.sh owner/repo      # explicit target
```

The script is idempotent — re-running it updates a ruleset in place when
one with the same `name` already exists, rather than creating a duplicate.

Requirements:

- `gh` CLI authenticated as a repo admin (org or user). Branch rulesets
  require admin scope to create.
- `jq` available on PATH.

## What's enforced (`main.json`)

Applies to the default branch:

- **Required PR before merging** — no direct pushes to `main`.
- **Required status checks** (not strict — branch does not need to be up
  to date): link-checker, Spellcheck, check-chars, build-deploy.
- **No force-pushes, no branch deletion.**
- **Bypass** in `pull_request` mode for the Maintain role (role id 2) —
  Maintainers can merge via a PR they authored, but cannot push directly.

## Editing the ruleset

Edit `main.json` here, then run `apply-rulesets.sh` to push the change to
the live repo. Or edit in the GitHub UI (Settings → Rules → Rulesets) and
re-export with:

```sh
gh api repos/OWNER/REPO/rulesets/RULESET_ID \
  | jq 'del(.id, .node_id, .source, .source_type, .created_at, .updated_at, ._links, .current_user_can_bypass)' \
  > .github/rulesets/main.json
```

The fields stripped by `jq del(...)` are server-assigned and would either
be ignored or rejected by the create/update endpoints.
