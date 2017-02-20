#!/usr/bin/python
#filename md5_part1.py

''' python script for files integrity checking procedure'''

#note: the register and the log file are connected: if log file is missing it is mandatory delete the register
from time import sleep #sleep is used just for my personal taste in user interaction
from time import strftime #used to collect date and time info
import os #used for moving inside folders trees
import hashlib #import functionalitis for the hash
from collections import namedtuple #allows make a "vector of classes" (similar to C programming vector of structures)

global Vector_struct; #varaible used for collect data from register and therefore check it and re-print it on the register
Vector_struct=[];

class Path(): #exception handler class on user-comand line input (mainly used for register and pool path)
    def check(self,stringa):
        try:
            posix = raw_input("provide the path for the {} directory  ".format(stringa));
        except EOFError:
            print "EOF error!"
            exit();
        except KeyboardInterrupt:
            print "Good bye!";
            sleep(1);
            exit();
        try:
            list1 = os.listdir(posix)
        except IOError:
            print "You don't have required privileges for '{}' , program alt!".format(posix);
            sleep(1);
            exit();
        except OSError:
            print "The path '{}' is not valid, program alt!".format(posix);
            sleep(1);
            exit();
        return(posix);

class log_and_alert():#class that manage the logging procedure
    def mex(self,stringa,posix,flag=0):#the flag variable allows to just update the log file (default: flag=0) or create a new and empty log file (flag=1)
                                        #this class manage also problem related to log file missing or other type of errors (like unvalid path)
        if flag==0:
            try:
                f=open(posix+os.sep+"Ingrity_log.txt","r")
            except IOError or OSError:
                print "log file missing, program alt!"
                sleep(1);
                exit();
            f.close();
            f=open(posix+os.sep+"Ingrity_log.txt","a")
            f.write(stringa);
            f.write("\n");
            f.close();
        else:
            try:
                f=open(posix+os.sep+"Ingrity_log.txt","w")
            except IOError or OSError:
                print "something gones wrong during the creation of the log file, program alt!"
                sleep(1);
                exit();
            f.write(stringa);
            f.write("\n");
            f.close();

class structura(): #single element of the list for manage register info ->one element=one line on the register
    def __init__(self, filename, hash, C_date, C_time, Last_date, Last_time, Status):
        self.filename=filename;
        self.hash=hash;
        self.C_date=C_date; #creation date
        self.C_time=C_time; #creation time
        self.Last_date=Last_date; #last check date (equal to creation one in case of new register)
        self.Last_time=Last_time; #last check time (equal to creation one in case of new register)
        self.Status=Status; #it takes OK if last check provide a match of hashes or fail in the other case // NOTE: the population of the register is considered a check
        self.sign=0;#it takes different alternate values (0 or 1) for each check, it allows to discover if a file is missing ->in any check the script switch the value...who didn't switch is for sure missing

class Hasher():#class that manage the hashing procedure
    def __init__(self, target, target_list):
        self.target=target;
        self.list=target_list;
        self.structure={};
    def hashing_p(self, name): #method that carry the hashing of a SINGLE file (reminder:hasing is a function that act one byte at time
        BLOCKSIZE = 65536
        hash_sup=hashlib.md5();
        os.chdir(target)
        afile=open(name,'rb')
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hash_sup.update(buf)
            buf = afile.read(BLOCKSIZE)
        h_sup=hash_sup.hexdigest();
        afile.close();
        return h_sup;
    def hashing(self,flag=0):# manage the hashing of a file set (in the case of flag=1 it is a single file hash --->
                             #like other method (it is possible cut it of this part of the code by directly call the other method
        if flag==0:
            for i in self.list: #select one filename at time from the set provided
                print"I am hashing {}".format(i);
                self.structure[i]=self.hashing_p(i);
            #print self.structure;
            return self.structure;
        else:
            #print"eseguo ",self.list
            self.structure=self.hashing_p(self.list);
            return self.structure;

class Register():#class that manage any operation on the register
    def __init__(self, posix, R_name="Register.txt",filename="",hash_str=0):
        self.posix=posix;
    def Creation(self): #simple creation of register (empty), creation and update of log file and several exception handlers
        os.chdir(posix);
        try:
            f=open(posix+os.sep+R_name,"w");
        except OSError:
                print "something gones wrong during the creation of the register, program alt!"
                sleep(1);
                exit();
        f.close();
        Obj_log=log_and_alert()
        Obj_log.mex("Register creation {}".format(strftime("%d/%m/%Y  %H:%M:%S")), posix,1)
        Obj_log.mex("#######################################",posix);
        del Obj_log;
    def Population(self,info): #populate the register with lines (format filename-hash-data_time_ofcreation-
                               # data_time_last_check (equal to creation one in this case)-Status (OK in this case)
                               #it also provide exception handlers and log of the update procedure
        self.info=info
        #print info;
        os.chdir(posix);
        try:
            f=open(R_name,"w");
        except OSError:
            print "There is not any register file here, program alt!"
            sleep(1);
            exit();
        status="OK"
        for ck in info:
            #print ck+" ",info[ck];
            when=strftime("%d/%m/%Y %H:%M:%S");
            #print when
            str_write=ck+"  "+info[ck]+"    "+when+"    "+when+"    "+status+"\n";
            f.write(str_write);
        f.close()
        Obj_log=log_and_alert()
        Obj_log.mex("\n Register UPDATE {}".format(strftime("%d/%m/%Y  %H:%M:%S")), posix)
        Obj_log.mex("----------------------------------------",posix);
        del Obj_log;

    def Scan(self):#scan and save any data inside a vector of "structured variables" (Vector:Vector_struct -single element:structura)
        try:
            f=open(posix+os.sep+R_name,"r")
        except IOError or OSError:
            print "something gones wrong during the register reading (register missing), program alt!"
            sleep(1);
            exit();
        i=-1;
        scanned_reg=namedtuple("filename","hash C_date C_time Last_date Last_time Status");
        while True:
            i=i+1;
            line= f.readline();
            if len(line)==0:
                break;
            s_l=line.split(None,7)
            #print s_l;
            Vector_struct.append(structura(s_l[0],s_l[1],s_l[2],s_l[3],s_l[4],s_l[5],s_l[6]));
        return Vector_struct

    def Check(self,target):
        Obj_log=log_and_alert()
        Obj_log.mex("\nBegin of a check procedure at {}".format(strftime("%d/%m/%Y  %H:%M:%S")), posix)
        Obj_log.mex("----------------------------------------",posix);
        target_lst = os.listdir(target);
        reference_sign=Vector_struct[0].sign;#usefull to understand which file is no more here.
        if reference_sign==0:######Possibile exception da gestire
             reference_sign=1;
        else:
             reference_sign=0;
        for i in target_lst: # in order to hand anytype of variation of files set
            Obj_hash = Hasher(target,i)#possible improvement: create and del a class in a for it's not so smart...
            target_hash = Obj_hash.hashing(2);
            del Obj_hash;
            flag=0; #to flag if i found the file ---->no file missing
            for ck in range (0,len(Vector_struct)):
                if Vector_struct[ck].filename!=i : #skip the code if the filename is not matching
                    continue
                flag=1;
                Vector_struct[ck].sign=reference_sign; #update of the sign -> check class structura() for the meaning
                if Vector_struct[ck].Status=="OK":
                    if Vector_struct[ck].hash==target_hash: #if the hash stored and current hash match: the file was not modified
                                                            #just update of the last successfull check
                        Vector_struct[ck].Last_date=strftime("%d/%m/%Y");
                        Vector_struct[ck].Last_time=strftime("%H:%M:%S");
                    else: #dismatch of hashes-> integrity failure->update last check and status
                        Vector_struct[ck].Last_date=strftime("%d/%m/%Y");#Comming soon:save the previous successful check date in order to
                        Vector_struct[ck].Last_time=strftime("%H:%M:%S");#provide a narrow window for the forensic
                        Vector_struct[ck].Status="FAIL";
                        Alert_str="ALERT: The integrity of ' {} ' was dectected compromised at {} !!!!".format(Vector_struct[ck].filename,strftime("%d/%m/%Y  %H:%M:%S"))
                        print Alert_str;
                        Alert_str=Alert_str;
                        Obj_log=log_and_alert() #login of the failure
                        Obj_log.mex(Alert_str, posix);#POSSIBLE improvement: use just one class and not create it for any log operation
                        del Obj_log;
                else:
                    print "Reminder: ",Vector_struct[ck].filename+" was modified!"#When in the register there is an old fail, it is not checked again
                break;
            if flag!=1:#new file to check ->update of the register
                Vector_struct.append(structura(i,target_hash,strftime("%d/%m/%Y"),strftime("%H:%M:%S"),strftime("%d/%m/%Y"),strftime("%H:%M:%S"),"OK"));
                Vector_struct[len(Vector_struct-1)].sign=reference_sign;
        for i in range(0,len(Vector_struct)): #check of any file in register but not in the folder anymore
            if Vector_struct[i].sign!=reference_sign:
                Vector_struct[i].sign=reference_sign;
                Alert_str="ALERT: '{}' is no more available in date {}!".format(Vector_struct[i].filename, strftime("%d/%m/%Y  %H:%M:%S"));
                print Alert_str;
                Alert_str=Alert_str+"/n";
                Obj_log=log_and_alert()
                Obj_log.mex(Alert_str, posix);
                del Obj_log;
        os.chdir(posix);
        f=open(R_name,"w");
        for i in range(0,len(Vector_struct)):
            str_write=Vector_struct[i].filename+" "+Vector_struct[i].hash+" "+Vector_struct[i].C_date+" "+Vector_struct[i].C_time+" "+Vector_struct[i].Last_date+" "+Vector_struct[i].Last_time+" "+Vector_struct[i].Status+"\n";
            f.write(str_write);
        f.close()

#-----------------------------------main-----------------------------------#
R_name="Register.txt"
flag=1
while flag==1:
    try: #enforcement of the input (and exception handler)
        line = raw_input("Do u want create/update the register or check the integrity?[R for update the register, I for checking]\n");
        if line=='R' or line=='r' or line=='I' or line =='i':
            flag=0;
    except EOFError:
        print "EOF error!"
        exit();
    except KeyboardInterrupt:
        print "Good bye!";
        sleep(1);
        exit();

if line == "R" or line=='r': #Procedure for the new register creation
    while True:
        Obj_path= Path()
        posix=Obj_path.check("register");#acquire (and check) the path for the register
        list1 = os.listdir(posix);
        Obj_reg = Register(posix);
        if not(R_name in list1):
            print "Register creation..."
            Obj_reg.Creation();
        target = Obj_path.check("target");#acquire (and check) the path of the target set of files (pool)
        if target != posix:
            break;
        else:
            print "target and register directories must be diffferent!"
    target_list = os.listdir(target);#collect the list of filenames for the integrity check
    #print "target ",target
    #print target_list
    Obj_hash = Hasher(target,target_list)
    structure = Obj_hash.hashing();#hashing of the list of files
    Obj_reg.Population(structure); #population of the register
    del Obj_reg;
    del Obj_hash;
    del structure;
    del Obj_path;
elif line == "I" or line== "i":#check procedure
    Obj_path= Path()
    posix=Obj_path.check("register");#acquire (and check) the path for the register
    list1 = os.listdir(posix);
    Obj_reg = Register(posix);
    list1 = os.listdir(posix);
    #Obj_reg = Register(posix);
    Obj_reg.Scan();
    target = Obj_path.check("target");#acquire (and check) the path of the target set of files (pool)
    Obj_reg.Check(target);
    del Obj_reg;
    del Obj_path;







