#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "jys"
__copyright__ = "Copyright (C) 2021 LATEJCON"

import sys
from os import path
import time
from QcIndex import QcIndex
from QcFichier import DEJBUT, FIN

def usage():
    script = '$PY/' + path.basename(sys.argv[0])
    print (f"""© l'ATEJCON.
Analyse le fichier plat du rejtrolexique du système Qc.
Donne le mot correspondant à un identifiant.

usage   : {script} <fichier Qc> [ "analyse" | "mot" <ident> ]
exemple : {script} Latejcon.qcrejtrolexique
exemple : {script} Latejcon.qcrejtrolexique mot 35944
""")
    
def main():
    try:
        if len(sys.argv) < 2 : raise Exception()
        nomFichierQc = path.abspath(sys.argv[1])
        action = 'analyse' 
        if len(sys.argv) > 2 : action = sys.argv[2]
        ident = 0
        if len(sys.argv) > 3 : ident = int(sys.argv[3])
        analyse(nomFichierQc, action, ident)
    except Exception as exc:
        if len(exc.args) == 0: usage()
        else:
            print ("******************************")
            print (exc.args[0])
            print ("******************************")
            raise
        sys.exit()

def analyse(nomFichierQc, action, ident):
    qcRejtroLexique = QcRejtroLexique(nomFichierQc)
    if action.startswith('ana'):
        qcRejtroLexique.afficheFichierRejtroLexique()
    elif action.startswith('mot'):
        mot = qcRejtroLexique.trouveGraphie(ident)
        print(f'mot : #{mot}#')
    qcRejtroLexique.close()
        

######################################################################################
# <donnejesIndexejes>     ::= <dejfinitionId>
# <blocEnVrac>            ::= <blocUtf8>
# <dejfinitionId>         ::= <flagId=37> <identifiant> <adresseMotUtf8>
# <flagId=37>             ::= <Entier1>
# <identifiant>           ::= <Entier3>
# <adresseMotUtf8>        ::= <Entier4>
# <blocUtf8>              ::= { <MotUtf8> }
######################################################################################
# <flagId=37>(1) <identifiant>(3) <adresseMotUtf8>(4) = 8
TAILLE_ENTREJE = 8
FLAG_ID = 37
#############################################################
class QcRejtroLexique(QcIndex):
    def __init__(self, nomQcFichier, enEjcriture = False, nombreIdentifiants = 0):
        self.nomQcFichier = nomQcFichier
        # init la couche d'en-dessous
        # nombreIdentifiants +1 parce que le premier identifiant est 1
        QcIndex.__init__(self, self.nomQcFichier, enEjcriture, TAILLE_ENTREJE, nombreIdentifiants +1) 
        if self.tailleEntreje != TAILLE_ENTREJE:
            raise Exception('{} : TAILLE_ENTREJE incompatibles'.format(self.nomQcFichier))

    ################################
    # ajoute un identifiant-mot directement sur le fichier
    def ajouteIdMot(self, identifiant, mot):
        # ejcrit ah la fin du fichier dans le bloc en vrac
        self.seek(0, FIN)
        adresseMotUtf8 = self.tell()
        self.ejcritMotUtf8(mot)
        # ejcrit dans le bloc indexej
        adresseIndex = self.donneAdresseIndex(identifiant)
        self.seek(adresseIndex, DEJBUT)
        # <flagId=37>(1) <identifiant>(3) <adresseMotUtf8>(4)
        self.ejcritNombre1(FLAG_ID)
        self.ejcritNombre3(identifiant)
        self.ejcritNombre4(adresseMotUtf8)
        
    ################################
    # donne la graphie d'un identifiant, '' si identifiant inconnu
    def trouveGraphie(self, ident):
        if ident > self.nombreEntrejes: return ''
        adresseIndex = self.donneAdresseIndex(ident)
        self.seek(adresseIndex, DEJBUT)
        # <flagId=37>(1) <identifiant>(3) <adresseMotUtf8>(4)
        flag = self.litNombre1()
        # entreje inutiliseje
        if flag == 0: return ''
        if flag != FLAG_ID: 
            raise Exception('{} : pas FLAG_ID à {:08X}'.format(self.nomQcFichier, self.tell() -1))
        if self.litNombre3() != ident:
            raise Exception('{} : incohérence à {:08X}'.format(self.nomQcFichier, self.tell() -3))
        adresseMotUtf8 = self.litNombre4()
        self.seek(adresseMotUtf8, DEJBUT)
        mot = self.litMotUtf8()
        return mot

    ################################
    # vidage complet du rejrolexique sous forme d'une liste 
    def vidage(self):
        motsIdentifiants = []
        for identifiant in range(self.nombreEntrejes):
            mot = self.trouveGraphie(identifiant)
            motsIdentifiants.append((identifiant, mot))
        motsIdentifiants.sort()
        return motsIdentifiants
        
    ################################
    # affiche les dejtails du fichier
    def afficheFichierRejtroLexique(self):
        self.afficheFichierIndex()
        total = 0
        for identifiant in range(1, self.nombreEntrejes):
            if self.trouveGraphie(identifiant) != '': total +=1
        print ("=============")
        print("NOMBRE D'IDENTIFIANTS      : ", self.nombreEntrejes -1)
        print("NOMBRE DE MOTS             : ", total)
        print ("=============")
        
            
if __name__ == '__main__':
    main()



