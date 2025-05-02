from tkinter import Button,Frame,Label,LabelFrame,Menu,PhotoImage,Scale,Scrollbar,BooleanVar,Pack,Grid,Place
from tkinter.simpledialog import _QueryDialog
from tkinter.messagebox import showinfo
from pandas import DataFrame,concat
from math import log,e
from tk2.entrylabel import EntryLabel
from tk2.omnispin import OmniSpin
from tk2.zoomscale import ZoomScale
__all__=['ops','isnan','isnum','Table','FastaTable','number','whereto']
######################################ops ######################################
NaN=float('nan')
def feval(f):
    def F(a):return DataFrame([(NaN if isnan(a[i])else f(a[i]))for i in range(len(a))])
    return F
def fcomp(f):
    def F(a,b):
        assert len(a)==len(b)
        return DataFrame([(NaN if(isnan(a[i])or isnan(b[i]))else f(a[i],b[i]))for i in range(len(a))])
    return F
def unary(f):
    @feval
    def op(a):
        if isnum(a):f(a)
        else:return NaN
    return op
def numop(f):
    @fcomp
    def op(a,b):
        if not(isnum(a)and isnum(b)):return NaN
        else:return f(a,b)
    return op
def isnum(a):return int(isinstance(a,(int,float))and(not isnan(a)))
def isnan(a):return int(str(a)==str(NaN))

#Compare
EQ=numop(lambda a,b:a==b)
NE=numop(lambda a,b:a!=b)
LT=numop(lambda a,b:a<b)
LE=numop(lambda a,b:a<=b)
GT=numop(lambda a,b:a>b)
GE=numop(lambda a,b:a>=b)
#Logic
BOOL=feval(lambda a:int(bool(a)))
NOT=feval(lambda a:int(not bool(a)))
AND=fcomp(lambda a,b:int(bool(a)and bool(b)))
NAND=fcomp(lambda a,b:int(not(bool(a)and bool(b))))
OR=fcomp(lambda a,b:int(bool(a)or bool_(b)))
NOR=fcomp(lambda a,b:int(not(bool(a)or bool(b))))
XOR=fcomp(lambda a,b:int(bool(a)!=bool(b)))
XNOR=fcomp(lambda a,b:int(bool(a)==bool(b)))
#Typechecking
ISNAN=lambda a:DataFrame([isnan(a[i])for i in range(len(a))])
ISTEXT=feval(lambda a:int(isinstance(a,str)))
ISNUMBER=feval(lambda a:int(isinstance(a,(int,float))))
ISEMPTY=feval(lambda a:int(a==''))
#Math
PLUS=numop(lambda a,b:a+b)
NEG=unary(lambda a:-a)
MINUS=numop(lambda a,b:a-b)
MUL=numop(lambda a,b:a*b)
DEL=numop(lambda a,b:(NaN if b==0 else(a/b)))
POW=numop(lambda a,b:a**b)
EXP=unary(lambda a:e**a)
LOG2=unary(lambda a:(log(a,2)if a>0 else NaN))
LOGE=unary(lambda a:(log(a)if a>0 else NaN))
LOG10=unary(lambda a:(log(a,10)if a>0 else NaN))
SQRT=unary(lambda a:((a**.5)if a>0 else NaN))
#Manipulation

CONCAT=fcomp(lambda a,b:str(a)+str(b))
CONCAT2=fcomp(lambda a,b:str(a)+' '+str(b))

ops={'-------Compare------':None,
     '[I1] = [I2]':EQ,'[I1] ≠ [I2]':NE,'[I1] < [I2]':LT,'[I1] ≤ [I2]':LE,'[I1] > [I2]':GT,'[I1] ≥ [I2]':GE,
     '--------Logic-------':None,
     'NOT [I1]':NOT,'BOOL [I1]':BOOL,
     '[I1] AND [I2]':AND,'[I1] NAND [I2]':NAND,'[I1] OR [I2]':OR,'[I1] NOR [I2]':NOR,'[I1] XOR [I2]':XOR,'[I1] XNOR [I2]':XNOR,
     '----Typechecking----':None,
     'ISERROR([I1])':ISNAN,'ISNUMBER([I1])':ISNUMBER,'ISTEXT([I1])':ISTEXT,'ISEMPTY([I1])':ISEMPTY,
     '--------Math--------':None,
     '[I1] + [I2]':PLUS,'- [I1]':NEG,'[I1] - [I2]':MINUS,'[I1] * [I2]':MUL,'[I1] / [I2]':DEL,'[I1] ^ [I2]':POW,'√ [I1]':SQRT,
     'EXP([I1])':EXP,'LOG2 [I1]':LOG2,'LN [I1]':LOGE,'LOG10 [I1]':LOG10,
     '-----Manipulate-----':None,
     'IF [I1] THEN [I2] ELSE [I3]':lambda a,b,c:DataFrame([i[1]if bool(i[0])else i[2]for i in zip(a,b,c)]),
     'CONCAT([I1]; [I2])':CONCAT,'CONCAT([I1];" ";[I2])':CONCAT2,
     }
#####################################table #####################################
def number(value):
    try:
        try:number2=int(value)
        except ValueError:number2=float(value)
    except ValueError:number2=value
    return number2
class TableButton(Button):
    def __init__(self,master,name,number,commands,**kw):
        Button.__init__(self,master=master,text=number,command=lambda:commands.get(commands['default'])(self.number),**kw)
        self.name=name
        self.number=number
        self.menu = Menu(self,tearoff=0)
        self.make_menu(commands)
        self.make_menu2(commands)
        self.bind('<Button-2>',self.open)
        self.bind('<Button-3>',self.open)
    def make_menu(self,commands):pass
    def make_menu2(self,commands):
        self.menu.add_separator()
        self.menu.add_command(label='Insert %s before'%self.name,command=lambda:commands['insert'](self.number))
        self.menu.add_command(label='Insert %s after'%self.name,command=lambda:commands['insert'](self.number+1))
        self.menu.add_command(label='Delete '+self.name,command=lambda:commands['delete'](self.number))
    def config(self,**kw):
        if'number'in kw:self.number=kw['number'];del kw['number']
        Button.config(self,**kw)
    def open(self,event):
        self.menu.tk_popup(self.winfo_rootx(),self.winfo_rooty())
class TableColumnButton(TableButton):
    def make_menu(self,commands):
        menu2=Menu(self.menu,tearoff=0)
        self.menu.add_command(label='Shrink/Expand',command=lambda:commands['shrink'](self.number))
        self.menu.add_command(label='Rename',command=lambda:commands['rename'](self.number,askstring('Rename column','Rename column')))
        self.menu.add_separator()
        menu2.add_command(label='0 (False)',command=lambda:commands['fill0'](self.number))
        menu2.add_command(label='1 (True)',command=lambda:commands['fill1'](self.number))
        self.menu.add_cascade(label='Fill...',menu=menu2)
        self.menu.add_command(label='Copy to...',command=lambda:commands['copy'](self.number))
        self.menu.add_command(label='Clear',command=lambda:commands['clear'](self.number))
        self.menu.add_separator()
        self.menu.add_command(label='Insert %s before'%self.name,command=lambda:commands['insert'](self.number))
        self.menu.add_command(label='Insert %s after'%self.name,command=lambda:commands['insert'](self.number+1))
        self.menu.add_command(label='Insert 8 %ss after'%self.name,command=lambda:[commands['insert'](self.number+1)for i in range(8)])
        self.menu.add_command(label='Delete '+self.name,command=lambda:commands['delete'](self.number))
    def make_menu2(self,commands):None
class TableRowButton(TableButton):
    def make_menu(self,commands):
        self.menu.add_command(label='Copy to...',command=lambda:commands['copy'](self.number))
        self.menu.add_command(label='Clear',command=lambda:commands['clear'](self.number))
        self.menu.add_separator()
        self.menu.add_command(label='Set as header',command=lambda:commands['head'](self.number))
class FastaTableButton(TableButton):
    def make_menu(self,commands):
        self.menu.add_command(label='Show coordinates',command=lambda:commands['show'](self.number))
        if self.name=='row':self.menu.add_command(label='Rename',command=lambda:commands['rename'](self.number,askstring('Rename row','Rename row')))
class Table(LabelFrame):
    width=10
    height=16
    minwidth=2
    minheight=5
    maxwidth=20
    maxheight=50
    def __init__(self,master=None,array=None,header=False,**kw):
        LabelFrame.__init__(self,master=master,**kw)
        self.vbar=Scrollbar(self,command=self.vscroll)
        self.hbar=Scrollbar(self,orient='horizontal',command=self.hscroll)
        self.zoomy=ZoomScale(self,from_=self.minheight,to=self.maxheight,default=self.height,style='inline',text='Rows',font=(None,6),orient='vertical',command=lambda y:self.zoom(None,y))
        self.zoomx=ZoomScale(self,from_=self.minwidth,to=self.maxwidth,default=self.width,style='inline',text='Cols',command=lambda x:self.zoom(x))
        self.zoomf=ZoomScale(self,from_=1,to=14,default=8,style='inline',text='Font',command=lambda f:self.zoom(None,None,f))
        self.bind("<Enter>", self._bind_mouse)
        self.bind("<Leave>", self._unbind_mouse)
        self.columnconfigure(tuple(range(self.width+1)), weight=1)
        self.rowconfigure(tuple(range(self.height+2)), weight=1)
        self.header=BooleanVar(self,value=header)
        self.create_ui()
        self.W=self.H=self.w=self.h=self.X=self.Y=0
        self.bind_all('<<editvalues>>', self.update_table)
        self.load(array)
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
        func = self.hscroll if event.state & 1 else self.vscroll 
        if event.num == 4 or event.delta > 0:func("scroll",'-1')
        elif event.num == 5 or event.delta < 0:func("scroll",'1')
    def create_ui(self):
        self.Array=[[EntryLabel(self,relief='groove',height=1)for y in range(self.maxheight)]for x in range(self.maxwidth)]
        self.rulerY=[TableRowButton(self,'row',y,{'insert':self.insertrow,'delete':self.deleterow,'copy':self.copyrow,'head':self.head,'clear':lambda n:self.fillrow(n,""),'default':None},height=1)for y in range(self.maxheight)]
        self.rulerX=[TableColumnButton(self,'column',x,{'insert':self.insertcol,'delete':self.deletecol,'copy':self.copycol,'shrink':self.shrink,'rename':self.rename,
                                                        'fill0':lambda n:self.fill(n,0),'fill1':lambda n:self.fill(n,1),'clear':lambda n:self.fill(n,""),
                                                        'default':'shrink'})for x in range(self.maxwidth)]
    def load(self,array,file=None):
        #if len(array)*len(array.T):
        self.array=self.preload(array)
        self.m={}
        if file is not None:self.config(text=file)
        self.event_generate('<<loadvalues>>')
        self.update_table()
        #else:showerror('Fail!','Cannot load data:\nEmpty data, nothing to load')
    def preload(self,array):return array
    def draw_ui(self):
        for i in range(len(self.Array)):
            for j in range(len(self.Array[i])):
                self.Array[i][j].grid_forget()
        for i in self.rulerX:i.grid_forget()
        for i in self.rulerY:i.grid_forget()
        for x in range(self.w):
            self.rulerX[x].grid(row=1,column=x+1,sticky='nsew')
        for y in range(self.h):
            self.rulerY[y].grid(row=y+2,column=0,sticky='nsew')
            for x in range(self.w):
                self.Array[x][y].grid(row=y+2,column=x+1,sticky='nsew')
                self.Array[x][y].bind('<<close>>',(lambda a,b:lambda e:self.update_array(a,b))(x,y))
        self.hbar.grid(row=self.height+2,column=1,columnspan=self.width,sticky='nsew')
        self.vbar.grid(row=2,column=self.width+1,rowspan=self.height,sticky='nsew')
        self.zoomy.grid(row=1,column=self.width+2,rowspan=self.height+2,sticky='nsew')
        self.zoomx.grid(row=self.height+3,column=0,columnspan=self.width+2,sticky='nsew')
        self.zoomf.grid(row=0,column=0,columnspan=self.width+2,sticky='nsew')
        self.rowconfigure(tuple(range(self.height+2)), weight=1)
    def update_array(self,x,y,val=None):
        if not val:
            val=self.Array[x][y].get()
        val=number(val)
        try:
            self.array.iloc[y+self.Y,x+self.X]=val
        except IndexError:
            showerror('Error','An error has occured in pandas package.')
        self.event_generate('<<editvalues>>');self.update_table()
    def shrink(self,x):
        if x in self.m:self.m[x]=not self.m[x]
        else: self.m[x]=True
        self.update_table()
    def rename(self,x,name=None):
        if name is not None:
            a=self.array.T.reset_index();
            b=[*a.loc[:,'index']]
            b[x]=name
            a.loc[:,'index']=b;
            self.array=a.set_index('index').T
            self.update_table()
    def head(self,y):
        a=self.array.T.reset_index();
        a.loc[:,'index']=self.array.iloc[y,:]
        self.array=a.set_index('index').T
        self.update_table()
    def fill(self,x,value):
        self.array.iloc[:,x]=[value for i in range(len(self.array.iloc[:,x]))]
        self.event_generate('<<editvalues>>');self.update_table()
    def fillrow(self,y,value):
        self.array.iloc[y,:]=[value for i in range(len(self.array.iloc[y,:]))]
        self.event_generate('<<editvalues>>');self.update_table()
    def insertcol(self,x):
        self.array = concat([self.array.iloc[:,0:x], DataFrame(['']*self.H), self.array.iloc[:, x:]], axis=1)
        self.event_generate('<<editvalues>>');self.update_table()
    def deletecol(self,x):
        self.array = concat([self.array.iloc[:,0:x], self.array.iloc[:, x+1:]], axis=1)
        self.event_generate('<<editvalues>>');self.update_table()
    def copycol(self,x):
        if col:=whereto('Copy column','Where to?',self.W-1,'y'):
            self.array.iloc[:,col]=self.array.iloc[:,x]
            self.event_generate('<<editvalues>>');self.update_table() 
    def copyrow(self,y):
        if row:=whereto('Copy row','Where to?',self.H-1,'x'):
            self.array.iloc[row,:]=self.array.iloc[y,:]
            self.event_generate('<<editvalues>>');self.update_table() 
    def insertrow(self,y):
        self.array = concat([self.array.iloc[0:y,:], DataFrame(['']*self.W).T, self.array.iloc[y:, :]], axis=0).reset_index(drop=True)
        self.event_generate('<<editvalues>>');self.update_table()
    def deleterow(self,y):
        self.array = concat([self.array.iloc[0:y,:], self.array.iloc[y+1:, :]], axis=0).reset_index(drop=True)
        self.event_generate('<<editvalues>>');self.update_table()
    def update_size(self,force=False):
        W=len(self.array.T)
        H=len(self.array)
        if force or(not((W==self.W)and(H==self.H))):
            self.w=min(W,self.width)
            self.h=min(H,self.height)
            self.W=W
            self.H=H
            self.draw_ui()
            self.event_generate('<<resize>>')
        while self.Y+self.h>H:self.Y-=1
        while self.X+self.w>W:self.X-=1
        if self.H:self.vbar.set(self.Y/self.H,(self.Y+self.height)/self.H)
        else:self.vbar.set(0,1)
        if self.W:self.hbar.set(self.X/self.W,(self.X+self.width)/self.W)
        else:self.hbar.set(0,1)
    def update_table(self,event=None,force=False):
        self.update_size(force=force)
        for x in range(self.w):
            self.rulerX[x].config(text='%s: %s'%(x+self.X,list(self.array.T.index)[x+self.X]),number=x+self.X)
        for y in range(self.h):
            self.rulerY[y].config(text=y+self.Y,number=y+self.Y,width=len(str(self.H)))
            for x in range(self.w):
                if((x+self.X)in self.m)and self.m[x+self.X]:m=1
                else:
                    m=max(len(str(k))for k in self.array.iloc[:,x+self.X])
                    if not m:m=1
                self.Array[x][y].set(self.array.iloc[y+self.Y,x+self.X])
                self.columnconfigure(x+1, weight=m)
                self.Array[x][y].label.config(width=m)
                self.rulerX[x].config(width=m)
    def up(self):self.Y-=(1 if self.Y else 0);self.update_table()
    def left(self):self.X-=(1 if self.X else 0);self.update_table()
    def right(self):self.X+=(1 if self.X+self.width<len(self.array.T)else 0);self.update_table()
    def down(self):self.Y+=(1 if self.Y+self.height<len(self.array)else 0);self.update_table()
    def vscroll(self,type,amount,*a):
        if type=='scroll':
            if amount=='-1':self.up()
            elif amount=='1':self.down()
        elif type=='moveto':
            self.Y=int(float(amount)*(self.H-1));self.update_table()
        if self.H:self.vbar.set(self.Y/self.H,(self.Y+self.height)/self.H)
        else:self.vbar.set(0,1)
    def hscroll(self,type,amount,*a):
        if type=='scroll':
            if amount=='-1':self.left()
            elif amount=='1':self.right()
        elif type=='moveto':
            self.X=int(float(amount)*(self.W-1));self.update_table()
        if self.W:self.hbar.set(self.X/self.W,(self.X+self.width)/self.W)
        else:self.hbar.set(0,1)
    def __getitem__(self,key):
        return self.array.iloc[key]
    def __setitem__(self,key,value):
        self.array.iloc[*key]=value
        self.event_generate('<<editvalues>>');self.update_table()
    def zoom(self,x=None,y=None,f=None):
        if x is not None:self.width=x
        if y is not None:self.height=y
        if bool(x)or bool(y):
            self.update_table(force=True)
        if f is not None:
            for i in range(len(self.Array)):
                for j in range(len(self.Array[i])):
                    self.Array[i][j].config(font=(None,f))
            for i in self.rulerX:i.config(font=(None,f))
            for i in self.rulerY:i.config(font=(None,f))
a={'afilmvj':'yellow','c':'khaki','de':'red','g':'purple1','h':'cyan','kpr':'DeepSkyBlue','nqstw':'lime','x':'grey','y':'YellowGreen','?.- ':'white'}
COLOR_PROTEIN={**{j:a[i] for i in a for j in i},**{j.upper():a[i] for i in a for j in i}}
a={'a':'lime','c':'DeepSkyBlue','tu':'red','g':'purple1','nx':'grey','?-. ':'white'}
COLOR_GENE={**{j:a[i] for i in a for j in i},**{j.upper():a[i] for i in a for j in i}}
class FastaColorEntry(EntryLabel):
    def __init__(self,master,protein,text=None,cnf={},**kw):
        EntryLabel.__init__(self,master,text=text,cnf=cnf,**kw)
        self.protein=protein
        protein.trace_add('write',self.setcolor)
        self.trace_add('write',self.recolor)
        self.setcolor()
    def close(self,event=None):
        self.pack_forget_()
        self.label.pack(side='left',fill='x',expand=True)
        self.event_generate('<<close>>')
        self.recolor()
    def setcolor(self,*a):
        self.color=COLOR_PROTEIN if self.protein.get()else COLOR_GENE
        self.recolor()
    def recolor(self,*a):
        self.label.config(bg=self.color.get(self.get(),'white'))
class FastaTable(Table):
    width=40
    height=20
    maxwidth=20
    maxheight=10
    maxwidth=80
    maxheight=50
    def preload(self,array):return array.T.reset_index(drop=True).T
    def create_ui(self):
        self.protein=BooleanVar(value=False)
        self.Array=[[FastaColorEntry(self,self.protein,font=(None,7),relief='flat')for y in range(self.maxheight)]for x in range(self.maxwidth)]
        self.rulerY=[FastaTableButton(self,'row',y,{'insert':self.insertrow,'delete':self.deleterow,'show':self.showy,'rename':self.rename,'default':'show'},font=(None,7))for y in range(self.maxheight)]
        self.rulerX=[FastaTableButton(self,'column',x,{'insert':self.insertrow,'delete':self.deleterow,'show':self.showx,'default':'show'},font=(None,7))for x in range(self.maxwidth)]
        self.loc=Label(self,relief='groove')
        self.loc.grid(row=1,column=0)
    def rename(self,x,name=None):
        if name is not None:
            b=[*self.array.index]
            b[x]=name
            self.array.index=b
            self.update_table() 
    def showx(self,x):
        showinfo('Coordinates','Column: %s'%(x))
    def showy(self,y):
        showinfo('Coordinates','Row: %s'%(y))
    def insertcol(self,x):
        self.array = concat([self.array.iloc[:,0:x], DataFrame(['']*self.H), self.array.iloc[:, x:]], axis=1).fillna("").T.reset_index(drop=True).T
        self.update_table()
    def deletecol(self,x):
        self.array = concat([self.array.iloc[:,0:x], self.array.iloc[:, x+1:]], axis=1).fillna("").T.reset_index(drop=True).T
        self.event_generate('<<editvalues>>')
    def deletecols(self,start,end):
        self.array = concat([self.array.iloc[:,0:start], self.array.iloc[:, end+1:]], axis=1).fillna("").T.reset_index(drop=True).T
        self.event_generate('<<editvalues>>')
    def insertrow(self,y):
        self.array = concat([self.array.iloc[0:y,:], DataFrame(['']*self.W).T, self.array.iloc[y:, :]], axis=0).fillna("")
        self.event_generate('<<editvalues>>')
    def deleterow(self,y):
        self.array = concat([self.array.iloc[0:y,:], self.array.iloc[y+1:, :]], axis=0).fillna("")
        self.event_generate('<<editvalues>>')
    def update_table(self,event=None,force=False):
        self.update_size(force=force)
        self.loc.config(text='row:%s column:%s'%(self.Y,self.X))
        indice=[str(i)for i in self.array.index]
        for x in range(self.w):
            self.rulerX[x].config(text=(x+self.X)%10,number=x+self.X,width=1,anchor='w')
        for y in range(self.h):
            self.rulerY[y].config(text=indice[y+self.Y][:32],number=y+self.Y,width=min(len(indice[y+self.Y]),32))
            for x in range(self.w):
                if((x+self.X)in self.m)and self.m[x+self.X]:m=1
                else:
                    m=max(len(str(k))for k in self.array.iloc[:,x+self.X])
                    if not m:m=1
                self.Array[x][y].set(self.array.iloc[y+self.Y,x+self.X])
                self.columnconfigure(x+1, weight=m)
                self.Array[x][y].label.config(width=m)


####################################whereto ####################################
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
