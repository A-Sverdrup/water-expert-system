from random import randrange,shuffle

def rand(percentage):
    b=[]
    c=len(table.table.array)
    for i in range(int(percentage*c)):
        while (a:=randrange(0,c))in b:None
        if a in b:raise RuntimeError("wtf")
        else:b.append(a)
        if i%1000:print(i)
    b.sort()
    if b!=[*set(b)]:raiseRuntimeError("wtf")
    table.table.load(table.table.array.iloc[b,:],f'{100*percentage}% random')

def rand(percentage):
    c=len(table.table.array)
    a=[*range(c)]
    shuffle(a)
    b=sorted(a[:int(percentage*c)])
    print('random',len(b)/c)
    table.table.load(table.table.array.iloc[b,:],f'{100*percentage}% random')
