from src.test_bank import TestBank

import os


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
        Méthode à appeler pour lancer tous les tests
        """

        # On parcours les banques de tests
        for test_bank in self.test_banks:

            # On importe les ensembles de points pour chaque fichier
            files_sets = test_bank.import_files()

            # Affichage des resultats
            print("====== Banque de tests : " + test_bank.bank_dir + " ======")
