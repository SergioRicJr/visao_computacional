import re

padrao_nao_pastas = '^[\w\W]+\.[A-Za-z]+$',
padrao_nome_excel_generico = '^vigas_[A-Za-zÀ-Úà-ú_]+[0-9]?_[0-9]{3}_[A-Za-zÀ-Úà-ú]+\.xlsx$'

nome = 'vigas_TERREO_CASA_475_JORGE.xlsx'
print(re.match(padrao_nome_excel_generico, nome))


# def listar_arquivos_prontos(self, pasta):
#     self.lista_arquivos = os.listdir(pasta)
#     for arquivo in self.lista_arquivos:
#         if not re.match(self.exre['padrao_nao_pastas'], arquivo) and arquivo != '.git':
#             self.listar_arquivos_prontos(arquivo)
#         if re.match(self.exre['padrao_nome_excel_generico'], arquivo):
#             self.lista_excel_pronto.append(arquivo)