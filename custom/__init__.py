from custom.customdialog import *
from custom.wheretodialog import *
from custom.gui import *
from custom.gui import _DatabaseProvider
from custom.op import *
from tkinter import Button,Checkbutton,Frame,Label,LabelFrame,Listbox,Scrollbar,Tk,Toplevel,Pack,Grid,Place,BooleanVar,IntVar
from tkinter.messagebox import showerror
from tkinter.filedialog import askopenfilename,asksaveasfilename
from tkinter.messagebox import showwarning,showerror
from tk2 import OmniSpin,OpenFileButton
from pandas import read_csv,DataFrame
from os.path import exists
class TaxSpin(Frame):
    def __init__(self,master=None,type=None,cnf={},maxvalue=10,**kw):
        self.frame=RadioCheck(master,text='Scientific name',type=type,variable=kw.pop('radiovariable',None),value=kw.pop('radiovalue',None))
        Frame.__init__(self,master=self.frame)
        self.sw=BooleanVar(self,False)
        self.col=0
        self.split=Checkbutton(self,text='Split?',variable=self.sw,height=1)
        self.split.grid(row=0,column=self.col,sticky='nsew')
        self.sw.trace_add('write',self.showhide)
        self.genus=OmniSpin(self,width=4,cnf={'from':0,'to':maxvalue})
        self.genus.grid(row=1,column=self.col,padx=0,sticky='nsew')
        self.species=OmniSpin(self,text='Species',width=4,cnf={'from':0,'to':maxvalue})
        self.frame.setwidget(self)
    def config(self,**kw):
        if 'state' in kw:
            self.genus.config(state=kw['state'])
            self.species.config(state=kw['state'])
            self.split.config(state=kw['state'])
            del kw['state']
        Frame.config(self,**kw)
    def showhide(self,*a):
        if self.sw.get():
            self.species.grid(row=2,column=self.col,sticky='nsew')
            self.genus.frame.configure(text='Genus',relief='groove')
        else:
            self.species.grid_forget()
            self.genus.frame.configure(text='',relief='flat')
    def get(self):
        if self.frame.get():
            if self.sw.get():return(self.genus.get(),self.species.get())
            else:return(self.genus.get(),)
    def validate(self):return 1
class TaxSpin2(LabelFrame):
    def __init__(self,master=None,type=None,maxvalue=10,**kw):
        self.frame=RadioCheck(master,text='Ranked lineage',type=type,variable=kw.pop('radiovariable',None),value=kw.pop('radiovalue',None))
        Frame.__init__(self,master=self.frame)
        self.value=0
        self.enabled=maxvalue>=9
        if self.enabled:
            self.spin=OmniSpin(self,width=4,type=str,values=tuple([f'{i}-{i+8}'for i in range(maxvalue-7)]))
            self.spin.grid(row=0,column=0,sticky='nsew')
        else:
            self.spin=Label(self,text='Not enough columns')
            self.spin.pack(fill='both',expand=True)
        self.frame.setwidget(self)
    def link(self,r):
        self.value=self.spins[r].get()-r
        for i in range(len(self.spins)):self.spins[i].set(self.value+i)
    def get(self):
        if self.frame.get():
            if self.enabled:
                a=self.spin.get().split('-')
                return slice(int(a[0]),int(a[1]),None)
            else:return None
    def validate(self):
        if self.enabled:return 1
        else:showerror('Error','Not enough columns for ranked lineage!');return 0
    def config(self,**kw):
        if'state'in kw:self.spin.config(state=kw['state']);del kw['state']
def askio(title=None, prompt=None, inputs=None, outputs=None, validate=all, **kw):
    return askcustom(title=title,prompt=prompt,widget=(Group,[],{'orient':'horizontal','widgets':{0:inputs,1:outputs},'validate':all}),validate=validate, **kw)
def setio(title,widgets,**kw):
    return (Group,[],{'title':title,'widgets':widgets,**kw})
def atleastoneoutput(io):
    if any([(io[1][i]is not None)for i in io[1]]):return 1
    else:showerror('Error!','Enable at least one output');return 0
class ScrolledList(Listbox):
    default = "<empty>"
    def __init__(self, master, **options):
        self.master = master
        self.frame = Frame(master)
        self.vbar = vbar = Scrollbar(self.frame, name="vbar")
        self.vbar.pack(side="right", fill="y")
        Listbox.__init__(self,master=self.frame,exportselection=0,background="white")
        if options:Listbox.configure(self,options)
        Listbox.pack(self,fill="both",expand=True)
        vbar["command"] = self.yview
        self["yscrollcommand"] = vbar.set
        self.bind("<ButtonRelease-1>", self.click_event)
        self.bind("<Key-Up>", self.up_event)
        self.bind("<Key-Down>", self.down_event)
        self.clear()
        methods = vars(Pack).keys() | vars(Grid).keys() | vars(Place).keys()
        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.frame, m))
    def destroy(self):
        Listbox.destroy(self)
        self.frame.destroy()
    def clear(self):
        self.delete(0, "end")
        self.empty = True
        self.insert("end", self.default)
    def append(self, item):
        if self.empty:
            self.delete(0, "end")
            self.empty = False
        self.insert("end", str(item))
    def click_event(self, event):
        self.activate("@%d,%d" % (event.x, event.y))
        index = self.index("active")
        self.select(index)
        self.on_select(index)
        return "break"
    def up_event(self, event):
        index = self.index("active")
        if self.selection_includes(index):index-=1
        else:index = sel.size() - 1
        if index < 0:self.bell()
        else:
            self.select(index)
            self.on_select(index)
        return "break"
    def down_event(self, event):
        index = self.index("active")
        if self.selection_includes(index):index+=1
        else:index = 0
        if index >= self.size():self.bell()
        else:
            self.select(index)
            self.on_select(index)
        return "break"
    def select(self, index):
        self.focus_set()
        self.activate(index)
        self.selection_clear(0, "end")
        self.selection_set(index)
        self.see(index)

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
        Button(a,text='Reload',command=self.askreload).grid(row=1,column=1,sticky='nsew')
        Button(a,text='Unload',command=self.askdelete).grid(row=2,column=1,sticky='nsew')
        a.grid(row=0,column=2,sticky='nsew')
        Button(self.ls,text='Unload all',command=self.close).grid(row=2,column=0,sticky='nsew')
        self.scr=ScrolledList(self.table)
        self.scr.pack(fill='both',expand=True)
        self.scr.on_select=lambda *a:None
        self.content={}
        self.fasta={}
        self.zindex={}
        self.names=[]
    def askreload(self):
        name=self.names[self.scr.index("active")]
        self.delete(name)
        self.add(name)
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
                    self.zindex[name]=self.openz(name+'.zindex')
                    self.rebuild(name)
##                    if not self.verify(file,self.zindex[name]):
##                        self.print('fail')
##                        self.zbuild(name,file)
##                    else:self.print('done')
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
        try:
            self.savez(name+'.zindex',self.zindex[name])
            self.print('done')
        except PermissionError:
            self.print('done')
            self.print(f'Error: {name}.zindex is not writeable')
            self.print('Warning: Z-Index will not be saved.')
    def askdelete(self):
        self.delete(self.names[self.scr.index("active")])
        self.scr.delete(self.scr.index("active"),self.scr.index("active")+1)
    def delete(self,name):
        self.scr.delete(self.names.index(name))
        self.fasta[name].close()
        del self.fasta[name]
        del self.zindex[name]
        del self.names[self.names.index(name)]
    def index(self,file):
        c={}
        while (b:=file.readline()):
            if b.startswith('>'):c[b[:-1]]=file.tell()
        return c
    def verify(self,file,index):
        v=1
        while (b:=file.readline()):
            if b.startswith('>'):
                if b[:-1] in index and index[b[:-1]]==file.tell():continue
                else:print(b,index[b[:-1]],file.tell);v=0;break
        return v
    def openz(self,file):return dict(zip((d:=read_csv(file,header=None)).iloc[:,0],d.iloc[:,1]))
    def savez(self,file,index):DataFrame(index.items()).to_csv(file,index=None,header=None)
    def __getitem__(self,key):
        if isinstance(key,tuple) and len(key)==2:return self.extract(*key)
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
    def open(self,file):
        self.close()
        self.openzl(file)
    def openzl(self,file):
        with open(file)as z:
            for i in z.read().splitlines():
                self.add(i)
    load=open
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
