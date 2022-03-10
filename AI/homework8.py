import pickle
import os.path

with open('Date.txt','r') as file:  #데이터 읽어오기
    list=file.read()

with open("Date.bin","wb") as FileOut:  #이진파일에 쓰기
    pickle.dump(list,FileOut)

with open('Date.bin','rb') as FileIn:   #이진파일 읽기
    data_list=pickle.load(FileIn)

print(data_list)    #출력