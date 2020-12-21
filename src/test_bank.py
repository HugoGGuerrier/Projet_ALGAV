import os


class TestBank:
    """
    Cette classe représente une banque de test, avec tous les fichiers qui lui sont associés.
    Ces fichiers devront être au format :
    x1 y2
    x2 y2
    x3 y3
    ...
    """

    # ----- Constructeur -----

    def __init__(self, bank_dir):
        """
        Création d'une nouvelle banque de test à partir d'un répertoire contenant tous les fichiers

        params :
            - bank_dir = Le chemin absolu vers le répertoire de la banque de test
        """

        self.bank_dir = bank_dir
        self.test_files = list()

        # On récupère tous les fichiers dans la banque de test
        for f in os.listdir(self.bank_dir):
            _, extension = os.path.splitext(f)
            if os.path.isfile(os.path.join(self.bank_dir, f)) and extension == ".points":
                self.test_files.append(os.path.join(self.bank_dir, f))

    # ----- Méthodes de classe -----

    def import_points(self):
        """
        Importe tous les points défini dans la banque de test et retourne la liste des ensembles de points défini dans
        les fichiers

        return -> list[set[(int, int))]] = La liste des ensembles de points
        """

        # On prépare le resultat
        res = list()

        # On parcours la liste des fichiers à importer
        for to_import in self.test_files:

            # On ouvre le fichier à lire et on initialise l'ensemble de points
            f = open(to_import, "r")
            points = set()

            # On lit ligne par ligne et on extrait les points
            for line in f.readlines():
                split_line = line.split("\n")[0]
                split_line = split_line.split(" ")
                new_point = (int(split_line[0]), int(split_line[1]))
                points.add(new_point)

            # On referme le fichier
            f.close()

            # On ajoute l'ensemble de points à la liste de résultat
            res.append(points)

        # on retourne le résultat de l'importation
        return res
