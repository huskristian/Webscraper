"""
    project: Webscraper
    author: Kristián Hus
    email: huskristian@seznam.cz
    discord: Kristus
"""
import requests
from bs4 import BeautifulSoup
import csv
import argparse

# Funkce, která odstraní část URL za posledním lomítkem
def remove_after_last_slash(url):
    last_slash_index = url.rfind('/')  # Najde pozici posledního lomítka v URL
    if last_slash_index != -1:  # Pokud nějaké lomítko existuje
        return url[:last_slash_index]  # Vrátí část URL před posledním lomítkem
    return url  # Pokud není lomítko, vrátí původní URL

# Funkce krok1, která získává data z hlavní stránky a následně volá krok2
# pro získání dat z podstránek
def krok1(url, output_file):
    response = requests.get(url)  # Zasílá HTTP GET požadavek na URL
    if response.status_code == 200:  # Pokud je požadavek úspěšný
        soup = BeautifulSoup(response.content, 'html.parser')  # Parsuje HTML obsah stránky
        rows = soup.find_all('tr')  # Najde všechny řádky tabulky na stránce

        data = []  # Vytvoří list pro uložení všech řádků dat

        for row in rows:  # Prochází každý řádek tabulky
            cells = row.find_all("td")  # Najde všechny buňky v daném řádku
            if len(cells) >= 2:
                cell1 = cells.pop(0)  # První buňku odebere a uloží do cell1
                cell2 = cells.pop(0)  # Druhou buňku odebere a uloží do cell2
                links = cell1.find_all("a")  # Hledá odkazy v první buňce
                if len(links) >= 1:
                    link1 = links.pop(0)  # Odebere první odkaz
                    href = link1.get("href")  # Získá hodnotu atributu href (URL podstránky)
                    url2 = remove_after_last_slash(url) + "/" + href  # Sestaví úplnou URL podstránky

                    row_data = [cell1.get_text(strip=True), cell2.get_text(strip=True)]  # Získá text z prvních dvou buněk
                    # Volá krok2, který získává další data z podstránky a přidává je do row_data
                    krok2(url2, data, row_data)

        # Otevře CSV soubor pro zápis a zapíše všechny získané řádky
        with open(output_file, 'w', newline='', encoding='cp1250') as file:
            writer = csv.writer(file, delimiter=";")  # Nastaví CSV writer s oddělovačem středníkem
            writer.writerows(data)  # Zapíše všechna data do CSV souboru
    else:
        print("Chyba při získavání dat")

# Funkce krok2, která získává další data z podstránky a přidává je do hlavního seznamu
def krok2(url, excel_rows, row_data):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        rows = soup.find_all('tr')
        hlavicky = []

        for row in rows:  # Prochází každý řádek tabulky
            cells = row.find_all("td")
            if len(cells) == 9:
                cell1 = cells.pop(3)  # Odebere čtvrtou buňku
                cell2 = cells.pop(3)  # Odebere pátou buňku
                platne_hlasy = cells.pop(5)  # Odebere osmou buňku
                # Přidá hodnoty z buněk do seznamu row_data
                row_data.extend([cell1.get_text(strip=True), cell2.get_text(strip=True), platne_hlasy.get_text(strip=True)])
            elif len(cells) == 5:  # Pokud je v řádku 5 buněk
                nazev_strany = cells.pop(1).get_text(strip=True)  # Odebere a získá název strany
                celkem_hlas = cells.pop(1).get_text(strip=True)  # Odebere a získá celkový počet hlasů
                row_data.append(celkem_hlas)  # Přidá počet hlasů do row_data
                hlavicky.append(nazev_strany)

        # Pokud excel_rows je prázdný (hlavní seznam neobsahuje žádné data)
        # vytvoří hlavičku tabulky a přidá ji do excel_rows
        if len(excel_rows) == 0:
            hlavicky = ['code', 'location', 'registered', 'envelopes', 'valid'] + hlavicky  # Přidá základní hlavičky.
            excel_rows.append(hlavicky)

        excel_rows.append(row_data)
    else:
        print("Chyba při získavání dat")

# Hlavní funkce, která spouští celý proces a volá krok1
def main(url, output_file):
    krok1(url, output_file)

if __name__ == '__main__':
    # Vytvoří objekt parseru pro zpracování argumentů z příkazové řádky
    parser = argparse.ArgumentParser(description='Web scraping script')
    parser.add_argument('url', type=str, help='URL of the website to scrape')
    parser.add_argument('output_file', type=str, help='Name of the output file')
    # Zpracuje argumenty
    args = parser.parse_args()


    if not args.url or not args.output_file:
        print("Chyba: Musíte zadat oba argumenty: URL a název výstupního souboru.")  # Zobrazí chybovou hlášku.
    else:
        main(args.url, args.output_file)
