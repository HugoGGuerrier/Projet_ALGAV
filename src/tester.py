from src.test_bank import TestBank
from src.algorithms import naive_circle, welzl_circle
from src.utils import get_precision

import os
import time
import sys
import math
import csv
import random


class Tester:
    """
    Cette classe sert à lancer tous les tests prévus sur les banques de tests données
    C'est elle qui est en charge de l'affichage des résultats de ces tests
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

            # On prépare les listes de résultats
            non_accu_results = list()
            accu_results = list()

            # ===== Mesure de l'efficacité des algorithmes =====

            # On affiche le titre
            print("====== Banque de tests : " + test_bank.bank_dir + " ======\n")
            print("Nombre de fichiers de test : " + str(len(files_sets)) + "\n")

            # --- Méthode 1 : Test sur tous les ensemble de points de la banque de test

            # On initialise les variables de test
            done = 0
            total_non_accu = len(files_sets)

            # On affiche le titre de la méthode
            print("Méthode sans accumulation :")

            # On affiche la bar de progression
            self._display_test_state(done, total_non_accu)

            # On parcourt les ensembles de points et on effectue les tests
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
                self._display_test_state(done, total_non_accu)

            # --- Méthode 2 : Accumulation des points pour tester la monté en charge des algorithmes

            # On définit les valeurs que l'on veut tester
            test_values = [10, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600]

            # On initialise les variables de test
            done = 0
            total_accu = len(test_values)
            current_set_index = 0
            current_set = list(files_sets[0])
            point_accumulator = list()

            # On affiche le titre de la méthode
            print("Méthode avec accumulation :")

            # On affiche la barre de progression
            self._display_test_state(done, total_accu)

            # On parcourt les valeurs a tester et on effectue les mesures
            while done < len(test_values):

                # On récupère la valeur visée
                target_value = test_values[done]
                missing = target_value - len(point_accumulator)

                if missing <= len(current_set):
                    point_accumulator = point_accumulator + current_set[:missing]
                    current_set = current_set[missing:]
                else:
                    point_accumulator = point_accumulator + current_set
                    current_set_index += 1
                    if current_set_index < len(files_sets):
                        current_set = list(files_sets[current_set_index])
                        continue
                    else:
                        print("\n!!! Il n'y a pas assez de points disponibles !!!\n")
                        break

                random.shuffle(point_accumulator)
                point_set = set(point_accumulator)

                # On effectue les tests sur l'accumulateur de points
                result = dict()

                # On mesure le temps de la méthode naive
                naive_start = time.perf_counter()
                naive_res = naive_circle(point_set)
                naive_end = time.perf_counter()

                # On mesure la précision de la fonction naive
                naive_precision = get_precision(point_set, naive_res)

                # On mesure le temps de la méthode de Welzl
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

                accu_results.append(result)

                # On met à jour la barre de progression
                self._display_test_state(done + 1, total_accu)

                # On incrémente done
                done += 1

            # ===== Exportation des résultats =====

            # On ouvre les fichier CSV
            non_accu_export_file = open(test_bank.name + "_non_accu_results.csv", "w", newline='')
            accu_export_file = open(test_bank.name + "_accu_results.csv", "w", newline='')

            # On défini le nom des colonnes
            col_names = ["nb_points", "naive_time", "naive_precision", "welzl_time", "welzl_precision"]

            # On créer les scribes CSV
            na_writer = csv.DictWriter(non_accu_export_file, fieldnames=col_names)
            na_writer.writeheader()
            a_writer = csv.DictWriter(accu_export_file, fieldnames=col_names)
            a_writer.writeheader()

            # On exporte les résultats de non accumulation
            for res in non_accu_results:
                na_writer.writerow(res)

            # On On exporte les résultats de l'accumulation
            for res in accu_results:
                a_writer.writerow(res)

            # On fermes les fichiers
            non_accu_export_file.close()
            accu_export_file.close()

            # ===== Affichage des résultats =====

            print("\n===== Résultats =====")
            print("\n--- Méthode sans accumulation :\n")

            format_str = "{test_nb:<20}| {point_nb:<20}| {naive_time:<20}| {welzl_time:<20}| {naive_prec:<20}| {welzl_prec:<20}"

            print(format_str.format(
                test_nb="N° du test",
                point_nb="Nb de points",
                naive_time="Temps naïf (s)",
                welzl_time="Temps Welzl (s)",
                naive_prec="Précision naïf",
                welzl_prec="Précision Welzl"
            ))

            total_point_nb = 0
            total_naive_time = 0
            total_naive_prec = 0
            total_welzl_time = 0
            total_welzl_prec = 0

            for i in range(len(non_accu_results)):
                result = non_accu_results[i]

                total_point_nb += result["nb_points"]
                total_naive_time += result["naive_time"]
                total_naive_prec += result["naive_precision"]
                total_welzl_time += result["welzl_time"]
                total_welzl_prec += result["welzl_precision"]

                print(format_str.format(
                    test_nb=str(i + 1),
                    point_nb=str(result["nb_points"]),
                    naive_time=str(round(result["naive_time"], 10)),
                    welzl_time=str(round(result["welzl_time"], 10)),
                    naive_prec=str(result["naive_precision"]),
                    welzl_prec=str(result["welzl_precision"]),
                ))

            print("\nNombre moyen de points dans un ensemble : " + str(total_point_nb / total_non_accu))
            print("Temps moyen pour la méthode naïve : " + str(total_naive_time / total_non_accu) + " s")
            print("Temps total pour la méthode naïve : " + str(total_naive_time) + " s")
            print("Temps moyen pour la méthode de Welzl : " + str(total_welzl_time / total_non_accu) + " s")
            print("Temps total pour la méthode de Welzl : " + str(total_welzl_time) + " s")
            print("Précision moyenne pour la méthode naïve : " + str(total_naive_prec / total_non_accu))
            print("Précision moyenne pour la méthode de Welzl : " + str(total_welzl_prec / total_non_accu))

            print("\n--- Méthode avec accumulation :\n")

            print(format_str.format(
                test_nb="N° du test",
                point_nb="Nb de points",
                naive_time="Temps naïf (s)",
                welzl_time="Temps Welzl (s)",
                naive_prec="Précision naïf",
                welzl_prec="Précision Welzl"
            ))

            for i in range(len(accu_results)):
                result = accu_results[i]

                print(format_str.format(
                    test_nb=str(i + 1),
                    point_nb=str(result["nb_points"]),
                    naive_time=str(round(result["naive_time"], 10)),
                    welzl_time=str(round(result["welzl_time"], 10)),
                    naive_prec=str(result["naive_precision"]),
                    welzl_prec=str(result["welzl_precision"]),
                ))
