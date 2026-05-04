"""Pre-render script: generate macros-pdf.tex from macros/macros.qmd.

HTML comments (<!-- ... -->) are not valid in a LaTeX preamble, so this script
strips them before the file is included in PDF output via include-in-header.
The generated macros-pdf.tex is a build artifact (excluded from git via .gitignore).
"""

import re

src = "macros/macros.qmd"
dst = "macros-pdf.tex"

with open(src) as f:
    content = f.read()

# Remove HTML comments (<!-- ... -->) which are invalid in LaTeX preambles
content = re.sub(r"<!--.*?-->", "", content, flags=re.DOTALL)

with open(dst, "w") as f:
    f.write(content)

print(f"Generated {dst} from {src}")
