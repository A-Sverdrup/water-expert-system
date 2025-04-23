__all__ = ['ToggleButton','ToggleRadioButton']

from tkinter import Button,BooleanVar

class ToggleButton(Button):
    '''A simple toggle button which stores a boolean value'''
    def __init__(self, master=None, value=False, **kw):
        kw['command']=self.flip
        kw['relief']='sunken'if value else'raised'
        Button.__init__(self,master,**kw)
        self.value=BooleanVar(self,value=value)
        self.get,self.set,self.trace_add=self.value.get,self.value.set,self.value.trace_add
        self.value.trace_add('write',self.__update)
    def flip(self):
        self.set(not self.get())
        self.__update()
    def __update(self,*args):
        self.config(relief='sunken'if self.get()else'raised')

class ToggleRadioButton(Button):
    '''A toggle button which acts like a RadioButton'''
    def __init__(self, master=None, value=None, variable=None, **kw):
        kw['command']=self.push
        Button.__init__(self,master,**kw)
        self.value=value
        self.variable=variable
        self.variable.trace_add('write',self.__update)
        self.__update()
    def push(self):
        self.variable.set(self.value)
        self.__update()
    def __update(self,*args):
        self.config(relief='sunken'if self.variable.get()==self.value else'raised')

if __name__ == "__main__":
    from tkinter import Tk, Label, StringVar
    test=ToggleButton(text='On/Off')
    test.pack(padx=10,pady=10)
    test.mainloop()

    root=Tk()
    v=StringVar(value='Number 1')
    Label(textvariable=v).pack(side='top')
    ToggleRadioButton(root,value='Number 1',variable=v,text='Number 1').pack(side='left')
    ToggleRadioButton(root,value='Number 2',variable=v,text='Number 2').pack(side='left')
    ToggleRadioButton(root,value='Number 3',variable=v,text='Number 3').pack(side='left')
    root.mainloop()
