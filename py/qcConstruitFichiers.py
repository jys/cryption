#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "jys"
__copyright__ = "Copyright (C) 2021 LATEJCON"

import sys
from os import path
import LateconResLingBase
import codecs
import re
from QcLexique import QcLexique
from QcRejtroLexique import QcRejtroLexique
from QcFormes import QcFormes
from QcFormes import MASCULIN, FEJMININ, SINGULIER, PLURIEL, PERS_1, PERS_2, PERS_3
from QcFormes import PREJSENT, IMPARFAIT, PASSEJ, FUTUR, CONDITIONNEL 
from QcRejtroFormes import QcRejtroFormes
from QcRejtroFormes import CAT_ADV, CAT_SUBM, CAT_SUBF, CAT_VER, CAT_PPR, CAT_PPA
import numpy

def usage():
    script = '$PY/' + path.basename(sys.argv[0])
    print (f"""© l'ATEJCON.
Construction les fichiers plats de la quasi-cryption de l'Atejcon.
Les fichiers plats sont :
    <racine>.qclexique
    <racine>.qcrejtrolexique
    <racine>.qcformes
    <racine>.qcrejtroformes

usage   : {script} <racine fichiers> [<forme testée>]
usage   : {script} Latejcon
usage   : {script} Latejcon choisis
""")

def main():
    try:
        if len(sys.argv) < 2 : raise Exception()
        racine = sys.argv[1]
        if len(sys.argv) > 2 : formeTesteje = sys.argv[2].strip()
        else: formeTesteje = ''
        construit(racine, formeTesteje)
    except Exception as exc:
        if len(exc.args) == 0: usage()
        else:
            print ("******************************")
            print (exc.args[0])
            print ("******************************")
            raise
        sys.exit()

FRE = 145
L_ADJ = 1
L_NC = 10
L_ADV = 2
L_V= 16
L_MASC = 1422
L_FEM = 1423
L_SING = 1425
L_PLUR = 1426
L_1 = 1428
L_2 = 1429
L_3 = 1430
L_PRES = 1435
L_IMPFT = 1436
L_PASS = 1437
L_FUTUR = 1438
L_COND_PRES = 1439
L_VERBE_PRINCIPAL_INFINITIF = 1559
L_VERBE_PRINCIPAL_PARTICIPE_PRESENT = 1560
L_VERBE_PRINCIPAL_PARTICIPE_PASSE = 1561

TAILLE_HASH = 100019
    
def construit(racine, formeTesteje):
    enTest = formeTesteje != ''
    
    # 1) si la sauvegarde numpy n'est pas lah, la creje
    nomNumpy = racine + '.npy'
    if not path.isfile(nomNumpy):
        base = LateconResLingBase.LateconResLingBase()
        lesFormes = list(trouveFormes(base))
        base.close()
        print(f"{len(lesFormes)} formes trouvées dans la base de l'Atejcon")
        npLesFormes = numpy.array(lesFormes)
        numpy.save(nomNumpy, npLesFormes)
    
    # 2) lit la sauvegarde numpy pour aller ah toute berzingue
    npLesFormes = numpy.load(nomNumpy, allow_pickle=True)
    lesFormes = npLesFormes.tolist()
    print(f'{len(lesFormes)} formes retrouvées')
        
    # 3) trouve les formes et les lemmes qui ont plusieurs macrocats, genres, nombres
    formesLemmes = {}
    formesMacros = {}
    formesGenres = {}
    formesNombres = {}
    lemmesMacros = {}
    for (grform, grlem, macrocat, macro_micro, genre, nombre, personne, temps) in lesFormes:
        if enTest:
            if formeTesteje in [grform, grlem]:
                print('    A) ', grform, grlem, macrocat, macro_micro, genre, nombre, personne, temps)
        if grform not in formesLemmes: formesLemmes[grform] = []
        formesLemmes[grform].append(grlem)
        if grform not in formesMacros: formesMacros[grform] = []
        formesMacros[grform].append(macrocat)
        if grform not in formesGenres: formesGenres[grform] = []
        formesGenres[grform].append(genre)
        if grform not in formesNombres: formesNombres[grform] = []
        formesNombres[grform].append(nombre)
        if grlem not in lemmesMacros: lemmesMacros[grlem] = []
        lemmesMacros[grlem].append(macrocat)        
    formesAmbiguees = []
    lemmesAmbiguus = []
    for (grform, lemmes) in formesLemmes.items():
        if len(list(set(lemmes))) > 1: formesAmbiguees.append(grform)
    for (grform, macrocats) in formesMacros.items():
        if len(list(set(macrocats))) > 1: formesAmbiguees.append(grform)
    for (grform, genres) in formesGenres.items():
        if len(list(set(genres))) > 1: formesAmbiguees.append(grform)
    for (grform, nombres) in formesNombres.items():
        if len(list(set(nombres))) > 1: formesAmbiguees.append(grform)
    print(f'{len(formesAmbiguees)} formes ambiguës')
    for (grlem, macrocats) in lemmesMacros.items():
        if len(list(set(macrocats))) > 1: lemmesAmbiguus.append(grlem)
    print(f'{len(lemmesAmbiguus)} lemmes ambigüs')
    
    # 4) vire les formes trop courtes, ambiguees, les verbes conjuguejs, les adverbes hors "ment", traduit les propriejtejs
    if enTest:
        if formeTesteje in formesAmbiguees: print (f'    4) {formeTesteje} dans formesAmbiguees')
        if formeTesteje in lemmesAmbiguus: print (f'    4) {formeTesteje} dans lemmesAmbiguus')
    ejquivalences = {L_MASC : MASCULIN, L_FEM : FEJMININ, L_SING : SINGULIER, 
                     L_PLUR : PLURIEL, L_1 : PERS_1, L_2 : PERS_2, L_3 : PERS_3, 
                     L_PRES : PREJSENT, L_IMPFT : IMPARFAIT, L_PASS : PASSEJ, 
                     L_FUTUR : FUTUR, L_COND_PRES : CONDITIONNEL}
    lesFormes2 = []
    while len(lesFormes) > 0:
        (grform, grlem, macrocat, macro_micro, genre, nombre, personne, temps) = lesFormes.pop()
        if len(grform) < 5: continue
        if macrocat == L_V and macro_micro not in (L_VERBE_PRINCIPAL_INFINITIF, L_VERBE_PRINCIPAL_PARTICIPE_PRESENT, L_VERBE_PRINCIPAL_PARTICIPE_PASSE): continue
        if macrocat == L_ADV and not grform.endswith('ment'): continue
        if macrocat == L_ADJ: continue
        if grform in formesAmbiguees: continue
        if grlem in lemmesAmbiguus: continue
        # changement de codage
        macrocat2 = genre2 = nombre2 = personne2 = temps2 = 0
        if genre in ejquivalences: genre2 = ejquivalences[genre]
        if nombre in ejquivalences: nombre2 = ejquivalences[nombre]
        if personne in ejquivalences: personne2 = ejquivalences[personne]
        if temps in ejquivalences: temps2 = ejquivalences[temps]
        if macrocat == L_ADV: macrocat2 = CAT_ADV
        elif macrocat == L_V:
            if macro_micro == L_VERBE_PRINCIPAL_INFINITIF: macrocat2 = CAT_VER
            elif macro_micro == L_VERBE_PRINCIPAL_PARTICIPE_PRESENT: macrocat2 = CAT_PPR
            elif macro_micro == L_VERBE_PRINCIPAL_PARTICIPE_PASSE: macrocat2 = CAT_PPA
            else: raise Exception(f'ERREUR INTERNE 021 : {grform}')
        elif macrocat == L_NC:
            if genre2 == MASCULIN: macrocat2 = CAT_SUBM
            elif genre2 == FEJMININ: macrocat2 = CAT_SUBF
            else: raise Exception(f'ERREUR INTERNE 022 : {grform}')
        lesFormes2.append((grform, grlem, macrocat2, genre2, nombre2, personne2, temps2))
    lesFormes2 = list(set(lesFormes2))
    print(f'{len(lesFormes2)} formes conservées')
    
    # 5) fabrique les 6 groupes CAT_ADV, CAT_SUBM, CAT_SUBF, CAT_VER, CAT_PPR, CAT_PPA
    catAdv = {}
    catSubm = {}
    catSubf = {}
    catVer = {}
    catPpr = {}
    catPpa = {}
    for (grform, grlem, macrocat, genre, nombre, personne, temps) in lesFormes2:
        if enTest:
            if formeTesteje in [grform, grlem]:
                print('    B) ', grform, grlem, macrocat, genre, nombre, personne, temps)
        if macrocat == CAT_ADV:
            if grlem not in catAdv: catAdv[grlem] = []
            catAdv[grlem].append((genre, nombre, personne, temps))
        elif macrocat == CAT_SUBM:
            if grlem not in catSubm: catSubm[grlem] = []
            catSubm[grlem].append((genre, nombre, personne, temps))
        elif macrocat == CAT_SUBF:
            if grlem not in catSubf: catSubf[grlem] = []
            catSubf[grlem].append((genre, nombre, personne, temps))
        elif macrocat == CAT_VER:
            if grlem not in catVer: catVer[grlem] = []
            catVer[grlem].append((genre, nombre, personne, temps))
        elif macrocat == CAT_PPR:
            if grlem not in catPpr: catPpr[grlem] = []
            catPpr[grlem].append((genre, nombre, personne, temps))
        elif macrocat == CAT_PPA:
            if grlem not in catPpa: catPpa[grlem] = []
            catPpa[grlem].append((genre, nombre, personne, temps))
        else: raise Exception(f'ERREUR INTERNE 023 : {grform}')
    # trouve les lemmes incomplets
    lemmesIncomplets = []
    for (grlem, formes) in catAdv.items():
        if len(formes) != 1: lemmesIncomplets.append((grlem, CAT_ADV))
        if len(list(set(formes))) != 1: lemmesIncomplets.append((grlem, CAT_ADV))
    for (grlem, formes) in catSubm.items():
        if len(formes) != 2: lemmesIncomplets.append((grlem, CAT_SUBM))
        if len(list(set(formes))) != 2: lemmesIncomplets.append((grlem, CAT_SUBM))
    for (grlem, formes) in catSubf.items():
        if len(formes) != 2: lemmesIncomplets.append((grlem, CAT_SUBF))
        if len(list(set(formes))) != 2: lemmesIncomplets.append((grlem, CAT_SUBF))
    for (grlem, formes) in catVer.items():
        if len(formes) != 1: lemmesIncomplets.append((grlem, CAT_VER))
        if len(list(set(formes))) != 1: lemmesIncomplets.append((grlem, CAT_VER))
    for (grlem, formes) in catPpr.items():
        if len(formes) != 1: lemmesIncomplets.append((grlem, CAT_PPR))
        if len(list(set(formes))) != 1: lemmesIncomplets.append((grlem, CAT_PPR))
    for (grlem, formes) in catPpa.items():
        if len(formes) != 4: lemmesIncomplets.append((grlem, CAT_PPA))
        if len(list(set(formes))) != 4: lemmesIncomplets.append((grlem, CAT_PPA))
    print(f'{len(lemmesIncomplets)} lemmes incomplets')
    
    # vire les formes des lemmes incomplets
    lesFormes3 = []
    while len(lesFormes2) > 0:
        (grform, grlem, macrocat, genre, nombre, personne, temps) = lesFormes2.pop()
        if (grlem, macrocat) in lemmesIncomplets: continue
        lesFormes3.append((grform, grlem, macrocat, genre, nombre, personne, temps))
        if enTest:
            if formeTesteje in [grform, grlem]:
                print('    C) ', grform, grlem, macrocat, genre, nombre, personne, temps)
    lesFormes3 = list(set(lesFormes3))
    print(f'{len(lesFormes3)} formes conservées')
    
    # 6) creje le lexique 
    print(f'Création du {racine}.qclexique') 
    qcLexique = QcLexique(f'{racine}.qclexique', True, TAILLE_HASH)
    for (grform, grlem, macrocat, genre, nombre, personne, temps) in lesFormes3:
        qcLexique.ajouteMot(grform)
    qcLexique.valideMots()
    qcLexique.close()

    # 7) creje le rejtrolexique en vidant le lexique 
    qcLexique = QcLexique(f'{racine}.qclexique')
    # vidage du lexique complet
    motsIdentifiants = qcLexique.vidage()
    print(f'{len(motsIdentifiants)} mots-identifiants trouvés')
    # rejcupehre identification systehme
    (maxIdentifiant, identifieurUnique) = qcLexique.donneIdentificationFichier()
    print(f'Création du {racine}.qcrejtrolexique') 
    qcRejtroLexique = QcRejtroLexique(f'{racine}.qcrejtrolexique', True, len(motsIdentifiants))
    for (identifiant, mot) in motsIdentifiants:
        qcRejtroLexique.ajouteIdMot(identifiant, mot)
    # ejcrit l'identification systehme
    qcRejtroLexique.ejcritIdentificationFichier(maxIdentifiant, identifieurUnique)
    qcRejtroLexique.close()
    
    qcRejtroLexique = QcRejtroLexique(f'{racine}.qcrejtrolexique')
    # vidage du rejtrolexique complet
    motsIdentifiants = qcRejtroLexique.vidage()
    print(f'{len(motsIdentifiants)} mots-identifiants trouvés')
    qcRejtroLexique.close()
    
    # 8) creje le fichier rejtroformes
    catAdv = {}
    catSubm = {}
    catSubf = {}
    catVer = {}
    catPpr = {}
    catPpa = {}
    for (grform, grlem, macrocat, genre, nombre, personne, temps) in lesFormes3:
        identForme = qcLexique.trouveIdentifiant(grform)
        if identForme == 0: raise Exception(f'ERREUR INTERNE 01 : {grform}')
        if macrocat == CAT_ADV:
            if grlem not in catAdv: catAdv[grlem] = []
            catAdv[grlem].append((identForme, genre, nombre, personne, temps))
        elif macrocat == CAT_SUBM:
            if grlem not in catSubm: catSubm[grlem] = []
            catSubm[grlem].append((identForme, genre, nombre, personne, temps))
        elif macrocat == CAT_SUBF:
            if grlem not in catSubf: catSubf[grlem] = []
            catSubf[grlem].append((identForme, genre, nombre, personne, temps))
        elif macrocat == CAT_VER:
            if grlem not in catVer: catVer[grlem] = []
            catVer[grlem].append((identForme, genre, nombre, personne, temps))
        elif macrocat == CAT_PPR:
            if grlem not in catPpr: catPpr[grlem] = []
            catPpr[grlem].append((identForme, genre, nombre, personne, temps))
        elif macrocat == CAT_PPA:
            if grlem not in catPpa: catPpa[grlem] = []
            catPpa[grlem].append((identForme, genre, nombre, personne, temps))
    nombreLemmes = len(catAdv) + len(catSubm) + len(catSubf) + len(catVer) + len(catPpr) + len(catPpa)
    print(f'{nombreLemmes} lemmes conservés')    
    rejtroLemmes = {}
    print(f'Création du {racine}.qcrejtroformes') 
    qcRejtroFormes = QcRejtroFormes(f'{racine}.qcrejtroformes', True, nombreLemmes)
    # l'ordre est obligatoirement CAT_ADV, CAT_SUBM, CAT_SUBF, CAT_ADJ, CAT_VER, CAT_PPR, CAT_PPA
    ajouteSejrie(qcRejtroFormes, CAT_ADV, catAdv, rejtroLemmes)
    ajouteSejrie(qcRejtroFormes, CAT_SUBM, catSubm, rejtroLemmes)
    ajouteSejrie(qcRejtroFormes, CAT_SUBF, catSubf, rejtroLemmes)
    ajouteSejrie(qcRejtroFormes, CAT_VER, catVer, rejtroLemmes)
    ajouteSejrie(qcRejtroFormes, CAT_PPR, catPpr, rejtroLemmes)
    ajouteSejrie(qcRejtroFormes, CAT_PPA, catPpa, rejtroLemmes)
    qcRejtroFormes.finAjouts()
    qcRejtroFormes.ejcritIdentificationFichier(maxIdentifiant, identifieurUnique)
    qcRejtroLexique.close()
         
    # 9) creje le fichier de formes
    # creje le dictionnaire formes -> lemmes 
    formesLemmes = {}
    for (grform, grlem, macrocat, genre, nombre, personne, temps) in lesFormes3:
        identForme = qcLexique.trouveIdentifiant(grform)
        if identForme == 0: raise Exception(f'ERREUR INTERNE 03 : {grform}')
        if (grlem, macrocat) not in rejtroLemmes: raise Exception(f'ERREUR INTERNE 04 : {grlem}')
        if identForme not in formesLemmes: formesLemmes[identForme] = []
        formesLemmes[identForme].append((rejtroLemmes[(grlem, macrocat)], genre, nombre, personne, temps))
    print(f'{len(formesLemmes)} formes conservées')    
    print(f'Création du {racine}.qcformes') 
    qcFormes = QcFormes(f'{racine}.qcformes', True, maxIdentifiant)
    for (identForme, descriptions) in formesLemmes.items():
        qcFormes.ajouteForme(identForme, descriptions)
    qcFormes.ejcritIdentificationFichier(maxIdentifiant, identifieurUnique)
    qcFormes.close()
    
    qcLexique.close()
    
################################
# ajoute les identifiants des lemmes d'une macrocat   
def ajouteSejrie(qcRejtroFormes, catejgorie, lemmesFormes, rejtroLemmes):
    lemmesFormesListe = list(lemmesFormes.items())
    # par ordre alphabejtique
    lemmesFormesListe.sort()
    for (grlem, formes) in lemmesFormesListe:
        numejroLemme = qcRejtroFormes.ajouteLemme(catejgorie, formes)
        if grlem in rejtroLemmes: raise Exception(f'ERREUR INTERNE 05 : {grlem}')
        rejtroLemmes[(grlem, catejgorie)] = numejroLemme
    qcRejtroFormes.finSejrie()
    
################################
# rejcupehre la liste des formes potentielles
def trouveFormes(base):
    rejsultat = base.executeSqlSelect(f'''
        SELECT DISTINCT grform.graphie, grlem.graphie, micro.macrocat, micro.macro_micro, micro.genre, micro.nombre, micro.personne, micro.temps 
            FROM formes 
            JOIN lemmes ON formes.lemme=lemmes.id 
            JOIN microcats AS micro ON formes.microcat=micro.id 
            JOIN graphies AS grform ON formes.graphie=grform.id 
            JOIN graphies AS grlem ON lemmes.graphie=grlem.id 
            JOIN origines_formes ON origines_formes.forme=formes.id 
            WHERE micro.langue={FRE} 
            AND origines_formes.origine IN (3,6,13,68,82,83,84,155)
            AND NOT grform.graphie LIKE "%\_%" 
            AND NOT grform.graphie LIKE "%-%" 
            AND NOT grform.graphie LIKE "%'%" 
            AND NOT grform.graphie LIKE "% %" 
            AND micro.macrocat IN ({L_NC},{L_ADV},{L_V});
        ''')
    return rejsultat

if __name__ == '__main__':
        main()
    
