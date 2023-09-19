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
Analyse le fichier plat des lemmes du système Sp7.
Donne les formes avec les propriétés grammaticales associées à un lemme

usage   : {script} <fichier Sp7> [ "analyse" | "formes" <lemme> ]
exemple : {script} Latejcon.sp7lemmes
exemple : {script} Latejcon.sp7lemmes for 10636
""")
    
def main():
    try:
        if len(sys.argv) < 2 : raise Exception()
        nomFichierQc = path.abspath(sys.argv[1])
        action = 'analyse' 
        if len(sys.argv) > 2 : action = sys.argv[2]
        identifiantLemme = 0
        if len(sys.argv) > 3 : identifiantLemme = int(sys.argv[3])
        analyse(nomFichierQc, action, identifiantLemme)
    except Exception as exc:
        if len(exc.args) == 0: usage()
        else:
            print ("******************************")
            print (exc.args[0])
            print ("******************************")
            raise
        sys.exit()


def analyse(nomFichierQc, action, identifiantLemme):
    sp7Lemmes = Sp7Lemmes(nomFichierQc)
    if action.startswith('ana'):
        sp7Lemmes.afficheFichierLemmes()
    elif action.startswith('for'):
        donnejes = sp7Lemmes.trouveDonnejes(identifiantLemme)
        for (identifiantForme, genre, nombre) in donnejes:
            print(f'{identifiantForme}, {genre}, {nombre}')
    sp7Lemmes.close()

######################################################################################
# <donnejesIndexejes>     ::= <dejfinitionLemme>
# <blocEnVrac>            ::= <donnejesLemme>
# <dejfinitionLemme>      ::= <flagIdLemme=23> <identifiant> <macrocat>
#                             <nombreDejfinitions> <adresseDejfinitions>
# <flagIdLemme=23>        ::= <Entier1>
# <identifiant>           ::= <Entier3>
# <macrocat>              ::= <Entier1>
# <nombreDejfinitions>    ::= <Entier1>
# <adresseDejfinitions>   ::= <Entier4>
# <donnejesLemme>         ::= { <identifiantForme> <genre> <nombre> }
# <identifiantForme>      ::= <Entier3>
# <genre>                 ::= <Entier1>
# <nombre>                ::= <Entier1>
######################################################################################

# <flagIdLemme=23>(1) <identifiant>(3) <macrocat>(1) <nombreDejfinitions>(1) <adresseDejfinitions>(4) = 10
TAILLE_ENTREJE = 10
FLAG_IDLEMME = 23
#############################################################
class Sp7Lemmes(QcIndex):
    def __init__(self, nomQcFichier, enEjcriture = False, nombreIdentifiants = 0):
        self.nomQcFichier = nomQcFichier
        # init la couche d'en-dessous
        # nombreIdentifiants +1 parce que le premier identifiant est 1
        QcIndex.__init__(self, self.nomQcFichier, enEjcriture, TAILLE_ENTREJE, nombreIdentifiants +1) 
        if self.tailleEntreje != TAILLE_ENTREJE:
            raise Exception('{} : TAILLE_ENTREJE incompatibles'.format(self.nomQcFichier))
        
    ################################
    # ajoute une description de lemme 
    def ajouteLemme(self, identifiantLemme, macrocat, description):
        # ejcrit ah la fin du fichier dans le bloc en vrac
        self.seek(0, FIN)
        adresseDejfinitions = self.tell()
        for (identifiantForme, genre, nombre) in description:
            # { <identifiantForme> <genre> <nombre> }
            self.ejcritNombre3(identifiantForme)
            self.ejcritNombre1(genre)
            self.ejcritNombre1(nombre)
        # ejcrit dans le bloc indexej
        adresseIndex = self.donneAdresseIndex(identifiantLemme)
        if adresseIndex == 0: 
            raise Exception('{} : IDENTIFIANT HORS LIMITE : {}'.format(self.nomQcFichier,  identifiantLemme))
        self.seek(adresseIndex, DEJBUT)
        # <flagIdLemme=23>(1) <identifiant>(3) <macrocat>(1) <nombreDejfinitions>(1) <adresseDejfinitions>(4)
        self.ejcritNombre1(FLAG_IDLEMME)
        self.ejcritNombre3(identifiantLemme)
        self.ejcritNombre1(macrocat)
        self.ejcritNombre1(len(description))
        self.ejcritNombre4(adresseDejfinitions)
        
    ################################
    # retourne la macrocat d'un lemme
    def trouveMacro(self, identifiantLemme):
        adresseIndex = self.donneAdresseIndex(identifiantLemme)
        if adresseIndex == 0: return 0
        self.seek(adresseIndex, DEJBUT)
        # <flagIdLemme=23>(1) <identifiant>(3) <macrocat>(1) <nombreDejfinitions>(1) <adresseDejfinitions>(4)
        flag = self.litNombre1()
        if flag == 0: return []
        if flag != FLAG_IDLEMME: 
            raise Exception('{} : pas FLAG_IDLEMME à {:08X}'.format(self.nomQcFichier, self.tell() -1))
        if self.litNombre3() != identifiantLemme:
            raise Exception('{} : incohérence à {:08X}'.format(self.nomQcFichier, self.tell() -3))
        macrocat = self.litNombre1()
        return macrocat
    
    ################################
    # retourne l'ensemble des donnejes d'un lemme
    def trouveDonnejes(self, identifiantLemme):
        adresseIndex = self.donneAdresseIndex(identifiantLemme)
        if adresseIndex == 0: return []
        self.seek(adresseIndex, DEJBUT)
        # <flagIdLemme=23>(1) <identifiant>(3) <macrocat>(1) <nombreDejfinitions>(1) <adresseDejfinitions>(4)
        flag = self.litNombre1()
        if flag == 0: return []
        if flag != FLAG_IDLEMME: 
            raise Exception('{} : pas FLAG_IDLEMME à {:08X}'.format(self.nomQcFichier, self.tell() -1))
        if self.litNombre3() != identifiantLemme:
            raise Exception('{} : incohérence à {:08X}'.format(self.nomQcFichier, self.tell() -3))
        self.litNombre1()   # <macrocat>
        nombreDejfinitions = self.litNombre1()
        adresseDejfinitions = self.litNombre4()
        # construit le rejsultat
        rejsultat = []
        self.seek(adresseDejfinitions, DEJBUT)
        for ii in range(nombreDejfinitions):
            # <identifiantForme> <genre> <nombre>
            identifiantForme = self.litNombre3()
            genre = self.litNombre1()
            nombre = self.litNombre1()
            rejsultat.append((identifiantForme, genre, nombre))
        return rejsultat
        
    ################################
    # affiche les dejtails du fichier
    def afficheFichierLemmes(self):
        self.afficheFichierIndex()
        longueurs = {}
        total = 0
        vides = []
        for identifiantLemme in range(1, self.nombreEntrejes):
            longueur = len(self.trouveDonnejes(identifiantLemme))
            if longueur == 0: vides.append(identifiantLemme)
            if longueur not in longueurs: longueurs[longueur] = 0
            longueurs[longueur] +=1
            total += longueur
        print ("=============")
        print('NOMBRE DE LEMMES           : ', self.nombreEntrejes -1)
        print("NOMBRE DE DONNÉES          : ", total)
        longueursListe = list(longueurs.items())
        longueursListe.sort()
        for (longueur, nombre) in longueursListe:
            print(f'{longueur} : {nombre}')
        print ("=============")
        print("NOMBRE DE VIDES            : ", len(vides))
        
            
if __name__ == '__main__':
    main()
        
