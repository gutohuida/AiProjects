def writeincsv(arq,content):
    with open(arq, 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        for line in content:
            wr.writerow([line])

import pandas as pd
import csv
import subprocess as sp
tmp = sp.call('clear',shell=True)
filename = input("Entre com o caminho do arquivo: ")
#"C:\\Users\\92007848\\Documents\\AIProj\\AiTeste\\Resourses\\Files\\DataSets\\LogicaDeProg\\Original\\LP.xlsx"
data = pd.read_excel(filename, sheet_name="Planilha2")

tutorias = []
adm = []
outras = []
count = 1
for line in data['PERGUNTA/RESPOSTA']:
    tmp = sp.call('clear',shell=True)
    print('Digite 1 para tutorias de duvidas')
    print('Digite 2 para tutorias administrativas')
    print('Digite qualquer outro valor para pular a tutoria')
    print('Digite 9 para encerrar')
    print()
    print()
    print('Tutoria ',count)
    print(line)
    print()
    option = input("Qual o tipo da tutoria? ")
    
    if(option == '1'):
        tutorias.append(line) 
    elif(option == '2'):
        adm.append(line)
    elif(option == '9'):
        break
    else:
        outras.append(line)
    count += 1


writeincsv('Duvidas.csv',tutorias)
writeincsv('Adm.csv',adm)
writeincsv('Outras.csv',outras)

