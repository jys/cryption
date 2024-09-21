#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "jys"
__copyright__ = "Copyright (C) 2024 LATEJCON"

import sys
from os import path
from codecs import open
from Sp7Cryption import Sp7Cryption


def usage():
    script = '$PY/' + path.basename(sys.argv[0])
    print (f"""© l'ATEJCON.
Analyse de la quasi-cryption.
Plusieurs utilisations :
o cryption d'un texte ou d'un fichier dans son entièreté
o cryption d'un texte ou d'un fichier phrase par phrase avec plusieurs
  niveaux de traces possibles (A, B, C, D, E)
Ce programme utilise l'analyse syntaxique et le substituteur communs.
Pas de trace : entièreté
A : ligne par ligne en cas de fichier
B : avec marquage des groupes nominaux reconnus et des NC substitués
C : + substitution
D : + modèles
E : + étiquetage

usage   : {script} <racine> <décalage> <texte|fichier> [<trace(A,B,C)>]
usage   : {script} Lat4 7 "les familles heureuses se ressemblent toutes"
usage   : {script} Lat2 -5 MadameBovary.txt B
""")

def main():
    try:
        if len(sys.argv) < 4 : raise Exception()
        racine = sys.argv[1]
        dejcalage = int(sys.argv[2])
        texteOuFichier = sys.argv[3]
        trace = 'Z'
        if len(sys.argv) > 4 : 
            trace = sys.argv[4]
            if trace not in ('ABCDE'): raise Exception()
        analyses(racine, dejcalage, texteOuFichier, trace)
    except Exception as exc:
        if len(exc.args) == 0: usage()
        else:
            print ("******************************")
            print (exc.args[0])
            print ("******************************")
            raise
        sys.exit()

def analyses(racine, dejcalage, texteOuFichier, trace):
    sp7Cryption = Sp7Cryption('ressources/' + racine)
    if path.isfile(texteOuFichier):
        with open(texteOuFichier, 'r', 'utf-8') as texteEnFichier:
            for texte in texteEnFichier:
                texte = texte.strip()
                if texte == "": continue
                texteSubst = sp7Cryption.cryptage(texte, dejcalage, trace)
                if trace not in ('BCDE'): print(texteSubst)
                # si trace clique pour § suivant
                if trace != 'Z': input('')
    else:
        texteSubst = sp7Cryption.cryptage(texteOuFichier, dejcalage, trace)
        if trace not in ('BCDE'): print(texteSubst)
    sp7Cryption.close()
    
 
if __name__ == '__main__':
        main()
       
