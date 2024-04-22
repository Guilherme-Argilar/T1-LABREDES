#script adicional usado para gerar arquivos de teste de envio de arquivos
import os
import random

file_size = 4000
file_name = "./teste/arquivo_teste_{}_bytes.txt".format(file_size)

# Gerar dados aleatórios usando apenas caracteres ASCII imprimíveis
random_data = ''.join(chr(random.randint(32, 126)) for _ in range(file_size)).encode('ascii')

with open(file_name, "wb") as file:
    file.write(random_data)

file_name
