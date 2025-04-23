"""OmniSpin is a Spinbox with (optional) title text, which can return proper int/float values instead of a string

Configuration options are passed to the Spinbox widget.
A LabelFrame widget is inserted between the master and the spinbox
Most methods calls are inherited from the Spinbox widget; Pack, Grid and
Place methods are redirected to the LabelFrame widget.
"""
__all__ = ['OmniSpin']

from tkinter import LabelFrame, Spinbox, BooleanVar, StringVar, Pack, Grid, Place

class OmniSpin(Spinbox):
    def __init__(self,master=None,text=None,type=int,cnf={},**kw):
        self.frame=LabelFrame(master,text=text,relief='flat'if text==None else None)
        if 'textvariable'not in kw:
            self.variable=StringVar(self.frame)
            self.trace_add=self.variable.trace_add
            self.set=self.variable.set
            kw['textvariable']=self.variable
        self.type=type
        Spinbox.__init__(self,self.frame,cnf=cnf,**kw)
        self.pack(fill='both',expand=True)
        spin_meths = vars(Spinbox).keys()
        methods = vars(Pack).keys() | vars(Grid).keys() | vars(Place).keys()
        methods = methods.difference(spin_meths)
        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.frame, m))
    def get(self):
        return self.type(Spinbox.get(self))
    def config(self,cnf={},**kw):
        if 'text'in kw:self.frame.config(text=kw.pop('text'))
        if 'text'in cnf:self.frame.config(text=cnf.pop('text'))
        Spinbox.config(self,cnf=cnf,**kw)
    def check(self,*a):
        Spinbox.config(self,state='normal'if self.enabled.get()else'disabled')

if __name__ == "__main__":
    Ospin = OmniSpin(text='OmniSpin',type=int,cnf={'from':0,'to':10})
    Ospin.pack(fill='both', side='left', expand=True)
    Ospin.focus_set()
    Ospin.mainloop()
