#!/usr/bin/env python
# coding: utf-8

# In[1]:


from itertools import permutations
import numpy as np
from tabulate import tabulate

def dvoi_zadacha(type_cabel, procedura, dvoi_left, dvoi_right, matrix, prib):
    for i in range(type_cabel+procedura):
        for j in range(procedura):
            dvoi_left[i][j]=matrix[j][i]
    for i in range(type_cabel+procedura):
        dvoi_right[i][0]=prib[i]

def search_answer(procedura, type_cabel, combination, matrix, fond, prib):
    none_combination = []

    for j in range(procedura+type_cabel):
        if j+1 not in combination:
            none_combination.append(j+1)

    table_for_answer = [[0] * (procedura+type_cabel+1)  for i in range (procedura+1)]
    #Заполнение единичной матрицы
    basis_znach_left = [[0] * (procedura)  for i in range (procedura)]
    basis_znach_right = [0]*(procedura)
    for i in range(procedura):
        for g in range(procedura):
            basis_znach_left[i][g]=matrix[i][combination[g]-1]
    for j in range(0,procedura+type_cabel+1):
        if j in combination:
            table_for_answer[combination.index(j)][j] += 1
        else:
            for i in range(procedura):
                if j == 0:
                    basis_znach_right[i]=fond[i]
                else:
                    basis_znach_right[i] = matrix[i][j-1]
            one_for_key = np.array([basis_znach_left[0]])
            two_for_key = np.array([basis_znach_right[0]])
            for i in range(1,procedura):
                one_for_key=np.vstack([one_for_key, basis_znach_left[i]])
                two_for_key=np.vstack([two_for_key, basis_znach_right[i]])
            key = np.linalg.solve(one_for_key, two_for_key)
            for i in range(procedura):
                table_for_answer[i][j] = float(key[i])
    combination=list(combination)
    doblicate=[[0]*(procedura+type_cabel+1) for i in range(procedura+1)]
    ci=np.array([prib[combination[0]-1]])
    for i in range(1,len(combination)):
        ci=np.vstack([ci, prib[combination[i]-1]])
    print(f'Значения базисных векторов в целевой функции: {ci}')
    for i in range(0,procedura+type_cabel+1):
        dinamic = np.array([table_for_answer[0][i]])
        for j in range(1, procedura):
            dinamic = np.vstack([dinamic, table_for_answer[j][i]])
        summ_dinamic = np.sum(ci * dinamic)-prib[i-1]
        table_for_answer[procedura][i] = summ_dinamic
    min_teta=0
    minimal_a_0=0
    iteration = 1
    print('После решений СЛАУ и нахождения базисных переменных получилась следующая таблица и базисы: \n')
    while minimal_a_0<=0 and min_teta!= '-':
        print(f'Итерация {iteration} \n  Таблица: \n',tabulate(table_for_answer, tablefmt="fancy_grid"))
        iteration += 1
        print('Индексы базисных векторов: \n', combination)
        for i in range(procedura+1):
            for j in range(procedura+type_cabel+1):
                doblicate[i][j]=table_for_answer[i][j]
        teta = ['-']*(procedura+type_cabel)
        minimal_a_0=0
        id_stolb=0
        id_strok=0
        for i in range(procedura):
            if table_for_answer[i][0] < minimal_a_0:
                minimal_a_0 = table_for_answer[i][0]
                id_strok=i
        if minimal_a_0 >= 0:
            break
        min_teta='-'
        for i in range(1,procedura+type_cabel+1):
            if table_for_answer[id_strok][i] < 0:
                teta[i-1] = -1 * table_for_answer[procedura][i]/table_for_answer[id_strok][i]
                if min_teta == '-':
                    min_teta = teta[i-1]
                    id_stolb = i
                elif min_teta > teta[i-1]:
                    min_teta = teta[i-1]
                    id_stolb = i
        if min_teta == '-':
            break
        izmena = np.array([table_for_answer[id_strok][0]])
        for j in range(1, procedura+type_cabel+1):
            izmena = np.vstack([izmena, table_for_answer[id_strok][j]])
        izmena = izmena/table_for_answer[id_strok][id_stolb]
        for j in range(procedura+type_cabel+1):
            if float(izmena[j])== -0.:
                table_for_answer[id_strok][j] = -float(izmena[j])
            else:
                table_for_answer[id_strok][j] = float(izmena[j])
        for i in range(procedura):
            for j in range(procedura+type_cabel+1):
                if i != id_strok:
                    table_for_answer[i][j]=-1*doblicate[i][id_stolb]*table_for_answer[id_strok][j]+doblicate[i][j]
        combination[id_strok]= id_stolb
        ci=np.array([prib[combination[0]-1]])
        for i in range(1,len(combination)):
            ci=np.vstack([ci, prib[combination[i]-1]])
        for i in range(0,procedura+type_cabel+1):
            dinamic = np.array([table_for_answer[0][i]])
            for j in range(1, procedura):
                dinamic = np.vstack([dinamic, table_for_answer[j][i]])
            summ_dinamic = np.sum(ci * dinamic)-prib[i-1]
            table_for_answer[procedura][i] = summ_dinamic
    if min_teta == '-':
        print('Решений нет')
    else:
        print(f'F={table_for_answer[procedura][0]}')
        for i in range(type_cabel+1):
            if i in combination:
                print(f'X{i}={round(table_for_answer[combination.index(i)][0],3)}')
    
type_cabel = int(input('Введите количество типов кабелей: '))
procedura = int(input('Введите количество процедур, производимых с кабелями: '))

matrix = [[0.0]*(type_cabel+procedura) for i in range(procedura)]
fond =[0.0]*(procedura)
for i in range(procedura):
    matrix[i][i+type_cabel] += 1
    for j in range (type_cabel+procedura):
        if j < type_cabel:
            matrix[i][j] = input(f'Введите количество времени, потраченное на {i+1} процедуру на 1 ед. кабеля {j+1}-ого типа:  ')
            if (matrix[i][j] == '-' or matrix[i][j] == ''):
                matrix[i][j] = '0'
            matrix[i][j] = float(matrix[i][j])
        if j == type_cabel-1:
            fond[i] = float(input(f'Введите, сколько по времени должна суммарно не превышать проведение {i+1} процедуры: '))
prib = [0.0]*(type_cabel+procedura)
for i in range (type_cabel+procedura):
    if i < type_cabel:
        prib[i] = input(f'Введите прибыль, которую можно получить за 1 км готового кабеля {i+1} типа кабеля: ')
        if (prib[i] == '-' or prib[i] == ''):
                prib[i] = '0'
        prib[i] = float(prib[i])
#Создание двойственной задачи
dvoi_left= [[0] * (procedura)  for i in range (type_cabel+procedura)]
dvoi_right = [[0] * (1)  for i in range (type_cabel+procedura)]
dvoi_zadacha(type_cabel, procedura, dvoi_left, dvoi_right, matrix, prib)

#Определение базиса
check_nalichie_combination = 0
spisok = [0]*(procedura+type_cabel)
for i in range (procedura+type_cabel):
    spisok[i]=i+1
spisok_combination = list(permutations(spisok, procedura))
for combination in spisok_combination:
    dvoi_matrix = np.array([dvoi_left[combination[0]-1]])
    dvoi_matrix_right = np.array([dvoi_right[combination[0]-1]])
    for i in range(1, len(combination)):
        dvoi_matrix = np.vstack([dvoi_matrix, dvoi_left[combination[i]-1]])
        dvoi_matrix_right = np.vstack([dvoi_matrix_right, dvoi_right[combination[i]-1]])
    if np.linalg.det(dvoi_matrix) != 0 and (np.linalg.matrix_rank(dvoi_matrix) == np.linalg.matrix_rank(np.hstack((dvoi_matrix, dvoi_matrix_right))) and np.linalg.matrix_rank(dvoi_matrix) == procedura):
        checker = np.linalg.solve(dvoi_matrix, dvoi_matrix_right)
        pol_checker = 0
        for j in range(0, len(checker)):
            if checker[j] >= 0:
                pol_checker += 1
        final_chek = 0
        if pol_checker == len(checker):
            for number in spisok:
                if number not in combination:
                    proverka = np.array([dvoi_left[number-1]])
                    if np.sum(proverka*checker) < dvoi_right[number-1]:
                        break
                    else:
                        final_chek += 1
        if final_chek == len(spisok) - procedura:
            check_nalichie_combination += 1
            break
if check_nalichie_combination == 1:
    search_answer(procedura, type_cabel, combination, matrix, fond, prib)
else:
    print("Сопряжённый базис не может быть найден. Решения нет")


# 
# 

# In[ ]:





# In[ ]:





# In[ ]:




