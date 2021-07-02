if __name__ == '__main__':
    import os
    import argparse
    import requests
    from colorama import Fore
    from bs4 import BeautifulSoup
    from collections import deque


    def print_tekst(sait):
        teksta = sait.find_all(['a', 'title', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li'])
        for el in teksta:
            if el.name == 'a':
                print(Fore.BLUE + el.get_text())
            else:
                print(Fore.RESET + el.get_text())
        return


    # ------- S T A R T -------
    argumenti = argparse.ArgumentParser()
    argumenti.add_argument('papka')
    ok = argumenti.parse_args()
    if not os.access(ok.papka, os.F_OK):
        os.mkdir(ok.papka)
    papka = ok.papka

    history = deque()
    while True:
        inp = input()
        if inp == 'back':
            if history:
                history.pop()
                inp = history.pop()
        clean_inp = inp.split("//")[-1].split(".")[0]  # replace('.', '_')  # без http и .com хуйни
        if inp == 'exit':
            break
        elif clean_inp in os.listdir(papka):
            with open(f'{papka}/{clean_inp}', 'rt') as fail:
                yo = str(fail.readlines())
                # yo = "\n".join([ele.strip('\n') for ele in yo])
                soup = BeautifulSoup(yo, 'html.parser')
                print_tekst(soup)
                history.append(inp)
        else:
            if 'https://' not in inp:
                big_inp = 'https://' + inp
            else:
                big_inp = inp
            try:
                r = requests.get(big_inp)
            except requests.exceptions.ConnectionError:
                print('Incorrect URL')
            else:
                if 200 <= r.status_code < 300:
                    history.append(inp)
                    soup = BeautifulSoup(r.content, 'html.parser')
                    with open(f'{papka}/{clean_inp}', 'wt', encoding='utf-8') as fail:
                        fail.write(str(soup))  # в файл вхуяривается сырой хтмл
                    print_tekst(soup)
                else:
                    print(r.status_code)
