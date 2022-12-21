import os 
import re
os.system("cls")

pasta = os.path.abspath(".")
a =  'PLANTA-vp-Térreo-465-Fulvio.jpg'

padrao_nome_planta = re.compile('^( )*(Planta|planta|PLANTA)-(vp|VP|Vp)-[\w\W]{3,40}-[\d]{3}-[\w\W]+\.(jpg|png|pdf)$')
padrao_nome_pasta_df = re.complie('^(VIGAS)_(E)_(PILARES)_[\d]{3}')

b = a.split('.')
info_nome = b[0].split("-")
info_nome = list(map(lambda x: x.strip(), info_nome))

pavimento = info_nome[2]
n_obra = info_nome[3]
nome_cliente = info_nome[4]


def percorrer_pasta(pasta):
    
    lista_arquivos = os.listdir(pasta)
    for arquivo in lista_arquivos:
        if re.match(padrao_nome_planta, arquivo):
            print(arquivo)

percorrer_pasta(pasta)
    
    #for arquivo in lista_arquivos:
        #if not re.match()

#[A-Z] nos padroes nao aceita acentos 


 #padrao para nome das fotos
#padrao = re.match(padrao_nome_planta, a)
#print(padrao)





