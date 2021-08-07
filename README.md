# MOTMRipper

Minutes of the meeting (MOTM) autogeneration using Pandoc, LaTeX, and Python. Retrofitted for any documentation commitee.

## Rationale

MOTMRipper is the answer to _"How might we generate MOTM documents fast?"_ Markdown is used as a quick language. Pandoc then parses the markdown into a beautifully formatted PDF document.

## Requirements

1. Install Pandoc. Download their installers [here](https://pandoc.org/installing.html).
   - If you are using Windows, I recommend using [MiKTeX](https://miktex.org/howto/miktex-console) to automatically handle your LaTeX dependencies.
2. Install Python 3 and `python-frontmatter`.
   ```bash
   $ pip install python-frontmatter
   ```

## Usage