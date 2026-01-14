if __name__!='__main__':raise ImportError("This program is a standalone software and cannot be imported as module")
import strings
strings.LANGUAGE='EN'
from strings import STRINGS
try:
    from tkinter import Tk,Toplevel,Button,Checkbutton,Entry,Frame,Label,LabelFrame,PanedWindow,PhotoImage,BooleanVar,StringVar,IntVar
    from tkinter.filedialog import askopenfilenames,askdirectory
    from tkinter.messagebox import showerror,showinfo,showwarning,askyesno
    from tkinter.ttk import Notebook,Style
except ImportError:
    from sys import stderr
    print('Your Python is not configured for Tk. The program cannot be run.',file=stderr)
    input('Press Enter to exit.')
    exit(1)
from sys import platform
if platform=='win32':None
elif platform=='darwin':showwarning(STRINGS.loc['MISC::WARNING',LANGUAGE],STRINGS.loc['PLATFORM::darwin',LANGUAGE])
elif platform=='linux':showwarning(STRINGS.loc['MISC::WARNING',LANGUAGE],STRINGS.loc['PLATFORM::linux',LANGUAGE])
elif platform=='android':showerror(STRINGS.loc['MISC::ERROR',LANGUAGE],STRINGS.loc['PLATFORM::android',LANGUAGE]);exit(1)
elif platform=='ios':showerror(STRINGS.loc['MISC::ERROR',LANGUAGE],STRINGS.loc['PLATFORM::ios',LANGUAGE]);exit(1)
elif platform=='emscripten':showerror(STRINGS.loc['MISC::ERROR',LANGUAGE],STRINGS.loc['PLATFORM::UNSUPPORTED',LANGUAGE]);exit(1)
elif platform=='wasi':showerror(STRINGS.loc['MISC::WARNING',LANGUAGE],STRINGS.loc['PLATFORM::UNSUPPORTED',LANGUAGE]);exit(1)
else:showwarning(STRINGS.loc['MISC::WARNING',LANGUAGE],STRINGS.loc['PLATFORM::OTHER',LANGUAGE].format(platform))
#print('Loading dependencies 1/4:\ntk2')
try:
    from tk2 import EntryLabel,LabelMenu2,OmniSpin,OmniText,OpenFileButton,ResizableOmniText,ScrolledLabelFrame,ToggleButton,ToggleRadioButton
except ImportError:
    showerror(STRINGS.loc['PRELOAD::MISSING:PACKAGE_TITLE',LANGUAGE].format('tk2'),STRINGS.loc['PRELOAD::MISSING:REQUIRED_LIBRARY',LANGUAGE].format('tk2'))
    exit(1)
#print('Loading dependencies 2/4:\n<GeneProt library>')
try:
    from custom import *
except ImportError:
    showerror(STRINGS.loc['PRELOAD::MISSING:PACKAGE_TITLE',LANGUAGE].format('custom'),STRINGS.loc['PRELOAD::MISSING:REQUIRED_LIBRARY',LANGUAGE].format('custom'))
    exit(1)
#print('Loading dependencies 3/4:\npandas')
try:
    from pandas import DataFrame,concat
except:
    from sys import platform
    if platform=='win32':advice='If you have admin rights, you can install pandas using Command Prompt:\n\npy -m pip install pandas'
    elif platform=='darwin':advice='You can install pandas via Terminal. You will have to input your password:\n\nsudo pip3 install pandas'
    else:advice='If you are a superuser, you can run\n\nsudo pip3 install pandas\n\nto install pandas'
    showerror(STRINGS.loc['PRELOAD::MISSING:PACKAGE_TITLE',LANGUAGE].format('pandas'),STRINGS.loc['PRELOAD::MISSING:REQUIRED_PACKAGE',LANGUAGE].format('pandas')+'\n'+advice)
    exit(1)
from re import search
from os import sep as ossep,getcwd,remove
from os.path import exists
from time import time
from zipfile import ZipFile
#print('Loading dependencies 4/4:\nBiopython')
try:
    from Bio.Entrez.Parser import NotXMLError
    from Bio import Entrez,SeqIO
    from urllib.error import HTTPError
    from http.client import RemoteDisconnected,IncompleteRead
    online=True
except:
    online=False
    if not askyesno(STRINGS.loc['PRELOAD::MISSING:PACKAGE_TITLE',LANGUAGE].format('bio'),STRINGS.loc['PRELOAD::MISSING:PACKAGE',LANGUAGE].format('bio','needed for online functionality','online functionality (access to GenBank, GenPept, NCBI Taxonomy)')):
        exit()
#import csv
import subprocess
from io import StringIO
tk=Tk()
tk.withdraw()
tk.title(STRINGS.loc['TITLE',LANGUAGE])
def testforblast(path,name,name2,message):
    #return False
    available=False
    a=0
    try:
        process = subprocess.Popen(path+' -version', stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        while True:
            output = process.stdout.readline()
            if output[:len(name)]==name:available=output;break
            if process.poll() is not None:a=97
            if a>100:break
            a+=1
    except FileNotFoundError:print('nope');available=False
    if not available:
        if not askyesno(STRINGS.loc['PRELOAD::MISSING:UTILITY_TITLE',LANGUAGE].format(name2),STRINGS.loc['PRELOAD::MISSING:UTILITY',LANGUAGE].format(name2,message)):exit()
    return available
L=ProgressLogger(tk,4)
if platform=='win32':
    blast_path=join(getcwd(),'bin','win32','blastn.exe')
    makeblastdb_path=join(getcwd(),'bin','win32','makeblastdb.exe')
    sevenz_path=join(getcwd(),'bin','win32','7z.exe')
elif platform=='darwin':
    blast_path=join(getcwd(),'bin','darwin','blastn')
    makeblastdb_path=join(getcwd(),'bin','darwin','makeblastdb')
    sevenz_path=join(getcwd(),'bin','darwin','7zz'),
elif platform=='linux':
    blast_path=join(getcwd(),'bin','linux','blastn')
    makeblastdb_path=join(getcwd(),'bin','linux','makeblastdb')
    sevenz_path=join(getcwd(),'bin','linux','7zzs')
else:
    blast_path=join(getcwd(),'bin','linux','blastn')
    makeblastdb_path=join(getcwd(),'bin','linux','makeblastdb')
    sevenz_path=join(getcwd(),'bin','linux','7zzs')

L.step(STRINGS.loc['PRELOAD::UTIL',LANGUAGE].format(1,3,'blastn'))
blast=testforblast(blast_path,'blastn','blastn',STRINGS.loc['PRELOAD::MISSING:UTILITY_MESSAGE',LANGUAGE].format(STRINGS.loc['PRELOAD::BLASTN:1',LANGUAGE],STRINGS.loc['PRELOAD::BLASTN:2',LANGUAGE]))
L.step(STRINGS.loc['PRELOAD::UTIL',LANGUAGE].format(2,3,'makeblastdb'))
makeblastdb=testforblast(makeblastdb_path,'makeblastdb','makeblastdb',STRINGS.loc['PRELOAD::MISSING:UTILITY_MESSAGE',LANGUAGE].format(STRINGS.loc['PRELOAD::MAKEBLASTDB:1',LANGUAGE],STRINGS.loc['PRELOAD::MAKEBLASTDB:2',LANGUAGE]))
L.step(STRINGS.loc['PRELOAD::UTIL',LANGUAGE].format(3,3,'7-Zip'))
sevenz=testforblast(sevenz_path,'7-Zip','7-Zip',STRINGS.loc['PRELOAD::MISSING:UTILITY_MESSAGE',LANGUAGE].format(STRINGS.loc['PRELOAD::SEVENZ:1',LANGUAGE],STRINGS.loc['PRELOAD::SEVENZ:2',LANGUAGE]))

L.step(STRINGS.loc['PRELOAD::GUI',LANGUAGE])
DB={}
FASTA=['FASTA','*.fas',((STRINGS.loc['FORMAT::FASTA',LANGUAGE],'*.fas *.fta *.fasta'),
                        (STRINGS.loc['FORMAT::FASTA:NUCL',LANGUAGE],'*.ffn *.fna'),
                        (STRINGS.loc['FORMAT::FASTA:PROT',LANGUAGE],'*.faa'),
                        (STRINGS.loc['FORMAT::*',LANGUAGE],'*'))]

class Downloader:
    def geneprot(self, LIST, mask, offset, fetch, base, pre, main, main2, post, mode, eskw={},efkw={},**kw):
        self.lock()
        i=f=d=0
        t=time()
        l=len(LIST)
        if mask is None:mask=[True]*l
        l2=sum([bool(i)for i in mask])-offset
        self.dashboard.config(all=f'{l} ({l2} to do)')
        FAILS=[]
        try:
            for i in range(offset,l):
                if bool(mask[i]):
                    pre(LIST=LIST,FAILS=FAILS,i=i,l=l,f=f,d=d,**kw)
                    if self.stopped.get():raise KeyboardInterrupt
                    entry=str(LIST[i]).rstrip()
                    if entry in ['','0',' ']:FAILS.append(LIST[i]);self.print(f'{i}/{l}: fail (invalid entry "{entry}")');f+=1;continue
                    else:
                        try:
                            handle = Entrez.esearch(db=base,term=(entry),**eskw)
                            record=Entrez.read(handle)
                            if 'ErrorList' in record:self.print(f'{i}/{l}: fail ({record["ErrorList"]})');FAILS.append(entry);f+=1;
                            else:
                                if fetch:
                                    if not record["IdList"]:self.print(f'{i}/{l}: fail (not found)');FAILS.append(entry);f+=1;
                                    elif len(record["IdList"])>1:self.print(f'{i}/{l}: fail (ambiguous)');FAILS.append(entry);f+=1;
                                    elif len(record["IdList"])==1:
                                        try:
                                            handle2 = Entrez.efetch(db=base, id=record["IdList"][0],**efkw)
                                            if mode=='r':record2 = handle2.read()
                                            elif mode=='rb':record2 = Entrez.read(handle2)
                                            main2(curr=record2,LIST=LIST,FAILS=FAILS,i=i,l=l,f=f,d=d,**kw)
                                            d+=1
                                        except(HTTPError,RemoteDisconnected,IncompleteRead,RuntimeError,NotXMLError,ValueError)as E:self.print(f'{i}/{l}: fail ({repr(E)})');FAILS.append(entry);f+=1
                                else:
                                    try:
                                        main(curr=record,LIST=LIST,FAILS=FAILS,i=i,l=l,f=f,d=d,**kw)
                                        d+=1
                                    except OtherError as E:self.print(f'{i}/{l}: fail (E.args[0])');FAILS.append(entry);f+=1;
                                    except(HTTPError,RemoteDisconnected,IncompleteRead,RuntimeError,NotXMLError,ValueError)as E:self.print(f'{i}/{l}: fail ({repr(E)})');FAILS.append(entry);f+=1    
                        except(HTTPError,RemoteDisconnected,IncompleteRead,RuntimeError,NotXMLError,ValueError)as E:self.print(f'{i}/{l}: fail ({repr(E)})');FAILS.append(entry);f+=1
                    T=int(time()-t)
                    T2=(int(T*(l-i)/(i)))if i!=0 else 0
                    self.dashboard.config(done=d,fail=f,left=l2-d,elapsed=f'{T//86400}d {(T//3600)%24:02.0f}:{(T//60)%60:02.0f}:{T%60:02.0f}',ETA=f'{T2//86400}d {(T2//3600)%24:02.0f}:{(T2//60)%60:02.0f}:{T2%60:02.0f}')
                    self.cpr()
                else:continue
        except KeyboardInterrupt:
            self.print('\nOperation successfully interrupted\n')
        post(LIST=LIST,FAILS=FAILS,i=i,l=l,f=f,d=d,**kw)
        self.unlock()
    def skip(self,*,curr=None,LIST=None,FAILS=None,i=None,l=None,f=None,d=None,**kw):None
    def ding(self,auto=False):
        if not auto:
            self.print('All done!')
            self.text.bell()
            print('All done!')
    def lpc(self,auto,text,end='\n'):
        if not auto:self.lock()
        self.print(text=text,end=end)
        self.cpr()
    def unding(self,auto):
        if not auto:
            self.unlock()
            self.print('All done!')
            self.text.bell()
            print('All done!')
    def print(self,text,end='\n'):
        self.text.insert('end',text+end);self.text.see('end');
        print(text,end=end)
    def stop(self,*a):
        self.text.insert('end','\n'+'~'*40+'\nE-Stop '+('engaged'if self.stopped.get()else'released')+'!\n'+'~'*40+'\n');self.text.see('end')
        self.unlock()
    def lock(self):
        for i in self.controls:i.config(state='disabled')
    def unlock(self):
        for i in self.controls:i.config(state='normal')
class Middle(Downloader,PanedWindow):
    DB=DB
    def __init__(self,tk,master,left,right,online,blast):
        self.table=left;self.fasta=right;self.table.printer=self
        for i in self.DB:self.DB[i].printer=self
        PanedWindow.__init__(self,master=master,orient='vertical')
        self.root=tk
        self.debug=BooleanVar(self,value=False)
        self.debug.trace_add('write',lambda*a:self.print(f'Debug mode {"en"if self.debug.get()else"dis"}abled!'))
        self.debugger=LabelFrame(master,text='Debug',relief='ridge')
        Checkbutton(self.debugger,text='Debug',variable=self.debug,state='normal').grid(row=0,column=0,columnspan=2)
        Button(self.debugger,text='Lock',command=self.lock).grid(row=1,column=1)
        Button(self.debugger,text='Un',command=self.unlock).grid(row=1,column=0)
        Button(self.debugger,text='X',command=lambda:(self.debugger.place_forget(),self.debug.set(False))).grid(row=1,column=2)
        def add_dedup():
            bc=LabelFrame(b,text=STRINGS.loc['MID::DEDUP',LANGUAGE])
            dd1=Button(bc,text=STRINGS.loc['MID::DEDUP:READS',LANGUAGE],command=self.dedup1);dd1.pack(side='left',fill='x',expand=True)
            dd2=Button(bc,text=STRINGS.loc['MID::DEDUP:ACCESSIONS',LANGUAGE],command=self.dedup2);dd2.pack(side='left',fill='x',expand=True)
            dd3=Button(bc,text=STRINGS.loc['MID::DEDUP:TAXIDS',LANGUAGE],command=self.dedup3);dd3.pack(side='left',fill='x',expand=True)
            bc.pack(fill='x',expand=True)
            de.destroy()
        de=Button(self.debugger,text='Add dedup',command=add_dedup);de.grid(row=2,column=0,columnspan=3)
        right.text.bind('<Control-Shift-Double-1>',lambda e:(self.debugger.place(x=0,y=0),self.debug.set(True),"break")[2]if right.text.get(1.0,1.5)=='debug'else"break")
        self.debugger.bind('<Control-Shift-1>',lambda e:(self.debugger.place_forget(),self.debug.set(False),"break")[2])

        tools=LabelFrame(self,text=STRINGS.loc['MID::TOOLS',LANGUAGE])
        tools.rowconfigure((0,1,2,3),weight=1)
        self.add(tools)
        
        self.google=Search(self.table.top,STRINGS.loc['MID::SEARCH',LANGUAGE],
                           {STRINGS.loc['MID::SEARCH:ANY',LANGUAGE]:'Any',
                            STRINGS.loc['MID::SEARCH:STRICT',LANGUAGE]:'Exact',
                            STRINGS.loc['MID::SEARCH:REGEX',LANGUAGE]:'Regex'},
                           'Any',self.query)        
        self.google.grid(row=0,column=1)

        tzm=LabelFrame(self.table.top,text=STRINGS.loc['MID::TABLE',LANGUAGE])
        tzm.grid(row=1,column=1)
        m1=Button(tzm,text=STRINGS.loc['MID::TABLE:FUNCTIONS',LANGUAGE],command=self.manipulate1);m1.pack(side='left',fill='x',expand=True)
        m2=Button(tzm,text=STRINGS.loc['MID::TABLE:STATISTICS',LANGUAGE],command=self.manipulate2);m2.pack(side='left',fill='x',expand=True)
        m3=Button(tzm,text=STRINGS.loc['MID::TABLE:OPERATE',LANGUAGE],state='disabled');m3.pack(side='left',fill='x',expand=True)
        
        a=LabelFrame(tools,text='Manage databases')
        aa=Frame(a)
        aa.pack(fill='x',expand=True)
        ab=Frame(a)
        ab.pack(fill='x',expand=True)
        db1=Button(aa,text=STRINGS.loc['DB::GB2TAXID',LANGUAGE],command=self.DB['gb2taxid']);db1.pack(side='left',fill='x',expand=True)
        db2=Button(aa,text=STRINGS.loc['DB::TAXDUMP',LANGUAGE],command=self.DB['taxdump']);db2.pack(side='left',fill='x',expand=True)
        db3=Button(ab,text=STRINGS.loc['DB::FASTA',LANGUAGE],command=self.DB['FDB']);db3.pack(side='left',fill='x',expand=True)
        db4=Button(aa,text=STRINGS.loc['DB::BLAST',LANGUAGE],command=self.DB['BLAST']);db4.pack(side='left',fill='x',expand=True)
        db5=Button(ab,text=STRINGS.loc['DB::SAPROBITY',LANGUAGE],command=self.DB['Saprobity']);db5.pack(side='left',fill='x',expand=True)
        a.grid(row=0,column=0,sticky='nsew')
        
        b=LabelFrame(tools,text=STRINGS.loc['MID::AUTO:FULL',LANGUAGE])
        ba=Frame(b)
        ba.pack(fill='x',expand=True)
        bb=Frame(b)
        bb.pack(fill='x',expand=True)
        run=Button(ba,text=STRINGS.loc['MID::AUTO:FULL',LANGUAGE],state='disabled');run.pack(side='left',fill='x',expand=True)
        rnd=Button(ba,text=STRINGS.loc['MID::AUTO:BOOTSTRAP',LANGUAGE],state='disabled');rnd.pack(side='left',fill='x',expand=True)
        rdn=Button(ba,text=STRINGS.loc['MID::AUTO:IDENTIFY',LANGUAGE],command=self.identify,state='normal'if blast else'disabled');rdn.pack(side='left',fill='x',expand=True)
        bl=Button(bb,text=STRINGS.loc['MID::AUTO:BLAST',LANGUAGE],command=self.blast,state='normal'if blast else'disabled');bl.pack(side='left',fill='x',expand=True)
        dd=Button(bb,text=STRINGS.loc['MID::AUTO:DEDUP',LANGUAGE],command=self.dedup);dd.pack(side='left',fill='x',expand=True)
        ev=Button(bb,text=STRINGS.loc['MID::AUTO:EVALUATE',LANGUAGE],state='disabled');ev.pack(side='left',fill='x',expand=True)
        b.grid(row=1,column=0,sticky='nsew')
        
        c=LabelFrame(tools,text=STRINGS.loc['MID::FASTA_TASKS',LANGUAGE])
        rn=Button(c,text=STRINGS.loc['MID::FASTA_TASKS:RENAME',LANGUAGE],state='disabled');rn.pack(side='left',fill='x',expand=True)
        mg=Button(c,text=STRINGS.loc['MID::FASTA_TASKS:MERGE',LANGUAGE],state='disabled');mg.pack(side='left',fill='x',expand=True)
        ft=Button(c,text=STRINGS.loc['MID::FASTA_TASKS:TABLE',LANGUAGE],command=self.storefasta);ft.pack(side='left',fill='x',expand=True)
        c.grid(row=2,column=0,sticky='nsew')
        
        d=LabelFrame(tools,text=STRINGS.loc['MID::ONLINE_TASKS'if online else'MID::OFFLINE_TASKS',LANGUAGE])
        Label(d,text=STRINGS.loc['MID::GET:TAXONOMY',LANGUAGE]).grid(row=0,column=0,sticky='nsew')
        tax1=Button(d,text=STRINGS.loc['MID::OFFLINE',LANGUAGE],command=self.offlinetaxonomy);tax1.grid(row=0,column=1,sticky='nsew')
        tax2=Button(d,text=STRINGS.loc['MID::ONLINE',LANGUAGE],command=self.onlinetaxonomy,state='normal'if online else'disabled');tax2.grid(row=0,column=2,sticky='nsew')
        Label(d,text=STRINGS.loc['MID::GET:SEQUENCES',LANGUAGE]).grid(row=1,column=0,sticky='nsew')
        seq1=Button(d,text=STRINGS.loc['MID::OFFLINE',LANGUAGE],command=self.offlinedownload);seq1.grid(row=1,column=1,sticky='nsew')
        seq2=Button(d,text=STRINGS.loc['MID::ONLINE',LANGUAGE],command=self.onlinedownload,state='normal'if online else'disabled');seq2.grid(row=1,column=2,sticky='nsew')
        Label(d,text=STRINGS.loc['MID::GET:SAPROBITY',LANGUAGE]).grid(row=2,column=0,sticky='nsew')
        sap1=Button(d,text=STRINGS.loc['MID::OFFLINE',LANGUAGE],command=self.offlinesaprobity);sap1.grid(row=2,column=1,sticky='nsew')
        sap2=Button(d,text=STRINGS.loc['MID::ONLINE',LANGUAGE],state='disabled');sap2.grid(row=2,column=2,sticky='nsew')
        self.controls=[m1,m2,#m3,
                       db1,db2,db3,db4,
                       rdn,dd,#rn,mg,
                       ft,tax1,seq1,sap1
                       ]
        d.columnconfigure((0,1,2), weight=1)
        d.rowconfigure((0,1,2), weight=1)
        d.grid(row=3,column=0,sticky='nsew')
        
        status=LabelFrame(self,text=STRINGS.loc['MID::STATUS',LANGUAGE])
        grid=Frame(status);grid.pack(fill='x',expand=True)
        self.dashboard=Dashboard(status,orient='horizontal');self.dashboard.pack(fill='both',expand=True)
        self.stopped=ToggleButton(status,text=STRINGS.loc['MID::ESTOP',LANGUAGE],border=4,bg='red',value=False)
        self.stopped.pack(side='left',fill='both',expand=True)
        self.stopped.trace_add('write',self.stop)
        self.add(status)
        
        self.text=OmniText(self,text='Log',scrolling=(1,1),width=40,height=16,log_buttons=True,font=('Courier New',7))
        self.add(self.text)
        
        if not online:
            Label(status,text='Package "bio" is unavailable!',relief='raised',state='disabled',height=7).pack()#fill='both',expand=True)#  .grid(row=2,column=0,columnspan=3,sticky='nsew')
            self.print('Package "bio" is unavailable!')
        else:
            self.controls.append(tax2)
            self.controls.append(seq2)
        if blast:self.controls.append(bl);self.print(blast)
        else:self.print('Blastn is unavailable!')
        if makeblastdb:self.print(makeblastdb)
        else:self.print('makeblastdb is unavailable!')
    def lock(self):
        for i in self.controls:i.config(state='disabled')
        self.DB['db'].withdraw()
    def storefasta(self):
        if xy:=whereto('Put FASTA in table','Where to?',(self.table.table.H-1,self.table.table.W-1),'xy'):self.table[*xy]=self.fasta.text.get('1.0','end').rstrip()
    def query(self):
        query=self.google.get()
        mode=self.google.mode.get()
        found=False
        for i in range(len(self.table[0,:])):
            col=list(str(i)for i in self.table[:,i])
            for j in range(len(self.table[:,0])):
                if {'Any':lambda q,s:(q in s),
                    'Exact':lambda q,s:q==s,
                    'Regex':lambda q,s:bool(search(q,s))}[mode](query,col[j]):
                    self.print('Found %s at column %s, row %s\n'%(query, i, j))
                    found=True
        if not found:self.text.insert('end','%s was not found in table'%query)
    def getspin(self):return{'width':4,'cnf':{'from':0,'to':self.table.table.W-1}}
    def getio(self,io,type):
        if type=='Taxonomy':
            if len(tx:=(io[0]['Taxonomy']))==2:
                if tx[0]=='Name':
                    tx2=tx[1]
                    if len(tx2)==2:taxnames = list(map(lambda a:a[0]+' '+a[1],zip(self.table[:,tx2[0]],self.table[:,tx2[1]])));print('ngs')
                    else:taxnames = self.table[:,tx2[0]];print('ns')
                elif tx[0]=='txid':
                    taxnames = self.table[:,tx[1]].astype('string').add('[taxid]');print('nx')
                else:
                    taxnames = list(map(lambda a:a[0]+' '+a[1],zip(self.table[:,tx[0]],self.table[:,tx[1]])));print('gs')
            else:taxnames = self.table[:,tx[0]];print('s')
            return taxnames
        elif type=='Filter':
            if'Filter'in io[0]:
                mask=(None if(io[0]['Filter']is None)else(self.table[:,io[0]['Filter']]))
                return mask
            return None
    def setdb(self,type):
        def shorten(s):return ('...'+s[-30:])if len(s)>30 else s
        if type=='GB2Taxid':
            enabled=self.DB['gb2taxid'].zip
            if enabled:return {'title':STRINGS.loc['DB::GB2TAXID',LANGUAGE],'prompt':STRINGS.loc['IO::LOADED_DATABASE',LANGUAGE],'value':True,'valid':True}  #shorten(self.DB['gb2taxid'].zip.filename)
            else:return {'title':STRINGS.loc['DB::GB2TAXID',LANGUAGE],'prompt':STRINGS.loc['IO::LOAD_FIRST',LANGUAGE].format(STRINGS.loc['DB::GB2TAXID',LANGUAGE]),'value':None,'valid':False,'error':'Load GB2Taxid first!'}
        elif type=='Taxdump':
            enabled=self.DB['taxdump'].zip
            if enabled:return {'title':STRINGS.loc['DB::TAXDUMP',LANGUAGE],'prompt':STRINGS.loc['IO::LOADED_DATABASE',LANGUAGE],'value':True,'valid':True}   #shorten(self.DB['taxdump'].zip.filename)
            else:return {'title':STRINGS.loc['DB::TAXDUMP',LANGUAGE],'prompt':STRINGS.loc['IO::LOAD_FIRST',LANGUAGE].format(STRINGS.loc['DB::TAXDUMP',LANGUAGE]),'value':None,'valid':False,'error':'Load new_taxdump.zip first!'}
        elif type=='Saprobity':
            enabled=self.DB['Saprobity'].flag.get()
            if enabled:return {'title':STRINGS.loc['DB::SAPROBITY',LANGUAGE],'prompt':STRINGS.loc['IO::LOADED_DATABASE',LANGUAGE],'value':True,'valid':True}   #shorten(self.DB['taxdump'].zip.filename)
            else:return {'title':STRINGS.loc['DB::SAPROBITY',LANGUAGE],'prompt':STRINGS.loc['IO::LOAD_FIRST',LANGUAGE].format(STRINGS.loc['DB::SAPROBITY',LANGUAGE]),'value':None,'valid':False,'error':'Load a saprobity index first!'}
    def manipulate1(self):
        spin=self.getspin()
        ff=lambda f,a:DataFrame([f(i)for i in a])
        fl2=lambda f,a,b:DataFrame([f(bool(i[0]),bool(i[1]))for i in zip(a,b)])
        def verify(io):
            if io[0]['op']==None or io[0]['op'] in op_nop:showerror(STRINGS.loc['MISC::ERROR',LANGUAGE],STRINGS.loc['DIALOG::OPTION:SELECT',LANGUAGE]);return False
            if io[0]['op'] in op_ternary and((io[0]['2']is None)or(io[0]['3']is None)):showerror(STRINGS.loc['MISC::ERROR',LANGUAGE],STRINGS.loc['IO::MANIPULATE1:ERROR3',LANGUAGE]);return False
            elif io[0]['op'] in op_binary and((io[0]['2']is None)or(io[0]['3']is not None)):showerror(STRINGS.loc['MISC::ERROR',LANGUAGE],STRINGS.loc['IO::MANIPULATE1:ERROR2',LANGUAGE]);return False
            elif io[0]['op'] in op_unary and((io[0]['2']is not None)or(io[0]['3']is not None)):showerror(STRINGS.loc['MISC::ERROR',LANGUAGE],STRINGS.loc['IO::MANIPULATE1:ERROR1',LANGUAGE]);return False
            else:return True
        io=askio('Compare',STRINGS.loc['IO::SELECT:COLUMNS',LANGUAGE],
                 setio(STRINGS.loc['IO::INPUTS',LANGUAGE],{'1':(DSpin,[],{**spin,**{'text':STRINGS.loc['IO::MANIPULATE1:INPUT1',LANGUAGE]}}),
                                 '2':(DSpin,[],{**spin,**{'type':'check','text':STRINGS.loc['IO::MANIPULATE1:INPUT2',LANGUAGE]}}),
                                 '3':(DSpin,[],{**spin,**{'type':'check','text':STRINGS.loc['IO::MANIPULATE1:INPUT3',LANGUAGE]}}),
                                 'op':(DCombo,[],{'text':STRINGS.loc['IO::MANIPULATE1:OPERATOR',LANGUAGE],'values':[*ops]}),
                                 },validate=any),
                 setio('Output',{'o':(DSpin,[],{**spin,**{'text':''}})}),
                 verify)
        if self.debug.get():print(io)
        elif io:
            args=[self.table[:,io[0]['1']]]
            if (I2:=io[0]['2'])is not None:args.append(self.table[:,I2])
            if (I3:=io[0]['3'])is not None:args.append(self.table[:,I3])
            self.table[:,io[1]['o']]=ops[io[0]['op']](*args)
    def manipulate2(self):
        io=whereto(STRINGS.loc['MID::TABLE:STATISTICS',LANGUAGE],STRINGS.loc['IO::SELECT:COLUMNS',LANGUAGE],self.table.table.W-1,'-y')
        if self.debug.get():print(io)
        elif io is not None:
            col=self.table[:,io]
            s=c=0;m=float('inf');M=float('-inf')
            for i in col:
                if isnum(i):s+=i;c+=1;m=min(i,m);M=max(i,M)
            showlines(STRINGS.loc['MID::TABLE:STATISTICS',LANGUAGE],
                      STRINGS.loc['MID::TABLE:STATISTICS',LANGUAGE],
                      {STRINGS.loc['IO::MANIPULATE2:sum',LANGUAGE]:s,
                       STRINGS.loc['IO::MANIPULATE2:mean',LANGUAGE]:0 if c==0 else(s/c),
                       STRINGS.loc['IO::MISC:COUNT',LANGUAGE]:c,
                       STRINGS.loc['IO::MANIPULATE2:min',LANGUAGE]:m,
                       STRINGS.loc['IO::MANIPULATE2:max',LANGUAGE]:M})
    def identify(self):
        spin=self.getspin()
        def verify(io):
            valid=1
            if not bool(io[0]['blast']['reads']):showerror(STRINGS.loc['MISC::ERROR',LANGUAGE],STRINGS.loc['IO::BLAST:ERROR_READS',LANGUAGE]);valid=0
            if not bool(io[0]['blast']['database']):showerror(STRINGS.loc['MISC::ERROR',LANGUAGE],STRINGS.loc['IO::BLAST:ERROR_DATABASE',LANGUAGE]);valid=0
            if(io[0]['dedup3']is not None)and(io[0]['GB2Taxid']is None):showerror(STRINGS.loc['MISC::ERROR',LANGUAGE],STRINGS.loc['IO::LOAD_FIRST',LANGUAGE].format(STRINGS.loc['DB::GB2TAXID',LANGUAGE]));valid=0
            if(io[0]['dedup3']is None)and(bool(io[1]['Taxonomy']['Name'])or(io[1]['Taxonomy']['Lineage']is not None)):showerror(STRINGS.loc['MISC::ERROR',LANGUAGE],'Deduplication stage 2 must be enabled to use Taxonomy');valid=0
            if(bool(io[1]['Taxonomy']['Name'])or(io[1]['Taxonomy']['Lineage']is not None))and(io[0]['Taxdump']is None):showerror(STRINGS.loc['MISC::ERROR',LANGUAGE],'Load new_taxdump.zip first!');valid=0
            return valid
        io=askio('Deduplicate',STRINGS.loc['IO::SELECT:COLUMNS',LANGUAGE],
                 setio(STRINGS.loc['IO::INPUTS',LANGUAGE],{
                      'blast':(Group,[],{'title':STRINGS.loc['IO::BLAST:AUTO',LANGUAGE],'widgets':{
                                 'blast':(DCombo,[],{'text':STRINGS.loc['IO::BLAST:BLAST',LANGUAGE],'values':['blastn'],'default':'blastn'}),
                                 'reads':(OpenFileButton,[],{'defaultextension':FASTA[1],'filetypes':FASTA[2],'text':STRINGS.loc['IO::BLAST:READS',LANGUAGE],'mandatory':True}),
                                 'database':(DCombo,[],{'text':STRINGS.loc['IO::BLAST:DATABASE',LANGUAGE],'values':self.DB['BLAST'].names})
                                            }}),
                      'GB2Taxid':(Group,[],{'type':'check','title':'Accessions \u2192 taxids','widgets':{
                                                                 'GB2Taxid':(Option,[],self.setdb('GB2Taxid')),
                                                                 }}),
                      'dedup3':(Option,[],{'type':'check','title':'Deduplicate taxids','prompt':STRINGS.loc['IO::MISC:AUTO_DETECT',LANGUAGE],'state':'disabled','value':'True'}),
                      'Taxdump':(Option,[],{'type':'check',**self.setdb('Taxdump')}),
                     },validate=None,error='Enable at least one input'),
                 setio(STRINGS.loc['IO::OUTPUTS',LANGUAGE],{'Table':(Constant,[],{'title':STRINGS.loc['IO::OUTPUT:TABLE_TITLE',LANGUAGE],'prompt':STRINGS.loc['IO::OUTPUT:TABLE',LANGUAGE],'state':'disabled'}),
                                        'Taxonomy':(Group,[],{'title':STRINGS.loc['IO::TAXONOMY',LANGUAGE],'widgets':{
                                            'Name':(DBool,[],{'type':'check','prompt':STRINGS.loc['TAXONOMY::SCINAME',LANGUAGE]}),
                                            'Lineage':(RadioGroup,[],{'validate':None,'widgets':{
                                                 'Full':(Option,[],{'type':'radio','default':False,'prompt':STRINGS.loc['TAXONOMY::FULL',LANGUAGE]}),
                                                 'Ranked':(Option,[],{'type':'radio','default':False,'prompt':STRINGS.loc['TAXONOMY::RANKED',LANGUAGE]}),
                                             }}),
                                         }}),
                             },validate=None),
                 verify)
        if self.debug.get():print(io)
        elif io:
            try:
                self.lock()
                self.blast(io=[io[0]['blast'],{'Table': None}],auto=True)
                if self.stopped.get():raise KeyboardInterrupt
                self.dedup2(io=[{'Accessions':1},{'Table':None}],auto=True)
                if self.stopped.get():raise KeyboardInterrupt
                if io[0]['GB2Taxid']:
                    self.table.table.insertcol(1)
                    self.table.table.rename(1,'taxid')
                    self.offlinetaxonomy(io=[{'Taxonomy': ('Accession', {'Accessions': 0, 'GB2Taxid': True}), 'Taxdump': True}, {'txid': 1, 'name':None, 'Taxonomy': None}],auto=True)
                if self.stopped.get():raise KeyboardInterrupt
                self.dedup3(io=[{'txid': 1, 'Count': 2}, {'Table': None}],auto=True)
                if self.stopped.get():raise KeyboardInterrupt
                if io[1]['Taxonomy']['Name']:
                    self.table.table.insertcol(2)
                    self.table.table.rename(2,'Scientific name')
                    n=3;name=2
                    if io[1]['Taxonomy']['Lineage'] is None:
                        self.offlinetaxonomy(io=[{'Taxonomy': ('txid', 0), 'Taxdump': True}, {'txid': None, 'name':name, 'Taxonomy': None}],auto=True)
                else:n=2;name=None
                if self.stopped.get():raise KeyboardInterrupt
                if io[1]['Taxonomy']['Lineage']:
                    if io[1]['Taxonomy']['Lineage'][0]=='Full':
                        self.table.table.insertcol(n)
                        self.table.table.rename(n,'Full lineage')
                        self.offlinetaxonomy(io=[{'Taxonomy': ('txid', 0), 'Taxdump': True}, {'txid': None, 'name':name, 'Taxonomy': ('Full', n)}],auto=True)
                    elif io[1]['Taxonomy']['Lineage'][0]=='Ranked':
                        for i in range(8):
                            self.table.table.insertcol(n+i)
                            self.table.table.rename(n+i,['Domain','Kingdom','Phylum','Class','Order','Family','Genus','Species'][i])
                        self.offlinetaxonomy(io=[{'Taxonomy': ('txid', 0), 'Taxdump': True}, {'txid': None, 'name':name, 'Taxonomy': ('Ranked', slice(n, n+8, None))}],auto=True)
            except KeyboardInterrupt:
                self.print('\nOperation successfully interrupted\n')
            self.unding(auto=False)
    def blast(self,io=None,auto=False):
        spin=self.getspin()
        def verify(io):
            if not bool(io['reads']):showerror(STRINGS.loc['MISC::ERROR',LANGUAGE],STRINGS.loc['IO::BLAST:ERROR_READS',LANGUAGE]);return 0
            elif not bool(io['database']):showerror(STRINGS.loc['MISC::ERROR',LANGUAGE],STRINGS.loc['IO::BLAST:ERROR_DATABASE',LANGUAGE]);return 0
            else:return 1
        if not auto:io=askio(STRINGS.loc['IO::BLAST',LANGUAGE],STRINGS.loc['IO::SELECT:FILES',LANGUAGE],
                     setio(STRINGS.loc['IO::INPUTS',LANGUAGE],{
                         'blast':(DCombo,[],{'text':STRINGS.loc['IO::BLAST:BLAST',LANGUAGE],'values':['blastn'],'default':'blastn'}),
                         'reads':(OpenFileButton,[],{'defaultextension':FASTA[1],'filetypes':FASTA[2],'text':STRINGS.loc['IO::BLAST:READS',LANGUAGE],'mandatory':True}),
                         'database':(DCombo,[],{'text':STRINGS.loc['IO::BLAST:DATABASE',LANGUAGE],'values':self.DB['BLAST'].names})
                      },validate=verify),
                    setio(STRINGS.loc['IO::OUTPUTS',LANGUAGE],{'Table':(Constant,[],{'title':STRINGS.loc['IO::OUTPUT:TABLE_TITLE',LANGUAGE],'prompt':STRINGS.loc['IO::OUTPUT:TABLE',LANGUAGE],'state':'disabled'})},validate=None),validate=None)
        if self.debug.get():print(io)
        elif io:
            self.lpc(auto,f'Running BLAST job...')
            L=ProgressLogger(self.root)
            command = blast_path+' -db %s -query %s -outfmt "6 delim=; qacc sacc evalue pident" -max_target_seqs 1 -max_hsps 1'%(self.DB['BLAST'][io[0]['database']],io[0]['reads'])
            self.print(command)
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            a=0;b=0
            io=StringIO()
            try:
                while True:
                    output = process.stdout.readline()# Read a line from stdout
                    if output:a+=1;io.write(output)
                    if process.poll() is not None: break
                    if self.stopped.get():raise KeyboardInterrupt
                    b+=1
                    L.step(f'Running BLAST job... {a}/{b}',0)
                remaining_output, remaining_error = process.communicate()
                if remaining_output:io.write(remaining_output)
                if remaining_error:self.print(remaining_error)
            except KeyboardInterrupt:
                process.terminate()  # Terminate the process if needed
                self.print(f'Received SIGTERM, terminating')
            L.close()
            self.print(f'Return Code:{process.returncode}')# Check the return code
            io.seek(0)
            self.table.table.load(DataFrame(data = [[i for i in row] for row in csv.reader(io,';')],columns=['read ID','Accessions','E-Value','Per.Ident']).replace(to_replace=None,value='',regex=[None]))
            self.unding(auto)
    def dedup(self,io=None,auto=False):
        spin=self.getspin()
        def verify(io):
            valid=1
            if(io[0]['dedup3']is not None)and(io[0]['GB2Taxid']is None):showerror(STRINGS.loc['MISC::ERROR',LANGUAGE],STRINGS.loc['IO::LOAD_FIRST',LANGUAGE].format(STRINGS.loc['DB::GB2TAXID',LANGUAGE]));valid=0
            if(io[0]['dedup3']is None)and(bool(io[1]['Taxonomy']['Name'])or(io[1]['Taxonomy']['Lineage']is not None)):showerror(STRINGS.loc['MISC::ERROR',LANGUAGE],'Deduplication stage 2 must be enabled to use Taxonomy');valid=0
            if(bool(io[1]['Taxonomy']['Name'])or(io[1]['Taxonomy']['Lineage']is not None))and(io[0]['Taxdump']is None):showerror(STRINGS.loc['MISC::ERROR',LANGUAGE],'Load new_taxdump.zip first!');valid=0
            return valid
        io=askio('Deduplicate',STRINGS.loc['IO::SELECT:COLUMNS',LANGUAGE],
                 setio(STRINGS.loc['IO::INPUTS',LANGUAGE],{'dedup1':(Group,[],{'type':'check','orient':'horizontal','title':'Stage 0: BLAST duplicate alignments','default':False,'widgets':{
                                                  'reads':(DSpin,[],{**spin,**{'text':'Read ID'}}),
                                                  'pident':(DSpin,[],{**spin,**{'text':'Per Ident'}}),
                                                  'evalue':(DSpin,[],{**spin,**{'text':'E-Value'}}),
                                                  }}),
                      'dedup2':(Group,[],{'type':'check','title':'Stage 1: accessions','widgets':{'Accessions':(DSpin,[],{**spin,**{'text':STRINGS.loc['IO::NCBI:ACCESSION',LANGUAGE]}})}}),
                      'GB2Taxid':(Group,[],{'type':'check','title':'Accessions \u2192 taxids','widgets':{
                                                                 'GB2Taxid':(Option,[],self.setdb('GB2Taxid')),
                                                                 }}),
                      'dedup3':(RadioGroup,[],{'title':'Stage 2: taxids','validate':None,'widgets':{
                                                             'dedup3c':(DBool,[],{'type':'radio','default':False,'prompt':STRINGS.loc['IO::MISC:AUTO_DETECT',LANGUAGE]}),
                                                             'dedup3i':(Group,[],{'type':'radio','default':False,'orient':'horizontal','widgets':{
                                                                 'txid':(DSpin,[],{**spin,**{'text':STRINGS.loc['IO::NCBI:TAXID',LANGUAGE]}}),
                                                                 'Count':(DSpin,[],{**spin,**{'text':STRINGS.loc['IO::MISC:COUNT',LANGUAGE]}}),
                                                                 }}),
                                                             }}),
                      'Taxdump':(Option,[],{'type':'check',**self.setdb('Taxdump')}),
                     },validate=any,error='Enable at least one input'),
                 setio(STRINGS.loc['IO::OUTPUTS',LANGUAGE],{'Table':(Constant,[],{'title':STRINGS.loc['IO::OUTPUT:TABLE_TITLE',LANGUAGE],'prompt':STRINGS.loc['IO::OUTPUT:TABLE',LANGUAGE],'state':'disabled'}),
                                        'Taxonomy':(Group,[],{'title':STRINGS.loc['IO::TAXONOMY',LANGUAGE],'widgets':{
                                            'Name':(DBool,[],{'type':'check','prompt':STRINGS.loc['TAXONOMY::SCINAME',LANGUAGE]}),
                                            'Lineage':(RadioGroup,[],{'validate':None,'widgets':{
                                                 'Full':(Option,[],{'type':'radio','default':False,'prompt':STRINGS.loc['TAXONOMY::FULL',LANGUAGE]}),
                                                 'Ranked':(Option,[],{'type':'radio','default':False,'prompt':STRINGS.loc['TAXONOMY::RANKED',LANGUAGE]}),
                                             }}),
                                         }}),
                             },validate=any),
                 verify)
        if self.debug.get():print(io)
        elif io:
            try:
                self.lock()
                if io[0]['dedup1']:self.dedup1(io=[io[0]['dedup1'],{'Table': None}],auto=True)
                if self.stopped.get():raise KeyboardInterrupt
                if io[0]['dedup2']:self.dedup2(io=[io[0]['dedup2'],{'Table': None}],auto=True)
                if self.stopped.get():raise KeyboardInterrupt
                if io[0]['GB2Taxid']:
                    self.table.table.insertcol(1)
                    self.table.table.rename(1,'taxid')
                    self.offlinetaxonomy(io=[{'Taxonomy': ('Accession', {'Accessions': 0, 'GB2Taxid': True}), 'Taxdump': True}, {'txid': 1, 'name':None, 'Taxonomy': None}],auto=True)
                if self.stopped.get():raise KeyboardInterrupt
                if io[0]['dedup3']is not None:
                    if io[0]['dedup3'][0]=='dedup3c':
                        self.dedup3(io=[{'txid': 1, 'Count': 2}, {'Table': None}],auto=True)
                    elif io[0]['dedup3'][0]=='dedup3i':self.dedup3(io=[io[0]['dedup3'][1],{'Table': None}],auto=True)
                if self.stopped.get():raise KeyboardInterrupt
                if io[1]['Taxonomy']['Name']:
                    self.table.table.insertcol(2)
                    self.table.table.rename(2,'Scientific name')
                    n=3;name=2
                    if io[1]['Taxonomy']['Lineage'] is None:
                        self.offlinetaxonomy(io=[{'Taxonomy': ('txid', 0), 'Taxdump': True}, {'txid': None, 'name':name, 'Taxonomy': None}],auto=True)
                else:n=2;name=None
                if self.stopped.get():raise KeyboardInterrupt
                if io[1]['Taxonomy']['Lineage']:
                    if io[1]['Taxonomy']['Lineage'][0]=='Full':
                        self.table.table.insertcol(n)
                        self.table.table.rename(n,'Full lineage')
                        self.offlinetaxonomy(io=[{'Taxonomy': ('txid', 0), 'Taxdump': True}, {'txid': None, 'name':name, 'Taxonomy': ('Full', n)}],auto=True)
                    elif io[1]['Taxonomy']['Lineage'][0]=='Ranked':
                        for i in range(8):
                            self.table.table.insertcol(n+i)
                            self.table.table.rename(n+i,['Domain','Kingdom','Phylum','Class','Order','Family','Genus','Species'][i])
                        self.offlinetaxonomy(io=[{'Taxonomy': ('txid', 0), 'Taxdump': True}, {'txid': None, 'name':name, 'Taxonomy': ('Ranked', slice(n, n+8, None))}],auto=True)
            except KeyboardInterrupt:
                self.print('\nOperation successfully interrupted\n')
            self.unding(auto)
    def dedup1(self,io=None,auto=False):
        spin=self.getspin()
        if not auto:io=askio('Deduplication stage 0',STRINGS.loc['IO::SELECT:COLUMNS',LANGUAGE],
                     setio(STRINGS.loc['IO::INPUTS',LANGUAGE],{'reads':(DSpin,[],{**spin,**{'text':'Read ID'}}),
                      'pident':(DSpin,[],{**spin,**{'text':'Per Ident'}}),
                      'evalue':(DSpin,[],{**spin,**{'text':'E-Value'}}),
                      }),
                    setio(STRINGS.loc['IO::OUTPUTS',LANGUAGE],{'Table':(Constant,[],{'title':STRINGS.loc['IO::OUTPUT:TABLE_TITLE',LANGUAGE],'prompt':STRINGS.loc['IO::OUTPUT:TABLE',LANGUAGE],'state':'disabled'})},validate=None),validate=None)
        if self.debug.get():print(io)
        elif io:
            self.lpc(auto,f'Running deduplication stage 0...')
            reads=self.table[:,io[0]['reads']]
            pident=self.table[:,io[0]['pident']]
            evalue=self.table[:,io[0]['evalue']]
            reads2={}
            second_pident=second_evalue=0
            try:
                for i in range(len(reads)):
                    if self.stopped.get():raise KeyboardInterrupt
                    if reads[i]not in reads2:reads2[reads[i]]=i
                    else:
                        j=reads2[reads[i]]
                        if float(evalue[j])<float(evalue[i]):
                            if float(pident[j])>float(pident[i]):second_pident+=1
                            else:second_evalue+=1
                            reads2[reads[i]]=i
                lst=[reads2[i]for i in reads2]
                new_table=self.table[lst,:].reset_index(drop=True)
                self.table.table.load(new_table,'Dedup stage 0')
            except KeyboardInterrupt:
                self.print('\nOperation successfully interrupted\n')
            self.print(f'Deduplicated {i+1} -> {len(lst)} reads')
            self.unding(auto)
    def dedup2(self,io=None,auto=False):
        if not auto:io=askio('Deduplication stage 1',STRINGS.loc['IO::SELECT:COLUMNS',LANGUAGE],
                     setio(STRINGS.loc['IO::INPUTS',LANGUAGE],{'Accessions':(DSpin,[],{**self.getspin(),**{'text':STRINGS.loc['IO::NCBI:ACCESSION',LANGUAGE]}})}),
                     setio(STRINGS.loc['IO::OUTPUTS',LANGUAGE],{'Table':(Constant,[],{'title':STRINGS.loc['IO::OUTPUT:TABLE_TITLE',LANGUAGE],'prompt':STRINGS.loc['IO::OUTPUT:TABLE',LANGUAGE],'state':'disabled'})},validate=None),validate=None)
        if self.debug.get():print(io)
        elif io:
            self.lpc(auto,f'Running deduplication stage 1...')
            accs=self.table[:,io[0]['Accessions']]
            accs2={}
            try:
                for i in range(len(accs)):
                    if self.stopped.get():raise KeyboardInterrupt
                    if accs[i]not in accs2:accs2[accs[i]]=1
                    else:accs2[accs[i]]+=1
                new_table=DataFrame(data=accs2.items(),columns=['Accession','Count'])
                self.table.table.load(new_table,'Dedup stage 1')
            except KeyboardInterrupt:
                self.print('\nOperation successfully interrupted\n')
            self.print(f'Deduplicated {i+1} reads -> {len(accs2)} unique accessions')
            self.unding(auto)
    def dedup3(self,io=None,auto=False):
        if not auto:io=askio('Deduplication stage 2',STRINGS.loc['IO::SELECT:COLUMNS',LANGUAGE],
                     setio(STRINGS.loc['IO::INPUTS',LANGUAGE],{'txid':(DSpin,[],{**self.getspin(),**{'text':STRINGS.loc['IO::NCBI:TAXID',LANGUAGE]}}),
                      'Count':(DSpin,[],{**self.getspin(),**{'text':STRINGS.loc['IO::MISC:COUNT',LANGUAGE]}})}),
                     setio(STRINGS.loc['IO::OUTPUTS',LANGUAGE],{'Table':(Constant,[],{'title':STRINGS.loc['IO::OUTPUT:TABLE_TITLE',LANGUAGE],'prompt':STRINGS.loc['IO::OUTPUT:TABLE',LANGUAGE],'state':'disabled'})},validate=None),validate=None)
        if self.debug.get():print(io)
        elif io:
            self.lpc(auto,f'Running deduplication stage 2...')
            txids=self.table[:,io[0]['txid']]
            counts=self.table[:,io[0]['Count']]
            txids2={}
            try:
                for i in range(len(txids)):
                    if self.stopped.get():raise KeyboardInterrupt
                    if txids[i]not in txids2:txids2[txids[i]]=counts[i]
                    else:txids2[txids[i]]+=counts[i]
                new_table=DataFrame(data=txids2.items(),columns=['taxid','Count'])
                self.table.table.load(new_table,'Dedup stage 2')
            except KeyboardInterrupt:
                self.print('\nOperation successfully interrupted\n')
            self.print(f'Deduplicated {i+1} -> {len(txids2)} taxids')
            self.unding(auto)
    def offlinesaprobity(self,io=None,auto=False):
        spin=self.getspin()
        def verify(io):return(io['Saprobity']is not None)
        if not auto:io=askio('Get saprobity offline',STRINGS.loc['IO::SELECT:COLUMNS',LANGUAGE],
                     setio(STRINGS.loc['IO::INPUTS',LANGUAGE],{'txid':(DSpin,[],{**spin,**{'text':STRINGS.loc['IO::NCBI:TAXID',LANGUAGE]}}),
                                     'Filter':(DSpin,[],{**spin,**{'type':'check','text':STRINGS.loc['IO::MISC:FILTER',LANGUAGE]}}),
                                     'Saprobity':(Constant,[],self.setdb('Saprobity'))
                                    },validate=verify),
                     setio(STRINGS.loc['IO::OUTPUTS',LANGUAGE],{'index':(DSpin,[],{**spin,**{'type':'check','text':'S'}}),
                                      'zone':(DSpin,[],{**spin,**{'type':'check','text':'Saprobity zone'}}),
                                      }, validate=any),
                    atleastoneoutput)
        if self.debug.get():print(io)
        elif io:
            self.lpc(auto,'Running offline saprobity job...')
            LIST=txids=self.table[:,io[0]['txid']].astype('string')
            untax=[*self.DB['Saprobity'].txids().astype('string')[self.DB['Saprobity'].txids()!='']]
            unsap=[*self.DB['Saprobity'].saprobities()[self.DB['Saprobity'].txids()!='']]
            mask=self.getio(io,'Filter')
            f=d=0
            offset=0
            t=time()
            l=len(LIST)
            if mask is None:mask=[True]*l
            l2=sum([bool(i)for i in mask])-offset
            self.dashboard.config(all=f'{l} ({l2} to do)')
            try:
                for i in range(l):
                    if bool(mask[i]):
                        self.cpr()
                        if self.stopped.get():raise KeyboardInterrupt
                        if LIST[i] in untax:
                            self.table[i,io[1]['index']]=unsap[untax.index(LIST[i])]
                            d+=1
                        else:
                            f+=1
                            self.print(f'{i}/{l}: not found in saprobity database')
                        self.cpr()
                        T=int(time()-t)
                        T2=(int(T*(l-i)/(i)))if i!=0 else 0
                        self.dashboard.config(done=d,fail=f,left=l2-d,elapsed=f'{T//86400}d {(T//3600)%24:02.0f}:{(T//60)%60:02.0f}:{T%60:02.0f}',ETA=f'{T2//86400}d {(T2//3600)%24:02.0f}:{(T2//60)%60:02.0f}:{T2%60:02.0f}')
            except KeyboardInterrupt:
                self.print('\nOperation successfully interrupted\n')
            self.unding(auto)
    def offlinetaxonomy(self,io=None,auto=False):
        spin=self.getspin()
        if not auto:io=askio('Get taxonomy offline',STRINGS.loc['IO::SELECT:COLUMNS',LANGUAGE],
                     setio(STRINGS.loc['IO::INPUTS',LANGUAGE],{'Taxonomy':(RadioGroup,[],{'title':'Search by','widgets':{
                                     'Accession':(Group,[],{'type':'radio','default':False,'title':'Accessions','widgets':{
                                         'Accessions':(DSpin,[],{**spin,**{'text':STRINGS.loc['IO::NCBI:ACCESSION',LANGUAGE]}}),
                                         'GB2Taxid':(Option,[],self.setdb('GB2Taxid')),
                                     },'validate':all}),
                                     'name':(DSpin,[],{**spin,**{'type':'radio','default':False,'text':STRINGS.loc['TAXONOMY::SCINAME',LANGUAGE]}}),
                                     'txid':(DSpin,[],{**spin,**{'type':'radio','default':False,'text':STRINGS.loc['IO::NCBI:TAXID',LANGUAGE]}})
                                     }}),
                                     'Filter':(DSpin,[],{**spin,**{'type':'check','text':STRINGS.loc['IO::MISC:FILTER',LANGUAGE]}}),
                                     'Taxdump':(Constant,[],self.setdb('Taxdump'))
                                    },validate=all),
                     setio(STRINGS.loc['IO::OUTPUTS',LANGUAGE],{'txid':(DSpin,[],{**spin,**{'type':'check','text':STRINGS.loc['IO::NCBI:TAXID',LANGUAGE]}}),
                                      'name':(DSpin,[],{**spin,**{'type':'check','text':STRINGS.loc['TAXONOMY::SCINAME',LANGUAGE]}}),
                                      'Taxonomy':(RadioGroup,[],{'type':'check','title':STRINGS.loc['TAXONOMY::LINEAGE',LANGUAGE],'widgets':{
                                          'Full':(DSpin,[],{**spin,**{'type':'radio','default':False,'text':STRINGS.loc['TAXONOMY::FULL',LANGUAGE]}}),
                                          'Ranked':(TaxSpin2,[],{'type':'radio','default':False,'maxvalue':self.table.table.W-1}),
                                      }})
                                      }, validate=any),
                    atleastoneoutput)
        if self.debug.get():print(io)
        elif io:
            self.lpc(auto,'Running offline taxonomy job...')
            t1=io[0]['Taxonomy']
            if t1[0]=='Accession':mode='g2t';LIST=accs=self.table[:,t1[1]['Accessions']]
            elif t1[0]=='txid':mode='';LIST=txids=self.table[:,t1[1]].astype('string')
            elif t1[0]=='name':mode='n2t';LIST=names=self.table[:,t1[1]]
            mask=self.getio(io,'Filter')
            f=d=0
            offset=0
            t=time()
            l=len(LIST)
            if mask is None:mask=[True]*l
            l2=sum([bool(i)for i in mask])-offset
            self.dashboard.config(all=f'{l} ({l2} to do)')
            try:
                for i in range(l):
                    if bool(mask[i]):
                        F=D=0
                        self.cpr()
                        if self.stopped.get():raise KeyboardInterrupt
                        if mode=='g2t':
                            txid=self.DB['gb2taxid'][accs[i][:2],accs[i],'Update database!']
                            if txid=='Update database!':F=1;self.print(f'{i}/{l}: fail (not found - update database?)')
                            else:D=1;
                        elif mode=='n2t':
                            txid=self.DB['taxdump']['revnames',names[i],'']
                            if txid=='':F=1;self.print(f'{i}/{l}: fail (not found - update database?)')
                            else:D=1
                        else:txid=txids[i]
                        if io[1]['txid']is not None:self.table[i,io[1]['txid']]=txid
                        if io[1]['name']is not None:
                            name=self.DB['taxdump']['names.dmp',txid,'']
                            self.table[i,io[1]['name']]=name
                            if name=='':F=1;D=0;self.print(f'{i}/{l}: fail (not found - update database?)')
                            else:D=1
                        self.cpr()
                        if io[1]['Taxonomy']is not None:
                            if io[1]['Taxonomy'][0]=='Full':tax=self.DB['taxdump']['fullnamelineage.dmp',txid,'']
                            elif io[1]['Taxonomy'][0]=='Ranked':tax=self.DB['taxdump']['rankedlineage.dmp',txid,['']*8]
                            self.table[i,io[1]['Taxonomy'][1]]=tax
                            if tax=='':F=1;D=0;self.print(f'{i}/{l}: fail (invalid taxid)')
                            else:D=1
                        f+=F;d+=D
                        self.cpr()
                        T=int(time()-t)
                        T2=(int(T*(l-i)/(i)))if i!=0 else 0
                        self.dashboard.config(done=d,fail=f,left=l2-d,elapsed=f'{T//86400}d {(T//3600)%24:02.0f}:{(T//60)%60:02.0f}:{T%60:02.0f}',ETA=f'{T2//86400}d {(T2//3600)%24:02.0f}:{(T2//60)%60:02.0f}:{T2%60:02.0f}')
            except KeyboardInterrupt:
                self.print('\nOperation successfully interrupted\n')
            self.unding(auto)
    def onlinetaxonomy(self,io=None,auto=False):
        spin={**self.getspin(),**{'type':'check'}}
        if not auto:io=askio('Get taxonomy online',STRINGS.loc['IO::SELECT:COLUMNS',LANGUAGE],
                     setio(STRINGS.loc['IO::INPUTS',LANGUAGE],{'Taxonomy':(RadioGroup,[],{'title':'Search by','widgets':{
                                                             'Name':(TaxSpin,[],{'type':'radio','default':False,'text':STRINGS.loc['TAXONOMY::SCINAME',LANGUAGE],'maxvalue':self.table.table.W-1}),
                                                             'txid':(DSpin,[],{**spin,**{'type':'radio','default':False,'text':STRINGS.loc['IO::NCBI:TAXID',LANGUAGE]}}),
                                                             }
                                                 }),
                      'Filter':(DSpin,[],{**spin,**{'text':STRINGS.loc['IO::MISC:FILTER',LANGUAGE]}})},validate=any),
                     setio(STRINGS.loc['IO::OUTPUTS',LANGUAGE],{'txid':(DSpin,[],{**spin,**{'text':STRINGS.loc['IO::NCBI:TAXID',LANGUAGE]}}),
                      'Current name':(DSpin,[],{**spin,**{'text':STRINGS.loc['TAXONOMY::SCINAME',LANGUAGE]}}),
                      'Full lineage':(DSpin,[],{**spin,**{'text':STRINGS.loc['TAXONOMY::FULL',LANGUAGE]}}),
                      'Exists':(DSpin,[],{**spin,**{'text':STRINGS.loc['IO::NCBI:EXISTS',LANGUAGE]}})},validate=any),
                     atleastoneoutput)
        if self.debug.get():print(io)
        elif io:
            self.lpc(auto,'Running online taxonomy job...')
            taxnames=self.getio(io,'Taxonomy')
            mask=self.getio(io,'Filter')
            if (io[1]['Current name']is not None) or (io[1]['Full lineage'] is not None):
                self.geneprot(LIST=taxnames, mask=mask, offset=0, pre=self.tpre, main=self.skip, main2=self.tmain, post=self.skip,
                              base='taxonomy', fetch=True, mode='rb',
                              eskw={'retmax':3},efkw={},sn=io[1]['Current name'],fl=io[1]['Full lineage'],ex=io[1]['Exists'],tx=io[1]['txid'])
            else:
                self.geneprot(LIST=taxnames, mask=mask, offset=0, pre=self.tpre, main=self.tmain2, main2=self.skip, post=self.skip,
                              base='taxonomy', fetch=False, mode='rb',
                              eskw={'retmax':3},efkw={},ex=io[1]['Exists'],tx=io[1]['txid'])
            self.unding(auto)
    def tpre(self,*,LIST=None,FAILS=None,i=None,l=None,f=None,d=None,**kw):
        if FAILS and kw['ex']:self.table[i-1,kw['ex']]=0;FAILS.clear()
    def tmain(self,curr,*,LIST=None,FAILS=None,i=None,l=None,f=None,d=None,**kw):
        if kw['sn']is not None:self.table[i,kw['sn']]=curr[0]['ScientificName']
        if kw['fl']is not None:self.table[i,kw['fl']]=curr[0]['Lineage']
        if kw['tx']is not None:self.table[i,kw['tx']]=curr[0]['TaxId']
        if kw['ex']is not None:self.table[i,kw['ex']]=1
        self.print(f'{i}/{l}: success')
    def tmain2(self,curr,*,LIST=None,FAILS=None,i=None,l=None,f=None,d=None,**kw):
        if kw['ex']is not None:self.table[i,kw['ex']]=int(bool(curr["IdList"]))
        if kw['tx']is not None:self.table[i,kw['tx']]=(curr["IdList"][0]if curr["IdList"]else'')
        self.print(f'{i}/{l}: success')
##    def rename(self,io=None,auto=False): #Unused and outdated. Rewrite!
##        if not auto:io=askio('Rename FASTA for phylogeny',STRINGS.loc['IO::SELECT:COLUMNS',LANGUAGE],
##                     {'Taxonomy':(TaxSpin,[],{'maxvalue':self.table.table.W-1}),
##                      'Accession':(DSpin,[],{**self.getspin(),**{'text':STRINGS.loc['IO::NCBI:ACCESSION',LANGUAGE]}}),
##                      'Saprobity':(DSpin,[],{**self.getspin(),**{'text':'Saprobity'}}),
##                      },
##                     {'FASTA':(Constant,[],{'title':STRINGS.loc['IO::OUTPUT:FASTA_TITLE',LANGUAGE],'prompt':STRINGS.loc['IO::OUTPUT:TEXT',LANGUAGE],'state':'disabled'})})        
##        if self.debug.get():print(io)
##        elif io:
##            taxnames=self.getio(io,'Taxonomy')
##            saprobcsv = dict(zip(self.table[:,io[0]['Accession']],zip(taxnames,self.table[:,io[0]['Saprobity']])))
##            fasta2=[i for i in self.fasta.text.get(1.0,'end').split('>')if i not in['','\n',' ']]
##            fasta3=[]
##            i=f=0
##            for S in fasta2:
##                G=[i for i in S.splitlines()if i]
##                h=G[0].split()
##                if h[0] in saprobcsv:                    
##                    fasta3.append('>%s %s %s\n%s'%(saprobcsv[h[0]][1],saprobcsv[h[0]][0],h[0],''.join(G[1:])))
##                    i+=1
##                else:
##                    fasta3.append('>'+S)
##                    f+=1
##                    self.print('%s not found in table'%h[0])
##                self.text.see('end')
##            self.print('Renamed %s entries, failed %s entries'%(i,f))
##            self.fasta.text.delete(0.0,'end')
##            self.fasta.text.insert(0.0,'\n'.join(fasta3))
##            self.ding(auto)
    def cpr(self):
        self.update();self.update_idletasks()
        self.table.update();self.table.update_idletasks()
        self.text.update();self.text.update_idletasks()
    def fmain(self,curr,*,LIST=None,FAILS=None,i=None,l=None,f=None,d=None,**kw):
        if kw['cn']is not None:self.table[i,kw['cn']]=curr["Count"]
        if kw['ex']is not None:self.table[i,kw['ex']]=int(bool(curr["Count"]))
        self.print(f'{i}/{l}: success')            
    def main(self,curr,*,LIST=None,FAILS=None,i=None,l=None,f=None,d=None,**kw):
        self.fasta.text.insert('end',curr)
        self.print(f'{i}/{l}: success')
    def offlinedownload(self,io=None,auto=False):
        if not auto:io=askio('Get sequences offline',STRINGS.loc['IO::SELECT:COLUMNS',LANGUAGE],
                            setio(STRINGS.loc['IO::INPUTS',LANGUAGE],{'Accession':(DSpin,[],{'text':STRINGS.loc['IO::NCBI:ACCESSION',LANGUAGE],'width':4,'cnf':{'from':0,'to':self.table.table.W-1}}),
                                  'Filter':(DSpin,[],{'type':'check','text':STRINGS.loc['IO::MISC:FILTER',LANGUAGE],'width':4,'cnf':{'from':0,'to':self.table.table.W-1}}),
                                  'FASTA':(DCombo,[],{'text':STRINGS.loc['IO::DOWNLOAD:REFERENCE',LANGUAGE],'values':self.DB['FDB'].names})},validate=all),
                            setio(STRINGS.loc['IO::OUTPUTS',LANGUAGE],{'FASTA':(Constant,[],{'title':STRINGS.loc['IO::OUTPUT:FASTA_TITLE',LANGUAGE],'prompt':STRINGS.loc['IO::OUTPUT:TEXT',LANGUAGE],'state':'disabled'})},validate=None),validate=None)      
        if self.debug.get():print(io)
        elif io:
            self.lpc(auto,'Running offline fetch sequence job...')
            LIST=self.table[:,io[0]['Accession']]
            mask=self.getio(io,'Filter')
            f=d=0;offset=0;t=time()
            l=len(LIST)
            if mask is None:mask=[True]*l
            l2=sum([bool(i)for i in mask])-offset
            self.dashboard.config(all=f'{l} ({l2} to do)')
            fas=io[0]['FASTA'];zindex=self.DB['FDB'].zindex[fas]
            try:
                for i in range(l):
                    if mask[i]:
                        try:
                            self.fasta.text.insert('end',self.DB['FDB'][fas,LIST[i]]);d+=1
                        except KeyError:
                            f+=1;self.print(f'{i}/{l}: fail (not found in reference)')
                        self.cpr()
                        T=int(time()-t)
                        T2=(int(T*(l-i)/(i)))if i!=0 else 0
                        self.dashboard.config(done=d,fail=f,left=l2-d,elapsed=f'{T//86400}d {(T//3600)%24:02.0f}:{(T//60)%60:02.0f}:{T%60:02.0f}',ETA=f'{T2//86400}d {(T2//3600)%24:02.0f}:{(T2//60)%60:02.0f}:{T2%60:02.0f}')
            except KeyboardInterrupt:
                self.print('\nOperation successfully interrupted\n')
            self.unding(auto)
    def onlinedownload(self,io=None,auto=False):
        def verify2(io):
            return 0 if io['ibase']=='' else 1
        def verify(io):
            if io[0]['ibase']=='':return 0
            if (io[0]['IN'][0]=='Taxonomy' and io[1]['OUT'][0]=='Search') or \
               (io[0]['IN'][0]=='Accession' and io[1]['OUT'][0]=='FASTA'):return 1
            else:showerror(STRINGS.loc['MISC::ERROR',LANGUAGE]);return 0
        if not auto:io=askio('Get taxonomy online',STRINGS.loc['IO::SELECT:COLUMNS',LANGUAGE],
                     setio(STRINGS.loc['IO::INPUTS',LANGUAGE],{'ibase':(DCombo,[],{'text':STRINGS.loc['IO::NCBI:DATABASE',LANGUAGE],'width':7,'values':['GenBank','GenPept']}),
                      'IN':(RadioGroup,[],{'widgets':{'Taxonomy':(TaxSpin,[],{'type':'radio','default':False,'maxvalue':self.table.table.W-1}),
                                                      'Accession':(DSpin,[],{'type':'radio','default':False,'text':STRINGS.loc['IO::NCBI:ACCESSION',LANGUAGE],'width':4,'cnf':{'from':0,'to':self.table.table.W-1}})
                                           }}),
                      'Filter':(DSpin,[],{'type':'check','text':STRINGS.loc['IO::MISC:FILTER',LANGUAGE],'width':4,'cnf':{'from':0,'to':self.table.table.W-1}})
                                     },validate=verify2),
                     setio(STRINGS.loc['IO::OUTPUTS',LANGUAGE],{'OUT':(RadioGroup,[],{'widgets':{'Search':(Group,[],{'title':'Search entries','type':'radio','default':False,'validate':any,'widgets':{
                                                                          'Exists':(DSpin,[],{**self.getspin(),**{'text':STRINGS.loc['IO::NCBI:EXISTS',LANGUAGE]}}),
                                                                          'Count':(DSpin,[],{**self.getspin(),**{'type':'check','text':STRINGS.loc['IO::MISC:COUNT',LANGUAGE]}})
                                                                        }}),
                                                                      'FASTA':(Option,[],{'type':'radio','default':False,'title':STRINGS.loc['IO::OUTPUT:FASTA_TITLE',LANGUAGE],'prompt':STRINGS.loc['IO::OUTPUT:TEXT',LANGUAGE],'state':'disabled'})
                                                            }}),
                                       },validate=any),verify)
        if self.debug.get():print(io)
        elif io:
            self.lpc(auto,f'Running online {io[0]["ibase"]}',end=' ')
            mask=self.getio(io,'Filter')
            if io[1]['OUT'][0]=='FASTA':
                self.print(f'fetch sequence job...')
                self.cpr()
                self.geneprot(LIST=self.table[:,io[0]['IN'][1]], mask=mask, offset=0, fetch=True, mode='r', pre=self.skip, main=self.skip, main2=self.main, post=self.skip,
                          base={'GenBank':'nuccore','GenPept':'protein'}[io[0]['ibase']],eskw={'retmax':3},efkw={'rettype':'fasta','retmode':'text'})
            elif io[1]['OUT'][0]=='Search':
                self.print(f'search job...')
                self.cpr()
                taxnames=self.getio([{'Taxonomy':io[0]['IN'][1]}],'Taxonomy')
                self.geneprot(LIST=taxnames, mask=mask, offset=0, fetch=False, mode='rb', pre=self.skip, main=self.fmain, main2=self.skip, post=self.skip,
                              base={'GenBank':'nuccore','GenPept':'protein'}[io[0]['ibase']], eskw={'retmax':3},efkw={},cn=io[1]['OUT'][1]['Count'],ex=io[1]['OUT'][1]['Exists'])
            self.unding(auto)
class FastaWrapper(WrapperStub):
    format=FASTA
    DB=DB
    def body(self,**kw):
        self.text=ResizableOmniText(self.container,scrolling=(0,1),minwidth=400,minheight=200,minfont=1,maxfont=18,**kw)
        self.google=Search(self.top,STRINGS.loc['FASTA::SEARCH',LANGUAGE],
                           {STRINGS.loc['FASTA::SEARCH:HEADERS',LANGUAGE]:'Headers',
                            STRINGS.loc['FASTA::SEARCH:SEQUENCES',LANGUAGE]:'Sequences',
                            STRINGS.loc['FASTA::SEARCH:ANY',LANGUAGE]:'Any'},'Headers',self.query)
        self.google.grid(row=0,column=2,sticky='nsew')
        self.searchpos=1.0
        return self.text
    def query(self):
        text=self.google.get()
        pos = self.text.search(text, self.searchpos, stopindex='end')
        self.text.focus_set()
        if pos:
            row, col = pos.split('.')
            end='%s.%s'%(row,int(col)+len(text))
            header=(self.text.get(f'{row}.0',f'{row}.1')=='>')
            try:
                if self.google.mode.get()=='Headers'and not header:self.searchpos = end;self.query()
                elif self.google.mode.get()=='Sequences'and header:self.searchpos = end;self.query()
                else:
                    self.text.tag_remove('sel',1.0,'end')
                    self.text.see(pos)
                    self.text.tag_add('sel', pos, end)
                    self.searchpos = end
            except RecursionError:
                self.text.tag_remove('sel',1.0,'end')
                self.bell()
        elif self.searchpos == 1.0:self.bell()
        else:
            self.searchpos = 1.0
            self.query()
    def load(self,file):
        with open(file)as f:
            self.text.delete(1.0,'end')
            self.text.insert(1.0,f.read())
            self.text.frame.config(text=file)
    def save(self,file):
        with open(file,'w')as f:f.write(self.send())
        if file in self.DB['FDB'].names:
            self.DB['FDB'].reload(file)
    def receive(self,payload):
        if payload is not None:
            self.text.delete(1.0,'end')
            self.text.insert(1.0,payload)
    def send(self):return self.text.get(1.0,'end')
class FastaTableWrapper(FastaWrapper):
    format=FASTA
    def body(self,**kw):
        self.frame=Frame(self.container)
        
        mode=LabelFrame(self.top,text='FASTA view')
        mode.grid(row=0,column=2)
        self.mode=BooleanVar(self,value=False)
        ToggleRadioButton(mode,False,self.mode,text='Text').grid(row=0,column=0,padx=10,sticky='we')
        ToggleRadioButton(mode,True,self.mode,text='Visual').grid(row=1,column=0,padx=10,sticky='we')
        self.mode.trace_add('write',self.switch)

        self.table=FastaTable(self.frame,array=DataFrame(data=[],index=['>']))
        self.visual=Frame(self.top)
        mode2=LabelFrame(self.top,text='Sequence type',)
        mode2.grid(row=0,column=3)
        ToggleRadioButton(mode2,False,self.table.protein,text='Nucleotide').grid(row=0,column=0,padx=10,sticky='we')
        ToggleRadioButton(mode2,True,self.table.protein,text='Protein').grid(row=1,column=0,padx=10,sticky='we')
        
        trim=LabelFrame(self.visual,text='Trim')
        self.svar=IntVar(self,value=0)
        self.start=OmniSpin(trim,text='From',width=4,cnf={'from':0,'to':10000},textvariable=self.svar)
        self.start.grid(row=0,column=0)
        self.svar.trace_add('write',self.verify)
        self.evar=IntVar(self,value=0)
        self.end=OmniSpin(trim,text='To',width=4,cnf={'from':0,'to':10000},textvariable=self.evar)
        self.end.grid(row=0,column=1)
        self.evar.trace_add('write',self.verify)
        self.trimmer=Button(trim,text='Remove',command=self.trim)
        self.trimmer.grid(row=1,column=0,columnspan=2)
        trim.grid(row=0,column=0)
        
        if'font'not in kw:kw['font']=('Courier New',7)
        self.text=ResizableOmniText(self.frame,scrolling=(0,1),minwidth=400,minheight=200,minfont=1,maxfont=18,**kw)
        self.google=Search(self.top,'Search in FASTA',{'Headers':'Headers','Sequences':'Sequences','Any':'Any'},'Headers',self.query)        
        self.google.grid(row=0,column=4)
        self.searchpos=1.0
        self.text.pack(fill='both',expand=True)
        
        self.text.bind('<Key>',self.syncttv)
        self.table.bind('<<editvalues>>',self.syncvtt)
        return self.frame
    def syncvtt(self,event=None):
        self.text.delete(1.0,'end')
        self.text.insert(1.0,'\n'.join([i+'\n'+''.join(self.table.array.loc[i])for i in [*self.table.array.index]]))
        #self.text.frame.config(text=self.table['text'])
    def syncttv(self,event=None):
        if not((event is not None) and \
               (event.char in {'\x01':'Select all','\x18':'Cut','\x03':'Copy','\x16':'Paste',
                               '\x1b':'Escape','\x1a':'Undo','\x19':'Redo'} or \
               event.keysym in ['Up','Down','Left','Right','Prior','Next','End','Home',
                                'F1','F2','F3','F4','F5','F6','F7','F8','F9','F10','F11','F12',
                                'F13','F14','F15','F16','F17','F18','F19','F20','F21','F22','F23','F24',
                                'XF86AudioLowerVolume','XF86AudioRaiseVolume','XF86AudioMute', 'XF86AudioNext','XF86AudioPlay','XF86AudioPrev','XF86AudioStop',
                                'Control_L','Control_R','Shift_L','Shift_R','Alt_L','Alt_R','Win_L','Win_R','App','Meta_L','Meta_R',
                                'Num_Lock','Caps_Lock','Scroll_Lock','Pause','Insert']) \
               ):
            #global events;print(event);events.append(event)
            text=self.send()
            if not set(text).issubset({' ','\n'}):
                try:self.table.load(DataFrame([['>'+i[0],*list(''.join(i[1:]))]for i in [[j for j in i.splitlines()if j]for i in text.split('>') if i]]).set_index(0).fillna(""),None)
                except IndexError:
                    try:self.table.load(DataFrame([['>'+i[0],[]]for i in [[j for j in i.splitlines()if j]for i in text.split('>') if i]]).set_index(0).fillna(""),None)
                    except IndexError:self.table.load(DataFrame([['>',[]]for i in [[j for j in i.splitlines()if j]for i in text.split('>') if i]]).set_index(0).fillna(""),None)
                except Exception as E:showerror('Error!',str(type(E))+':'+str(E))
    def switch(self,*a):
        if self.mode.get():
            self.syncttv()
            self.google.grid_forget()
            self.text.pack_forget()
            self.table.pack(fill='both',expand=True)
            self.visual.grid(row=0,column=4)
        else:
            self.syncvtt()
            self.visual.grid_forget()
            self.table.pack_forget()
            self.text.pack(fill='both',expand=True)
            self.google.grid(row=0,column=4)
    def verify(self,*a):
        if self.start.get()>self.end.get():self.trimmer.config(state='disabled')
        else:self.trimmer.config(state='normal')
    def trim(self):self.table.deletecols(self.start.get(),self.end.get())
    def load(self,file):
        with open(file)as f:
            f={'>'+i[0]:''.join(i[1:])for i in [[j for j in i.splitlines()if j]for i in f.read().split('>') if i]}
        self.table.load(DataFrame([[i,*f[i]]for i in f]).set_index(0).fillna(""),file)
        self.syncvtt()  
    def receive(self,payload):
        if payload is not None:
            self.text.delete(1.0,'end')
            self.text.insert(1.0,payload)
            self.syncttv()
class FastaViewer:
    def __init__(self,name,string,fclass):
        self.name=name
        self.string=string
        self.counter=1
        self.fclass=fclass
    def receive(self,payload):
        root=Tk()
        root.title(self.string%self.counter)
        a=self.fclass(root,self.string%self.counter,width=800,height=400)#,font=('Courier New',7))
        a.receive(payload)
        a.pack(fill='both',expand=True)
        if self.radio:self.radio.instance(a)
        self.counter+=1
class FastCons(FastaTableWrapper):
    def body(self,**kw):
        a=FastaTableWrapper.body(self,**kw)
        
        Button(self.ls,text='Merge FASTA',command=self.opens).grid(row=2,column=0,padx=10,sticky='we')
            
        batch=LabelFrame(self.top,text='Split')
        batch.grid(row=0,column=5)
        self.consgroup=Entry(batch)
        self.consgroup.grid(row=0,column=0,columnspan=2,sticky='nsew')
        Button(batch,text='Preview',command=self.preview).grid(row=1,column=0,sticky='nsew')
        Button(batch,text='Save',command=self.split).grid(row=1,column=1,sticky='nsew')
        Button(batch,text='Consensus',command=self.consensus).grid(row=2,column=0,columnspan=2,sticky='nsew')
        
        cons=LabelFrame(self.top,text='Consensus')
        
        self.c0=BooleanVar(self,True)
        self.c1=BooleanVar(self,True)
        self.c2=BooleanVar(self,True)
        self.c3=BooleanVar(self,True)
        Checkbutton(cons,text='100%',variable=self.c0,height=1).grid(row=0,column=0,sticky='nsew')
        c1=Checkbutton(cons,text='',variable=self.c1,height=1)
        c1.grid(row=0,column=1,sticky='nsew')
        self.num=OmniSpin(cons,width=2,cnf={'from':51,'to':99})
        self.num.delete(0,'end')
        self.num.insert(0,90)
        self.num.grid(row=0,column=2,sticky='nsew')
        Checkbutton(cons,text='50%',variable=self.c2,height=1).grid(row=0,column=3,sticky='nsew')
        self.zero=Checkbutton(cons,text='IUPAC',variable=self.c3,height=1)
        self.zero.grid(row=1,column=0,columnspan=2,sticky='nsew')
        self.table.protein.trace_add('write',lambda*a:self.zero.config(text=('PID (JalView)'if self.table.protein.get()else'IUPAC')))
        self.ignore=BooleanVar(self,False)
        Checkbutton(cons,text='Ignore gaps?',variable=self.ignore,height=1).grid(row=1,column=2,columnspan=2,sticky='nsew')
        Button(cons,text='Calculate',command=self.consensusall).grid(row=2,column=0,columnspan=6,sticky='nsew')
        cons.grid(row=0,column=6)
        return a
    def precons(self):
        percons='% Consensus'
        array=self.table.array.T[[j for j in self.table.array.T if not(percons in j)]].T
        self.table.load(array);self.syncvtt()
    def consensusall(self,array=None,title='All'):
        protein=self.table.protein.get()
        unknown='X'if protein else'N'
        if array is None:self.precons();array=self.table.array
        if self.c0.get():self.text.insert('end',consensusNum(array,self.ignore.get(),100,title,unknown))
        if self.c1.get():self.text.insert('end',consensusNum(array,self.ignore.get(),self.num.get(),title,unknown))
        if self.c2.get():self.text.insert('end',consensusNum(array,self.ignore.get(),50,title,unknown))
        if self.c3.get():self.text.insert('end',(consensusNum(array,True,0,title,unknown)if self.table.protein.get()else consensusIUPAC(array,self.ignore.get(),title)))
        self.syncttv()
    def zones(self):
        if (f:=self.consgroup.get()):
            return {zone:z for zone in [i for i in f.split(';')if i]if not(z:=self.table.array.T[[j for j in self.table.array.T if j.startswith('>%s'%zone)]].T).empty}
        else: print('nozons');return []
    def zonestruct(self):
        z=self.zones()
        return{i:{str(j):''.join(z[i].loc[j])for j in z[i].T}for i in z}
    def preview(self):
        if (f:=self.consgroup.get()):
            for i in(z:=self.zonestruct()):showfasta(z[i],i)
        else:showinfo('Nothing to preview','No zones selected.\nOnly global consensus will be calculated')
    def split(self):
        if (f:=self.consgroup.get()):
            if cd:=askdirectory():
                for i in(z:=self.zonestruct()):
                    with open('%s%s%s.fas'%(cd,ossep,i),'w')as f:
                        f.write('\n'.join('\n'.join(j)for j in z[i].items()))
        else:showerror('Nothing to split','No zones specified.')
    def consensus(self):
        self.precons()
        s=''
        for i in(z:=self.zones()):
            print(i)
            self.consensusall(z[i],i)
        self.syncttv()
    def opens(self):
        if (files:=askopenfilenames(defaultextension=FASTA[-2],filetypes=FASTA[-1])):
            file='[Unknown Error]'
            try:
                self.text.delete(1.0,'end')
                self.text.frame.config(text=None)
                for file in reversed(files):
                    print(file)
                    with open(file)as f:
                        self.text.insert('end',f.read())
            except:showerror('Fail!','Cannot load %s file!'%file)
def consensusNum(array,ignore=False,num=50,title='',unknown='N'):
    constr=''
    for x in range(len(array.T)):
        col=[i.upper()for i in sorted(list(array.iloc[:,x]))]
        if len(set(col))==1:constr+=col[0]
        else:
            total=sum(col.count(i)for i in set(col))
            sw={i:col.count(i)for i in set(col)}
            if '-' in sw and ignore:
                del sw['-']
                total-=col.count('-')
            m=max(sw,key=lambda i:sw[i])
            if sw[m]>=total*num/100:constr+=m
            else:constr+=('?'if(('-'in set(col))and not ignore)else unknown)
    if num==0:num='Jalview PID'
    return '\n>%s%% Consensus %s\n%s'%(num,title,constr)
def consensusIUPAC(array,ignore=False,title=''):
    constr=''
    for x in range(len(array.T)):
        col=[i.upper()for i in sorted(list(array.iloc[:,x]))]
        sub={'W':'AT','S':'CG','R':'AG','Y':'CT','K':'GT','M':'AC','B':'CGT','D':'AGT','H':'ACT','V':'ACG','N':'ACGT'}
        nuc={**{'':'-','-':'-','A':'A','T':'T','C':'C','G':'G'},**{sub[i]:i for i in sub}}
        s=''.join(sorted(set(col)))
        for i in(sub2:={**sub,**{'U':'T'},**({'-':'','?':''}if ignore else{})}):s=s.replace(i,sub2[i])
        #print(''.join(sorted(set(s))))
        constr+=nuc.get(''.join(sorted(set(s))),'?')
    return '\n>IUPAC%% Consensus %s\n%s'%(title,constr)    
class Bulker(Downloader,WrapperStub):
    format='Accession list','*',(('All files','*'),)
    def body(self,**kw):
        d=LabelFrame(self.top,text='Directory')
        sel=Button(d,text='Select',command=self.chdir);sel.grid(row=0,column=0,sticky='nsew')
        Button(d,text='Merge',command=self.merge,state='disabled').grid(row=2,column=0,sticky='nsew')
        self.cd=EntryLabel(d,relief='ridge',width=20)
        self.cd.grid(row=1,column=0,sticky='nsew')
        d.grid(row=0,column=1,rowspan=2,sticky='nsew')
        
        self.dashboard=Dashboard(self.top,orient='vertical')
        self.dashboard.grid(row=0,column=2,rowspan=2)
        self.LIST=[]
        
        self.base=StringVar(self,value='GenBank')
        gp=LabelFrame(self.top,text='Select database:');gp.grid(row=0,column=5,columnspan=2,sticky='nsew')
        base1=ToggleRadioButton(gp,value='GenBank',variable=self.base,text='GenBank');base1.pack(side='left',fill='both',expand=True)
        base2=ToggleRadioButton(gp,value='GenPept',variable=self.base,text='GenPept');base2.pack(side='left',fill='both',expand=True)
        down=Button(self.top,text='Download FASTA',command=self.download);down.grid(row=1,column=5)
        self.stopped=ToggleButton(self.top,text=STRINGS.loc['MID::ESTOP',LANGUAGE],border=4,bg='red',value=False)
        self.stopped.grid(row=1,column=6)
        self.stopped.trace_add('write',self.stop)

        chunk=LabelFrame(self.top,text='Chunks')
        self.chunkoff=OmniSpin(chunk,text='Offset',cnf={'from':0,'to':100000})
        self.chunkoff.grid(row=0)
        self.chunksize=OmniSpin(chunk,text='Size (10^n)',cnf={'from':0,'to':6})
        self.chunksize.grid(row=1)
        chunk.grid(row=0,column=8,rowspan=2)
        
        self.text=ResizableOmniText(self,text='Log',scrolling=(0,1),minwidth=400,minheight=200,font=('Courier New',7),width=800)#,**kw)
        self.container.add(self.text)
        self.controls=[sel,self.cd,base1,base2,down,self.chunkoff,self.chunksize]
        return self.text
    def chdir(self):
        if cd:=askdirectory():self.cd.set(cd)
    def merge(self):NotImplemented
    def load(self,file):
        try:
            with open(file)as f:self.LIST=f.read().splitlines()
        except UnicodeDecodeError:
            with open(file,encoding='ansi')as f:self.LIST=f.read().splitlines()
        self.dashboard.config(all=len(self.LIST))
    def save(self,file):
        with open(file,'w')as f:f.write('\n'.join(FAILS))
    def cpr(self):
        self.text.update();self.text.update_idletasks()
        self.dashboard.update();self.dashboard.update_idletasks()
    def pre(self,*,LIST=None,FAILS=None,i=None,l=None,f=None,d=None,**kw):
        if (not i%(10**int(self.chunksize.get())))and self.fasta:
            self.print(f'milestone {i}/{l}: saving chunk {int(i//10**int(self.chunksize.get()))} ({len(self.fasta)} sequences)')
            with open('%s%schunk%s.fas'%(self.cd.get(),ossep,int(i//10**int(self.chunksize.get()))),'w')as file:
                file.write('\n'.join(self.fasta))
                self.fasta.clear()
    def main(self,curr,*,LIST=None,FAILS=None,i=None,l=None,f=None,d=None,**kw):
        self.fasta.append(curr)
    def post(self,*,LIST=None,FAILS=None,i=None,l=None,f=None,d=None,**kw):
        if self.fasta:
            self.print(f'milestone {i}/{l}: saving chunk {int(i//10**int(self.chunksize.get()))+1} ({len(self.fasta)} sequences)')
            with open('%s%schunk%s.fas'%(self.cd.get(),ossep,int(i//10**int(self.chunksize.get()))+1),'w')as file:
                file.write('\n'.join(self.fasta))
                self.fasta.clear()
        if FAILS:self.print('PLEASE DO NOT FORGET TO SAVE ACCESSION LIST OF FAILS')
    def download(self):
        self.fasta=[]
        self.print(f'Chunk size: 10^{int(self.chunksize.get())} -> {10**int(self.chunksize.get())} sequences\nChunk offset: {int(self.chunkoff.get())} -> Start from sequence {int(self.chunkoff.get())*10**int(self.chunksize.get())}')
        self.geneprot(LIST=self.LIST, mask=None, offset=int(self.chunkoff.get())*10**int(self.chunksize.get()), fetch=True, mode='r',
                      pre=self.pre, main=self.skip,main2=self.main, post=self.post, base={'GenBank':'nuccore','GenPept':'protein'}[self.base.get()],
                      eskw={'retmax':3},efkw={'rettype':'fasta','retmode':'text'})
class ClusterFAC(LabelFrame):
    DB=DB
    def __init__(self,master,tree,fastaviewer,**kw):
        LabelFrame.__init__(self,master=master,text='ClusterFAC',**kw)
        self.tree=tree
        self.fastav=fastaviewer
        self.tree.bind('<<loadvalues>>',self.updtree)
        window=PanedWindow(self,orient='vertical')
        window.pack(fill='both',expand=True)
        self.debug=BooleanVar(self,value=False)
        self.lists=ScrolledList(window,text='Clusters')
        self.lists.on_select=self.switch;self.lists.on_double=self.add;self.lists.on_delete=self.deletecl
        self.lists.append('Cluster 1')
        self.lists.append('Add...')
        window.add(self.lists.frame)
        self.cs=Button(self,text='Confirm split FASTA for consensus',command=self.offlinedownload)
        window.add(self.cs)
        window2=PanedWindow(window,orient='horizontal')
        window.add(window2)
        
        self.defaultlist=ScrolledList(window2,text='Tree')
        self.defaultlist.on_select=self.skip;self.defaultlist.on_double=self.skip;self.defaultlist.on_delete=self.skip;#self.defaultlist.make_menu=
        window2.add(self.defaultlist.frame)
        
        self.bf=bf=Frame(window2)
        prefix='R0lGODlhEAAQAHAAACwAAAAAEAAQAIH///8AAAAAAAAAAAAC'
        self.images=[None,PhotoImage(data=prefix[:-18]+'EAAAD///8AAAAAAAACKkSOYXmw6ZiKkCJnZ8aWP7+AjQga5YmmnsaxlOhe7bhh1UMz2SjhlxQoAAA7'),None,
                     PhotoImage(data=prefix+'IIRvgcuhDN2DSE4K7NRcpt5l4EiWoGhiqKOuLfqKcQYVADs='),None,
                     PhotoImage(data=prefix+'IoQPgbuhzNyDR05qb8zcpQ6G4qiQkmFOGYVYbOu9lfbSRgEAOw=='),None,
                     PhotoImage(data=prefix+'KoQPgacbjZ6TkZpnE2YY9vaBnzaG5omiZLdurchecVtlswzhi7ZnzJ4oAAA7'),None]
        self.commands=[None,self.allright,None,self.right,None,self.left,None,self.allleft,None]
        for i in range(len(self.images)):(Button if i%2 else Label)(bf,height=16 if i%2 else 2,image=self.images[i],command=self.commands[i]).grid(row=i,column=0,sticky='ns')
        window2.add(bf)
        
        self.currentlist=ScrolledList(window2,text='Cluster 1')
        self.currentlist.on_select=self.skip;self.currentlist.on_double=self.skip;self.currentlist.on_delete=self.left
        window2.add(self.currentlist.frame)
        
        self.flat=[]
        self.default=[]
        self.clusters=[[]]
        self.pointer=0
    def lock(self):
        self.lists.config(state='disabled')
        self.defaultlist.config(state='disabled')
        self.currentlist.config(state='disabled')
        self.cs.config(state='disabled')
        for i in self.bf.winfo_children():i.config(state='disabled')
    def unlock(self):
        self.lists.config(state='normal')
        self.defaultlist.config(state='normal')
        self.currentlist.config(state='normal')
        self.cs.config(state='normal')
        for i in self.bf.winfo_children():i.config(state='normal')
    def updtree(self,event):self.tree.tree.trace_add('write',self.updlist)
    def switch(self,index):
        if self.lists.get(index)!='Add...':
            self.pointer=index
            self.currentlist.clear()
            self.currentlist.config(text=self.lists.get(index))
            for i in self.clusters[index]:
                self.currentlist.append(i[1])
    def add(self,index):
        if self.lists.get(index)=='Add...':
            self.clusters.append([])
            self.lists.insert(index,f'Cluster {index+1}')
    def deletecl(self,index):
        self.lists.delete(index)
        del self.clusters[index]
    def skip(self,*a):None
    def allright(self,*a):
        for i in range(len(self.default)):self.right(i)
    def allleft(self,*a):
        for i in range(len(self.default)):self.left(0)
    def right(self,index=None):
        if index is None:index=self.defaultlist.index("active")
        cluster=self.clusters[self.pointer]
        data=self.default[index]
        if data not in cluster:cluster.append(data)
        cluster.sort(key=lambda a:a[0])
        self.currentlist.insert(cluster.index(data),data[1])
    def left(self,index=None):
        if index is None:index=self.currentlist.index("active")
        del self.clusters[self.pointer][index]
        self.currentlist.delete(index)
    def updlist(self,*a):
        self.defaultlist.clear()
        self.default.clear()
        for i in range(len(self.tree.tree.flat)):
            if self.tree.tree.state[i]:
                self.defaultlist.append(self.tree.tree.flat[i])
                self.default.append((i,self.tree.tree.flat[i]))
    def offlinedownload(self,io=None,auto=False):
        if not auto:io=askio('Get sequences offline',STRINGS.loc['IO::SELECT:COLUMNS',LANGUAGE],
                            setio(STRINGS.loc['IO::INPUTS',LANGUAGE],{'FASTA':(DCombo,[],{'text':STRINGS.loc['IO::DOWNLOAD:REFERENCE',LANGUAGE],'values':self.DB['FDB'].names})},validate=all),
                            setio(STRINGS.loc['IO::OUTPUTS',LANGUAGE],{'FASTA':(Constant,[],{'title':STRINGS.loc['IO::OUTPUT:FASTA_TITLE',LANGUAGE],'prompt':STRINGS.loc['IO::OUTPUT:TEXT',LANGUAGE],'state':'disabled'})},validate=None),validate=None)      
        if self.debug.get():print(io)
        elif io:
            self.lock()
            n=1
            L=ProgressLogger(tk,maximum=(l3:=len(self.clusters)))
            for LIST in self.clusters:
                L.step(f'Running offline fetch sequence job...\nCluster {n}/{l3}',1)
                S='';f=d=0;offset=0;t=time();l=len(LIST);mask=[True]*l
                #l2=sum([bool(i)for i in mask])-offset
                #self.dashboard.config(all=f'{l} ({l2} to do)')
                fas=io[0]['FASTA']
                zindex=self.DB['FDB'].zindex[fas]
                try:
                    for i in range(l):
                        if mask[i]:
                            try:
                                S+=self.DB['FDB'][fas,LIST[i][1]];L.step(f'Running offline fetch sequence job...\nCluster {n}/{l3}: Sequence {i}/{l} fetched',0)
                            except KeyError:
                                f+=1;L.step(f'Running offline fetch sequence job...\nCluster {n}/{l3}: Sequence {i}/{l} not found',0)
                            #self.cpr()
                            #T=int(time()-t)
                            #T2=(int(T*(l-i)/(i)))if i!=0 else 0
                            #self.dashboard.config(done=d,fail=f,left=l2-d,elapsed=f'{T//86400}d {(T//3600)%24:02.0f}:{(T//60)%60:02.0f}:{T%60:02.0f}',ETA=f'{T2//86400}d {(T2//3600)%24:02.0f}:{(T2//60)%60:02.0f}:{T2%60:02.0f}')
                    self.fastav.receive(S)
                except KeyboardInterrupt:
                    showwarning('E-Stop','Operation successfully interrupted')
                    L.close()
                n+=1
            L.close()
            self.unlock()
            #self.ding(auto)
    def save(self,file):
        with open(file,'w')as f:f.write(self.send())
        if file in self.DB['FDB'].names:self.DB['FDB'].rebuild(file)
    def receive(self,payload):
        if payload is not None:
            self.text.delete(1.0,'end')
            self.text.insert(1.0,payload)
    def send(self):return self.text.get(1.0,'end')
class About(WrapperStub):
    printer=None
    name='About'
    format=[]
    lstype=None
    def body(self,**kw):
        try:
            with open(join(getcwd(),'bin','Licenses.txt'))as f:license=f.read()
        except:license=f'Cannot read [{join(getcwd(),"bin","Licenses.txt")}]'
        self.text=ResizableOmniText(self.container,scrolling=(0,1),minwidth=400,minheight=200,minfont=1,maxfont=18,text='About',**kw)
        self.text.insert('end','''\
Created by Antoniy Elias Sverdrup
© Anthony&Co. Media Production 2017-2025. All rights reserved.

This is a beta-version of this software.
You may encounter previously unknown errors or unintended behaviour.
Please report found issues to https://github.com/A-Sverdrup/water-expert-system/issues

This program was developed on Windows and was not yet tested on MacOS, Linux or BSD.

Bundled software licenses:

'''+license)
        return self.text
def rebuild():
    if askyesno('Question','Have you already downloaded nucl_gb.accession2taxid.gz?'):    
        t={'type':'check','default':False,'justify':'left','anchor':'w','value':True,}
        tk.withdraw()
        DB['db'].withdraw()
        io=askcustom('Rebuild GB2Taxid','''\
This operation will take significant time, disk space and computational resource.
Once started, this operation cannot be stopped (paused or cancelled) until completed.
This operation has high CPU utilization and RAM usage, and can make the computer unusable
for other tasks while running.
If you want to continue, please make sure that:''',
                         (Group,[],{'title':'Checklist','widgets':{
                          '1':(DBool,[],{**t,'prompt':'The computer has no scheduled restarts and, if Windows, no pending updates.'}),
                          '2':(DBool,[],{**t,'prompt':'The computer is plugged in (if laptop) or has an UPS (if desktop).'}),
                          '3':(DBool,[],{**t,'prompt':'Sleep mode and hibernation are disabled.'}),
                          '4':(DBool,[],{**t,'prompt':'Other users are informed not to shut down or restart the computer.'}),
                          '5':(DBool,[],{**t,'prompt':'Other users are informed not to attempt to terminate the program.'}),
                          '6':(DBool,[],{**t,'prompt':'There are no other resource-intensive tasks already running.'}),
                          '7':(DBool,[],{**t,'prompt':'There are no other users currently using this computer in person or via remote connection'}),
                          '8':(DBool,[],{**t,'prompt':'There are no users planning to use this computer in the next 18-24 hours'}),
                          '9':(DBool,[],{**t,'prompt':'At least 28 GB of free disk space is available'}),
                          '10':(DBool,[],{**t,'prompt':f'You have write permissions to\n{join(getcwd(),"temp","")}'}),
                          '11':(DBool,[],{**t,'prompt':'The folder is not set to read-only and is an antivirus exclusion\n(antivirus scanning locks the folder to read-only)'}),
                          },'validate':all}))
        if io:
            if file:=askopenfilename(defaultextension='*.gz',filetypes=(('GZ archive','*.gz'),)):rebuild2(file)
        tk.deiconify()
    else:Link('https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/nucl_gb.accession2taxid.gz','Download nucl_gb.accession2taxid.gz')
def rebuild2(file):
    L=ProgressLogger(tk,maximum=6)
    L.step(f'Stage 1/6: Unpacking {basename(file)}',1)
    sourcepath=join(getcwd(),"temp",'nucl_gb.accession2taxid')
    try:
        if exists(sourcepath):
            try:remove(sourcepath)
            except:raise OtherError('Error!',f'Cannot remove pre-existing\n{sourcepath}\nfrom temp folder')
        if not exists(join(getcwd(),"temp")):
            try:mkdir(join(getcwd(),"temp"),mode=777)
            except:raise OtherError('Error!',f'Cannot create temp folder\n{join(getcwd(),"temp")}')
        command = sevenz_path+' e %s -o"%s"'%(file,join(getcwd(),"temp"))
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        a=0;b=0
        io=StringIO()
        try:
            while True:
                output = process.stdout.readline()
                if output:a+=1;io.write(output)
                if process.poll() is not None: break
                b+=1
                if b>1000:raise OtherError('Error!','Unknown error')
            remaining_output, remaining_error = process.communicate()
            if remaining_output:io.write(remaining_output)
            if remaining_error:print(remaining_error)
        except KeyboardInterrupt:
            process.terminate()
            print(f'Received SIGTERM, terminating')
            raise OtherError('Error!','7-Zip process terminated')
        sourcepath=join(getcwd(),"temp",'nucl_gb.accession2taxid')
        if process.returncode==0 and exists(sourcepath):
            L.step('Stage 2/6: Loading nucl_gb.accession2taxid')
            f=open(sourcepath)
            if f.readline()!='accession\taccession.version\ttaxid\tgi\n':raise OtherError('Error!','Not a nucl_gb.accession2taxid file')
            L.close()
            def s3p(n):
                n=list(str(n));l=len(n)
                for i in range(l//3):n.insert(l-3*(i+1),' ')
                return''.join(n)
            constant=37.79725160900933;
            estimate=getsize(sourcepath)/constant
            total='~'+s3p(round(estimate)).strip()
            step=round(estimate/100,-3)
            L=ProgressLogger(tk,maximum=100)
            L.step(f'Stage 3/6: Processing\nLine 0/{total}',0)
            fl={};n=0
            while (l:=f.readline()):
                s=l.split('\t')
                if s[0][:2] not in fl:
                    fl[s[0][:2]]=open(join(getcwd(),"temp",s[0][:2]),'w')
                    fl[s[0][:2]].write(s[0]+';'+s[2]+'\n')
                    fl[s[0][:2]].close()
                elif fl[s[0][:2]].closed:
                    fl[s[0][:2]]=open(join(getcwd(),"temp",s[0][:2]),'a')
                    fl[s[0][:2]].write(s[0]+';'+s[2]+'\n')
                    fl[s[0][:2]].close()
                else:raise OtherError('Error!','Unknown error')
                n+=1
                if n%step==0:L.step(f'Stage 3/6: Processing\nLine {s3p(n)}/{total}')
            f.close()
            datepath=join(getcwd(),"temp",'__date__')
            with open(datepath,'w')as t:t.write(str(time()))
            L.close()
            L=ProgressLogger(tk,maximum=6)
            L.step('Stage 4/6: Removing nucl_gb.accession2taxid',4)
            try:remove(sourcepath)
            except:showwarning('Error!',f'Cannot remove\n{sourcepath}')
            L.close()
            z=ZipFile(join(getcwd(),"temp",'gb2taxid.zip'),'w',8)
            n=0;l=len([*fl])
            L=ProgressLogger(tk,maximum=l)
            for i in fl:
                z.write(join(getcwd(),"temp",i),i)
                n+=1
                L.step('Stage 5/6: Zipping\nFile {n}/{l}')
            L.step('Stage 5/6: Zipping\nTimestamp',0)
            z.write(datepath,'__date__')
            z.close()
            L.close()
            L=ProgressLogger(tk,maximum=6)
            L.step('Stage 6/6: Cleaning up temporary files',6)
            for i in fl:
                try:remove(join(getcwd(),"temp",i))
                except:showwarning('Error!',f'Cannot remove {join(getcwd(),"temp",i)}')
            try:remove(datepath)
            except:showwarning('Error!',f'Cannot remove {datepath}')
            L.close()
            showinfo('Done!','Database rebuild complete\n')
            try:
                from os import rename
                from os.path import samefile
                dbpath=join(getcwd(),"db",'gb2taxid.zip')
                flag=0
                if samefile(DB['gb2taxid'].zip.filename,dbpath):flag=1;DB['gb2taxid'].close()
                if exists(dbpath):remove(dbpath)
                rename(join(getcwd(),"temp",'gb2taxid.zip'),dbpath)
                if flag:DB['gb2taxid'].load(dbpath)
            except:showwarning('Error!',f'Cannot move gb2taxid.zip from temp folder to DB folder.')
        else:raise OtherError('Error!',f'Cannot unpack\n{file}')  
    except OtherError as E:showerror(*E.args)

s=Style()
s.configure('TW2.TNotebook',tabposition='sw',tabmargins=0)

ui2=Notebook(tk)
ui2.pack(fill='both',expand=True)

page1=PanedWindow(ui2,orient='horizontal')
fasta=FastaWrapper(page1,'GeneProt',text='FASTA',font=('Courier New',7),width=300)
table=TableWrapper(page1,'Table')
DB['db']=db=DatabaseProvider(tk)
DB['gb2taxid']=GB2TaxIdProvider(db,sevenz=sevenz)
DB['gb2taxid'].rebuild=rebuild
DB['taxdump']=TaxdumpProvider(db)
DB['FDB']=FASTAProvider(db)
DB['BLAST']=BLASTDBProvider(db,makeblastdb=makeblastdb)
DB['Saprobity']=SaprobityProvider(db)
mid=Middle(tk,page1,table,fasta,online=online,blast=blast)
page1.add(table)
page1.add(mid)
page1.add(fasta)

page2=FastCons(tk,'FastCons',font=('Courier New',8),width=800,height=400)

fastav=FastaViewer(STRINGS.loc['GUI::FASTA:NEW',LANGUAGE],STRINGS.loc['GUI::FASTA:TITLE',LANGUAGE],FastaWrapper)
vfastav=FastaViewer(STRINGS.loc['GUI::FASTA:NEW_VISUAL',LANGUAGE],STRINGS.loc['GUI::FASTA:TITLE_VISUAL',LANGUAGE],FastaTableWrapper)

page3=PanedWindow(ui2,orient='horizontal')
tree=TreeWrapper(page3,'TreeView')
cluster=ClusterFAC(page3,tree,fastav)
page3.add(tree)
page3.add(cluster)

if online:page4=Bulker(tk,'Very Large Bulk Downloader',width=800,height=400)
else:page4=Label(ui2,text='Package "bio" is unavailable!',width=80,height=30,relief='raised',state='disabled')

page5=About(ui2,'About')

ui2.add(page1,text='GeneProt')
ui2.add(page2,text='FastCons')
ui2.add(page3,text='TreeView')
ui2.add(page4,text='VLB')
ui2.add(page5,text='About')
radio=Transceiver()
radio.instance(fasta)
radio.instance(page2)
radio.instance(DB['FDB'],1,0)
radio.invisible_instance(fastav,0,1)
fastav.radio=radio
radio.invisible_instance(vfastav,0,1)
vfastav.radio=radio
L.close()
def destroy():
    L=ProgressLogger(tk,1)
    L.step(STRINGS.loc['MISC::EXIT',LANGUAGE])
    tk.destroy()
    exit(0)
tk.wm_protocol('WM_DELETE_WINDOW',destroy)
tk.deiconify()
if exists(join(getcwd(),'default.zlist')):DB['FDB'].load(join(getcwd(),'default.zlist'))
if exists(join(getcwd(),'db','gb2taxid.zip')):DB['gb2taxid'].open(join(getcwd(),'db','gb2taxid.zip'))
if exists(join(getcwd(),'db','new_taxdump.zip')):DB['taxdump'].open(join(getcwd(),'db','new_taxdump.zip'))
#exec(open('deacftpo.py').read())
tk.mainloop()
