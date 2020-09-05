
import speech_recognition as sr
import webbrowser as wb
import pyttsx3
import os
from os.path import join
import csv
import random as rng
import nltk
import time
import tkinter as Tk
from tkinter.filedialog import askopenfilename 
from nltk.tokenize import word_tokenize
nltk.download('punkt')
#load mind
path = "Z:\School\Intelligent SYS\Hermes"
if not(os.path.isfile("mind.txt")):
    g = rng.randint(0,2)
    if g == 1:
        g = 'M_Names.txt'
    elif g == 0:
        g = 'F_Names.txt'
    else:
        g = 'N_Names.txt'
    hermes_actual = (rng.choice(list(open(g))))
    M = open("mind.txt",'w')
    M.close()
    with open("mind.txt",'a') as w:
        w.write("Name:"+hermes_actual)
    with open("mind.txt",'a') as w:
        w.write("Gender:"+g.replace('_Names.txt',''))
#load voicebox
engine = pyttsx3.init()
engine.setProperty('rate',130)
g = ''
with open('mind.txt','r') as r:
    for line in r:
        if "Gender:" in line:
            g = line.replace('Gender:','')
        if g == 'F':
            engine.setProperty('voice','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
#load speech listener
r = sr.Recognizer()
mic = sr.Microphone(device_index=1)
#load name
nm = ['','']
with open('mind.txt','r') as r:
    for line in r:
        if 'Name2:' in line:
            nm[1] = line.replace('Name2:','')
        if 'Name:' in line:
            nm[0] = line.replace('Name:','')
        
#var list:
#---checks if it isn't the first command
loop = False
#---var for array of keywords to check for to launch a specific task/method
chk_gsearch = ["search","who is","what is"]
chk_gmap = ["where is","how do I get to"]
chk_run = ["open","launch","run"]
chk_nickname = ["can I call you"]
#METHODS
#---Isolate Query
def IQ (t):
    for c in t.split():
        if any(c in s for s in nm):
            print("i see my name")
            print(c)
            t = t.replace(c,"")
            print(t)
    return(t)
#---Isolate Program
def IP(name,line):
    a = line[(len(name))+1:]
    return(a)
#HERMES
engine.say("Hello, I am "+ nm[0] +", your personal computer assistant, What can I do for you today?")
engine.runAndWait()
while True:
    audio = 0
    try:
        #change val in microphone to switch inputs(headset or not,, fix later)
        if loop == True:
            r = sr.Recognizer()
        with mic as source:
            print("Listening")
            audio = r.listen(source)
    except Exception:
        print("listening failed")
        loop = True
        continue
    #x is the simplified code for what i say, given that audio is up to date
    try:
        x = r.recognize_google(audio)
    except Exception:
        continue
    if nm[0] in x or nm[1] in x:
        print(x)
        if any(v in x for v in chk_gsearch):
            print("search")
            text = IQ(x)
            text = text.replace("search","")
            text = text.replace("who is","")
            text_audio = text
            text = text.replace(" ","+")
            engine.say("searching for"+ text_audio)
            engine.runAndWait()
            wb.open_new("https://www.google.com/search?q="+text)
            #google search
        elif any(v in x for v in chk_gmap):
            print("search map")
            text = IQ(x)
            text = text.replace("where is","")
            text = text.replace("how do I get to","")
            engine.say(text+ " is right here")
            engine.runAndWait()
            wb.open_new("https://www.google.com/maps/place/"+text)
            #google map search
        elif any(v in x for v in chk_run):
            print("open")
            text = IQ(x)
            text = text.replace("open","")
            text = text.replace("launch","")
            text = text.replace("run","")
            ishere = False
            with open('mind.txt','r') as r:
                for line in r:
                    if text in line:
                        os.system(IP(text,line))
                        engine.say("Launching "+text)
                        engine.runAndWait()
                        ishere = True
                        throwaway = input("Press enter to resume...")
                        loop = True
            if ishere == False:
                engine.say("Sorry, but I don't have the program"+text+"in memory. Let me find it in now")
                engine.runAndWait()
                findExe = (text.replace(" ","") +".exe")
                lookfor = findExe
                tempPath = 'null'
                tempPath = askopenfilename()
                with open("mind.txt",'a') as w:
                    w.write(text+","+tempPath)
                with open('mind.txt','r') as r:
                    if tempPath != 'null':
                        for line in r:
                            if text in line:
                                os.system(IP(text,line))
                        engine.say("Launching "+text)
                        engine.runAndWait()
                throwaway = input("Press enter to resume...")
                loop = True
            #open program
        elif any(v in x for v in chk_nickname):
            print("Add name")
            canName = False
            text = IQ(x)
            text = text.replace('can I call you','')
            for word in text:
                print(word)
                if any(word in s for s in nm):
                    canName = True
                    print("true")
            if canName == True:
                engine.say("Yes you can call me "+text)
                engine.runAndWait()
                with open("mind.txt",'a') as w:
                    w.write("/nName2:"+ text)
        elif "write this down" in x:
            print("dictate")
            text = IQ(x)
            text = text.replace("write this down","")
            print(text)
            #types what you say
        elif "show me your heart" in x:
            print("hermes")
            #opens Hermes program for editting and/or veiwing
        elif "show me your mind" in x:
            print("ego")
            #opens Hermes expandable memory archive
    else:
        print("no")
    loop = True
    continue

