# Webscraper

Skript získává výsledky parlamentních voleb z roku 2017 v konkrétních krajích [z tohoto webu](https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ) (Zde si vyeberte okres) a ukládá je do CSV souboru.

## Postupy

První si nainstalujte knihovny potřebné pro spuštění ze souboru s názvem [requirements.txt](./requirements.txt). Celý skript následně spustíte z příkazového řádku pomocí tohoto příkazu:

python webscraper.py <url_adresa_okresu> <csv_soubor>

CSV soubor bude výstup se všemi daty.

## Příklad

Příklad pro okres Prostějov

  1.URL -> https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103
  2.Název CSV souboru -> [výstup.csv](./výstup.csv)

Příkaz:

  python webscraper.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" "výstup.csv"
