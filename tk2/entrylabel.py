__all__ = ['EntryLabel','LabelEntry']

from tkinter import Frame, Entry, Label, StringVar, Pack, Grid, Place

class EntryLabel(Entry):
    '''A label which can be edited upon double-click'''
    def __init__(self, master=None, text=None, **kw):
        self.frame=Frame(master)
        self.variable=StringVar(self.frame,value=text)
        Entry.__init__(self, master=self.frame, textvariable=self.variable)
        self.pack_=self.pack
        self.pack_forget_=self.pack_forget
        self.label=Label(master=self.frame, textvariable=self.variable, **kw)
        self.label.pack(side='left',fill='both',expand=True)
        self.label.bind('<Double-1>',self.open)
        for i in ['<Return>','<Escape>','<FocusOut>']:
            self.bind(i,self.close)
        self.closed=True
        entry_meths = vars(Entry).keys()
        methods = vars(Pack).keys() | vars(Grid).keys() | vars(Place).keys()
        methods = methods.difference(entry_meths)
        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.frame, m))
        self.get=self.variable.get
        self.set=self.variable.set
        self.trace_add=self.variable.trace_add
    def config(self,**kw):
        Entry.config(self,**kw)
        #if 'font' in kw and kw['font'][0]==None:kw['font']=(self.label.cget('font'),kw['font'][1])
        self.label.config(**kw)
    def open(self,event):
        self.label.pack_forget()
        self.config(width=len(str(self.get())))
        self.pack_(side='left',pady=2,fill='both',expand=True)
        self.event_generate('<<open>>')
        self.closed=False
        self.focus_set()
    def close(self,event=None):
        self.pack_forget_()
        self.label.pack(side='left',fill='both',expand=True)
        if self.closed==False:self.event_generate('<<close>>');self.closed=True

class LabelEntry(Label):
    '''An simpler, presumably less laggy EntryLabel'''
    def __init__(self, master=None, text=None, **kw):
        self.variable=StringVar(master,value=text)
        Label.__init__(self, master=master, textvariable=self.variable)
        self.entry=Entry(self, textvariable=self.variable, **kw)
        self.bind('<Double-1>',self.open)
        for i in ['<Return>','<Escape>','<FocusOut>']:
            self.entry.bind(i,self.close)
        self.get=self.variable.get
        self.set=self.variable.set
        self.trace_add=self.variable.trace_add
    def config(self,**kw):
        Label.config(self,**kw)
        self.entry.config(**kw)
    def open(self,event):
        self.entry.pack(side='left',fill='both',expand=True)
        self.config(width=len(str(self.get())))
        self.event_generate('<<open>>')
        self.entry.focus_set()
    def close(self,event=None):
        self.entry.pack_forget()
        self.event_generate('<<close>>')
        
if __name__ == "__main__":
    test=EntryLabel(text='EntryLabel (double-click me!)')
    test.pack(padx=10,pady=10)
    test2=EntryLabel(text='LabelEntry (double-click me!)')
    test2.pack(padx=10,pady=10)
    test.mainloop()

