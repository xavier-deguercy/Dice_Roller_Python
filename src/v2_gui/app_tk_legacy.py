# src/v2_gui/app_tk.py
"""
IHM Tkinter (orientée objet) — Dice Roller

Fonctionnalités couvertes ici :
- Choix du dé (d4, d6, d8, d10, d12, d20, d100)
- US-003 : lancer plusieurs dés (NdY) via un Spinbox "Nombre"
- d20 uniquement : avantage / désavantage (2d20 garder meilleur/pire)
- Inspiration bardique : +1d4 (optionnel)
- US-004 : critiques d20 (1 = échec critique, 20 = réussite critique)

Important :
- L'IHM ne contient PAS les règles : elle appelle la classe DiceRoller (core).
- Pour que l'import marche proprement, lance en module :
  python -m src.v2_gui.app_tk
"""

import tkinter as tk
from tkinter import ttk

# Import "propre" (recommandé) : le core est sous src/core/
from src.core.dice_roller import DiceRoller


class DiceRollerApp(tk.Tk):
    """Application Tkinter : UI séparée du moteur (DiceRoller)."""

    DES_AUTORISES = [4, 6, 8, 10, 12, 20, 100]

    def __init__(self):
        super().__init__()

        # --- Fenêtre ---
        self.title("Dice Roller")
        self.geometry("520x520")
        self.resizable(False, False)

        # --- Moteur (logique métier) ---
        self.roller = DiceRoller()

        # --- État UI (Tkinter Variables) ---
        self.nb_faces_var = tk.StringVar(value="20")           # dé sélectionné (texte)
        self.n_dice_var = tk.IntVar(value=1)                   # US-003 : nombre de dés
        self.mode_d20_var = tk.StringVar(value="normal")       # normal / avantage / desavantage
        self.inspiration_var = tk.BooleanVar(value=False)      # +1d4
        self.result_var = tk.StringVar(value="Résultat : -")   # message affiché

        # Widgets qu’on doit activer/désactiver
        self.spin_n = None
        self.d20_options = None

        # Build UI
        self._build_ui()
        self._refresh_d20_visibility()

    # ---------------------------------------------------------------------
    # UI
    # ---------------------------------------------------------------------

    def _build_ui(self):
        """Construit tous les widgets (une seule fois)."""
        root = ttk.Frame(self, padding=16)
        root.pack(fill="both", expand=True)

        ttk.Label(root, text="Dice Roller", font=("Segoe UI", 16, "bold")).pack(anchor="w")
        ttk.Label(root, text="Choisis un dé, un nombre, puis clique “Lancer”.").pack(anchor="w", pady=(2, 14))

        # ---- Ligne : choix du dé + nombre de dés ----
        line = ttk.Frame(root)
        line.pack(fill="x", pady=(0, 12))

        ttk.Label(line, text="Type de dé :").pack(side="left")

        self.combo_de = ttk.Combobox(
            line,
            textvariable=self.nb_faces_var,
            values=[str(x) for x in self.DES_AUTORISES],
            state="readonly",
            width=8
        )
        self.combo_de.pack(side="left", padx=(10, 18))
        self.combo_de.set("20")

        ttk.Label(line, text="Nombre :").pack(side="left")

        # tk.Spinbox = robuste selon versions Python
        self.spin_n = tk.Spinbox(
            line,
            from_=1,
            to=50,
            width=5,
            textvariable=self.n_dice_var
        )
        self.spin_n.pack(side="left", padx=(10, 0))

        # Mise à jour options quand le dé change
        self.combo_de.bind("<<ComboboxSelected>>", lambda _e: self._refresh_d20_visibility())

        # ---- Options ----
        options = ttk.LabelFrame(root, text="Options", padding=12)
        options.pack(fill="x", pady=(0, 12))

        # Options d20 uniquement
        self.d20_options = ttk.LabelFrame(options, text="D20 uniquement", padding=10)
        self.d20_options.pack(fill="x", pady=(0, 10))
        
        # 
        ttk.Radiobutton(
            self.d20_options,
            text="Normal (1d20) — autorise aussi Nd20",
            value="normal",
            variable=self.mode_d20_var,
            command=self._refresh_d20_visibility
        ).pack(anchor="w")

        # 
        ttk.Radiobutton(
            self.d20_options,
            text="Avantage (2d20, garder le meilleur)",
            value="avantage",
            variable=self.mode_d20_var,
            command=self._refresh_d20_visibility
        ).pack(anchor="w")

        # 
        ttk.Radiobutton(
            self.d20_options,
            text="Désavantage (2d20, garder le moins bon)",
            value="desavantage",
            variable=self.mode_d20_var,
            command=self._refresh_d20_visibility
        ).pack(anchor="w")

        # Inspiration bardique
        ttk.Checkbutton(
            options,
            text="Inspiration bardique (+1d4)",
            variable=self.inspiration_var
        ).pack(anchor="w")

        # ---- Action ----
        ttk.Button(root, text="Lancer", command=self.on_roll_click).pack(anchor="w", pady=(0, 12))

        # ---- Résultat ----
        ttk.Label(root, textvariable=self.result_var, font=("Segoe UI", 11)).pack(anchor="w")

    def _refresh_d20_visibility(self):
        """
        Affiche/masque les options d20.
        Gère aussi le cas : avantage/désavantage => N forcé à 1 (car 2d20 spécifique).
        """
        is_d20 = (self.nb_faces_var.get() == "20")

        if is_d20:
            # Affiche le bloc d20
            self.d20_options.pack(fill="x", pady=(0, 10))
        else:
            # Cache le bloc d20 + remet le mode normal
            self.mode_d20_var.set("normal")
            self.d20_options.forget()

        # Si avantage/désavantage : N doit être 1 (sinon ambigu : 2d20 ou Nd20 ?)
        if is_d20 and self.mode_d20_var.get() in ("avantage", "desavantage"):
            self.n_dice_var.set(1)
            self.spin_n.config(state="disabled")
        else:
            self.spin_n.config(state="normal")

    # ---------------------------------------------------------------------
    # Action principale
    # ---------------------------------------------------------------------

    def on_roll_click(self):
        """Déclenché au clic sur 'Lancer' : lit l’UI, appelle le core, affiche."""
        # 1) Lecture / validation
        try:
            nb_faces = int(self.nb_faces_var.get())
        except ValueError:
            self.result_var.set("Résultat : type de dé invalide")
            return

        try:
            n = int(self.n_dice_var.get())
        except Exception:
            self.result_var.set("Résultat : nombre de dés invalide")
            return

        if nb_faces not in self.DES_AUTORISES:
            self.result_var.set(f"Résultat : dé non supporté (d{nb_faces})")
            return
        if n < 1:
            self.result_var.set("Résultat : le nombre de dés doit être >= 1")
            return

        # 2) Lancer principal (core)
        try:
            msg = self._compute_roll_message(nb_faces, n)
        except Exception:
            self.result_var.set("Résultat : erreur au lancer")
            return

        self.result_var.set(msg)

    def _compute_roll_message(self, nb_faces: int, n: int) -> str:
        """
        Calcule le message final à afficher.
        - d20 + avantage/désavantage => utilise roller.roll_d20(mode)
        - sinon => lance NdY via roll_die en boucle (compatible même si roll_many n'existe pas)
        - inspiration => +1d4
        - critique => uniquement d20 (sur le résultat retenu avant bonus)
        """
        mode = "normal"
        rolls = []
        base = 0  # résultat principal (avant bonus)
        kept = None  # utile pour d20 avantage/désavantage

        # --- Cas d20 avantage/désavantage (spécifique) ---
        if nb_faces == 20 and self.mode_d20_var.get() in ("avantage", "desavantage"):
            mode = self.mode_d20_var.get()
            info = self.roller.roll_d20(mode)  # dict standardisé du core
            rolls = info["rolls"]
            kept = info["final_value"]
            base = kept

            # Forme lisible
            msg = f"d20 {mode} → {rolls} (retenu {kept})"

        else:
            # --- Cas général : NdY (US-003) ---
            # (Si tu ajoutes roll_many dans le core plus tard, on pourra remplacer ici.)
            rolls = [self.roller.roll_die(nb_faces) for _ in range(n)]
            base = sum(rolls)

            if n == 1:
                msg = f"d{nb_faces} → {rolls[0]}"
                base = rolls[0]
            else:
                msg = f"{n}d{nb_faces} → {rolls} (total {base})"

        # --- Critiques d20 (US-004) ---
        # Critique basé sur le résultat d20 retenu (avant bonus)
        # - pour Nd20 en mode normal (n==1), base est le résultat du dé
        # - pour avantage/désavantage, base = kept
        if nb_faces == 20:
            if base == 20:
                msg = "🎉 Réussite critique ! " + msg
            elif base == 1:
                msg = "💀 Échec critique ! " + msg

        # --- Inspiration bardique (+1d4) ---
        if self.inspiration_var.get():
            bonus = self.roller.roll_die(4)
            total = base + bonus
            msg += f" | Inspiration +{bonus} → Total {total}"

        return msg


if __name__ == "__main__":
    app = DiceRollerApp()
    app.mainloop()
