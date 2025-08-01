from tkinter import Button,Entry,Frame,LabelFrame,Label,Listbox,Menu,PanedWindow,Scrollbar,Toplevel,IntVar,StringVar,BooleanVar,Pack,Grid,Place
from tkinter.filedialog import askopenfilename,asksaveasfilename
from tkinter.messagebox import showerror,showinfo
from tkinter.ttk import Notebook,Progressbar,Treeview
from datetime import datetime
from time import time
from re import sub,match,search
from sys import platform
from tk2.scrolledframe import ScrolledLabelFrame
from tk2.togglebutton import ToggleButton,ToggleRadioButton
from tk2.contextmenu import RIGHT_MOUSE_BUTTON
from tk2.zoomscale import ZoomScale
from tk2.omnientry import OmniEntry
from zipfile import ZipFile
from webbrowser import open as webopen
from strings import STRINGS,LANGUAGE
__all__=['LoadSave','LogPrinter','WrapperStub','Search','Transceiver','Dashboard',
         'DatabaseProvider','_DatabaseProvider','GB2TaxIdProvider','TaxdumpProvider',
         'ScrolledList','TreeViewMSL','Tree','TreeWrapper','ProgressLogger','Link']
#LANGUAGE='EN'
class LoadSave(LabelFrame):
    def __init__(self,master,type,defaultextension,filetypes,*,name=None,open=None,load=None,save=None,unload=None,unloadall=None,close=None):
        LabelFrame.__init__(self,master=master,text=name if name else STRINGS.loc['GUI::LOADSAVE',LANGUAGE])
        self.type=type
        self.de=defaultextension
        self.ft=filetypes
        self.open=open
        self.load=load
        self.save=save
        self.unload=unload
        self.unloadall=unloadall
        self.close=close
        row=0
        if open:Button(self,text=STRINGS.loc['GUI::LOADSAVE:open',LANGUAGE].format(type),command=lambda:self.wrapopen(self.open)).grid(row=row,column=0,padx=10,sticky='we');row+=1
        if load:Button(self,text=STRINGS.loc['GUI::LOADSAVE:load',LANGUAGE].format(type),command=lambda:self.wrapopen(self.load)).grid(row=row,column=0,padx=10,sticky='we');row+=1
        if save:Button(self,text=STRINGS.loc['GUI::LOADSAVE:save',LANGUAGE].format(type),command=self.F2).grid(row=row,column=0,padx=10,sticky='we');row+=1
        if unload:Button(self,text=STRINGS.loc['GUI::LOADSAVE:unload',LANGUAGE].format(type),command=lambda:self.wrap(self.unload,self.B4)).grid(row=row,column=0,padx=10,sticky='we');row+=1
        if unloadall:Button(self,text=STRINGS.loc['GUI::LOADSAVE:unloadall',LANGUAGE],command=lambda:self.wrap(self.unloadall,self.B5)).grid(row=row,column=0,padx=10,sticky='we');row+=1
        if close:Button(self,text=STRINGS.loc['GUI::LOADSAVE:close',LANGUAGE].format(type),command=lambda:self.wrap(self.close,self.B6)).grid(row=row,column=0,padx=10,sticky='we');row+=1
    def wrapopen(self,func):
        if (file:=askopenfilename(defaultextension=self.de,filetypes=self.ft)):
##            try:
            func(file)
##            except:showerror('Fail!','Cannot load %s file!'%self.type)
    def F2(self):
        if (file:=asksaveasfilename(defaultextension=self.de,filetypes=self.ft)):
##            try:
            self.save(file)
##            except:showerror('Fail!','Cannot save %s file!'%self.type)
    def wrap(self,func,string):
        #try:
        func()
        #except:showerror('Fail!','Cannot '+f'{string[0].lower()+string[1:]%self.type} file!'if string!=self.B5 else(self.B5+'!'))
class WrapperStub(LabelFrame):
    lstype='ls'
    def __init__(self,master,name,*,text=None,**kw):
        self.name=name
        LabelFrame.__init__(self,master=master,text=text if text else name)
        self.container=PanedWindow(self,orient='vertical')
        self.container.pack(fill='both',expand=True)
        self.top=Frame(self.container)
        self.ls=None
        if bool(self.lstype):
            self.ls=LoadSave(self.top,*self.format,
                             name=(self.lsname if('n'in self.lstype)else None),
                             open=(self.open if('o'in self.lstype)else None),
                             load=(self.load if('l'in self.lstype)else None),
                             save=(self.save if('s'in self.lstype)else None),
                             unload=(self.unload if('u'in self.lstype)else None),
                             unloadall=(self.unloadall if('a'in self.lstype)else None),
                             close=(self.close if('c'in self.lstype)else None)
                             )
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
    def instance(self,widget,send=1,receive=1,orient='vertical',*,row=0,column=1,sticky='nsew',**kw):
        frame=LabelFrame(widget.top,text=STRINGS.loc['GUI::TRANSCEIVER',LANGUAGE])
        Button(frame,text=STRINGS.loc['GUI::TRANSCEIVER:receive',LANGUAGE],state='normal'if receive else'disabled',command=lambda:self.recmenu(widget,frame)).grid(row=0,column=0,padx=10,sticky='we')
        Button(frame,text=STRINGS.loc['GUI::TRANSCEIVER:send',LANGUAGE],state='normal'if send else'disabled',command=lambda:self.sendmenu(widget,frame)).grid(row=(1 if orient=='vertical'else 0),column=(1 if orient=='horizontal'else 0),padx=10,sticky='we')
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
        self.lang={
            'all':str(STRINGS.loc['GUI::DASHBOARD:all',LANGUAGE]),
            'fail':str(STRINGS.loc['GUI::DASHBOARD:fail',LANGUAGE]),
            'done':str(STRINGS.loc['GUI::DASHBOARD:done',LANGUAGE]),
            'left':str(STRINGS.loc['GUI::DASHBOARD:left',LANGUAGE]),
            'elapsed':str(STRINGS.loc['GUI::DASHBOARD:elapsed',LANGUAGE]),
            'ETA':str(STRINGS.loc['GUI::DASHBOARD:ETA',LANGUAGE]),
            }
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
            for i in kw:self.dict[i].config(text=self.lang[i].format(kw[i]))
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
        self.window.title(STRINGS.loc['DB::PROVIDER',LANGUAGE])
        self.deiconify=self.window.deiconify
        self.withdraw=self.window.withdraw
        self.window.withdraw()
        Notebook.__init__(self,master=self.window)
        self.pack(fill='both',expand=True)
class _DatabaseProvider(WrapperStub,LogPrinter):
    printer=None
    name=None
    lstype='oc'
    legend=True
    def __init__(self,master=None,**kw):
        self.master=master
        self.kw=kw
        WrapperStub.__init__(self,master=master,name=self.name)
        master.add(self,text=self.name)
        self.pos=len(master.tabs())-1
        self.config(text='')
    def body(self,master=None):
        self.filenames=[]
        self.zip=None
        if self.legend:
            self.legend=LabelFrame(self.top,text=STRINGS.loc['DB::LEGEND',LANGUAGE])
            self.make_legend(self.legend)
            self.legend.grid(row=0,column=1,sticky='nsew')
        self.table=LabelFrame(self.container,text=STRINGS.loc['DB::MANUAL_ADVICE',LANGUAGE])
        self.body2(self.table)
        return self.table
    def __call__(self):
        self.master.deiconify()
        self.master.select(self.pos)
    def make_legend(self,legend):
        Label(legend,relief='groove',font=(None,4),width=2).grid(row=0,column=0)
        Label(legend,text=STRINGS.loc['DB::LEGEND:UNAVAILABLE',LANGUAGE]).grid(row=0,column=1)
        Label(legend,relief='groove',font=(None,4),bg='red',width=2).grid(row=0,column=2)
        Label(legend,text=STRINGS.loc['DB::LEGEND:AVAILABLE',LANGUAGE]).grid(row=0,column=3)
        Label(legend,relief='groove',font=(None,4),bg='green',width=2).grid(row=0,column=4)
        Label(legend,text=STRINGS.loc['DB::LEGEND:LOADED',LANGUAGE]).grid(row=0,column=5)
    def __getitem__(self,key):
        #try:
        if isinstance(key,tuple) and len(key)==2:return self[key[0]][key[1]]
        elif isinstance(key,tuple) and len(key)==3:return self[key[0]].get(key[1],key[2])
        elif key in self.content:return self.content[key]
        elif key in self.filenames:self.load(key);return self[key]
        else:return {}
        #except AttributeError:return ''
    def load(self,key):
        self.print(f'loading {self.name}/{key} ... ',end=' ')
        self.content[key]=self.read(key)
        self.buttongrid[key].config(bg='green')
        self.print(f'done',end='\n')
    def open(self,file):
        try:
            self.zip=ZipFile(file)
            self.config(text=f'{file}')
            self.filenames=self.zip.namelist()
            for i in self.buttongrid:
                self.buttongrid[i].config(bg='red'if i in self.filenames else 'systemButtonFace',state='normal'if i in self.filenames else'disabled')
            return True
        except FileNotFoundError:
            showerror(STRINGS.loc['MISC::ERROR',LANGUAGE],STRINGS.loc['MISC::FILE_NOT_FOUND',LANGUAGE].format(file))
            self.close()
            return False
    def close(self):
        if self.zip:
            self.zip.close()
            self.zip=None
            self.config(text='')
        self.filenames=[]
        for i in self.buttongrid:
            self.buttongrid[i].config(bg='systemButtonFace',state='disabled')
    def save(self):None
class GB2TaxIdProvider(_DatabaseProvider):
    printer=None
    name=STRINGS.loc['DB::GB2TAXID',LANGUAGE]
    format=[STRINGS.loc['DB::DB',LANGUAGE],'*.zip',((STRINGS.loc['FORMAT::ZIP',LANGUAGE],'*.zip'),)]
    def body2(self,master):
        self.ls.grid(row=0,column=0,rowspan=2)
        self.legend.grid(row=0,column=1,columnspan=2,sticky='nsew')
        d=LabelFrame(self.top,text='Created')
        self.date=Label(d,text='',relief='groove')
        self.date.pack(fill='both',expand=True)
        d.grid(row=1,column=1,sticky='nsew')
        db=LabelFrame(self.top,text=STRINGS.loc['DB::MANAGE',LANGUAGE])
        db.grid(row=1,column=2,sticky='nsew')
        self.areyousure=Button(db,text=STRINGS.loc['DB::REBUILD',LANGUAGE],state=('normal'if('sevenz'in self.kw)and self.kw['sevenz']else'disabled'),command=self.nope)
        self.areyousure.pack(side='left',fill='both',expand=True)
        if('sevenz'not in self.kw)or(not self.kw['sevenz']):Label(db,text='7-Zip: Unavailable',state='disabled',relief='groove').pack(side='left',fill='both',expand=True)
        else:self.areyousure.bind('<Double-1>',self.scram)
        alph='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.buttongrid={}
        master.rowconfigure(tuple(range(36)),weight=1)
        master.columnconfigure(tuple(range(36)),weight=1)
        for i in range(36):
            Label(master,text=alph[i],font=(None,5),relief='raised').grid(row=0,column=i+1,sticky='nsew')
        for i in range(10,36):
            Label(master,text=alph[i],font=(None,5),relief='raised').grid(row=i+1-10,column=0,sticky='nsew')
            for j in range(36):
                a=alph[i]+alph[j]
                self.buttongrid[a]=Button(master,text=a,font=(None,5),width=1,height=1,relief='groove',state='disabled',command=(lambda f:lambda:self.load(f))(a))
                self.buttongrid[a].grid(row=i+1-10,column=j+1,sticky='nsew')
        self.content={}
    def open(self,file):
        if _DatabaseProvider.open(self,file):
            try:
                stamp=float(self.zip.read('__date__').decode())
                if 0<=stamp<=32536799999:self.date.config(text=datetime.fromtimestamp(stamp).isoformat(' '))
                else:self.date.config(text=STRINGS.loc['DB::GB2TAXID:INCORRECT',LANGUAGE])
                if (time()-stamp)>15768000:showinfo(STRINGS.loc['DB::GB2TAXID:OUTDATED',LANGUAGE],STRINGS.loc['DB::GB2TAXID:OUTDATED_MESSAGE',LANGUAGE])
            except KeyError:
                self.date.config(text=STRINGS.loc['DB::GB2TAXID:UNKNOWN',LANGUAGE])
                showinfo(STRINGS.loc['DB::GB2TAXID:UNDATED',LANGUAGE],STRINGS.loc['DB::GB2TAXID:UNDATED_MESSAGE',LANGUAGE])
    def nope(self):
        self.areyousure.config(text=STRINGS.loc['DB::GB2TAXID:REBUILD',LANGUAGE])
        self.after(5000,lambda:self.areyousure.config(text=STRINGS.loc['DB::REBUILD',LANGUAGE]))
    def scram(self,event):self.rebuild()
    def read(self,key):
        return dict([i.split(';')for i in self.zip.read(key).decode().splitlines()])
    def close(self):
        _DatabaseProvider.close(self)
        self.date.config(text='')
class TaxdumpProvider(_DatabaseProvider):
    printer=None
    name=STRINGS.loc['DB::TAXDUMP',LANGUAGE]
    format=[STRINGS.loc['DB::DB',LANGUAGE],'*.zip',((STRINGS.loc['FORMAT::ZIP',LANGUAGE],'*.zip'),)]       
    def body2(self,master):
        db=LabelFrame(self.top,text=STRINGS.loc['DB::MANAGE',LANGUAGE])
        db.grid(row=0,column=2,sticky='nsew')
        Button(db,text='Update',command=lambda:Link('https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/new_taxdump/new_taxdump.zip','Download update')).grid(row=0,column=0,sticky='nsew')
        left=['citations.dmp','delnodes.dmp','division.dmp','gc.prt','gencode.dmp','images.dmp','merged.dmp','names.dmp','nodes.dmp']
        right=['excludedfromtype.dmp','fullnamelineage.dmp','host.dmp','rankedlineage.dmp','taxidlineage.dmp','typematerial.dmp','typeoftype.dmp']
        self.buttongrid={}
        h=0
        master.rowconfigure(tuple(range(9)),weight=1)
        master.columnconfigure((0,1),weight=1)
        for i in left:
            self.buttongrid[i]=Button(master,text=i,relief='groove',state='disabled',command=(lambda f:lambda:self.load(f))(i))
            self.buttongrid[i].grid(row=h,column=0,sticky='nsew')
            h+=1
        h=0
        for i in right:
            self.buttongrid[i]=Button(master,text=i,relief='groove',state='disabled',command=(lambda f:lambda:self.load(f))(i))
            self.buttongrid[i].grid(row=h,column=1,sticky='nsew')
            h+=1
        self.content={}
        self.buttongrid['revnames']=Button(master,text='<Reverse name lookup>\n(Auto-generated)',relief='groove',state='disabled',command=lambda:self.load('revnames'))
        self.buttongrid['revnames'].grid(row=h,column=1,rowspan=2,sticky='nsew')
    def make_legend(self,legend):
        Label(legend,relief='groove',font=(None,4),width=2).grid(row=0,column=0)
        Label(legend,text=STRINGS.loc['DB::LEGEND:UNAVAILABLE',LANGUAGE]).grid(row=0,column=1)
        Label(legend,relief='groove',font=(None,4),bg='grey',width=2).grid(row=0,column=2)
        Label(legend,text=STRINGS.loc['DB::LEGEND:UNSUPPORTED',LANGUAGE]).grid(row=0,column=3)
        Label(legend,relief='groove',font=(None,4),bg='red',width=2).grid(row=1,column=0)
        Label(legend,text=STRINGS.loc['DB::LEGEND:AVAILABLE',LANGUAGE]).grid(row=1,column=1)
        Label(legend,relief='groove',font=(None,4),bg='green',width=2).grid(row=1,column=2)
        Label(legend,text=STRINGS.loc['DB::LEGEND:LOADED',LANGUAGE]).grid(row=1,column=3)
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
        try:
            self.zip=ZipFile(file)
            self.config(text=f'{file}')
            self.filenames=self.zip.namelist()+['revnames']
            use=['fullnamelineage.dmp','names.dmp','rankedlineage.dmp']
            if all(i in self.filenames for i in use):
                self.name='new_taxdump.zip'
            else:
                showerror(STRINGS.loc['MISC::ERROR',LANGUAGE],STRINGS.loc['DB::TAXDUMP:ERROR',LANGUAGE])
                self.close()
            for i in self.buttongrid:
                self.buttongrid[i].config(bg=('red'if i in use else 'grey')if i in self.filenames else 'systemButtonFace',state=('normal'if i in use else 'disabled')if i in self.filenames else'disabled')
            self.buttongrid['revnames'].config(bg='red',state='normal')
        except FileNotFoundError:
            showerror(STRINGS.loc['MISC::ERROR',LANGUAGE],STRINGS.loc['MISC::FILE_NOT_FOUND',LANGUAGE].format(file))
            self.close()
            return False
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
class TreeViewMSL(LabelFrame):
    def __init__(self, root, columns, text=None, width=500):
        LabelFrame.__init__(self,master=root,text=text)
        self.column_count=len(columns)
        #style=Style()
        self.tree=Treeview(self, columns=columns[1:])
        #style.configure('Treeview',rowheight=24)
        Li=[len(i)for i in columns];S=sum(Li)
        i=0
        for col in['#0',*self.tree['columns']]:self.tree.column(col, width=int(width*Li[i]/S));i+=1
        for col in columns[1:]:self.tree.heading(col, text=col);self.tree.column(col, anchor='w')
        self.tree.heading('#0', text=columns[0])
        self.tree.pack(side='left',expand=True, fill='both')
        scrollbar=Scrollbar(root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side='right',fill='y',expand=True)
        self.tree.bind('<<TreeviewSelect>>',self.select_event)
        self.tree.bind('<Double-1>',self.double_click_event)
        self.tree.bind(RIGHT_MOUSE_BUTTON,self.right_click_event)
        self.tree.bind('<Key-Delete>',self.delete_event)
        self.data={}
        self.rev_data={}
    def append(self,values):
        self.data[values]=self.tree.insert('','end',text=values[0],values=values[1:],open=True)
        self.rev_data[self.data[values]]=values
        return self.data[values]
    def delete(self,value):
        self.tree.delete(self.data[value])
    def event_handler(self, event, function):
        if item:=self.selection():
            data=self.rev_data.get(item)
            function(data)
    def selection(self):
        selected_item=self.tree.selection()
        if selected_item:return self.rev_data.get(selected_item[0])
    def select_event(self, event):self.event_handler(event,self.on_select)
    def double_click_event(self, event):self.event_handler(event,self.on_double)
    def right_click_event(self, event):self.event_handler(event,self.on_right)
    def delete_event(self, event):self.event_handler(event,self.on_right)
    def on_select(self, data):pass
    def on_double(self, data):pass
    def on_right(self, data):pass
    def on_delete(self, data):pass
class Tree(Frame):
    def __init__(self,master,data,root=None,level=0,name=None,**kw):
        Frame.__init__(self,master=master,
                       #border=1,relief='solid',highlightbackground='green', highlightthickness=2,
                       **kw)
        self.name=name
        self.strings=[]
        self.data=[]
        self.buttons=[]
        self.widgets=[]
        if not root:root=self
        self.root=root
        i=0
        self.watch=IntVar(self)
        self.trace_add=self.watch.trace_add
        def makeui(data,root=self):
            if isinstance(data[-1],float):bootstrap=1
            else:bootstrap=0
            for i in range(len(data)-bootstrap):
                if isinstance(data[i],str):
                    l=ToggleButton(root,text=data[i],anchor='e',width=len(str(data[i]))-8,font=(None,6),relief='raised')
                    l.grid(row=i,column=bootstrap,sticky='nsew')
                    l.trace_add('write',lambda*a:self.root.get())
                    self.strings.append(data[i])
                    self.data.append(l)
                    self.widgets.append(l)
                elif isinstance(data[i],tuple):
                    t=Tree(root,data[i],(root if root else self),level+1,name=name+str(level))
                    t.grid(row=i,column=bootstrap,sticky='nsew')
                    self.strings.append(t)
                    self.data.append(t)
                    self.widgets.append(t)
            if bootstrap:
                self.enabled=ToggleButton(root,text=data[-1],width=len(str(data[-1])),font=(None,6),relief='raised')
                self.enabled.grid(row=0,column=0,rowspan=i+1,sticky='nsew')
                self.enabled.trace_add('write',self.sel)
                self.widgets.append(self.enabled)
        if data:makeui(data)
        self.columnconfigure((0,1),weight=1)
        if i:self.rowconfigure(tuple(range(i)),weight=1)
        self.flat=self.flatten()
        self.get()
    def sel(self,*a):
        for i in self.widgets:
            if i!=self.enabled:i.set(self.enabled.get())
        self.get()
    def set(self,value):self.enabled.set(value)
    def __getitem__(self,key):return self.data[key]
    def config(self,**kw):
        if'font'in kw:
            font=kw.pop('font')
            for i in self.widgets:i.config(font=font)
    def flatten(self):
        flat=[i for i in self.strings]
        i=0
        while 1:
            if i>=len(flat):break
            if isinstance(flat[i],Tree):flat=flat[:i]+flat[i].flatten()+flat[i+1:]
            elif isinstance(flat[i],str):i+=1
        return flat
    def get(self,depth=0):
        flat=[i for i in self.data]
        i=0
        while 1:
            if i>=len(flat):break
            if isinstance(flat[i],Tree):flat=flat[:i]+flat[i].get(depth+1)+flat[i+1:]
            elif isinstance(flat[i],ToggleButton):i+=1
        if depth:return flat
        else:
            self.state=[i.get()for i in flat];
            self.watch.set(self.watch.get()+1)#self.event_generate('<<treeselect>>')            
            if self.root!=self:self.root.get()
            return self.state
    def zoom(self,size):self.config(font=(None,size))
def parse_newick(newick):# Function to recursively parse the Newick string
    subtree = newick.strip()# Remove any whitespace
    if match(r'^[\w\s\-\.\/:;]*$', subtree):return subtree# Base case: if the subtree is just a node (A1, A2, etc.)
    elif match(r"^\'[\w\s\-\.,\/:;]*\'$", subtree):return subtree[1:-1]# Base case: if the subtree is just a node (A1, A2, etc.)
    last_close = subtree.rfind(')')# Find the last closing parenthesis to identify the bootstrap value
    if last_close == -1:raise ValueError("Invalid Newick format")# If there are no closing parenthesis,the tree is invalid.
    before_last_close = subtree[:last_close].strip()# Extract the part before the last closing parenthesis
    if before_last_close[0]=='(':before_last_close=before_last_close[1:]
    after_last_close = subtree[last_close+1:].strip()
    bootstrap_match = search(r'(\d+(\.\d+)?)$', after_last_close)# Check for bootstrap value
    if bootstrap_match:bootstrap_value = float(bootstrap_match.group(1))
    else:bootstrap_value = None
    def split_siblings(subtree):
        stack=0;split_indices=[];in_quotes=False
        for i,char in enumerate(subtree):
            if char == "'":in_quotes=not in_quotes
            if char=='(':stack+=1
            elif char==')':stack-=1
            elif char==','and stack==0 and not in_quotes:split_indices.append(i)# Only split at top-level commas
        if not split_indices:return [subtree]# If no split indices found, return the subtree as is
        siblings=[];start_index=0
        for index in split_indices: # Split the subtree at the found indices
            siblings.append(subtree[start_index:index].strip())
            start_index=index+1
        siblings.append(subtree[start_index:].strip())  # Add the last segment
        return siblings
    parsed_left_subtrees=[parse_newick(sibling)for sibling in split_siblings(before_last_close)]# Parse each sibling and return as a tuple
    return tuple([*parsed_left_subtrees,bootstrap_value])
class TreeWrapper(WrapperStub):
    format=('Newick','*.nwk *.tree',((STRINGS.loc['FORMAT::NWK',LANGUAGE],'*.nwk *.tree'),(STRINGS.loc['FORMAT::TXT',LANGUAGE],'*.txt'),(STRINGS.loc['FORMAT::*',LANGUAGE],'*')))
    DB=None
    lstype='l'
    def body(self,**kw):        
        self.frame=ScrolledLabelFrame(self.container, width=500, borderwidth=2)
        self.tree=Tree(self.frame,tuple(),name=self.name);self.tree.pack(fill='both',expand=True)
        self.zoomer=ZoomScale(self.top,from_=1,to=10,default=6,command=self.zoom)
        self.zoomer.grid(row=0,column=1)
        return self.frame
    def load(self,file):
        try:
            with open(file)as f:
                self.tree.destroy()
                nwkdata=parse_newick(f.read())
                self.tree=Tree(self.frame,nwkdata,name=self.name)
                self.event_generate('<<loadvalues>>')
                self.frame.config(text=file)
                self.tree.pack(fill='both',expand=True)
                self.tree.zoom(self.zoomer.get())
        except FileNotFoundError:
            showerror(STRINGS.loc['MISC::ERROR',LANGUAGE],STRINGS.loc['MISC::FILE_NOT_FOUND',LANGUAGE].format(file))
        #except ValueError:
        #    showerror('Error!','This is not a valid Newick tree')
    def zoom(self,size):self.tree.zoom(size)
class ProgressLogger(Toplevel):
    def __init__(self,master,maximum=None):
        Toplevel.__init__(self,master=master)
        self.root=master
        self.title(STRINGS.loc['MISC::PLEASE_WAIT',LANGUAGE])
        self.protocol('WM_DELETE_WINDOW',lambda*a:None)
        self.root.withdraw()if platform=='darwin' else self.root.wm_attributes('-disabled',True)
        frame=Frame(self)
        frame.pack(padx=25,pady=25,fill='both',expand=True)
        self.text=Label(frame,text='',width=30,height=2)
        self.text.pack(fill='x',expand=True)
        if maximum is not None:self.progress=Progressbar(frame,orient='horizontal',maximum=maximum,mode='determinate')
        else:self.progress=Progressbar(frame,orient='horizontal',mode='indeterminate');self.progress.start()
        self.maximum=maximum
        self.progress.pack(fill='x',expand=True)
        self.resizable(0,0)
        self.wm_attributes('-topmost',True)
        self.root.wm_attributes('-topmost',False)
        self.deiconify()
        self.focus_set()
        self.focus_force()
    def step(self,text,amount=None):
        self.text.config(text=text)
        if self.maximum:self.progress.step(amount)
        self.update()
        self.update_idletasks()
    def close(self):
        self.root.deiconify()if platform=='darwin' else self.root.wm_attributes('-disabled',False)
        self.destroy()
class Link(Toplevel):
    def __init__(self,link,title='Internet link'):
        Toplevel.__init__(self)
        self.title(title)
        self.entry=OmniEntry(self,width=min(len(link),50),scrolling=len(link)>50,log_buttons=False,state='readonly')
        self.entry.insert('end',link)
        self.entry.pack(fill='both',expand=True)
        f=Frame(self)
        f.pack(fill='both',expand=True)
        Button(f,text='Copy',command=self.entry.copy).pack(side='left',fill='both',expand=True)
        Button(f,text='Open in browser',command=lambda:webopen(link)).pack(side='left',fill='both',expand=True)
        Button(self,text='Close',command=self.destroy).pack()
        self.deiconify()
        self.wm_attributes('-topmost',True)
        self.entry.focus_set()
        self.entry.focus_force()
