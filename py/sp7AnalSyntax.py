#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "jys"
__copyright__ = "Copyright (C) 2023 LATEJCON"

import sys
from os import path
from codecs import open
import re
from QcLexique import QcLexique
from QcRejtroLexique import QcRejtroLexique
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
Analyse syntaxique de phrases.

usage   : {script} <racine fichiers> <texte ou fichier texte>
usage   : {script} Splus7 "les familles heureuses se ressemblent toutes"
usage   : {script} Splus7 MadameBovary.txt 
""")

def main():
    try:
        if len(sys.argv) < 3 : raise Exception()
        racine = sys.argv[1]
        texteOuFichier = sys.argv[2]
        analyses(racine, texteOuFichier)
    except Exception as exc:
        if len(exc.args) == 0: usage()
        else:
            print ("******************************")
            print (exc.args[0])
            print ("******************************")
            raise
        sys.exit()

BLEU = "\033[1;34m"
BLEUBLEU = "\033[1;94m"
MAGENTA = "\033[1;35m"
ROUGE = "\033[1;31m"
CYAN = "\033[1;36m"
NORMAL = "\033[m"
GRIS = "\033[47m"
JAUNE = "\033[43m"
BLANC = "\033[107m"
BLEU_SUBS = "\033[1;4;34m"
BLEU_GENR = "\033[1;3;34m"
ROUGE_SUBS = "\033[1;4;31m"
ROUGE_GENR = "\033[1;3;31m"
SPLUS7 = 7

txtMacro = {L_ADJ : "ADJ", L_ADV : "ADV", L_CONJ : "CONJ", L_DET : "DET", 
            L_NC : "NC", L_NP : "NP", L_PREP : "PREP", L_PRON : "PRON", L_V : "V"}
txt = {0 : "-", MASCULIN : "m", FEJMININ : "f", SINGULIER : "s", PLURIEL : "p", 
        PERS_1 : "1", PERS_2: "2", PERS_3 : "3", COPULE : "c",
        INFINITIF : "IN", PART_PASSEJ : "PP", PART_PREJSENT : "PR", IMPEJRATIF : "IM",
        CONJUGUEJ : "CJ"}

def analyses(racine, texteOuFichier):
    if path.isfile(texteOuFichier):
        with open(texteOuFichier, 'r', 'utf-8') as texteEnFichier:
            for texte in texteEnFichier:
                texte = texte.strip()
                if texte == "": continue
                analyseParagraphe(racine, texte)  
                # clique pour § suivant
                input('')
    else:
        analyseParagraphe(racine, texteOuFichier)
    
def analyseParagraphe(racine, texteOuFichier):
    # ouvre le lexique, rejtrolexique et les fichiers de formes et de lemmes 
    qcLexique = QcLexique(f'{racine}.sp7lexique')
    qcRejtroLexique = QcRejtroLexique(f'{racine}.sp7rejtrolexique')
    sp7Formes = Sp7Formes(f'{racine}.sp7formes')
    sp7Lemmes = Sp7Lemmes(f'{racine}.sp7lemmes')
    # texte ou fichier
    if path.isfile(texteOuFichier):
        with open(texteOuFichier, 'r', 'utf-8') as texteEnFichier:
            texte = texteEnFichier.read()
    else:
        texte = texteOuFichier
    phrases = re.split("\.|;", texte)
    # on traite § par §
    for phrase in phrases:
        # on garde la phrase originale
        phrase2 = phrase.strip()
        if phrase2 == '': continue
        # double les apostrophes par des espaces
        phrase2 = phrase2.replace("'", "' ")
        # Ejtiquette la phrase
        phraseEjtiqueteje = []
        # sejpare tous les mots du texte par espaces, tirets, points et apostrophes
        mots = re.split("\s+|-|\"|\.+|\(|\)|;|,", phrase2)
        for mot in mots:
            mot = mot.strip()
            if mot == '': continue
            # creje l'entreje
            phraseEjtiqueteje.append([mot, [], {}, ''])
            # trouve l'identifiant de la forme 
            identifiantForme = qcLexique.trouveIdentifiant(mot.lower())
            # si forme inconnue, raf
            if identifiantForme == 0: continue
            # trouve les propriejtejs de la forme
            propriejtejs = sp7Formes.trouveDonnejes(identifiantForme)
            ejtiquettes = set()
            macrolemmes = set()
            for (identifiantLemme, macro, genre, nombre, personne, temps, divers) in propriejtejs:
                ejtiquette = txtMacro[macro] + txt[genre] + txt[nombre]
                phraseEjtiqueteje[-1][2][ejtiquette] = identifiantLemme
            ejtiquettes = list(phraseEjtiqueteje[-1][2].keys())
            phraseEjtiqueteje[-1][1] = ejtiquettes
        #print (phraseEjtiqueteje)
        affichageEjtiquetej = ""
        for [mot, ejtiquettes, ejtiqlemmes, choix] in phraseEjtiqueteje:
            affichageEjtiquetej += f'{BLEU}{mot}{NORMAL} ' + ' '.join(ejtiquettes) + ' '
            for (ejtiq, identLemme) in ejtiqlemmes.items():
                affichageEjtiquetej += f'({ejtiq} : {identLemme}) '
        #print(affichageEjtiquetej)
        
        # Essaie tous les modehles au dejbut de chaque mot
        modehlesOk = []
        for idx1erMot in range(len(phraseEjtiqueteje)):
            for sp7Modehle in sp7Modehles.sp7Modehles :
                modehle = sp7Modehle.split()
                for idxMod in range(len(modehle)):
                    # si fin de texte avant fin de modehle, modehle suivant
                    if idx1erMot + idxMod == len(phraseEjtiqueteje): break
                    # si mot hors modehle, modehle suivant
                    if modehle[idxMod] not in phraseEjtiqueteje[idx1erMot + idxMod][1]: break
                    # si arrivej au bout du modhle, c'est gagnej !
                    if idxMod == len(modehle) -1:  
                        modehlesOk.append((modehle, idx1erMot))
        #print(modehlesOk)
        
        # fait le mejnage dans les modehles
        modehlesParMot = [[] for x in range(len(phraseEjtiqueteje))]
        for idxModOk in range(len(modehlesOk)):
            (modehle, idx1erMot) = modehlesOk[idxModOk]
            for idxMod in range(len(modehle)):
                modehlesParMot[idx1erMot + idxMod].append(idxModOk)
        # vire les modehles en collision
        aEffacer = []
        for numModehles in modehlesParMot:
            if len(numModehles) <2 : continue
            refModehle = numModehles[0]
            for numModehle in numModehles[1:]:
                if len(modehlesOk[numModehle][0]) < len(modehlesOk[refModehle][0]):
                    aEffacer.append(numModehle)
                elif len(modehlesOk[numModehle][0]) > len(modehlesOk[refModehle][0]):
                    aEffacer.append(refModehle)
                    refModehle = numModehle
                else:
                    aEffacer.append(numModehle)
                    aEffacer.append(refModehle)
        aEffacer= list(set(aEffacer))
        aEffacer.sort(reverse=True)
        for numEffacej in aEffacer: modehlesOk.pop(numEffacej)
        #print(modehlesOk)
        
        # ejtablit le plan de substitution
        substantifs = []
        for (modehle, idx1erMot) in modehlesOk:
            numsGenre = []
            for idxMod in range(len(modehle)):
                phraseEjtiqueteje[idx1erMot + idxMod][3] = modehle[idxMod]
                if modehle[idxMod][:2] == 'NC': numSubs = idx1erMot + idxMod
                if modehle[idxMod][-2:-1] in ('f', 'm'): numsGenre.append(idx1erMot + idxMod)
            substantifs.append((numSubs, numsGenre))
        #print(substantifs)
        #print(phraseEjtiqueteje)
        
        # affiche phrase analyseje
        phraseCouleur = phrase
        coulSubs = [ROUGE_SUBS, BLEU_SUBS]
        coulGenr = [ROUGE_GENR, BLEU_GENR]
        nbSubst = 0
        enCours = len(phraseCouleur)
        for (numSubs, numsGenre) in substantifs[::-1]:
            nbSubst +=1
            for numMot in numsGenre[::-1]:
                mot = phraseEjtiqueteje[numMot][0]
                if numMot == numSubs: couleur = coulSubs[nbSubst%2]
                else: couleur = coulGenr[nbSubst%2]
                enCours = phraseCouleur.rfind(mot, 0, enCours)
                nouveauMot = f'{couleur}{mot}{NORMAL}'
                phraseCouleur = phraseCouleur[:enCours] + phraseCouleur[enCours:].replace(mot, nouveauMot, 1)
        #print(phraseCouleur)
        #print (hexString(phraseCouleur))
        
        #substitution des NC
        phraseSubs = phrase
        enCours = len(phraseSubs)
        for (numSubs, numsGenre) in substantifs[::-1]:
            # le NC d'origine
            ejtiquette = phraseEjtiqueteje[numSubs][3]
            #print('mot=', phraseEjtiqueteje[numSubs][0])
            #print('ejtiquette=', ejtiquette)
            pluriel = ejtiquette[-1] == 'p'
            masculin = ejtiquette[-2] == 'm'
            # trouve le lemme du NC substitej
            idLemmeNC = phraseEjtiqueteje[numSubs][2][ejtiquette]
            # si le lemme est inconnu, on ne fait rien
            if idLemmeNC == 0: continue
            # trouve le NC substituant
            compteur = SPLUS7
            maxIdentifiant = sp7Lemmes.donneNombreEntrejesFichier()
            while compteur > 0:
                idLemmeNC +=1
                if idLemmeNC >= maxIdentifiant: idLemmeNC = 1
                ## cherche n'importe quel NC 
                #macro = sp7Lemmes.trouveMacro(idLemmeNC)
                #if macro == L_NC: compteur -=1
                # cherche NC de mesme genre
                macro = sp7Lemmes.trouveMacro(idLemmeNC)
                if macro != L_NC: continue
                descFormes = sp7Lemmes.trouveDonnejes(idLemmeNC)
                for (identifiantForme, genre, nombre) in descFormes:
                    # True si genres diffejrents
                    if masculin ^ (genre == MASCULIN): continue
                # de mesme genre ?
                if masculin ^ (genre == FEJMININ): compteur -=1                
            # on a le nouveau NC et ses formes
            nouveauNC = 'ERREUR1'
            for (identifiantForme, genre, nombre) in descFormes:
                # trouve la forme qui a le mesme nombre et le mesme genre
                if (pluriel ^ (nombre == SINGULIER)) and (masculin ^ (genre == FEJMININ)): 
                    nouveauNC = qcRejtroLexique.trouveGraphie(identifiantForme)
                    break
            changementGenre = masculin ^ (genre == MASCULIN)
            #print('masculin=', masculin)
            #print('identifiantForme=', identifiantForme)
            #print('genre=', genre)
            #print('nombre=', nombre)
            #print('changementGenre=', changementGenre)
            # changement du groupe nominal
            for numMot in numsGenre[::-1]:
                mot = phraseEjtiqueteje[numMot][0]
                if numMot == numSubs:
                    enCours = phraseSubs.rfind(mot, 0, enCours)
                    phraseSubs = phraseSubs[:enCours] + phraseSubs[enCours:].replace(mot, f'{BLEU}{nouveauNC}{NORMAL}', 1)
                elif changementGenre:
                    # remplacement des changements de genres
                    ejtiquette = phraseEjtiqueteje[numMot][3]
                    idLemme = phraseEjtiqueteje[numMot][2][ejtiquette]
                    descFormes = sp7Lemmes.trouveDonnejes(idLemme)
                    nouveauMot = 'ERREUR2'
                    for (identifiantForme, genre, nombre) in descFormes:
                        # trouve celle qui a le mesme nombre et le genre opposé
                        # False si nombres identiques et genres diffejrents
                        # True si nombres diffejrents ou genres identiques
                        if (pluriel ^ (nombre == PLURIEL)) or (masculin ^ (genre == FEJMININ)): continue
                        nouveauMot = qcRejtroLexique.trouveGraphie(identifiantForme)
                        break
                    enCours = phraseSubs.rfind(mot, 0, enCours)
                    phraseSubs = phraseSubs[:enCours] + phraseSubs[enCours:].replace(mot, nouveauMot, 1)
                else: continue
        print(phraseSubs)
        
    sp7Lemmes.close()
    sp7Formes.close()
    qcRejtroLexique.close()
    qcLexique.close()
    
#decode une chaine de caracteres en hexadecimal
def hexString(string):
    result = ''
    for char in string:
        result += oct(ord(char))+"'"+char+"'"+', '
    result += '\n'
    return result
       
 
if __name__ == '__main__':
        main()
       
