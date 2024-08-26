#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "jys"
__copyright__ = "Copyright (C) 2023 LATEJCON"

import sys
from os import path
import LateconResLingBase
from codecs import open
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
#from QcRejtroFormes import QcRejtroFormes
#from QcRejtroFormes import CAT_ADV, CAT_SUBM, CAT_SUBF, CAT_VER, CAT_PPR, CAT_PPA
import numpy

def usage():
    script = '$PY/' + path.basename(sys.argv[0])
    print (f"""© l'ATEJCON.
Construction les fichiers plats de la quasi-cryption Sp7 de l'Atejcon 
avec analyse syntaxique.
Les données sont prises dans la base SQL ou dans le fichier Sp7.npy.
Pour reconstruire suite à changement dans la base, effacer Sp7.npy.
Filtrage des Ncxx par le fichier <racine>-sp7-filtrageGraphies.txt,
pas de filtrage si pas de fichier.
Les fichiers plats sont :
    <racine>.sp7lexique
    <racine>.sp7rejtrolexique
    <racine>.sp7formes
    <racine>.sp7rejtroformes

usage   : {script} <racine fichiers> 
usage   : {script} complet
""")
    
def main():
    try:
        if len(sys.argv) < 2 : raise Exception()
        racine = sys.argv[1]
        construit(racine)
    except Exception as exc:
        if len(exc.args) == 0: usage()
        else:
            print ("******************************")
            print (exc.args[0])
            print ("******************************")
            raise
        sys.exit()

FRE = 145
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
L_VERBE_AUXILIAIRE_INFINITIF = 1566
L_VERBE_MODALITE_INFINITIF = 1572
L_VERBE_COPULE_INFINITIF = 1578
L_VERBE_PRINCIPAL_PARTICIPE_PRESENT = 1560
L_VERBE_AUXILIAIRE_PARTICIPE_PRESENT =  1567
L_VERBE_MODALITE_PARTICIPE_PRESENT = 1573
L_VERBE_COPULE_PARTICIPE_PRESENT = 1579
L_VERBE_PRINCIPAL_PARTICIPE_PASSE = 1561
L_VERBE_AUXILIAIRE_PARTICIPE_PASSE = 1568 
L_VERBE_MODALITE_PARTICIPE_PASSE = 1574
L_VERBE_COPULE_PARTICIPE_PASSE = 1580
L_VERBE_PRINCIPAL_INDICATIF = 1556 
L_VERBE_AUXILIAIRE_INDICATIF = 1563
L_VERBE_MODALITE_INDICATIF = 1569
L_VERBE_COPULE_INDICATIF = 1575 
L_VERBE_PRINCIPAL_SUBJONCTIF = 1557
L_VERBE_AUXILIAIRE_SUBJONCTIF = 1564
L_VERBE_MODALITE_SUBJONCTIF = 1570
L_VERBE_COPULE_SUBJONCTIF = 1576
L_VERBE_PRINCIPAL_IMPERATIF = 1558
L_VERBE_AUXILIAIRE_IMPERATIF = 1565
L_VERBE_MODALITE_IMPERATIF = 1571
L_VERBE_COPULE_IMPERATIF = 1577

TAILLE_HASH = 100019
    
def construit(racine):
    # 1) si la sauvegarde numpy n'est pas lah, la creje
    nomNumpy = 'Sp7.npy'
    if not path.isfile(nomNumpy):
        base = LateconResLingBase.LateconResLingBase()
        lesFormesSql = list(trouveFormes(base))
        base.close()
        print("{:6d} formes trouvées dans la base de l'Atejcon".format(len(lesFormesSql)))
        npLesFormes = numpy.array(lesFormesSql)
        numpy.save(nomNumpy, npLesFormes)
    
    # 2) lit la sauvegarde numpy pour aller ah toute berzingue
    npLesFormes = numpy.load(nomNumpy, allow_pickle=True)
    lesFormesSql = npLesFormes.tolist()
    print("{:6d} formes retrouvées".format(len(lesFormesSql)))
    
    # 3) creje le lexique 
    print(' '*7 + f'Création du {racine}.sp7lexique') 
    qcLexique = QcLexique(f'{racine}.sp7lexique', True, TAILLE_HASH)
    for (grform, grlem, macrocat, macro_micro, genre, nombre, personne, temps) in lesFormesSql:
        if macrocat not in (L_ADJ, L_ADV, L_CONJ, L_DET, L_NC, L_NP, L_PREP, L_PRON, L_V): continue
        if genre not in (None, L_MASC, L_FEM): continue
        if nombre not in (None, L_SING, L_PLUR): continue
        if personne not in (None, L_1, L_2, L_3): continue
        if temps not in (None, L_PRES, L_IMPFT, L_PASS, L_FUTUR, L_COND_PRES): continue
        qcLexique.ajouteMot(grform)
    qcLexique.valideMots()
    qcLexique.close()

    # 4) creje le rejtrolexique en vidant le lexique 
    qcLexique = QcLexique(f'{racine}.sp7lexique')
    # vidage du lexique complet
    motsIdentifiants = qcLexique.vidage()
    print("{:6d} mots-identifiants trouvés".format(len(motsIdentifiants)))
    # rejcupehre identification systehme
    (maxIdentifiant, identifieurUnique) = qcLexique.donneIdentificationFichier()
    print(' '*7 + f'Création du {racine}.sp7rejtrolexique') 
    qcRejtroLexique = QcRejtroLexique(f'{racine}.sp7rejtrolexique', True, len(motsIdentifiants))
    for (identifiant, mot) in motsIdentifiants:
        qcRejtroLexique.ajouteIdMot(identifiant, mot)
    # ejcrit l'identification systehme
    qcRejtroLexique.ejcritIdentificationFichier(maxIdentifiant, identifieurUnique)
    qcRejtroLexique.close()
    # vejrification
    qcRejtroLexique = QcRejtroLexique(f'{racine}.sp7rejtrolexique')
    # vidage du rejtrolexique complet
    motsIdentifiants = qcRejtroLexique.vidage()
    print(f'{len(motsIdentifiants)} mots-identifiants trouvés')
    qcRejtroLexique.close()
    
    # 5) ejtablit la structure des lemmes
    print(' '*7 + f'Création du {racine}.sp7lemmes') 
    # ejtablit les filtres de graphies
    nomFichierFiltreGraphies = f'{racine}-sp7-filtrageGraphies.txt'
    avecFiltage = path.isfile(nomFichierFiltreGraphies)
    if avecFiltage:
        filtreGraphies = set()
        with open(nomFichierFiltreGraphies, 'r', 'utf8') as fichierFiltreGraphies:
            for ligne in fichierFiltreGraphies:
                ligne = ligne.strip()
                if ligne == '': continue
                filtreGraphies.add(ligne)
        print("{:6d} graphies prises en compte dans le filtrage".format(len(filtreGraphies)))
    else:
        print(' '*7 + 'Pas de filtrage des graphies des Ncxx')
    # un lemme, c'est une graphie + une macrocat
    ejquiv = {L_MASC : MASCULIN, L_FEM : FEJMININ, L_SING : SINGULIER, L_PLUR : PLURIEL}
    compt = 0
    lesLemmes = {}
    for (grform, grlem, macrocat, macro_micro, genre, nombre, personne, temps) in lesFormesSql:
        #if macrocat not in (L_ADJ, L_DET, L_NC, L_PRON, L_V): continue
        if macrocat not in (L_NC,): continue
        if genre not in (L_MASC, L_FEM): continue
        if nombre not in (L_SING, L_PLUR): continue
        if avecFiltage and macrocat == L_NC and grlem not in filtreGraphies : continue
        # les donnejes
        identForme = qcLexique.trouveIdentifiant(grform)
        descForme = (identForme, ejquiv[genre], ejquiv[nombre])
        if (grlem, macrocat) not in lesLemmes: lesLemmes[(grlem, macrocat)] = [0, []]
        lesLemmes[(grlem, macrocat)][1].append(descForme)
        compt +=1
    print("{:6d} formes prises en compte".format(compt))
    # numejrote les lemmes
    tousLesLemmes = list(lesLemmes.keys())
    tousLesLemmes.sort()
    identLemme = 1
    for (grlem, macrocat) in tousLesLemmes: 
        lesLemmes[(grlem, macrocat)][0] = identLemme
        identLemme +=1
    
    # 6) creje le fichier des lemmes
    sp7Lemmes = Sp7Lemmes(f'{racine}.sp7lemmes', True, len(lesLemmes))
    for (grlem, macrocat) in tousLesLemmes:
        (identLemme, descFormes) = lesLemmes[(grlem, macrocat)]
        sp7Lemmes.ajouteLemme(identLemme, macrocat, list(set(descFormes)))
    sp7Lemmes.ejcritIdentificationFichier(maxIdentifiant, identifieurUnique)
    sp7Lemmes.close()
    print("{:6d} lemmes pris en compte".format(len(lesLemmes)))
    
    # 7) ejtablit la structure des formes
    print(' '*7 + f'Création du {racine}.sp7formes') 
    ejquiv = {L_MASC : MASCULIN, L_FEM : FEJMININ, L_SING : SINGULIER, 
              L_PLUR : PLURIEL, L_1 : PERS_1, L_2 : PERS_2, L_3 : PERS_3, None : 0}
    compt = 0
    lesFormes = {}
    for (grform, grlem, macrocat, macro_micro, genre, nombre, personne, temps) in lesFormesSql:
        # ne garde que L_ADJ, L_ADV, L_CONJ, L_DET, L_NC, L_NP, L_PREP, L_PRON, L_V
        # L_MASC, L_FEM, L_SING, L_PLUR, L_1, L_2, L_3, L_PRES, L_IMPFT, L_PASS, L_FUTUR, L_COND_PRES
        if macrocat not in (L_ADJ, L_ADV, L_CONJ, L_DET, L_NC, L_NP, L_PREP, L_PRON, L_V): continue
        if genre not in (None, L_MASC, L_FEM): continue
        if nombre not in (None, L_SING, L_PLUR): continue
        if personne not in (None, L_1, L_2, L_3): continue
        if temps not in (None, L_PRES, L_IMPFT, L_PASS, L_FUTUR, L_COND_PRES): continue
        # les donnejes
        divers = 0
        if grlem == "être": divers = COPULE
        if macro_micro in (L_VERBE_COPULE_INDICATIF, L_VERBE_COPULE_SUBJONCTIF, L_VERBE_COPULE_IMPERATIF,
                           L_VERBE_COPULE_INFINITIF, L_VERBE_COPULE_PARTICIPE_PRESENT, L_VERBE_COPULE_PARTICIPE_PASSE): 
            divers = COPULE
        if macro_micro in (L_VERBE_PRINCIPAL_INFINITIF, L_VERBE_AUXILIAIRE_INFINITIF,
                           L_VERBE_MODALITE_INFINITIF, L_VERBE_COPULE_INFINITIF): 
            modetemps = INFINITIF
        elif macro_micro in (L_VERBE_PRINCIPAL_PARTICIPE_PRESENT, L_VERBE_AUXILIAIRE_PARTICIPE_PRESENT,
                           L_VERBE_MODALITE_PARTICIPE_PRESENT, L_VERBE_COPULE_PARTICIPE_PRESENT): 
            modetemps = PART_PREJSENT
        elif macro_micro in (L_VERBE_PRINCIPAL_PARTICIPE_PASSE, L_VERBE_AUXILIAIRE_PARTICIPE_PASSE,
                           L_VERBE_MODALITE_PARTICIPE_PASSE, L_VERBE_COPULE_PARTICIPE_PASSE): 
            modetemps = PART_PASSEJ
        #elif macro_micro in (L_VERBE_PRINCIPAL_INDICATIF, L_VERBE_AUXILIAIRE_INDICATIF,
                           #L_VERBE_MODALITE_INDICATIF, L_VERBE_COPULE_INDICATIF): 
            #modetemps = {L_PRES : IND_PREJSENT, L_IMPFT : IND_IMPARFAIT, L_PASS : IND_PASSEJ, 
                         #L_FUTUR : IND_FUTUR, L_COND_PRES : CONDITIONNEL}[temps]
        #elif macro_micro in (L_VERBE_PRINCIPAL_SUBJONCTIF, L_VERBE_AUXILIAIRE_SUBJONCTIF,
                           #L_VERBE_MODALITE_SUBJONCTIF, L_VERBE_COPULE_SUBJONCTIF): 
            #modetemps = {L_PRES : SUB_PREJSENT, L_IMPFT : SUB_IMPARFAIT}[temps]
        elif macro_micro in (L_VERBE_PRINCIPAL_IMPERATIF, L_VERBE_AUXILIAIRE_IMPERATIF,
                           L_VERBE_MODALITE_IMPERATIF, L_VERBE_COPULE_IMPERATIF): 
            modetemps = IMPEJRATIF
        elif macro_micro in (L_VERBE_PRINCIPAL_INDICATIF, L_VERBE_AUXILIAIRE_INDICATIF,
                           L_VERBE_MODALITE_INDICATIF, L_VERBE_COPULE_INDICATIF,
                           L_VERBE_PRINCIPAL_SUBJONCTIF, L_VERBE_AUXILIAIRE_SUBJONCTIF,
                           L_VERBE_MODALITE_SUBJONCTIF, L_VERBE_COPULE_SUBJONCTIF): 
            modetemps = CONJUGUEJ
        else: modetemps = 0
        identForme = qcLexique.trouveIdentifiant(grform)
        # trouve l'identifiant de lemme
        if (grlem, macrocat) in lesLemmes: identLemme = lesLemmes[(grlem, macrocat)][0]
        else: identLemme = 0
        descForme = (identLemme, macrocat, ejquiv[genre], ejquiv[nombre], ejquiv[personne], modetemps, divers)
        if identForme not in lesFormes: lesFormes[identForme] = []
        lesFormes[identForme].append(descForme)
        compt +=1
    print("{:6d} formes prises en compte".format(compt))
        
    # 8) creje le fichier des formes
    sp7Formes = Sp7Formes(f'{racine}.sp7formes', True, maxIdentifiant)
    toutesLesFormes = list(lesFormes.keys())
    toutesLesFormes.sort()
    for identForme in toutesLesFormes:
        descFormes = lesFormes[identForme]
        sp7Formes.ajouteForme(identForme, list(set(descFormes)))
    sp7Formes.ejcritIdentificationFichier(maxIdentifiant, identifieurUnique)
    sp7Formes.close()
    qcLexique.close()
    print("{:6d} graphies formes prises en compte".format(len(lesFormes)))
            
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
            AND NOT grform.graphie LIKE "%\_%" 
            AND NOT grform.graphie LIKE "%-%" 
            AND NOT grform.graphie LIKE "% %"
            AND origines_formes.origine IN (156,157);
        ''')
    return rejsultat
            #AND micro.macrocat IN ({L_NC},{L_ADV},{L_V},{L_ADJ},{L_DET},{L_PRON});
            #            AND origines_formes.origine IN (3,6,13,68,82,83,84,90,155)
            #ORDER BY grform.graphie ;


if __name__ == '__main__':
        main()
