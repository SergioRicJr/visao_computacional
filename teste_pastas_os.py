import os 
import re
from leitura_viga import *
os.system("cls")

pasta = os.path.abspath(".") #dá no mesmo
pasta = os.getcwd() #mesma coisa

a =  'PLANTA-vp-Térreo-465-Fulvio.jpg'
b = a.split('.')
info_nome = b[0].split("-")
info_nome = list(map(lambda x: x.strip(), info_nome))

pavimento = info_nome[2]
n_obra = info_nome[3]
nome_cliente = info_nome[4]

nome_pasta = 'VIGAS_E_PILARES_465_FULVIO'

padrao_nome_da_pasta_vdd = re.compile(f'^(VIGAS_E_PILARES)_({n_obra})_({nome_cliente.upper()}|{nome_cliente.lower}|{nome_cliente})')

a = re.match(padrao_nome_da_pasta_vdd, nome_pasta)




padrao_nome_planta = re.compile('^( )*(Planta|planta|PLANTA)-(vp|VP|Vp)-[\w\W]{3,40}-[\d]{3}-[\w\W]+\.(jpg|png|pdf)$')
padrao_nome_pasta_df = re.compile('^(VIGAS)_(E)_(PILARES)_[\d]{3}')

padrao_nome_planta_2 = re.compile('(Planta|planta|PLANTA)-(vp|VP|Vp)-[\w\W]{3,40}-[\d]{3}-[\w\W]+\.(jpg|png|pdf)')

def percorrer_pasta(pasta):
    lista_arquivos = os.listdir(pasta)
    for arquivo in lista_arquivos:
        if re.match(padrao_nome_planta, arquivo):
            planta = planta_vigapilar(arquivo)
            planta.iniciar_processo()
        

            

#percorrer_pasta(pasta)
    
    #for arquivo in lista_arquivos:
        #if not re.match()

#[A-Z] nos padroes nao aceita acentos 


 #padrao para nome das fotos
#padrao = re.match(padrao_nome_planta, a)
#print(padrao)





#caminho = 'C:\\Users\\sergi\\visao_computacional\\Planta-vp-Térreo-465-Fulvio.jpg'

#a = re.finditer(padrao_nome_planta_2, caminho)


#for i in a:
    #nome_arquivo = i[0]
#print(nome_arquivo)