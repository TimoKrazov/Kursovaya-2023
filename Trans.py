#!/usr/bin/env python
# coding: utf-8

# In[80]:


from tabulate import tabulate

def fictiv_szu(a, b):
    fictiv = sum(a) - sum(b)
    if fictiv > 0:
        b.append(fictiv)
    elif fictiv < 0:
        a.append(abs(fictiv))
    print('Посмотрим, соответствует ли количество запасов, количеству потребностей:')
    if fictiv > 0:
        print(f'Запасы превышают кол-во потребностей товара на складе на {abs(fictiv)} единиц груза, поэтому введём фиктивный склад')
    elif fictiv < 0:
        print(f'Склады запрашивают больше товара,чем имеется на {abs(fictiv)} единиц груза, поэтому введём фиктивную базу')
    else: 
        print(f'Количество запрашиваемого груза удовлетворяет количеству его наличия')

def first_virod(a, b, right_peremena, down_peremena, opor_plan, answer_user):
    if a[down_peremena] == 0 and b[right_peremena] == 0:
        if right_peremena != len(b)-1:
            opor_plan[down_peremena][right_peremena + 1] = 0.0001
            if answer_user == "Y":
                print("Чтобы опорный план не был вырожденным, сразу добавим значение равное 0.0001")
        elif down_peremena != len(a) - 1:
            opor_plan[down_peremena + 1][right_peremena] = 0.0001
            if answer_user == "Y":
                print("Чтобы опорный план не был вырожденным, сразу добавим значение равное 0.0001")

def szu(opor_plan, a, b, answer_user):
    right_peremena = 0
    down_peremena = 0
    while right_peremena < len(b) or down_peremena < len(a):
        minimal = min(a[down_peremena], b[right_peremena])
        a[down_peremena] -= minimal
        b[right_peremena] -= minimal
        opor_plan[down_peremena][right_peremena] += minimal
        first_virod(a, b, right_peremena, down_peremena, opor_plan, answer_user)
        if b[right_peremena] == 0:
            right_peremena += 1
        if a[down_peremena] == 0:
            down_peremena += 1

def virod_potencial_check(opor_plan, a, b, teta, plus_or_minus):
    virod_potencial = 0 #В начале virod_potencial служит счётчиком для подсчёта одинаковых минусовых элементов в опорном плане
    for i in range(len(a)):
        for j in range(len(b)):
            if opor_plan[i][j] == teta and plus_or_minus[i][j] == '-':
                virod_potencial += 1
    for i in range(len(a)):
        for j in range(len(b)):
            if plus_or_minus[i][j] == '-':
                if opor_plan[i][j] == teta:
                    if virod_potencial > 1:
                        opor_plan[i][j] = 0.0001
                        virod_potencial -= 1
                    else:
                        opor_plan[i][j] = 0
                else:
                    opor_plan[i][j] = opor_plan[i][j] - teta
            elif plus_or_minus[i][j] == '+':
                opor_plan[i][j] = opor_plan[i][j] + teta
            
def potencial(answer_user, a, b, opor_plan, ci, cel_fun):
    full_checker = 1
    case = 1
    while full_checker == 1:
        if answer_user == "Y":
            print(f'{case} итерация')
        case += 1
        u_vidim = ['-'] * (len(a))
        v_vidim = ['-'] * (len(b))
        for i in range(len(a)):
            for j in range(len(b)):
                u_vidim[i] = f'U{i+1}'
                v_vidim[j] = f'V{j+1}'
        full_checker = 0
        u = ['-'] * (len(a))
        v = ['-'] * (len(b))
        u[0] = 0
        for k in range(len(a)+len(b)):
            for i in range(len(a)):
                for j in range(len(b)):
                    if opor_plan[i][j] > 0:
                        if u[i] != '-':
                            v[j] = u[i] + ci[i][j]
                        elif v[j] != '-':
                            u[i] = v[j] - ci[i][j]
        for i in range(len(a)):
            for j in range(len(b)):
                ci[i][j] = ci[i][j] - v[j] + u[i]
        delta = min(map(min, ci))
        if answer_user == "Y":
            print("Определим Ui и Vj: \n", tabulate([u], headers=u_vidim, tablefmt="fancy_grid"), '\n', tabulate([v], headers=v_vidim, tablefmt="fancy_grid"))
            print(f'Построим оценочную матрицу {case-1}-ой итерации \n C{case - 1} = \n', tabulate(ci, tablefmt="fancy_grid"))
            print(f'Минимальное число в оценочной матрице Δ={delta}')
        for i in range(len(a)):
            for j in range(len(b)):
                if ci[i][j] == delta:
                    index_strok = i
                    index_stolb = j
        double = [[0]*len(b) for i in range(len(a))]
        for i in range(len(a)):
            for j in range (len(b)):
                double[i][j] = opor_plan[i][j]
        vremen = 1000000
        double[index_strok][index_stolb] = vremen
        virod_down = [0]*(len(b))
        virod_right = [0]*(len(a))
        cheker_wrong = 1
        while cheker_wrong != 0:
            cheker_wrong = 0
            for i in range(len(virod_down)):
                cheker = 0
                if virod_down[i] == 0:
                    for j in range(len(a)):
                        if virod_right[j] == 0:
                            if double[j][i] > 0:
                                cheker+=1
                    if cheker == 1:
                        virod_down[i] = 1
                        cheker_wrong += 1
            for i in range(len(virod_right)):
                cheker = 0
                if virod_right[i] == 0:
                    for j in range(len(b)):
                        if virod_down[j] == 0:
                            if double[i][j] > 0:
                                cheker+=1
                    if cheker == 1:
                        virod_right[i] = 1
                        cheker_wrong += 1
        plus_or_minus = [[1]*len(b) for i in range(len(a))]
        for i in range(len(a)):
            for j in range(len(b)):
                if virod_down[j] == 0 and virod_right[i] == 0 and double[i][j] != 0:
                    plus_or_minus[i][j] = 0 
        plus_or_minus[index_strok][index_stolb] = '+'
        glass = 1
        while glass != 0:
            glass = 0
            for i in range(len(a)):
                for j in range(len(b)):
                    if plus_or_minus[i][j] == '+':
                        for g in range(len(a)):
                            if plus_or_minus[g][j] == 0:
                                plus_or_minus[g][j] = '-'
                                glass += 1
                        for g in range(len(b)):
                            if plus_or_minus[i][g] == 0:
                                plus_or_minus[i][g] = '-'
                                glass += 1
                    if plus_or_minus[i][j] == '-':
                        for g in range(len(a)):
                            if plus_or_minus[g][j] == 0:
                                plus_or_minus[g][j] = '+'
                                glass += 1
                        for g in range(len(b)):
                            if plus_or_minus[i][g] == 0:
                                plus_or_minus[i][g] = '+'
                                glass += 1
        teta = -1
        for i in range(len(a)):
            for j in range(len(b)):
                if plus_or_minus[i][j] == '-':
                    if teta == -1:
                        teta = opor_plan[i][j]
                    elif teta > opor_plan[i][j]:
                        teta = opor_plan[i][j]
        if teta == -1:
            teta = 0
        if answer_user == "Y":
            print(f'Θ={teta}')
        virod_potencial_check(opor_plan, a, b, teta, plus_or_minus)
        cel_fun = cel_fun + delta*teta
        if answer_user == "Y":
            print(f'Перестроим матрицу X{case-2} под оценочную матрицу \n X{case-1}= \n', tabulate(opor_plan, tablefmt="fancy_grid"))
            print(f'Значение целевой функции равно L = {cel_fun}')
        for i in range(len(a)):
            for j in range (len(b)):
                if ci[i][j] < 0:
                    full_checker = 1
    return cel_fun
    
cel_fun = 0
postavki = int(input('Введите количество оптовых баз: '))
potrebitely = int(input('Введите количество пунктов назначения: '))
a = [0] * postavki
b = [0] * potrebitely

for i in range(postavki):
    a[i]=int(input(f'Сколько товара хранится на {i+1}-ой базе: '))
for i in range(potrebitely):
    b[i]=int(input(f'Сколько требует товара {i+1}-ый склад: '))
fictiv_szu(a, b)
matrix = [[0] * len(b) for i in range(len(a))]
for i in range(postavki):
    for j in range(potrebitely):
        matrix[i][j] = int(input(f'Введите тариф перевозки 1 единицы товара с {i+1}-ой базы в {j+1}-ый склад: ' ))

answer_user = input('Хотите увидеть пункты решения задачи? (Y/N)  :')
if answer_user == "Y":
    print('Определим начальный опорный план задания при помощи метода северо-западного угла:')
    
opor_plan=[[0]*len(b) for i in range(len(a))]
szu(opor_plan, a, b, answer_user)
# Определение первоначальной оценочной матрицы
ci = [[0] * len(b) for i in range(len(a))]
for i in range(len(a)):
    for j in range(len(b)):
        ci[i][j] = matrix[i][j]
# Подсчёт целефой функции по первоначальному опорному плану
for i in range(len(a)):
    for j in range(len(b)):
        if opor_plan[i][j] > 0:
            cel_fun += opor_plan[i][j]*ci[i][j]
if answer_user == "Y":
    print('X0 = ', '\n', tabulate(opor_plan, tablefmt="fancy_grid"))
    print('Матрица с тарифами будет иметь следующий вид: \n', 'C= \n', tabulate(ci, tablefmt="fancy_grid"))
    print(f'Значение целевой функции равно L = {cel_fun}')
    print("Для улучшения опорного плана теперь будем использовать метод потенциалов")
cel_fun = potencial(answer_user, a, b, opor_plan, ci, cel_fun)
print("Оценочная матрица не содержит отрицательных чисел, поэтому")
print(f'Значение целевой функции равно L = {cel_fun}')


# 

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




