''' Creation Date: 14/11/2022 '''


import inquirer


from Functions.construct_csv import construct_csv
from Functions.library import Formats


OPTIONS = {'Build CSV': construct_csv, 'Create Keywords': quit, 'Exit': quit}


def select_option():
    ''' Returns: User selected action. '''
    return inquirer.list_input(
        message = f'What would you like to do',
        choices = list(OPTIONS.keys())
    )


if __name__ == '__main__':
    while True:
        choice = select_option()
        if choice == 'Exit':
            quit()
        print(Formats.status(f'{choice} selected'))
        try:
            OPTIONS[choice]()
            print('\n')
        except KeyboardInterrupt:
            print(Formats.alert(f'Aborting {choice}'))
            pass
