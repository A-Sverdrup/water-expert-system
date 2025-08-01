__all__ = ['ZoomScale']

from tkinter import Button,Frame,Label,LabelFrame,PhotoImage,Scale,Pack,Grid,Place

class ZoomScale(Scale):
    'A Scale widget specifically for zooming in'
    def __init__(self,master,*,from_,to,default,command,orient='horizontal',style='frame',relief='flat',font=None,text='Zoom'):
        if style=='frame' and text!='':self.frame=LabelFrame(master,width=1,height=1,text=text)
        else:self.frame=Frame(master,width=1,height=1,relief=(relief if text else'flat'))
        if orient=='horizontal':Scale.__init__(self,self.frame,from_=from_,to=to,showvalue=False,resolution=1,orient=orient,command=self.zoom)
        elif orient=='vertical':Scale.__init__(self,self.frame,from_=to,to=from_,showvalue=False,resolution=-1,orient=orient,command=self.zoom)
        self.set(default)
        self.command=command
        p='R0lGODlhEAAQAHAAACwAAAAAEAAQAIH///8AAAAAAAAAAAAC'
        self.images={'minus':PhotoImage(master=self,data=p+'FISPqcvtD6Nkodp7Dd52+g+GIlMAADs='),
                     'plus':PhotoImage(master=self,data=p+'H4SPqRax256KEtHKHM6v+Q9m4KhNJXahZ5Wyq9RuSgEAOw==')}
        side='left'if orient=='horizontal'else'bottom'
        fill='y'if orient=='horizontal'else'x'
        if style=='inline':
            if font is None:Label(self.frame,text=text,relief='raised').pack(side='left'if orient=='horizontal'else'top',fill=fill,expand=False)
            else:Label(self.frame,text=text,font=font,relief='raised').pack(side='left'if orient=='horizontal'else'top',fill=fill,expand=False)
        Button(self.frame,image=self.images['minus'],width=16,height=16,command=lambda:self.set(self.get()-1)).pack(side=side,fill=fill,expand=False)
        self.pack(side=side,fill='both',expand=True)
        Button(self.frame,image=self.images['plus'],width=16,height=16,command=lambda:self.set(self.get()+1)).pack(side=side,fill=fill,expand=False)
        text_meths = vars(Scale).keys()
        methods = vars(Pack).keys() | vars(Grid).keys() | vars(Place).keys()
        methods = methods.difference(text_meths)
        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.frame, m))
    def zoom(self,size):
        size=int(float(size))
        self.set(size)
        self.command(size)
        return "break"
    
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
