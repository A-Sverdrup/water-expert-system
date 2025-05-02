"""OmniText is a text widget that can be configured to have a vertical (scrolling=(0,1)), horizontal (scrolling=(1,0)) or both scrollbars (scrolling=(1,1)).

Since, unlike tkinter's and idlelib's versions of ScrolledText, it relies on LabelFrame instead of a regular Frame,
it can also have a title (text=...).

It has a context menu for basic editing functionality (Select all, Cut, Copy, Paste, Delete) as well, which can be
overriden by replacing make_menu function in a subclass.

It can also have "Copy" and "Clear" buttons, which are useful when using this for an output log (log_buttons=True).
It can also have a slider for adjusting font size (minfont=..., maxfont=...)

(Options to make the bars disappear automatically when not needed, to move them to the other side of the window
have not been implemented yet. Undo/Redo has not been implemented either).

Configuration options are passed to the Text widget.
A LabelFrame widget is inserted between the master and the text, to hold
the Scrollbar widget.
Most methods calls are inherited from the Text widget; Pack, Grid and
Place methods are redirected to the LabelFrame widget.
"""
__all__ = ['OmniText']

from tkinter import Button, LabelFrame, Text, Scrollbar, Pack, Grid, Place
from tkinter.font import Font
if __name__ == "__main__" or __name__ == "omnitext":
    from contextmenu import ContextMenu, COPY
    from zoomscale import ZoomScale
else:
    from tk2.contextmenu import ContextMenu, COPY
    from tk2.zoomscale import ZoomScale
      
class OmniText(Text,ContextMenu):
    __doc__=__doc__
    def __init__(self, master=None, *, scrolling=(0,0), log_buttons=False, **kw):
        self.frame = LabelFrame(master)
        if 'text' in kw:
            self.frame.configure(text=kw['text'])
            del kw['text']
        if 'minfont' in kw or 'maxfont' in kw:
            try:
                assert('minfont' in kw)and('maxfont' in kw)
                minfont=kw.pop('minfont');maxfont=kw.pop('maxfont')
                if minfont<=0:
                    raise ValueError(f'Bad minimum font size {minfont}')
                default=9 if minfont<9<maxfont else (minfont if minfont>9 else (maxfont if maxfont<9 else None))
                if default is not None:
                    ZoomScale(self.frame,from_=minfont,to=maxfont,default=default,style='inline',text='Font',command=self.zoomfont).pack(side='top',fill='both',expand=True)
            except AssertionError:
                raise TypeError('Wrong number of arguments: expected minfont AND maxfont')
        if log_buttons:
            Button(self.frame,text='Clear',command=lambda:self.delete(0.0,'end')).pack(side='bottom', fill='x')
            Button(self.frame,text=COPY,command=self.copy).pack(side='bottom', fill='x')
        if scrolling[1]!=0:
            self.vbar = Scrollbar(self.frame)
            self.vbar.pack(side='right', fill='y')
            self.vbar['command'] = self.yview
            kw.update({'yscrollcommand': self.vbar.set})
        if scrolling[0]!=0:
            self.hbar = Scrollbar(self.frame,orient='horizontal')
            self.hbar.pack(side='bottom', fill='x')
            self.hbar['command'] = self.xview
            kw.update({'xscrollcommand': self.hbar.set,'wrap':'none'})
        Text.__init__(self, self.frame, **kw)
        self.pack(side='left', fill='both', expand=True)
        text_meths = vars(Text).keys()
        methods = vars(Pack).keys() | vars(Grid).keys() | vars(Place).keys()
        methods = methods.difference(text_meths)
        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.frame, m))
        ContextMenu.__init__(self)
    def zoomfont(self,size):
        current_font=Font(font=self.cget("font"))
        self.config(font=(current_font.actual("family"), size, current_font.actual("slant"), current_font.actual("weight")))
    def config(self,**kw):
        if 'text'in kw:self.frame.config(text=kw.pop('text'))
        Text.config(self,**kw)
    def __str__(self):
        return str(self.frame)
    def copy(self):
        self.event_generate(self.keys[platform][SELECT])
        self.event_generate(self.keys[platform][COPY])

if __name__ == "__main__":
    Otext = OmniText(scrolling=(1,1), bg='white', height=10, log_buttons=True, text='OmniText')
    Otext.insert('end', __doc__)
    Otext.pack(fill='both', side='left', expand=True)
    Otext.focus_set()
    Otext.mainloop()
