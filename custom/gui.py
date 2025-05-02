from tkinter import Button,Entry,Frame,LabelFrame,Label,Listbox,Menu,PanedWindow,Toplevel,Scrollbar,IntVar,StringVar,BooleanVar,Pack,Grid,Place
from tkinter.filedialog import askopenfilename,asksaveasfilename
from tkinter.messagebox import showerror,showinfo
from tkinter.ttk import Notebook
from datetime import date
from time import time
from re import sub
from tk2.scrolledframe import ScrolledLabelFrame
from tk2.togglebutton import ToggleButton,ToggleRadioButton
from tk2.contextmenu import RIGHT_MOUSE_BUTTON
from tk2.zoomscale import ZoomScale
from zipfile import ZipFile
__all__=['LoadSave','OpenClose','LogPrinter','WrapperStub','Search','Transceiver','Dashboard',
         'DatabaseProvider','_DatabaseProvider','GB2TaxIdProvider','TaxdumpProvider','ScrolledList','Tree','TreeWrapper']

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
    def __init__(self,master,name,*,text=None,**kw):
        self.name=name
        LabelFrame.__init__(self,master=master,text=text if text else name)
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
    def __init__(self):self.list={};self.menu=Menu(tearoff=0)
    def instance(self,widget,send=1,receive=1,*,row=0,column=1,sticky='nsew',**kw):
        frame=LabelFrame(widget.top,text='Data')
        Button(frame,text='Receive',state='normal'if receive else'disabled',command=lambda:self.recmenu(widget,frame)).grid(row=0,column=0,padx=10,sticky='we')
        Button(frame,text='Send to',state='normal'if send else'disabled',command=lambda:self.sendmenu(widget,frame)).grid(row=1,column=0,padx=10,sticky='we')
        self.list[widget]=(send,receive)
        frame.grid(row=row,column=column,sticky=sticky,**kw)
        frame.bind("<Destroy>", lambda event:self.list.pop(widget))
        return frame
    def invisible_instance(self,widget,send=1,receive=1,*,row=0,column=1,sticky='nsew',**kw):
        self.list[widget]=(send,receive)
        return lambda event:self.list.pop(widget)
    def recmenu(self,widget,frame):
        try:self.menu.destroy()
        except:print('Already destroyed!')
        self.menu = Menu(frame,tearoff=0)
        for i in self.list:
            if self.list[i][0]:self.menu.add_command(label=i.name,command=(lambda j:lambda:widget.receive(j.send()))(i))
        self.menu.tk_popup(frame.winfo_rootx(),frame.winfo_rooty())
    def sendmenu(self,widget,frame):
        self.menu.destroy()
        self.menu = Menu(frame,tearoff=0)
        for i in self.list:
            if self.list[i][1]:self.menu.add_command(label=i.name,command=(lambda j:lambda:j.receive(widget.send()))(i))
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
        self.rowconfigure((0,1)if(orient=='horizontal')else(0,1,2,3),weight=1)
        self.columnconfigure((0,1,2)if(orient=='vertical')else(0,1,2,3),weight=1)
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
        master.bind('<FocusIn>',lambda e:self.window.wm_attributes('-topmost',True))
        self.window.bind('<FocusIn>',lambda e:self.window.wm_attributes('-topmost',False))
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
        master.add(self,text=self.name)
        self.pos=len(master.tabs())-1
        self.config(text='')
    def body(self,master=None):
        self.filenames=[]
        self.zip=None
        _legend=LabelFrame(self.top,text='Legend')
        self.legend(_legend)
        _legend.grid(row=0,column=1,sticky='nsew')
        self.legend=_legend
        self.table=LabelFrame(self.container,text='Click to pre-load files manually')
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
        self.legend.grid(row=0,column=1,columnspan=2,sticky='nsew')
        self.date=Label(self.top,text='',relief='groove')
        self.date.grid(row=1,column=1)
##        self.areyousure=Button(self.top,text='Rebuild Database',command=self.nope)
##        self.areyousure.bind('<Double-1>',self.scram)
##        self.areyousure.grid(row=1,column=2)
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
    def open(self,file):
        _DatabaseProvider.open(self,file)
        try:
            stamp=int(self.zip.read('__date__').decode())
            if 0<=stamp<=32536799999:self.date.config(text=date.fromtimestamp(stamp).isoformat())
            else:self.date.config(text='Incorrect date')
            if (time()-stamp)>15768000:showinfo('Out of date','Your GB2Taxid database is over 6 months old. You should consider rebuilding it.')
        except:
            self.date.config(text='')
            showinfo('No timestamp','Your GB2Taxid database does not have a timestamp. You will not be notified to update your database when it becomes out of date.')
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
class ScrolledList(Listbox):
    default = "<empty>"
    def __init__(self, master, **kw):
        if'text'in kw:text=kw.pop('text')
        else:text=None
        self.frame = LabelFrame(master,text=text)
        self.vbar = vbar = Scrollbar(self.frame, name="vbar")
        self.vbar.pack(side="right", fill="y")
        Listbox.__init__(self,self.frame,exportselection=0,background="white")
        if kw:Listbox.configure(self,kw)
        Listbox.pack(self,fill="both",expand=True)
        vbar["command"] = self.yview
        self["yscrollcommand"] = vbar.set
        self.bind("<ButtonRelease-1>", self.click_event)
        self.bind("<Double-ButtonRelease-1>", self.double_click_event)
        self.bind(RIGHT_MOUSE_BUTTON, self.popup_event)
        self.bind("<Key-Up>", self.up_event)
        self.bind("<Key-Down>", self.down_event)
        self.bind("<Key-Delete>", self.delete_event)
        self.menu=Menu(self,tearoff=0)
        self.clear()
        list_meths = vars(Listbox).keys()
        methods = vars(Pack).keys() | vars(Grid).keys() | vars(Place).keys()
        methods = methods.difference(list_meths)
        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.frame, m))
    def config(self,**kw):
        if 'text'in kw:self.frame.config(text=kw.pop('text'))
        Listbox.config(self,**kw)
    def destroy(self):
        Listbox.destroy(self)
        self.frame.destroy()
    def clear(self):
        self.delete(0, "end")
        self.empty = True
        #self.insert("end", self.default)
    def append(self, item):
        if self.empty:
            self.delete(0, "end")
            self.empty = False
        Listbox.insert(self, "end", str(item))
    def insert(self, index, item):
        if self.empty:
            self.delete(0, "end")
            self.empty = False
        Listbox.insert(self, index, str(item))
    def click_event(self, event):
        self.activate("@%d,%d" % (event.x, event.y))
        index = self.index("active")
        self.select(index)
        self.on_select(index)
        return "break"
    def double_click_event(self, event):
        index = self.index("active")
        self.select(index)
        self.on_double(index)
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
    def delete_event(self, event):
        index = self.index("active")
        self.select(index)
        self.on_delete(index)
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
    def popup_event(self, event):
        self.menu.destroy()
        self.menu=Menu(self,tearoff=0)
        self.make_menu()
        self.activate("@%d,%d" % (event.x, event.y))
        index = self.index("active")
        self.select(index)
        self.make_menu(index)
        self.menu.tk_popup(event.x_root,event.y_root)
        return "break"
    def make_menu(self,index=None):
        pass
class Tree(Frame):
    def __init__(self,master,data,id=0,root=None,**kw):
        Frame.__init__(self,master=master,**kw)
        self.strings=[]
        self.data=[]
        self.buttons=[]
        self.widgets=[]
        i=0
        for i in range(int(len(data))):
            if isinstance(data[i],tuple):
                t=Tree(self,data[i],id,(root if root else self))
                id=t.id
                t.grid(row=i,column=1,sticky='nsew')
                self.strings.append(t)
                self.data.append(t)
                self.widgets.append(t)
            elif isinstance(data[i],float):
                t.enabled=ToggleButton(self,text=data[i],width=len(str(data[i])),font=(None,6),relief='raised')
                t.enabled.grid(row=i-1,column=0,sticky='nsew')
                t.enabled.trace_add('write',t.sel)
                t.widgets.append(t.enabled)
            elif isinstance(data[i],str):
                l=ToggleButton(self,text=data[i],anchor='e',width=len(str(data[i])),font=(None,6),relief='raised')
                l.grid(row=i,column=0,columnspan=2,sticky='nsew')
                l.trace_add('write',lambda*a:self.root.get())
                #l2=Label(self,text=id,anchor='e',width=len(str(data[i])),font=(None,6),relief='raised')
                #l2.grid(row=i,column=2,sticky='nsew')
                self.strings.append(data[i])
                self.data.append(l)
                self.widgets.append(l)
                id+=1
        self.columnconfigure((0,1),weight=1)
        if i:self.rowconfigure(tuple(range(i)),weight=1)
        self.id=id
        self.root=(root if id else self)
        self.flat=self.flatten()
        self.watch=IntVar(self)
        self.trace_add=self.watch.trace_add
        self.get()
    def sel(self,*a):
        for i in self.widgets:
            if i!=self.enabled:
                i.set(self.enabled.get())
        self.root.get()
    def set(self,value):
        self.enabled.set(value)
    def __getitem__(self,key):
        return self.data[key]
    def config(self,**kw):
        if'font'in kw:
            font=kw.pop('font')
            for i in self.widgets:i.config(font=font)
    def flatten(self,depth=0):
        flat=[i for i in self.strings]
        i=0
        while 1:
            if i>=len(flat):break
            if isinstance(flat[i],Tree):
                flat=flat[:i]+flat[i].flatten(depth+1)+flat[i+1:]
            elif isinstance(flat[i],str):i+=1
        return flat
    def get(self,depth=0):
        flat=[i for i in self.data]
        i=0
        while 1:
            if i>=len(flat):break
            if isinstance(flat[i],Tree):
                flat=flat[:i]+flat[i].get(depth+1)+flat[i+1:]
            elif isinstance(flat[i],ToggleButton):i+=1
        if depth:return flat
        else:self.state=[i.get()for i in flat];self.watch.set(self.watch.get()+1);return self.state
    def zoom(self,size):
        self.config(font=(None,size))
class TreeWrapper(WrapperStub):
    format=('Newick','*.nwk *.tree',(('Newick file','*.nwk *.tree'),('Text file','*.txt'),('All files','*')))
    DB=None
    lstype='l'
    def body(self,**kw):
        self.frame=ScrolledLabelFrame(self.container, width=500, borderwidth=2)
        self.tree=Tree(self.frame,tuple());self.tree.pack(fill='both',expand=True)
        self.zoomer=ZoomScale(self.top,from_=1,to=10,default=6,command=self.zoom)
        self.zoomer.grid(row=0,column=1)
        return self.frame
    def load(self,file):
        with open(file)as f:
            self.tree.destroy()
            r1='[0-9]\\.[0-9]{4}';r2='[A-Za-z\\-_.0-9]*?[,)]))|(?:(?<!%s)(?=\\'%r1;left_bootstrap='(?<=\\))(?=%s[,)])'%r1;names='(?:(?<=[(,])(?=%s,\\(*?%s)%s))'%(r2,r2,r1)
            self.tree=Tree(self.frame,eval(sub(left_bootstrap,',',sub(names,"'",f.read()))[:-2]))#Bad! Bad! Potential for arbitrary code execution!
            self.event_generate('<<loadvalues>>')
            self.frame.config(text=file)
            self.tree.pack(fill='both',expand=True)
            self.tree.zoom(self.zoomer.get())
    def zoom(self,size):self.tree.zoom(size)
