# Mermaid
This directory must contain all template Markdown files which embed Mermaid diagrams.

## Exporting
If a Mermaid diagram does not render properly on GitHub, the Markdown file needs to be exported using the mermaid-cli to produce a new file with a static image in place of the mermaid diagram.

To export a Markdown file, run the following command at the project root:

`mmdc -i docs/mermaid/[template-file] -o [output-file] -a docs/images --theme neutral --iconPacks @iconify-json/mdi @iconify-json/logos`

This command exports mermaid diagrams in the neutral theme, and supports the `mdi` and `logos` icon sets. To add another icon set, specify the relevant `@iconify-json/[icon-set]` package.