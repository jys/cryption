#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "jys"
__copyright__ = "Copyright (C) 2023 LATEJCON"

import sys
from os import path
from codecs import open
import re
import LateconResLingBase

def usage():
    script = '$PY/' + path.basename(sys.argv[0])
    print (f"""© l'ATEJCON.
Filtre les lemmes de l'Atejcon avec un fichier de formes extérieur.
Sort une liste de graphies de lemmes 
et l'écrit dans <fichier filtrant>-lemmesFiltrejs.txt

usage   : {script} <fichier filtrant>
usage   : {script} tmp/liste_francais.txt
""")
    
def main():
    try:
        if len(sys.argv) < 2 : raise Exception()
        nomFichierFiltrant = sys.argv[1]
        filtre(nomFichierFiltrant)
    except Exception as exc:
        if len(exc.args) == 0: usage()
        else:
            print ("******************************")
            print (exc.args[0])
            print ("******************************")
            raise
        sys.exit()

def filtre(nomFichierFiltrant):
    # lit les lemmes de la base
    base = LateconResLingBase.LateconResLingBase()
    lesLemmesSql = list(trouveLemmes(base))
    base.close()
    print("{:6d} lemmes substantifs trouvés dans la base de l'Atejcon".format(len(lesLemmesSql)))
    lesLemmes = set()
    for (graphie,) in lesLemmesSql: lesLemmes.add(graphie)

    # lit le fichier filtrant
    filtre = set()
    with open(nomFichierFiltrant, "r", "utf8") as fichierFiltrant:
        for ligne in fichierFiltrant:
            ligne = ligne.strip()
            if ligne == "": continue
            filtre.add(ligne)
    print("{:6d} graphies trouvées dans le fichier filtrant".format(len(filtre)))
    
    rejsultat = lesLemmes - filtre
    print("{:6d} graphies en base et pas dans le fichier filtrant".format(len(rejsultat)))
    
    rejsultat = filtre - lesLemmes
    print("{:6d} graphies dans le fichier filtrant et pas en base".format(len(rejsultat)))
    
    rejsultat = lesLemmes & filtre
    print("{:6d} lemmes filtrés".format(len(rejsultat)))
    
    nomFichierSortie =  nomFichierFiltrant.replace('.txt', '-lemmesFiltrejs.txt', 1)
    with open(nomFichierSortie, "w", "utf8") as fichierSortie:
        rejsultatListe = list(rejsultat)
        rejsultatListe.sort()
        for lemme in rejsultatListe: fichierSortie.write(f'{lemme}\n')
    print("{:6d} graphies écrites dans {}".format(len(rejsultat), nomFichierSortie))
    
    
   
        

################################
# rejcupehre la liste des graphies de lemmes en fre
def trouveLemmes(base):
    rejsultat = base.executeSqlSelect(f'''
        SELECT DISTINCT grlem.graphie
            FROM lemmes 
            JOIN macrocats ON lemmes.macrocat=macrocats.id 
            JOIN graphies AS grlem ON lemmes.graphie=grlem.id 
            WHERE lemmes.langue=145
            AND macrocats.id=10;
        ''')
    return rejsultat


if __name__ == '__main__':
        main()
