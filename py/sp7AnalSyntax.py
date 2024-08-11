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
De base, les substantifs et leur groupe nominal sont affichés
en alternance de couleurs bleue et rouge.
Ainsi que le texte post-substitution.
Il y a possibilité d'avoir plusieurs niveaux de traces supplémentaires 
(A, B, C, D), le niveau D étant par défaut.

usage   : {script} <racine fichiers> <texte ou fichier texte> [<trace(A,B,C)>]
usage   : {script} Splus7 "les familles heureuses se ressemblent toutes"
usage   : {script} Splus7 MadameBovary.txt B
""")

def main():
    try:
        if len(sys.argv) < 3 : raise Exception()
        racine = sys.argv[1]
        texteOuFichier = sys.argv[2]
        trace = 'D'
        if len(sys.argv) > 3 : 
            trace = sys.argv[3]
            if trace not in ('ABCD'): raise Exception()
        analyses(racine, texteOuFichier, trace)
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

def analyses(racine, texteOuFichier, trace):
    if path.isfile(texteOuFichier):
        with open(texteOuFichier, 'r', 'utf-8') as texteEnFichier:
            for texte in texteEnFichier:
                texte = texte.strip()
                if texte == "": continue
                analyseParagraphe(racine, texte, trace)  
                # clique pour § suivant
                input('')
    else:
        analyseParagraphe(racine, texteOuFichier, trace)
    
def analyseParagraphe(racine, texteOuFichier, trace):
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
        # sejpare tous les mots du texte par espaces, points et apostrophes, pas les tirets
        mots = re.split("\s+|\"|\.+|\(|\)|;|,", phrase2)
        indexDansPhrase = 0
        for mot in mots:
            mot = mot.strip()
            if mot == '': continue
            # trouve son index dans la phrase d'origine
            indexDansPhrase = phrase.find(mot, indexDansPhrase)
            # creje l'entreje
            phraseEjtiqueteje.append([mot, indexDansPhrase, [], {}, ''])
            # trouve l'identifiant de la forme 
            identifiantForme = qcLexique.trouveIdentifiant(mot.lower())
            # si forme inconnue, raf
            if identifiantForme == 0: continue
            # trouve les propriejtejs de la forme
            propriejtejs = sp7Formes.trouveDonnejes(identifiantForme)
            #print('propriejtejs=', propriejtejs)
            for (identifiantLemme, macro, genre, nombre, personne, temps, divers) in propriejtejs:
                ejtiquette = txtMacro[macro] + txt[genre] + txt[nombre]
                phraseEjtiqueteje[-1][3][ejtiquette] = identifiantLemme
            ejtiquettes = list(phraseEjtiqueteje[-1][3].keys())
            phraseEjtiqueteje[-1][2] = ejtiquettes
        if trace in 'A': print ('\nphraseEjtiqueteje1=', phraseEjtiqueteje)
        # invalide les NCxx interdits et les NCxx commencant par une majuscule
        for idxMot in range(len(phraseEjtiqueteje)):
            (mot, index, ejtiquettes, ejtiqlemmes, choix) = phraseEjtiqueteje[idxMot]
            if mot[0].islower() and mot not in sp7Modehles.sp7NcInterdits: continue
            nouvelleEjtiquettes = []
            for ejtiquette in ejtiquettes: 
                if not ejtiquette.startswith('NC'): nouvelleEjtiquettes.append(ejtiquette)
            phraseEjtiqueteje[idxMot][2] = nouvelleEjtiquettes
        if trace in 'A': print ('\nphraseEjtiqueteje2=', phraseEjtiqueteje)
        # affiche la phrase ejtiqueteje en plus clair        
        affichageEjtiquetej = ""
        for (mot, index, ejtiquettes, ejtiqlemmes, choix) in phraseEjtiqueteje:
            affichageEjtiquetej += f'{BLEU}{mot}{NORMAL} ' + ' '.join(ejtiquettes) + ' '
            for (ejtiq, identLemme) in ejtiqlemmes.items():
                affichageEjtiquetej += f'({ejtiq} : {identLemme}) '
        if trace in 'A': print('\naffichageEjtiquetej=', affichageEjtiquetej)
        
        # Essaie tous les modehles ah partir de chaque mot
        modehlesOk = []
        for idx1erMot in range(len(phraseEjtiqueteje)):
            for sp7Modehle in sp7Modehles.sp7Modehles :
                modehle = sp7Modehle.split()
                for idxMod in range(len(modehle)):
                    # si fin de texte avant fin de modehle, modehle suivant
                    if idx1erMot + idxMod == len(phraseEjtiqueteje): break
                    # si mot hors modehle, modehle suivant
                    if modehle[idxMod] not in phraseEjtiqueteje[idx1erMot + idxMod][2]: break
                    # si arrivej au bout du modehle, c'est gagnej !
                    if idxMod == len(modehle) -1:  
                        modehlesOk.append((modehle, idx1erMot))
        if trace in ('AB'): print('\nmodehlesOk1=', modehlesOk)
        
        # fait le mejnage dans les modehles
        aEffacer = []
        # les modehles ejtant uniques, il ne peut y avoir de doublon dans la liste
        for (modehleA, idx1erMotA) in modehlesOk:
            for (modehleB, idx1erMotB) in modehlesOk:
                # si 2 modehles sont supeposables, on verra plus tard
                if idx1erMotA == idx1erMotB and len(modehleA) == len(modehleB): continue
                # on vire si un modhele est inclus dans l'autre
                if idx1erMotA <= idx1erMotB and idx1erMotA + len(modehleA) >= idx1erMotB + len(modehleB):
                    aEffacer.append((modehleB, idx1erMotB))
                elif idx1erMotB <= idx1erMotA and idx1erMotB + len(modehleB) >= idx1erMotA + len(modehleA):
                    aEffacer.append((modehleA, idx1erMotA))
        if trace in ('AB'): print('\naEffacer=', aEffacer)
        for numEffacej in aEffacer: 
            if numEffacej in modehlesOk: modehlesOk.remove(numEffacej)
        if trace in ('AB'): print('\nmodehlesOk2=', modehlesOk)
        # garde uniquement le dernier des superposables
        if len(modehlesOk) != 0:
            aEffacer = []
            (modehleA, idx1erMotA) = modehlesOk[0]
            for (modehleB, idx1erMotB) in modehlesOk[1:]:
                if idx1erMotA == idx1erMotB and len(modehleA) == len(modehleB):
                    aEffacer.append((modehleA, idx1erMotA))
                (modehleA, idx1erMotA) = (modehleB, idx1erMotB)
            for numEffacej in aEffacer: 
                if numEffacej in modehlesOk: modehlesOk.remove(numEffacej)
        if trace in ('AB'): print('\nmodehlesOk3=', modehlesOk)
        # vejrifie les chevauchements
        for (modehleA, idx1erMotA) in modehlesOk:
            for (modehleB, idx1erMotB) in modehlesOk:
                if idx1erMotB > idx1erMotA and idx1erMotB < idx1erMotA + len(modehleA):
                    print('CHEVAUCHEMENT :', (modehleA, idx1erMotA), (modehleB, idx1erMotB))
                if idx1erMotB + len(modehleB) > idx1erMotA and idx1erMotB + len(modehleB) < idx1erMotA + len(modehleA):
                    print('CHEVAUCHEMENT :', (modehleA, idx1erMotA), (modehleB, idx1erMotB))
         
        # ejtablit le plan de substitution
        substantifs = []
        for (modehle, idx1erMot) in modehlesOk:
            numsGenre = []
            for idxMod in range(len(modehle)):
                phraseEjtiqueteje[idx1erMot + idxMod][4] = modehle[idxMod]
                if modehle[idxMod][:2] == 'NC': numSubs = idx1erMot + idxMod
                if modehle[idxMod][-2:-1] in ('f', 'm'): numsGenre.append(idx1erMot + idxMod)
            substantifs.append((numSubs, numsGenre))
        if trace in ('ABC'): print('\nsubstantifs=', substantifs)
        if trace in ('ABC'): print('\nphraseEjtiqueteje=', phraseEjtiqueteje)
        
        # affiche phrase analyseje
        phraseCouleur = phrase
        coulSubs = [ROUGE_SUBS, BLEU_SUBS]
        coulGenr = [ROUGE_GENR, BLEU_GENR]
        nbSubst = 0
        for (numSubs, numsGenre) in substantifs[::-1]:
            nbSubst +=1
            for numMot in numsGenre[::-1]:
                mot = phraseEjtiqueteje[numMot][0]
                if numMot == numSubs: couleur = coulSubs[nbSubst%2]
                else: couleur = coulGenr[nbSubst%2]
                indexMot = phraseEjtiqueteje[numMot][1]
                nouveauMot = f'{couleur}{mot}{NORMAL}'
                phraseCouleur = phraseCouleur[:indexMot] + phraseCouleur[indexMot:].replace(mot, nouveauMot, 1)
        if trace in ('ABCD'): print('\n', phraseCouleur)
        #print (hexString(phraseCouleur))
        
        #substitution des NC
        phraseSubs = phrase
        for (numSubs, numsGenre) in substantifs[::-1]:
            # le NC d'origine
            ejtiquette = phraseEjtiqueteje[numSubs][4]
            #print('mot=', phraseEjtiqueteje[numSubs][0])
            #print('ejtiquette=', ejtiquette)
            pluriel = ejtiquette[-1] == 'p'
            masculin = ejtiquette[-2] == 'm'
            # trouve le lemme du NC substituej
            idLemmeNC = phraseEjtiqueteje[numSubs][3][ejtiquette]
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
                    # True si genres diffejrents, nombres diffejrents
                    if masculin ^ (genre == MASCULIN): continue
                    if pluriel ^ (nombre == PLURIEL): continue
                    nouveauNC = qcRejtroLexique.trouveGraphie(identifiantForme)
                    # si graphie interdite, on la saute
                    if nouveauNC in sp7Modehles.sp7NcInterdits: continue
                    compteur -=1
                    break
                ## de mesme genre ?
                #if masculin ^ (genre == FEJMININ): compteur -=1                
            ## on a le nouveau NC et ses formes
            #nouveauNC = 'ERREUR1'
            #for (identifiantForme, genre, nombre) in descFormes:
                ## trouve la forme qui a le mesme nombre et le mesme genre
                #if (pluriel ^ (nombre == SINGULIER)) and (masculin ^ (genre == FEJMININ)): 
                    #nouveauNC = qcRejtroLexique.trouveGraphie(identifiantForme)
                    #break
            changementGenre = masculin ^ (genre == MASCULIN)
            #print('masculin=', masculin)
            #print('identifiantForme=', identifiantForme)
            #print('genre=', genre)
            #print('nombre=', nombre)
            #print('changementGenre=', changementGenre)
            # changement du groupe nominal
            for numMot in numsGenre[::-1]:
                mot = phraseEjtiqueteje[numMot][0]
                indexMot = phraseEjtiqueteje[numMot][1]
                if numMot == numSubs:
                    phraseSubs = phraseSubs[:indexMot] + phraseSubs[indexMot:].replace(mot, f'{BLEU}{nouveauNC}{NORMAL}', 1)
                elif changementGenre:
                    # remplacement des changements de genres
                    ejtiquette = phraseEjtiqueteje[numMot][4]
                    idLemme = phraseEjtiqueteje[numMot][3][ejtiquette]
                    descFormes = sp7Lemmes.trouveDonnejes(idLemme)
                    nouveauMot = 'ERREUR2'
                    for (identifiantForme, genre, nombre) in descFormes:
                        # trouve celle qui a le mesme nombre et le genre opposé
                        # False si nombres identiques et genres diffejrents
                        # True si nombres diffejrents ou genres identiques
                        if (pluriel ^ (nombre == PLURIEL)) or (masculin ^ (genre == FEJMININ)): continue
                        nouveauMot = qcRejtroLexique.trouveGraphie(identifiantForme)
                        break
                    phraseSubs = phraseSubs[:indexMot] + phraseSubs[indexMot:].replace(mot, nouveauMot, 1)
                else: continue
        print('\n', phraseSubs)
        
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
       
