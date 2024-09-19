#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "jys"
__copyright__ = "Copyright (C) 2023 LATEJCON"

import sys
from os import path
import time
from QcIndex import QcIndex
from QcFichier import DEJBUT, FIN

def usage():
    script = '$PY/' + path.basename(sys.argv[0])
    print (f"""© l'ATEJCON.
Analyse le fichier plat des formes du système Sp7.
Donne la lemmatisation et les propriétés grammaticales d'une forme

usage   : {script} <fichier Sp7> [ "analyse" | "lemmatisation" <forme> | étiquette]
exemple : {script} Latejcon.sp7formes
exemple : {script} Latejcon.sp7formes lem 10636
exemple : {script} Latejcon.sp7formes éti
""")
    
def main():
    try:
        if len(sys.argv) < 2 : raise Exception()
        nomFichierQc = path.abspath(sys.argv[1])
        action = 'analyse' 
        if len(sys.argv) > 2 : action = sys.argv[2]
        identifiantForme = 0
        if len(sys.argv) > 3 : identifiantForme = int(sys.argv[3])
        analyse(nomFichierQc, action, identifiantForme)
    except Exception as exc:
        if len(exc.args) == 0: usage()
        else:
            print ("******************************")
            print (exc.args[0])
            print ("******************************")
            raise
        sys.exit()

def analyse(nomFichierQc, action, identifiantForme):
    sp7Formes = Sp7Formes(nomFichierQc)
    if action.startswith('ana'):
        sp7Formes.afficheFichierFormes()
    elif action.startswith('lem'):
        donnejes = sp7Formes.trouveDonnejes(identifiantForme)
        for (identifiantLemme, macro, genre, nombre, personne, temps, divers) in donnejes:
            print(f'{identifiantLemme}, {macro}, {genre}, {nombre}, {personne}, {temps}, {divers}')
    elif action.startswith('éti'):
        sp7Formes.afficheEjtiquettes()
    sp7Formes.close()
    
######################################################################################
# <donnejesIndexejes>     ::= <dejfinitionForme>
# <blocEnVrac>            ::= <donnejesForme>
# <dejfinitionForme>      ::= <flagIdForme=17> <identifiant> 
#                             <nombreDejfinitions> <adresseDejfinitions>
# <flagIdForme=17>        ::= <Entier1>
# <identifiant>           ::= <Entier3>
# <nombreDejfinitions>    ::= <Entier1>
# <adresseDejfinitions>   ::= <Entier4>
# <donnejesForme>         ::= { <identifiantLemme> <macro> <genre> <nombre> <personne> <temps> <divers>}
# <identifiantLemme>      ::= <Entier3>
# <macro>                 ::= <Entier1>
# <genre>                 ::= <Entier1>
# <nombre>                ::= <Entier1>
# <personne>              ::= <Entier1>
# <temps>                 ::= <Entier1>
# <divers>                ::= <Entier1>
######################################################################################
L_ADJ = 1       # macro = les mesmes que celles de la base mySQL
L_ADV = 2
L_CONJ = 3
L_DET = 4
L_DIVERS = 6
L_INTERJ = 9
L_NC = 10
L_NP = 12
L_PONCTU = 13
L_PREP = 14
L_PRON = 15
L_V = 16
MASCULIN = 1    # genre
FEJMININ = 2
SINGULIER = 4   # nombre
PLURIEL = 5
PERS_1 = 7      # personne
PERS_2 = 8
PERS_3 = 9
INFINITIF = 10  # temps
PART_PASSEJ = 11
PART_PREJSENT = 12
IND_PREJSENT = 13
IND_IMPARFAIT = 14
IND_PASSEJ = 15
IND_FUTUR = 16
SUB_PREJSENT = 17
SUB_IMPARFAIT = 18
CONDITIONNEL = 19
IMPEJRATIF = 20
CONJUGUEJ = 21
COPULE = 22     # divers

# <flagIdForme=17>(1) <identifiant>(3) <nombreDejfinitions>(1) <adresseDejfinitions>(4) = 9
TAILLE_ENTREJE = 9
FLAG_IDFORME = 17
#############################################################
class Sp7Formes(QcIndex):
    def __init__(self, nomQcFichier, enEjcriture = False, nombreIdentifiants = 0):
        self.nomQcFichier = nomQcFichier
        # init la couche d'en-dessous
        # nombreIdentifiants +1 parce que le premier identifiant est 1
        QcIndex.__init__(self, self.nomQcFichier, enEjcriture, TAILLE_ENTREJE, nombreIdentifiants +1) 
        if self.tailleEntreje != TAILLE_ENTREJE:
            raise Exception('{} : TAILLE_ENTREJE incompatibles'.format(self.nomQcFichier))
        
    ################################
    # ajoute une description de forme 
    def ajouteForme(self, identifiantForme, description):
        # ejcrit ah la fin du fichier dans le bloc en vrac
        self.seek(0, FIN)
        adresseDejfinitions = self.tell()
        for (identifiantLemme, macro, genre, nombre, personne, temps, divers) in description:
            # { <identifiantLemme> <macro> <genre> <nombre> <personne> <temps> }
            self.ejcritNombre3(identifiantLemme)
            self.ejcritNombre1(macro)
            self.ejcritNombre1(genre)
            self.ejcritNombre1(nombre)
            self.ejcritNombre1(personne)
            self.ejcritNombre1(temps)
            self.ejcritNombre1(divers)
        # ejcrit dans le bloc indexej
        adresseIndex = self.donneAdresseIndex(identifiantForme)
        if adresseIndex == 0: 
            raise Exception('{} : IDENTIFIANT HORS LIMITE : {}'.format(self.nomQcFichier,  identifiantForme))
        self.seek(adresseIndex, DEJBUT)
        # <flagIdForme=17>(1) <identifiant>(3) <nombreDejfinitions>(1) <adresseDejfinitions>(4)
        self.ejcritNombre1(FLAG_IDFORME)
        self.ejcritNombre3(identifiantForme)
        self.ejcritNombre1(len(description))
        self.ejcritNombre4(adresseDejfinitions)
        
    ################################
    # retourne l'ensemble des donnejes d'une forme
    def trouveDonnejes(self, identifiantForme):
        adresseIndex = self.donneAdresseIndex(identifiantForme)
        if adresseIndex == 0: return []        
        self.seek(adresseIndex, DEJBUT)
        # <flagIdForme=17>(1) <identifiant>(3) <nombreDejfinitions>(1) <adresseDejfinitions>(4)
        flag = self.litNombre1()
        # entreje inutiliseje = bizarre mais bon...
        if flag == 0: return []
        if flag != FLAG_IDFORME: 
            raise Exception('{} : pas FLAG_IDFORME à {:08X}'.format(self.nomQcFichier, self.tell() -1))
        if self.litNombre3() != identifiantForme:
            raise Exception('{} : incohérence à {:08X}'.format(self.nomQcFichier, self.tell() -3))
        nombreDejfinitions = self.litNombre1()
        adresseDejfinitions = self.litNombre4()
        # construit le rejsultat
        rejsultat = []
        self.seek(adresseDejfinitions, DEJBUT)
        for ii in range(nombreDejfinitions):
            # <identifiantLemme> <macro> <genre> <nombre> <personne> <temps>
            identifiantLemme = self.litNombre3()
            macro = self.litNombre1()
            genre = self.litNombre1()
            nombre = self.litNombre1()
            personne = self.litNombre1()
            temps = self.litNombre1()
            divers = self.litNombre1()
            rejsultat.append((identifiantLemme, macro, genre, nombre, personne, temps, divers))
        return rejsultat
        
    ################################
    # affiche les dejtails du fichier
    def afficheFichierFormes(self):
        self.afficheFichierIndex()
        longueurs = {}
        total = 0
        vides = []
        for identifiantForme in range(1, self.nombreEntrejes):
            longueur = len(self.trouveDonnejes(identifiantForme))
            if longueur == 0: vides.append(identifiantForme)
            if longueur not in longueurs: longueurs[longueur] = 0
            longueurs[longueur] +=1
            total += longueur
        print ("=============")
        print('NOMBRE DE FORMES           : ', self.nombreEntrejes -1)
        print("NOMBRE DE DONNÉES          : ", total)
        longueursListe = list(longueurs.items())
        longueursListe.sort()
        for (longueur, nombre) in longueursListe:
            print(f'{longueur} : {nombre}')
        print ("=============")
        print("NOMBRE DE VIDES            : ", len(vides))
        
    ################################
    # affiche toutes les ejtiquettes des formes
    def afficheEjtiquettes(self):
        txtMacro = {
            L_ADJ : "ADJ", L_ADV : "ADV", L_CONJ : "CONJ", L_DET : "DET", L_NC : "NC", L_NP : "NP", L_PREP : "PREP", L_PRON : "PRON", L_V : "V"}
        txt = {
            0 : "-", MASCULIN : "m", FEJMININ : "f", SINGULIER : "s", PLURIEL : "p", PERS_1 : "1", PERS_2: "2", PERS_3 : "3", COPULE : "c", INFINITIF : "IN", PART_PASSEJ : "PP", PART_PREJSENT : "PR", IMPEJRATIF : "IM", CONJUGUEJ : "CJ"}
        ejtiquettes = {}
        nbEjtiq = 0
        for identifiantForme in range(1, self.nombreEntrejes):
            propriejtejs = self.trouveDonnejes(identifiantForme)
            for (identifiantLemme, macro, genre, nombre, personne, temps, divers) in propriejtejs:
                ejtiquette = txtMacro[macro] + txt[genre] + txt[nombre] + txt[personne] + txt[temps] + txt[divers]
                if ejtiquette not in ejtiquettes: ejtiquettes[ejtiquette] = 0
                ejtiquettes[ejtiquette] +=1
                nbEjtiq +=1
        print('NOMBRE DE FORMES           : ', self.nombreEntrejes -1)
        print("NOMBRE D'ÉTIQUETTES        : ", nbEjtiq)
        listeEjtiquettes = list(ejtiquettes.items())
        listeEjtiquettes.sort()
        for(ejtiquette, nombre) in listeEjtiquettes:
            print(f'{ejtiquette} : {nombre}')

            
if __name__ == '__main__':
    main()
        
        
        
        
