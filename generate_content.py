import os
import nbformat
import base64

header = r"""
---
title: "Introduction to Scientific Programming in Python"
author: "Pablo Peñas (<pablo.penas@virtuscollege.es)>"
date: "June 14, 2024"
fontsize: 10pt
geometry: margin=1in
mainfont: "Times"
papersize: a4
toc: true  # Include table of contents
toc-depth: 3  # Depth of the table of contents
numbersections: true  # Number the sections
header-includes:
  - \usepackage{amsmath}  # Additional LaTeX packages if needed
  - \usepackage{graphicx}
  - \setcounter{tocdepth}{3}  # Set the TOC depth
  - \setcounter{secnumdepth}{3}  # Set the section numbering depth
  - \renewcommand{\thesection}{\hspace*{\baselineskip}}  # Remove numbering from sections
  - \renewcommand{\thesubsection}{\arabic{section}.\arabic{subsection}}  # Number subsections normally

---
"""


def read_notebook(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return nbformat.read(f, as_version=4)

def get_notebook_summary(notebook):
    summary = []
    for cell in notebook['cells']:
        if cell['cell_type'] == 'markdown':
            content = ''.join(cell['source']).strip()
            if content !="#### Answer":
                summary.append(content+' \n')
                summary.append(' \n')
        elif cell['cell_type'] == 'code':
            code = ''.join(cell['source']).strip()
            if code !="":
                formatted_code = f"```python\n{code}\n```"
                summary.append(formatted_code)
                summary.append('\n')

        # Process outputs
        for output in cell.get('outputs', []):
            if output['output_type'] == 'stream':
                summary.append('*Output:* \n')
                text_output = ''.join(output['text']).strip()
                summary.append(f"```\n{text_output}\n```")
            elif output['output_type'] == 'display_data' or output['output_type'] == 'execute_result':
                    for data_type, data in output['data'].items():
                        if data_type == 'text/plain':
                            text_output = ''.join(data).strip()
                            summary.append(f"```\n{text_output}\n```")
                        elif data_type == 'image/png':
                            image_data = base64.b64encode(base64.b64decode(data)).decode('utf-8')
                            summary.append(f'![](data:image/png;base64,{image_data})')
                        elif data_type == 'image/jpeg':
                            image_data = base64.b64encode(base64.b64decode(data)).decode('utf-8')
                            summary.append(f'![](data:image/jpeg;base64,{image_data})')
                        elif data_type == 'text/html':
                            html_output = ''.join(data).strip()
                            summary.append(html_output)
    return summary

def summarize_notebooks(directory):
    summaries = {}
    for root, _, files in os.walk(directory):
        files = sorted(files)[:]
        for file in files:
            if file.endswith('.ipynb'):
                file_path = os.path.join(root, file)
                notebook = read_notebook(file_path)
                summaries[file] = get_notebook_summary(notebook)
    return summaries

def create_outline_file(summaries, output_path='Booklet/CODING_BOOKLET.md'):
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(header)
        for notebook, summary in summaries.items():
            ### f.write(r'\rule{\textwidth}{1mm}')
            f.write(r'\newpage')
            f.write('\n')
            f.write(f'*{notebook}* \n\n')
            for item in summary:
                f.write(f'{item}\n')
            f.write('\n')

if __name__ == "__main__":
    directory = 'Sessions/'  # Change this to the directory containing your notebooks
    summaries = summarize_notebooks(directory)
    create_outline_file(summaries)