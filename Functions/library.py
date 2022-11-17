''' Creation Date: 09/11/2022 '''


import pandas

from colorama import Fore, Style


# Stores general classes and functions used across project
class Formats:
    ''' Purpose: Correctly format print messages given purpose. '''
    def status(self):
        ''' Format: [-] message...'''
        indicator = '\n[' + Fore.GREEN + '-' + Style.RESET_ALL + ']'
        return f'{indicator} {self}...'
    def question(self):
        ''' Format: [?] message: '''
        indicator = '\n[' + Fore.YELLOW + '?' + Style.RESET_ALL + ']'
        return f'{indicator} {self}: '
    def alert(self):
        ''' Format: [!] message...'''
        indicator = '\n[' + Fore.RED + '!' + Style.RESET_ALL + ']'
        return f'{indicator} {self}...'
    def info(self):
        ''' Formats: [i] message'''
        indicator = '\n[' + Fore.BLUE + 'i' + Style.RESET_ALL + ']'
        return f'{indicator} {self}'


# Stores general functionality around working with CSV type data
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
