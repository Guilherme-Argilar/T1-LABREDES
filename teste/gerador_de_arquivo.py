import os

file_size = 1200
file_name = f"./teste/arquivo_teste_{file_size}_bytes.txt"

random_data = os.urandom(file_size)

with open(file_name, "wb") as file:
    file.write(random_data)

file_name
