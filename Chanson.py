from timeit import default_timer as timer
from time import sleep
from SwSpotify import spotify
#from PyLyrics import *
import clock
from win10toast import ToastNotifier
from lyricsgenius import *


genius = Genius()


Spotify = "ON"
Start_Timer = timer()

# Charge le dictionnaire pour compter le nombre de fois que j'ai écouté chaque chanson

    
def ChargeDico():
    Dico = {}
    last = 0
    for i in getInfo("Compte_Chanson.txt"):
        Chanson = ""
        Compte = " "
        for j in range(len(i)):
            if i[j] == " ":
                last = j
        Chanson = i[0:last]
        Compte = i[last + 1:len(i) - 1]
        Dico[Chanson] = Compte
    tic = timer()
    return Dico

def getInfo(filename):
    file = open(filename,"r")
    informations = file.readlines()
    file.close()
    return informations

def StringTime(time_now):
    datum = str(clock.now())[0:10]
    return datum + " " +  str(time_now//3600) +":"+ str((time_now%3600) //60)+":"+str(time_now%60)+"\n"
    
def AddTime():
    time_now = timer()
    informations = getInfo("Temps.txt")
    file = open("Temps.txt","w")
    file.writelines(informations)
    file.write(StringTime(time_now))
    file.close()
    return time_now

def getSong():
    statement = True
    while True:
        try:
            return spotify.current()
        except :
            if statement :
                statement = False
                print("Spotify est éteint")
            sleep(10)
    
    
def AddOneCounter():
    stock = getInfo("Compte_Chanson.txt")
    Dico[str(song + " " + artist)] =  int(Dico[str(song + " " + artist)]) + 1
    counter = 0
    for r in stock:
        for j in range(len(r)):
            if r[j] == " ":
                last = j
        if str(song + " " + artist) ==  r[0:last]: 
            stock[counter] = song + " " + artist + " " + str(Dico[str(song+" "+artist)])+ "\n"
            file = open("Compte_Chanson.txt", "w+")
            file.writelines(stock)
            break
        counter += 1
    file.close()

# Retourne les x chansons les plus écoutées sur Spotify
def Podium(Top):
    Bests = []
    if len(Dico) < Top:
        return
    for i in range(Top):
        Ecoute = 0
        for x, y in Dico.items():
            if int(y) > int(Ecoute) and str(x) + " Ecouté " + str(y) + " fois" not in Bests:
                BestTitle = x
                Ecoute = y
        Bests.append(str(BestTitle) + " Ecouté " + str(Ecoute) + " fois")
    print(Bests)


NouvelleChanson = "SpotifyOFF"
Dico=ChargeDico()
hours_stocked = 3600

while True:
    # Prends l'artiste et le titre sur Spotify
    #try:
        song,artist = getSong()
        
        # Prends les paroles de cette chanson
        AncienneChanson = NouvelleChanson
        print(artist)
        print(song)
        NouvelleChanson = genius.search_song(song, artist).lyrics

        # Ecrit les paroles dans la console
        if NouvelleChanson != AncienneChanson:
            print("////////////")
            print(song, artist)
            print(NouvelleChanson)
            print("////////////")

                # Si j'ai déjà écouté la chanson par le passé, ajouter une unité au nombre de fois que j'ai écouté la chanson.
            if str(song + " " + artist) in Dico:
                AddOneCounter()

                # Si c'est la première fois qu'on écoute la chanson, cela ajoute la nouvelle chanson dans le dictionnaire et l'écrit dans le document texte sur une nouvelle ligne.
            else:
                fileactual = getInfo("Compte_Chanson.txt")
                file = open("Compte_Chanson.txt", "w+")
                fileactual.append(str(song + " " + artist + " " + "1" + "\n"))
                file.writelines(fileactual)
                Dico[str(song + " " + artist)] = 1
                file.close()

        # Dors pendant la chanson et met a jour le temps passé à écouter Spotify chaque minutes
        else:
            now = AddTime()
            if int(now) >hours_stocked:
                hours_stocked += 3600
                toaster = ToastNotifier()
                toaster.show_toast("Good Job!","Tu travailles depuis "+str(hours_stocked/3600)+" heures, et Thomas ne dort pas !",duration = 100)
            sleep(3)
    # Détecte si Spotify est éteint
    #except:
       # print("An error occurred,")
        #sleep(15)
        
 