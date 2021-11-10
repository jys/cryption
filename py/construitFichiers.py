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
from QcRejtroFormes import CAT_ADV, CAT_SUBM, CAT_SUBF, CAT_ADJ, CAT_VER 

def usage():
    script = '$PY/' + path.basename(sys.argv[0])
    print (f"""© l'ATEJCON.
Construction les fichiers plats de la quasi-cryption de l'Atejcon.
Les fichiers plats sont :
    <racine>.qclexique
    <racine>.qcrejtrolexique
    <racine>.qcformes
    <racine>.qcrejtroformes

usage   : {script} <racine fichiers>
usage   : {script} Latejcon
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
#L_PC = 1440
#L_PQPFT = 1441
#L_PASS_ANT = 1442
#L_FUTUR_ANT = 1443
#L_COND_PASS = 1444

TAILLE_HASH = 100019
    
def construit(racine):
    base = LateconResLingBase.LateconResLingBase()
    
    # 1) trouve les lemmes idoines : id, macrocat, graphie 
    idslemmes = trouveIdsLemmes(base)
    print(f'{len(idslemmes)} lemmes idoines trouvés')
    
    # 2) les regroupe par macrocat et trouve toutes leurs formes
    toutesLesGraphies = set()
    toutesLesFormes = []
    #tousLesIdLemmes = []
    lemmesAdv = []
    lemmesSubM = []
    lemmesSubF = []
    lemmesAdj = []
    lemmesVer = []
    for (idLemme, macrocat, graphieLemme) in idslemmes:
        if macrocat == L_ADV:
            # ejcarte les adverbes qui ne finissent pas par "ment"
            if not graphieLemme.endswith('ment'): continue
            lemmesAdv.append((graphieLemme, idLemme))
        elif macrocat == L_NC:
            genres = trouveGenreSub(base, idLemme)
            # ejcarte les substantifs bi-genres
            if len(genres) != 1: continue
            if genres[0][0] == L_MASC: lemmesSubM.append((graphieLemme, idLemme))
            elif genres[0][0] == L_FEM: lemmesSubF.append((graphieLemme, idLemme))
            else: continue
        elif macrocat == L_ADJ:
            lemmesAdj.append((graphieLemme, idLemme))
        elif macrocat == L_V:
            lemmesVer.append((graphieLemme, idLemme))
        else: raise Exception('ERREUR INTERNE 01')
        # trouve toutes les formes du lemme retenu
        graphiesFormes = trouveGraphiesFormes(base, idLemme)
        for (graphieForme, idForme) in graphiesFormes: 
            toutesLesGraphies.add(graphieForme)
            toutesLesFormes.append((idForme, graphieForme))
    nombreLemmes = len(lemmesAdv) + len(lemmesSubM) + len(lemmesSubF) + len(lemmesAdj) + len(lemmesVer)
    print(f'{nombreLemmes} lemmes conservées')
    print(f'{len(toutesLesGraphies)} formes conservées')
        
    # 3) creje le lexique 
    print(f'Création du {racine}.qclexique') 
    qcLexique = QcLexique(f'{racine}.qclexique', True, TAILLE_HASH)
    for graphie in toutesLesGraphies:
        qcLexique.ajouteMot(graphie)
    qcLexique.valideMots()
    qcLexique.close()
    
    # 4) creje le rejtrolexique en vidant le lexique pour crejer le rejtrolexique
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
    
    # 5) creje le rejtroformes
    ejquivalences = {L_MASC : MASCULIN, L_FEM : FEJMININ, L_SING : SINGULIER, 
                     L_PLUR : PLURIEL, L_1 : PERS_1, L_2 : PERS_2, L_3 : PERS_3, 
                     L_PRES : PREJSENT, L_IMPFT : IMPARFAIT, L_PASS : PASSEJ, 
                     L_FUTUR : FUTUR, L_COND_PRES : CONDITIONNEL,
                     L_ADJ : CAT_ADJ, L_ADV : CAT_ADV, L_V : CAT_VER}
    rejtroLemmeCats = {}
    print(f'Création du {racine}.qcrejtroformes') 
    qcRejtroFormes = QcRejtroFormes(f'{racine}.qcrejtroformes', True, nombreLemmes)
    # l'ordre est obligatoirement CAT_ADV, CAT_SUBM, CAT_SUBF, CAT_ADJ, CAT_VER
    ajouteSejrie(qcLexique, qcRejtroFormes, base, CAT_ADV, lemmesAdv, rejtroLemmeCats, ejquivalences)
    ajouteSejrie(qcLexique, qcRejtroFormes, base, CAT_SUBM, lemmesSubM, rejtroLemmeCats, ejquivalences)
    ajouteSejrie(qcLexique, qcRejtroFormes, base, CAT_SUBF, lemmesSubF, rejtroLemmeCats, ejquivalences)
    ajouteSejrie(qcLexique, qcRejtroFormes, base, CAT_ADJ, lemmesAdj, rejtroLemmeCats, ejquivalences)
    ajouteSejrie(qcLexique, qcRejtroFormes, base, CAT_VER, lemmesVer, rejtroLemmeCats, ejquivalences)
    qcRejtroFormes.finAjouts()
    qcRejtroFormes.ejcritIdentificationFichier(maxIdentifiant, identifieurUnique)
    qcRejtroLexique.close()
    
    # 6) creje le formes
    print(f'Création du {racine}.qcformes') 
    qcFormes = QcFormes(f'{racine}.qcformes', True, len(toutesLesGraphies))
    for (idForme, graphieForme) in toutesLesFormes:
        description = []
        identifiantForme = qcLexique.trouveIdentifiant(graphieForme)
        if identifiantForme == 0: raise Exception(f'ERREUR INTERNE 03 : {graphieForme}')
        attributsForme = trouveAttributsForme(base, idForme)
        for (idLemme, bMacrocat, bGenre, bNombre, bPersonne, bTemps) in attributsForme:
            # <identifiantLemme> <macro> <numejroLemmeCat> <genre> <nombre> <personne> <temps>
            if bMacrocat in ejquivalences: macro = ejquivalences[bMacrocat]
            elif bMacrocat == L_NC and bGenre == L_FEM: macro = CAT_SUBF
            elif bMacrocat == L_NC and bGenre == L_MASC: macro = CAT_SUBM
            else: continue
            if idLemme not in rejtroLemmeCats:
                raise Exception(f'ERREUR INTERNE 05 : {graphieForme}')
            numejroLemmeCat = -1
            for (numejroLemme, catejgorie) in rejtroLemmeCats[idLemme]:
                if catejgorie == macro: numejroLemmeCat = numejroLemme
            if numejroLemmeCat == -1: raise Exception(f'ERREUR INTERNE 06 : {graphieForme}')
            genre = nombre = personne = temps = 0
            if bGenre in ejquivalences: genre = ejquivalences[bGenre]
            if bNombre in ejquivalences: nombre = ejquivalences[bNombre]
            if bPersonne in ejquivalences: personne = ejquivalences[bPersonne]
            if bTemps in ejquivalences: temps = ejquivalences[bTemps]
            description.append((numejroLemmeCat, genre, nombre, personne, temps))
        qcFormes.ajouteForme(identifiantForme, description)
    qcFormes.ejcritIdentificationFichier(maxIdentifiant, identifieurUnique)
    qcFormes.close()
    
    qcLexique.close()
    base.close()

################################
# ajoute les identifiants des lemmes d'une macrocat   
def ajouteSejrie(qcLexique, qcRejtroFormes, base, catejgorie, lemmesMacrocat, rejtroLemmeCats, ejquivalences):
    # par ordre alphabejtique
    lemmesMacrocat.sort()
    for (graphieLemme, idLemme) in lemmesMacrocat:
        description = []
        attributsLemme = trouveAttributsLemme(base, idLemme)
        for (graphieForme, bGenre, bNombre, bPersonne, bTemps) in attributsLemme:
            # <genre> <nombre> <personne> <temps> <identifiantForme>
            identifiantForme = qcLexique.trouveIdentifiant(graphieForme)
            if identifiantForme == 0: raise Exception(f'ERREUR INTERNE 08 : {graphieForme}')
            genre = nombre = personne = temps = 0
            if bGenre in ejquivalences: genre = ejquivalences[bGenre]
            if bNombre in ejquivalences: nombre = ejquivalences[bNombre]
            if bPersonne in ejquivalences: personne = ejquivalences[bPersonne]
            if bTemps in ejquivalences: temps = ejquivalences[bTemps]
            description.append((identifiantForme, genre, nombre, personne, temps))
        numejroLemme = qcRejtroFormes.ajouteLemme(catejgorie, description)
        if idLemme not in rejtroLemmeCats: rejtroLemmeCats[idLemme] = []
        rejtroLemmeCats[idLemme].append((numejroLemme, catejgorie))
    qcRejtroFormes.finSejrie()
        
################################
# rejcupehre la liste des ids, macros et graphies des lemmes idoines
def trouveIdsLemmes(base):
    #rejsultat = base.executeSqlSelect(f'''
        #SELECT lemmes.id, lemmes.macrocat, graphies.graphie
            #FROM lemmes 
            #JOIN graphies ON lemmes.graphie=graphies.id 
            #WHERE lemmes.langue={FRE} 
            #AND NOT graphies.graphie LIKE "%\_%" 
            #AND NOT graphies.graphie LIKE "%-%" 
            #AND NOT graphies.graphie LIKE "%'%" 
            #AND NOT graphies.graphie LIKE "% %" 
            #AND LENGTH(graphies.graphie) > 5 
            #AND lemmes.macrocat IN ({L_NC},{L_ADV});
        #''')
    #return rejsultat
    rejsultat = base.executeSqlSelect(f'''
        SELECT DISTINCT lemmes.id, lemmes.macrocat, graphies.graphie
            FROM lemmes 
            JOIN graphies ON lemmes.graphie=graphies.id 
            JOIN surlemmes ON surlemmes.lemme=lemmes.id
            JOIN origines_surlemmes ON origines_surlemmes.surlemme=surlemmes.id
            WHERE lemmes.langue={FRE} 
            AND origines_surlemmes.origine IN (3,6,13,68)
            AND NOT graphies.graphie LIKE "%\_%" 
            AND NOT graphies.graphie LIKE "%-%" 
            AND NOT graphies.graphie LIKE "%'%" 
            AND NOT graphies.graphie LIKE "% %" 
            AND LENGTH(graphies.graphie) > 5 
            AND lemmes.macrocat IN ({L_NC},{L_ADV});
        ''')
    return rejsultat


################################
# rejcupehre le genre d'un lemme donnej
def trouveGenreSub(base, idLemme):
    rejsultat = base.executeSqlSelect(f'''
        SELECT DISTINCT microcats.genre 
            FROM formes 
            JOIN lemmes ON formes.lemme=lemmes.id 
            JOIN microcats ON formes.microcat=microcats.id 
            WHERE lemmes.id={idLemme};
        ''')
    return rejsultat

################################
# rejcupehre toutes les graphies des formes d'un lemme donnej
def trouveGraphiesFormes(base, idLemme):
    rejsultat = base.executeSqlSelect(f'''
        SELECT DISTINCT graphies.graphie, formes.id
            FROM formes 
            JOIN graphies ON formes.graphie=graphies.id 
            WHERE formes.lemme={idLemme};
        ''')
    return rejsultat

################################
# rejcupehre toutes les propriejtejs intejressantes d'une forme donneje
def trouveAttributsForme(base, idForme):
    rejsultat = base.executeSqlSelect(f'''
        SELECT DISTINCT formes.lemme, micro.macrocat, micro.genre, micro.nombre, micro.personne, micro.temps 
            FROM formes 
            JOIN microcats AS micro ON formes.microcat=micro.id 
            WHERE micro.macrocat IN ({L_NC},{L_ADV}) 
            AND formes.id="{idForme}";
        ''')
    return rejsultat

################################
# rejcupehre toutes les propriejtejs intejressantes d'un lemme donnej
def trouveAttributsLemme(base, idLemme):
    rejsultat = base.executeSqlSelect(f'''
        SELECT DISTINCT grform.graphie, micro.genre, micro.nombre, micro.personne, micro.temps 
            FROM formes 
            JOIN lemmes ON formes.lemme=lemmes.id 
            JOIN graphies AS grform ON formes.graphie=grform.id 
            JOIN microcats AS micro ON formes.microcat=micro.id 
            WHERE micro.macrocat IN ({L_NC},{L_ADV}) 
            AND lemmes.id="{idLemme}";
        ''')
    return rejsultat


if __name__ == '__main__':
        main()
