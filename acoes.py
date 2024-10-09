import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import codecs 
import os


def buscarDados():
    global paginaUolBaixada
    url= "http://economia.uol.com.br/cotacoes/"
    HEADERS = {
            "authority" : url.split("//")[1].split("/")[0],
            "method" : "GET" ,
            "path" : "/"+url.split("//")[1]+"/",
            "scheme" : url, 
            "referer" : url,
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upagrade-insecure-requests" : "1",
            "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130'
            }
    page = requests.get(url=url, headers=HEADERS)
    soup = BeautifulSoup(page.content, 'lxml')
    paginaUolBaixada = soup
    infos = soup.findAll("div", class_="ticker-slide")[0].find(class_="ipca")
    tables = soup.findAll("table", class_="data-table")
    ##print(tables[0])
   
    cont = 0
    JsonGeral = []
    for table in tables :
        ##print(table.previousSibling.contents[0])
        if cont >=3 and cont <= 5:
        
            for tr in table.findAll("tr"):
                empresa = tr.findAll("td")[0].findAll("a")[0].contents[0]
                variacao = tr.findAll("td")[1].findAll("a")[0].contents[0]
                cotacao = tr.findAll("td")[2].findAll("a")[0].contents[0]
                linhaJson = {
                    "empresa": empresa,
                    "variacao": variacao,
                    "cotacao": cotacao,
                    "tipo" : table.previousSibling.contents[0],
                }
                
                
                JsonGeral.append(linhaJson)
        cont = cont + 1
    converterParastring(JsonGeral)

def converterParastring(lista):
    texto = ""
   
    cont = 0
    listaVaricoes = {}
    for linha in lista:
        if cont == 0:
            texto = texto + linha["tipo"]+ " \n"
        texto = texto + linha["empresa"] + " -> " + linha["cotacao"] + " -> " + linha["variacao"] + " \n"
        
        cont= cont + 1
        if cont == 5:
            cont = 0
            
    print(texto)
    
    file_object = codecs.open("infoEconocico.txt", "a", encoding="utf8")
    file_object.write(str(texto))
    file_object.write(u'\ufeff')
    file_object.close()

buscarDados()





 
