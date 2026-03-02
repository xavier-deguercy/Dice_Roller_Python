"""
Interface Tkinter de Dice Roller.

Cette couche:
- lit les choix utilisateur,
- appelle le core (`DiceRoller.resolve_roll`),
- transforme le resultat en texte lisible.
"""

import tkinter as tk
from tkinter import ttk

from src.core.dice_roller import DiceRoller, RollRequest, RuleOptionRequest
from src.core.formatting import format_roll_result


class DiceRollerApp(tk.Tk):
    """
    Fenetre principale Tkinter.

    Important:
    - pas de regles de lancer ici,
    - le core decide des resultats, l'UI ne fait que presenter.
    """

    ROLL_KIND_LABELS = {
        "Jet generique": "generic_roll",
        "Ability check": "ability_check",
        "Jet d'attaque": "attack_roll",
        "Jet de sauvegarde": "saving_throw",
    }
    BARDIC_DIE_CHOICES = ("Aucun", "d6", "d8", "d10", "d12")

    def __init__(self):
        super().__init__()

        self.title("Dice Roller")
        self.geometry("560x700")
        self.resizable(False, False)

        self.roller = DiceRoller()

        # Etat UI: ces variables sont liees aux widgets Tkinter.
        self.nb_faces_var = tk.StringVar(value="20")
        self.n_dice_var = tk.IntVar(value=1)
        self.mode_d20_var = tk.StringVar(value="normal")
        self.roll_kind_label_var = tk.StringVar(value="Jet generique")
        self.guidance_var = tk.BooleanVar(value=False)
        self.bardic_die_var = tk.StringVar(value="Aucun")
        self.heroic_inspiration_var = tk.BooleanVar(value=False)
        self.result_var = tk.StringVar(value="Resultat : -")

        self.spin_n = None
        self.roll_kind_combo = None
        self.d20_options = None
        self.guidance_checkbutton = None
        self.bardic_combo = None
        self.heroic_checkbutton = None

        self._build_ui()
        self.n_dice_var.trace_add("write", self._on_dice_count_change)
        self._refresh_d20_visibility()
        self._refresh_rule_options_state()

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
            text="Choisis un de, un nombre, puis construis le jet a lancer.",
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

        context = ttk.LabelFrame(root, text="Contexte de jet", padding=12)
        context.pack(fill="x", pady=(0, 12))

        ttk.Label(context, text="Type de jet :").pack(anchor="w")
        self.roll_kind_combo = ttk.Combobox(
            context,
            textvariable=self.roll_kind_label_var,
            values=list(self.ROLL_KIND_LABELS.keys()),
            state="readonly",
            width=24,
        )
        self.roll_kind_combo.pack(anchor="w", pady=(6, 0))
        self.roll_kind_combo.bind(
            "<<ComboboxSelected>>",
            lambda _event: self._refresh_rule_options_state(),
        )

        options = ttk.LabelFrame(root, text="Modes de jet", padding=12)
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

        rules = ttk.LabelFrame(root, text="Options officielles", padding=12)
        rules.pack(fill="x", pady=(0, 12))

        ttk.Label(
            rules,
            text="Le core valide la compatibilite de ces options avec le type de jet.",
        ).pack(anchor="w", pady=(0, 8))

        self.guidance_checkbutton = ttk.Checkbutton(
            rules,
            text="Guidance (+1d4 sur ability check)",
            variable=self.guidance_var,
        )
        self.guidance_checkbutton.pack(anchor="w")

        bardic_line = ttk.Frame(rules)
        bardic_line.pack(fill="x", pady=(8, 0))
        ttk.Label(bardic_line, text="Bardic Inspiration :").pack(side="left")
        self.bardic_combo = ttk.Combobox(
            bardic_line,
            textvariable=self.bardic_die_var,
            values=self.BARDIC_DIE_CHOICES,
            state="readonly",
            width=8,
        )
        self.bardic_combo.pack(side="left", padx=(10, 0))

        self.heroic_checkbutton = ttk.Checkbutton(
            rules,
            text="Heroic Inspiration (relance)",
            variable=self.heroic_inspiration_var,
        )
        self.heroic_checkbutton.pack(anchor="w", pady=(8, 0))

        ttk.Button(root, text="Lancer", command=self.on_roll_click).pack(
            anchor="w",
            pady=(0, 12),
        )
        ttk.Label(
            root,
            textvariable=self.result_var,
            font=("Segoe UI", 11),
            wraplength=520,
            justify="left",
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

        self._refresh_rule_options_state()

    def _on_dice_count_change(self, *_args):
        """Rafraichit les options de regle quand le nombre de des change."""
        self._refresh_rule_options_state()

    def _refresh_rule_options_state(self):
        """
        Ajuste visuellement les options officielles selon le contexte courant.

        Le core garde la validation metier definitive. L'UI se limite a
        reduire les saisies incoherentes les plus evidentes.
        """
        if (
            self.guidance_checkbutton is None
            or self.bardic_combo is None
            or self.heroic_checkbutton is None
        ):
            return

        roll_kind = self.ROLL_KIND_LABELS.get(
            self.roll_kind_label_var.get(),
            "generic_roll",
        )

        guidance_allowed = roll_kind == "ability_check"
        self.guidance_checkbutton.config(
            state="normal" if guidance_allowed else "disabled"
        )
        if not guidance_allowed:
            self.guidance_var.set(False)

        bardic_allowed = roll_kind in ("ability_check", "attack_roll", "saving_throw")
        self.bardic_combo.config(state="readonly" if bardic_allowed else "disabled")
        if not bardic_allowed:
            self.bardic_die_var.set("Aucun")

        try:
            heroic_allowed = self.mode_d20_var.get() == "normal" and int(
                self.n_dice_var.get()
            ) == 1
        except (tk.TclError, ValueError):
            heroic_allowed = False

        self.heroic_checkbutton.config(
            state="normal" if heroic_allowed else "disabled"
        )
        if not heroic_allowed:
            self.heroic_inspiration_var.set(False)

    def _selected_roll_kind(self) -> str:
        """Traduit le libelle UI en valeur metier."""
        label = self.roll_kind_label_var.get()
        try:
            return self.ROLL_KIND_LABELS[label]
        except KeyError as exc:
            raise ValueError("type de jet invalide") from exc

    def _build_official_options(self) -> tuple[RuleOptionRequest, ...]:
        """Construit les options officielles choisies dans l'UI."""
        options: list[RuleOptionRequest] = []

        if self.guidance_var.get():
            options.append(RuleOptionRequest(name="guidance"))

        if self.bardic_die_var.get() != "Aucun":
            die_faces = int(self.bardic_die_var.get()[1:])
            options.append(
                RuleOptionRequest(name="bardic_inspiration", die_faces=die_faces)
            )

        if self.heroic_inspiration_var.get():
            options.append(RuleOptionRequest(name="heroic_inspiration"))

        return tuple(options)

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
        request = RollRequest(
            die_faces=nb_faces,
            count=n,
            roll_mode=self.mode_d20_var.get(),
            roll_kind=self._selected_roll_kind(),
            official_options=self._build_official_options(),
        )
        result = self.roller.resolve_roll(request)
        return format_roll_result(result)


if __name__ == "__main__":
    app = DiceRollerApp()
    app.mainloop()
