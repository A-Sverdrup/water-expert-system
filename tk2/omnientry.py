"""OmniEntry is an entry widget that can be configured to have a horizontal scrollbar (scrolling=True) and a title (text='...' keyword option in __init__) and is horizontally scrollable with your MouseWheel

It has a context menu for basic editing functionality (Select all, Cut, Copy, Paste, Delete) as well, which can be overriden by replacing make_menu function in a subclass.

(Option to make the scrollbar disappear automatically when not needed has not been implemented yet. Undo/Redo has not been implemented either).

It can also have a "Copy" button.

It can also be readonly via OmniEntry(state='readonly') - beware though that the internal state is still 'normal'!

Configuration options are passed to the Entry widget.
A LabelFrame widget is inserted between the master and the entry to hold the Scrollbar widget.
Most methods calls are inherited from the Entry widget; Pack, Grid and Place methods are redirected to the LabelFrame widget.
"""

from tkinter import Button, Entry, LabelFrame, Scrollbar, Pack, Grid, Place
if __name__ == "__main__":
    from contextmenu import COPY, ContextMenu
else:
    from tk2.contextmenu import COPY, ContextMenu
class OmniEntry(Entry,ContextMenu):
    def __init__(self, master=None, scrolling=False, log_buttons=False, cnf={}, **kw):
        self.frame = LabelFrame(master)
        if 'text' in kw:
            self.frame.configure(text=kw['text'])
            del kw['text']
        if 'state' in kw and kw['state']=='readonly':
            self.readonly=True
            del kw['state']
        else:self.readonly=False
        if log_buttons:
            Button(self.frame,text=COPY,command=self.copy).pack(side='bottom', fill='x')
        if bool(scrolling):
            self.hbar = Scrollbar(self.frame,orient='horizontal')
            self.hbar.pack(side='bottom', fill='x')
            self.hbar['command'] = self.xview
            kw.update({'xscrollcommand':self.hbar.set})
        Entry.__init__(self, self.frame, **kw)
        if self.readonly:self.bind('<Key>',self.readonlycheck)
        self.pack(fill='both', expand=True)
        self.bind("<Enter>", self._bind_mouse)
        self.bind("<Leave>", self._unbind_mouse)
        entry_meths = vars(Entry).keys()
        methods = vars(Pack).keys() | vars(Grid).keys() | vars(Place).keys()
        methods = methods.difference(entry_meths)
        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.frame, m))
        ContextMenu.__init__(self)
    def readonlycheck(self,event):
        if event.char not in ['\x03','\x01']:return"break"
    def copy(self):
        self.clipboard_clear()
        self.clipboard_append(self.get())
    
    def _bind_mouse(self, event=None):
        self.bind_all("<4>", self._on_mousewheel)
        self.bind_all("<5>", self._on_mousewheel)
        self.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mouse(self, event=None):
        self.unbind_all("<4>")
        self.unbind_all("<5>")
        self.unbind_all("<MouseWheel>")
        
    def _on_mousewheel(self, event):
        """Linux uses event.num; Windows / Mac uses event.delta"""
        func = self.xview_scroll #if event.state & 1 else self.yview_scroll 
        if event.num == 4 or event.delta > 0: func(-1, "units" )
        elif event.num == 5 or event.delta < 0: func(1, "units" )
if __name__ == "__main__":
    from tkinter import Tk,Label
    tk=Tk()
    random=True
    two=111
    for i in __doc__.splitlines():
        if i=='':
            random = not random
            two=two%two-1
        else:
            OEntry = OmniEntry(tk,scrolling=random, log_buttons=two%3==0)
            OEntry.insert('end', i)
            OEntry.pack(fill='x', expand=True)
            OEntry.focus_set()
    OEntry.mainloop()
