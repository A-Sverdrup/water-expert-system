'''
tkinter OptionMenu, but it actually works,
and is not based on obsolete Menubutton widget

LabelMenu:  a self-made OptionMenu made from a label and a button.
ButtonMenu: a self-made clickable OptionMenu made from two buttons.
OptionButton: a self-made clickable OptionMenu made from a single button.
EntryMenu: an Option menu you can type in, with input validation and numerical data support.


LabelMenu2, ButtonMenu2, OptionButton2: similar widgets which show labels differing from values
'''
__all__ = ['ButtonMenu','LabelMenu','EntryMenu', 'OptionButton','ButtonMenu2','LabelMenu2', 'OptionButton2']

from tkinter import Button, Frame, Entry, Label, Menu, BooleanVar, IntVar, StringVar, DoubleVar, Variable

class _OptionMenu(Frame,Variable):
    '''Base class for LabelMenu, ButtonMenu and EntryMenu'''
    def __init__(self, master=None, values=None, default=None, variable=StringVar, **kw):
        self.variable=variable
        width= None if'width'not in kw else kw['width']
        Frame.__init__(self,master=master,**kw)
        variable.__init__(self,master=master,value=default)
        self.body(width)
        self.button = Button(self, text='...',command=self.open)
        self.button.pack(side='right',fill='both')
        self.menu = Menu(self,tearoff=0)
        self.values=values
        self.trace_add('write',self.update_body)
        self.update_body()
        #if default!=None:
        #    self.set(default)
    def open(self):
        self.menu.destroy()
        self.menu = Menu(self,tearoff=0)
        self.fill_menu()
        self.menu.tk_popup(self.winfo_rootx(),self.winfo_rooty())
    def body(self,*args):
        pass
    def update_body(self,*args):
        pass
    def fill_menu(self):
        for i in range(len(self.values)):
            self.menu.add_command(label=str(self.values[i]),command=(lambda e:lambda:self.set(self.values[e]))(i))
class ButtonMenu(_OptionMenu):
    def body(self,*a):
        self.button2=Button(self,justify='right',command=self.open)
        self.button2.pack(side='left',fill='x',expand=True)
    def update_body(self,*args):
        self.button2.config(text=str(self.get()))
class LabelMenu(_OptionMenu):
    def body(self,*a):
        self.label=Label(self,justify='right')
        self.label.pack(side='left',fill='x',expand=True)
    def update_body(self,*args):
        self.label.config(text=str(self.get()))
def _booltest(boolean):
    if boolean=='True':return True
    elif boolean=='False':return False
    else:raise ValueError("Invalid literal for a boolean!")
class EntryMenu(_OptionMenu):
    def __init__(self, master=None, values=None, default=None, variable=StringVar, *, strict=False, min=None, max=None, **kw):
        if strict and values==None:
            raise ValueError("Cannot use strict input without values!")
        self.strict=strict
        if variable==IntVar: self.__test=int; self.__numeric=True
        elif variable==BooleanVar: self.__test=_booltest; self.__numeric=False
        elif variable==DoubleVar: self.__test=float; self.__numeric=True
        elif variable==StringVar: self.__test=lambda a:a; self.__numeric=False
        else:raise NotImplemented("Unknown variable type")
        if not self.__numeric:
            if min:raise ValueError('bad keyword "min": %s is not a numeric type variable!'%variable)
            if max:raise ValueError('bad keyword "min": %s is not a numeric type variable!'%variable)
            if strict and (min or max):raise ValueError('cannot use minimum/maximum with strict input!')
        else:
            self.min=min if min else float('-inf')
            self.max=max if max else float('inf')
        _OptionMenu.__init__(self,master=master,variable=variable,values=values,default=default,**kw)
    def body(self,width=None):
        self.entry=Entry(self,justify='right',width=width)
        self.entry.pack(side='left',pady=2,fill='x',expand=True)
        self.entry.bind('<Return>',self.validate)
    def update_body(self,*args):
        self.entry.delete(0,'end')
        self.entry.insert(0,str(self.get()))
    def validate(self,key):
        temp=self.entry.get()
        try:
            temp=self.__test(temp)
        except ValueError:
            self.entry.bell()
            self.update_body()
            return"break"
        if self.strict:
            if temp in self.values:
                self.set(temp)
            else:
                self.entry.bell()
                self.update_body()
                return"break"
        elif self.__numeric:
            if self.min<=temp<=self.max:
                self.set(temp)
            else:
                self.entry.bell()
                self.update_body()
                return"break"
        else:
            self.set(temp)
        return ""
    
class OptionButton(_OptionMenu,Button,Variable):
    def __init__(self, master=None, values=None, default=None, variable=StringVar, **kw):
        kw['command']=self.open
        Button.__init__(self,master=master,**kw)
        variable.__init__(self,master=master,value=default)
        self.menu = Menu(self,tearoff=0)
        self.values=values
        self.fill_menu()
        self.trace_add('write',self.update_body)
        if default!=None:
            self.set(default)    
    
    def update_body(self,*args):
        self.config(text=str(self.get()))

class _OptionMenu2():
    '''Base class for LabelMenu2, ButtonMenu2 and EntryMenu2'''
    def fill_menu(self):
        for i in self.values:
            self.menu.add_command(label=i,command=(lambda j:lambda:self.set(self.values[j]))(i))
class ButtonMenu2(_OptionMenu2,ButtonMenu):
    def update_body(self,*args):
        self.button2.config(text=dict(reversed(i)for i in self.values.items())[self.get()])
class LabelMenu2(_OptionMenu2,LabelMenu):
    def update_body(self,*args):
        self.label.config(text=dict(reversed(i)for i in self.values.items())[self.get()])
class OptionButton2(_OptionMenu2,OptionButton):
    def update_body(self,*args):
        self.config(text=dict(reversed(i)for i in self.values.items())[self.get()])

if __name__ == "__main__":
    from tkinter import Tk
    root=Tk()
    root.title('OptionMenu1')
    labels=['ButtonMenu','OptionButton','LabelMenu','','EntryMenu (non-strict)','EntryMenu (strict)','EntryMenu (range min=-10 max=10)']
    labels2=['StringVar','BooleanVar\nUnsolvable:\nBad format!','IntVar','DoubleVar']
    for i in range(len(labels)):Label(root,text=labels[i]).grid(row=i+1,column=0,sticky='nsew')
    for i in range(len(labels2)):Label(root,text=labels2[i]).grid(row=0,column=i+1,sticky='nsew')

    row=1
    for widget in [ButtonMenu, OptionButton, LabelMenu, EntryMenu]:
        widget(root,['Option1','Option2','Option3'],'ButtonMenu').grid(row=row,column=1,sticky='nsew')
        widget(root,[False,True],False,BooleanVar).grid(row=row,column=2,sticky='nsew')
        widget(root,[1,2,3],1,IntVar).grid(row=row,column=3,sticky='nsew')
        widget(root,[-1.0,0.1,1.0],1.0,DoubleVar).grid(row=row,column=4,sticky='nsew')

        row+=1
        
    EntryMenu(root,['Option1','Option2','Option3'],'Option1',strict=True).grid(row=6,column=1,sticky='nsew')
    EntryMenu(root,[False,True],False,BooleanVar,strict=True).grid(row=6,column=2,sticky='nsew')
    EntryMenu(root,[1,2,3],1,IntVar,strict=True).grid(row=6,column=3,sticky='nsew')
    EntryMenu(root,[-1.0,0.1,1.0],1.0,DoubleVar,strict=True).grid(row=6,column=4,sticky='nsew')
    
    EntryMenu(root,[1,2,3],1,IntVar,min=-10,max=10).grid(row=7,column=3,sticky='nsew')
    EntryMenu(root,[-1.0,0.1,1.0],1.0,DoubleVar,min=-10,max=10).grid(row=7,column=4,sticky='nsew')



    root2=Tk()
    root2.title('OptionMenu2')
    labels=['ButtonMenu2', 'OptionButton2', 'LabelMenu2'];labels2=['StringVar','IntVar']
    for i in range(len(labels)): Label(root2,text=labels[i]).grid(row=i+1,column=0,sticky='nsew')
    for i in range(len(labels2)): Label(root2,text=labels2[i]).grid(row=0,column=i*2+1,columnspan=2,sticky='nsew')

    row=1
    for i in [ButtonMenu2, OptionButton2, LabelMenu2]:
        a=ButtonMenu2(root2,{'Key1':'Value1','Key2':'Value2'},'Value1')
        a.grid(row=row,column=1,sticky='nsew')
        
        b=ButtonMenu2(root2,{'One':1,'Two':2},1)
        b.grid(row=row,column=3,sticky='nsew')

        A=Label(root2,relief='ridge');A.grid(row=row,column=2,sticky='nsew');a.trace_add('write',(lambda j,k:lambda*args:k.config(text=j.get()))(a,A))
        B=Label(root2,relief='ridge');B.grid(row=row,column=4,sticky='nsew');b.trace_add('write',(lambda j,k:lambda*args:k.config(text=j.get()))(b,B))
        row+=1

    root.mainloop()
