#input file format should be <arrival time> <process id> <cpu burst> and should be stable sorted increasingly with arrival time, and same arrival time rows should be sorted increasingly according to process id
#
#should be called from terminal as follows
#  enter directory
#  python <this file name>.py <input file name>
#
#output will be 4 text files
#pid finish_time waiting_time turnaround_time
#sorted in increasing process id

import sys

class Scheduler():
    def __init__(self,name,inpt):
        self.filename=inpt
        self.name=inpt+'_'+name
        self.time=-1
        self.qtime=-1
        self.waitqueue=[]
        self.ol=[]
        self.firstline=True

    def splitline(self,line):
        return (int(line.split(' ',3)[0]),int(line.split(' ',3)[1]),int(line.split(' ',3)[2]))

    def app(self,x):
        self.waitqueue.append(x)

    def output(self,x):
        self.ol=self.insert(self.ol,x)

    def writetofile(self):
        fh = open(self.name+".txt", "w")
        for i in self.ol:
            fh.write(i[1])
        fh.close()

    def settime(self,a,c):
        self.time=max(self.time,a)
        self.time+=c

    def out(self,pid,arr_t,cpub):
        self.settime(arr_t,cpub)
        ft=self.time
        wt,tt = ft-arr_t-cpub,ft-arr_t
        self.output((pid,str(pid)+' '+str(ft)+' '+str(wt)+' '+str(tt)+'\n'))

    def out2(self,pid,arr_t,cpub,rq):
        self.settime(arr_t,rq)
        ft=self.time
        wt,tt = ft-arr_t-cpub,ft-arr_t
        self.output((pid,str(pid)+' '+str(ft)+' '+str(wt)+' '+str(tt)+'\n'))

    def wtq_empty(self):
        if self.waitqueue==[]:
            return True
        return False

    def insert(self,l,p):
        if l==[]:
            l=[p]
            return l
        if l[-1][0]<p[0]:
            l.append(p)
            return l
        if l[0][0]>p[0]:
            l=[p]+l
            return l
        for i in range(0,len(l)):
            if l[i][0]>p[0]:
                l=l[:i]+[p]+l[i:]
                return l

    def find_sjf(self):
        mincpub=self.waitqueue[0][2]
        minj=self.waitqueue[0]
        minpid=self.waitqueue[0][1]
        for x in self.waitqueue:
            (a,p,b) = (x[0],x[1],x[-1])
            if b<mincpub:
                mincpub=b
                minj=x
                minpid=p
            if b==mincpub and p<minpid:
                mincpub=b
                minj=x
                minpid=p

        return minj

def sch(rro,ppbool,pushback,choice_first,pre_codn):
    firstline=True
    fo = open(rro.filename, "r+")

    if(ppbool):
        cur_p=None
        cft=-1
        p_to_app=False

    for line in fo:
        if(rro.firstline):
            if(pushback):
                rro.qtime=int(line)
                rro.firstline=False
            else:
                rro.qtime=None
                rro.firstline=False
            continue

        arr_t,pid,cpub = rro.splitline(line)

        if(rro.time==-1):
            rro.time=arr_t

        if(ppbool):
            if(p_to_app):
                (ca,cpid,ccb,crt)=cur_p
                if(cft==rro.time and arr_t>=rro.time):
                    rro.app(cur_p)
                    p_to_app=False

        if(rro.wtq_empty()):
            if(pushback):
                rro.app((arr_t,pid,cpub,cpub))
                rro.settime(arr_t,0)
            else:
                rro.app((arr_t,pid,cpub))
            
        else:
            prevline=rro.waitqueue[-1]
            if(arr_t==prevline[0] or rro.time>=arr_t):
                if(pushback):
                    rro.app((arr_t,pid,cpub,cpub))
                else:
                    rro.app((arr_t,pid,cpub))
            else:
                while(rro.time<arr_t):
                    if(rro.wtq_empty()):
                        rro.time=arr_t
                        break

                    if(choice_first):
                        x = rro.waitqueue[0] #fcfs and r
                    else:
                        x = rro.find_sjf()
                    if(pushback):
                        (at,pi,cb,rt)=x
                    else:
                        (at,pi,cb)=x

                    if(not pushback):
                        rro.waitqueue.remove((at,pi,cb))
                        rro.out(pi,at,cb)
                    else:
                        if(pre_codn=='qtime'):
                            qt=rro.qtime
                        elif(pre_codn=='nextp'):
                            qt=arr_t - rro.time

                        if(rt<=qt):
                            rro.waitqueue.remove((at,pi,cb,rt))
                            rro.out2(pi,at,cb,rt)

                        else:
                            rro.settime(at,qt)
                            indx=rro.waitqueue.index((at,pi,cb,rt))
                            rro.waitqueue[indx]=(at,pi,cb,rt-qt)
                            if(ppbool):
                                cur_p=rro.waitqueue.pop(0)
                                if(rro.time<=arr_t):
                                    rro.app(cur_p)    
                                else:
                                    p_to_app=True
                                    cft=rro.time               

                if(pushback):
                    rro.app((arr_t,pid,cpub,cpub))
                else:
                    rro.app((arr_t,pid,cpub))
    if(ppbool):
        if(p_to_app):
            rro.app(cur_p)

    while(not rro.wtq_empty()):
        if(choice_first):
            x = rro.waitqueue[0] #fcfs and r
        else:
            x = rro.find_sjf()
        if(pushback):
            (at,pi,cb,rt)=x
        else:
            (at,pi,cb) = x

        if(not pushback):
            rro.waitqueue.remove((at,pi,cb))
            rro.out(pi,at,cb)
        else:
            if(pre_codn=='qtime'):
                qt=rro.qtime
            elif(pre_codn=='nextp'):
                qt=rro.time+rt

            if(rt<=qt):
                rro.waitqueue.remove((at,pi,cb,rt))
                rro.out2(pi,at,cb,rt)

            else:
                rro.settime(at,qt)
                indx=rro.waitqueue.index((at,pi,cb,rt))
                rro.waitqueue[indx]=(at,pi,cb,rt-qt)
                if(choice_first):
                    y=rro.waitqueue.pop(indx)
                    rro.app(y)
 
    fo.close()

def main(filename):
    # 4 parameters
    # 1(bool) - whether there is a requirement of pre-empted process to be put at end of queue
    # 2(bool) - is there an pre_emption
    # 3(bool) - While choosing next process do we take the first element of the queue
    # 4(string) - pre_emption condition, Will be None for nin preempted schedulers
    fcfso=Scheduler("FCFS",filename)
    sch(fcfso,False,False,True,None)
    fcfso.writetofile()

    sjfo=Scheduler("SJF",filename)
    sch(sjfo,False,False,False,None)
    sjfo.writetofile()

    rro=Scheduler("RR",filename)
    sch(rro,True,True,True,'qtime')
    rro.writetofile()

    srtfo=Scheduler("SRTF",filename)
    sch(srtfo,False,True,False,'nextp')
    srtfo.writetofile()

filename=sys.argv[1]
main(filename)
#for i in range(1,11):
#    main("input"+str(i))










