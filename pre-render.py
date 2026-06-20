"""Pre-render script: generate macros-pdf.tex from macros/macros.qmd.

HTML comments (<!-- ... -->) are not valid in a LaTeX preamble, so this script
strips them before the file is included in PDF output via include-in-header.
The generated macros-pdf.tex is a build artifact (excluded from git via .gitignore).

For HTML output, macros-header.html (a JavaScript loader) fetches and parses
macros/macros.qmd at runtime and registers the macros with MathJax. The macros.qmd
file is copied to the output directory by Quarto (via project.resources in _quarto.yml).
"""

import re

src = "macros/macros.qmd"
dst_pdf = "macros-pdf.tex"

with open(src, encoding="utf-8") as f:
    content = f.read()

# Remove HTML comments (<!-- ... -->) which are invalid in LaTeX preambles
content_pdf = re.sub(r"<!--.*?-->", "", content, flags=re.DOTALL)

with open(dst_pdf, "w", encoding="utf-8") as f:
    f.write(content_pdf)

print(f"Generated {dst_pdf} from {src}")
