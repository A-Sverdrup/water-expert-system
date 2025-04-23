from tkinter.simpledialog import _QueryDialog
from tkinter.messagebox import showerror
from tkinter import Checkbutton,Entry,Frame,Label,LabelFrame,Radiobutton,Spinbox,BooleanVar,StringVar,Grid,Pack,Place
from tkinter.ttk import Combobox
__all__=['CustomDialog','Constant','DBool','DCombo','DCombo2','DSpin','Group','NoneVar','Option','RadioCheck','RadioGroup','askcustom','showlines']
class RadioCheck(LabelFrame):
    def __init__(self,master=None,text=None,type=None,default=True,**kw):
        if type=='radio':
            self.switch=kw['variable']
            self.radiovalue=kw['value']
        if'variable'in kw:del kw['variable']
        if'value'in kw:del kw['value']
        LabelFrame.__init__(self,master=master,text=text,relief='flat'if text==None else None,**kw)
        self.enabled=BooleanVar(self,value=True)
        self.type=type
        if type=='radio':
            radio=Radiobutton(self,width=0,variable=self.switch,value=self.radiovalue)
            self.switch.trace_add('write',self.state)
            radio.bind('<Button-2>',lambda e:radio.deselect())
            radio.bind('<Button-3>',lambda e:radio.deselect())
            radio.pack(side='left',fill='both',expand=False)
        elif type=='check':
            self.enabled.set(default)
            self.enabled.trace_add('write',self.state)
            Checkbutton(self,width=0,variable=self.enabled).pack(side='left',fill='both',expand=False)
    def get(self):
        if self.type=='radio':
            return self.switch.get()==self.radiovalue
        else:#elif self.type=='check':
            return self.enabled.get()
    def setwidget(self,widget):
        self.widget=widget
        self.widget.pack(side='left',fill='both',expand='true')
        if self.type=='radio':self.widget.config(state='disabled')
        for m in vars(Pack).keys() | vars(Grid).keys() | vars(Place).keys():
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self.widget, m, getattr(self, m))
    def state(self,*a):
        self.widget.config(state=('normal'if self.get()else'disabled'))
class DSpin(Spinbox):
    def __init__(self,master=None,text=None,type=None,classtype=int,default=True,cnf={},**kw):
        self.frame=RadioCheck(master,text=text,type=type,variable=kw.pop('radiovariable',None),value=kw.pop('radiovalue',None),default=default)
        if'text'in kw:del kw['text']
        self.variable=StringVar(self.frame)
        self.trace_add=self.variable.trace_add
        self.set=self.variable.set
        kw['textvariable']=self.variable
        self.type=classtype
        Spinbox.__init__(self,self.frame,cnf=cnf,**kw)
        self.frame.setwidget(self)
    def get(self):
        if self.frame.get():return self.type(Spinbox.get(self))
    def config(self,cnf={},**kw):
        if'text'in kw:self.frame.config(text=kw['text']);del kw['text']
        Spinbox.config(self,cnf=cnf,**kw)
    def validate(self):
        try:
            self.get()
            return 1
        except ValueError:return 0
class DEntry(Entry):
    def __init__(self,master=None,text=None,type=None,mandatory=True,default=True,cnf={},**kw):
        sefl.mandatory=mandatory
        self.frame=RadioCheck(master,text=text,type=type,variable=kw.pop('radiovariable',None),value=kw.pop('radiovalue',None),default=default)
        if'text'in kw:del kw['text']
        self.variable=StringVar(self.frame)
        self.trace_add=self.variable.trace_add
        self.set=self.variable.set
        kw['textvariable']=self.variable
        self.type=classtype
        Entry.__init__(self,self.frame,cnf=cnf,**kw)
        self.frame.setwidget(self)
    def get(self):
        if self.frame.get():return Entry.get(self)
    def config(self,cnf={},**kw):
        if'text'in kw:self.frame.config(text=kw['text']);del kw['text']
        Entry.config(self,cnf=cnf,**kw)
    def validate(self):
        if self.mandatory:
            if self.get():return 1
            else:showerror('Error','You must enter a value!');return 0
        else:return 1
class DCombo(Combobox):
    def __init__(self,master=None,text=None,type=None,values=[],mandatory=True,default=True,**kw):
        self.mandatory=mandatory
        self.values=values
        self.frame=RadioCheck(master,text=text,type=type,variable=kw.pop('radiovariable',None),value=kw.pop('radiovalue',None),default=default)
        if'text'in kw:del kw['text']
        self.variable=StringVar(self.frame)
        self.trace_add=self.variable.trace_add
        self.set=self.variable.set
        kw['textvariable']=self.variable
        Combobox.__init__(self,master=self.frame,values=self.values,state='readonly',**kw)
        self.frame.setwidget(self)
    def get(self):
        if self.frame.get():return Combobox.get(self)
    def config(self,cnf={},**kw):
        if'text'in kw:self.frame.config(text=kw['text']);del kw['text']
        Spinbox.config(self,cnf=cnf,**kw)
    def validate(self):
        if self.mandatory:
            if self.get():
                try:self.values.index(Combobox.get(self));return 1
                except:showerror('Error','Unknown error!');return 0
            else:showerror('Error','You must select a value!');return 0
        else:return 1
class DCombo2(DCombo):
    def get(self):
        if self.frame.get():return self.values.index(Combobox.get(self))
class Constant(LabelFrame):
    def __init__(self, master=None, title=None, prompt=None, value=None, valid=True, error=None, **kw):
        self.value=value
        self.valid=valid
        self.error=error
        LabelFrame.__init__(self,master=master,text=title,relief=None if title else 'flat')
        Label(self,text=prompt,**kw).pack()
    def get(self):return self.value
    def validate(self):
        if not self.valid:showerror('Error',self.error)
        return self.valid
class Option(Label):
    def __init__(self, master=None, title=None, prompt=None, type=type, value=None, valid=True, error=None, default=True, **kw):
        self.frame=RadioCheck(master,text=title,type=type,variable=kw.pop('radiovariable',None),value=kw.pop('radiovalue',None),default=default)
        self.value=value
        self.valid=valid
        self.error=error
        Label.__init__(self,master=self.frame,text=prompt,**kw)
        self.frame.setwidget(self)
    def get(self):
        if self.frame.get():return self.value
    def validate(self):
        if self.frame.get():
            if not self.valid:showerror('Error',self.error)
            return self.valid
        else:return True
class DBool(Option):
    def get(self):return self.frame.get()
    def validate(self):return self.get()
Constant=Option
class NoneVar(object):
    def get(self):return None
    def config(self,**kw):return None
class Group(Frame):
    def __init__(self, master=None, title=None, type=None, widgets=None, validate=all, error=None, default=True, orient='vertical', **kw):
        self.frame=RadioCheck(master,text=title,type=type,variable=kw.pop('radiovariable',None),value=kw.pop('radiovalue',None),default=default)
        Frame.__init__(self,master=self.frame)
        h=0
        self.title=title
        self.variable=StringVar(self,value='')
        self.validation=validate
        self.error=error
        self.widgets={}
        for i in widgets:
            self.widgets[i]=widgets[i][0](master=self,radiovariable=self.variable,radiovalue=i,*widgets[i][1],**widgets[i][2])
            self.widgets[i].grid(row=(h if orient=='vertical'else 1),column=(h if orient=='horizontal'else 1),padx=5,sticky='we')
            h+=1
        self.frame.setwidget(self)
    def get(self):
        if self.frame.get():
            return{i:self.widgets[i].get()for i in self.widgets}
    def validate(self):
        #self.error=f'Validate {self.title} {self.validation} - {self.error}'
        #print(self.title,self.validation)
        if self.frame.get():
            if self.validation==any:
                if any([self.widgets[i].validate()for i in self.widgets])\
                   and any([(self.widgets[i].get()is not None)for i in self.widgets]):return 1
                elif self.error:showerror('Error',self.error)
            elif self.validation==all:
                if all([self.widgets[i].validate()for i in self.widgets])\
                   and all([(self.widgets[i].get()is not None)for i in self.widgets]):return 1
                elif self.error:showerror('Error',self.error)
            elif self.validation==None:
                return True
            else:
                return self.validation(self.get())#showerror('Error',);return 0
        else:return True
    def config(self,**kw):
        for i in self.widgets:self.widgets[i].config(**kw)
class RadioGroup(Group,Frame):
    def __init__(self, master=None, title=None, type=None, widgets=None, validate='atleastone', default=True, **kw):
        Group.__init__(self, master=master, title=title, type=type, widgets=widgets, validate=validate, default=default, **kw)
        self.widgets['']=NoneVar()
    def get(self):
        if self.frame.get():
            if self.variable.get():return(self.variable.get(),self.widgets[self.variable.get()].get())
            else:return None
    def validate(self):
        #print('radio',self.title,self.validation)
        if self.validation and self.frame.get():
            if self.variable.get():
                a=self.widgets[self.variable.get()].validate()
                #print('radio2',a)
                return a
            else:showerror('Error','You must select an option!');return 0
        else:return True

class CustomDialog(_QueryDialog):
    def body(self, master):
        Label(master,text=self.prompt,justify='center').grid(row=0,columnspan=2,padx=5,sticky='we')
        self.group=self.minvalue[0](master,*self.minvalue[1],**self.minvalue[2])
        self.group.grid(row=1,column=0,sticky='we')
        return self.group
    def getresult(self):
        return self.group.get()
    def validate(self):
        result = self.getresult()
        v1=self.group.validate()
        v2=(self.initialvalue(result)if self.initialvalue else True)
        if v1 and v2:
            self.result=result
            return 1
        else:
            #print('v',v1, v2)
            self.result=None
            return 0
def askcustom(title=None, prompt=None, widget=None, validate=None, **kw):
    '''inputs: {'name':(Class,[args],{'kw':'kwargs}),}
       outputs: {'name':(Class,[args],{'kw':'kwargs}),}'''
    d = CustomDialog(title, prompt, minvalue=widget, initialvalue=validate, **kw)
    return d.result

class LineDisplay(_QueryDialog):
    def body(self, master):
        l=0
        for i in self.initialvalue:
            Label(master,text=i).grid(row=l,column=0,sticky='nsew')
            a=Entry(master);a.insert(0,self.initialvalue[i]);a.grid(row=l,column=1,sticky='nsew')
            l+=1
        return a
    def getresult(self):
        return None
    def validate(self):
        return 1

def showlines(title=None, prompt=None, values=None, **kw):
    d = LineDisplay(title, prompt, initialvalue=values, **kw)
    return d.result
