"""OmniSpin is a Spinbox with (optional) title text and (optional) checkbutton to enable/disable

Configuration options are passed to the Spinbox widget.
A LabelFrame widget is inserted between the master and the spinbox, to hold 
the Checkbutton widget.
Most methods calls are inherited from the Spinbox widget; Pack, Grid and
Place methods are redirected to the LabelFrame widget.
"""
__all__ = ['_FileButton','OpenFileButton','OpenFilesButton','SaveAsFileButton','DirectoryButton']

from tkinter import Button,Entry,LabelFrame,StringVar
from tkinter.filedialog import askopenfilename,askopenfilenames,askdirectory,asksaveasfilename

class _FileButton(LabelFrame):
    def __init__(self,master=None,text=None,command=None,mandatory=False,**kw):
        self.kw={}
        if'defaultextension'in kw:self.kw['defaultextension']=kw.pop('defaultextension')
        if'filetypes'in kw:self.kw['filetypes']=kw.pop('filetypes')
        self.text=text
        if'command'in kw:self.text=kw.pop('command')
        LabelFrame.__init__(self,master=master,text=self.text)
        self.variable=StringVar(self)
        self.entry=Entry(self,textvariable=self.variable,width=20)
        self.entry.pack(side='left',fill='both',expand=True)
        self.button=Button(self,text='...',command=self.select)
        self.button.pack(side='left',fill='both',expand=True)
        self.mandatory=mandatory
    def config(self,**kw):
        if'state'in kw:
            state=kw.pop('state')
            self.entry.config(state=state)
            self.button.config(state=state)
        LabelFrame.config(self,**kw)
    def select(self):
        name=self.command(**self.kw)
        if name:
            self.variable.set(name)
    def get(self):
        return self.variable.get()
    def validate(self):
        if self.mandatory:
            return bool(self.get())
class OpenFileButton(_FileButton):
    text='Select file to open'
    command=lambda self,**kw:askopenfilename(**kw)
class OpenFilesButton(_FileButton): #TODO: fix broken get when multiple files are selected or when entry text was modified
    text='Select files to open'
    command=lambda self,**kw:askopenfilenames(**kw)
class SaveAsFileButton(_FileButton):
    text='Select file to save as'
    command=lambda self,**kw:askopenfilename(**kw)
class DirectoryButton(_FileButton):
    text='Select directory'
    command=lambda self,**kw:askdirectory(**kw)
    
if __name__=='__main__':
    OpenFileButton().pack()
    OpenFilesButton().pack()#TODO: fix unintended get behavior
    SaveAsFileButton().pack()
    a=DirectoryButton(mandatory=True);a.pack()
