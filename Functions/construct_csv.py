''' Creation Date: 14/11/2022 '''


import os
import itertools
import re
import inquirer

try:
    import Functions.library as lib
except ImportError:
    import library as lib


TOPIC_HEADER = 'TOPIC:'
DATATYPE_CHOICES = {'Audio':'audio', 'Chat':'chat'}
DIC = ['group', 'datatype', 'text']
LINE_HEADER = ['name','timestamp']
CSV_HEADER = f'{",".join(itertools.chain(DIC[:-1], ["topic"], LINE_HEADER, [DIC[-1]]))}\n'


def load_textfile(filename: str):
    ''' Returns: List of text lines from textfile. '''
    data = []
    with open(f'{lib.DATAFOLDER}{filename}') as file:
        for line in file: # Remove whitespace and quotation marks
            if clean_line := re.sub(r'"', '', line).strip():
                data.append(clean_line)
    return data


def check_group(_, text: str):
    ''' Purpose: Validates group name only contains acceptable characters. '''
    if not re.match(r'^[A-Za-z0-9_-]*$', text):
        raise inquirer.errors.ValidationError('', reason = f'{text} contains invalid characters...')
    return True


def get_group(textfile: str):
    ''' Returns: User input for group column. '''
    return inquirer.text(
        message = f'Please enter group name for {textfile}',
        validate = check_group
    )


def check_filename(_, text: str):
    ''' Purpose: Validates filename has acceptable characters and does not exist. '''
    if not re.match(r'^[A-Za-z0-9_-]*$', text):
        raise inquirer.errors.ValidationError('', reason = f'{text} contains invalid characters...')
    existing = lib.get_files(lib.DATAFOLDER, '.csv')
    if f'{text}.csv' in existing:
        raise inquirer.errors.ValidationError('', reason = f'{text} is an existing filename...')
    return True


def get_filename():
    ''' Returns: User entered filename. '''
    return inquirer.text(
        message = 'Please enter a CSV filename',
        validate = check_filename
    )


def create_csv(filename: str, data: list):
    ''' Purpose: Creates new CSV file from compiled data. '''
    topic = ''
    with open(f'{lib.DATAFOLDER}{filename}.csv', 'a') as output:
        output.write(CSV_HEADER)
        for dic in data:
            group = dic.get(DIC[0])
            datatype = dic.get(DIC[1])
            for text in dic.get(DIC[2]):
                if text.startswith(TOPIC_HEADER):
                    topic = text[len(TOPIC_HEADER):].strip()
                    continue
                args = ''
                if text.startswith('[') and ']' in text:
                    args = text.split('[', 1)[1].split(']')[0]
                    text = text[len(args) + 2:].lstrip()
                fields = args + ',' * (len(LINE_HEADER) - 1 - args.count(','))
                line = ','.join([f'"{group}"', f'"{datatype}"', f'"{topic}"', f'"{fields}"', f'"{text}"'])
                output.write(f'{line}\n')


def construct_csv():
    try:
        textfiles = lib.get_files(lib.DATAFOLDER, '.txt')
        print(lib.Formats.status(f'Found {len(textfiles)} textfiles'))
        data = [] # List of Dictionaries
        for textfile in textfiles:
            print(lib.Formats.status(f'Processing {textfile}'))
            group = get_group(textfile)
            datatype = lib.get_choice(DATATYPE_CHOICES, f'Please select datatype for {textfile}')
            contents = load_textfile(textfile)
            dictionary = dict(zip(DIC, [group, datatype, contents]))
            data.append(dictionary)
        filename = get_filename()
        print(lib.Formats.status('Creating CSV output'))
        create_csv(filename, data)
    except Exception as error:
        print(lib.Formats.alert(f'CSV construction failed:\n{error}'))
        quit()


if __name__ == '__main__':
    construct_csv()
