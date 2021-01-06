from src.tester import Tester
from src.unit_tests import do_unit_tests

import os
import sys


# Récupération du chemin absolu du répertoire courrant
base_path = os.path.abspath(".") + os.path.sep

# Définition des banques de tests à lire dans le répertoire "test_bank"
# test_banks = ["Varoumas/samples"]
test_banks = ["Hugo/samples"]

# Lancement du programme principal
if __name__ == "__main__":

    # On regarde si on doit lancer les tests unitaires
    if len(sys.argv) >= 2 and sys.argv[1] == "test_unit":
        do_unit_tests()
    else:
        # On crée un nouveau testeur
        tester = Tester(base_path + "test_bank" + os.path.sep)

        # On ajoute toutes les banques de test voulu
        for bank in test_banks:
            tester.add_bank(bank)

        # On lance les tests
        tester.run()
