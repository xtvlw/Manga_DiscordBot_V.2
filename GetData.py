from bs4 import BeautifulSoup as bs
from requests import get
from os import getcwd
from random import randrange
from time import time

def CleanCaracters(string):
    caracters = '''"'!@#$¨&*()_+=´`[{~^]}<>:?/;.,\|'''
    string = string.replace('!get ', '')
    for caracter in caracters:
        string = str(string).replace(caracter, '')
    return string.replace(' ', '-').lower()


def GetDataInfo(manga_name):
    MainPage = f'https://www.supermangas.site/manga/{CleanCaracters(manga_name)}/'
    page = get(MainPage).text
    soup = bs(page, 'html.parser')
    GenderClass = soup.find_all('a', class_='genero_btn')
    Genders = 'Genero:'
    for gender in GenderClass:
        if 'autor' in gender.get('href'):
            Genders = Genders[:-1]
            break
        Genders += f' {gender.get_text()},'
    manga = soup.find('ul', class_='boxAnimeSobre')
    manga_info = manga.get_text()
    manga_info = "\n" + manga_info[manga_info.find('Formato'):manga_info.find('Assinar')]
    manga_image = soup.find_all('div', class_='animeCapa')[0].find('img').get('src')
    manga_info = Genders + manga_info
    return {"Info":manga_info[:-3], "image": manga_image}


def GetImageData(manga_name, manga_capter=1):
    MainPage = f'https://www.supermangas.site/manga/{CleanCaracters(manga_name)}/{manga_capter}'
    page = get(MainPage).text
    soup = bs(page, 'html.parser')
    ImageTag = soup.find_all('div',class_="capituloViewBox")
    arc_path = f'{getcwd()}/MangaBotV2/mangas/{manga_name}Cap{manga_capter}_{randrange(1, 10)}.html'
    arc = open(arc_path, 'w')
    for tag in ImageTag:
        link = tag.find('img').get('data-src')
        arc.write(f"<div><center><img src={link}></img></center></div>\n")
    arc.write("<style>body{ background-color: black}</style>")
    return arc_path
