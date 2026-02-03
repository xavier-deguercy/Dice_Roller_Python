import random  

# ici on vas definir la classe DiceRoller
class DiceRoller:                                                                   # classe pour gérer le lancer de dés
    DES_AUTORISES = [4, 6, 8, 10, 12, 20, 100]                                      # liste des dés autorisés

    def roll_die(self, nb_faces: int) -> int:                                       # méthode pour lancer un dé
        if nb_faces not in self.DES_AUTORISES: 
            raise ValueError(f"Dé non supporté : d{nb_faces}")

        return random.randint(1, nb_faces)

    def roll_d20(self, mode: str = "normal") -> dict:
        """
        Retourne un dict pour que l'UI puisse afficher des détails.
        mode: "normal" | "avantage" | "desavantage"
        """
        if mode not in ("normal", "avantage", "desavantage"):
            raise ValueError("mode d20 invalide")

        if mode == "normal":
            r = self.roll_die(20)
            return {"mode": mode, "rolls": [r], "selected": r}

        r1 = self.roll_die(20)
        r2 = self.roll_die(20)
        selected = max(r1, r2) if mode == "avantage" else min(r1, r2)
        return {"mode": mode, "rolls": [r1, r2], "selected": selected}
    # 
    def roll_many(self, nb_faces: int, n: int) -> dict:
        if not isinstance(n, int) or n < 1:
            raise ValueError("n doit être un entier >= 1")

        rolls = [self.roll_die(nb_faces) for _ in range(n)]
        return {"nb_faces": nb_faces, "n": n, "rolls": rolls, "total": sum(rolls)}

def main(): # fonction principale
    
    print("=== Dice Roller - US-002 (OOP) ===")                                     # titre de l'application
    roller = DiceRoller()                                                           # création d'une instance de DiceRoller

    print(f"Dés autorisés : {roller.DES_AUTORISES}")                                # afficher les dés autorisés
    saisie = input("Nombre de faces du dé (ex: 6 pour d6) : ")                      # demander le nombre de faces
 




