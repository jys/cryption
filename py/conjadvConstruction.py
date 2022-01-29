#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "jys"
__copyright__ = "Copyright (C) 2021 LATEJCON"

import sys
from os import path
import LateconResLingBase
import codecs
import re

def usage():
    script = '$PY/' + path.basename(sys.argv[0])
    print (f"""© l'ATEJCON.
Construction de la conjugaison des adverbes menteurs.

usage   : {script} <fichier html de résultats>
usage   : {script} ../site/latejcon.art/latejconsledise/lit-16-A-adverbes.html
""")

def main():
    try:
        if len(sys.argv) < 2 : raise Exception()
        nomFichierHtml = sys.argv[1]
        construit(nomFichierHtml)
    except Exception as exc:
        if len(exc.args) == 0: usage()
        else:
            print ("******************************")
            print (exc.args[0])
            print ("******************************")
            raise
        sys.exit()

################################
FRE = 145
L_ADJ = 1
L_NC = 10
L_ADV = 2
L_PLUR = 1426
        
################################
def construit(nomFichierHtml):
    # ouvre le fichier de sortie et ejcrit le dejbut
    fichierHtml = codecs.open(nomFichierHtml, 'w', 'utf8')
    ejcritDejbut(fichierHtml)
    # ouvre la base sql
    base = LateconResLingBase.LateconResLingBase()
    # 1) trouve tous les adverbes menteurs
    adverbes = trouveGraphiesAdv(base)
    print(f'{len(adverbes)} adverbes menteurs trouvejs')
    # 2) pour chacun trouve le radical
    for (adverbe,) in adverbes:
        radical = adverbe[:-4]
        if radical[-1] == 'm': radical = radical[:-1] + 'n'
        candidat = trouveRadical(base, radical)
        if candidat == '':
            if radical[-1] == 'é': radical = radical[:-1] + 'e'
            if radical[-1] == 'û': radical = radical[:-1] + 'u'
            candidat = trouveRadical(base, radical)
        if candidat == '': 
            radical = radical[:-1]
            candidat = trouveRadical(base, radical)
        if candidat == '': 
            radical = radical[:-1]
            candidat = trouveRadical(base, radical)
        if candidat == '': 
            radical = radical[:-1]
            candidat = trouveRadical(base, radical)
        if candidat == '': 
            radical = radical[:-1]
            candidat = trouveRadical(base, radical)
        if candidat == '': print(adverbe)
        else: ejcritPhrase(fichierHtml, candidat, adverbe)
    # ejcrit la fin et ferme le fichier
    ejcritFin(fichierHtml)
    fichierHtml.close()
    
################################
def trouveRadical(base, radical):
    radicaux = trouveRadicaux(base, radical)
    candidat = ''
    for (forme,) in radicaux: 
        if candidat == '' or len(forme) < len(candidat): candidat = forme
    return candidat

################################
def ejcritPhrase(fichierHtml, candidat, adverbe):
    # calcule le nombre magique
    nbMagique = 0x55
    #for carac in candidat.encode(): nbMagique^=carac
    for carac in adverbe.encode(): nbMagique^=carac
    nbMagique %= 64 
    deb = ''
    fin = ''
    if nbMagique & 0x1: 
        deb = deb + '<i>'
        fin = '</i>' + fin
    if nbMagique & 0x2: 
        deb = deb + '<b>'
        fin = '</b>' + fin
    if nbMagique & 0x4: 
        deb = deb + '<small>'
        fin = '</small>' + fin
    if nbMagique < 16: deb = deb + '<font color="#000000">'
    elif nbMagique < 24: deb = deb + '<font color="#FF0000">'
    elif nbMagique < 32: deb = deb + '<font color="#32CD32">'
    elif nbMagique < 40: deb = deb + '<font color="#0000FF">'
    elif nbMagique < 48: deb = deb + '<font color="#B8860B">'
    elif nbMagique < 56: deb = deb + '<font color="#FF00FF">'
    else: deb = deb + '<font color="#00CED1">'
    fin = '</font>' + fin
    nbMagique = (nbMagique >> 4) ^ (nbMagique & 0x0F)
    if not nbMagique & 0x07: 
        deb = '<mark>' + deb
        fin = fin + '</mark>'
    if adverbe in ('vraiment', 'sincèrement'): fichierHtml.write('<img id="imgright" alt="lit-16-A-A-Abribat.png" src="lit-16-A-A-Abribat.png"/>\n')
    
    #fichierHtml.write(f'{deb}Les&nbsp;{candidat}&nbsp;mentent&nbsp;{adverbe}.{fin} ')
    fichierHtml.write(f'{deb}Les {candidat} mentent {adverbe}.{fin} ')
    
################################
def ejcritDejbut(fichierHtml):
    fichierHtml.write("""
<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" href="latejconsledise-1-2.css">
<meta http-equiv="content-type" content="text/html; charset=utf-8">
<title>adverbes menteurs</title>
<style>
.articlecorps {
  width: auto;
  margin-left: 20px;
  margin-right: 20px;
  margin-top: 50px;
  margin-bottom: 20px;
  background-color: #F5F5F5;
}  
.articlecorps  p {
  margin: 0px;
  margin-top: 10px;
  font-size: 120%;
  text-align: justify;
}
mark {
  background-color: LightGray;
}
</style>
<link rel="icon" type="image/png" href="../faviconLaR.png"/>
</head>
<body>
<table id="table1"><tr>
<td id="td1"><img alt="../echiquierLatejcon4-200.png" src="../echiquierLatejcon4-200.png"/></td>
<td id="td2"><h1>&nbsp;&nbsp;La conjugaison des adverbes menteurs</h1>
<video width="250" height="200" controls style="float:right">
  <source src="lit-16-A-JpAbribat.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>
<br/>L'ideje nous en est venue en regardant le psychanalyste Jean-Paul Abribat dans "Enfin pris&nbsp;?", le film de Pierre Carles de 2002. <br/>Lacanien, il l'ejtait certainement...bien qu'il faille considejrer que, de son point de vue, (la) certaine ment...<br/>
Il faut dire aussi que les adverbes sont assez mal vus par les crypto-structuralistes qui grouillent à l'Atejcon. 
<br/>Ne confondons pas lacanien et latejconnien. Mais qu'importe, haro sur l'adverbe qui ment&nbsp;!
</td>
<td id="td1"><a href="lit-00-A-latejconsledise.html"><article id="article1"><img alt="Adham-Sartre-nb-100.jpeg" src="Adham-Sartre-nb-100.jpeg"/><br/>latejconsledise</article></a></td>
</tr></table>

<article class="articlecorps">
<p>
""")
    
################################
def ejcritFin(fichierHtml):
    fichierHtml.write("""
</p>
</article>
<table id="table2"><tr>
<td id="td2"><img alt="../echiquierLatejcon5-100.png" src="../echiquierLatejcon5-100.png"/></td>
<td id="td2"><a href="lit-00-A-latejconsledise.html"><article id="article1"><img alt="Adham-Sartre-c-100.jpeg" src="Adham-Sartre-c-100.jpeg"/><br/>latejconsledise</article></a></td>
</tr></table>
</body>
</html>

""")
    
################################
# rejcupehre toutes les graphies des adverbes menteurs
def trouveGraphiesAdv(base):
    rejsultat = base.executeSqlSelect(f'''
        SELECT DISTINCT graphies.graphie AS gr 
            FROM lemmes 
            JOIN graphies ON lemmes.graphie=graphies.id 
            WHERE langue={FRE} 
            AND macrocat={L_ADV} 
            AND NOT graphies.graphie  LIKE "%\_%" 
            AND NOT graphies.graphie LIKE "%-%" 
            AND graphies.graphie LIKE "%ment"
            ORDER BY RAND();
        ''')
    return rejsultat

################################
# rejcupehre toutes les graphies des radicaux
def trouveRadicaux(base, radical):
    rejsultat = base.executeSqlSelect(f'''
        SELECT DISTINCT graphies.graphie 
            FROM formes 
            JOIN graphies ON formes.graphie=graphies.id 
            JOIN microcats ON formes.microcat=microcats.id 
            WHERE microcats.langue={FRE} 
            AND microcats.macrocat IN ({L_ADJ},{L_NC}) 
            AND microcats.nombre={L_PLUR} 
            AND graphies.graphie LIKE "{radical}%"
            AND NOT graphies.graphie  LIKE "%\_%" 
            AND NOT graphies.graphie LIKE "%-%";
        ''')
    return rejsultat


if __name__ == '__main__':
        main()
