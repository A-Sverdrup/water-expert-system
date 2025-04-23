__all__=['bind_together']
def bind_together(root):
    'bind together nested PanedWindows to create a grid with resizable cells'
    def onB1Motion(event):#bindings are executed with event objects
        root.bind('<Motion>',onB1Motion)
        root.bind('<ButtonRelease-1>',lambda event:root.unbind('<Motion>',onB1Motion))
        widget = event.widget #get widget/paned window of event
        x,y = event.x,event.y #get x and y coord of event
        data = widget.identify(x,y) #paned window identify
        if data != '': #identify returns empty string if child window
            idx = data[0] #get sash index
            orient = event.widget['orient'] #check for orientation of paned window
            for child in widget.master.winfo_children(): #get all children of master
                if isinstance(child,PanedWindow): #if children is paned window do..
                    if child['orient'] == orient: #if child paned window is same orient as event paned do..
                        child.sash_place(idx,x,y) #places the sash with same index on same position
    
    root.bind('<Button1-Motion>',onB1Motion)
    for i in root.winfo_children():
        i.bind('<Button1-Motion>',onB1Motion)

if __name__=='__main__':
    from tkinter import Tk, Label, PanedWindow
    tk = Tk()
    tk.geometry("400x400")
    main = PanedWindow(tk, orient='horizontal', bd=2, relief="solid", bg="black")
    main.pack(fill="both", expand=1)
    top = PanedWindow(main, orient='vertical', bd=1, relief="solid", bg="red")
    main.add(top)
    top.add(Label(top, text= "Top-Left"))
    top.add(Label(top, text= "Top-Right"))
    middle = PanedWindow(main, orient='vertical', bd=1, relief="solid", bg="green")
    main.add(middle)
    middle.add(Label(middle, text= "Mid-Left"))
    middle.add(Label(middle, text= "Mid-Right"))
    bottom = PanedWindow(main, orient='vertical', bd=1, relief="solid", bg="blue")
    main.add(bottom)
    bottom.add(Label(bottom, text= "Bottom-Left"))
    bottom.add(Label(bottom, text= "Bottom-Right"))
    bind_together(main)
    tk.mainloop()
