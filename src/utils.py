import math


def distance(p1, p2):
    """
    Simple fonction pour calculer la distance entre deux points

    params :
        - p1 = Le point 1
        - p2 = Le point 2

    return -> float = La distance entre les deux points
    """

    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)


def is_inside(point_set, circle):
    """
    Vérifie si tous les points de l'ensemble sont à l'interieur du cercle

    params :
        - point_set = L'ensemble de points à vérifier
        - circle = Le cercle

    return -> bool = True si tous les points sont dans le cercle
    """

    # On parcourt tous les points de l'ensemble
    for point in point_set:
        if distance(point, circle.center) > circle.radius:
            return False

    # Si on arrive là, alors tous les points sont dans le cercle
    return True
