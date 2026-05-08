"""Pre-render script: generate macros-pdf.tex and macros-html.html from macros/macros.qmd.

HTML comments (<!-- ... -->) are not valid in a LaTeX preamble, so this script
strips them before the file is included in PDF output via include-in-header.
The generated macros-pdf.tex is a build artifact (excluded from git via .gitignore).

For HTML output, the macros need to be wrapped in $$ delimiters so MathJax can
process them. The generated macros-html.html is also a build artifact.
"""

import re

src = "macros/macros.qmd"
dst_pdf = "macros-pdf.tex"
dst_html = "macros-html.html"

with open(src, encoding="utf-8") as f:
    content = f.read()

# Remove HTML comments (<!-- ... -->) which are invalid in LaTeX preambles
content_pdf = re.sub(r"<!--.*?-->", "", content, flags=re.DOTALL)

with open(dst_pdf, "w", encoding="utf-8") as f:
    f.write(content_pdf)

print(f"Generated {dst_pdf} from {src}")

# For HTML, wrap in $$ delimiters for MathJax
content_html = "$$\n" + content + "\n$$\n"

with open(dst_html, "w", encoding="utf-8") as f:
    f.write(content_html)

print(f"Generated {dst_html} from {src}")
