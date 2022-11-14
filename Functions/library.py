''' Creation Date: 09/11/2022 '''


from colorama import Fore, Style


# Stores general classes and functions used across project

class Formats:
    ''' Purpose: Correctly format print messages given purpose. '''
    def status(message: str):
        ''' Format: [-] message...'''
        indicator = '\n[' + Fore.GREEN + '-' + Style.RESET_ALL + ']'
        return f'{indicator} {message}...'
    def question(message: str):
        ''' Format: [?] message: '''
        indicator = '\n[' + Fore.YELLOW + '?' + Style.RESET_ALL + ']'
        return f'{indicator} {message}: '
    def alert(message: str):
        ''' Format: [!] message...'''
        indicator = '\n[' + Fore.RED + '!' + Style.RESET_ALL + ']'
        return f'{indicator} {message}...'
    def info(message: str):
        ''' Formats: [i] message'''
        indicator = '\n[' + Fore.BLUE + 'i' + Style.RESET_ALL + ']'
        return f'{indicator} {message}'