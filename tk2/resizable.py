from tkinter import Frame,LabelFrame,Text,Scrollbar,Pack,Grid,Place
if __name__ == "__main__":
    from contextmenu import ContextMenu, COPY
    from omnitext import OmniText
    from zoomscale import ZoomScale
else:
    from tk2.contextmenu import ContextMenu, COPY
    from tk2.omnitext import OmniText
    from tk2.zoomscale import ZoomScale
__all__=['ResizableFrame','ResizableLabelFrame','ResizableOmniText']

class Resizable():
    def __init__(self, master=None, minheight=0, minwidth=0, maxheight=float('inf'), maxwidth=float('inf')):
        self.minheight=minheight
        self.minwidth=minwidth
        self.maxheight=maxheight
        self.maxwidth=maxwidth
        self.pack_propagate(0)
        self.grid_propagate(0)
        self.resizeMode='none'
        self.bind("<ButtonPress-1>", self.StartResize)
        self.bind("<ButtonRelease-1>", self.StopResize)
        self.bind("<Motion>", self.MonitorCursorPosition)
        self.cursor=''
        from sys import platform
        self.diag=('size_nw_se'if platform=='win32' else('resizebottomright'if platform=='darwin' else 'fleur'))
        self.dragBandWidth=10
    def StartResize(self, event):
        '''Set the resize mode if the left button of the mouse is clicked close to the right or bottom edge of the frame.'''
        if event.x > self.winfo_width()-self.dragBandWidth:
            if event.y > self.winfo_height()-self.dragBandWidth:
                self.resizeMode='both'
            else:
                self.resizeMode='horizontal'
        elif event.y > self.winfo_height()-self.dragBandWidth:
            self.resizeMode='vertical' 
        else:self.resizeMode='none'
    def MonitorCursorPosition(self,event):        
        '''Check whether the cursor is close to the right or bottom edge of the frame.'''
        # If the cursor is close to edge, change cursor icon
        if event.x > self.winfo_width()-self.dragBandWidth:
            if event.y > self.winfo_height()-self.dragBandWidth:
                self.config(cursor=self.diag)
            else:
                self.config(cursor='sb_h_double_arrow')
        elif event.y > self.winfo_height()-self.dragBandWidth:
            self.config(cursor='sb_v_double_arrow')
        else:self.config(cursor='')
        #Actually resize
        width=max(self.minwidth,min(event.x,self.maxwidth))
        height=max(self.minheight,min(event.y,self.maxheight))
        if self.resizeMode in ['horizontal','both']:self.config(width=width)
        if self.resizeMode in ['vertical','both']:self.config(height=height)
    def StopResize(self, event):
        '''Disable any resize mode and set the standard arrow as cursor.'''
        self.resizeMode='none'
        self.config(cursor='')

def stripkw(kw):
    kw2={}
    if'minwidth'in kw:
        kw2['minwidth']=kw['minwidth']
        if'width'not in kw:kw['width']=kw['minwidth']
        del kw['minwidth']
    if'maxwidth'in kw:kw2['maxwidth']=kw['maxwidth'];del kw['maxwidth']
    if'minheight'in kw:
        kw2['minheight']=kw['minheight']
        if'height'not in kw:kw['height']=kw['minheight']
        del kw['minheight']
    if'maxheight'in kw:kw2['maxheight']=kw['maxheight'];del kw['maxheight']
    return kw,kw2

class ResizableFrame(Frame,Resizable):
    def __init__(self, master=None, **kw):
        kw1,kw2=stripkw(kw)
        Frame.__init__(self,master=master,**kw)
        Resizable.__init__(self,master=master,**kw2)
class ResizableLabelFrame(LabelFrame,Resizable):
    def __init__(self, master=None, **kw):
        kw1,kw2=stripkw(kw)
        LabelFrame.__init__(self,master=master,**kw)
        Resizable.__init__(self,master=master,**kw2)

class ResizableOmniText(OmniText,ContextMenu):
    """ResizableOmniText is a text widget that can be configured to have a vertical (scrolling=(0,1)), horizontal (scrolling=(1,0)) or both scrollbars (scrolling=(1,1)).

It can also have a title (text=...).

It is now based on ResizableLabelFrame instead of a LabelFrame. This allows you to resize it by dragging bottom edge, right edge or bottom-right corner.

It has a context menu for basic editing functionality (Select all, Cut, Copy, Paste, Delete) as well, which can be
overriden by replacing make_menu function in a subclass.

It can also have "Copy" and "Clear" buttons, which are useful when using this for an output log (log_buttons=True).
It can also have a slider for adjusting font size (minfont=..., maxfont=...)

(Options to make the bars disappear automatically when not needed, to move them to the other side of the window
have not been implemented yet. Undo/Redo has not been implemented either).

Configuration options are passed to the Text widget.
A ResizableLabelFrame widget is inserted between the master and the text, to hold
the Scrollbar widget.
Most methods calls are inherited from the Text widget; Pack, Grid and
Place methods are redirected to the ResizableLabelFrame widget.
"""
    def __init__(self, master=None, *, scrolling=(0,0), log_buttons=False, **kw):
        kw1,kw2=stripkw(kw)
        self.frame = ResizableLabelFrame(master,**kw2)
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
    def config(self,**kw):
        if 'text'in kw:self.frame.config(text=kw.pop('text'))
        if'minheight'in kw:self.minheight=kw.pop('minheight')
        if'maxheight'in kw:self.maxheight=kw.pop('maxheight')
        if'minwidth'in kw:self.minwidth=kw.pop('minwidth')
        if'maxwidth'in kw:self.maxwidth=kw.pop('maxwidth')
        Text.config(self,**kw)
if __name__ == "__main__":
    from tkinter import Tk,Button
    root=Tk()
    root.title("Resizable Widgets") 
    root.geometry('600x400')
    resFrame=ResizableLabelFrame(root,text='Try resizing this!',minwidth=120,minheight=100)
    resFrame.grid(row=0,column=0,sticky='nsew')
    Frame(root,bg="red",width=100,height=100).grid(row=0,column=1,sticky='nsew')
    Frame(root,bg="red",width=100,height=100).grid(row=1,column=0,sticky='nsew')

    Otext = ResizableOmniText(root,scrolling=(1,1), bg='white',minwidth=100, minheight=100, height=10, text='ResizableOmniText')
    Otext.insert('end', ResizableOmniText.__doc__)
    Otext.grid(row=1,column=1,sticky='nsew')
    Otext.focus_set()
        
    root.mainloop()
