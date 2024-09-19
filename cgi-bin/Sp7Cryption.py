#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "jys"
__copyright__ = "Copyright (C) 2024 LATEJCON"

import sys
from os import path
import codecs
import re
from QcLexique import QcLexique
from QcRejtroLexique import QcRejtroLexique
from Sp7Formes import Sp7Formes
from Sp7Formes import L_ADJ, L_ADV, L_CONJ, L_DET, L_DIVERS, L_INTERJ
from Sp7Formes import L_NC, L_NP, L_PONCTU, L_PREP, L_PRON, L_V
from Sp7Formes import MASCULIN, FEJMININ, SINGULIER, PLURIEL, PERS_1, PERS_2, PERS_3
from Sp7Formes import INFINITIF, PART_PASSEJ, PART_PREJSENT, IMPEJRATIF, CONJUGUEJ
from Sp7Formes import COPULE
from Sp7Lemmes import Sp7Lemmes
import sp7Modehles

def usage():
    script = '$PY/' + path.basename(sys.argv[0])
    print (f"""© l'ATEJCON.
Programme de test de la classe Sp7Cryption.
Encrypte un menu propos en français par la quasi-cryption de l'Atejcon.

usage   : {script} <fichier texte | texte | mot> <racine fichiers> <décalage>
usage   : {script} menuPropos.txt Splusplus7 7
usage   : {script} menuPropos.txt Splusplus7 -7
usage   : {script} "le coq chante et la poule pond" Splusplus7 -7
""")

def main():
    try:
        if len(sys.argv) < 3 : raise Exception()
        texteOuNomFichier = sys.argv[1]
        racine = sys.argv[2]
        dejcalage = int(sys.argv[3])
        substitue(texteOuNomFichier, racine, dejcalage)
    except Exception as exc:
        if len(exc.args) == 0: usage()
        else:
            print ("******************************")
            print (exc.args[0])
            print ("******************************")
            raise
        sys.exit()

def substitue(texteOuNomFichier, racine, dejcalage):
    texteOuNomFichier = texteOuNomFichier.strip()
    sp7Cryption = Sp7Cryption(racine)
    if path.isfile(texteOuNomFichier):
        # lit le fichier d'entreje
        with codecs.open(texteOuNomFichier, 'r', 'utf-8') as fichierEntreje:
            entreje = fichierEntreje.read()
        print(entreje)
        entreje = sp7Cryption.cryptage(entreje, dejcalage)
        print(entreje)
        # ejcrit fichier quasi-cryptej
        nomSplit = texteOuNomFichier.split('.')
        nomFichierSortie = '.'.join(nomSplit[:-1]) + '-QC7.' + nomSplit[-1]
        with codecs.open(nomFichierSortie, 'w', 'utf-8') as fichierSortie:
            fichierSortie.write("--message quasi-crypté (cryptage symejtrique à clef publique). On peut le dejcrypter par la Quasi-Cryption de l'Atejon sur https://latejcon.art--\n\n")
            fichierSortie.write(entreje)
    elif len(texteOuNomFichier.split()) >1: 
        entreje = sp7Cryption.cryptage(texteOuNomFichier, dejcalage)
        print(entreje)
        vejrif = sp7Cryption.cryptage(entreje, -dejcalage)
        print(vejrif)
        if vejrif == texteOuNomFichier: print("Décryptage OK")
        else: print("Décryptage NOK")
    else: 
        sp7Cryption.afficheMot(texteOuNomFichier, dejcalage)
    sp7Cryption.close()
    
################################################################
txtMacro = {L_ADJ : "ADJ", L_ADV : "ADV", L_CONJ : "CONJ", L_DET : "DET", 
            L_NC : "NC", L_NP : "NP", L_PREP : "PREP", L_PRON : "PRON", L_V : "V"}
txt = {0 : "-", MASCULIN : "m", FEJMININ : "f", SINGULIER : "s", PLURIEL : "p", 
        PERS_1 : "1", PERS_2: "2", PERS_3 : "3", COPULE : "c",
        INFINITIF : "IN", PART_PASSEJ : "PP", PART_PREJSENT : "PR", IMPEJRATIF : "IM",
        CONJUGUEJ : "CJ"}
################################################################
class Sp7Cryption:
    def __init__(self, racine):
        # ouvre les 4 classes
        self.qcLexique = QcLexique(f'{racine}.sp7lexique')
        self.qcRejtroLexique = QcRejtroLexique(f'{racine}.sp7rejtrolexique')
        self.sp7Formes = Sp7Formes(f'{racine}.sp7formes')
        self.sp7Lemmes = Sp7Lemmes(f'{racine}.sp7lemmes')
        
    ################################
    def close(self):
        self.qcLexique.close()
        self.qcRejtroLexique.close()
        self.sp7Formes.close()
        self.sp7Lemmes.close()
        
    ################################
    def cryptage2(self, phrase, dejcalage):
        phraseSubs = self.cryptage(phrase, dejcalage)
        # remplace les \n par <br/>
        phraseSubs = phraseSubs.replace('\n', '<br/>')
        return phraseSubs
        
    ################################
    def cryptage(self, phrase, dejcalage):
        # remplace les apostrophes bizarres
        phrase = phrase.replace('’', "'").replace('‘', "'")
        # si pas de dejcalage, raf
        if dejcalage == 0: return phrase
        # on garde la phrase originale
        phrase2 = phrase.strip()
        if phrase2 == '': return phrase
        # double les apostrophes par des espaces
        phrase2 = phrase2.replace("'", "' ")
        # Ejtiquette la phrase
        phraseEjtiqueteje = []
        #####
        # 1) sejpare tous les mots du texte par espaces, points et apostrophes, pas les tirets
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
            identifiantForme = self.qcLexique.trouveIdentifiant(mot.lower())
            # si forme inconnue, raf
            if identifiantForme == 0: continue
            # trouve les propriejtejs de la forme
            propriejtejs = self.sp7Formes.trouveDonnejes(identifiantForme)
            ejtiquettes = set()
            macrolemmes = set()
            for (identifiantLemme, macro, genre, nombre, personne, temps, divers) in propriejtejs:
                ejtiquette = txtMacro[macro] + txt[genre] + txt[nombre]
                # pour les verbes, on ajoute le temps
                if temps != 0: ejtiquette += txt[temps]
                phraseEjtiqueteje[-1][3][ejtiquette] = identifiantLemme
            ejtiquettes = list(phraseEjtiqueteje[-1][3].keys())
            phraseEjtiqueteje[-1][2] = ejtiquettes
        #####
        # 2) invalide les NCxx interdits et les NCxx commencant par une majuscule
        for idxMot in range(len(phraseEjtiqueteje)):
            (mot, index, ejtiquettes, ejtiqlemmes, choix) = phraseEjtiqueteje[idxMot]
            #if mot[0].islower() and mot not in sp7Modehles.sp7NcInterdits: continue
            if mot not in sp7Modehles.sp7NcInterdits: continue
            nouvelleEjtiquettes = []
            for ejtiquette in ejtiquettes: 
                if not ejtiquette.startswith('NC'): nouvelleEjtiquettes.append(ejtiquette)
            phraseEjtiqueteje[idxMot][2] = nouvelleEjtiquettes
        #####
        # 3) Essaie tous les modehles ah partir de chaque mot
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
        #####
        # 4) fait le mejnage dans les modehles
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
        for numEffacej in aEffacer: 
            if numEffacej in modehlesOk: modehlesOk.remove(numEffacej)
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
        #####
        # 5) ejtablit le plan de substitution
        substantifs = []
        for (modehle, idx1erMot) in modehlesOk:
            numsGenre = []
            avecNC = False
            for idxMod in range(len(modehle)):
                phraseEjtiqueteje[idx1erMot + idxMod][4] = modehle[idxMod]
                if modehle[idxMod][:2] == 'NC': 
                    numSubs = idx1erMot + idxMod
                    avecNC = True
                if modehle[idxMod][-2:-1] in ('f', 'm'): numsGenre.append(idx1erMot + idxMod)
            if avecNC: substantifs.append((numSubs, numsGenre))
        #####
        # 6) substitution des NC
        phraseSubs = phrase
        for (numSubs, numsGenre) in substantifs[::-1]:
            # le NC d'origine
            ancienNC = phraseEjtiqueteje[numSubs][0]
            ejtiquette = phraseEjtiqueteje[numSubs][4]
            # trouve le lemme du NC substitej
            idLemmeNC = phraseEjtiqueteje[numSubs][3][ejtiquette]
            # si le lemme est inconnu, on ne fait rien
            if idLemmeNC == 0: continue
            # trouve le NC substituant
            nouveauNC, nouvelleEjtiquette = self.trouveSubstituant(idLemmeNC, ejtiquette, dejcalage)
            nouveauNC = mesmeCasse(ancienNC, nouveauNC)
            indexMot = phraseEjtiqueteje[numSubs][1]
            phraseSubs = phraseSubs[:indexMot] + phraseSubs[indexMot:].replace(ancienNC, nouveauNC, 1)
        return phraseSubs
    
    ################################
    def trouveSubstituant(self, idLemmeNC, ejtiquette, dejcalage):
        # dans les 2 sens
        if dejcalage >0 : 
            compteur = dejcalage
            increjment = 1
        else:
            compteur = -dejcalage
            increjment = -1
        pluriel = ejtiquette[-1] == 'p'
        masculin = ejtiquette[-2] == 'm'
        maxIdentifiant = self.sp7Lemmes.donneNombreEntrejesFichier()
        while compteur > 0:
            idLemmeNC += increjment
            if idLemmeNC >= maxIdentifiant: idLemmeNC = 1
            if idLemmeNC == 0: idLemmeNC = maxIdentifiant
            # cherche NC de mesme genre
            macro = self.sp7Lemmes.trouveMacro(idLemmeNC)
            if macro != L_NC: continue
            descFormes = self.sp7Lemmes.trouveDonnejes(idLemmeNC)
            for (identifiantForme, genre, nombre) in descFormes:
                # True si genres diffejrents, nombres diffejrents
                if masculin ^ (genre == MASCULIN): continue
                if pluriel ^ (nombre == PLURIEL): continue
                nouveauNC = self.qcRejtroLexique.trouveGraphie(identifiantForme)
                # si graphie interdite, on la saute
                if nouveauNC in sp7Modehles.sp7NcInterdits: continue
                nouvelleEjtiquette = txtMacro[L_NC] + txt[genre] + txt[nombre]
                compteur -=1
                break
        return nouveauNC, nouvelleEjtiquette 
    
    ################################
    def afficheMot(self, mot, dejcalage):
        # trouve l'identifiant de la forme 
        identifiantForme = self.qcLexique.trouveIdentifiant(mot.lower())
        print('1) identifiantForme=', identifiantForme)
        # si forme inconnue, raf
        if identifiantForme == 0: return
        # trouve les propriejtejs de la forme
        print( '2) propriétés de la forme :')
        propriejtejs = self.sp7Formes.trouveDonnejes(identifiantForme)
        lesSubstantifs = []
        for (identifiantLemme, macro, genre, nombre, personne, temps, divers) in propriejtejs:
            ejtiquette = txtMacro[macro] + txt[genre] + txt[nombre]
            print(f'{identifiantLemme}, {ejtiquette}, {personne}, {temps}, {divers}')
            if macro == L_NC: lesSubstantifs.append((identifiantLemme, ejtiquette))
        # trouve les formes dejcalejes 
        print( '3) formes décalées :')
        for (identifiantLemme, ejtiquette) in lesSubstantifs:
            nouveauNC, nouvelleEjtiquette = self.trouveSubstituant(identifiantLemme, ejtiquette, dejcalage)
            print(f'{mot}, {identifiantLemme}, {ejtiquette} ==> {nouveauNC}, {nouvelleEjtiquette}')
            
######################
# met la casse du mot origine sur le mot remplacsant
def mesmeCasse (origine, cible):
    if origine.islower(): return cible.lower()
    if origine.isupper(): return cible.upper()
    return cible[0].upper() + cible[1:].lower()
            
if __name__ == '__main__':
    main()
                
