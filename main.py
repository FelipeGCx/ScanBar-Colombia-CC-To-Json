# %%
from PIL import Image as PIL
from pdf417decoder import PDF417Decoder
import json
from localSites import *

def is_number(s):
  try:
    float(s)
    return True
  except ValueError:
    return False

def decode(image_name):
  image = PIL.open(image_name)
  decoder = PDF417Decoder(image)

  if (decoder.decode() > 0):
    decoded = decoder.barcode_data_index_to_string(0)
    data_set = setData(decoded)
    data_dict = setDataInDict(data_set)
    createJSON(data_dict)
  else:
    print('No fue posible decodificar la imagen')  

def setData(decoded):
  dec = decoded.split('\x00')
  dec.remove('PubDSK_1')
  data = []
  for i in dec:
    if i != '':
      data.append(i)
  cc = ''
  lastname = ''
  if len(data[1]) > 6:
      for i in data[1]:
          if is_number(i):
              cc += i
          else:
              lastname += i
      a = len(cc)-10
      b = len(cc)
      n = cc[0:a]
      cc = cc[a:b]
      cc = cc + lastname
      data.pop(1)
      data.insert(1, n)
      data.insert(2, cc)
  cc = ''
  lastname = ''
  for i in data[2]:
      if is_number(i):
          cc += i
      else:
          lastname += i
  data.pop(2)
  data.insert(2, lastname)
  data.insert(2, cc)
  return data

def setDataInDict(data):
  flag = False
  if len(data) < 13:
      flag = True
      data.insert(6, '')

  Genero = (data[7])[1]
  FechaNacimiento = f'{(data[7])[2:6]}-{(data[7])[6:8]}-{(data[7])[8:10]}'
  Departamento = (data[7])[10:12]
  Ciudad = (data[7])[12:15]
  RH = (data[7])[16:18]
  AfisCode = (data[0])[2:len(data[0])]
  FingerCard = data[1]
  NumeroDocumento = data[2]
  Apellidos = f'{data[3]} {data[4]}'
  if flag:
      Nombres = data[5]
  else:
      Nombres = f'{data[5]} {data[6]}'

  siteInfo = Search(Departamento, Ciudad)
  Departamento = siteInfo[0]
  Ciudad = siteInfo[1]

  final_data = {
      "AfisCode": AfisCode,
      "Cedula": NumeroDocumento,
      "Nombres": Nombres,
      "Apellidos": Apellidos,
      "FechaDeNacimiento": FechaNacimiento,
      "CiudadDeNacimiento": Ciudad,
      "DepartamentoDeNacimiento": Departamento,
      "TipoDeSangre": RH,
      "Genero": 'Femenino' if (Genero == 'F') else 'Masculino'
  }
  return final_data

def createJSON(final_data):
  with open(f"{final_data['Cedula']}.json", "w") as write_file:
    json.dump(final_data, write_file)

image = "barcode4_2.jpg"
decode(image)

# %%
