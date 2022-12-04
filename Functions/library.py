''' Creation Date: 09/11/2022 '''


import pandas
import os
import inquirer
from colorama import Fore, Style


DATAFOLDER = 'Raw_Data/'
RESULTFOLDER = 'Results/'


class Formats:
    ''' Purpose: Correctly print messages given purpose. '''
    def status(self):
        ''' [-] message...'''
        indicator = '\n[' + Fore.GREEN + '-' + Style.RESET_ALL + ']'
        print(f'{indicator} {self}...')
    def question(self):
        ''' [?] message: '''
        indicator = '\n[' + Fore.YELLOW + '?' + Style.RESET_ALL + ']'
        print(f'{indicator} {self}: ')
    def alert(self):
        ''' [!] message...'''
        indicator = '\n[' + Fore.RED + '!' + Style.RESET_ALL + ']'
        print(f'{indicator} {self}...')
    def info(self):
        ''' [i] message'''
        indicator = '[' + Fore.BLUE + 'i' + Style.RESET_ALL + ']'
        print(f'{indicator} {self}')


class Dataframe:
    ''' Purpose: Loads CSV file to dataframe for processing. '''
    def __init__(self, filename: str):
        self.dataframe = pandas.read_csv(filename, encoding = 'ISO-8859-1')
    def get_headers(self):
        ''' Returns: List of headers for given CSV file. '''
        return self.dataframe.columns.tolist()
    def get_column(self, column: str):
        ''' Returns: List of values for given CSV column. '''
        return self.dataframe[column].tolist()
    def get_length(self):
        ''' Returns: Number of rows in given CSV data. '''
        return len(self.dataframe.index)


def get_choice(choices, message: str):
    ''' Returns: Get user choice from list or dict key options. '''
    dictionary = type(choices) is dict
    options = list(choices.keys()) if dictionary else choices
    choice = inquirer.list_input(
        message = message,
        choices = options)
    return choices[choice] if dictionary else choice 


def get_files(location: str, extension: str):
    ''' Returns: List of file names at location with extension. '''
    return [file for file in os.listdir(location) if file.endswith(extension) or extension == '*']


def get_CSV(filename: str):
    ''' Returns: CSV loaded to dataframe with select columns dropped. '''
    return pandas.read_csv(os.path.join(os.path.dirname(__file__), f'../{DATAFOLDER}{filename}'), encoding='ISO-8859-1')


def nice_print(self):
    ''' Returns: Nicely formatted string representation of class contents. '''
    return '\n'.join(f'{item} = {self.__dict__[item]}' for item in self.__dict__)
