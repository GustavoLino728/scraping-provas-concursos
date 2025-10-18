import requests
import csv
import os
from bs4 import BeautifulSoup
from unidecode import unidecode


def normalizar_banca(banca):
    """Limpa o input do usuario para que possa chegar no padrão das urls utilizadas pelo site"""
    banca_sem_acento = unidecode(banca)
    banca_lower = banca_sem_acento.lower()
    banca_normalizada = banca_lower.replace(' ', '-')
    banca_normalizada = ''.join(c for c in banca_normalizada if c.isalnum() or c == '-')
    return banca_normalizada

def decidir_banca():
    """Recebe o input do usuario e o retorna para montar a url que será raspada"""
    banca = 1
    while banca != '0':
        os.system("cls")
        print("-----------------------------------")
        print("Seja bem vindo ao Seletor de Provas de Concursos, aqui você irá poder ter acesso a todas as provas feitas por uma banca escolhida e com o assunto que você desejar")
        print("Consulte: [https://www.pciconcursos.com.br/organizadoras/] para ter acesso a lista de bancas que estão disponiveis")
        print("Aperte CNTRL+C para encerrar o programa")
        print("-----------------------------------")
        
        banca = input("Digite a banca desejada: ")
        
        banca_normalizada = normalizar_banca(banca)
        print(f"Banca normalizada: {banca_normalizada}")
            
        return banca_normalizada
    
def extrair_provas_banca_nivel_superior():
    """Extrai do site todas as ocorrencias de provas da banca inputada pelo usuario e devolve um dicionario para ser salvo como csv"""
    banca = decidir_banca()
    base_url = f"https://www.pciconcursos.com.br/provas/{banca}"
    pagina = 1
    provas = []

    while True:
        url = base_url if pagina == 1 else f"{base_url}/{pagina}"
        print(f"Buscando: {url}")
        response = requests.get(url)
        if response.status_code != 200:
            print("Erro ao acessar página ou fim das páginas.")
            break
        
        soup = BeautifulSoup(response.text, 'html.parser')
        tabela = soup.find('table', {'id': 'lista_provas'})
        if not tabela:
            print("Tabela não encontrada, fim das páginas.")
            break
        
        linhas = tabela.find_all('tr')[1:]
        if not linhas:
            print("Sem mais provas, fim da paginação.")
            break

        encontrou_superior = False
        for linha in linhas:
            colunas = linha.find_all('td')
            nivel = colunas[4].text.strip()
            if nivel == "Superior":
                encontrou_superior = True
                titulo = colunas[0].text.strip()
                link = colunas[0].find('a').get('href', '').strip()
                ano = colunas[1].text.strip()
                orgao = colunas[2].text.strip()
                instituicao = colunas[3].text.strip()
                
                provas.append({
                    "titulo": titulo,
                    "ano": ano,
                    "orgao": orgao,
                    "instituicao": instituicao,
                    "nivel": nivel,
                    "link": link
                })
        
        if not encontrou_superior:
            print("Nenhuma prova de nível superior nesta página, finalizando.")
            break
        
        pagina += 1

    print(f"Total de provas nível superior encontradas: {len(provas)}")
    return provas

def salvar_como_csv(provas, filename='provas_banca_superior.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["titulo", "ano", "orgao", "instituicao", "nivel", "link"])
        writer.writeheader()
        for prova in provas:
            writer.writerow(prova)
    print(f"Arquivo CSV '{filename}' criado com sucesso.")