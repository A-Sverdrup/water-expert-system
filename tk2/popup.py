__all__ = ['popup']
def popup(cls):
    '''Tkinter class decorator'''
    class Popup(cls):
        '''Pass popup_text and popup_font keywords to configure pop-up of %s'''%cls.__name__
        def __init__(self,master,cnf={},**kw):
            from tkinter import Label as l
            self.master=master; self.tk=master.tk #Tkinter
            #Получить настройки "всплывайки" и удалить их из настроек
            if 'popup_text'in kw and bool(kw['popup_text']):PT,PF=kw['popup_text'],(kw['popup_font']if'popup_font'in kw else(None,));self.__oops=0#Инициализация
            else:self.__oops=1 #А нужна ли "всплывайка"?
            if 'popup_text' in kw:del kw['popup_text']
            if 'popup_font' in kw:del kw['popup_font']
            super().__init__(master=master,cnf=cnf,**kw)#Создать родительский виджет
            if not self.__oops:
                self.POPUP=l(self.master,text=PT,font=PF)#Создать "всплывайку"
                self.bind('<Enter>',self.__ON)
                self.bind('<Motion>',self.__ON)
                self.bind('<Leave>',self.__OFF)#Реакция на движения
        def config(self,**kw):
            #Настройка - текст/шрифт всплывайки? если да, передать всплывайке; если нет - родителю.
            if 'popup_text' in kw:self.POPUP.config(text=kw['popup_text']);del kw['popup_text']
            if 'popup_font' in kw:self.POPUP.config(font=kw['popup_font']);del kw['popup_font']
            super().config(**kw)
        configure=config
        def __ON(self,e):
            self.POPUP.place(x=self.winfo_x()+e.x+1,y=self.winfo_y()+e.y+1,anchor='nw')
            self.POPUP.lift()
        def __OFF(self,e):self.POPUP.place_forget()
    return Popup
if __name__=='__main__':
    from tkinter import Tk,Button,Entry,Label
    tk=Tk()
    tk.title('test Test TeStEs')
    
    Button=popup(Button);   Label=popup(Label);   Entry=popup(Entry)
    
    a=Label(tk,text='test',popup_text='test')
    a.place(x=34,y=25)
    Button(tk,text='Test',popup_text='TeStEs',popup_font=('Times',16,'bold')).place(x=50,y=50)
    Entry(tk,popup_text='TESTING').place(x=0,y=100)
    tk.mainloop()
