from custom.customdialog import *
from custom.gui import *
from custom.table import *
from tkinter import Button,LabelFrame,Menu
from tkinter.messagebox import showerror
from tkinter.filedialog import askopenfilename,asksaveasfilename
from pandas import read_csv,DataFrame
from os.path import exists

class FASTAProvider(_DatabaseProvider):
    printer=None
    name='FASTA DB'
    format=['Z-List','*.zlist',(('Z-Index List','*.zlist'),)]
    lstype='ls'
    def legend(self,legend):None
    def body2(self,master=None):
        self.table.config(text='')
        a=LabelFrame(self.top,text='Manage FASTA')
        Button(a,text='Load',command=self.askadd).grid(row=0,column=1,sticky='nsew')
        Button(a,text='Reload',command=self.reload).grid(row=1,column=1,sticky='nsew')
        Button(a,text='Unload',command=self.askdelete).grid(row=2,column=1,sticky='nsew')
        a.grid(row=0,column=2,sticky='nsew')
        Button(self.ls,text='Unload all',command=self.close).grid(row=2,column=0,sticky='nsew')
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
        if(name:=askopenfilename(defaultextension='*.fas',filetypes=(('FASTA','*.fas *.fta *.fasta'),('Nucleotide FASTA','*.ffn *.fna'),('Amino acid FASTA','*.faa'),('Z-List','*.zlist'),('All files','*')))):
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
        #self.scr.delete(self.scr.index("active"),self.scr.index("active")+1)
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
    def close(self):
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
        print(io)
        return self[io['FASTA']]
    def receive(self,payload):
        None
        if(file:=asksaveasfilename(defaultextension='*.fas',filetypes=(('FASTA','*.fas *.fta *.fasta'),('Nucleotide FASTA','*.ffn *.fna'),('Amino acid FASTA','*.faa'),('All files','*')))):
            with open(file,'w')as f:
                f.write(payload)
            self.add(file)

class OtherError(Exception):
    '''Custom error message for Downloader'''

def show(t,w=0,depth=-1,d=0):
    for i in range(len(t)):
        if isinstance(t[i],tuple):
            if depth:show(t[i],w+4,depth-1,d+1)
            else:print(' '*w+f't({d})[{i}]')
        else:print(' '*w+str(t[i]))
