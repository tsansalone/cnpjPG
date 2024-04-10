import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'

def get_page(url):
    request = Request(url)
    request.add_header('User-Agent', USER_AGENT)
    response = urlopen(request)
    return response

def construct_url(row, city='Praia Grande'):
    address_parts = [row['tipo_logradouro'], row['logradouro'], row['numero_logradouro'], row['bairro'], city]
    address = '+'.join(part.replace(' ', '+') for part in address_parts)
    base_url = f"https://www.google.com/maps/place/{address}"
    return base_url

def get_latlong(row):
    url = construct_url(row)
    html = get_page(url)
    soup = BeautifulSoup(html, 'html.parser')
    
    """
        Localizando a latitude e longitude no script do google maps
        substituir toda a função por uma chamada a API para garantir estabilidade
        webscrapping esta sendo utilizado apenas para PoC e para fixar os conhecimentos
    """
    script = str(soup.find(lambda tag: tag.name == "script" and isinstance(tag.string, str) and tag.string.startswith("(function(){window.APP_OPTIONS")))
    init_state = "window.APP_INITIALIZATION_STATE=[[["
    start = script.find(init_state)
    end = script[start:].find("]") + start
    _, long, lat = (script[start+len(init_state):end]).split(",")
    return lat, long

df = pd.read_csv('dataset_cnpj_praia_grande_02.csv', delimiter=';', encoding='ISO-8859-1', dtype='str')

df['latlong'] = df.apply(get_latlong, axis=1)

df.to_csv('dataset_cnpj_praia_grande_03.csv', index=False, sep=';', encoding='ISO-8859-1')