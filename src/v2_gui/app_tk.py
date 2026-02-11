"""
Interface Tkinter de Dice Roller.

Cette couche:
- lit les choix utilisateur,
- appelle le core (`DiceRoller.resolve_roll`),
- transforme le resultat en texte lisible.
"""

import tkinter as tk
from tkinter import ttk

from src.core.dice_roller import DiceRoller


class DiceRollerApp(tk.Tk):
    """
    Fenetre principale Tkinter.

    Important:
    - pas de regles de lancer ici,
    - le core decide des resultats, l'UI ne fait que presenter.
    """

    def __init__(self):
        super().__init__()

        self.title("Dice Roller")
        self.geometry("520x520")
        self.resizable(False, False)

        self.roller = DiceRoller()

        # Etat UI: ces variables sont liees aux widgets Tkinter.
        self.nb_faces_var = tk.StringVar(value="20")
        self.n_dice_var = tk.IntVar(value=1)
        self.mode_d20_var = tk.StringVar(value="normal")
        self.inspiration_var = tk.BooleanVar(value=False)
        self.result_var = tk.StringVar(value="Resultat : -")

        self.spin_n = None
        self.d20_options = None

        self._build_ui()
        self._refresh_d20_visibility()

    def _build_ui(self):
        """Construit l'interface une seule fois."""
        root = ttk.Frame(self, padding=16)
        root.pack(fill="both", expand=True)

        ttk.Label(
            root,
            text="Dice Roller",
            font=("Segoe UI", 16, "bold"),
        ).pack(
            anchor="w"
        )
        ttk.Label(
            root,
            text="Choisis un de, un nombre, puis clique Lancer.",
        ).pack(anchor="w", pady=(2, 14))

        line = ttk.Frame(root)
        line.pack(fill="x", pady=(0, 12))

        ttk.Label(line, text="Type de de :").pack(side="left")

        self.combo_de = ttk.Combobox(
            line,
            textvariable=self.nb_faces_var,
            values=[str(x) for x in self.roller.DES_AUTORISES],
            state="readonly",
            width=8,
        )
        self.combo_de.pack(side="left", padx=(10, 18))
        self.combo_de.set("20")

        # Spinbox classique (robuste selon versions tkinter).
        ttk.Label(line, text="Nombre :").pack(side="left")
        self.spin_n = tk.Spinbox(
            line,
            from_=1,
            to=50,
            width=5,
            textvariable=self.n_dice_var,
        )
        self.spin_n.pack(side="left", padx=(10, 0))
        self.combo_de.bind(
            "<<ComboboxSelected>>",
            lambda _e: self._refresh_d20_visibility(),
        )

        options = ttk.LabelFrame(root, text="Options", padding=12)
        options.pack(fill="x", pady=(0, 12))

        self.d20_options = ttk.LabelFrame(
            options,
            text="D20 uniquement",
            padding=10,
        )
        self.d20_options.pack(fill="x", pady=(0, 10))

        ttk.Radiobutton(
            self.d20_options,
            text="Normal (1d20) - autorise aussi Nd20",
            value="normal",
            variable=self.mode_d20_var,
            command=self._refresh_d20_visibility,
        ).pack(anchor="w")

        ttk.Radiobutton(
            self.d20_options,
            text="Avantage (2d20, garder le meilleur)",
            value="avantage",
            variable=self.mode_d20_var,
            command=self._refresh_d20_visibility,
        ).pack(anchor="w")

        ttk.Radiobutton(
            self.d20_options,
            text="Desavantage (2d20, garder le moins bon)",
            value="desavantage",
            variable=self.mode_d20_var,
            command=self._refresh_d20_visibility,
        ).pack(anchor="w")

        ttk.Checkbutton(
            options,
            text="Inspiration bardique (+1d4)",
            variable=self.inspiration_var,
        ).pack(anchor="w")

        ttk.Button(root, text="Lancer", command=self.on_roll_click).pack(
            anchor="w",
            pady=(0, 12),
        )
        ttk.Label(
            root,
            textvariable=self.result_var,
            font=("Segoe UI", 11),
        ).pack(
            anchor="w"
        )

    def _refresh_d20_visibility(self):
        """
        Affiche/masque les options d20 selon le de selectionne.

        Regle UI:
        - avantage/desavantage impose n=1,
        - sinon le champ nombre reste editable.
        """
        is_d20 = self.nb_faces_var.get() == "20"

        if is_d20:
            self.d20_options.pack(fill="x", pady=(0, 10))
        else:
            self.mode_d20_var.set("normal")
            self.d20_options.forget()

        if is_d20 and self.mode_d20_var.get() in ("avantage", "desavantage"):
            self.n_dice_var.set(1)
            self.spin_n.config(state="disabled")
        else:
            self.spin_n.config(state="normal")

    def on_roll_click(self):
        """Point d'entree du bouton Lancer."""
        # 1) Lecture/validation des entrees utilisateur.
        try:
            nb_faces = int(self.nb_faces_var.get())
        except ValueError:
            self.result_var.set("Resultat : type de de invalide")
            return

        try:
            n = int(self.n_dice_var.get())
        except (tk.TclError, ValueError):
            self.result_var.set("Resultat : nombre de des invalide")
            return

        # 2) Delegation au core + gestion d'erreurs utilisateur.
        try:
            self.result_var.set(self._compute_roll_message(nb_faces, n))
        except ValueError as exc:
            self.result_var.set(f"Resultat : {exc}")
        except Exception:
            self.result_var.set("Resultat : erreur au lancer")

    def _compute_roll_message(self, nb_faces: int, n: int) -> str:
        """Transforme le resultat structure du core en message UI."""
        details = self.roller.resolve_roll(
            nb_faces=nb_faces,
            n=n,
            mode=self.mode_d20_var.get(),
            inspiration=self.inspiration_var.get(),
        )

        # Corps principal du message.
        if details["is_d20_special"]:
            msg = (
                f"d20 {details['mode']} -> {details['rolls']} "
                f"(retenu {details['selected']})"
            )
        elif details["count"] == 1:
            msg = f"d{details['die_faces']} -> {details['rolls'][0]}"
        else:
            msg = (
                f"{details['count']}d{details['die_faces']} -> "
                f"{details['rolls']} (total {details['base_value']})"
            )

        # Prefixe critique si applicable.
        if details["critical"] == "success":
            msg = "Reussite critique ! " + msg
        elif details["critical"] == "failure":
            msg = "Echec critique ! " + msg

        # Suffixe bonus si inspiration active.
        if details["bonus"] > 0:
            msg += (
                f" | Inspiration +{details['bonus']} -> "
                f"Total {details['final_value']}"
            )

        return msg


if __name__ == "__main__":
    app = DiceRollerApp()
    app.mainloop()
