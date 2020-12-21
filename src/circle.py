class Circle:
    """
    Cette classe représente simplement un cercle
    """

    # ----- Constructeur -----

    def __init__(self, center, radius):
        """
        Création d'un nouveau cercle avec son centre et son rayon

        params :
            - center = Le centre du cercle sous la forme (x, y)
            - radius = Le rayon du cercle
        """

        self.center = center
        self.radius = radius
