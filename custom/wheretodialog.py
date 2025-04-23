from tkinter.simpledialog import _QueryDialog
from tk2 import OmniSpin
from tkinter import Label
__all__=['whereto']
class WhereToDialogXY(_QueryDialog):
    def body(self, master):
        w = Label(master,text='Where to?',justify='left');w.grid(row=0,padx=5,sticky='w')
        self.row = OmniSpin(master,text=self.prompt[0],width=4,cnf={'from':0,'to':self.maxvalue[0]});self.row.grid(row=1,column=1,padx=5,sticky='we')
        self.column = OmniSpin(master,text=self.prompt[1],width=4,cnf={'from':0,'to':self.maxvalue[1]});self.column.grid(row=1,column=0,padx=5,sticky='we')
        return self.column
    def getresult(self):
        return(int(self.row.get()),int(self.column.get()))
    def validate(self):
        self.result = self.getresult()
        return 1
class WhereToDialog(_QueryDialog):
    def body(self, master):
        w = Label(master,text=self.minvalue,justify='left');w.grid(row=0,padx=5,sticky='w')
        self.spin = OmniSpin(master,text=self.prompt,width=4,cnf={'from':0,'to':self.maxvalue});self.spin.grid(row=1,padx=5,sticky='we')
        return self.spin
    def getresult(self):
        return int(self.spin.get())
    def validate(self):
        self.result = self.getresult()
        return 1

def whereto(title, prompt, maxvalue, type, **kw):
    if type=='xy':d = WhereToDialogXY(title, ('Row','Column'), maxvalue=maxvalue, **kw)
    elif type=='x':d = WhereToDialog(title, 'Row', minvalue='Where to?', maxvalue=maxvalue, **kw)
    elif type=='y':d = WhereToDialog(title, 'Column', minvalue='Where to?', maxvalue=maxvalue, **kw)
    elif type=='-y':d = WhereToDialog(title, 'Column', minvalue='Select column', maxvalue=maxvalue, **kw)
    return d.result


