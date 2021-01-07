from src.circle import Circle

import math


def distance(p1, p2):
    """
    Simple fonction pour calculer la distance entre deux points

    params :
        - p1 = Le point 1
        - p2 = Le point 2

    return -> float = La distance euclidienne entre les deux points
    """

    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)


def diameter_circle(p1, p2):
    """
    Cette fonction retourne le plus petit cercle passant par p1 et p2

    params :
        - p1 = Le point 1
        - p2 = Le point 2

    return -> Circle = Le cercle
    """

    c_x = (p1[0] + p2[0]) / 2
    c_y = (p1[1] + p2[1]) / 2
    c_rad = distance((c_x, c_y), p1)
    return Circle((c_x, c_y), c_rad)


def circumscribed_circle(p1, p2, p3):
    """
    Cette fonction retourne le cercle circonscrit dans le triangle formé par les trois points

    params :
        - p1 = Le point 1
        - p2 = Le point 2
        - p3 = Le point 3

    return -> Circle = Le cercle circonscrit
    """

    # On vérifie que les points ne soient pas colinéaires
    if ((p1[0] - p2[0]) * (p1[1] - p3[1]) - (p1[1] - p2[1]) * (p1[0] - p3[0])) == 0:
        return None

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

    # On retourne le résultat
    return Circle((c_x, c_y), c_rad)


def point_in_circle(point, circle):
    """
    Cette fonction retourne si le point est dans le cercle

    params :
        - point = Le point a tester
        - circle = Le cercle

    return -> bool = True si le point est dans le cercle
    """

    return distance(point, circle.center) <= circle.radius


def set_in_circle(point_set, circle):
    """
    Vérifie si tous les points de l'ensemble sont à l'interieur du cercle

    params :
        - point_set = L'ensemble de points à vérifier
        - circle = Le cercle

    return -> bool = True si tous les points sont dans le cercle
    """

    # On parcourt tous les points de l'ensemble
    for point in point_set:
        if not point_in_circle(point, circle):
            return False

    # Si on arrive là, alors tous les points sont dans le cercle
    return True


def get_precision(point_set, circle):
    """
    Cette fonction renvoie la proportion de points de l'ensemble dans le cercle

    params :
        - point_set = L'ensemble de points a tester
        - circle = Le cercle à tester

    return -> float = La proportion de points à l'interieur du cercle
    """

    # On verifie que l'ensemble de points n'est pas vide
    if len(point_set) <= 0:
        return 1

    # On prépare le résultat
    res = 0

    # On parcourt tous les points de l'ensemble
    for point in point_set:
        if distance(point, circle.center) <= circle.radius:
            res += 1

    # On revoie la proportion
    return res / len(point_set)