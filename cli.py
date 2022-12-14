''' Creation Date: 14/11/2022 '''


import inquirer


# from Functions.keywords import
from Functions.efa_analysis import efa_analysis
from Functions.construct_csv import construct_csv
from Functions.library import Formats


OPTIONS = {'Build CSV': construct_csv, 'Create Keywords': quit, 'EFA Analysis': efa_analysis, 'Exit': quit}


def select_option():
    ''' Returns: User selected action. '''
    return inquirer.list_input(
        message = 'What would you like to do',
        choices = list(OPTIONS.keys())
    )


if __name__ == '__main__':
    while True:
        choice = select_option()
        if choice == 'Exit':
            quit()
        Formats.status(f'{choice} selected')
        try:
            OPTIONS[choice]()
            print('\n')
        except KeyboardInterrupt:
            Formats.alert(f'Aborting {choice}')
