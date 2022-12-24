import os
os.system('cls')
import re
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd
import pytesseract
from pytesseract import Output
import numpy as np
import cv2 
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe" 
#arrumar caminho tesseract dependendo do computador

padrao_n_planta = re.compile('(Planta|planta|PLANTA)-(vp|VP|Vp)-[\w\W]{3,40}-[\d]{3}-[\w\W]+\.(jpg|png|pdf)')
#a = re.finditer(padrao_n_planta, caminho)
#nome_arquivo = []
#for i in a:
    #nome_arquivo.append(i[0])



class planta_vigapilar:
  def __init__(self):
    self.vigas_tam = []
    self.vigas_nome = []
    self.v_x = []
    self.v_y = []
    self.exre = {
        'padrao_nome_planta_2': '^(Planta|planta|PLANTA)-(vp|VP|Vp)-[\w\W]{3,40}-[\d]{3}-[\w\W]+\.(jpg|png|pdf)$',
        'padrao_nao_pastas': '^[\w\W]+\.[A-Za-z]+$',
        'padrao_nome_excel_generico': '^vigas_[A-Za-zÀ-Úà-ú]+[0-9]?_[0-9]{3}_[A-Za-zÀ-Úà-ú]+\.xlsx$',
        'padrao_n_planta': '(Planta|planta|PLANTA)-(vp|VP|Vp)-[\w\W]{3,40}-[\d]{3}-[\w\W]+\.(jpg|png|pdf)',
        'p_nome_1': '^(V|v)[0-9]{1}',
        'p_nome_2': '^(V|v)[0-9]{2}',
        'p_vep':'^[0-9]{2}(x|X)[0-9]{2}$',
        'p_vep_colado': '[0-9]{2}(x|X)[0-9]{2}',
        'p_nome_viga':  '^(V|v)[0-9]{1,2}$',
        'p_nome_viga_colado': '(V|v)[0-9]{1,2}',
        'p_nome_viga_completo': '^(V|v)[0-9]{1,2}[0-9]{2}(x|X)[0-9]{2}$'
    }
    self.min_conf = 0
    self.lista_excel_pronto = []
    self.lista_arquivos = os.listdir(os.getcwd())
  
  def iniciar_processo_individual(self):
    self.carregar_imagem()
    self.ler_imagem(self.img)
    self.add_info_list(self.resultado)
    self.muda_lado_90()
    self.ler_imagem(self.img_virada)
    self.add_info_list(self.resultado)
    self.dividir_tam_viga()
    self.informacoes_nome()
    self.criar_df()
    self.ordem_df()
    self.exportar_df()

  def ler_plantas_automaticamente(self):
    self.listar_arquivos_prontos(os.getcwd())
    self.lista_arquivos = os.listdir(os.getcwd())
    for arquivo in self.lista_arquivos:
        self.vigas_tam = []
        self.vigas_nome = []
        self.v_x = []
        self.v_y = []
        if re.match(self.exre['padrao_nome_planta_2'], arquivo):
            a =  arquivo
            b = a.split('.')
            info_nome = b[0].split("-")
            info_nome = list(map(lambda x: x.strip(), info_nome))
            pavimento = info_nome[2]
            n_obra = info_nome[3]
            nome_cliente = info_nome[4]
            if f'vigas_{pavimento}_{n_obra}_{nome_cliente}.xlsx' not in self.lista_excel_pronto:
                self.caminho_img = arquivo
                self.img = cv2.imread(self.caminho_img)
                self.ler_imagem(self.img)
                self.add_info_list(self.resultado)
                self.muda_lado_90()
                self.ler_imagem(self.img_virada)
                self.add_info_list(self.resultado)
                self.dividir_tam_viga()
                self.informacoes_nome()
                self.criar_df()
                self.ordem_df()
                self.exportar_df()
                #if f"VIGAS_E_PILARES_{n_obra}_{nome_cliente.upper()}" not in self.lista_arquivos:
                  #os.mkdir(f'C:/Users/sergi/visao_computacional/VIGAS_E_PILARES_{n_obra}_{nome_cliente.upper()}')
                #os.rename(f'vigas_{pavimento}_{n_obra}_{nome_cliente}.xlsx', f'VIGAS_E_PILARES_{n_obra}_{nome_cliente}/vigas_{pavimento}_{n_obra}_{nome_cliente}.xlsx')   
                #os.rename(f'Planta-vp-{pavimento}-{n_obra}-{nome_cliente}.jpg', f'VIGAS_E_PILARES_{n_obra}_{nome_cliente}/Planta-vp-{pavimento}-{n_obra}-{nome_cliente}.jpg')
  
  def carregar_imagem(self):
    self.caminho_img = input('Digite o nome da imagem: ')
    self.img = cv2.imread(self.caminho_img)
  
  def informacoes_nome(self):
    a = re.finditer(padrao_n_planta, self.caminho_img)
    for i in a:
      self.nome_imagem = i[0]  
    b = self.nome_imagem.split('.')
    info_nome = b[0].split("-")
    info_nome = list(map(lambda x: x.strip(), info_nome))
    self.pavimento = info_nome[2]
    self.n_obra = info_nome[3]
    self.nome_cliente = info_nome[4]
  
  def ler_imagem(self, img):
    self.config = r'--psm 11'
    self.resultado = pytesseract.image_to_data(img, lang='por', config=self.config, output_type=Output.DICT)   
  
  def muda_lado_90(self):
    img_pil = Image.fromarray(self.img)
    img_pil = img_pil.rotate(-90)
    img_virada = np.array(img_pil)
    self.img_virada = img_virada
  
  def add_info_list(self, resultado): #adicionar tratamento de erro p viga com 3 caracteres colado ou solto apos 'V'
    for i in range(len(resultado['text'])): 
      if float(resultado['conf'][i]) > self.min_conf:
        resultado['text'][i] = resultado['text'][i].strip()
        if i == 0:
          if re.match(self.exre["p_nome_viga"], resultado['text'][i]) and re.match(self.exre["p_vep"], resultado['text'][i+1]):
            self.vigas_nome.append(resultado['text'][i])
        elif i == len(resultado['text'])-1:
          if re.match(self.exre["p_vep"], resultado['text'][i]) and re.match(self.exre["p_nome_viga"], resultado['text'][i-1]):
            self.vigas_tam.append(resultado['text'][i])
        elif i !=0 and i != len(resultado['text']) - 1:
          if re.match(self.exre["p_nome_viga"], resultado['text'][i]) and re.match(self.exre["p_vep"], resultado['text'][i+1]):
            self.vigas_nome.append(resultado['text'][i])
          elif re.match(self.exre["p_vep"], resultado['text'][i]) and re.match(self.exre["p_nome_viga"], resultado['text'][i-1]):
            self.vigas_tam.append(resultado['text'][i])
        if re.match(self.exre["p_nome_viga_completo"], resultado['text'][i]):
          a = re.search(self.exre["p_vep_colado"], resultado['text'][i])
          self.vigas_tam.append(a[0])
          b = re.search(self.exre["p_nome_1"], resultado['text'][i]) if len(resultado['text'][i]) == 7 else re.search(self.exre["p_nome_2"], resultado['text'][i])
          self.vigas_nome.append(b[0])

  def dividir_tam_viga(self):
    for i in range(len(self.vigas_tam)):
      vt = self.vigas_tam[i].strip()
      if re.match(self.exre["p_vep"], vt):
        a = re.split('[X|x]', vt)
        self.v_x.append(a[0])
        self.v_y.append(a[1])

  def criar_df(self):
    vigas = {'Viga': self.vigas_nome, 'X': self.v_x, 'Y': self.v_y}
    self.df = pd.DataFrame(vigas)

  def ordem_df(self):
    self.df['sort'] = self.df['Viga'].apply(lambda x: x[1:]).astype(int)
    self.df.sort_values('sort', inplace=True)
    self.df.drop(['sort'], axis=1, inplace=True)
    self.df.drop_duplicates(inplace=True)
    self.df.reset_index(drop=True, inplace=True)


  def exportar_df(self): #implementar regex em todos os exemplos para melhorar tratamento de erros == urgente
    self.df.to_excel(f"vigas_{self.pavimento}_{self.n_obra}_{self.nome_cliente}.xlsx", index=False)
    if f"VIGAS_E_PILARES_{self.n_obra}_{self.nome_cliente.upper()}" not in self.lista_arquivos:
      os.mkdir(f'C:/Users/sergi/visao_computacional/VIGAS_E_PILARES_{self.n_obra}_{self.nome_cliente.upper()}')
    os.rename(f'vigas_{self.pavimento}_{self.n_obra}_{self.nome_cliente}.xlsx', f'VIGAS_E_PILARES_{self.n_obra}_{self.nome_cliente}/vigas_{self.pavimento}_{self.n_obra}_{self.nome_cliente}.xlsx')   
    os.rename(f'Planta-vp-{self.pavimento}-{self.n_obra}-{self.nome_cliente}.jpg', f'VIGAS_E_PILARES_{self.n_obra}_{self.nome_cliente}/Planta-vp-{self.pavimento}-{self.n_obra}-{self.nome_cliente}.jpg') 

  def listar_arquivos_prontos(self, pasta):
    self.lista_arquivos = os.listdir(pasta)
    for arquivo in self.lista_arquivos:
        if not re.match(self.exre['padrao_nao_pastas'], arquivo) and arquivo != '.git':
            self.listar_arquivos_prontos(arquivo)
        if re.match(self.exre['padrao_nome_excel_generico'], arquivo):
            self.lista_excel_pronto.append(arquivo)


#caminho_imagem = r"C:\Users\sergi\visao_computacional\Planta-vp-Terreo-465-Fulvio.jpg"
planta = planta_vigapilar()
#planta.carregar_imagem()
#planta.listar_arquivos_prontos(os.getcwd())
#print(planta.lista_excel_pronto)
#planta.iniciar_processo_individual()
planta.ler_plantas_automaticamente()




#pasta = os.getcwd()
#planta.listar_arquivos_prontos(pasta)
#print(planta.lista_excel_pronto)