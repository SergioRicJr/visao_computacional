import re
import pandas as pd
import os
os.system('cls')

#CANCELAR TRATAMENTO DE ERRO DE NOME DE IMAGEM, DEIXAR SO ADICIONAR



# padrao_nao_pastas = '^[\w\W]+\.[A-Za-z]+$',
# padrao_nome_excel_generico = '^vigas_[A-Za-zÀ-Úà-ú_]+[0-9]?_[0-9]{3}_[A-Za-zÀ-Úà-ú]+\.xlsx$'

# nome = 'vigas_TERREO_CASA_475_JORGE.xlsx'
# print(re.match(padrao_nome_excel_generico, nome))


# def listar_arquivos_prontos(self, pasta):
#     self.lista_arquivos = os.listdir(pasta)
#     for arquivo in self.lista_arquivos:
#         if not re.match(self.exre['padrao_nao_pastas'], arquivo) and arquivo != '.git':
#             self.listar_arquivos_prontos(arquivo)
#         if re.match(self.exre['padrao_nome_excel_generico'], arquivo):
#             self.lista_excel_pronto.append(arquivo)
# dic = [['V82', '14', '25'], ['V76', '14', '25'], ['V55', '14', '25']]
# df = pd.DataFrame(dic)

# # for i in df['Vigas']:
# #     print(i)

# # with open("vigas_superior_472_carlos.xlsx", "r+") as arq:
# #     for i in dic: isso corrompe arquivo excel.
# #         for x in i:    
# #             print(x)
# #             arq.write(x)

# with pd.ExcelWriter("vigas_superior_472_carlos.xlsx", engine='openpyxl',mode='a', if_sheet_exists='overlay') as writer: 
#     df.to_excel(writer, sheet_name='Sheet1', startrow=writer.sheets["Sheet1"].max_row, index=False, header=False)

# # with pd.ExcelWriter("test.xlsx", engine='openpyxl', mode='a') as writer:
#     df.to_excel(writer)


# with pd.ExcelWriter("existing_file_name.xlsx", engine="openpyxl", mode="a") as writer:
#     df.to_excel(writer, sheet_name="name", startrow=num, startcol=num)

# writer = pd.ExcelWriter('vigas_superior_472_carlos.xlsx', engine='xlsxwriter', mode='a', if_sheet_exists='overlay' )
# df.to_excel(writer, sheet_name="F1", startrow=writer.sheets["F1"].max_row, index=False, header=False)


# RE funciona com f string?
tt = 'TERREO'

n_pattern = f'vigas_{tt}[0-9]?_[0-9]{{3}}'#[0-9]'#+'_[0-9]{3}_[A-Za-zÀ-Úà-ú]+\.xlsx'
padrao_nome_excel_generico = re.compile(n_pattern)
# print(n_pattern)

nome = 'vigas_TERREO_475_JORGE.xlsx'

pavimento = 'terreo'

numero_foto_obra = '2'
n_obra = '465'
nome_cliente = 'fulvio'


padrao_n_planta_correto = f'(Planta|planta|PLANTA)-(vp|VP|Vp)-{pavimento}({numero_foto_obra})?-{n_obra}-{nome_cliente}\.(jpg|png|pdf)'
padrao_n_planta_corr = f'(Planta|planta|PLANTA)-(vp|VP|Vp)-{pavimento}-{n_obra}-{nome_cliente}\.(jpg|png|pdf)'
#padrao_n_planta_correto = f'(Planta|planta|PLANTA)-(vp|VP|Vp)-terreo2-465-fulvio\.(jpg|png|pdf)'

lista_de_imagens_em_pasta = ['planta-vp-terreo2-465-fulvio.jpg','planta-vp-terreo2-465-fulvio.jpg', 'planta-vp-terreo-465-fulvio.jpg','Planta-vp-terreo-465-fulvio.jpg', 'planta-vp-terreo-465-fulvio.jpg' ]
#lista_de_imagens_em_pasta = []
junto = str(lista_de_imagens_em_pasta).strip('[]')
junto = re.sub("[',]", " ",junto)
print(junto)
#lista_de_imagens_em_pasta = []
qtde = 0
for i in lista_de_imagens_em_pasta:
    a = re.match(padrao_n_planta_correto, i)
    if a != None:
        qtde +=1
    print(a)
print(qtde)
# qtde = 0
# print(a)
    
        
#     qtde += 1
# print(qtde)




# def essaaqui():
#     a = re.finditer(padrao_n_planta_corr, junto)
#     qtde_sem = 0
#     for i in a:
#         print(i[0])
#         qtde_sem += 1
#     print(qtde_sem)
#     if qtde_sem >1:
#         print('esse arquivo já existe na pasta')
#         exit() #funciona
#     print('oi')
#     print('ainda estou aqui')

# essaaqui()


# padrao_n_planta = re.compile('(Planta|planta|PLANTA)-(vp|VP|Vp)-[\w\W_]{3,40}-[\d]{3}-[\w\W]+\.(jpg|png|pdf)')
# padrao_n_planta_cnumero = '(Planta|planta|PLANTA)-(vp|VP|Vp)-[\w\W_]{3,40}[0-9]{1}-[\d]{3}-[\w\W]+\.(jpg|png|pdf)'

# caminho_img = "planta-vp-superior2-472-carlos.jpg"
# a = re.finditer(padrao_n_planta, caminho_img)
# for i in a:
#     nome_imagem = i[0]
#     b = nome_imagem.split('.')
#     info_nome = b[0].split("-")
#     info_nome = list(map(lambda x: x.strip(), info_nome))
#     #padrao_nome_planta_cnumero = '(Planta|planta|PLANTA)-(vp|VP|Vp)-[\w\W_]{3,40}[0-9]{1}-[\d]{3}-[\w\W]+\.(jpg|png|pdf)'
#     pavimento = info_nome[2]
#     n_obra = info_nome[3]
#     nome_cliente = info_nome[4]
#     if re.match('[\w\W_]{3,40}[0-9]{1}', info_nome[2]):
#         numero_foto_obra = pavimento[-1]
#         pavimento = pavimento[:-1]

#print(pavimento, n_obra, nome_cliente, numero_foto_obra, sep='\n')
