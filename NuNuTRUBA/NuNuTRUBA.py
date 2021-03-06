# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 12:10:49 2021

@author: Gözde

"""

from tkinter import *
from tkinter import messagebox 
import tkinter
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import *    
import tkinter as tk
import os
import scp
import paramiko



fields = 'KUYRUK', 'CPU SAYISI', 'GPU SAYISI','PİPS ', "PARAMETRELER", 'GİDEN DOSYALAR', "DÖNEN DOSYALAR"
works =  'Ip/Host Adı','Kullanıcı Adı','Şifre'
 
 
    
def fet2(entries):
    dosya = open("settings.ink","w",encoding="utf-8")
    for entry in entries:
        field = entry[0]
        text  = entry[1].get()
        dosya.write('%s\n' % (text))
        
            
           
def make2(root, works):
    sendentries = []
    b=0
    for work in works:
        
        row = tk.Frame(root)
        lab = tk.Label(row, width=15, text=work, bg="white", anchor='w')
    
        ent = tk.Entry(row)
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        lab.pack(side=tk.LEFT)
     
        ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        sendentries.append((work, ent))
        
    return sendentries    
            
    
def settings():
    root = tk.Tk()
    root.config(bg="white")
    root.title("   NuNuTRUBA")
   

    
    ents = make2(root, works)
    
    
    root.bind('<Return>', (lambda event, e=ents: fet2(e)))   
    b1 = tk.Button(root, text='KAYDET',  fg = "white",
      bg= "grey", command=(lambda e=ents: fet2(e)))
    b1.pack(side=tk.LEFT, padx=5, pady=5)
    b2 = tk.Button(root, text='ÇIKIŞ',   fg = "white",
      bg= "grey", command=root.destroy)
    b2.pack(side=tk.LEFT, padx=5, pady=5) 

    
     
     
     

def Enquiry(lis1): 
    if not lis1: 
        return 1
    else: 
        return 0
            
                
            
                  
def fetch(entries):
    name=open("filenamefortruba.ink","r")
    name.readline()
    filename=name.readline()
    filename=filename.rstrip()
    namejob=filename[0:-3]
    namejob=namejob+".job"
    pyfile=open(filename,"r")
    line=pyfile.readlines()
    lines=str(line)
    jobfile=open(namejob,"w",newline="\n")
    jobfile.write("#!/bin/bash") 
    b=0
    x=0
    for entry in entries:
        b=b+1
        field = entry[0]
        text  = entry[1].get()
        i=0
        newtext=[]                
        if(b==1):
            search=lines.find("#NuNuTRUBA_KUYRUK")
            search=search+18
            jobfile.write("\n#SBATCH -p ")
            if Enquiry(text):
                x=search
                while True:
                    jobfile.write(lines[search])
                    search=search+1
                    if(lines[search]==":"):                       
                        break
            else:
                jobfile.write(text)
        
        if(b==2):
            search=lines.find("#NuNuTRUBA_CPUSAYISI")
            search=search+21
            jobfile.write("\n#SBATCH -c ")
            if Enquiry(text):
                while True:
                    jobfile.write(lines[search])
                    search=search+1
                    if(lines[search]==":"):
                        break
            else:
                jobfile.write(text)
        if(b==3):
            jobfile.write("\n#SBATCH -J ")
            jobfile.write(namejob)
            search=lines.find("#NuNuTRUBA_GPUSAYISI")
            search=search+21
            jobfile.write("\n#SBATCH --gres=gpu:")
            if Enquiry(text):
                while True:
                    jobfile.write(lines[search])
                    search=search+1
                    if(lines[search]==":"):
                        break
            else:
                jobfile.write(text)
   
        if (b==4):
             jobfile.write("\n#SBATCH --time=00-02:00")
             #jobfile.write("\n#SBATCH --qos=normal")
             '''BU SATIR OLMAZSA MODULLER module: command not found hatası veriyor
             https://www.tchpc.tcd.ie/node/182'''

             jobfile.write("\n. /etc/profile.d/modules.sh")
             jobfile.write("\nmodule load centos7.3/comp/python/3.6.5-gcc")
             jobfile.write("\nmodule load centos7.3/lib/cuda/10.0")
           
             textstr=str(text)
             x=0
             search=lines.find("#NuNuTRUBA_PIP")
             search=search+15
             jobfile.write("\npip install --user ")
             if Enquiry(text):
                 while True:
                     jobfile.write(lines[search])
                     search=search+1
                     if(lines[search]==","):
                         jobfile.write("\npip install --user ")
                         search=search+1
                     if(lines[search]==":"):  
                          jobfile.write("\npython3 ")
                          jobfile.write(name)
                          jobfile.write(" ")
                          jobfile.write("${1}")
                          break
             else:
                 i=0
                 while True:
                     if(text[i]==","):
                         jobfile.write("\npip install --user ")
                         i=i+1
                     if(text[i]==":"):
                          jobfile.write("\npython3 ")
                          jobfile.write(name)
                          jobfile.write(" ")
                          jobfile.write("${1}")
                          break
                     jobfile.write(text[i])
                     i=i+1
                     
        if (b==5):
         name=open("filenamefortruba.ink","r")
         name.readline()
         filename=name.readline()
         filename=filename.rstrip()
         jobname=name.readline()
         jobname=jobname.rstrip()
         pyfile=open(filename,"r")
         line=pyfile.readlines()
         lines=str(line)   
         search=lines.find("#NuNuTRUBA_PARAMETRELER")
         search=search+24
         com=open("command.ink","w")
         com.write("sbatch ")
         com.write(jobname)
         com.write(" ")
         if Enquiry(text):
           while True:
            com.write(lines[search])
            search=search+1
            if(lines[search]==","):
                
                com.write(",sbatch ")
                com.write(jobname)
                com.write(" ")
                search=search+1
            if(lines[search]==":"):  
                     com.write(",:") 
                     break
         
         else:
             i=0
             while True:
               if text[i]==",":
                   com.write(",sbatch ")
                   com.write(jobname)
                   com.write(" ")
                   i=i+1
               com.write(text[i])  
               i=i+1
               if text[i]==":":
                   com.write(",:") 
                   break
        if(b==6):
            if Enquiry(text):
                 a=1
            else:    
             name=open("filenamefortruba.ink","r")
             read=name.readlines()[9:11]
             
             name=open("filenamefortruba.ink","r")
             lines=name.readlines()[0:8]
           
             name1=open("filenamefortruba.ink","w")
             for line in lines:
                 name1.write(line)
             name1.write("#NuNuTRUBA_GIDENDOSYALAR=")  
             name1.write(text)
             name1.write("\n")
             read=str(read)
             read=read.replace("[","")
             read=read.replace("'","")
             read=read.replace("]","")
             name1.write(read) 
             name1.close()
             
        if(b==7):
            if Enquiry(text):
                 a=1
            else:    
           
             name=open("filenamefortruba.ink","r")
             lines=name.readlines()[0:9]
           
             name1=open("filenamefortruba.ink","w")
             for line in lines:
                 name1.write(line)
             name1=open("filenamefortruba.ink","a")
             name1.write("#NuNuTRUBA_DONENDOSYALAR=")
             name1.write(text)
        if(b==8):
           if Enquiry(text):
               a=5
           else:    
            dosya=open("command.ink","a")
            dosya.write("\n")
            dosya.write(text)

                       
                     
                     

       


        
def output():
    import paramiko
    send=open("settings.ink","r")
    ilk=send.readline() 
    hostname=ilk.rstrip()
    
    ilk=send.readline()
    username=ilk.rstrip()
    
    ilk=send.readline() 
    password=ilk.rstrip()
    
    
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=hostname, username=username, password=password)
    except:
        print("[!] Cannot connect to the SSH Server")
    
    name=open("filenamefortruba.ink","r")
    line=name.readlines()
    lines=str(line)
    search=lines.find("#NuNuTRUBA_DONENDOSYALAR=")
    search=search+25
    i=search
    file=[]
    
    while True:
            search=search+1
            if(lines[search]==","):
                file=lines[i:search]
                from scp import SCPClient                     
                scp = SCPClient(client.get_transport())
                liste=['/truba','home',username,file]
                alinan='/'.join(liste)
                
                name=open("filenamefortruba.ink","r")
                adres=name.readline()
                adres=str(adres)   
                adres=adres[::-1]
                a=0
                while True:
                     a=a+1
                     if(adres[a]=="/"):
                         break
                adres=adres[a+1:]
                adres=adres[::-1]
                liste2=[adres,file]
                gelen='/'.join(liste2)
                scp.get(alinan,gelen)
                             
                i=search+1
                
            if(lines[search]==":"):  
                file=lines[i:search]
                from scp import SCPClient                     
                scp = SCPClient(client.get_transport())
                liste=['/truba','home',username,file]
                alinan='/'.join(liste)
                
                name=open("filenamefortruba.ink","r")
                adres=name.readline()
                adres=str(adres)   
                adres=adres[::-1]
                a=0
                while True:
                     a=a+1
                     if(adres[a]=="/"):
                         break
                adres=adres[a+1:]
                adres=adres[::-1]
                liste2=[adres,file]
                gelen='/'.join(liste2)
                scp.get(alinan,gelen)                    
                                      
                
                i=search+1
                        
                break
                
def commands(entries):
  for entry in entries:
   field = entry[0]
   text  = entry[1].get()
   if Enquiry(text):
    send=open("settings.ink","r")
    ilk=send.readline() 
    hostname=ilk.rstrip()
    
    ilk=send.readline()
    username=ilk.rstrip()
    
    ilk=send.readline() 
    password=ilk.rstrip()
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=hostname, username=username, password=password)
    except:
        print("[!] Cannot connect to the SSH Server")

    stdin,stdout,stderr = client.exec_command("sacct")
    sonuc = stdout.read()    
    aa=sonuc.decode("utf-8")
    lab=Label(root,text=aa, fg = "white",
           bg= "black",font = ("Courier New","11","normal")).place(x=100,y=550)
   else:    
    send=open("settings.ink","r")
    ilk=send.readline() 
    hostname=ilk.rstrip()
    
    ilk=send.readline()
    username=ilk.rstrip()
    
    ilk=send.readline() 
    password=ilk.rstrip()
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=hostname, username=username, password=password)
    except:
        print("[!] Cannot connect to the SSH Server")
    print(text)
    stdin,stdout,stderr = client.exec_command(text)
    sonuc = stdout.read()    
    aa=sonuc.decode("utf-8")
    lab=Label(root,text=aa, fg = "white",
           bg= "black",font = ("Courier New","11","normal")).place(x=100,y=550)

        
def makeform(root, fields):
    entries = []
    a=0
    dosyaname=open("filenamefortruba.ink","r")
    dosyaname.readline()
    dosyaname.readline()
    dosyaname.readline()
    for field in fields:
       row = tk.Frame(root)
       if a==0:
        text=dosyaname.readline()   
        text=str(text)
        b=len(text)
        text=text[19:b]
       if a==1:
        text=dosyaname.readline() 
        text=str(text)
        b=len(text)
        text=text[22:b]
       if a==2:
        text=dosyaname.readline() 
        text=str(text)
        b=len(text)
        text=text[22:b] 
       if a==3:
        text=dosyaname.readline() 
        text=str(text)
        b=len(text)
        text=text[15:b]  
       if a==4:
        text=dosyaname.readline() 
        text=str(text)
        b=len(text)
        text=text[24:b] 
       if a==5:
        text=dosyaname.readline() 
        text=str(text)
        b=len(text)
        text=text[25:b]
       if a==6:
        text=dosyaname.readline() 
        text=str(text)
        b=len(text)
        text=text[25:b]
      
       row = tk.Frame(root)
       lab = tk.Label(row, width=25, text=field, fg = "white",
       bg= "grey",font = ("Courier New","11","normal"),anchor='w')
       ent = tk.Entry(row)
       ent.insert(0,text)
       row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
       lab.pack(side=tk.LEFT)
       ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
       entries.append((field, ent))  
       a=a+1
    return entries

def send():
    import paramiko
    send=open("settings.ink","r")
    ilk=send.readline() 
    hostname=ilk.rstrip()
    
    ilk=send.readline()
    username=ilk.rstrip()
    
    ilk=send.readline() 
    password=ilk.rstrip()
    
    
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=hostname, username=username, password=password)
    except:
        print("[!] Cannot connect to the SSH Server")
    
        
           
    from scp import SCPClient           
    scp = SCPClient(client.get_transport())
    name=open("filenamefortruba.ink","r")
    adres1=name.readline()
    adres1=adres1.rstrip()
    adres2=adres1[0:-3]
    adres2=adres2+".job"
    
    filename=name.readline()
    filename=filename.rstrip()
    
    liste2=['/truba','home',username,filename]
    gonderilen='/'.join(liste2)
    scp.put(adres1, gonderilen)
 
    
    scp = SCPClient(client.get_transport())
    filename2=filename[0:-3]
    filename2=filename2+".job"
    liste2=['/truba','home',username,filename2]
    gonderilen='/'.join(liste2)
  
    scp.put(adres2, gonderilen)
   
    
    
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=hostname, username=username, password=password)
    except:
        print("[!] Cannot connect to the SSH Server")
    
    name=open("filenamefortruba.ink","r")
    line=name.readlines()
    lines=str(line)
    search=lines.find("#NuNuTRUBA_GIDENDOSYALAR=")
    search=search+25
    i=search
    file=[]
    yok=search

           
    if(lines[yok]!=":"):           
      while True:
            search=search+1

            if(lines[search]==","):
                file=lines[i:search]
                liste=['/truba','home',username,file]
                host='/'.join(liste) 
                
                name=open("filenamefortruba.ink","r")
                adres=name.readline()
                adres=str(adres)   
                adres=adres[::-1]
                a=0
                while True:
                     a=a+1
                     if(adres[a]=="/"):
                         break
                adres=adres[a+1:]
                adres=adres[::-1]
                liste2=[adres,file]
                local='/'.join(liste2)
                from scp import SCPClient                     
                scp = SCPClient(client.get_transport())
              
                scp.put(local,host)
                i=search+1
           
            if(lines[search]==":"):  
                file=lines[i:search]
                from scp import SCPClient                     
                scp = SCPClient(client.get_transport())
                liste=['/truba','home',username,file]
                host='/'.join(liste)
                
                name=open("filenamefortruba.ink","r")
                adres=name.readline()
                adres=str(adres)   
                adres=adres[::-1]
                a=0
                while True:
                     a=a+1
                     if(adres[a]=="/"):
                         break
                adres=adres[a+1:]
                adres=adres[::-1]
                liste2=[adres,file]
                local='/'.join(liste2)
                scp.put(local,host)
                
                i=search+1
                        
                break
             
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=hostname, username=username, password=password)
    except:
        print("[!] Cannot connect to the SSH Server")

    root = tk.Tk()
    name=open("filenamefortruba.ink","r")
    readcom=open("command.ink","r")
    commands=readcom.readlines()
    command=str(commands)
    
    i=2
    a=2
    while True:
        i=i+1
        if(command[i]==","):
            sendcommand=command[a:i] 
            stdin,stdout,stderr = client.exec_command(sendcommand)
            sonuc = stdout.read()
            metin=sonuc.decode("utf-8")
            lab=Label(root,text=metin).pack()
            a=i+1
        if(command[i]==":"):
       
            break
    
def file():
    root = tk.Tk()
    root.title("   NuNuTRUBA")
    root.geometry("800x800")
    root.config(bg="white")
    filename=tkinter.filedialog.askopenfilename()
   
    namefile=open("filenamefortruba.ink","w")
    namefile.write(filename)
    namefile.write("\n")
    
    name=os.path.basename(filename)    
    namefile.write(name)
    namefile.write("\n")
    
    namejob=name[0:-3]
    namejob=namejob+".job"
    jobname=namejob
    jobfile=open(namejob,"w",newline="\n")
    namefile.write(namejob)
    
    if os.path.getsize(name)==0:
        fileempty=open(name,"w")
        fileempty.write("#NuNuTRUBA_KUYRUK=short:\n")
        fileempty.write("#NuNuTRUBA_CPUSAYISI=4:\n")
        fileempty.write("#NuNuTRUBA_GPUSAYISI=1:\n")
        fileempty.write("#NuNuTRUBA_PIP=numpy,sys:\n")
        fileempty.write("#NuNuTRUBA_PARAMETRELER=1,2,3:\n")
        fileempty.write("#NuNuTRUBA_GIDENDOSYALAR=:\n")
        fileempty.write("#NuNuTRUBA_DONENDOSYALAR=:\n")
        fileempty.close()
        
        
    pyfile=open(name,"r")
    line=pyfile.readlines()
    lines=str(line)
    edit=open(name,"a")
    jobfile.write("#!/bin/bash\n")
    

    
    if(lines.find('#NuNuTRUBA_KUYRUK')==-1):
        edit.write("#NuNuTRUBA_KUYRUK=short:\n")  
        
    if(lines.find('#NuNuTRUBA_CPUSAYISI')==-1):
        edit.write("#NuNuTRUBA_CPUSAYISI=4:\n")
        
    if(lines.find('#NuNuTRUBA_GPUSAYISI')==-1):
        edit.write("#NuNuTRUBA_GPUSAYISI=1:\n")
        
    if(lines.find('#NuNuTRUBA_PIP')==-1):
        edit.write("#NuNuTRUBA_PIP=numpy,sys:\n")
        
    if(lines.find('#NuNuTRUBA_PARAMETRELER')==-1):
        edit.write("#NuNuTRUBA_PARAMETRELER=1,2,3:\n")
        
    if(lines.find('#NuNuTRUBA_GIDENDOSYALAR')==-1):
        edit.write("#NuNuTRUBA_GIDENDOSYALAR=:\n")
        
    if(lines.find('#NuNuTRUBA_DONENDOSYALAR=')==-1):
        edit.write("#NuNuTRUBA_DONENDOSYALAR=:\n")     
    edit.close()
   

    pyfile=open(name,"r")
    line=pyfile.readlines()
    lines=str(line)
    search=lines.find("#NuNuTRUBA_KUYRUK")
    namefile.write("\n#NuNuTRUBA_KUYRUK =")
    search=search+18
    jobfile.write("#SBATCH -p ")
    while True:
        namefile.write(lines[search])
        jobfile.write(lines[search])
        search=search+1
        if(lines[search]==":"):
            break
      
    search=lines.find("#NuNuTRUBA_CPUSAYISI")
    namefile.write("\n#NuNuTRUBA_CPUSAYISI =")
    search=search+21
    jobfile.write("\n#SBATCH -c ")
    while True:
        namefile.write(lines[search])
        jobfile.write(lines[search])
        search=search+1
        if(lines[search]==":"):
            break
    jobfile.write("\n#SBATCH -J ")
    namejob=name[0:-3]
    jobfile.write(namejob)
    search=lines.find("#NuNuTRUBA_GPUSAYISI")
    namefile.write("\n#NuNuTRUBA_GPUSAYISI =")
    search=search+21
    jobfile.write("\n#SBATCH --gres=gpu:")
    while True:
        namefile.write(lines[search])
        jobfile.write(lines[search])
        search=search+1
        if(lines[search]==":"):
            break
    jobfile.write("\n#SBATCH --time=00-02:00")
    #jobfile.write("\n#SBATCH --qos=normal")
    '''BU SATIR OLMAZSA MODULLER module: command not found hatası veriyor
    https://www.tchpc.tcd.ie/node/182'''
    jobfile.write("\n. /etc/profile.d/modules.sh")
             
    jobfile.write("\nmodule load centos7.3/comp/python/3.6.5-gcc")
    jobfile.write("\nmodule load centos7.3/lib/cuda/10.0")
    
    search=lines.find("#NuNuTRUBA_PIP=")
    search=search+15
    namefile.write("\n#NuNuTRUBA_PIP=")
    jobfile.write("\npip install --user ")
    while True:
            namefile.write(lines[search])
            jobfile.write(lines[search])
            search=search+1
            if(lines[search]==","):
                namefile.write(",")
                jobfile.write("\npip install --user ")
                search=search+1
            if(lines[search]==":"):  
                    namefile.write(lines[search])
                    break
        

    search=lines.find("#NuNuTRUBA_PARAMETRELER")
    search=search+24
    namefile.write("\n#NuNuTRUBA_PARAMETRELER=")
    com=open("command.ink","w")
    com.write("sbatch ")
    com.write(jobname)
    com.write(" ")
    while True:
            namefile.write(lines[search])
            com.write(lines[search])
            search=search+1
            if(lines[search]==","):
                namefile.write(",")
                com.write(",sbatch ")
                com.write(jobname)
                com.write(" ")
                search=search+1
            if(lines[search]==":"): 
                 namefile.write(lines[search])
                 break
    com.write(",:")  
    jobfile.write("\npython3 ")
    jobfile.write(name)
    jobfile.write(" ")
    jobfile.write("${1}")
    search=lines.find("#NuNuTRUBA_GIDENDOSYALAR=")
    namefile.write("\n#NuNuTRUBA_GIDENDOSYALAR=")
    search=search+25
    while True:
            if(lines[search]==":"):
                namefile.write(lines[search])
                break
            namefile.write(lines[search])
            search=search+1
            if(lines[search]==","):
                namefile.write(",")
                search=search+1
            if(lines[search]==":"):  
                    namefile.write(lines[search])
                    break
    search=lines.find("#NuNuTRUBA_DONENDOSYALAR=")
    namefile.write("\n#NuNuTRUBA_DONENDOSYALAR=")
    search=search+25
    while True:
            if(lines[search]==":"):
                namefile.write(lines[search])
                break
            namefile.write(lines[search])
            search=search+1
            if(lines[search]==","):
                namefile.write(",")
                search=search+1
            if(lines[search]==":"):  
                    namefile.write(lines[search])
                    break
                
    lab1=Label(root,text="GİRİLEN BİLGİLER").place(x=100,y=1)          
    namefile=open("filenamefortruba.ink","r")
    lines=namefile.readlines()[3:14]
    lines=str(lines)

    lines=lines.replace(",","\n")
    lines=lines.replace("'"," ")
    lines=lines.replace("["," ")
    lines=lines.replace("]"," ")
    lab1=Label(root,text=lines).place(x=100,y=25)
    namefile.readline()
    namefile.readline()
    lab1=Label(root,text="             ").pack()
    lab1=Label(root,text="").pack() 
    lab1=Label(root,text="").pack()     
    lab1=Label(root,text="").pack() 
    lab1=Label(root,text="").pack() 
    lab1=Label(root,text="").pack()     
    lab1=Label(root,text="").pack() 
    lab1=Label(root,text="").pack() 
    lab1=Label(root,text="").pack() 
    lab1=Label(root,text="").pack() 
    lab1=Label(root,text="").pack()     
    lab1=Label(root,text="").pack()     
    lab1=Label(root,text="").pack()     
    lab1=Label(root,text="             ").pack()     
 
    
   
    
    lab1=Label(root,text="JOB DOSYASI").place(x=500,y=1)    
    namefile=open("filenamefortruba.ink","r")
    namefile.readline()
    namefile.readline()
    jobname=namefile.readline()
    jobname=jobname.rstrip()
    jobfile=open(jobname,"r")

    lines=jobfile.readlines()
    lines=str(lines)
    lines=lines.replace(",","\n")
    lines=lines.replace("'"," ")
    lines=lines.replace("["," ")
    lines=lines.replace("]"," ")
    lab1=Label(root,text=lines).place(x=500,y=25)
    
    ents = makeform(root, fields)        
    


    
    
    root.bind('<Return>', (lambda event, e=ents: fetch(e)))   
    b1 = tk.Button(root, text='DÜZENLE',  fg = "white",
      bg= "grey", command=(lambda e=ents: fetch(e)))
    b1.pack(side=tk.LEFT, padx=5, pady=5)
   
    
    b2 = tk.Button(root, text='GÖNDER',   fg = "white",
      bg= "grey", command=send)
    b2.pack(side=tk.LEFT, padx=5, pady=5)  
    
    
    
    b1.pack(side=tk.LEFT, padx=5, pady=5) 
    b2 = tk.Button(root, text='ÇIKTI',   fg = "white",
      bg= "grey", command=output)
    b2.pack(side=tk.LEFT, padx=5, pady=5)  
    
   
    
     
    b2 = tk.Button(root, text='ÇIKIŞ',   fg = "white",
      bg= "grey", command=root.destroy)
    b2.pack(side=tk.LEFT, padx=5, pady=5) 
    
def commake(root):
        komentries = []

        ent = tk.Entry(root)
        
        ent.place(x=560,y=210)
        komentries.append(("KOMUT", ent))

        try:
            send=open("settings.ink","r")
            ilk=send.readline() 
            hostname=ilk.rstrip()
    
            ilk=send.readline()
            username=ilk.rstrip()
        
            ilk=send.readline() 
            password=ilk.rstrip()
    
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=hostname, username=username, password=password)
            stdin,stdout,stderr = client.exec_command("sacct")
            sonuc = stdout.read()    
            aa=sonuc.decode("utf-8")
            lab=Label(root,text=aa, fg = "white",
            bg= "black",font = ("Courier New","11","normal")).place(x=100,y=550)
        except:
            print("[!] Cannot connect to the SSH Server")


        return komentries    
    

root=Tk()
root.title("   NuNuTRUBA")

root.config(bg="black")
foto=PhotoImage(file="ekran.png")
yazı = Label(root,image= foto).pack()
yazı = Label(root,text = "NuNuTRUBA", 
             fg = "white", 
             bg= "black",
             font = ("Harrington","40","italic","bold"),
            padx=30,
            pady=30).place(x=470,y=40)
start=tkinter.Button(root, 
      text="TRUBA GİRİŞ",
      command = file ,
      fg = "white",
      bg= "black",
      font = ("Courier New","19","bold"),
      padx=15,
      pady=15).place(x=560,y=240)

setting=tkinter.Button(root, 
      text="AYARLAR",
      command=settings,
      fg = "white",
      bg= "black",
      font = ("Courier New","19","bold"),
      padx=15,
      pady=15).place(x=590,y=330)

buton2=tkinter.Button(root, 
      text="ÇIKIŞ",
      command = root.destroy,
      fg = "white",
      bg= "black",
      font = ("Courier New","19","bold"),
      padx=15,
      pady=15).place(x=605,y=420)

ents=commake(root)

root.bind('<Return>', (lambda event, e=ents: commands(e)))   
b1 = tk.Button(root, text='KOMUT',  fg = "pink",
      bg= "black",font = ("Courier New","12"), command=(lambda e=ents: commands(e)))
b1.place(x=710,y=200)               
 

root.mainloop()
