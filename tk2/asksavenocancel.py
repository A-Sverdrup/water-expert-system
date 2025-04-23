from tkinter.simpledialog import _QueryDialog,Label,Button,Frame
__all__ = ['_QuerySave','asksavenocancel']
class _QuerySave(_QueryDialog):
    def body(self, master):
        Label(master, text=self.prompt, justify='left').grid(row=0, padx=5, columnspan=3,sticky='we')
    def buttonbox(self):
        box = Frame(self)
        self.initial_focus=b1=Button(box, text='Save',command=lambda*e:(self.setresult(True),self.ok()))
        b1.grid(row=1,column=0,padx=5)
        b1.bind('<Return>',b1['command'])
        b2 = Button(box, text='Don\'t save',command=lambda:(self.setresult(False),self.ok()))
        b2.grid(row=1, column=1, padx=5)
        b2.bind('<Return>',b2['command'])
        b3 = Button(box, text='Cancel',command=lambda:(self.setresult(None),self.cancel()))
        b3.grid(row=1, column=2, padx=5)
        b3.bind('<Return>',b3['command'])
        self.bind("<Escape>", self.cancel)
        box.pack()
    def validate(self):
        return 1
    def setresult(self,result):
        self.result=result
def asksavenocancel(title, prompt, **kw):
    d = _QuerySave(title, prompt, **kw)
    return d.result
if __name__ == '__main__':
    print(asksavenocancel('This is a "Do you want to save" dialog','You have unsaved changes. Proceed?'))
