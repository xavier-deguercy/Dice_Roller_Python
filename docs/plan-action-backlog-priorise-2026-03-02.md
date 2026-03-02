# PLAN D’ACTION — TICKETS BACKLOG PRIORISÉS

Date du plan : 2026-03-02

Source : [rapport-audit-statique-2026-03-02.md](/C:/Users/xavie/Dropbox/projet_perso_xavier/Programme_dnd/dice-roller-python/docs/rapport-audit-statique-2026-03-02.md)

---

## 1. Objectif

Transformer les constats de l’audit statique en un plan d’action directement exploitable dans le backlog produit.

Ce document ne remplace pas le backlog principal.
Il propose un **ordre d’exécution priorisé**, des **tickets actionnables** et une **séquence de stabilisation**.

---

## 2. Principes de priorisation

- `P0` : correction immédiate, bloque la fiabilité du socle
- `P1` : consolidation technique nécessaire à court terme
- `P2` : amélioration structurante ou qualité de fonctionnement
- `P3` : confort, maturité, amélioration non bloquante

Règle de lecture :

- les tickets `P0` doivent être traités avant toute extension fonctionnelle supplémentaire ;
- les tickets `P1` stabilisent le produit avant les prochaines évolutions de périmètre ;
- les tickets `P2/P3` s’intègrent ensuite dans les itérations de qualité et d’industrialisation.

---

## 3. Séquence recommandée

1. Sécuriser le contrat métier central
2. Réaligner le backlog avec l’état réel du code
3. Encadrer les volumes et durcir les validations
4. Réduire les duplications UI/core
5. Améliorer l’observabilité et la qualité de maintenance
6. Compléter l’industrialisation

---

## 4. Tickets backlog priorisés

## 4.1 Bloc P0 — Stabilisation immédiate

### TICKET-P0-001 — Valider systématiquement les dés supportés dans le core

- Priorité : `P0`
- Type : `Core`
- Référence audit :
  - trou de validation sur `die_faces`
- Constat :
  - le contrat documentaire restreint les dés à `d4`, `d6`, `d8`, `d10`, `d12`, `d20`, `d100`
  - ce contrôle n’est pas visiblement centralisé sur tout le chemin `resolve_roll()`
- Risque :
  - états métier invalides
  - résultats non conformes au CDC
  - perte de confiance dans le point d’entrée métier
- Action attendue :
  - introduire une validation centrale de `die_faces` dans `resolve_roll()`
  - garantir que `roll_many()` ne contourne pas cette validation
  - rendre le comportement homogène sur tous les chemins publics
- Définition de done :
  - un dé non supporté est rejeté de façon cohérente depuis l’API métier
  - aucune branche métier visible n’accepte un nombre de faces hors liste autorisée
  - un test dédié couvre ce cas
- Effort estimé : `S`
- Dépendances : aucune

### TICKET-P0-002 — Réaligner le backlog sur l’état réel du code

- Priorité : `P0`
- Type : `Documentation / Produit`
- Référence audit :
  - décalage entre backlog et implémentation visible
- Constat :
  - plusieurs US marquées `A FAIRE` sont déjà partiellement ou substantiellement matérialisées dans le code
- Risque :
  - mauvaise priorisation
  - décisions de sprint fondées sur une vision fausse du périmètre
  - traçabilité affaiblie
- Action attendue :
  - revoir les statuts de `US-TECH-003`, `US-015`, `US-016`, `US-017`
  - distinguer ce qui est “implémenté”, “stabilisé”, “documenté”, “à finaliser”
  - mettre à jour les DoD si nécessaire
- Définition de done :
  - le backlog reflète le dépôt tel qu’il existe
  - aucun item majeur déjà présent en code n’est laissé en `A FAIRE` sans justification
- Effort estimé : `S`
- Dépendances : aucune

### TICKET-P0-003 — Ajouter un garde-fou central sur la volumétrie des lancers

- Priorité : `P0`
- Type : `Core + CLI`
- Référence audit :
  - absence de borne centrale sur `count`
- Constat :
  - l’UI borne le nombre de dés, mais le core et la CLI n’exposent pas de limite visible équivalente
- Risque :
  - appels excessifs
  - consommation mémoire/temps non encadrée
  - comportement incohérent selon le point d’entrée
- Action attendue :
  - définir une borne métier ou technique explicite sur `count`
  - appliquer cette borne dans le core
  - documenter la règle si elle est retenue
- Définition de done :
  - la limite est unique, documentée et appliquée côté core
  - un appel hors borne produit une erreur claire
- Effort estimé : `S`
- Dépendances :
  - arbitrage produit sur la limite acceptable

---

## 4.2 Bloc P1 — Consolidation du socle

### TICKET-P1-001 — Centraliser les constantes métier partagées UI/core

- Priorité : `P1`
- Type : `Tech`
- Référence audit :
  - duplication des types de jet et des dés de barde
- Constat :
  - certaines règles de disponibilité sont répétées entre le core et la GUI
- Risque :
  - dérive de comportement à la prochaine évolution
  - maintenance plus coûteuse
- Action attendue :
  - déplacer les constantes métier partagées dans un point central
  - faire consommer ces constantes par la GUI et le CLI
- Définition de done :
  - une seule source de vérité pour les listes métier exposées à l’interface
  - suppression des duplications visibles
- Effort estimé : `M`
- Dépendances :
  - `TICKET-P0-001`

### TICKET-P1-002 — Réduire le masquage des erreurs techniques dans la GUI

- Priorité : `P1`
- Type : `UI / Qualité`
- Référence audit :
  - `except Exception` générique dans Tkinter
- Constat :
  - l’interface convertit toute exception inattendue en message générique
- Risque :
  - bugs silencieux
  - diagnostic difficile
  - faible observabilité
- Action attendue :
  - distinguer les erreurs utilisateur des erreurs techniques
  - conserver un message utilisateur simple
  - introduire une trace minimale côté technique
- Définition de done :
  - les `ValueError` métier restent gérées proprement
  - les erreurs inattendues ne sont plus totalement opaques
- Effort estimé : `S`
- Dépendances : aucune

### TICKET-P1-003 — Finaliser la cohérence architecturale autour du pattern Strategy

- Priorité : `P1`
- Type : `Core / Architecture`
- Référence audit :
  - lancers multiples encore hors stratégie dédiée
- Constat :
  - le backlog technique cible une formalisation Strategy plus homogène que celle visible actuellement
- Risque :
  - architecture partiellement inachevée
  - confusion entre objectif documentaire et état réel
- Action attendue :
  - décider si `multi` doit devenir une vraie stratégie dédiée
  - soit compléter le pattern
  - soit ajuster le backlog pour refléter le design final retenu
- Définition de done :
  - alignement explicite entre code, backlog et choix architectural
- Effort estimé : `M`
- Dépendances :
  - `TICKET-P0-002`

### TICKET-P1-004 — Ajouter des tests unitaires ciblés sur le contrat métier

- Priorité : `P1`
- Type : `Tests`
- Référence audit :
  - besoin de figer les validations centrales
- Constat :
  - la base de tests existe, mais certains invariants clés méritent des tests dédiés
- Risque :
  - régression silencieuse sur les validations et le contrat d’entrée
- Action attendue :
  - ajouter des tests pour :
    - dé non supporté via `resolve_roll`
    - limite `count`
    - cohérence des messages d’erreur métier
- Définition de done :
  - les invariants critiques du core sont couverts explicitement
- Effort estimé : `S`
- Dépendances :
  - `TICKET-P0-001`
  - `TICKET-P0-003`

---

## 4.3 Bloc P2 — Qualité structurelle et maintenabilité

### TICKET-P2-001 — Sortir la logique d’activation UI dans une couche de présentation dédiée

- Priorité : `P2`
- Type : `UI / Architecture`
- Référence audit :
  - `app_tk.py` reste dense et concentre plusieurs responsabilités
- Constat :
  - la classe Tkinter gère la construction, l’état, les règles de disponibilité visuelle et l’orchestration
- Risque :
  - complexité croissante
  - testabilité GUI limitée
- Action attendue :
  - isoler les règles de disponibilité de widgets dans une couche dédiée ou des helpers spécialisés
- Définition de done :
  - la classe principale Tkinter est plus courte et plus focalisée
  - les règles UI sont testables séparément ou au moins isolées
- Effort estimé : `M`
- Dépendances :
  - `TICKET-P1-001`

### TICKET-P2-002 — Introduire une journalisation minimale

- Priorité : `P2`
- Type : `Qualité / Observabilité`
- Référence audit :
  - absence de logging structuré
- Constat :
  - aucune trace technique n’est visible en cas d’erreur inattendue
- Risque :
  - faible diagnostic en cas de défaut
  - difficulté de support, même sur un MVP local
- Action attendue :
  - ajouter un logging minimal sur les erreurs techniques non prévues
  - éviter toute fuite d’information inutile à l’utilisateur final
- Définition de done :
  - les erreurs inattendues importantes laissent une trace exploitable
- Effort estimé : `S`
- Dépendances :
  - `TICKET-P1-002`

### TICKET-P2-003 — Nettoyer les points d’entrée et le code de démonstration interne

- Priorité : `P2`
- Type : `Tech`
- Référence audit :
  - présence d’une fonction `main()` de démonstration dans le module core
- Constat :
  - le module métier contient encore un point d’entrée de démonstration non essentiel
- Risque :
  - confusion sur le vrai point d’entrée
  - bruit structurel
- Action attendue :
  - retirer, déplacer ou clairement isoler ce code de démonstration
- Définition de done :
  - les points d’entrée applicatifs sont explicites et sans ambiguïté
- Effort estimé : `S`
- Dépendances : aucune

---

## 4.4 Bloc P3 — Industrialisation et convergence outillage

### TICKET-P3-001 — Aligner les dépendances de développement avec la CI

- Priorité : `P3`
- Type : `Outillage`
- Référence audit :
  - `ruff` est utilisé en CI mais pas déclaré dans les dépendances du projet
- Constat :
  - l’environnement CI est plus complet que l’environnement local décrit par `requirements.txt`
- Risque :
  - reproductibilité locale partielle
  - friction d’onboarding
- Action attendue :
  - déclarer clairement les dépendances de dev
  - choisir une convention explicite (`requirements-dev`, extra, ou autre)
- Définition de done :
  - un environnement local standard permet d’exécuter les mêmes contrôles que la CI
- Effort estimé : `S`
- Dépendances : aucune

### TICKET-P3-002 — Ajouter une métrique de couverture minimale en CI

- Priorité : `P3`
- Type : `CI / Qualité`
- Référence audit :
  - absence de couverture visible
- Constat :
  - la CI vérifie les tests, mais ne mesure pas leur portée
- Risque :
  - impression de sécurité sans indicateur de profondeur
- Action attendue :
  - produire une mesure de couverture
  - fixer un seuil réaliste sur le core
- Définition de done :
  - la CI expose une couverture minimale exploitable
- Effort estimé : `S`
- Dépendances :
  - `TICKET-P1-004`

### TICKET-P3-003 — Envisager un type-checking minimal sur le core

- Priorité : `P3`
- Type : `Qualité / Typage`
- Référence audit :
  - le projet bénéficie déjà d’un modèle dataclass structuré
- Constat :
  - le design se prête bien à un contrôle de types plus strict
- Risque :
  - erreurs de contrat plus difficiles à détecter tôt
- Action attendue :
  - introduire un type-checking progressif sur `src/core`
- Définition de done :
  - un contrôle statique de type minimal s’exécute au moins sur le cœur métier
- Effort estimé : `M`
- Dépendances :
  - `TICKET-P1-001`

---

## 5. Plan de mise en œuvre par itérations

### Itération 1 — Verrouillage du socle

- `TICKET-P0-001`
- `TICKET-P0-002`
- `TICKET-P0-003`

Résultat attendu :

- contrat métier cohérent
- backlog réaligné
- volumétrie encadrée

### Itération 2 — Consolidation technique

- `TICKET-P1-001`
- `TICKET-P1-002`
- `TICKET-P1-003`
- `TICKET-P1-004`

Résultat attendu :

- duplication réduite
- erreurs mieux traitées
- architecture alignée avec le backlog
- tests plus ciblés

### Itération 3 — Maintenabilité et industrialisation

- `TICKET-P2-001`
- `TICKET-P2-002`
- `TICKET-P2-003`
- `TICKET-P3-001`
- `TICKET-P3-002`
- `TICKET-P3-003`

Résultat attendu :

- base plus maintenable
- observabilité minimale
- outillage convergent

---

## 6. Recommandation de gouvernance backlog

Pour éviter de reproduire l’écart observé entre audit, code et backlog :

- chaque ticket technique doit préciser s’il vise :
  - implémentation
  - stabilisation
  - alignement documentaire
  - durcissement qualité
- le statut d’une US doit distinguer :
  - “partiellement codé”
  - “fonctionnel”
  - “stabilisé”
  - “documenté”
- tout changement de portée technique doit mettre à jour :
  - le backlog
  - le CDC si la règle métier change
  - la DoD si l’exigence de qualité change

---

## 7. Prochaine action recommandée

La prochaine action la plus rentable est :

1. Exécuter `TICKET-P0-001`  
2. Puis mettre à jour immédiatement `TICKET-P0-002` dans le backlog produit  
3. Ensuite seulement, engager `TICKET-P0-003`

Cet ordre traite d’abord la **fiabilité du contrat métier**, puis la **fiabilité du pilotage**, avant d’étendre à nouveau le produit.
