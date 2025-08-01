from custom.customdialog import *
from custom.gui import *
from custom.table import *
from tkinter import Button,Checkbutton,Label,LabelFrame,Menu,BooleanVar
from tkinter.messagebox import showerror
from tkinter.filedialog import askopenfilename,asksaveasfilename
from tk2.omnispin import OmniSpin
from pandas import read_csv,DataFrame
from os.path import basename,dirname,exists,getsize,isdir
from os import sep as ossep,getcwd,mkdir
from json import loads as njs
import csv
from strings import STRINGS,LANGUAGE
#LANGUAGE='EN'
csv.register_dialect(';', delimiter=';')
csv.register_dialect('\t', delimiter='\t')
csv.register_dialect('|', delimiter='|')
csv.register_dialect(' ', delimiter=' ')
csv.register_dialect(',', delimiter=',')
class TableWrapper(LogPrinter,WrapperStub):
    format=('CSV','*.csv',((STRINGS.loc['FORMAT::CSV',LANGUAGE],'*.csv'),(STRINGS.loc['FORMAT::*',LANGUAGE],'*')))
    def body(self,**kw):
        dl=LabelFrame(self.ls,text='Separator')
        self.delimiter=DCombo2(dl,values={'Tab':'\t','Space':' ',',':',',';':';','|':'|'},width=1)
        self.delimiter.set(';')
        self.delimiter.pack(fill='x',expand=True)
        self.table=Table(self.container,array=DataFrame([['']*10 for i in range(20)]))
        self.table.grid(row=0,column=0,sticky='nsew')
        hd=Checkbutton(self.ls,text='Use headers',variable=self.table.header)
        if self.ls.grid_size()[1]>2:
            dl.grid(row=0,column=1,rowspan=2,sticky='nsew')
            hd.grid(row=2,column=1,sticky='nsew')
        else:
            dl.grid(row=2,column=0,sticky='nsew')
            hd.grid(row=3,column=0,sticky='nsew')
        return self.table
    def __getitem__(self,key):
        return self.table[key]
    def __setitem__(self,key,value):
        self.table[key]=value
    def zoom(self,x=None,y=None,f=None):
        self.table.zoom(x,y,f)
    def load(self,file):
        try:
            self.print(f'Loading {file}...',end=' ')
            with open(file) as csvfile:
                array = DataFrame(data = [[number(i)for i in row] for row in csv.reader(csvfile, self.delimiter.get())]).replace(to_replace=None,value='',regex=[None])
            if self.table.header.get():
                array.index=['index',*array.index[1:]]
                array=array.T.set_index('index').T.reset_index(drop=True)
            self.table.load(array,file)
            del array
            self.print('done')
        except UnicodeDecodeError:showerror('Error','Error loading file\nEncoding is not UTF-8')
    def save(self,file):
        if self.table.header.get():self.table.array.to_csv(file,sep=self.delimiter.get(),encoding='utf-8',index=False)
        else:self.table.array.to_csv(file,sep=self.delimiter.get(),encoding='utf-8',index=False,header=False)
        self.table.config(text=file)
        self.table.event_generate('<<loadvalues>>')
class FASTAProvider(_DatabaseProvider):
    printer=None
    name=STRINGS.loc['DB::FASTA',LANGUAGE]
    format=['Z-List','*.zlist',((STRINGS.loc['FORMAT::ZLIST',LANGUAGE],'*.zlist'),)]
    lstype='lsa'
    legend=False
    def body2(self,master=None):
        self.table.config(text='')
        a=LabelFrame(self.top,text=STRINGS.loc['DB::FASTA:MANAGE',LANGUAGE])
        Button(a,text=STRINGS.loc['DB::FASTA:ADD',LANGUAGE],command=self.askadd).grid(row=0,column=1,sticky='nsew')
        Button(a,text=STRINGS.loc['DB::FASTA:RELOAD',LANGUAGE],command=self.reload).grid(row=1,column=1,sticky='nsew')
        Button(a,text=STRINGS.loc['DB::FASTA:DELETE',LANGUAGE],command=self.askdelete).grid(row=2,column=1,sticky='nsew')
        a.grid(row=0,column=2,sticky='nsew')
        self.scr=ScrolledList(self.table)
        self.scr.pack(fill='both',expand=True)
        self.scr.on_select=lambda *a:None
        self.content={}
        self.fasta={}
        self.zindex={}
        self.accs={}
        self.raccs={}
        self.names=[]
    def reload(self,name=None):
        if name is None:name=self.names[self.scr.index("active")]
        self.print(f'Updating {name}...')
        self.rebuild(name)
    def askadd(self):
        if(name:=askopenfilename(defaultextension='*.fas',filetypes=((STRINGS.loc['FORMAT::FASTA',LANGUAGE],'*.fas *.fta *.fasta'),
                                                                     (STRINGS.loc['FORMAT::FASTA:NUCL',LANGUAGE],'*.ffn *.fna'),
                                                                     (STRINGS.loc['FORMAT::FASTA:PROT',LANGUAGE],'*.faa'),
                                                                     (STRINGS.loc['FORMAT::ZLIST',LANGUAGE],'*.zlist'),
                                                                     (STRINGS.loc['FORMAT::*',LANGUAGE],'*')))):
            if name.endswith('.zlist'):self.openzl(name)
            else:self.add(name)
    def add(self,name):
        if name in self.fasta:
            self.delete(name)
            self.add(name)
        else:
            self.print(f'Loading {name}...',end=' ')
            try:
                file=open(name)
                self.fasta[name]=file
                self.names.append(name)
                self.print('done')
                if exists(name+'.zindex'):
                    self.print('Verifying Z-Index...',end=' ')
                    self.openz(name)
                    self.rebuild(name)
                else:
                    self.print('Z-index is missing!')
                    self.zbuild(name,file)
                self.scr.append(name)
            except FileNotFoundError:showerror('Error',f'File {name} is missing!')
    def rebuild(self,name,error='Z-index out of date!'):
        if not self.verify(self.fasta[name],self.zindex[name]):
            self.print(error)
            self.zbuild(name,self.fasta[name])
        else:self.print('done')
    def zbuild(self,name,file):
        self.print('Rebuilding Z-Index...',end=' ')
        self.zindex[name]=self.index(file)
        self.accs[name]={i:self.accession(i)for i in self.zindex[name]}
        self.raccs[name]={self.accession(i):i for i in self.zindex[name]}
        try:
            self.savez(name,self.zindex[name])
            self.print('done')
        except PermissionError:
            self.print('done')
            self.print(f'Error: {name}.zindex is not writeable')
            self.print('Warning: Z-Index will not be saved.')
    def askdelete(self):
        self.delete(self.names[self.scr.index("active")])
    def delete(self,name):
        self.scr.delete(self.names.index(name))
        self.fasta[name].close()
        del self.fasta[name]
        del self.zindex[name]
        del self.accs[name]
        del self.raccs[name]
        del self.names[self.names.index(name)]
    def index(self,file):
        c={}
        file.seek(0)
        while (b:=file.readline()):
            if b.startswith('>'):
                c[b[:-1]]=file.tell()
        return c
    def accession(self,s):
        s2=s.split(' 'if' 'in s else'_')[0].split(':')[0][1:]
        return s2[:-2]if(s2[-2]=='.'and s2[-1].isdigit())else s2
    def verify(self,file,index):
        v=1
        i2={i:index[i]for i in index}
        file.seek(0)
        while (b:=file.readline()):
            if b.startswith('>'):
                if b[:-1] in i2 and i2[b[:-1]]==file.tell():
                    del i2[b[:-1]]
                else:print(repr(b),b[:-1] in index,self.accession(b)in index,file.tell());v=0;break
        if bool(i2):v=0
        return v
    def openz(self,name):
        self.zindex[name]=dict(zip((d:=read_csv(name+'.zindex',header=None)).iloc[:,0],d.iloc[:,1]))
        self.accs[name]={i:self.accession(i)for i in self.zindex[name]}
        self.raccs[name]={self.accession(i):i for i in self.zindex[name]}
    def savez(self,name,index):
        DataFrame(index.items()).to_csv(name+'.zindex',index=None,header=None)
    def __getitem__(self,key):
        if isinstance(key,tuple) and len(key)==2:
            f,h=key
            if h in self.raccs[f]:return self.extract(f,self.raccs[f][h])
            elif h[-2]=='.'and h[:-2]in self.raccs[f]:return self.extract(f,self.raccs[f][h[:-2]])
            elif h in self.accs[f]:return self.extract(f,h)
            elif '>'+h in self.accs[f]:return self.extract(f,'>'+h)
            else:return '>Error\nNNNNNNNN'
        elif key in self.names:return self.extract(key)
    def extract(self,name,header=None):
        file=self.fasta[name]
        if header is None:
            file.seek(0)
            return file.read()
        else:
            s=header+'\n'
            file.seek(self.zindex[name][header])
            while (b:=file.readline()):
                if b.startswith('>'):break
                else:s+=b
            return s
    def save(self,file):
        with open(file,'w')as z:z.write('\n'.join(self.fasta))
    def unloadall(self):
        for i in range(len(self.names)):self.delete(self.names[0])
    def load(self,file):
        self.close()
        self.openzl(file)
    def openzl(self,file):
        with open(file)as z:
            for i in z.read().splitlines():
                self.add(i)
    def send(self):
        io=askcustom('Select file','Select file:',setio('',{'FASTA':(DCombo,[],{'text':'FASTA','values':self.names})}))
        if io is not None:return self[io['FASTA']]
#Unused, FASTAProvider is radio.instance'd to only send and not receive
#This is because this is stupid. What's the point if you have to save the file first anyway?
##    def receive(self,payload): 
##        if payload is not None:
##            if(file:=asksaveasfilename(defaultextension='*.fas',filetypes=(('FASTA','*.fas *.fta *.fasta'),('Nucleotide FASTA','*.ffn *.fna'),('Amino acid FASTA','*.faa'),('All files','*')))):
##                with open(file,'w')as f:
##                    f.write(payload)
##                self.add(file)
class BLASTDBProvider(_DatabaseProvider):
    printer=None
    name=STRINGS.loc['DB::BLAST',LANGUAGE]
    format=[STRINGS.loc['DB::DB',LANGUAGE],'*.njs',((STRINGS.loc['FORMAT::NJS',LANGUAGE],'*.njs'),)]
    lstype='luan'
    lsname=STRINGS.loc['DB::MANAGE',LANGUAGE]
    legend=False
    def body2(self,master=None):
        self.table.config(text='')
        a=LabelFrame(self.top,text=STRINGS.loc['DB::CREATE',LANGUAGE])
        Button(a,text='Create a database',command=self.askadd,state='disabled'
               #('normal'if 'makeblastdb'in self.kw and self.kw['makeblastdb']else'disabled')
               ).grid(row=0,column=0,sticky='nsew')
        Label(a,text=(self.kw['makeblastdb'].rstrip())if self.kw['makeblastdb']else'makeblastdb: Unavailable',state='disabled').grid(row=1,column=0,sticky='nsew')
        a.grid(row=0,column=2,sticky='nsew')
        self.scr=TreeViewMSL(self.table,('Title',
                                         'Type',
                                         'Version',
                                         'Created',
                                         'Sequences',
                                         'Main file'))
        self.scr.pack(fill='both',expand=True)
        self.scr.on_select=lambda *a:None
        self.data={}
        self.files=[]
        self.list={}
        self.names=[]
        self.revdata={}
    def askadd(self):
        if(name:=askopenfilename(defaultextension='*.fas',filetypes=(('FASTA','*.fas *.fta *.fasta'),('Nucleotide FASTA','*.ffn *.fna'),('Amino acid FASTA','*.faa'),('All files','*')))):
            self.copy(name)
    def askdelete(self):
        if item:=self.scr.selection():
            self.delete(item)
    unload=askdelete
    def delete(self,name):
        if name in self.revdata:
            self.names.remove(name[0])
            self.files.remove(self.revdata[name])
            del self.data[self.revdata[name]]
            del self.list[name[0]]
            del self.revdata[name]
        self.scr.delete(name)
    def unloadall(self):
        for i in [*self.revdata]:self.delete(i)
    def close(self):pass#Kludge
    def copy(self,file):
        if exists(getcwd()+ossep+'db') and not isdir(getcwd()+ossep+'db'):
            showerror(STRINGS.loc['MISC::ERROR',LANGUAGE],getcwd()+ossep+'db is not a directory!')
        else:
            if not exists(getcwd()+ossep+'db'):
                try:mkdir(getcwd()+ossep+'db',mode=777)
                except PermissionError:showerror(STRINGS.loc['MISC::ERROR',LANGUAGE],'Cannot create directory '+getcwd()+ossep+'db')
            if exists(file):
                with open(file,'rb')as f1:
                    L=ProgressLogger(self.master.window,int(getsize(file)/2**24))
                    n2=getcwd()+ossep+'db'+ossep+basename(file)
                    open(n2,'wb').close()
                    while ch:=f1.read(2**24):
                        with open(n2,'r+b')as f2:
                            f2.seek(getsize(n2))
                            f2.write(ch)
                        L.step(f'Copying {file} into {n2}')
                    L.close()
#MAKE IT AND PUT IT INTO MAIN GENEPROT
#FIGURE OUT WHY MAKEBLASTDB HAS A PERMISSION ERROR
##    def make(self=None): 
##        from tk2 import OmniText            
##        import subprocess
##        import sys
##        from io import StringIO
##        omni=OmniText(scrolling=(1,1),state='readonly')
##        omni.pack()
##        command = 'D:/smb/BLAST/bin/makeblastdb.exe \
##        -in D:/smb/BLAST/db\\gene-COI.fasta \
##        -parse_seqids \
##        -blastdb_version 5 \
##        -title "gene-COI" \
##        -dbtype nucl'
##        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
##        a=0
##        io=StringIO()
##        try:
##            while True:
##                output = process.stdout.readline()# Read a line from stdout
##                if output:print(output);omni.insert('end',output);io.write(StringIO)
##                if process.poll() is not None: break
##                omni.update_idletasks();omni.update()
##            remaining_output, remaining_error = process.communicate()
##            if remaining_output:omni.insert('end',remaining_output.strip)
##            #if remaining_error:#omni.insert('end',remaining_error.strip)
##        except KeyboardInterrupt:
##            process.terminate()  # Terminate the process if needed
##            omni.insert('end',"Process terminated.")
##        omni.insert('end',"Return Code:%s"%process.returncode)# Check the return code
    def __getitem__(self,key):
        if key in self.list:return self.list[key]
    def load(self,file):
        try:
            with open(file)as d:
                data=njs(d.read())
                self.files.append(file)
                self.names.append(data['description'])
                self.list[data['description']]=dirname(file)+ossep+data['dbname']
                self.data[file]=(data['description'],data['dbtype'],data['version'],data['last-updated'],data['number-of-sequences'],data['dbname'])
                self.revdata[self.data[file]]=file
                self.scr.append(self.data[file])
        except FileNotFoundError:
            showerror(STRINGS.loc['MISC::ERROR',LANGUAGE],STRINGS.loc['MISC::FILE_NOT_FOUND',LANGUAGE].format(file))
            self.close()
            return False
    add=load

class SaprobityProvider(TableWrapper,LogPrinter):
    printer=None
    name=STRINGS.loc['DB::SAPROBITY',LANGUAGE]
    lstype='lcs'
    def __init__(self,master=None,**kw):
        self.master=master
        self.kw=kw
        TableWrapper.__init__(self,master=master,name=self.name)
        master.add(self,text=self.name)
        self.flag=BooleanVar(self,False)
        self.pos=len(master.tabs())-1
        self.config(text='')
    def body(self,master=None):
        body=TableWrapper.body(self,master=master)
        self.table.bind('<<resize>>',self.resize)
        self.table.bind('<<loadvalues>>',self.upflag)
        col=LabelFrame(self.top,text='Select columns')
        self.txid=OmniSpin(col,text='taxid',width=4,cnf={'from':0,'to':self.table.W-1})#,textvariable=self.svar)
        self.txid.grid(row=0,column=0,padx=10,sticky='nsew')
        self.saprobity=OmniSpin(col,text='Saprobity',width=4,cnf={'from':0,'to':self.table.W-1})
        self.saprobity.grid(row=0,column=1,padx=10,sticky='nsew')
        col.grid(row=0,column=1,sticky='nsew')
        return body
    def resize(self,event):
        for i in[self.txid,self.saprobity]:i['to']=self.table.W-1
    def txids(self):return self[:,self.txid.get()]
    def saprobities(self):return self[:,self.saprobity.get()]
    def load(self,file):
        TableWrapper.load(self,file=file)
        self.flag.set(True)
    def upflag(self,event):self.flag.set(True)
    def __call__(self):
        self.master.deiconify()
        self.master.select(self.pos)
    def close(self):
        self.table.load(DataFrame([['']*10 for i in range(20)]),'')
        self.flag.set(False)

class OtherError(Exception):
    '''Custom error message for Downloader'''

def join(*a):
    return ossep.join(a)
