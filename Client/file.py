import json

'''
Faz a leitura do aquivo json e retorna as informações que contém indicando o caminho do arquivo.
'''
def read(_path):
    with open(_path, encoding='utf-8') as r_json:
        data = json.load(r_json)
        return data

'''
 Faz a escrita no arquivo especificando os dados a serem escritos e o caminho do arquivo 
'''     
def write(data, _path):
    with open(_path, 'w') as json_file:
        json.dump(data, json_file)
        

