from pandas import DataFrame
from math import log,e
__all__=['ops','isnan','isnum']
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
def isnan(a):return int(a==NaN)

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
ISNAN=feval(lambda a:DataFrame([isnan(a[i])for i in range(len(a))]))
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

ops={'Compare':None,
     '[I1] = [I2]':EQ,'[I1] ≠ [I2]':NE,'[I1] < [I2]':LT,'[I1] ≤ [I2]':LE,'[I1] > [I2]':GT,'[I1] ≥ [I2]':GE,
     'Logic':None,
     'NOT [I1]':NOT,'BOOL [I1]':BOOL,
     '[I1] AND [I2]':AND,'[I1] NAND [I2]':NAND,'[I1] OR [I2]':OR,'[I1] NOR [I2]':NOR,'[I1] XOR [I2]':XOR,'[I1] XNOR [I2]':XNOR,
     'Typechecking':None,
     'ISERROR([I1])':ISNAN,'ISNUMBER([I1])':ISNUMBER,'ISTEXT([I1])':ISTEXT,'ISEMPTY([I1])':ISEMPTY,
     'Math':None,
     '[I1] + [I2]':PLUS,'- [I1]':NEG,'[I1] - [I2]':MINUS,'[I1] * [I2]':MUL,'[I1] / [I2]':DEL,'[I1] ^ [I2]':POW,'√ [I1]':SQRT,
     'EXP([I1])':EXP,'LOG2 [I1]':LOG2,'LN [I1]':LOGE,'LOG10 [I1]':LOG10,
     'Manipulate':None,
     'IF [I1] THEN [I2] ELSE [I3]':lambda a,b,c:DataFrame([i[1]if bool(i[0])else i[2]for i in zip(a,b,c)]),
     'CONCAT([I1]; [I2])':CONCAT,'CONCAT([I1];" ";[I2])':CONCAT2,
     }
