import argparse
import json
import glob
import logging
import os
import sys

def setup_logging():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def adapt_to_all(folder, contents):
    return [ item.replace('(./', f'(./{folder}/') for item in contents]


def create_index():
    notebooks_path = os.path.join(os.path.dirname(__file__), '..', 'notebooks')
    all_contents = []
    for file in glob.glob(os.path.join(notebooks_path, '*')):
        if os.path.isdir(file):
            folder_contents = create_index_folder(file)
            all_contents.extend(adapt_to_all(os.path.basename(file), folder_contents))
    
    dump_file(notebooks_path, all_contents)

def get_notebook_head(notebook_path):
    notebook_filename = os.path.basename(notebook_path)
    with open(notebook_path, 'r') as notebook_file:
        notebook_json = json.load(notebook_file)
        cells = notebook_json.get('cells', [])
        if len(cells):
            contents = cells[0].get('source', [f'Not valid notebook'])
            contents[0] = (f'[{notebook_filename[:-6]}](./{notebook_filename}) **{contents[0][2:].strip()}**')
            contents.append('***')
            return contents
        else:
            return f'Not valid notebook {notebook_filename}'

def format_contents(list_of_contents):
    return ''.join([item if item.endswith('\n') else f'{item}\n' for item in list_of_contents])

def create_index_folder(folder_path):
    contents = [f' # {os.path.basename(folder_path)}']
    for file in sorted(glob.glob(os.path.join(folder_path, '*.ipynb'))):
        head = get_notebook_head(file)
        contents.extend(head)
    if len(contents) <= 1:
        logging.info(f'Notebooks not found in {folder_path}')
        return []
    dump_file(folder_path, contents)
    return contents

def dump_file(folder_path, contents):
    with open(os.path.join(folder_path, 'README.md'), 'w+') as index_file:
        index_file.write(format_contents(contents))

if __name__ == '__main__':
    setup_logging()
    parser = argparse.ArgumentParser(prog='indexer', description='This tool creates the indexes of the notebook using markdown files README.md')
    args = parser.parse_args()
    create_index()