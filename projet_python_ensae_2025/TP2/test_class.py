from dataclasses import dataclass
import random as rd

@dataclass
class Voiture:
    marque: str = ""
    vitesse: int = 0 
    prix_millier: int = 0
    
    def afficher_cara(self):
        print(f"les fonctionnalité de ma voiture sont la vitesse, {self.vitesse}, la marque {self.marque} et elle coûte {self.prix_millier} millier d'€")

    def voiture_random(self, list_marque: list = [],list_vitesse: list = [],list_prix: list = []) -> str :
        m = rd.randint(len(list_marque))
        marq = list_marque[m]
        v = rd.randint(len(list_vitesse))
        vit = list_vitesse[v]
        p = rd.randint(len(list_prix))
        pri = list_prix[p]
        return f"ta voiture de trou duq est une {marq} qui va à {vit}km/h. Elle t'as fait cracher {pri} millier de tunes"



voiture_1 = Voiture("Porsche",310)

#voiture_1.afficher_cara()

Voiture.voiture_random(voiture_1)
