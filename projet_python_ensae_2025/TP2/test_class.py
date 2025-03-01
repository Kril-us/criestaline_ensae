class Voiture:
    def __init__(self,marque,vitesse):
        self.marque = marque
        self.vitesse = vitesse

    def afficher_cara(self):
        print(f"les fonctionnalité de ma voiture sont la vitesse, {self.vitesse} et la marque {self.marque}")

voiture_1 = Voiture("Porsche",310)

voiture_1.afficher_cara()