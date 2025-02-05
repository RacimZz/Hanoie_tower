# Tours de Hanoï - Simulation et Jeu Interactif

Ce projet propose une simulation interactive du jeu des **Tours de Hanoï**, combinant un **mode didacticiel** pour explorer les mouvements optimaux et un **mode de jeu interactif** avec des commandes personnalisées. L'interface graphique est développée avec **Turtle** et **Tkinter**, offrant une expérience visuelle immersive et une gestion avancée des parties.

## Fonctionnalités

### 🎨 Mode Didacticiel : Découverte des Mouvements Optimaux
- Animation fluide des déplacements des disques avec des couleurs dégradées.
- Visualisation progressive des solutions optimales via l'algorithme récursif de Hanoï.
- Représentation graphique avec **Turtle** :
  - Classe `Disc` pour les disques.
  - Classe `Tower` pour les tours.
  - Fonction récursive `hanoi()` pour animer la résolution.
- Lancement de l'animation par un simple appui sur la **barre d'espace**.

### 🎮 Mode de Jeu : Jouer avec des Commandes Personnalisées
- Saisie interactive des tours de départ et d'arrivée (valeurs possibles : `0, 1, 2`).
- Fonctionnalités avancées :
  - **Abandon de la partie**.
  - **Annulation du dernier coup**.
  - **Retour au menu précédent**.
- Interface intuitive avec **compteur de coups** et **boutons interactifs**.

### 📄 Menu Interactif à la Fin de la Partie
- Affichage des statistiques :
  - **Nom du joueur**.
  - **Nombre de coups**.
  - **Temps de jeu**.
- Option pour **jouer avec un autre joueur**.
- Accès à un **menu interactif** avec :
  - **Classements des joueurs**.
  - **Statistiques détaillées**.
  - **Option de sortie définitive**.

### 💾 Sauvegarde des Données avec Pickle
- **Scores et configurations des parties** sauvegardés automatiquement.
- Reprise de la progression entre différentes sessions de jeu.

## Interface et Fonctionnalités Spécifiques

### 🗂 Accueil du Programme
- Trois boutons principaux :
  1. **Mode Didacticiel**.
  2. **Mode Jeu**.
  3. **Notice du jeu** (via **Tkinter**).

### 🎨 Spécificités de l'Interface Graphique
- **Lecture du nombre de disques** via `turtle.textinput()`.
- **Boutons interactifs** définis par une classe personnalisée :
  - Texte dynamique.
  - Position ajustée via `ajuster_positions_boutons(n)`.
  - Taille et couleur modifiables.
- **Plateau adaptatif** :
  - Changement de taille et position des tours en fonction de `n`.
- **Représentation des disques** :
  - Chaque disque est une instance de `Disc`.
  - Couleurs dégradées du bleu au rouge (`interpolate_color`).

### 🔍 Interaction et Gestion des Entrées Utilisateur
- **Saisie contrôlée** pour les tours de départ et d'arrivée (`lireCoords`) :
  - Validation stricte (`0, 1, 2`).
  - Messages d'erreur affichés en rouge.
  - Tour de départ mise en évidence en **vert**, tour d’arrivée en **bleu**.
- **Affichage des résultats** (`resultat`) via une fenêtre Tkinter.
- **Gestion complète des parties** :
  - Historique et scores regroupés dans un fichier via **Pickle**.
  - Accès aux options interactives à la fin du jeu.

### 📝 Algorithmes et Fonctions Clés
- **`resoudreHanoi(n)`** : Génération des mouvements optimaux pour `n` disques.
- **`afficherMouvements()`** : Animation des déplacements optimaux.
- **`lecture_nombre_disque()`** : Initialisation du jeu.
- **`boucleJeu()`** : Gestion de la partie.
- **`resultat()`** : Affichage des résultats et relance éventuelle.
- **Menu interactif** : Propose le classement, les statistiques et les sauvegardes.

## 📚 Installation et Exécution

### Prérequis
- **Python 3.x**
- Bibliothèques nécessaires (installables avec pip) :
  ```sh
  pip install tkinter
  ```

### Exécution du Programme
```sh
python main.py
```

## 📚 Auteur
Projet développé dans le cadre d'un projet par binome (& Arris Zaidi) sur les **Tours de Hanoï** en Python.



