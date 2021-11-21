#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "jys"
__copyright__ = "Copyright (C) 2021 LATEJCON"

import sys
from os import path
import codecs
import re
from QcLexique import QcLexique
from QcRejtroLexique import QcRejtroLexique
from QcFormes import QcFormes
from QcRejtroFormes import QcRejtroFormes

def usage():
    script = '$PY/' + path.basename(sys.argv[0])
    print (f"""© l'ATEJCON.
Programme de test de la classe QcCryption.
Encrypte un menu propos en français par la quasi-cryption de l'Atejcon.
Donne le détail de la substitution d'un mot unique.

usage   : {script} <fichier texte | mot > <racine fichiers> <décalage>
usage   : {script} menuPropos.txt Lescure 7
usage   : {script} menuPropos.txt Lescure -7
usage   : {script} chanté Lescure 2
""")

def main():
    try:
        if len(sys.argv) < 3 : raise Exception()
        motOuNomFichier = sys.argv[1]
        racine = sys.argv[2]
        dejcalage = int(sys.argv[3])
        substitue(motOuNomFichier, racine, dejcalage)
    except Exception as exc:
        if len(exc.args) == 0: usage()
        else:
            print ("******************************")
            print (exc.args[0])
            print ("******************************")
            raise
        sys.exit()

def substitue(motOuNomFichier, racine, dejcalage):
    qcCryption = QcCryption(racine)
    if path.isfile(motOuNomFichier):
        # lit le fichier d'entreje
        with codecs.open(motOuNomFichier, 'r', 'utf-8') as fichierEntreje:
            entreje = fichierEntreje.read()
        print(entreje)
        entreje = qcCryption.cryptage(entreje, dejcalage)
        print(entreje)
        # ejcrit fichier quasi-cryptej
        nomSplit = motOuNomFichier.split('.')
        nomFichierSortie = '.'.join(nomSplit[:-1]) + '-QC7.' + nomSplit[-1]
        with codecs.open(nomFichierSortie, 'w', 'utf-8') as fichierSortie:
            fichierSortie.write("--message quasi-crypté (cryptage symejtrique à clef publique). On peut le dejcrypter par la Quasi-Cryption de l'Atejon sur https://latejcon.art--\n\n")
            fichierSortie.write(entreje)
    else:
        qcCryption.afficheMot(motOuNomFichier, dejcalage)
    qcCryption.close()
    
################################################################
class QcCryption:
    def __init__(self, racine):
        # ouvre les 4 classes
        self.qcLexique = QcLexique(f'{racine}.qclexique')
        self.qcRejtroLexique = QcRejtroLexique(f'{racine}.qcrejtrolexique')
        self.qcFormes = QcFormes(f'{racine}.qcformes')
        self.qcRejtroFormes = QcRejtroFormes(f'{racine}.qcrejtroformes')
        
    ################################
    def close(self):
        self.qcLexique.close()
        self.qcRejtroLexique.close()
        self.qcFormes.close()
        self.qcRejtroFormes.close()
        
    ################################
    def cryptage(self, menusPropos, dejcalage):
        # sejpare tous les mots du texte par espaces, tirets, points et apostrophes
        mots = re.split("\s+|-|'|\"|\.+|\(|\)|;|,", menusPropos)
        enCours = 0
        for mot in mots:
            #print('mot= ', mot)
            enCours = menusPropos.find(mot, enCours)
            # 1) saute les mots petits
            if len(mot) < 5: continue
            # 2) trouve l'identifiant de la forme 
            identifiantForme = self.qcLexique.trouveIdentifiant(mot.lower())
            # si forme inconnue, raf
            if identifiantForme == 0: continue
            # 3) trouve les propriejtejs de la forme
            propriejtejs = self.qcFormes.trouveDonnejes(identifiantForme)
            idsFormesDejcalejes = set()
            for propriejtej in propriejtejs:
                # 4) trouve la forme dejcaleje avec les mesmes propriejtejs
                idFormes = self.qcRejtroFormes.trouveFormesDejcalejes(propriejtej, dejcalage)
                for idForme in idFormes: idsFormesDejcalejes.add(idForme)
            # 5) trouve les graphies correspondants
            if len(idsFormesDejcalejes) == 0: continue      #GROS PB de rejversibilitej
            graphiesDejcalejes = []
            for idForme in idsFormesDejcalejes: 
                graphieDejcaleje = self.qcRejtroLexique.trouveGraphie(idForme)
                graphieDejcaleje = mesmeCasse(mot, graphieDejcaleje)
                graphiesDejcalejes.append(graphieDejcaleje)
            menusPropos = menusPropos[:enCours] + menusPropos[enCours:].replace(mot, '|'.join(graphiesDejcalejes), 1)
        return menusPropos
    
    ################################
    def afficheMot(self, mot, dejcalage):
        identifiantForme = self.qcLexique.trouveIdentifiant(mot.lower())
        print('1) identifiantForme=', identifiantForme)
        if identifiantForme == 0: return
        print( '2)')
        propriejtejs = self.qcFormes.trouveDonnejes(identifiantForme)
        for (numejroLemmeCat, genre, nombre, personne, temps) in propriejtejs:
            print(f'{numejroLemmeCat}, {genre}, {nombre}, {personne}, {temps}')
        print( '3)')
        idsFormesDejcalejes = set()
        for propriejtej in propriejtejs:
            idFormes = self.qcRejtroFormes.trouveFormesDejcalejes(propriejtej, dejcalage)
            print(idFormes)
            for idForme in idFormes: idsFormesDejcalejes.add(idForme)
        print( '4)')
        for idForme in idsFormesDejcalejes: 
            graphieDejcaleje = self.qcRejtroLexique.trouveGraphie(idForme)
            graphieDejcaleje = mesmeCasse(mot, graphieDejcaleje)
            print(f'{idForme} : {graphieDejcaleje}')
        
######################"""""        
# met la casse du mot origine sur le mot remplacsant
def mesmeCasse (origine, cible):
    if origine.islower(): return cible.lower()
    if origine.isupper(): return cible.upper()
    return cible[0].upper() + cible[1:].lower()
            
if __name__ == '__main__':
    main()
                
                
        
    
    
    
