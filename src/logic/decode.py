import sys
sys.path.append("./src")
from logic.sites import search_site
from pdf417decoder import PDF417Decoder
from PIL import Image 
import json

class Decode:
    def __init__(self, image_name):
        self.image_name = image_name
        global api
        api = API()

    def run(self):
        api.decode(self.image_name)

class API:
    
    def decode(self,image_name):
        # open the image
        image = Image.open(image_name)
        # decode the image
        image_decoded = PDF417Decoder(image)
        # if the image is decoded
        if (image_decoded.decode() > 0):
            # get the decoded data
            decoded_string = image_decoded.barcode_data_index_to_string(0)
            # print the decoded data including the null characters
                # std=[]
                # for st in decoded_string:
                #     std.append(st)
                # print(std)
            # serialize the data
            data_serialized = self.serialize_data(decoded_string)
            data_dict = self.parse_data_to_dict(data_serialized)
            self.create_json(data_dict)
        else:
            print('We could not decode the image')  

    def serialize_data(self, data):
        data_split = data.split('\x00')
        data_split.remove('PubDSK_1')
        response = []
        for i in data_split:
            if i != '':
                response.append(i)
        cc = ''
        lastname = ''
        if len(response[1]) > 6:
            for i in response[1]:
                if self.is_number(i):
                    cc += i
                else:
                    lastname += i
            a = len(cc)-10
            b = len(cc)
            n = cc[0:a]
            cc = cc[a:b]
            cc = cc + lastname
            response.pop(1)
            response.insert(1, n)
            response.insert(2, cc)
        cc = ''
        lastname = ''
        for i in response[2]:
            if self.is_number(i):
                cc += i
            else:
                lastname += i
        response.pop(2)
        response.insert(2, lastname)
        response.insert(2, cc)
        return response

    def parse_data_to_dict(self, data):
        flag = False
        if len(data) < 13:
            flag = True
            data.insert(6, '')
        gender = (data[7])[1]
        data_of_birth = f'{(data[7])[2:6]}-{(data[7])[6:8]}-{(data[7])[8:10]}'
        departament = (data[7])[10:12]
        municipality = (data[7])[12:15]
        blood_type_rh = (data[7])[16:18]
        afis_code = (data[0])[2:len(data[0])]
        finger_card = data[1]
        document_id = data[2]
        last_name = f'{data[3]} {data[4]}'
        if flag:
            first_name = data[5]
        else:
            first_name = f'{data[5]} {data[6]}'
        site_answer = search_site(departament, municipality)
        departament = site_answer['departament']
        municipality = site_answer['municipality']
        final_data = {
            "afisCode": f'00{afis_code}',
            "cedula": document_id,
            "nombres": first_name,
            "apellidos": last_name,
            "fechaDeNacimiento": data_of_birth,
            "lugarDeNacimiento": municipality,
            "departamentoDeNacimiento": departament,
            "grupoSanguineoRH": blood_type_rh,
            "sexo": 'Femenino' if (gender == 'F') else 'Masculino'
        }
        return final_data 

    def is_number(self,value):
        try:
            float(value)
            return True
        except ValueError:
            return False
    
    def create_json(self, data, directory='src/exports'):
        with open(f"{directory}/{data['cedula']}.json", "w") as write_file:
            json.dump(data, write_file, indent=4)
