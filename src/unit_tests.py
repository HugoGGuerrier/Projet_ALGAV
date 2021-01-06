from src.algorithms import naive_circle
from src.utils import distance


def do_unit_tests():
    """
    Cette méthode lance tous les tests unitaires pour vérifier si les algorithmes font bien leur boulot
    """

    # On déclare tous les ensemble de points de test
    point_set1 = {(0, 0), (0, 1)}
    point_set2 = {(0, 0), (0, 2)}
    point_set3 = {(0, -1), (0, 0)}
    point_set4 = {(0, 0), (0, 1), (0, 2)}
    point_set5 = {(0, 0), (4, 0), (0, 4)}
    point_set6 = {(0, 0), (4, 0), (0, 4), (3, 3)}

    # On test les algorithmes
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

    # On affiche que tous les tests sont passés
    print("Tous les tests unitaires sont passés !")
