#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "jys"
__copyright__ = "Copyright (C) 2021 LATEJCON"

import sys
from os import path
import time
from QcFichier import QcFichier
from QcFichier import DEJBUT, FIN

def usage():
    script = '$PY/' + path.basename(sys.argv[0])
    print (f"""© l'ATEJCON.
Analyse un fichier plat du système Qc.

usage   : {script} <fichier Qc>
exemple : {script} /tmp/Nind_testLateconNumber.lat
""")
    
def main():
    try:
        if len(sys.argv) < 2 : raise Exception()
        nomFichierQc = path.abspath(sys.argv[1])
        analyse(nomFichierQc)
    except Exception as exc:
        if len(exc.args) == 0: usage()
        else:
            print ("******************************")
            print (exc.args[0])
            print ("******************************")
            raise
        sys.exit()

def analyse(nomFichierQc):
    qcIndex = QcIndex(nomFichierQc)
    qcIndex.analyseIndex(nomFichierQc)
    
    
######################################################################################
# <fichier>               ::= <blocIndexej> <blocSpejcifique> <blocEnVrac> <blocIdentification> 
# <blocIndexej>           ::= <flagIndexej=47> <tailleEntreje> <nombreEntrejes>
#                             { <donnejesIndexejes> }
# <flagIndexej=47>        ::= <Entier1>
# <tailleEntreje>         ::= <Entier1>
# <nombreEntrejes>        ::= <Entier3>
# <donnejesIndexejes>     ::= { <Octet> }
# <blocSpejcifique>       ::= <flagSpejcifique=59> <tailleSpejcifique> <donnejesSpejcifiques>
# <flagSpejcifique=59>    ::= <Entier1>
# <tailleSpejcifique>     ::= <Entier3>
# <donnejesSpejcifiques>  ::= { <Octet> }
# <blocEnVrac>            ::= { <Octet> }
# <blocIdentification>    ::= <flagIdentification=53> <maxIdentifiant>
#                             <identifieurUnique> 
# <flagIdentification=53> ::= <Entier1>
# <maxIdentifiant>        ::= <Entier3>
# <identifieurUnique>     ::= <dateHeure>
# <dateHeure >            ::= <Entier4>
######################################################################################
FLAG_INDEXEJ = 47
FLAG_SPEJCIFIQUE = 59
FLAG_IDENTIFICATION = 53
# <flagIndexej=47>(1) <tailleEntreje>(1) <nombreEntrejes>(3) = 5
TAILLE_DEJBUTINDEX = 5
# <flagIdentification=53>(1) <maxIdentifiant>(4) <identifieurUnique>(4) = 9
TAILLE_IDENTIFICATION = 9
#############################################################
class QcIndex(QcFichier):
    def __init__(self, nomQcFichier, enEjcriture = False, tailleEntreje = 0, nombreEntrejes = 0, tailleSpejcifique = 0):
        self.nomQcFichier = nomQcFichier
        # init la couche d'en-dessous
        QcFichier.__init__(self, self.nomQcFichier, enEjcriture)
        if enEjcriture:
            self.tailleEntreje = tailleEntreje
            self.nombreEntrejes = nombreEntrejes
            # ejcrit la partie fixe du bloc d'index
            # <flagIndexej=47> <tailleEntreje> <nombreEntrejes>
            self.seek(0, DEJBUT)
            self.ejcritNombre1(FLAG_INDEXEJ)
            self.ejcritNombre1(tailleEntreje)
            self.ejcritNombre3(nombreEntrejes)
            #ejcrit le bloc index ah 0
            self.ejcritZejros(tailleEntreje * nombreEntrejes)
            # ejcrit la partie spejcifique
            # <flagSpejcifique=59> <tailleSpejcifique> <donnejesSpejcifiques>
            self.tailleSpejcifique = tailleSpejcifique
            self.ejcritNombre1(FLAG_SPEJCIFIQUE)
            self.ejcritNombre3(tailleSpejcifique)
            # adresse dejbut spejcifique 
            self.dejbutSpejcifique = self.tell()
            self.ejcritZejros(tailleSpejcifique)
        else:   
            # lit la partie fixe du bloc d'index
            self.seek(0, DEJBUT)
            # <flagIndexej=47> <tailleEntreje> <nombreEntrejes>
            if self.litNombre1() != FLAG_INDEXEJ: 
                raise Exception('{} : pas FLAG_INDEXEJ à {:08X}'.format(self.nomQcFichier, self.tell() -1))
            self.tailleEntreje = self.litNombre1()
            self.nombreEntrejes = self.litNombre3()
            # lit la partie fixe du bloc spejcifique
            adrBlocSpejcifique = self.tailleEntreje * self.nombreEntrejes + TAILLE_DEJBUTINDEX
            self.seek(adrBlocSpejcifique, DEJBUT)
            if self.litNombre1() != FLAG_SPEJCIFIQUE: 
                raise Exception('{} : pas FLAG_SPEJCIFIQUE à {:08X}'.format(self.nomQcFichier, self.tell() -1))
            self.tailleSpejcifique = self.litNombre3()
            # adresse dejbut spejcifique 
            self.dejbutSpejcifique = self.tell()
    
    #############################################################   
    # retourne l'identification du fichier
    def donneIdentificationFichier(self):
        #<flagIdentification=53> <maxIdentifiant> <identifieurUnique>
        self.seek(-TAILLE_IDENTIFICATION, FIN)
        if self.litNombre1() != FLAG_IDENTIFICATION: 
            raise Exception('{} : pas FLAG_IDENTIFICATION à {:08X}'.format(self.nomQcFichier, self.tell() -1))
        maxIdentifiant = self.litNombre4()
        identifieurUnique = self.litNombre4()
        return (maxIdentifiant, identifieurUnique)

    #############################################################   
    # ejcrit l'identification ah la fin du fichier
    def ejcritIdentificationFichier(self, maxIdentifiant, identifieurUnique):
        # <flagIdentification=53> <maxIdentifiant> <identifieurUnique>
        self.seek(0, FIN)
        self.ejcritNombre1(FLAG_IDENTIFICATION)
        self.ejcritNombre4(maxIdentifiant)
        self.ejcritNombre4(identifieurUnique)

    #############################################################   
    # donne l'adresse dans le fichier de l'index spejcifiej, 0 si hors limite
    def donneAdresseIndex(self, index):
        if index > self.nombreEntrejes: return 0
        return (index * self.tailleEntreje) + TAILLE_DEJBUTINDEX
        
    #############################################################   
    # donne l'adresse dans le fichier du bloc en vrac
    def donneAdresseEnVrac(self):
        return (self.nombreEntrejes * self.tailleEntreje) + TAILLE_DEJBUTINDEX
        
    #############################################################   
    # analyse le fichier index, renvoie True si c'est bon
    def analyseIndex(self, trace):
        try:
            cestBon = True
            # lit la partie fixe du bloc d'index
            self.seek(0, DEJBUT)
            # <flagIndexej=47> <tailleEntreje> <nombreEntrejes>
            if self.litNombre1() != FLAG_INDEXEJ: 
                    raise Exception('{} : pas FLAG_INDEXEJ à {:08X}'.format(self.nomQcFichier, self.tell() -1))
            tailleEntreje = self.litNombre1()
            nombreEntrejes = self.litNombre3()
            if trace: 
                print('TAILLE ENTRÉES             : ', tailleEntreje)
                print("NOMBRE D'ENTRÉES           : ", nombreEntrejes)
                print ("=============")
            # <flagSpejcifique=59> <tailleSpejcifique> <donnejesSpejcifiques>
            adrBlocSpejcifique = tailleEntreje * nombreEntrejes + TAILLE_DEJBUTINDEX
            self.seek(adrBlocSpejcifique, DEJBUT)
            if self.litNombre1() != FLAG_SPEJCIFIQUE: 
                raise Exception('{} : pas FLAG_SPEJCIFIQUE à {:08X}'.format(self.nomQcFichier, self.tell() -1))
            tailleSpejcifique = self.litNombre3()
            if trace: 
                print('TAILLE SPÉCIFIQUES         : ', tailleSpejcifique)
                print ("=============")
            # <flagIdentification=53> <maxIdentifiant> <identifieurUnique>
            self.seek(-TAILLE_IDENTIFICATION, FIN)
            if self.litNombre1() != FLAG_IDENTIFICATION: 
                raise Exception('{} : pas FLAG_IDENTIFICATION à {:08X}'.format(self.nomQcFichier, self.tell() -1))
            maxIdentifiant = self.litNombre4()
            identifieurUnique = self.litNombre4()
            if trace: 
                print('MAX IDENTIFIANTS           : ', maxIdentifiant)
                print("IDENTIFIEUR UNIQUE         : ", identifieurUnique)
                print("                           : ", time.ctime(int(identifieurUnique)))
                print ("=============")
        except Exception as exc: 
            cestBon = False
            if trace: print ('ERREUR :', exc.args[0])
        return cestBon
        
        
       
if __name__ == '__main__':
    main()



