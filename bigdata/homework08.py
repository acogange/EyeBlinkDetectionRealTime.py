num_list=[[1,4,7],[2,5,8],[3,6,9]]  #리스트 정의
new_list=[[int(0) for i in range(3) ]for j in range(3)] #같은 크기의 리스트 초기화

def transpose_list(list_a,list_b):  #힘수
    for i in range(3):
        for j in range(3):
            list_b[j][i]=list_a[i][j]
    return list_b       #전치행렬 반환

list3=transpose_list(num_list,new_list) #함수 실행

print(list3)