#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "jys"
__copyright__ = "Copyright (C) 2024 LATEJCON"

# l'ordre des modehles donne la prioritej, 
# l'indice de plus haut rang est le + prioritaire
# les ADJxx sont systejmatiquement doublejs par ADV-- ADJxx sans exemples explicites
sp7Modehles = (
    # 
    # à cheval, comme jument, de juments, entre chevaux
    'PREP-- NCms', 'PREP-- NCfs', 'PREP-- NCfp', 'PREP-- NCmp',
    # et cheval, ou jument, mais juments, donc chevaux
    'CONJ-- NCms', 'CONJ-- NCfs', 'CONJ-- NCfp', 'CONJ-- NCmp',
    # le cheval, une jument, mes juments, quatorze chevaux
    'DETms NCms', 'DETfs NCfs', 'DETfp NCfp', 'DETmp NCmp',
    'DETms ADV-- NCms', 'DETfs ADV-- NCfs', 'DETfp ADV-- NCfp', 'DETmp ADV-- NCmp',
    # cher mari, chère femme, chers voisins, belles voisines
    'ADJms NCms', 'ADJfs NCfs', 'ADJmp NCmp', 'ADJfp NCfp', 
    # si son travail, et sa conduite, ou vingt familles, donc des gendarmes
    'CONJ-- DETms NCms', 'CONJ-- DETfs NCfs', 'CONJ-- DETfp NCfp', 'CONJ-- DETmp NCmp',
    # hors motif impérieux, sans cause sérieuse, à balles réelles, sauf services concernés
    'PREP-- NCms ADJms', 'PREP-- NCfs ADJfs', 'PREP-- NCfp ADJfp', 'PREP-- NCmp ADJmp',
    # à moindre frais, sans vraie raison, entre pauvres filles, avec épais nuages
    'PREP-- ADJms NCms', 'PREP-- ADJfs NCfs', 'PREP-- ADJfp NCfp', 'PREP-- ADJmp NCmp',
    # avec le chien, sans la chienne, comme des bêtes, pour dix écus
    'PREP-- DETms NCms', 'PREP-- DETfs NCfs', 'PREP-- DETfp NCfp', 'PREP-- DETmp NCmp',
    'PREP-- DETms ADV-- NCms', 'PREP-- DETfs ADV-- NCfs', 
    'PREP-- DETfp ADV-- NCfp', 'PREP-- DETmp ADV-- NCmp',
    # contenant le portrait, ...
    'V--PR DETms NCms', 'V--PR DETfs NCfs', 'V--PR DETfp NCfp', 'V--PR DETmp NCmp',
    # et contenant le portrait, ...
    'CONJ-- V--PR DETms NCms', 'CONJ-- V--PR DETfs NCfs', 
    'CONJ-- V--PR DETfp NCfp', 'CONJ-- V--PR DETmp NCmp',
    'CONJ-- V--PR DETms ADV-- NCms', 'CONJ-- V--PR DETfs ADV-- NCfs', 
    'CONJ-- V--PR DETfp ADV-- NCfp', 'CONJ-- V--PR DETmp ADV-- NCmp',
    # et garçon poli, mais fille polie, donc femmes puissantes, ni hommes vieux
    'CONJ-- NCms ADJms', 'CONJ-- NCfs ADJfs', 'CONJ-- NCfp ADJfp', 'CONJ-- NCmp ADJmp',
    'CONJ-- NCms ADV-- ADJms', 'CONJ-- NCfs ADV-- ADJfs', 
    'CONJ-- NCfp ADV-- ADJfp', 'CONJ-- NCmp ADV-- ADJmp',
    # et joli garçon, mais jolie fille, donc puissantes femmes, ni jeunes hommes
    'CONJ-- ADJms NCms', 'CONJ-- ADJfs NCfs', 'CONJ-- ADJfp NCfp', 'CONJ-- ADJmp NCmp',
    'CONJ-- ADV-- ADJms NCms', 'CONJ-- ADV-- ADJfs NCfs', 
    'CONJ-- ADV-- ADJfp NCfp', 'CONJ-- ADV-- ADJmp NCmp',
    # le garçon poli, une fille polie, leurs femmes puissantes, des hommes vieux
    'DETms NCms ADJms', 'DETfs NCfs ADJfs', 'DETfp NCfp ADJfp', 'DETmp NCmp ADJmp',
    'DETms NCms ADV-- ADJms', 'DETfs NCfs ADV-- ADJfs', 
    'DETfp NCfp ADV-- ADJfp', 'DETmp NCmp ADV-- ADJmp',
    # puisque le but principal
    'CONJ-- DETms NCms ADJms', 'CONJ-- DETfs NCfs ADJfs', 
    'CONJ-- DETfp NCfp ADJfp', 'CONJ-- DETmp NCmp ADJmp',
    'CONJ-- DETms NCms ADV-- ADJms', 'CONJ-- DETfs NCfs ADV-- ADJfs', 
    'CONJ-- DETfp NCfp ADV-- ADJfp', 'CONJ-- DETmp NCmp ADV-- ADJmp',
    # le joli garçon, une jolie fille, dix vieilles femmes, des pauvres hommes
    'DETms ADJms NCms', 'DETfs ADJfs NCfs', 'DETfp ADJfp NCfp', 'DETmp ADJmp NCmp',
    'DETms ADV-- ADJms NCms', 'DETfs ADV-- ADJfs NCfs', 
    'DETfp ADV-- ADJfp NCfp', 'DETmp ADV-- ADJmp NCmp',
    # puisque le principal but
    'CONJ-- DETms ADJms NCms', 'CONJ-- DETfs ADJfs NCfs', 
    'CONJ-- DETfp ADJfp NCfp', 'CONJ-- DETmp ADJmp NCmp',
    'CONJ-- DETms ADV-- ADJms NCms', 'CONJ-- DETfs ADV-- ADJfs NCfs', 
    'CONJ-- DETfp ADV-- ADJfp NCfp', 'CONJ-- DETmp ADV-- ADJmp NCmp',
    # contenant le flacon vide, ...
    'V--PR DETms NCms ADJms', 'V--PR DETfs NCfs ADJfs', 
    'V--PR DETfp NCfp ADJfp', 'V--PR DETmp NCmp ADJmp',
    'V--PR DETms NCms ADV-- ADJms', 'V--PR DETfs NCfs ADV-- ADJfs', 
    'V--PR DETfp NCfp ADV-- ADJfp', 'V--PR DETmp NCmp ADV-- ADJmp',
    # contenant le joli flacon, ...
    'V--PR DETms ADJms NCms', 'V--PR DETfs ADJfs NCfs', 
    'V--PR DETfp ADJfp NCfp', 'V--PR DETmp ADJmp NCmp',
    'V--PR DETms ADV-- ADJms NCms', 'V--PR DETfs ADV-- ADJfs NCfs', 
    'V--PR DETfp ADV-- ADJfp NCfp', 'V--PR DETmp ADV-- ADJmp NCmp',
    # le joli garçon naïf, une jolie fille pubère, dix vieilles femmes aigries, des pauvres hommes esseulés
    'DETms ADJms NCms ADJms', 'DETfs ADJfs NCfs ADJfs', 
    'DETfp ADJfp NCfp ADJfp', 'DETmp ADJmp NCmp ADJmp',
    'DETms ADV-- ADJms NCms ADJms', 'DETfs ADV-- ADJfs NCfs ADJfs', 
    'DETfp ADV-- ADJfp NCfp ADJfp', 'DETmp ADV-- ADJmp NCmp ADJmp',
    'DETms ADJms NCms ADV-- ADJms', 'DETfs ADJfs NCfs ADV-- ADJfs', 
    'DETfp ADJfp NCfp ADV-- ADJfp', 'DETmp ADJmp NCmp ADV-- ADJmp',
    'DETms ADV-- ADJms NCms ADV-- ADJms', 'DETfs ADV-- ADJfs NCfs ADV-- ADJfs', 
    'DETfp ADV-- ADJfp NCfp ADV-- ADJfp', 'DETmp ADV-- ADJmp NCmp ADV-- ADJmp',
    # contenant le joli flacon vide, ...
    'V--PR DETms ADJms NCms ADJms', 'V--PR DETfs ADJfs NCfs ADJfs', 
    'V--PR DETfp ADJfp NCfp ADJfp', 'V--PR DETmp ADJmp NCmp ADJmp',
    'V--PR DETms ADV-- ADJms NCms ADJms', 'V--PR DETfs ADV-- ADJfs NCfs ADJfs', 
    'V--PR DETfp ADV-- ADJfp NCfp ADJfp', 'V--PR DETmp ADV-- ADJmp NCmp ADJmp',
    'V--PR DETms ADJms NCms ADV-- ADJms', 'V--PR DETfs ADJfs NCfs ADV-- ADJfs', 
    'V--PR DETfp ADJfp NCfp ADV-- ADJfp', 'V--PR DETmp ADJmp NCmp ADV-- ADJmp',
    'V--PR DETms ADV-- ADJms NCms ADV-- ADJms', 'V--PR DETfs ADV-- ADJfs NCfs ADV-- ADJfs', 
    'V--PR DETfp ADV-- ADJfp NCfp ADV-- ADJfp', 'V--PR DETmp ADV-- ADJmp NCmp ADV-- ADJmp',
    # tout le jour, toute une semaine, toutes les semaines, tous les jours
    'DETms DETms NCms', 'DETfs DETfs NCfs', 'DETfp DETfp NCfp', 'DETmp DETmp NCmp',
    # contenant tout le jour, ...
    'V--PR DETms DETms NCms', 'V--PR DETfs DETfs NCfs', 
    'V--PR DETfp DETfp NCfp', 'V--PR DETmp DETmp NCmp',
    # jeune et joli garçon, jeune et jolie fille, jeunes et jolies femmes, jeunes et jolis garçons
    'ADJms CONJ-- ADJms NCms', 'ADJfs CONJ-- ADJfs NCfs', 
    'ADJfp CONJ-- ADJfp NCfp', 'ADJmp CONJ-- ADJmp NCmp',
    'ADV-- ADJms CONJ-- ADJms NCms', 'ADV-- ADJfs CONJ-- ADJfs NCfs', 
    'ADV-- ADJfp CONJ-- ADJfp NCfp', 'ADV-- ADJmp CONJ-- ADJmp NCmp',
    'ADJms CONJ-- ADV-- ADJms NCms', 'ADJfs CONJ-- ADV-- ADJfs NCfs', 
    'ADJfp CONJ-- ADV-- ADJfp NCfp', 'ADJmp CONJ-- ADV-- ADJmp NCmp',
    'ADV-- ADJms CONJ-- ADV-- ADJms NCms', 'ADV-- ADJfs CONJ-- ADV-- ADJfs NCfs', 
    'ADV-- ADJfp CONJ-- ADV-- ADJfp NCfp', 'ADV-- ADJmp CONJ-- ADV-- ADJmp NCmp',
    # garçon jeune et joli, fille jeune et jolie, femmes jeunes et jolies , garçons jeunes et jolis
    'NCms ADJms CONJ-- ADJms', 'NCfs ADJfs CONJ-- ADJfs', 
    'NCfp ADJfp CONJ-- ADJfp', 'NCmp ADJmp CONJ-- ADJmp',
    'NCms ADV-- ADJms CONJ-- ADJms', 'NCfs ADV-- ADJfs CONJ-- ADJfs', 
    'NCfp ADV-- ADJfp CONJ-- ADJfp', 'NCmp ADV-- ADJmp CONJ-- ADJmp',
    'NCms ADJms CONJ-- ADV-- ADJms', 'NCfs ADJfs CONJ-- ADV-- ADJfs', 
    'NCfp ADJfp CONJ-- ADV-- ADJfp', 'NCmp ADJmp CONJ-- ADV-- ADJmp',
    'NCms ADV-- ADJms CONJ-- ADV-- ADJms', 'NCfs ADV-- ADJfs CONJ-- ADV-- ADJfs', 
    'NCfp ADV-- ADJfp CONJ-- ADV-- ADJfp', 'NCmp ADV-- ADJmp CONJ-- ADV-- ADJmp',
    # pour tout le jour, dans toute une semaine, comme toutes les semaines, de tous les jours
    'PREP-- DETms DETms NCms', 'PREP-- DETfs DETfs NCfs', 
    'PREP-- DETfp DETfp NCfp', 'PREP-- DETmp DETmp NCmp',
    # pour le jour entier, comme la semaine dernière, 
    # sauf les semaines paires, entre plusieurs jours singuliers
    'PREP-- DETms NCms ADJms', 'PREP-- DETfs NCfs ADJfs', 
    'PREP-- DETfp NCfp ADJfp', 'PREP-- DETmp NCmp ADJmp',
    'PREP-- DETms NCms ADV-- ADJms', 'PREP-- DETfs NCfs ADV-- ADJfs', 
    'PREP-- DETfp NCfp ADV-- ADJfp', 'PREP-- DETmp NCmp ADV-- ADJmp',
    # pour le même jour, comme la merveilleuse semaine, 
    # sauf les pauvres femmes, entre plusieurs éminents spécialistes
    'PREP-- DETms ADJms NCms', 'PREP-- DETfs ADJfs NCfs',
    'PREP-- DETfp ADJfp NCfp', 'PREP-- DETmp ADJmp NCmp',
    'PREP-- DETms ADV-- ADJms NCms', 'PREP-- DETfs ADV-- ADJfs NCfs',
    'PREP-- DETfp ADV-- ADJfp NCfp', 'PREP-- DETmp ADV-- ADJmp NCmp',
    # le mari vieux et trompé, une femme jeune mais frivole,
    # plusieurs filles éméchées donc hilares, des universitaires tristes puisque sérieux
    'DETms NCms ADJms CONJ-- ADJms', 'DETfs NCfs ADJfs CONJ-- ADJfs',
    'DETfp NCfp ADJfp CONJ-- ADJfp', 'DETmp NCmp ADJmp CONJ-- ADJmp',
    'DETms NCms ADV-- ADJms CONJ-- ADJms', 'DETfs NCfs ADV-- ADJfs CONJ-- ADJfs',
    'DETfp NCfp ADV-- ADJfp CONJ-- ADJfp', 'DETmp NCmp ADV-- ADJmp CONJ-- ADJmp',
    'DETms NCms ADJms CONJ-- ADV-- ADJms', 'DETfs NCfs ADJfs CONJ-- ADV-- ADJfs',
    'DETfp NCfp ADJfp CONJ-- ADV-- ADJfp', 'DETmp NCmp ADJmp CONJ-- ADV-- ADJmp',
    'DETms NCms ADV-- ADJms CONJ-- ADV-- ADJms', 'DETfs NCfs ADV-- ADJfs CONJ-- ADV-- ADJfs',
    'DETfp NCfp ADV-- ADJfp CONJ-- ADV-- ADJfp', 'DETmp NCmp ADV-- ADJmp CONJ-- ADV-- ADJmp',
    # contenant le flacon rouge et bleu, ...
    'V--PR DETms NCms ADJms CONJ-- ADJms', 'V--PR DETfs NCfs ADJfs CONJ-- ADJfs',
    'V--PR DETfp NCfp ADJfp CONJ-- ADJfp', 'V--PR DETmp NCmp ADJmp CONJ-- ADJmp',
    'V--PR DETms NCms ADV-- ADJms CONJ-- ADJms', 'V--PR DETfs NCfs ADV-- ADJfs CONJ-- ADJfs',
    'V--PR DETfp NCfp ADV-- ADJfp CONJ-- ADJfp', 'V--PR DETmp NCmp ADV-- ADJmp CONJ-- ADJmp',
    'V--PR DETms NCms ADJms CONJ-- ADV-- ADJms', 'V--PR DETfs NCfs ADJfs CONJ-- ADV-- ADJfs',
    'V--PR DETfp NCfp ADJfp CONJ-- ADV-- ADJfp', 'V--PR DETmp NCmp ADJmp CONJ-- ADV-- ADJmp',
    'V--PR DETms NCms ADV-- ADJms CONJ-- ADV-- ADJms', 
    'V--PR DETfs NCfs ADV-- ADJfs CONJ-- ADV-- ADJfs',
    'V--PR DETfp NCfp ADV-- ADJfp CONJ-- ADV-- ADJfp', 
    'V--PR DETmp NCmp ADV-- ADJmp CONJ-- ADV-- ADJmp',
    # à bon et juste compte, sans réelle et claire motivation,
    # avec sincères et forts remerciements, sauf justes et nobles causes
    'PREP-- ADJms CONJ-- ADJms NCms', 'PREP-- ADJfs CONJ-- ADJfs NCfs',
    'PREP-- ADJfp CONJ-- ADJfp NCfp', 'PREP-- ADJmp CONJ-- ADJmp NCmp',
    'PREP-- ADV-- ADJms CONJ-- ADJms NCms', 'PREP-- ADV-- ADJfs CONJ-- ADJfs NCfs',
    'PREP-- ADV-- ADJfp CONJ-- ADJfp NCfp', 'PREP-- ADV-- ADJmp CONJ-- ADJmp NCmp',
    'PREP-- ADJms CONJ-- ADV-- ADJms NCms', 'PREP-- ADJfs CONJ-- ADV-- ADJfs NCfs',
    'PREP-- ADJfp CONJ-- ADV-- ADJfp NCfp', 'PREP-- ADJmp CONJ-- ADV-- ADJmp NCmp',
    'PREP-- ADV-- ADJms CONJ-- ADV-- ADJms NCms', 
    'PREP-- ADV-- ADJfs CONJ-- ADV-- ADJfs NCfs',
    'PREP-- ADV-- ADJfp CONJ-- ADV-- ADJfp NCfp', 
    'PREP-- ADV-- ADJmp CONJ-- ADV-- ADJmp NCmp',
    # en tombant
    'PREP-- V--PR',
    # pour pouvoir
    'PREP-- V--IN',
    # est arrivée
    #'V-sCJ ADJms', 'V-pCJ ADJmp', 'V-sCJ ADJfs', 'V-pCJ ADJfp'
    # elle est arrivée
    #'PRONms V-sCJ ADJms', 'PRONmp V-pCJ ADJmp', 'PRONfs V-sCJ ADJfs', 'PRONfp V-pCJ ADJfp'
    )

# graphies interdites comme NCxx
sp7NcInterdits = (
    'abord', 'ailleurs', 'aller', 'an', 'après', 'attendant', 'attendu', 'autre', 'avance', 'avant', 'avoir', 'bas', 'bien', 'blanc', 'bleu', 'bref', 'car', 'cas', 'côté', 'coup', 'dans', 'début', 'dernier', 'dessus', 'douce', 'droit', 'détail', 'effet', 'encore', 'entrant', 'est', 'étant', 'être', 'face', 'façon', 'fait', 'fin', 'fois', 'forme', 'grand', 'grande', 'gros', 'haut', 'hâte', 'jaune', 'jeter', 'juste', 'la', 'large', 'lieu', 'lire', 'loin', 'long', 'lors', 'malgré', 'mieux', 'milieu', 'moins', 'même', 'net', 'noir', 'outre', 'pari', 'paris', 'part', 'partie', 'pas', 'passant', 'peine', 'pendant', 'petit', 'petite', 'peu', 'plus', 'plutôt', 'point', 'pour', 'privé', 'près', 'quantité', 'reste', 'rien', 'rire', 'rouge', 'somme', 'sorte', 'suite', 'suivant', 'tard', 'temps', 'travers', 'tôt', 'tout', 'une', 'vers', 'vert'
    )
