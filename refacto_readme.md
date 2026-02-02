# Refacto — Pattern Strategy (Dice Roller)

Ce document explique comment le pattern **Strategy** est appliqué dans le projet
pour gérer les différents modes de lancer (normal / avantage / désavantage).

---

## 1) Pourquoi utiliser Strategy ici ?

Problème classique :
- Plusieurs variantes d’un même comportement (lancer un dé).
- Besoin d’ajouter de nouveaux modes sans casser le reste.

Solution :
Le pattern **Strategy** permet de **séparer les variantes** du lancer dans des
classes dédiées et d’**échanger la stratégie** au moment de l’appel.

---

## 2) Les rôles du pattern dans ce projet

### ✅ Interface (abstraction)
**`RollStrategy`**

Elle définit *ce qu’est* une stratégie de lancer :
- une méthode `roll()` qui renvoie un dict standardisé.

### ✅ Stratégies concrètes
**`NormalRollStrategy`**, **`AdvantageRollStrategy`**, **`DisadvantageRollStrategy`**

Chaque classe encapsule un comportement différent :
- normal → 1 dé
- avantage → 2 dés, garder le meilleur
- désavantage → 2 dés, garder le moins bon

### ✅ Contexte
**`DiceRoller`**

Le contexte :
1. possède un dictionnaire de stratégies
2. choisit laquelle exécuter via `roll(nb_faces, strategy)`
3. ne connaît pas les détails internes de la stratégie

---

## 3) Schéma de circulation (simplifié)

```
DiceRoller.roll(nb_faces, "avantage")
        ↓
_strategies["avantage"]  ->  AdvantageRollStrategy
        ↓
AdvantageRollStrategy.roll(...)
        ↓
{"strategy": "avantage", "rolls": [...], "final_value": ...}
```

---

## 4) Exemple d’utilisation

```python
roller = DiceRoller()

result = roller.roll(20, "avantage")
print(result)
# Exemple :
# {'strategy': 'avantage', 'rolls': [12, 18], 'final_value': 18, 'die_faces': 20}
```

---

## 5) Pourquoi c’est mieux qu’un gros if/elif ?

✅ **Lisibilité** : chaque mode est isolé  
✅ **Extensibilité** : tu ajoutes une stratégie sans modifier la logique centrale  
✅ **Testabilité** : chaque stratégie se teste en isolation  
✅ **Responsabilités claires** : `DiceRoller` orchestre, les stratégies exécutent  

---

## 6) Lien avec l’IHM Tkinter

L’IHM ne contient pas la logique du lancer :
- elle choisit le mode (`normal`, `avantage`, `desavantage`)
- elle appelle `roll_d20()` ou `roll()` du core

Ainsi, **l’UI reste un simple client** du core.

---

## 7) Ajouter une nouvelle stratégie (ex. "critique")

1. Créer une nouvelle classe qui implémente `RollStrategy`
2. L’ajouter dans `self._strategies`

```python
class CriticalRollStrategy(RollStrategy):
    def roll(self, roller, nb_faces):
        value = roller.roll_die(nb_faces)
        return {
            "strategy": "critique",
            "rolls": [value],
            "final_value": value * 2,
            "die_faces": nb_faces,
        }

# Dans DiceRoller.__init__ :
self._strategies["critique"] = CriticalRollStrategy()
```

---

## 8) Points à retenir

- Strategy = **une interface + plusieurs implémentations**
- Le contexte (`DiceRoller`) **délègue** l’action
- Facile à étendre et à maintenir

---

Si tu veux, je peux te proposer un exercice pour implémenter une nouvelle
stratégie, ou un mini-test unitaire avec pytest.
