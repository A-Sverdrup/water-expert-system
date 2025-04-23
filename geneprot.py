if __name__!='__main__':raise ImportError("This program is a standalone software and cannot be imported as module")
try:
    from tkinter import Tk,Toplevel,Button,Checkbutton,Entry,Frame,Label,LabelFrame,Menu,PanedWindow,Scrollbar,BooleanVar,StringVar,IntVar
    from tkinter.filedialog import askopenfilenames,askdirectory
    from tkinter.messagebox import showerror,showinfo,showwarning,askyesno
    from tkinter.simpledialog import askstring
    from tkinter.ttk import Notebook,Style
except ImportError:
    from sys import stderr
    print('Your Python is not configured for Tk. The program cannot be run.',file=stderr)
    input('Press Enter to exit.')
    exit(1)
try:
    from tk2 import EntryLabel,LabelMenu2,OmniSpin,OmniText,ResizableOmniText,ToggleButton,ToggleRadioButton,OpenFileButton
except ImportError:
    showerror('Package "tk2" cannot be loaded!','Required library (tk2) is corrupted or missing.\nThe program cannot be run.\n\nPlease check for missing files and/or reinstall the program')
    exit(1)
try:
    from custom import *
except ImportError:
    showerror('Package "custom" cannot be loaded!','Required library (custom) is corrupted or missing.\nThe program cannot be run.\n\nPlease check for missing files and/or reinstall the program')
    exit(1)
try:
    from pandas import read_csv,DataFrame,concat,ExcelFile,ExcelWriter,read_excel
except:
    from sys import platform
    if platform=='win32':advice='If you have admin rights, you can install pandas using Command Prompt:\n\npy -m pip install pandas'
    elif platform=='darwin':advice='You can install pandas via Terminal. You will have to input your password:\n\nsudo pip3 install pandas'
    else:advice='If you are a superuser, you can run\n\nsudo pip3 install pandas\n\nto install pandas'
    showerror('Package "pandas" cannot be loaded!','An external package (pandas) is corrupted, missing or unavailable.\nThe program cannot be run.\n\n'+advice)
    exit()
from re import search
from os import sep as ossep
from time import time
try:
    from Bio.Entrez.Parser import NotXMLError
    from Bio import Entrez,SeqIO
    from urllib.error import HTTPError
    from http.client import RemoteDisconnected,IncompleteRead
    online=True
except:
    online=False
    if not askyesno('Package "bio" cannot be loaded!','An external package (bio) is corrupted, missing or unavailable.\nThis package is needed for online functionality. The program can be run without it, however, online functionality (access to GenBank, GenPept, NCBI Taxonomy) will be unavailable. Continue loading?'):
        exit()
from sys import platform
if platform=='win32':None
elif platform=='darwin':showwarning('Warning','This program was developed on Windows and was not tested on MacOS.\nYou may encounter previously unknown errors or unintended behaviour.')
else:showwarning('Warning',f'This program was developed on Windows and was not tested on [{platform}].\nYou may encounter previously unknown errors or unintended behaviour.')
import csv
csv.register_dialect(';', delimiter=';')
csv.register_dialect('\t', delimiter='\t')
csv.register_dialect('|', delimiter='|')
csv.register_dialect(' ', delimiter=' ')
csv.register_dialect(',', delimiter=',')
DB={}
FASTA=['FASTA','*.fas',(('FASTA','*.fas *.fta *.fasta'),('Nucleotide FASTA','*.ffn *.fna'),('Amino acid FASTA','*.faa'),('All files','*'))]

class TableWrapper(LogPrinter,WrapperStub):
    format=('CSV','*.csv',(('CSV table','*.csv'),('All files','*')))
    def body(self,**kw):
        dl=LabelFrame(self.ls,text='Separator')
        dl.grid(row=2,column=0)
        self.delimiter=LabelMenu2(dl,values={'Tab':'\t','Space':' ',',':',',';':';','|':'|'},default=';',relief='ridge',width=100,border=2)
        self.delimiter.pack(fill='both',expand=True)
        self.table=Table(self.container,array=DataFrame([['']*10 for i in range(20)]))
        Checkbutton(self.ls,text='Use headers',variable=self.table.header).grid(row=3,column=0)
        return self.table
    def __getitem__(self,key):
        return self.table[key]
    def __setitem__(self,key,value):
        self.table[key]=value
    def load(self,file):
        try:
            self.print(f'Loading {file}...',end=' ')
            with open(file) as csvfile: array = DataFrame(data = [[number(i)for i in row] for row in csv.reader(csvfile, self.delimiter.get())]).replace(to_replace=None,value='',regex=[None])
            if self.table.header.get():
                array.index=['index',*array.index[1:]]
                array=array.T.set_index('index').T.reset_index(drop=True)
            self.table.load(array,file)
            del array
            self.print('done')
        except UnicodeDecodeError:showerror('Error','Error loading file\nEncoding is not UTF-8')
    def save(self,file):
        if self.table.header.get():self.table.array.to_csv(file,sep=self.delimiter.get(),encoding='utf-8',index=False)
        else:self.table.array.to_csv(file,sep=self.delimiter.get(),encoding='utf-8',index=False,header=False)
##class LeftTable(TableWrapper):
##    def body(self,**kw):
##        col=LabelFrame(self.top,text='Columns')
##        col.grid(row=0,column=2,sticky='nsew')
##        
##        tab=TableWrapper.body(self)
##        self.table.bind('<<resize>>',self.resize)
##        
##        self.taxonomy=TaxSpin(col,self.table.W-1)
##        self.taxonomy.grid(row=0,column=0,rowspan=3)
##        self.exist=OmniSpin(col,text='Exists',width=4,cnf={'from':0,'to':self.table.W-1})
##        self.exist.grid(row=0,column=1,padx=10,sticky='nsew')
##        self.accession=OmniSpin(col,text='Accession',width=4,cnf={'from':0,'to':self.table.W-1})
##        self.accession.grid(row=1,column=1,padx=10,sticky='nsew')
##        self.saprobity=OmniSpin(col,text='Saprobity',width=4,cnf={'from':0,'to':self.table.W-1})
##        self.saprobity.grid(row=2,column=1,padx=10,sticky='nsew')
##        return self.table
##    def resize(self,event):
##        for i in[self.exist,self.accession,self.saprobity]:i['to']=self.table.W-1
##    def accessions(self):
##        return self[:,self.accession.get()]
##    def taxnames(self):
##        if len(self.taxonomy.get())==2:
##            taxnames = list(map(lambda a:a[0]+' '+a[1],zip(self[:,self.taxonomy.get()[0]], \
##                                                           self[:,self.taxonomy.get()[1]])))
##        else:taxnames = self[:,self.taxonomy.get()[0]]
##        return taxnames
##    def saprobities(self):
##        return self[:,self.saprobity.get()]

##class TableWrapper2(WrapperStub):
##    format=('Table','*.xlsx *.xls *.ods',(('Electronic tables','*.xlsx *.xls *.ods'),('Microsoft Excel 2007-2021','*.xlsx'),('Microsoft Excel 95-2003','*.xls'),('OpenOffice/LibreOffice','*.ods'),('All files','*')))
##    def body(self,**kw):
##        dl=LabelFrame(self.ls,text='Separator')
##        dl.grid(row=2,column=0)
##        self.file=None
##        self.saved=True
##        self.table=Table(self.container,array=DataFrame([['']*10 for i in range(20)]))
##        self.table.bind('<<editvalues>>',self.repl)
##        self.remote=Notebook(self.table,style='TW2.TNotebook')
##        self.remote.grid(row=self.table.height+2,column=0,columnspan=self.table.width+2,sticky='nsew')
##        self.sheets=[]
##        return self.table
##    def __getitem__(self,key):
##        return self.table[key]
##    def __setitem__(self,key,value):
##        self.table[key]=value
##    def load(self,file):
##        for i in range(len(self.remote.tabs())):self.remote.forget(0)
##        self.sheets=[]
##        if self.file:
##            self.remote.unbind('<<NotebookTabChanged>>')
##            self.file.close()
##            self.file=None
##        self.file=ExcelFile(file)
##        self.names=self.file.sheet_names
##        for i in range(len(self.file.sheet_names)):
##            self.remote.add(Frame(self.remote),text=self.file.sheet_names[i])
##            self.sheets.append(read_excel(self.file, self.file.sheet_names[i], engine='openpyxl'))#self.file.parse(self.file.sheet_names[i]).fillna(''))
##        self.file.close()
##        self.file=None
##        self.table.load(self.sheets[0],file)
##        self.remote.bind('<<NotebookTabChanged>>',self.flip)
##    def repl(self,event):
##        print(self.remote.index("current"),'stoopid!')
##        self.sheets[self.remote.index("current")]=self.table.array
##    def flip(self,event):
##        print('loading')
##        self.table.load(self.sheets[self.remote.index("current")].fillna(''))
##        print('loaded')
##    def save(self,file):
##        writer=ExcelWriter(file,mode='w')#,if_sheet_exists="replace")
##        for i in range(len(self.sheets)):
##            self.sheets[i].to_excel(writer, sheet_name=self.names[i],index=None)
##        writer.close()
        
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
    def print(self,text,end='\n'):
        self.text.insert('end',text+end);self.text.see('end');
    def stop(self,*a):
        self.text.insert('end','\n'+'~'*40+'\nE-Stop '+('engaged'if self.stopped.get()else'released')+'!\n'+'~'*40+'\n');self.text.see('end')
        self.unlock()
    def lock(self):
        for i in self.controls:i.config(state='disabled')
    def unlock(self):
        for i in self.controls:i.config(state='normal')
class Middle(Downloader,LabelFrame):
    DB=DB
    def __init__(self,master,left,right,online):
        self.table=left;self.fasta=right;self.table.printer=self
        for i in self.DB:self.DB[i].printer=self
        LabelFrame.__init__(self,master=master,text='Toolbox')
        self.inner=PanedWindow(self,orient='vertical')
        self.inner.pack(fill='both',expand=True)
        
        self.google=Search(self.table.top,'Search in table',{'Any match':'Any','Exact match':'Exact','Use RegEx':'Regex'},'Any',self.query)        
        self.google.grid(row=0,column=1)
        #self.inner.add(self.google)

        tzm=LabelFrame(self.table.top,text='Manipulate data')
        tzm.grid(row=1,column=1)
        m1=Button(tzm,text='Function',command=self.manipulate1);m1.pack(side='left',fill='x',expand=True)
        m2=Button(tzm,text='Statistics',command=self.manipulate2);m2.pack(side='left',fill='x',expand=True)
        m3=Button(tzm,text='Operate',state='disabled');m3.pack(side='left',fill='x',expand=True)
        
        a=LabelFrame(self.inner,text='Manage databases')
        db1=Button(a,text='GB2Taxid',command=self.DB['gb2taxid']);db1.pack(side='left',fill='x',expand=True)
        db2=Button(a,text='Taxdump',command=self.DB['taxdump']);db2.pack(side='left',fill='x',expand=True)
        db3=Button(a,text='FASTA',command=self.DB['FDB']);db3.pack(side='left',fill='x',expand=True)
        
        self.debug=BooleanVar(self,value=False)
        self.debugger=LabelFrame(self,text='Debug',relief='ridge')
        Checkbutton(self.debugger,text='Debug',variable=self.debug,state='disabled').grid(row=0,column=0,columnspan=2)
        Button(self.debugger,text='Lock',command=self.lock).grid(row=1,column=1)
        Button(self.debugger,text='Un',command=self.unlock).grid(row=1,column=0)
        self.bind('<Control-Shift-Double-1>',lambda e:(self.debugger.place(x=0,y=0),self.debug.set(True),print('Debug mode enabled!'),"break")[3])
        self.debugger.bind('<Control-Shift-Double-1>',lambda e:(self.debugger.place_forget(),self.debug.set(False),print('Debug mode disabled!'),"break")[3])
        self.inner.add(a)
        
        b=LabelFrame(self.inner,text='Automation')
        bl=Button(b,text='Run BLAST',state='disabled');bl.pack(side='left',fill='x',expand=True)
        run=Button(b,text='Complete run',state='disabled');run.pack(side='left',fill='x',expand=True)
        rnd=Button(b,text='Bootstrap runs',state='disabled');rnd.pack(side='left',fill='x',expand=True)
        dd=Button(b,text='Deduplicate',command=self.dedup);dd.pack(side='left',fill='x',expand=True)
        self.inner.add(b)
##        bb=LabelFrame(self.inner,text='Deduplicate')
##        dd1=Button(bb,text='Reads',command=self.dedup1);dd1.pack(side='left',fill='x',expand=True)
##        dd2=Button(bb,text='accessions',command=self.dedup2);dd2.pack(side='left',fill='x',expand=True)
##        dd3=Button(bb,text='taxids',command=self.dedup3);dd3.pack(side='left',fill='x',expand=True)
##        self.inner.add(bb)
        
        c=LabelFrame(self.inner,text='FASTA Tasks')
        rn=Button(c,text='Rename',state='disabled');rn.pack(side='left',fill='x',expand=True)
        mg=Button(c,text='Merge',state='disabled');mg.pack(side='left',fill='x',expand=True)
        ft=Button(c,text='Put into table',command=self.storefasta);ft.pack(side='left',fill='x',expand=True)
        self.inner.add(c)
        
        d=LabelFrame(self.inner,text='NCBI tasks'if online else'Offline tasks')
        Label(d,text='Get taxonomy data').grid(row=0,column=0,sticky='nsew')
        tax1=Button(d,text='Offline',command=self.offlinetaxonomy);tax1.grid(row=0,column=1,sticky='nsew')
        tax2=Button(d,text='Online',command=self.onlinetaxonomy,state='normal'if online else'disabled');tax2.grid(row=0,column=2,sticky='nsew')
        Label(d,text='Get sequence data').grid(row=1,column=0,sticky='nsew')
        seq1=Button(d,text='Offline',state='disabled',command=self.offlinedownload);seq1.grid(row=1,column=1,sticky='nsew')
        seq2=Button(d,text='Online',command=self.onlinedownload,state='normal'if online else'disabled');seq2.grid(row=1,column=2,sticky='nsew')
        self.controls=[m1,m2,#m3,
                       db1,db2,db3,
                       #bl,run,rnd,
                       dd,#rn,mg,
                       ft,
                       tax1,#seq1
                       ]
        if not online:
            Label(status,text='Package "bio" is unavailable!',relief='raised',state='disabled',height=7).grid(row=2,column=0,columnspan=3,sticky='nsew')
        else:
            self.controls.append(tax2)
            self.controls.append(seq2)
        d.columnconfigure((0,1,2), weight=1)
        d.rowconfigure((0,1)if online else(0,1,2), weight=1)
        self.inner.add(d)
        
        status=LabelFrame(self.inner,text='Job status')
        self.inner.add(status)
        grid=Frame(status);grid.pack(fill='x',expand=True)
        self.dashboard=Dashboard(status,orient='horizontal');self.dashboard.pack(fill='x',expand=True)
        self.stopped=ToggleButton(status,text='Emergency STOP',border=4,bg='red',value=False)
        self.stopped.pack(side='left',fill='x',expand=True)
        self.stopped.trace_add('write',self.stop)
        
        self.text=OmniText(self.inner,text='Log',scrolling=(1,1),width=40,height=16,log_buttons=True,font=('Courier New',7))
        self.inner.add(self.text)
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
                    self.text.insert('end','Found %s at column %s, row %s\n'%(query, i, j));self.text.see('end')
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
        if type=='GB2Taxid':
            enabled=self.DB['gb2taxid'].zip
            if enabled:return {'title':'GB2Taxid','prompt':self.DB['gb2taxid'].zip.filename,'value':True,'valid':True}
            else:return {'title':'GB2Taxid','prompt':'Load GB2Taxid first!','value':None,'valid':False,'error':'Load GB2Taxid first!'}
        elif type=='Taxdump':
            enabled=self.DB['taxdump'].zip
            if enabled:return {'title':'Taxdump','prompt':self.DB['taxdump'].zip.filename,'value':True,'valid':True}
            else:return {'title':'Taxdump','prompt':'Load new_taxdump.zip first!','value':None,'valid':False,'error':'Load new_taxdump.zip first!'}
    def manipulate1(self):
        spin=self.getspin()
        ff=lambda f,a:DataFrame([f(i)for i in a])
        fl2=lambda f,a,b:DataFrame([f(bool(i[0]),bool(i[1]))for i in zip(a,b)])
        def verify(io):
            if ops[io[0]['op']]==None:showerror('Error','You must select an option!');return False
            if io[0]['op']=='IF [I1] THEN [I2] ELSE [I3]'and((io[0]['2']is None)or(io[0]['3']is None)):showerror('Error','This function requires 3 inputs!');return False
            elif io[0]['op'].startswith('[I1]')and io[0]['op'].endswith('[I2]')and(io[0]['2']is None):showerror('Error','This function requires 2 inputs!');return False
            elif io[0]['op'].startswith('CONCAT')and(io[0]['2']is None):return False
            else:return True
        io=askio('Compare','Select columns:',
                 setio('Inputs',{'1':(DSpin,[],{**spin,**{'text':'Input I1'}}),
                                 '2':(DSpin,[],{**spin,**{'type':'check','text':'Input I2'}}),
                                 '3':(DSpin,[],{**spin,**{'type':'check','text':'Input I3'}}),
                                 'op':(DCombo,[],{'text':'Operation','values':[*ops]}),
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
        io=whereto('Statistics','Select column',self.table.table.W-1,'-y')
        if self.debug.get():print(io)
        elif io is not None:
            col=self.table[:,io]
            s=c=0;m=float('inf');M=float('-inf')
            for i in col:
                if isnum(i):s+=i;c+=1;m=min(i,m);M=max(i,M)
            showlines('Statistics','Statistics',{'Sum':s,'Mean':0 if c==0 else(s/c),'Count':c,'Minimum':m,'Maximum':M})
    def dedup(self):
        spin=self.getspin()
        def verify(io):
            valid=1
            if(io[0]['dedup3']is None)and(bool(io[1]['Taxonomy']['Name'])or(io[1]['Taxonomy']['Lineage']is not None)):showerror('Error','Deduplication stage 3 must be enabled to use Taxonomy');valid=0
            if(bool(io[1]['Taxonomy']['Name'])or(io[1]['Taxonomy']['Lineage']is not None))and(io[0]['Taxdump']is None):showerror('Error','Load new_taxdump.zip first!');valid=0
            return valid
        io=askio('Deduplicate','Select columns:',
                 setio('Inputs',{'dedup1':(Group,[],{'type':'check','orient':'horizontal','title':'Stage 1: BLAST duplicate alignments','widgets':{
                                                  'reads':(DSpin,[],{**spin,**{'text':'Read ID'}}),
                                                  'pident':(DSpin,[],{**spin,**{'text':'Per Ident'}}),
                                                  'evalue':(DSpin,[],{**spin,**{'text':'E-Value'}}),
                                                  }}),
                      'dedup2':(Group,[],{'type':'check','title':'Stage 2: accessions','widgets':{'Accessions':(DSpin,[],{**spin,**{'text':'Accessions'}})}}),
                      'GB2Taxid':(Group,[],{'type':'check','title':'Accessions \u2192 taxids','widgets':{
                                                                 'GB2Taxid':(Option,[],self.setdb('GB2Taxid')),
                                                                 }}),
                      'dedup3':(RadioGroup,[],{'title':'Stage 3: taxids','validate':None,'widgets':{
                                                             'dedup3c':(DBool,[],{'type':'radio','prompt':'Auto-select'}),
                                                             'dedup3i':(Group,[],{'type':'radio','orient':'horizontal','widgets':{
                                                                 'txid':(DSpin,[],{**spin,**{'text':'taxids'}}),
                                                                 'Count':(DSpin,[],{**spin,**{'text':'Count'}}),
                                                                 }}),
                                                             }}),
                      'Taxdump':(Option,[],{'type':'check',**self.setdb('Taxdump')}),
                     },validate=any,error='Enable at least one input'),
                 setio('Outputs',{'Table':(Constant,[],{'title':'Table','prompt':'<table output>','state':'disabled'}),
                                        'Taxonomy':(Group,[],{'title':'Taxonomy','widgets':{
                                            'Name':(DBool,[],{'type':'check','prompt':'Scientific name'}),
                                            'Lineage':(RadioGroup,[],{'validate':None,'widgets':{
                                                 'Full':(Option,[],{'type':'radio','prompt':'Full lineage'}),
                                                 'Ranked':(Option,[],{'type':'radio','prompt':'Ranked lineage'}),
                                             }}),
                                         }}),
                             },validate=any),
                 verify)
        if self.debug.get():print(io)
        elif io:
            if io[0]['dedup1']:self.dedup1(io=[io[0]['dedup1'],{'Table': None}],auto=True)
            if io[0]['dedup2']:self.dedup2(io=[io[0]['dedup2'],{'Table': None}],auto=True)
            if io[0]['GB2Taxid']:
                    self.table.table.insertcol(1)
                    self.table.table.rename(1,'taxid')
                    self.offlinetaxonomy(io=[{'Taxonomy': ('Accession', {'Accessions': 0, 'GB2Taxid': True}), 'Taxdump': True}, {'txid': 1, 'name':None, 'Taxonomy': None}],auto=True)
            if io[0]['dedup3']is not None:
                if io[0]['dedup3'][0]=='dedup3c':
                    self.dedup3(io=[{'txid': 1, 'Count': 2}, {'Table': None}],auto=True)
                elif io[0]['dedup3'][0]=='dedup3i':self.dedup3(io=[io[0]['dedup3'][1],{'Table': None}],auto=True)
            if io[1]['Taxonomy']['Name']:
                self.table.table.insertcol(2)
                self.table.table.rename(2,'Scientific name')
                n=3;name=2
                if io[1]['Taxonomy']['Lineage'] is None:
                    self.offlinetaxonomy(io=[{'Taxonomy': ('txid', 0), 'Taxdump': True}, {'txid': None, 'name':name, 'Taxonomy': None}],auto=True)
            else:n=2;name=None
            if io[1]['Taxonomy']['Lineage'][0]=='Full':
                self.table.table.insertcol(n)
                self.table.table.rename(n,'Full lineage')
                self.offlinetaxonomy(io=[{'Taxonomy': ('txid', 0), 'Taxdump': True}, {'txid': None, 'name':name, 'Taxonomy': ('Full', n)}],auto=True)
            elif io[1]['Taxonomy']['Lineage'][0]=='Ranked':
                for i in range(8):
                    self.table.table.insertcol(n+i)
                    self.table.table.rename(n+i,['Domain','Kingdom','Phylum','Class','Order','Family','Genus','Species'][i])
                self.offlinetaxonomy(io=[{'Taxonomy': ('txid', 0), 'Taxdump': True}, {'txid': None, 'name':name, 'Taxonomy': ('Ranked', slice(n, n+8, None))}],auto=True)
            self.ding()
    def dedup1(self,io=None,auto=False):
        spin=self.getspin()
        if not auto:io=askio('Deduplication stage 1','Select columns:',
                     setio('Inputs',{'reads':(DSpin,[],{**spin,**{'text':'Read ID'}}),
                      'pident':(DSpin,[],{**spin,**{'text':'Per Ident'}}),
                      'evalue':(DSpin,[],{**spin,**{'text':'E-Value'}}),
                      }),
                    setio('Outputs',{'Table':(Constant,[],{'title':'Table','prompt':'<table output>','state':'disabled'})},validate=None),validate=None)
        if self.debug.get():print(io)
        elif io:
            self.print(f'Running deduplication stage 1...')
            self.cpr()
            reads=self.table[:,io[0]['reads']]
            pident=self.table[:,io[0]['pident']]
            evalue=self.table[:,io[0]['evalue']]
            reads2={}
            second_pident=second_evalue=0
            for i in range(len(reads)):
                if reads[i]not in reads2:reads2[reads[i]]=i
                else:
                    j=reads2[reads[i]]
                    if float(evalue[j])<float(evalue[i]):
                        if float(pident[j])>float(pident[i]):second_pident+=1
                        else:second_evalue+=1
                        reads2[reads[i]]=i
            lst=[reads2[i]for i in reads2]
            new_table=self.table[lst,:].reset_index(drop=True)
            self.table.table.load(new_table,'Dedup stage 1')
            self.print(f'Deduplicated {i+1} -> {len(lst)} reads')
            self.ding(auto)
    def dedup2(self,io=None,auto=False):
        if not auto:io=askio('Deduplication stage 2','Select columns:',
                     setio('Inputs',{'Accessions':(DSpin,[],{**self.getspin(),**{'text':'Accessions'}})}),
                     setio('Outputs',{'Table':(Constant,[],{'title':'Table','prompt':'<table output>','state':'disabled'})},validate=None),validate=None)
        if self.debug.get():print(io)
        elif io:
            self.print(f'Running deduplication stage 2...')
            self.cpr()
            accs=self.table[:,io[0]['Accessions']]
            accs2={}
            for i in range(len(accs)):
                if accs[i]not in accs2:accs2[accs[i]]=1
                else:accs2[accs[i]]+=1
            new_table=DataFrame(data=accs2.items(),columns=['Accession','Count'])
            self.table.table.load(new_table,'Dedup stage 2')
            self.print(f'Deduplicated {i+1} reads -> {len(accs2)} unique accessions')
            self.ding(auto)
    def dedup3(self,io=None,auto=False):
        if not auto:io=askio('Deduplication stage 3','Select columns:',
                     setio('Inputs',{'txid':(DSpin,[],{**self.getspin(),**{'text':'taxids'}}),
                      'Count':(DSpin,[],{**self.getspin(),**{'text':'Count'}})}),
                     setio('Outputs',{'Table':(Constant,[],{'title':'Table','prompt':'<table output>','state':'disabled'})},validate=None),validate=None)
        if self.debug.get():print(io)
        elif io:
            self.print(f'Running deduplication stage 3...')
            self.cpr()
            txids=self.table[:,io[0]['txid']]
            counts=self.table[:,io[0]['Count']]
            txids2={}
            for i in range(len(txids)):
                if txids[i]not in txids2:txids2[txids[i]]=counts[i]
                else:txids2[txids[i]]+=counts[i]
            new_table=DataFrame(data=txids2.items(),columns=['taxid','Count'])
            self.table.table.load(new_table,'Dedup stage 3')
            self.print(f'Deduplicated {i+1} -> {len(txids2)} taxids')
            self.ding(auto)
    def offlinetaxonomy(self,io=None,auto=False):
        spin=self.getspin()
        if not auto:io=askio('Get taxonomy offline','Select columns:',
                     setio('Inputs',{'Taxonomy':(RadioGroup,[],{'title':'Search by','widgets':{
                                     'Accession':(Group,[],{'type':'radio','title':'Accessions','widgets':{
                                         'Accessions':(DSpin,[],{**spin,**{'text':'Accession'}}),
                                         'GB2Taxid':(Option,[],self.setdb('GB2Taxid')),
                                     },'validate':all}),
                                     'name':(DSpin,[],{**spin,**{'type':'radio','text':'Scientific name'}}),
                                     'txid':(DSpin,[],{**spin,**{'type':'radio','text':'taxid'}})
                                     }}),
                                     'Filter':(DSpin,[],{**spin,**{'type':'check','text':'Filter'}}),
                                     'Taxdump':(Constant,[],self.setdb('Taxdump'))
                                    },validate=all),
                     setio('Outputs',{'txid':(DSpin,[],{**spin,**{'type':'check','text':'taxid'}}),
                                      'name':(DSpin,[],{**spin,**{'type':'check','text':'Scientific name'}}),
                                      'Taxonomy':(RadioGroup,[],{'type':'check','title':'Taxonomic lineage','widgets':{
                                          'Full':(DSpin,[],{**spin,**{'type':'radio','text':'Full lineage'}}),
                                          'Ranked':(TaxSpin2,[],{'type':'radio','maxvalue':self.table.table.W-1}),
                                      }})
                                      }, validate=any),
                    atleastoneoutput)
        if self.debug.get():print(io)
        elif io:
            self.lock()
            self.print('Running offline taxonomy job...')
            self.cpr()
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
            self.unlock()
            self.ding(auto)
    def onlinetaxonomy(self,io=None,auto=False):
        spin={**self.getspin(),**{'type':'check'}}
        if not auto:io=askio('Get taxonomy online','Select columns:',
                     setio('Inputs',{'Taxonomy':(RadioGroup,[],{'title':'Search by','widgets':{
                                                             'Name':(TaxSpin,[],{'type':'radio','text':'Scientific name','maxvalue':self.table.table.W-1}),
                                                             'txid':(DSpin,[],{**spin,**{'type':'radio','text':'taxid'}}),
                                                             }
                                                 }),
                      'Filter':(DSpin,[],{**spin,**{'text':'Filter'}})},validate=any),
                     setio('Outputs',{'txid':(DSpin,[],{**spin,**{'text':'taxid'}}),
                      'Current name':(DSpin,[],{**spin,**{'text':'Current name'}}),
                      'Full lineage':(DSpin,[],{**spin,**{'text':'Full lineage'}}),
                      'Exists':(DSpin,[],{**spin,**{'text':'Exists'}})},validate=any),
                     atleastoneoutput)
        if self.debug.get():print(io)
        elif io:
            taxnames=self.getio(io,'Taxonomy')
            mask=self.getio(io,'Filter')
            self.print('Running online taxonomy job...')
            self.cpr()
            if (io[1]['Current name']is not None) or (io[1]['Full lineage'] is not None):
                self.geneprot(LIST=taxnames, mask=mask, offset=0, pre=self.tpre, main=self.skip, main2=self.tmain, post=self.skip,
                              base='taxonomy', fetch=True, mode='rb',
                              eskw={'retmax':3},efkw={},sn=io[1]['Current name'],fl=io[1]['Full lineage'],ex=io[1]['Exists'],tx=io[1]['txid'])
            else:
                self.geneprot(LIST=taxnames, mask=mask, offset=0, pre=self.tpre, main=self.tmain2, main2=self.skip, post=self.skip,
                              base='taxonomy', fetch=False, mode='rb',
                              eskw={'retmax':3},efkw={},ex=io[1]['Exists'],tx=io[1]['txid'])
            self.ding(auto)
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
    def rename(self,io=None,auto=False):
        if not auto:io=askio('Rename FASTA for phylogeny','Select columns:',
                     {'Taxonomy':(TaxSpin,[],{'maxvalue':self.table.table.W-1}),
                      'Accession':(DSpin,[],{**self.getspin(),**{'text':'Accession'}}),
                      'Saprobity':(DSpin,[],{**self.getspin(),**{'text':'Saprobity'}}),
                      },
                     {'FASTA':(Constant,[],{'title':'FASTA','prompt':'<text output>','state':'disabled'})})        
        if self.debug.get():print(io)
        elif io:
            taxnames=self.getio(io,'Taxonomy')
            saprobcsv = dict(zip(self.table[:,io[0]['Accession']],zip(taxnames,self.table[:,io[0]['Saprobity']])))
            fasta2=[i for i in self.fasta.text.get(1.0,'end').split('>')if i not in['','\n',' ']]
            fasta3=[]
            i=f=0
            for S in fasta2:
                G=[i for i in S.splitlines()if i]
                h=G[0].split()
                if h[0] in saprobcsv:                    
                    fasta3.append('>%s %s %s\n%s'%(saprobcsv[h[0]][1],saprobcsv[h[0]][0],h[0],''.join(G[1:])))
                    i+=1
                else:
                    fasta3.append('>'+S)
                    f+=1
                    self.print('%s not found in table'%h[0])
                self.text.see('end')
            self.print('Renamed %s entries, failed %s entries'%(i,f))
            self.fasta.text.delete(0.0,'end')
            self.fasta.text.insert(0.0,'\n'.join(fasta3))
            self.ding(auto)
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
        if not auto:io=askio('Get sequences offline','Select columns:',
                            setio('Inputs',{'Accession':(DSpin,[],{'text':'Accession','width':4,'cnf':{'from':0,'to':self.table.table.W-1}}),
                                  'Filter':(DSpin,[],{'type':'check','text':'Filter','width':4,'cnf':{'from':0,'to':self.table.table.W-1}}),
                                  'FASTA':(DCombo,[],{'text':'Reference FASTA','values':self.DB['FDB'].names})},validate=all),
                            setio('Outputs',{'FASTA':(Constant,[],{'title':'FASTA','prompt':'<text output>','state':'disabled'})},validate=None),validate=None)      
        if self.debug.get():print(io)
        elif io:
            self.print('Running offline fetch sequence job...')
            self.cpr()
            mask=((self.table[:,io[0]['Filter']])if(io[0]['Filter'])else None)
            lst=self.table[:,io[0]['Accession']]
            fas=io[0]['FASTA']
            print(fas)
            print(zindex:=self.DB['FDB'].zindex[fas])
            print(asvindex:=[i[:i.index(' ')]for i in zindex])
            
            for i in range(len(lst)):
                if mask[i]:
                    try:
                        self.text.insert('end',self.DB['FDB'][fas,[*zindex][asvindex.index(lst[i])]])
                    except:
                        #if lst[i][-2]=='.':
                        print('not in asv')
                        #try:
                        #    self.text.insert('end',self.DB['FDB'][fas,[*zindex][asvindex.index(lst[i][:-2])]])
                        #except:print('not in as')
            #self.geneprot(LIST=self.table[:,io[0]['Accession']], mask=mask, offset=0, fetch=True, pre=self.skip, main=self.skip, main2=self.main, post=self.skip,
            #          base={'GenBank':'nuccore','GenPept':'protein'}[self.base.get()],
            #          eskw={'retmax':3},efkw={'rettype':'fasta','retmode':'text'})
            self.ding(auto)
    def onlinedownload(self,io=None,auto=False):
        def verify2(io):
            return 0 if io['ibase']=='' else 1
        def verify(io):
            if io[0]['ibase']=='':return 0
            if (io[0]['IN'][0]=='Taxonomy' and io[1]['OUT'][0]=='Search') or \
               (io[0]['IN'][0]=='Accession' and io[1]['OUT'][0]=='FASTA'):return 1
            else:showerror('Error','Choose (Taxonomy AND Search) OR (Accession AND Download FASTA)');return 0
        if not auto:io=askio('Get taxonomy online','Select columns:',
                     setio('Inputs',{'ibase':(DCombo,[],{'text':'Database','width':7,'values':['GenBank','GenPept']}),
                      'IN':(RadioGroup,[],{'widgets':{'Taxonomy':(TaxSpin,[],{'type':'radio','maxvalue':self.table.table.W-1}),
                                                      'Accession':(DSpin,[],{'type':'radio','text':'Accession','width':4,'cnf':{'from':0,'to':self.table.table.W-1}})
                                           }}),
                      'Filter':(DSpin,[],{'type':'check','text':'Filter','width':4,'cnf':{'from':0,'to':self.table.table.W-1}})
                                     },validate=verify2),
                     setio('Outputs',{'OUT':(RadioGroup,[],{'widgets':{'Search':(Group,[],{'title':'Search entries','type':'radio','validate':any,'widgets':{
                                                                          'Exists':(DSpin,[],{**self.getspin(),**{'text':'Exists'}}),
                                                                          'Count':(DSpin,[],{**self.getspin(),**{'type':'check','text':'Count'}})
                                                                        }}),
                                                                      'FASTA':(Option,[],{'type':'radio','title':'Download','prompt':'<text output>','state':'disabled'})
                                                            }}),
                                       },validate=any),verify)
        if self.debug.get():print(io)
        elif io:
            mask=self.getio(io,'Filter')
            self.print(f'Running online {io[0]["ibase"]}',end=' ')
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
            self.ding(auto)
class FastaWrapper(WrapperStub):
    format=FASTA
    DB=DB
    def body(self,**kw):
        self.text=ResizableOmniText(self.container,scrolling=(0,1),minwidth=400,minheight=200,font=('Courier New',7),**kw)
        self.google=Search(self.top,'Search in FASTA',{'Headers':'Headers','Sequences':'Sequences','Any':'Any'},'Headers',self.query)        
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
            self.text.tag_remove('sel',1.0,'end')
            self.text.see(pos)
            self.text.tag_add('sel', pos, end)
            self.searchpos = end
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
        if file in self.DB['FDB'].names:self.DB['FDB'].rebuild(file)
    def receive(self,payload,*,inner=False):
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
        self.text=ResizableOmniText(self.frame,scrolling=(0,1),minwidth=400,minheight=200,**kw)
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
            try:
                text=self.send()
                if not set(text).issubset({' ','\n'}):
                    self.table.load(DataFrame([['>'+i[0],*list(''.join(i[1:]))]for i in [[j for j in i.splitlines()if j]for i in text.split('>') if i]]).set_index(0).fillna(""),None)
            except Exception as E:showerror('Error!',str(E))
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
    def receive(self,payload,*,inner=False):
        self.text.delete(1.0,'end')
        self.text.insert(1.0,payload)
        self.syncttv()

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
        print(''.join(sorted(set(s))))
        constr+=nuc.get(''.join(sorted(set(s))),'?')
    return '\n>IUPAC%% Consensus %s\n%s'%(title,constr)
counter=1
def showfasta(payload,title=None):
    global counter
    root=Tk()#Toplevel(tk)
    root.title('FASTA Preview #%s'%counter)
    a=FastaWrapper(root,'FASTA Preview #%s'%counter,width=800,height=400)#,font=('Courier New',7))
    a.receive(payload)
    a.config(text=title)
    a.pack(fill='both',expand=True)
    radio.instance(a)
    counter+=1
                
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
        self.stopped=ToggleButton(self.top,text='Emergency STOP',border=4,bg='red',value=False)
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

def rebuild():
    io=askcustom('Rebuild GB2Taxid','''\
This operation will take significant time and disk space, cannot be paused (if cancelled, all progress will be lost)
and will make the computer unusable until database rebuild is completed.
If you want to continue, please make sure that:''',
                     (Group,[],{'title':'Checklist','widgets':{'1':(DBool,[],{'type':'check','default':False,'justify':'left','value':True,'prompt':'The computer has no scheduled restarts, is plugged in (if laptop) or has an UPS (if desktop)'}),
                      '2':(DBool,[],{'type':'check','default':False,'justify':'left','value':True,'prompt':'Other users are informed not to shut down or restart the computer. Sleep mode and hibernation are disabled.'}),
                      '3':(DBool,[],{'type':'check','default':False,'justify':'left','value':True,'prompt':'All other apps are closed and there are no background tasks running.'}),
                      '4':(DBool,[],{'type':'check','default':False,'justify':'left','value':True,'prompt':'There are no other users currently working on this computer in person or via remote connection'}),
                      '5':(DBool,[],{'type':'check','default':False,'justify':'left','value':True,'prompt':'There are no users planning to use this computer in the next 18-24 hours'}),
                      '6':(DBool,[],{'type':'check','default':False,'justify':'left','value':True,'prompt':'At least 24 GB of free disk space is available'}),
                      },'validate':all}))
    if False:
        from os import remove
        from os.path import getsize
        from zipfile import ZipFile
        print('loading...',end='')
        f=open('D:/SMB/taxonomy ncbi/nucl_gb.accession2taxid')
        print('done')
        f.read(38)
        if f.readline()=='accession\taccession.version\ttaxid\tgi\n':print('header')
        fl={}
        n=0
        print('processing...')
        while (l:=f.readline()):
            s=l.split('\t')
            if s[0][:2] not in fl:
                fl[s[0][:2]]=open('gb2taxid/'+s[0][:2],'w')
                fl[s[0][:2]].write(s[0]+';'+s[2]+'\n')
                fl[s[0][:2]].close()
            elif fl[s[0][:2]].closed:
                fl[s[0][:2]]=open('gb2taxid/'+s[0][:2],'a')
                fl[s[0][:2]].write(s[0]+';'+s[2]+'\n')
                fl[s[0][:2]].close()
            else:print('bruh')
            n+=1
            if n<1000000:
                if n<100000:
                    if n<10000:
                        if n<1000:
                            if n<100:
                                if n<10:print(n)
                                elif n%10==0:print(n)
                            if n%100==0:print(n)
                        if n%1000==0:print(n)
                    if n%10000==0:print(n)
                if n%100000==0:print(n)
            elif n%1000000==0:print(n)
        print('done')
        print('zipping...')
        z=ZipFile('gb2taxid/gb2taxid.zip','w',8)
        n=0
        l=len([*fl])
        for i in fl:
            z.write('gb2taxid/'+i,i)
            n+=1
            print(f'{n}/{l}')
        z.close()
        print('done')
        print('cleaning up...')
        for i in fl:remove('gb2taxid/'+i)
        print('done')


tk=Tk()
tk.withdraw()
tk.title('GeneProt marker gene/protein metagenomic sequencing data manipulation and ecological assessment expert system')# (GP MPGMSD DM&EAES)')
load=Toplevel(tk)
Label(load,text='Loading...').pack()

s=Style()
s.configure('TW2.TNotebook',tabposition='sw',tabmargins=0)

ui2=Notebook(tk)
ui2.pack(fill='both',expand=True)

page1=PanedWindow(ui2,orient='horizontal')
fasta=FastaWrapper(page1,'GeneProt',width=300)
table=TableWrapper(page1,'Table')
DB['db']=db=DatabaseProvider(tk)
DB['gb2taxid']=gb2tax=GB2TaxIdProvider(db)
gb2tax.rebuild=rebuild
DB['taxdump']=taxdump=TaxdumpProvider(db)
DB['FDB']=FDB=FASTAProvider(db)
mid=Middle(page1,table,fasta,online=online)
page1.add(table)
page1.add(mid)
page1.add(fasta)

page2=FastCons(tk,'FastCons',font=('Courier New',8),width=800,height=400)

if online:page3=Bulker(tk,'Very Large Bulk Downloader',width=800,height=400)
else:page3=Label(ui2,text='Package "bio" is unavailable!',width=80,height=30,relief='raised',state='disabled')

#tab2=TableWrapper2(ui2,'Excel test')
ui2.add(page1,text='GeneProt')
#ui2.add(tab2,text='EXCELlent')
ui2.add(page2,text='FastCons')
ui2.add(page3,text='VLB')
radio=Transceiver()
radio.instance(fasta)
radio.instance(page2)
radio.instance(FDB)

load.destroy()
tk.deiconify()
exec(open('deacftpo.py').read())
tk.mainloop()
