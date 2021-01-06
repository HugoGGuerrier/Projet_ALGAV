from src.test_bank import TestBank
from src.algorithms import naive_circle, welzl_circle, get_precision

import os
import time
import sys
import math


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

    # ----- Méthodes internes -----

    def _display_test_state(self, passed_tests, total_tests):
        """
        Cette méthode sert à afficher l'état des tests, pour ne pas attendre 15 minutes pour rien

        params :
            - passed_tests = Le nombre de tests passés
            - total_tests = Le nombre total de tests
        """

        prop = passed_tests / total_tests

        done_number = math.floor(prop * 20)
        leave_number = 20 - done_number

        progress_bar = "\t[" + ("█" * done_number) + (" " * leave_number) + "] - " + str(passed_tests) + "/" + str(total_tests)

        # Display the progress bar
        sys.stdout.write(progress_bar)
        sys.stdout.flush()

        # Display a carriage return
        if prop < 1:
            sys.stdout.write("\r")
            sys.stdout.flush()
        else:
            sys.stdout.write("\n")
            sys.stdout.flush()

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
            # On compare ainsi la rapidité et l'efficacité de chaque méthode

            # On prépare la liste de résultats pour les premières mesures
            non_accu_results = list()

            # On affiche la bar de progression
            done = 0
            total = len(files_sets)
            self._display_test_state(done, total)

            # On affiche le titre
            print("====== Banque de tests : " + test_bank.bank_dir + " ======\n")
            print("Nombre de fichiers de test : " + str(total) + "\n")

            # On affiche les résultats pour la méthode sans accumulation des points
            print("Méthode sans accumulation :")

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

                # On met à jour la barre de progression
                done += 1
                self._display_test_state(done, total)

            # --- Le second test consiste à accumuler les points pour avoir un idée de la complexité et de l'évolution de la courbe

            # TODO

            # --- Affichage des resultats

            print("")

            format_str = "{test_nb:<20}| {point_nb:<20}| {naive_time:<20}| {welzl_time:<20}| {naive_prec:<20}| {welzl_prec:<20}"

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

            for i in range(len(non_accu_results)):
                result = non_accu_results[i]

                accu_naive_time += result["naive_time"]
                accu_naive_prec += result["naive_precision"]
                accu_welzl_time += result["welzl_time"]
                accu_welzl_prec += result["welzl_precision"]

                print(format_str.format(
                    test_nb=str(i + 1),
                    point_nb=str(result["nb_points"]),
                    naive_time=str(round(result["naive_time"], 10)),
                    welzl_time=str(round(result["welzl_time"], 10)),
                    naive_prec=str(result["naive_precision"]),
                    welzl_prec=str(result["welzl_precision"]),
                ))

            print("\nTemps moyen pour la méthode naïve : " + str(accu_naive_time / total) + " s")
            print("Temps moyen pour la méthode de Welzl : " + str(accu_welzl_time / total) + " s")
            print("Précision moyenne pour la méthode naïve : " + str(accu_naive_prec / total))
            print("Précision moyenne pour la méthode de Welzl : " + str(accu_welzl_prec / total))
