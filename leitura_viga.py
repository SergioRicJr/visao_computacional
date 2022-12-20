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



class planta_vigapilar:
  def __init__(self, caminho_img):
    self.n_obra = input('Digite o número da obra: ')
    self.n_cliente = input('Digite o nome do cliente: ')
    self.pavimento = input('escreva o pavimento: ')
    self.caminho_img = caminho_img
    self.vigas_tam = []
    self.vigas_nome = []
    self.v_x = []
    self.v_y = []
    self.exre = {  
        'p_nome_1': '^(V|v)[0-9]{1}',
        'p_nome_2': '^(V|v)[0-9]{2}',
        'p_vep':'^[0-9]{2}(x|X)[0-9]{2}$',
        'p_vep_colado': '[0-9]{2}(x|X)[0-9]{2}',
        'p_nome_viga':  '^(V|v)[0-9]{1,2}$',
        'p_nome_viga_colado': '(V|v)[0-9]{1,2}',
        'p_nome_viga_completo': '^(V|v)[0-9]{1,2}[0-9]{2}(x|X)[0-9]{2}$'
    }
    self.min_conf = 0
  
  def iniciar_processo(self):
    self.carregar_imagem()
    self.ler_imagem(self.img)
    self.add_info_list(self.resultado)
    self.muda_lado_90()
    self.ler_imagem(self.img_virada)
    self.add_info_list(self.resultado)
    self.dividir_tam_viga()
    self.criar_df()
    self.ordem_df()
    self.exportar_df()

  def carregar_imagem(self):
    self.img = cv2.imread(self.caminho_img)
  
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

#adicionar funcao para pegar nome do pavimento automaticamente
#adicionar funcao para criar pasta e guardar excel de vigas e pilares de cada obra
  def exportar_df(self):
    self.df.to_excel(f"vigas_{self.pavimento}_{self.n_obra}_{self.n_cliente}.xlsx", index=False)
  #criar pasta caso n exista baseado no nome e guardar arquivo, mudar nome da foto para isso 



#caminho_imagem = "PROJETO MONTAGEM FULVIO 4k final.jpg"
#planta = planta_vigapilar(caminho_imagem)
#planta.iniciar_processo()