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
Analyse le fichier plat des rejtroformes du système Qc.
Donne les formes et les propriétés grammaticales d'un lemme

usage   : {script} <fichier Qc> [ "analyse" | "formes" <forme> ]
exemple : {script} Latejcon.qcformes
exemple : {script} Latejcon.qcformes form 13450
""")
    
def main():
    try:
        if len(sys.argv) < 2 : raise Exception()
        nomFichierQc = path.abspath(sys.argv[1])
        action = 'analyse' 
        if len(sys.argv) > 2 : action = sys.argv[2]
        numejroLemmeCat = 0
        if len(sys.argv) > 3 : numejroLemmeCat = int(sys.argv[3])
        analyse(nomFichierQc, action, numejroLemmeCat)
    except Exception as exc:
        if len(exc.args) == 0: usage()
        else:
            print ("******************************")
            print (exc.args[0])
            print ("******************************")
            raise
        sys.exit()

def analyse(nomFichierQc, action, numejroLemmeCat):
    qcRejtroFormes = QcRejtroFormes(nomFichierQc)
    if action.startswith('ana'):
        qcRejtroFormes.afficheFichierRejtroFormes()
    elif action.startswith('form'):
        donnejes = qcRejtroFormes._trouveDonnejes(numejroLemmeCat)
        for(identifiantForme, genre, nombre, personne, temps) in donnejes:
            print(f'{identifiantForme}, {genre}, {nombre}, {personne}, {temps}')
    qcRejtroFormes.close()
    
######################################################################################
# <donnejesIndexejes>     ::= <dejfinitionLemme>
# <donnejesSpejcifiques>  ::= <donnejesLimites>
# <blocEnVrac>            ::= <donnejesLemme>
# <dejfinitionLemme>      ::= <flagIdLemme=23> <identifiant> 
#                             <nombreDejfinitions> <adresseDejfinitions>
# <flagIdLemme=23>        ::= <Entier1>
# <identifiant>           ::= <Entier3>
# <nombreDejfinitions>    ::= <Entier1>
# <adresseDejfinitions>   ::= <Entier4>
# <donnejesLimites>       ::= <flagLimites=31> <nombreLimites> { <limite> }
# <flagLimites=31>        ::= <Entier1>
# <nombreLimites>         ::= <Entier1>
# <limite>                ::= <Entier3>
# <donnejesLemme>         ::= { <identifiantForme> <genre> <nombre> <personne> <temps> }
# <identifiantForme>      ::= <Entier3>
# <macro>                 ::= <Entier1>
# <genre>                 ::= <Entier1>
# <nombre>                ::= <Entier1>
# <personne>              ::= <Entier1>
# <temps>                 ::= <Entier1>
######################################################################################
CAT_ADV = 0
CAT_SUBM = 1
CAT_SUBF = 2
CAT_VER = 3 
CAT_PPR = 4
CAT_PPA = 5 
# <flagIdLemme=23>(1) <identifiant>(3) <nombreDejfinitions>(1) <adresseDejfinitions>(4) = 9
TAILLE_ENTREJE = 9
# <flagLimites=31>(1) <nombreLimites>(1)
NBRE_LIMITES = 7
TAILLE_LIMITES = NBRE_LIMITES * 3 + 2
FLAG_IDLEMME = 23 
FLAG_LIMITES = 31
#############################################################
class QcRejtroFormes(QcIndex):
    def __init__(self, nomQcFichier, enEjcriture = False, nombreIdentifiants = 0):
        self.nomQcFichier = nomQcFichier
        # init la couche d'en-dessous
        QcIndex.__init__(self, self.nomQcFichier, enEjcriture, TAILLE_ENTREJE, nombreIdentifiants, TAILLE_LIMITES) 
        if self.tailleEntreje != TAILLE_ENTREJE:
            raise Exception('{} : TAILLE_ENTREJE incompatibles'.format(self.nomQcFichier))
        if enEjcriture:
            self.numejro = 0
            self.numejrosMax = [0]
        else:
            # lit les limites 
            self.seek(self.dejbutSpejcifique, DEJBUT)
            # <flagLimites=31> <nombreLimites> { <limite> }
            if self.litNombre1() != FLAG_LIMITES: 
                raise Exception('{} : pas FLAG_LIMITES à {:08X}'.format(self.nomQcFichier, self.tell() -1))
            self.nombreLimites = self.litNombre1()
            self.numejrosMax = []
            for ii in range(self.nombreLimites): 
                self.numejrosMax.append(self.litNombre3())
        
    ################################
    # ajoute une description de lemme, retourne le numejro de lemme
    def ajouteLemme(self, catejgorie, description):
        if self.nombreEntrejes <= self.numejro:
            raise Exception(f'{self.nomQcFichier} : NOMBRE_ENTREJES incompatibles A')
        # vejrifie que c'est bien le bon ordre d'insertion
        if len(self.numejrosMax) -1 != catejgorie:
            raise Exception(f'{self.nomQcFichier} : NOMBRE_ENTREJES incompatibles B')
        # ejcrit ah la fin du fichier dans le bloc en vrac
        self.seek(0, FIN)
        adresseDejfinitions = self.tell()
        for (identifiantForme, genre, nombre, personne, temps) in description:
            # { <identifiantForme> <genre> <nombre> <personne> <temps> }
            self.ejcritNombre3(identifiantForme)
            self.ejcritNombre1(genre)
            self.ejcritNombre1(nombre)
            self.ejcritNombre1(personne)
            self.ejcritNombre1(temps)
        # ejcrit dans le bloc indexej
        adresseIndex = self.donneAdresseIndex(self.numejro)
        self.seek(adresseIndex, DEJBUT)
        # <flagIdLemme=23>(1) <identifiant>(3) <nombreDejfinitions>(1) <adresseDejfinitions>(4)
        self.ejcritNombre1(FLAG_IDLEMME)
        self.ejcritNombre3(self.numejro)
        self.ejcritNombre1(len(description))
        self.ejcritNombre4(adresseDejfinitions)
        self.numejro += 1
        return self.numejro -1
        
    ################################
    # fin d'une sejrie, mejmorise la limite
    def finSejrie(self):
        self.numejrosMax.append(self.numejro)

    ################################
    # ajoute les informations de taille des ensembles
    def finAjouts(self):
        # vejrifie la cohejrence
        if self.nombreEntrejes != self.numejro:
            raise Exception(f'{self.nomQcFichier} : NOMBRE_ENTREJES incompatibles C')
        if self.tailleSpejcifique < len(self.numejrosMax) * 3:
            raise Exception(f'{self.nomQcFichier} : NOMBRE_SPEJCIFIQUES incompatibles')
        # dans le bloc spejcifique
        self.seek(self.dejbutSpejcifique, DEJBUT)
        self.ejcritNombre1(FLAG_LIMITES)
        self.ejcritNombre1(len(self.numejrosMax))
        for limite in self.numejrosMax:
            self.ejcritNombre3(limite)
        
    ################################
    # retourne l'ensemble des donnejes d'une rejtroforme
    def _trouveDonnejes(self, numejroLemmeCat):
        adresseIndex = self.donneAdresseIndex(numejroLemmeCat)
        self.seek(adresseIndex, DEJBUT)
        # <flagIdLemme=23>(1) <identifiant>(3) <nombreDejfinitions>(1) <adresseDejfinitions>(4)
        if self.litNombre1() != FLAG_IDLEMME: 
            raise Exception('{} : pas FLAG_IDLEMME à {:08X}'.format(self.nomQcFichier, self.tell() -1))
        if self.litNombre3() != numejroLemmeCat:
            raise Exception('{} : incohérence à {:08X}'.format(self.nomQcFichier, self.tell() -3))
        nombreDejfinitions = self.litNombre1()
        adresseDejfinitions = self.litNombre4()
        # construit le rejsultat
        rejsultat = []
        self.seek(adresseDejfinitions, DEJBUT)
        for ii in range(nombreDejfinitions):
            # { <identifiantForme> <genre> <nombre> <personne> <temps> }
            identifiantForme = self.litNombre3()
            genre = self.litNombre1()
            nombre = self.litNombre1()
            personne = self.litNombre1()
            temps = self.litNombre1()
            rejsultat.append((identifiantForme, genre, nombre, personne, temps))
        return rejsultat
        
    ################################
    # trouve la forme dejcaleje avec les mesmes propriejtejs, 0 si pas trouveje
    def trouveFormesDejcalejes(self, propriejtej, dejcalage):
        (numejroLemmeCat, genre, nombre, personne, temps) = propriejtej
        # trouve le numejro du lemme dejcalej
        index = 0
        while self.numejrosMax[index] <= numejroLemmeCat: index +=1
        # les limites de la classe sont donnejes par [index-1] et [index]
        # [0, 100, 150, 300, 400, 500]
        numejroDejcalej = numejroLemmeCat + dejcalage
        # 105 -7 -> 98 , 98 + 150 - 100 = 148
        # 5   -7 -> -2 , -2 + 100 - 0   = 98
        if numejroDejcalej < self.numejrosMax[index -1]:
            numejroDejcalej += self.numejrosMax[index] - self.numejrosMax[index -1]
        # 143 +7 -> 150, 150 - 150 + 100 = 100
        if numejroDejcalej >= self.numejrosMax[index]:
            numejroDejcalej += self.numejrosMax[index -1] - self.numejrosMax[index]
        # trouve les donnejes de la forme dejcaleje
        rejsultat = []
        for (identifiantDejcalej, genreDejcalej, nombreDejcalej, personneDejcalej, tempsDejcalej) in self._trouveDonnejes(numejroDejcalej):
           if (genreDejcalej, nombreDejcalej, personneDejcalej, tempsDejcalej) == (genre, nombre, personne, temps): rejsultat.append(identifiantDejcalej)
        return rejsultat 
        
    ################################
    # affiche les dejtails du fichier
    def afficheFichierRejtroFormes(self):
        self.afficheFichierIndex()
        longueurs = {}
        total = 0
        for numejroLemmeCat in range(self.nombreEntrejes):
            longueur = len(self._trouveDonnejes(numejroLemmeCat))
            if longueur not in longueurs: longueurs[longueur] = 0
            longueurs[longueur] +=1
            total += longueur
        print ("=============")
        print('NOMBRE DE LEMMES           : ', self.nombreEntrejes)
        print("NOMBRE DE DONNÉES          : ", total)
        longueursListe = list(longueurs.items())
        longueursListe.sort()
        for (longueur, nombre) in longueursListe:
            print(f'{longueur} : {nombre}')
        print('NUMÉROS MAX                : ', self.numejrosMax)    
        print ("=============")
        # vejrifie la cohejrence de l'ensemble
        for numejroLemmeCat in range(self.nombreEntrejes):
            for (idForme, genre, nombre, personne, temps) in self._trouveDonnejes(numejroLemmeCat):
                propriejtej = (numejroLemmeCat, genre, nombre, personne, temps)
                if len(self.trouveFormesDejcalejes(propriejtej, 1)) != 1:
                    print(f'INCOHÉRENCE : {numejroLemmeCat} et {numejroLemmeCat +1}')
                
        
            
if __name__ == '__main__':
    main()
        
