from os import remove
from os.path import getsize
from zipfile import ZipFile
print('loading...',end='')
f=open('nucl_gb.accession2taxid')
print('done')
print(f.readline())
#f.read(38)
#if f.readline()=='accession\taccession.version\ttaxid\tgi\n':print('header')
fl={}
n=0
print('processing...')
while (l:=f.readline()):
    s=l.split('\t')
    if s[0][:2] not in fl:
        fl[s[0][:2]]=open('gb2taxid/'+s[0][:2],'w')
        fl[s[0][:2]].write(s[0]+';'+s[2]+'\n')
        fl[s[0][:2]].close()
    elif fl[s[0][:2]].closed:
        fl[s[0][:2]]=open('gb2taxid/'+s[0][:2],'a')
        fl[s[0][:2]].write(s[0]+';'+s[2]+'\n')
        fl[s[0][:2]].close()
    else:print('unknown error')
    n+=1
    if n<1000000:
        if n<100000:
            if n<10000:
                if n<1000:
                    if n<100:
                        if n<10:print(n)
                        elif n%10==0:print(n)
                    if n%100==0:print(n)
                if n%1000==0:print(n)
            if n%10000==0:print(n)
        if n%100000==0:print(n)
    elif n%1000000==0:print(n)
print('done')
print('zipping...')
z=ZipFile('gb2taxid/gb2taxid.zip','w',8)
n=0
l=len([*fl])
for i in fl:
    z.write('gb2taxid/'+i,i)
    n+=1
    print(f'{n}/{l}')
z.close()
print('done')
print('cleaning up...')
for i in fl:remove('gb2taxid/'+i)
print('done')
