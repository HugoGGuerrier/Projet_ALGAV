from src.test_bank import TestBank
from src.algorithms import naive_circle, welzl_circle, get_precision

import os
import time


class Tester:
    """
    Cette classe sert à lancer tous les tests prévu sur les banques de tests données.
    C'est elle qui est en charge aussi de l'affichage des résultats de ces tests.
    """

    # ----- Contructeur -----

    def __init__(self, test_bank_dir):
        """
        Création d'un nouvelle instance du testeur avec le chemin de la racine des banques de test

        params :
            - test_bank_dir = Le dossier contenant toutes les banques de test
        """

        self.test_bank_dir = test_bank_dir
        self.test_banks = list()

    # ----- Méthodes de classe -----

    def add_bank(self, bank_dir):
        """
        Ajouter une banque de test au tester à partir du chemin relatif de cette dernière par rapport au répertoire
        contenant toutes les banques de test

        params :
            - bank_dir = Le répertoire contenant la banque de test à ajouter
        """

        new_bank = TestBank(os.path.join(self.test_bank_dir, bank_dir))
        self.test_banks.append(new_bank)

    def run(self):
        """
        Méthode à appeler pour lancer tous les tests et afficher les resultats
        """

        # On parcours les banques de tests
        for test_bank in self.test_banks:

            # On importe les ensembles de points pour chaque fichier
            files_sets = test_bank.import_points()

            # --- Dans un premier temps on parcourt tous les ensembles de points et on applique les deux algorithmes

            # On prépare la liste de résultats pour les premières mesures
            non_accu_results = list()

            for point_set in files_sets:
                result = dict()

                # On mesure le temps mis par la fonction naïve
                naive_start = time.perf_counter()
                naive_res = naive_circle(point_set)
                naive_end = time.perf_counter()

                # On mesure la précision de la fonction naive
                naive_precision = get_precision(point_set, naive_res)

                # On mesure le temps mis par la fonction welzl
                welzl_start = time.perf_counter()
                welzl_res = welzl_circle(point_set)
                welzl_end = time.perf_counter()

                # On mesure la précision du cercle obtenu avec welzl
                welzl_precision = get_precision(point_set, welzl_res)

                # On ajoute les mesures au résultat
                result["nb_points"] = len(point_set)
                result["naive_time"] = naive_end - naive_start
                result["naive_precision"] = naive_precision
                result["welzl_time"] = welzl_end - welzl_start
                result["welzl_precision"] = welzl_precision

                non_accu_results.append(result)

            # --- Le second test consiste à accumuler les points pour avoir un idée de la complexité et de l'évolution de la courbe

            # TODO

            # --- Affichage des resultats

            print("====== Banque de tests : " + test_bank.bank_dir + " ======\n")
            print("Nombre de fichiers de test : " + str(len(files_sets)) + "\n")

            # On affiche les résultats pour la méthode sans accumulation des points
            print("Méthode sans accumulation :\n")

            format_str = "{test_nb:<20}| {point_nb:<20}| {naive_time:<30}| {welzl_time:<30}| {naive_prec:<20}| {welzl_prec:<20}"

            print(format_str.format(
                test_nb="N° du test",
                point_nb="Nb de points",
                naive_time="Temps naïf (s)",
                welzl_time="Temps Welzl (s)",
                naive_prec="Précision naïf",
                welzl_prec="Précision Welzl"
            ))

            accu_naive_time = 0
            accu_naive_prec = 0
            accu_welzl_time = 0
            accu_welzl_prec = 0
            test_number = len(non_accu_results)

            for i in range(len(non_accu_results)):
                result = non_accu_results[i]

                accu_naive_time += result["naive_time"]
                accu_naive_prec += result["naive_precision"]
                accu_welzl_time += result["welzl_time"]
                accu_welzl_prec += result["welzl_precision"]

                print(format_str.format(
                    test_nb=str(i + 1),
                    point_nb=str(result["nb_points"]),
                    naive_time=str(result["naive_time"]),
                    welzl_time=str(result["welzl_time"]),
                    naive_prec=str(result["naive_precision"]),
                    welzl_prec=str(result["welzl_precision"]),
                ))

            print("\nTemps moyen pour la méthode naïve : " + str(accu_naive_time / test_number) + " s")
            print("Temps moyen pour la méthode de Welzl : " + str(accu_welzl_time / test_number) + " s")
            print("Précision moyenne pour la méthode naïve : " + str(accu_naive_prec / test_number))
            print("Précision moyenne pour la méthode de Welzl : " + str(accu_welzl_prec / test_number))
