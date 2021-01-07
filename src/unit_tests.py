from src.utils import distance, diameter_circle, circumscribed_circle, point_in_circle, get_precision
from src.algorithms import naive_circle, trivial
from src.utils import distance
from src.circle import Circle


def do_unit_tests():
    """
    Cette méthode lance tous les tests unitaires pour vérifier si les algorithmes et les fonctions utiles font bien leur
    boulot
    """

    # On teste la fonction de calcul de distance entre 2 points
    assert distance((0, 0), (0, 0)) == 0
    assert distance((521, 12), (521, 12)) == 0
    assert distance((0, 0), (1, 0)) == 1
    assert distance((-1, -1), (1, -1)) == 2
    assert distance((0, 0), (0, 256)) == 256

    # On teste la fonction de création du plus petit cercle passant par deux point
    assert diameter_circle((0, 0), (0, 0)).center == (0, 0)
    assert diameter_circle((0, 0), (0, 0)).radius == 0

    assert diameter_circle((0, 0), (0, 1)).center == (0, 0.5)
    assert diameter_circle((0, 0), (0, 1)).radius == 0.5

    assert diameter_circle((-5, 0), (5, 0)).center == (0, 0)
    assert diameter_circle((-5, 0), (5, 0)).radius == 5

    # On teste la fonction de creation d'un cercle circonscrit
    assert circumscribed_circle((0, 0), (0, 0), (0, 0)) is None

    assert circumscribed_circle((0, 0), (0, 1), (1, 0)).center == (0.5, 0.5)
    assert circumscribed_circle((0, 0), (0, 1), (1, 0)).radius == distance((0.5, 0.5), (0, 0))

    # On teste la fonction de vérification d'un point dans un cercle
    assert point_in_circle((0, 0), Circle((0, 0), 0))
    assert point_in_circle((1, 1), Circle((0, 0), 2))
    assert not point_in_circle((1, 1), Circle((0, 0), 1))

    # On déclare tous les ensemble de points de test
    point_set1 = {(0, 0), (0, 1)}
    point_set2 = {(0, 0), (0, 2)}
    point_set3 = {(0, -1), (0, 0)}
    point_set4 = {(0, 0), (0, 1), (0, 2)}
    point_set5 = {(0, 0), (4, 0), (0, 4)}
    point_set6 = {(0, 0), (4, 0), (0, 4), (3, 3)}
    point_set7 = {(1, 1)}
    point_set8 = set()

    # On teste l'algorithme naif
    assert naive_circle(point_set1).center == (0, 0.5)
    assert naive_circle(point_set1).radius == 0.5

    assert naive_circle(point_set2).center == (0, 1)
    assert naive_circle(point_set2).radius == 1

    assert naive_circle(point_set3).center == (0, -0.5)
    assert naive_circle(point_set3).radius == 0.5

    assert naive_circle(point_set4).center == (0, 1)
    assert naive_circle(point_set4).radius == 1

    assert naive_circle(point_set5).center == (2, 2)
    assert naive_circle(point_set5).radius == distance((2, 2), (0, 0))

    assert naive_circle(point_set6).center == (2, 2)
    assert naive_circle(point_set6).radius == distance((2, 2), (0, 0))

    # On teste la fonction trivial utilisée pour l'algorithme de Welzl
    assert trivial(point_set1).center == (0, 0.5)
    assert trivial(point_set1).radius == 0.5

    assert trivial(point_set7).center == (1, 1)
    assert trivial(point_set7).radius == 0

    assert trivial(point_set8).center == (0, 0)
    assert trivial(point_set8).radius == 0

    assert trivial(point_set4).center == (0, 1)
    assert trivial(point_set4).radius == 1

    assert trivial(point_set6) is None

    # On affiche que tous les tests sont passés
    print("Tous les tests unitaires sont passés !")
