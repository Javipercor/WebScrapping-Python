import whois
import requests
import builtwith
from bs4 import BeautifulSoup
from scraper import tableScraper
from scraper import graphScraper

tablescraper=tableScraper()
graphscraper=graphScraper()

url='https://www.worldometers.info/coronavirus'
page=requests.get(url)
soup=BeautifulSoup(page.content,features="lxml")

#Cargamos el contenido de la página y llamamos a la función para obtener el encabezado de la tabla
table=soup.find('table')
header=tablescraper.get_header(table)

#Realizamos la primera consulta a la tabla con todos los paises y guardamos
countries=tablescraper.get_data(table,'a','mt_a')
data_countries=tablescraper.create_dataset(countries,header)
tablescraper.save_data(data_countries,'data_countries',';')
#Realizamos la segunda consulta esta vez a la tabla con los totales por continente y guardamos
continents=tablescraper.get_data(table,'tr','total_row_world')
data_continents=tablescraper.create_dataset(continents,header)
tablescraper.save_data(data_continents,'data_continents',';')
#Realizamos la tercera consulta, esta vez a las gráficas de evolución de caso por cada día y guardamos
total_days,series_countries=graphscraper.get_series(table,'a','mt_a','href',url)
data_series_countries=graphscraper.create_series_dataset(total_days,series_countries)
graphscraper.save_data(data_series_countries,'data_series_countries',';')


