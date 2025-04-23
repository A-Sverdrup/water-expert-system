from tkinter import Frame,LabelFrame,Canvas,Scrollbar,Widget

__all__=['ScrolledFrame','ScrolledLabelFrame']

class ScrolledFrame:
    """
    A scrollable Frame that can be treated like any other Frame widgets.
    keyword arguments are passed to the underlying Frame
    except the keyword arguments 'width' and 'height', which are passed to the underlying Canvas
    Note that a widget layed out in this frame will have Canvas as self.master
    """
    def __init__(self, master, **kwargs):
        width = kwargs.pop('width', None)
        height = kwargs.pop('height', None)
        self.outer = Frame(master, **kwargs)

        self.vsb = Scrollbar(self.outer, orient='vertical')
        self.vsb.grid(row=0, column=1, sticky='ns')
        self.hsb = Scrollbar(self.outer, orient='horizontal')
        self.hsb.grid(row=1, column=0, sticky='ew')
        self.canvas = Canvas(self.outer, highlightthickness=0, width=width, height=height)
        self.canvas.grid(row=0, column=0, sticky='nsew')
        self.outer.rowconfigure(0, weight=1)
        self.outer.columnconfigure(0, weight=1)
        self.canvas['yscrollcommand'] = self.vsb.set
        self.canvas['xscrollcommand'] = self.hsb.set
        # mouse scroll does not work with "bind", but with "bind_all". Therefore to use multiple windows (un)bind_all must be called each time
        self.canvas.bind("<Enter>", self._bind_mouse)
        self.canvas.bind("<Leave>", self._unbind_mouse)
        self.vsb['command'] = self.canvas.yview
        self.hsb['command'] = self.canvas.xview

        self.inner = Frame(self.canvas)
        # pack the inner Frame into the Canvas with the topleft corner 4 pixels offset
        self.canvas.create_window(4, 4, window=self.inner, anchor='nw')
        self.inner.bind("<Configure>", self._on_frame_configure)

        self.outer_attr = set(dir(Widget))

    def __getattr__(self, item):
        if item in self.outer_attr:
            # geometry attributes etc (eg pack, destroy, tkraise) are passed on to self.outer
            return getattr(self.outer, item)
        else:
            # all other attributes (_w, children, etc) are passed to self.inner
            return getattr(self.inner, item)

    def _on_frame_configure(self, event=None):
        x1, y1, x2, y2 = self.canvas.bbox("all")
        height = self.canvas.winfo_height()
        width = self.canvas.winfo_width()
        self.canvas.config(scrollregion = (0,0, max(x2, width), max(y2, height)))

    def _bind_mouse(self, event=None):
        self.canvas.bind_all("<4>", self._on_mousewheel)
        self.canvas.bind_all("<5>", self._on_mousewheel)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mouse(self, event=None):
        self.canvas.unbind_all("<4>")
        self.canvas.unbind_all("<5>")
        self.canvas.unbind_all("<MouseWheel>")
        
    def _on_mousewheel(self, event):
        """Linux uses event.num; Windows / Mac uses event.delta"""
        func = self.canvas.xview_scroll if event.state & 1 else self.canvas.yview_scroll 
        if event.num == 4 or event.delta > 0: func(-1, "units" )
        elif event.num == 5 or event.delta < 0: func(1, "units" )
    
    def __str__(self):
        return str(self.outer)

class ScrolledLabelFrame:
    """
    A scrollable LabelFrame that can be treated like any other Frame widgets.
    keyword arguments are passed to the underlying Frame
    except the keyword arguments 'width' and 'height', which are passed to the underlying Canvas
    Note that a widget layed out in this frame will have Canvas as self.master
    """
    def __init__(self, master, **kwargs):
        width = kwargs.pop('width', None)
        height = kwargs.pop('height', None)
        self.outer = LabelFrame(master, **kwargs)

        self.vsb = Scrollbar(self.outer, orient='vertical')
        self.vsb.grid(row=0, column=1, sticky='ns')
        self.hsb = Scrollbar(self.outer, orient='horizontal')
        self.hsb.grid(row=1, column=0, sticky='ew')
        self.canvas = Canvas(self.outer, highlightthickness=0, width=width, height=height)
        self.canvas.grid(row=0, column=0, sticky='nsew')
        self.outer.rowconfigure(0, weight=1)
        self.outer.columnconfigure(0, weight=1)
        self.canvas['yscrollcommand'] = self.vsb.set
        self.canvas['xscrollcommand'] = self.hsb.set
        # mouse scroll does not work with "bind", but with "bind_all". Therefore to use multiple windows (un)bind_all must be called each time
        self.canvas.bind("<Enter>", self._bind_mouse)
        self.canvas.bind("<Leave>", self._unbind_mouse)
        self.vsb['command'] = self.canvas.yview
        self.hsb['command'] = self.canvas.xview

        self.inner = Frame(self.canvas)
        # pack the inner Frame into the Canvas with the topleft corner 4 pixels offset
        self.canvas.create_window(4, 4, window=self.inner, anchor='nw')
        self.inner.bind("<Configure>", self._on_frame_configure)

        self.outer_attr = set(dir(Widget))

    def __getattr__(self, item):
        if item in self.outer_attr:
            # geometry attributes etc (eg pack, destroy, tkraise) are passed on to self.outer
            return getattr(self.outer, item)
        else:
            # all other attributes (_w, children, etc) are passed to self.inner
            return getattr(self.inner, item)

    def _on_frame_configure(self, event=None):
        x1, y1, x2, y2 = self.canvas.bbox("all")
        height = self.canvas.winfo_height()
        width = self.canvas.winfo_width()
        self.canvas.config(scrollregion = (0,0, max(x2, width), max(y2, height)))

    def _bind_mouse(self, event=None):
        self.canvas.bind_all("<4>", self._on_mousewheel)
        self.canvas.bind_all("<5>", self._on_mousewheel)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mouse(self, event=None):
        self.canvas.unbind_all("<4>")
        self.canvas.unbind_all("<5>")
        self.canvas.unbind_all("<MouseWheel>")
        
    def _on_mousewheel(self, event):
        """Linux uses event.num; Windows / Mac uses event.delta"""
        func = self.canvas.xview_scroll if event.state & 1 else self.canvas.yview_scroll 
        if event.num == 4 or event.delta > 0: func(-1, "units" )
        elif event.num == 5 or event.delta < 0: func(1, "units" )
    
    def __str__(self):
        return str(self.outer)
    
#  **** SCROLL BAR TEST ****
if __name__ == "__main__":
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    from tkinter import Label,Tk
    root = Tk()
    root.title("Scrollbar Test")
    root.geometry('400x500')
    lbl = Label(root, text="Hold shift while using the scroll wheel to scroll horizontally")
    lbl.pack()
    
    # use the Scrolled Frame just like any other Frame
    frame = ScrolledFrame(root, width=300, borderwidth=2, relief='sunken', background="light gray")
    #frame.grid(column=0, row=0, sticky='nsew') # fixed size
    frame.pack(fill='both', expand=True) # fill window

    for i in range(30):
        for j in range(20):
            label = Label(frame, text="{}{}".format(alphabet[j], i), relief='ridge')
            label.grid(column=j, row=i, sticky='ew', padx=2, pady=2)

    root.mainloop()
