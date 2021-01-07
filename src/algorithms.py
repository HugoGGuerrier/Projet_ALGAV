from src.circle import Circle
from src.utils import distance, set_in_circle, point_in_circle, circumscribed_circle, diameter_circle

import random


def naive_circle(point_set):
    """
    Creer le cercle minimum de l'ensemble de points passé en paramètre en utilisant l'algorithme naïf
    On concidère cette méthode comme la méthode de référence

    params :
        - point_set = L'ensemble de points à évaluer

    return -> Circle = Le cercle minimum de l'ensemble de points
    """

    # On vérifie la taille de l'ensemble de points
    if len(point_set) <= 0:
        return None

    # --- Partie 1 : On teste tous les cercle de centre entre deux points

    for p1 in point_set:
        for p2 in point_set:

            # On teste sur les deux points ne sont pas confondus
            if p1 != p2:

                # On calcule le cercle de centre (p1 + p2) / 2 et de rayon |p1p2| / 2
                cercle = diameter_circle(p1, p2)

                # On teste sir tous les points de l'ensemble sont dans le cercle
                if set_in_circle(point_set, cercle):
                    return cercle

    # --- Partie 2 : On teste tous les cercles circonscrit pour tous les trios de points dans l'ensemble

    for p1 in point_set:
        for p2 in point_set:
            for p3 in point_set:

                # On récupère le cercle circonscrit des trois points
                cercle = circumscribed_circle(p1, p2, p3)

                # On teste si tous les points sont dans le cercle
                if cercle is not None and set_in_circle(point_set, cercle):
                    return cercle


def trivial(r):
    """
    Fonction triviale permettant de trouver un cercle avec tous les points de r sur sa limite

    params :
        - r = Un ensemble de points avec |r| <= 3

    return -> Circle = Le cercle avec tous les points de r à sa limite
    """

    # Si r ne contient pas de points
    if len(r) == 0:
        return Circle((0, 0), 0)

    # Si r contient 1 point
    elif len(r) == 1:
        return Circle(list(r)[0], 0)

    # Si r contient 2 points
    elif len(r) == 2:
        r = list(r)
        return diameter_circle(r[0], r[1])

    # Si r contient 3 points ou plus
    elif len(r) == 3:
        r = list(r)

        # On vérifie si on ne peut pas déterminer le cercle avec seulement 2 points
        if point_in_circle(r[2], diameter_circle(r[0], r[1])):
            return diameter_circle(r[0], r[1])
        elif point_in_circle(r[1], diameter_circle(r[0], r[2])):
            return diameter_circle(r[0], r[2])
        elif point_in_circle(r[0], diameter_circle(r[1], r[2])):
            return diameter_circle(r[1], r[2])

        return circumscribed_circle(r[0], r[1], r[2])

    # Autrement on retourne None
    return None


def welzl(p, r):
    """
    Cette fonction est l'implémentation rigoureuse de l'algorithme de Welzl tel que décris dans la revue

    params :
        - p = Une liste de points
        - r = Un accumulateur de points

    return -> Circle = Le plus petit cercle couvrant tous les points de p
    """

    # On fait des copies locales des arguments pour ne pas fausser l'algorithme
    p = p.copy()
    r = r.copy()

    # On applique le corps de l'algorithme de Welzl
    if len(p) == 0 or len(r) == 3:
        res = trivial(r)
    else:
        rand_point = p.pop(0)
        res = welzl(p, r)
        if res is not None and not point_in_circle(rand_point, res):
            r.append(rand_point)
            res = welzl(p, r)

    # On retourne le cercle résultat
    return res


def welzl_circle(point_set):
    """
    Creer le cercle minimum de l'ensemble de point passé en paramètre en utilisant l'algorithme de welzl

    params :
        - point_set = L'ensemble de points à évaluer

    return -> Circle = Le cercle minimum de l'ensemble de points
    """

    # On transforme l'ensemble en liste pour le mélanger et éviter de faire un tirage aléatoire a chaque fois
    point_list = list(point_set)
    random.shuffle(point_list)

    # On lance l'algorithme de Welzl
    return welzl(point_list, list())
