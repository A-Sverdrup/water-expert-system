from tkinter import Button,Entry,Frame,LabelFrame,Label,Listbox,Menu,PanedWindow,Toplevel,Scrollbar,StringVar,BooleanVar,Pack,Grid,Place
from tkinter.filedialog import askopenfilename,asksaveasfilename
from tkinter.messagebox import showerror
from tkinter.ttk import Notebook
from tk2 import ToggleRadioButton
from zipfile import ZipFile
__all__=['LoadSave','OpenClose','LogPrinter','WrapperStub','Search','Transceiver','Dashboard','DatabaseProvider','_DatabaseProvider','GB2TaxIdProvider','TaxdumpProvider',]

class LoadSave(LabelFrame):
    B1='Load %s'
    B2='Save %s'
    def __init__(self,master,type,defaultextension,filetypes,load=None,save=None):
        LabelFrame.__init__(self,master=master,text='File')
        self.type=type
        self.de=defaultextension
        self.ft=filetypes
        self.load=load
        self.save=save
        if load:Button(self,text=self.B1%type,command=self.F1).grid(row=0,column=0,padx=10,sticky='we')
        if save:Button(self,text=self.B2%type,command=self.F2).grid(row=(1 if load else 0),column=0,padx=10,sticky='we')
    def F1(self):
        if (file:=askopenfilename(defaultextension=self.de,filetypes=self.ft)):
##            try:
            self.load(file)
##            except:showerror('Fail!','Cannot load %s file!'%self.type)
    def F2(self):
        if (file:=asksaveasfilename(defaultextension=self.de,filetypes=self.ft)):
##            try:
            self.save(file)
##            except:showerror('Fail!','Cannot save %s file!'%self.type)
class OpenClose(LoadSave):
    B1='Open %s'
    B2='Close %s'
    def F2(self):
        try:
            self.unload()
        except:showerror('Fail!','Cannot close %s!'%self.type)
class WrapperStub(LabelFrame):
    lstype='ls'
    def __init__(self,master,name,**kw):
        self.name=name
        LabelFrame.__init__(self,master=master,text=name)
        self.container=PanedWindow(self,orient='vertical')
        self.container.pack(fill='both',expand=True)
        self.top=Frame(self.container)
        if self.lstype in'ls':self.ls=LoadSave(self.top,*self.format,(self.load if('l'in self.lstype)else None),(self.save if('s'in self.lstype)else None))
        elif self.lstype in'oc':self.ls=OpenClose(self.top,*self.format,(self.open if('o'in self.lstype)else None),(self.close if('c'in self.lstype)else None))
        self.ls.grid(row=0,column=0,rowspan=10,sticky='nsew')
        self.container.add(self.top)
        self.container.add(self.body(**kw))
class Search(LabelFrame):
    def __init__(self,master=None,text=None,values=None,default=None,command=None,**kw):
        LabelFrame.__init__(self,master=master,text=text,**kw)
        top=Frame(self)
        top.pack(fill='x',expand=True)
        self.entry=Entry(top)
        self.entry.pack(side='left',fill='x',expand=True)
        Button(top,text='Search',command=command).pack(side='left',fill='x',expand=True)
        grid=Frame(self)
        grid.pack(fill='x',expand=True)
        self.mode=StringVar(self,value=default)
        for i in values:
            ToggleRadioButton(grid,value=values[i],variable=self.mode,text=i).pack(side='left',fill='x',expand=True)
    def get(self):
        return self.entry.get()
class Transceiver:
    def __init__(self):self.list=[];self.menu=Menu(tearoff=0)
    def instance(self,widget,row=0,column=1,sticky='nsew',**kw):
        frame=LabelFrame(widget.top,text='Data')
        Button(frame,text='Receive',command=lambda:self.recmenu(widget,frame)).grid(row=0,column=0,padx=10,sticky='we')
        Button(frame,text='Send to',command=lambda:self.sendmenu(widget,frame)).grid(row=1,column=0,padx=10,sticky='we')
        self.list.append(widget)
        frame.grid(row=row,column=column,sticky=sticky,**kw)
        frame.bind("<Destroy>", lambda event:self.list.remove(widget))
        return frame   
    def invisible_instance(self,widget,row=0,column=1,sticky='nsew',**kw):
        self.list.append(widget)
        return lambda event:self.list.remove(widget)        
    def recmenu(self,widget,frame):
        try:self.menu.destroy()
        except:print('Already destroyed!')
        self.menu = Menu(frame,tearoff=0)
        for i in self.list:
            self.menu.add_command(label=i.name,command=(lambda j:lambda:widget.receive(j.send()))(i))
        self.menu.tk_popup(frame.winfo_rootx(),frame.winfo_rooty())
    def sendmenu(self,widget,frame):
        self.menu.destroy()
        self.menu = Menu(frame,tearoff=0)
        for i in self.list:
            self.menu.add_command(label=i.name,command=(lambda j:lambda:j.receive(widget.send()))(i))
        self.menu.tk_popup(frame.winfo_rootx(),frame.winfo_rooty())
class Dashboard(Frame):
    def __init__(self,master,orient,**kw):
        Frame.__init__(self,master=master,**kw)
        self.lang={'all':'Total entries: %s','fail':'Failed: %s','done':'Done: %s','left':'Remaining: %s','elapsed':'Elapsed: %s','ETA':'ETA: %s'}
        self.dict={i:Label(self,relief='ridge')for i in self.lang}
        self.config(**{i:0 for i in self.lang})
        self.dict['all'].grid(row=0,column=0,columnspan=3,sticky='nsew')
        self.dict['fail'].grid(row=1,column=0,sticky='nsew')
        self.dict['done'].grid(row=1,column=1,sticky='nsew')
        self.dict['left'].grid(row=1,column=2,sticky='nsew')
        self.config(elapsed='0d 00:00:00',ETA='0d 00:00:00')
        self.dict['elapsed'].grid(row=2*(orient=='vertical'),column=3*(orient=='horizontal'),columnspan=3,sticky='nsew')
        self.dict['ETA'].grid(row=1+2*(orient=='vertical'),column=3*(orient=='horizontal'),columnspan=3,sticky='nsew')
    def config(self,**kw):
        if all((i in self.dict)for i in kw):
            for i in kw:self.dict[i].config(text=self.lang[i]%kw[i])
        else:Frame.config(self,**kw)
class LogPrinter():
    def print(self,s,end='\n'):
        if self.printer:self.printer.print(s,end=end);self.printer.cpr()
        print(s,end=end)
class DatabaseProvider(Notebook):
    def __init__(self,master=None):
        self.window=Toplevel(master)
        self.window.bind("<Escape>",lambda e:self.window.withdraw())
        self.window.maxsize(800,800)
        self.window.wm_attributes('-topmost',True)
        self.window.wm_protocol('WM_DELETE_WINDOW',self.window.withdraw)
        self.window.title('Database provider')
        self.deiconify=self.window.deiconify
        self.window.withdraw()
        Notebook.__init__(self,master=self.window)
        self.pack(fill='both',expand=True)
class _DatabaseProvider(WrapperStub,LogPrinter):
    printer=None
    name=None
    lstype='oc'
    def __init__(self,master=None):
        self.master=master
        WrapperStub.__init__(self,master=master,name=self.name)
        master.add(self,text=self.name)#self.frame.pack()
        self.pos=len(master.tabs())-1
        self.config(text='')
    def body(self,master=None):
        self.filenames=[]
        self.zip=None
        legend=LabelFrame(self.top,text='Legend')
        self.legend(legend)
        legend.grid(row=0,column=1,sticky='nsew')
        self.table=LabelFrame(self.container,text='Click to pre-load files manually')
        #self.table.pack(fill='x',expand=True)
        self.body2(self.table)
        return self.table
    def __call__(self):
        self.master.deiconify()
        self.master.select(self.pos)
    def legend(self,legend):
        Label(legend,relief='groove',font=(None,4),width=2).grid(row=0,column=0)
        Label(legend,text='- Unavailable').grid(row=0,column=1)
        Label(legend,relief='groove',font=(None,4),bg='red',width=2).grid(row=0,column=2)
        Label(legend,text='- Available, not loaded').grid(row=0,column=3)
        Label(legend,relief='groove',font=(None,4),bg='green',width=2).grid(row=0,column=4)
        Label(legend,text='- Available, loaded').grid(row=0,column=5)
    def __getitem__(self,key):
        if isinstance(key,tuple) and len(key)==2:return self[key[0]][key[1]]
        elif isinstance(key,tuple) and len(key)==3:return self[key[0]].get(key[1],key[2])
        elif key in self.content:return self.content[key]
        elif key in self.filenames:self.load(key);return self[key]
    def load(self,key):
        self.print(f'loading {self.name}/{key} ... ',end=' ')
        self.content[key]=self.read(key)
        self.grid[key].config(bg='green')
        self.print(f'done',end='\n')
    def open(self,file):
        self.zip=ZipFile(file)
        self.config(text=f'{file}')
        self.filenames=self.zip.namelist()
        for i in self.grid:
            self.grid[i].config(bg='red'if i in self.filenames else 'systemButtonFace',state='normal'if i in self.filenames else'disabled')
    def close(self):
        if self.zip:
            self.zip.close()
            self.zip=None
        self.filenames=[]
        for i in self.grid:
            self.grid[i].config(bg='systemButtonFace',state='disabled')
    def save(self):None
class GB2TaxIdProvider(_DatabaseProvider):
    printer=None
    name='GB2Taxid'
    format=['DB','*.zip',(('ZIP archive','*.zip'),)]        
    def body2(self,master):
        self.ls.grid(row=0,column=0,rowspan=2)
##        self.areyousure=Button(self.top,text='Rebuild Database',command=self.nope)
##        self.areyousure.bind('<Double-1>',self.scram)
##        self.areyousure.grid(row=1,column=1)
        alph='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.grid={}
        master.rowconfigure(tuple(range(36)),weight=1)
        master.columnconfigure(tuple(range(36)),weight=1)
        for i in range(36):
            Label(master,text=alph[i],font=(None,5),relief='raised').grid(row=0,column=i+1,sticky='nsew')
        for i in range(10,36):
            Label(master,text=alph[i],font=(None,5),relief='raised').grid(row=i+1-10,column=0,sticky='nsew')
            for j in range(36):
                a=alph[i]+alph[j]
                self.grid[a]=Button(master,text=a,font=(None,5),width=1,height=1,relief='groove',state='disabled',command=(lambda f:lambda:self.load(f))(a))
                self.grid[a].grid(row=i+1-10,column=j+1,sticky='nsew')
        self.content={}
    def nope(self):
        self.areyousure.config(text='Rebuild GB2Taxid [Double-click to confirm]')
        self.after(5000,lambda:self.areyousure.config(text='Rebuild GB2Taxid'))
    def scram(self,event):self.rebuild()
    def read(self,key):
        return dict([i.split(';')for i in self.zip.read(key).decode().splitlines()])

class TaxdumpProvider(_DatabaseProvider):
    printer=None
    name='new_taxdump.zip'
    format=['DB','*.zip',(('ZIP archive','*.zip'),)]        
    def body2(self,master):
        left=['citations.dmp','delnodes.dmp','division.dmp','gc.prt','gencode.dmp','images.dmp','merged.dmp','names.dmp','nodes.dmp']
        right=['excludedfromtype.dmp','fullnamelineage.dmp','host.dmp','rankedlineage.dmp','taxidlineage.dmp','typematerial.dmp','typeoftype.dmp']
        self.grid={}
        h=0
        master.rowconfigure(tuple(range(9)),weight=1)
        master.columnconfigure((0,1),weight=1)
        for i in left:
            self.grid[i]=Button(master,text=i,relief='groove',state='disabled',command=(lambda f:lambda:self.load(f))(i))
            self.grid[i].grid(row=h,column=0,sticky='nsew')
            h+=1
        h=0
        for i in right:
            self.grid[i]=Button(master,text=i,relief='groove',state='disabled',command=(lambda f:lambda:self.load(f))(i))
            self.grid[i].grid(row=h,column=1,sticky='nsew')
            h+=1
        self.content={}
        self.grid['revnames']=Button(master,text='<Reverse name lookup>\n(Auto-generated)',relief='groove',state='disabled',command=lambda:self.load('revnames'))
        self.grid['revnames'].grid(row=h,column=1,rowspan=2,sticky='nsew')
    def legend(self,legend):
        Label(legend,relief='groove',font=(None,4),width=2).grid(row=0,column=0)
        Label(legend,text='- Unavailable').grid(row=0,column=1)
        Label(legend,relief='groove',font=(None,4),bg='grey',width=2).grid(row=0,column=2)
        Label(legend,text='- Available, unsupported').grid(row=0,column=3)
        Label(legend,relief='groove',font=(None,4),bg='red',width=2).grid(row=1,column=0)
        Label(legend,text='- Available, not loaded').grid(row=1,column=1)
        Label(legend,relief='groove',font=(None,4),bg='green',width=2).grid(row=1,column=2)
        Label(legend,text='- Available, loaded').grid(row=1,column=3)
    def read(self,key):
        if key=='rankedlineage.dmp':
            return {j[0]:j[-2:1:-1]for j in[i.split('|')for i in self.zip.read(key).decode().replace('\t','').splitlines()]}
        elif key=='names.dmp':
            names={j[0]:j[1]for j in[i.split('|')for i in self.zip.read(key).decode().replace('\t','').splitlines()]if j[-2]=='scientific name'}
            self.content['revnames']=dict(zip(*[*zip(*names.items())][::-1]))
            return names
        elif key=='revnames':
            self.print(f'require {self.name}/names.dmp')
            revnames=dict(zip(*[*zip(*self['names.dmp'].items())][::-1]))
            self.print(f'loading {self.name}/revnames ...',end=' ')
            return revnames
        elif key=='fullnamelineage.dmp':
            return {j[0]:j[2]for j in[i.split('|')for i in self.zip.read(key).decode().replace('\t','').splitlines()]}
    def open(self,file):
        self.zip=ZipFile(file)
        self.config(text=f'{file}')
        self.filenames=self.zip.namelist()+['revnames']
        use=['fullnamelineage.dmp','names.dmp','rankedlineage.dmp']
        if all(i in self.filenames for i in use):
            self.name='new_taxdump.zip'
        else:
            showerror('Error!','There are files missing in the archive. Are you sure you have downloaded new-taxdump.zip and not taxdmp.zip?')
            self.close()#self.name='taxdmp.zip'
        for i in self.grid:
            self.grid[i].config(bg=('red'if i in use else 'grey')if i in self.filenames else 'systemButtonFace',state=('normal'if i in use else 'disabled')if i in self.filenames else'disabled')
        self.grid['revnames'].config(bg='red',state='normal')
