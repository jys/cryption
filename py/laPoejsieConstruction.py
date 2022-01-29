#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "jys"
__copyright__ = "Copyright (C) 2022 LATEJCON"

import sys
from os import path
import codecs
import re

def usage():
    script = '$PY/' + path.basename(sys.argv[0])
    print (f"""© l'ATEJCON.
Construction des affichages de la poejsie c'est...

usage   : {script} <fichier des phrases> <fichier html de résultats>
usage   : {script} phrases.txt ../site/latejcon.art/latejconsledise/lit-17-A-laPoejsieCest.html
""")

def main():
    try:
        if len(sys.argv) < 3 : raise Exception()
        nomFichierTxt = sys.argv[1]
        nomFichierHtml = sys.argv[2]
        construit(nomFichierTxt, nomFichierHtml)
    except Exception as exc:
        if len(exc.args) == 0: usage()
        else:
            print ("******************************")
            print (exc.args[0])
            print ("******************************")
            raise
        sys.exit()
        
################################
def construit(nomFichierTxt, nomFichierHtml):
    # ouvre le fichier d'entreje et extrait toutes les phrases
    with codecs.open(nomFichierTxt, 'r', 'utf8') as fichierTxt:
        phrases = fichierTxt.read().split('.')
    # ouvre le fichier de sortie et ejcrit le dejbut
    fichierHtml = codecs.open(nomFichierHtml, 'w', 'utf8')
    ejcritDejbut(fichierHtml)
    for phrase in phrases: ejcritPhrase(fichierHtml, phrase)
    # ejcrit la fin et ferme le fichier
    ejcritFin(fichierHtml)
    fichierHtml.close()

################################
def ejcritPhrase(fichierHtml, phrase):
    # calcule le nombre magique
    nbMagique = 0x55
    for carac in phrase.encode(): nbMagique^=carac
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
    if 'feuille' in phrase: fichierHtml.write('<img id="imgright" alt="lit-17-A-A-feuille.png" src="lit-17-A-A-feuille.png"/>\n')
    if 'fleur' in phrase: fichierHtml.write('<img id="imgleft" alt="lit-17-A-B-fleurs.png" src="lit-17-A-B-fleurs.png"/>\n')
    if 'oison' in phrase: fichierHtml.write('<img id="imgleft" alt="lit-17-A-C-oiseau.png" src="lit-17-A-C-oiseau.png"/>\n')
    if 'plume' in phrase: print(phrase)
    
    fichierHtml.write(f'{deb}{phrase}.{fin}\n')

################################
def ejcritDejbut(fichierHtml):
    fichierHtml.write("""
<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" href="latejconsledise-1-2.css">
<meta http-equiv="content-type" content="text/html; charset=utf-8">
<title>la poejsie c'est...</title>
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
<td id="td2"><h1>&nbsp;&nbsp;La poejsie c'est...</h1>

<br/><br/>
<img id="imgright" alt="lit-17-A-D-plume.png" src="lit-17-A-D-plume.png"/>
Ça s'est passé en 2003. À la radio, quelqu'un a cité Jean Tardieu : "<b>La poésie, c’est quand un mot rencontre un autre mot pour la première fois.</b>"
<br/><br/>Plus tard, pour retrouver cette citation, il a ejté demandé à Google de chercher les articles qui contenaient le dejbut de phrase <b>"la poésie c'est"</b> (avec les apostrophes). Et Google a donné une liste trehs longue de pages Internet en affichant l'extrait avec le texte recherché. C'ejtait autant de dejfinitions de la poejsie. Certaines ejtaient de vraies dejfinitions, d'autres ejtaient plus improbables, en particulier celles qui avaient le texte recherché à cheval sur deux phrases : "<b>... la poésie. C'est ...</b>".
<br/>Il fut ejvident que le moteur de recherche avait fait œuvre poejtique ! Nous en prejsentons ici le rejsultat.
(maintenant, il faut utiliser Qwant plutost que Google pour que ça fonctionne).
<br/><br/>Peut-estre que Tzara, Breton, Soupault auraient ejté enthousiasmejs par l’informatique et par Internet. Mais peut-estre pas... Parce qu'ils s'intejressaient surtout à la mejcanique de l'inconscient. Allez savoir... Les Oulipiens ? Oui, peut-être... En tout cas, nous, ça nous enthousiasme et en accord avec nous-mesme, nous dejclarons haut et fort que <b>la poejsie c'est aussi la sidejration sejmantique surgie d'un quasi-hasard piloté</b>. (convainquez-vous-en avec <b><a target="_blank" href="http://lab.latejcon.art:55557/cgi-bin/QuasiCryption">la quasi-cryption</a></b>.)
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
<script type="text/javascript">
function souris(event)
{
  // la taille de l'ejcran
  const ejcranH = window.innerWidth;
  const ejcranV = window.innerHeight;
  // la taille de la page
  const pageH  = document.documentElement.scrollWidth;
  const pageV = document.documentElement.scrollHeight;
  // les coordonnejes de la souris
  const x = event.clientX;
  const y = event.clientY;
  // les talons
  const talH = 80
  const talV = 100
  // les increjments  
  const incH = (pageH - ejcranH) / (ejcranH - 2*talH)
  const incV = (pageV - ejcranV) / (ejcranV - 2*talV)
  // positionnement de la page
  var posH = 0
  var posV = 0
  if (x > talH) {
    posH = (x - talH) * incH; 
  }
  if (y > talV) {
    posV = (y - talV) * incV; 
  }
  window.scrollTo(posH, posV)
}
</script>

</body>
</html>

""")
    



if __name__ == '__main__':
        main()
