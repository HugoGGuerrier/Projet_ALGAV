from src.circle import Circle
from src.utils import distance, is_inside

import math


def naive_circle(point_set):
    """
    Creer le cercle minimum de l'ensemble de points passé en paramètre en utilisant l'algorithme naïf

    params :
        - point_set = L'ensemble de points à évaluer

    return -> Circle = Le cercle minimum de l'ensemble de points
    """

    # On vérifie la taille de l'ensemble de points
    if len(point_set) <= 0:
        return None

    # On prépare les attribut du cercle
    c_x = 0
    c_y = 0
    c_rad = 0

    # --- Partie 1 : On teste tous les cercle de centre entre deux points

    for p1 in point_set:
        for p2 in point_set:

            # On teste sur les deux points ne sont pas confondus
            if p1 != p2:

                # On calcule le cercle de centre (p1 + p2) / 2 et de rayon |p1p2| / 2
                c_x = (p1[0] + p2[0]) / 2
                c_y = (p1[1] + p2[1]) / 2
                c_rad = distance((c_x, c_y), p2)
                cercle = Circle((c_x, c_y), c_rad)

                # On teste sir tous les points de l'ensemble sont dans le cercle
                if is_inside(point_set, cercle):
                    return cercle

    # --- Partie 2 : On teste tous les cercles circonscrit pour tous les trios de points dans l'ensemble

    for p1 in point_set:
        for p2 in point_set:
            for p3 in point_set:

                # On teste si les trois points sont coolinéaires
                if ((p1[0] - p2[0]) * (p1[1] - p3[1]) - (p1[1] - p2[1]) * (p1[0] - p3[0])) == 0:
                    continue

                # On vérifie que p1 n'est pas sur la même ligne que p2 ou p3 pour éviter les multiplication par 0
                if p1[1] == p2[1]:
                    tmp = p1
                    p1 = p3
                    p3 = tmp
                elif p1[1] == p3[1]:
                    tmp = p1
                    p1 = p2
                    p2 = tmp

                # On récupère les centres des segments p1-p2 et p1-p3
                # Soient m = (p1 + p2) / 2 et n = (p1 + p3) / 2
                m_x = (p1[0] + p2[0]) / 2
                m_y = (p1[1] + p2[1]) / 2
                n_x = (p1[0] + p3[0]) / 2
                n_y = (p1[1] + p3[1]) / 2

                # On calcule les équations des droites d1 et d2 respectivement médianes de p1-p2 et p1-p3
                d1_a = (p2[0] - p1[0]) / (p1[1] - p2[1])
                d1_b = m_y - d1_a * m_x
                d2_a = (p3[0] - p1[0]) / (p1[1] - p3[1])
                d2_b = n_y - d2_a * n_x

                # On peut maintenant avoir les coordonnées du cercle
                c_x = (d2_b - d1_b) / (d1_a - d2_a)
                c_y = d1_a * c_x + d1_b
                c_rad = distance((c_x, c_y), p1)
                cercle = Circle((c_x, c_y), c_rad)

                # On teste si tous les points sont dans le cercle
                if is_inside(point_set, cercle):
                    return cercle


def welzl_circle(point_set):
    """
    Creer le cercle minimum de l'ensemble de point passé en paramètre en utilisant l'algorithme de welzl

    params :
        - point_set = L'ensemble de points à évaluer

    return -> Circle = Le cercle minimum de l'ensemble de points
    """

    res = Circle((0, 0), 0)

    return res


def get_precision(point_set, circle):
    """
    Cette fonction renvoie la proportion de similarités entre deux cercle

    params :
        - circle_ref = Le cercle de référence
        - circle = Le cercle à tester

    return -> float = La proportion de similarités
    """

    # On prépare le résultat
    res = 0

    # On parcourt tous les points de l'ensemble
    for point in point_set:
        if distance(point, circle.center) <= circle.radius:
            res += 1

    # Si on arrive là, alors tous les points sont dans le cercle
    return res / len(point_set)
