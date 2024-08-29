#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "jys"
__copyright__ = "Copyright (C) 2024 LATEJCON"

import sys
from os import path
from codecs import open
import re
from QcLexique import QcLexique
from QcRejtroLexique import QcRejtroLexique
from Sp7Formes import Sp7Formes
from Sp7Lemmes import Sp7Lemmes
from Sp7Formes import L_ADJ, L_ADV, L_CONJ, L_DET, L_DIVERS, L_INTERJ
from Sp7Formes import L_NC, L_NP, L_PONCTU, L_PREP, L_PRON, L_V
from Sp7Formes import MASCULIN, FEJMININ, SINGULIER, PLURIEL, PERS_1, PERS_2, PERS_3
from Sp7Formes import INFINITIF, PART_PASSEJ, PART_PREJSENT, IMPEJRATIF, CONJUGUEJ
from Sp7Formes import COPULE
import sp7Modehles

def usage():
    script = '$PY/' + path.basename(sys.argv[0])
    print (f"""© l'ATEJCON.
Cherche une graphie particulière dans un système Sp7.
Affiche tout ce qui est trouvé.
On peut préciser une fenêtre pour examiner les lemmes suivants (ou précédents)
qui servent au remplacement.

usage   : {script} <racine fichiers> <graphie> [plage suivants]
usage   : {script} Splus7 ghâts
usage   : {script} Splus7 anniversaire 20
""")
def main():
    try:
        if len(sys.argv) < 3 : raise Exception()
        racine = sys.argv[1]
        graphie = sys.argv[2]
        if len(sys.argv) > 3: plage = int(sys.argv[3])
        else: plage =1
        chercheGraphie(racine, graphie, plage)
    except Exception as exc:
        if len(exc.args) == 0: usage()
        else:
            print ("******************************")
            print (exc.args[0])
            print ("******************************")
            raise
        sys.exit()
        
BLEU = "\033[1;34m"
MAGENTA = "\033[1;35m"
NORMAL = "\033[m"
txtMacro = {L_ADJ : "ADJ", L_ADV : "ADV", L_CONJ : "CONJ", L_DET : "DET", 
            L_NC : "NC", L_NP : "NP", L_PREP : "PREP", L_PRON : "PRON", L_V : "V"}
txt = {0 : "-", MASCULIN : "m", FEJMININ : "f", SINGULIER : "s", PLURIEL : "p", 
        PERS_1 : "1", PERS_2: "2", PERS_3 : "3", COPULE : "c",
        INFINITIF : "IN", PART_PASSEJ : "PP", PART_PREJSENT : "PR", IMPEJRATIF : "IM",
        CONJUGUEJ : "CJ"}
        
        
def chercheGraphie(racine, graphie, plage):
    # ouvre le lexique, rejtrolexique et les fichiers de formes et de lemmes 
    qcLexique = QcLexique(f'{racine}.sp7lexique')
    qcRejtroLexique = QcRejtroLexique(f'{racine}.sp7rejtrolexique')
    sp7Formes = Sp7Formes(f'{racine}.sp7formes')
    sp7Lemmes = Sp7Lemmes(f'{racine}.sp7lemmes')
    # trouve l'identifiant de la forme 
    identifiantForme = qcLexique.trouveIdentifiant(graphie.lower())
    print(f'identifiant {BLEU}{graphie.lower()}{NORMAL} = {identifiantForme}')
    
    # trouve les propriejtejs de la forme
    propriejtejs = sp7Formes.trouveDonnejes(identifiantForme)
    ejtiquettes = set()
    lemmes = set()
    for (identifiantLemme, macro, genre, nombre, personne, temps, divers) in propriejtejs:
        ejtiquette = txtMacro[macro] + txt[genre] + txt[nombre]  
        ejtiquettes.add(ejtiquette)
        lemmes.add(identifiantLemme)
    #print(f'propriejtejs forme {BLEU}{identifiantForme}{NORMAL} = {propriejtejs} = {BLEU}{ejtiquettes}{NORMAL}')
    print(f'propriejtejs forme {BLEU}{identifiantForme}{NORMAL} = {ejtiquettes}')
    print(f'lemmes forme {BLEU}{identifiantForme}{NORMAL} = {lemmes}')
    
    # trouve les propriejtejs de chaque lemme
    for lemmeId in lemmes:
        # ejtablit la liste des lemems ah afficher
        if lemmeId == 0: listeIds = [0]
        else:
            if plage > 0: listeIds = [idx for idx in range(lemmeId, lemmeId + plage)]
            else: listeIds = [idx for idx in reversed(range(lemmeId + plage +1, lemmeId +1))]
        couleur = BLEU
        for lemId in listeIds:
            macro = sp7Lemmes.trouveMacro(lemId)
            descFormes = sp7Lemmes.trouveDonnejes(lemId)
            #print(f'propriejtejs lemme {BLEU}{lemId}{NORMAL} = {macro} {descFormes}')
            propriejtejs = []
            for (identifiantForme, genre, nombre) in descFormes:
                ejtiquette = txtMacro[macro] + txt[genre] + txt[nombre]
                graphieForme = qcRejtroLexique.trouveGraphie(identifiantForme)
                propriejtejs.append(f'{couleur}{graphieForme}{NORMAL} {ejtiquette}')
            print(f'propriejtejs lemme {couleur}{lemId}{NORMAL} = {", ".join(propriejtejs)}')
            couleur = MAGENTA
            
 
if __name__ == '__main__':
        main()
