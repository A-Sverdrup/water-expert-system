'''
tkinter OptionMenu, but it actually works,
and is not based on obsolete Menubutton widget

LabelMenu:  a self-made OptionMenu made from a label and a button.
ButtonMenu: a self-made clickable OptionMenu made from two buttons.
EntryMenu: an Option menu you can type in, with input validation and numerical data support.

OptionButton: a self-made clickable OptionMenu made from a single button.
ButtonEntry: a widget which opens an Entry upon double-click. Supports input validation and numerical data.
'''
__all__ = ['ButtonMenu','LabelMenu','EntryMenu', 'OptionButton', 'ButtonEntry']

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
        if default!=None:
            self.set(default)
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
    
class OptionButton(Button,Variable):
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
    def open(self):
        self.menu.tk_popup(self.winfo_rootx(),self.winfo_rooty())
    def update_body(self,*args):
        self.config(text=str(self.get()))
    def fill_menu(self):
        for i in range(len(self.values)):
            self.menu.add_command(label=str(self.values[i]),command=(lambda e:lambda:self.set(self.values[e]))(i))

class ButtonEntry(_OptionMenu):
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
        self.values=values
        self.variable=variable
        if 'relief' not in kw:kw.update({'relief':'raised','border':2})
        #if 'relief' in kw:relief=kw['relief'];del kw['relief']
        #else:relief='raised'
        Frame.__init__(self,master=master,**kw)
        variable.__init__(self,master=master,value=default)
        self.button = Label(self,text=default,)#relief=relief)
        self.button.bind('<Double-1>',self.open)
        self.button.pack(side='left',fill='both',expand=True)
        #print(self.button['width'])
        self.entry=Entry(self,justify='right')
        self.entry.bind('<Return>',self.validate)
        self.entry.bind('<Escape>',self.close)
        self.entry.bind('<FocusOut>',self.close)
    def open(self,event):
        self.button.pack_forget()
        self.entry.config(width=len(str(self.get())))
        self.entry.pack(side='left',pady=2,fill='x',expand=True)
        self.entry.focus_set()
    def close(self,event=None):
        self.entry.pack_forget()
        self.button.pack(side='left',fill='x',expand=True)
    def update_body(self,*args):
        self.entry.delete(0,'end')
        self.entry.insert(0,str(self.get()))
        self.button.config(text=str(self.get()))
    def validate(self,key):
        self.close()
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
        self.update_body()
        return ""
        
if __name__ == "__main__":
    from tkinter import Tk
    root=Tk()
    labels=['ButtonMenu',
            'OptionButton',
            'LabelMenu',
            '',
            'EntryMenu (non-strict)',
            'EntryMenu (strict)',
            'EntryMenu (range min=-10 max=10)',
            '',
            'ButtonEntry (double-click)',
            ]
    for i in range(len(labels)):
        Label(root,text=labels[i]).grid(row=i+1,column=0,sticky='nsew')
    labels2=['StringVar',
            'BooleanVar\nUnsolvable:\nBad format!',
            'IntVar',
            'DoubleVar']
    for i in range(len(labels2)):
        Label(root,text=labels2[i]).grid(row=0,column=i+1,sticky='nsew')
        
    ButtonMenu(root,['Option1','Option2','Option3'],'ButtonMenu!').grid(row=1,column=1,sticky='nsew')
    ButtonMenu(root,[False,True],False,BooleanVar).grid(row=1,column=2,sticky='nsew')
    ButtonMenu(root,[1,2,3],1,IntVar).grid(row=1,column=3,sticky='nsew')
    ButtonMenu(root,[-1.0,0.1,1.0],1.0,DoubleVar).grid(row=1,column=4,sticky='nsew')
        
    OptionButton(root,['Option1','Option2','Option3'],'OptionButton').grid(row=2,column=1,sticky='nsew')
    OptionButton(root,[False,True],False,BooleanVar).grid(row=2,column=2,sticky='nsew')
    OptionButton(root,[1,2,3],1,IntVar).grid(row=2,column=3,sticky='nsew')
    OptionButton(root,[-1.0,0.1,1.0],1.0,DoubleVar).grid(row=2,column=4,sticky='nsew')
    
    LabelMenu(root,['Option1','Option2','Option3'],'LabelMenu').grid(row=3,column=1,sticky='nsew')
    LabelMenu(root,[False,True],False,BooleanVar).grid(row=3,column=2,sticky='nsew')
    LabelMenu(root,[1,2,3],1,IntVar).grid(row=3,column=3,sticky='nsew')
    LabelMenu(root,[-1.0,0.1,1.0],1.0,DoubleVar).grid(row=3,column=4,sticky='nsew')
        
    ButtonEntry(root,['Option1','Option2','Option3'],'EntryMenu').grid(row=5,column=1,sticky='nsew')
    ButtonEntry(root,[False,True],False,BooleanVar).grid(row=5,column=2,sticky='nsew')
    ButtonEntry(root,[1,2,3],1,IntVar).grid(row=5,column=3,sticky='nsew')
    ButtonEntry(root,[-1.0,0.1,1.0],1.0,DoubleVar).grid(row=5,column=4,sticky='nsew')

    ButtonEntry(root,['Option1','Option2','Option3'],'Option1',strict=True).grid(row=6,column=1,sticky='nsew')
    ButtonEntry(root,[False,True],False,BooleanVar,strict=True).grid(row=6,column=2,sticky='nsew')
    ButtonEntry(root,[1,2,3],1,IntVar,strict=True).grid(row=6,column=3,sticky='nsew')
    ButtonEntry(root,[-1.0,0.1,1.0],1.0,DoubleVar,strict=True).grid(row=6,column=4,sticky='nsew')
    
    ButtonEntry(root,[1,2,3],1,IntVar,min=-10,max=10).grid(row=7,column=3,sticky='nsew')
    ButtonEntry(root,[-1.0,0.1,1.0],1.0,DoubleVar,min=-10,max=10).grid(row=7,column=4,sticky='nsew')
    
    root.mainloop()
