import turtle
import random
import time
import os
from turtle import *
import tkinter as tk
import pickle


def lecture_nombre_disque():
    while True:
        try:
            n = int(turtle.textinput("Jeu de Hanoi", "Entrez le nombre de disque "))
            if n > 0:
                break
            else:
                print('Veuillez entrez un nombre plus grand que 0')
        except ValueError:
            print('Veuillez entrez un nombre valide')
    return n

class Chronometre:
    def __init__(self):
        self.start_time_chrono = time.time()
        self.running = True

    def afficher_temps(self):
        while self.running:
            elapsed_time = time.time() - self.start_time_chrono
            minutes, seconds = divmod(elapsed_time, 60)
            formatted_time = f"{int(minutes):02d}:{int(seconds):02d}"
            turtle.undo()
            turtle.penup()
            turtle.hideturtle()
            turtle.goto(0, 250)  # Positionnez le chronomètre en haut de l'écran
            turtle.write(f"Temps : {formatted_time}", align="center", font=("Times New Roman", 15, "bold"))
            time.sleep(1)

class Button:
    def __init__(self, text, pos, size, color, text_color="white"):
        self.text = text
        self.pos = pos
        self.size = size
        self.color = color
        self.text_color = text_color
        self.btn_turtle = turtle.Turtle()
        self.create_button()

    def draw_rounded_rect(self, x, y, width, height, corner_radius):
        """ Dessine un rectangle avec des coins arrondis """
        self.btn_turtle.penup()
        self.btn_turtle.goto(x + corner_radius, y)
        self.btn_turtle.pendown()
        self.btn_turtle.forward(width - 2 * corner_radius)
        self.btn_turtle.circle(corner_radius, 90)
        self.btn_turtle.forward(height - 2 * corner_radius)
        self.btn_turtle.circle(corner_radius, 90)
        self.btn_turtle.forward(width - 2 * corner_radius)
        self.btn_turtle.circle(corner_radius, 90)
        self.btn_turtle.forward(height - 2 * corner_radius)
        self.btn_turtle.circle(corner_radius, 90)

    def create_button(self):
        # Paramètres esthétiques du bouton
        corner_radius = 10  # Rayon des coins arrondis
        shadow_offset = 3  # Décalage pour l'ombre

        # Créer et dessiner l'ombre du bouton en noir
        self.btn_turtle.hideturtle()
        self.btn_turtle.speed(0)
        self.btn_turtle.color("black")  # Couleur de l'ombre modifiée en noir
        self.draw_rounded_rect(self.pos[0] + shadow_offset, self.pos[1] - shadow_offset,
                               self.size[0], self.size[1], corner_radius)

        # Créer et dessiner le bouton
        self.btn_turtle.color(self.color)
        self.btn_turtle.begin_fill()
        self.draw_rounded_rect(self.pos[0], self.pos[1], self.size[0], self.size[1], corner_radius)
        self.btn_turtle.end_fill()

        # Afficher le texte du bouton
        self.btn_turtle.penup()
        self.btn_turtle.goto(self.pos[0] + self.size[0]/2, self.pos[1] + self.size[1]/2 - 15)
        self.btn_turtle.color(self.text_color)
        self.btn_turtle.write(self.text, align="center", font=("Arial", 12, "bold"))

def ajusterVue(n):
    """ajuster la vue de l'interface en fonction du nombre de disque"""
    # Ajuster la largeur et la hauteur en fonction de n
    if n>11 :
        largeur_vue = 120* n  # La largeur est plus grande pour gérer un plus grand nombre de disques
        hauteur_vue = 55 * n   # Hauteur suffisante pour les tours et les disques empilés
    elif n==2:
        largeur_vue = 300* n  # La largeur est plus grande pour gérer un plus grand nombre de disques
        hauteur_vue = 399 * n   # Hauteur suffisante pour les tours et les disques empilés
    else :
        largeur_vue = 150* n  # La largeur est plus grande pour gérer un plus grand nombre de disques
        hauteur_vue = 180 * n   # Hauteur suffisante pour les tours et les disques empilés

    # Coordonnées pour centrer le jeu
    x_min = -largeur_vue / 2
    y_min = -hauteur_vue / 2
    x_max = largeur_vue / 2
    y_max = hauteur_vue / 2

    # Mise à jour des worldcoordinates pour centrer le jeu
    turtle.setworldcoordinates(x_min, y_min, x_max, y_max)


class Disque(turtle.Turtle):
    def __init__(self, n, nmax):
        """ Initialise un disque. """
        super().__init__(shape="square", visible=False)
        self.speed(5)
        self.penup()
        self.shapesize(1.5, n * 1.5, 2)  # Modifie la forme pour ressembler à un disque
        self.fillcolor(n / nmax, 0.5, 1 - n / nmax)  # Couleur dégradée pour chaque disque
        self.original_color = self.fillcolor()  # Sauvegarde de la couleur originale
        self.showturtle()

    def sauvegarder_couleur(self):
        """ Sauvegarde la couleur actuelle du disque """
        self.original_color = self.fillcolor()

    def restaurer_couleur(self):
        """ Restaure la couleur originale du disque """
        self.fillcolor(self.original_color)

#declaration de nos variables globales
coups = {}
scores= {}
nb_defaite={}
abandon=False
coup = 0
toutscores= False

def on_jouer_click(x, y):
    """code a executer quand le boutton jouer a été cliqué"""
    print("Vous etes sur le mode \"jeu\" ")
    global coups,scores,nb_defaite,abandon,coup


    #A-----------------------------------------------------------------------------------------

    def init(n) :
        L=[]
        for i in range(n,0,-1) :
            L.append(i)
        return [L,[],[]]

    def nbDisques(plateau,numtour):
        return len(plateau[numtour])

    def TourVIDE(plateau,numtour) :
        if len(plateau[numtour]) == 0 :
            return True
        else :
            return False

    def disqueSup(plateau, numtour):
        if TourVIDE(plateau,numtour) :
            return -1
        return plateau[numtour][len(plateau[numtour])-1]

    def posDisque(plateau, numdisque) :
        for i in range(0,len(plateau)) :
            for j in plateau[i] :
                if j==numdisque :
                    return i

    def verifDepl(plateau, nt1, nt2):
        if disqueSup(plateau,nt2) > disqueSup(plateau,nt1) or TourVIDE(plateau,nt2) :
            return True
        return False

    def verifVictoire(plateau, n) :
        p=list(plateau[2])
        dec =True
        i=0
        while i<len(p)-1 and dec :
            if p[i] < p[i+1] :
                dec = False
            i+=1
        if TourVIDE(plateau,0) and TourVIDE(plateau,1) and dec and len(p)==n:
            return True
        else :
            return False

    #B----------------------------------------------------------------------------------------




    def couleur_turtle_aleatoire():
        couleurs = ["black", "red", "green", "blue", "yellow", "orange", "purple", "pink"]
        couleur_aleatoire = random.choice(couleurs)
        return couleur_aleatoire

    def dessinePlateau(n, couleur_plateau="black", couleur_tours="black"):
        largeur_plateau =100*n
        hauteur_plateau = 50
        largeur_tour = 6
        hauteur_tour = n * 30  # Hauteur ajustée des tours

        turtle.speed(0)
        turtle.up()
        turtle.goto(-largeur_plateau / 2, -200)
        turtle.down()

        turtle.color(couleur_plateau)
        turtle.begin_fill()
        for _ in range(2):
            turtle.forward(largeur_plateau)
            turtle.left(90)
            turtle.forward(hauteur_plateau)
            turtle.left(90)
        turtle.end_fill()
        espace=0
        turtle.color(couleur_tours)
        for j in range(3):
            tour_x = -largeur_plateau / 3 + 3.2
            turtle.up()
            turtle.goto(tour_x+espace, -150)
            turtle.down()
            turtle.begin_fill()
            for _ in range(2):
                turtle.forward(largeur_tour)
                turtle.left(90)
                turtle.forward(hauteur_tour)
                turtle.left(90)
            turtle.end_fill()
            espace+= largeur_plateau/3


    def interpolate_color(color_start, color_end, position):
        """Interpoler entre deux couleurs."""
        r = color_start[0] + (color_end[0] - color_start[0]) * position
        g = color_start[1] + (color_end[1] - color_start[1]) * position
        b = color_start[2] + (color_end[2] - color_start[2]) * position
        return (r, g, b)



    def dessineDisque(nd, plateau, n):
        largeur_plateau = 100 * n
        largeur_disque_max = 25 * n  # Largeur maximale pour le plus grand disque
        hauteur_disque = 25
        positions_tours = [((-largeur_plateau / 3) + 6, -150), (6, -150), ((largeur_plateau / 3) + 6, -150)]

        for tour_index, tour in enumerate(plateau):
            if nd in tour:
                x, y_base = positions_tours[tour_index]
                y = y_base + hauteur_disque * tour.index(nd)
                break

        largeur_disque = largeur_disque_max - (n - nd) * 20  # Largeur décroissante

        # Utiliser la classe Disc pour dessiner le disque
        disque = Disque(n, n)
        disque.penup()
        disque.goto(x - largeur_disque / 2, y)
        disque.pendown()

        # Remplir le disque avec le dégradé de couleur
        couleur_debut = (0, 0.5, 1)  # Couleur de début (bleu)
        couleur_fin = (1, 0.5, 0)    # Couleur de fin (rouge)

        disque.sauvegarder_couleur()  # Sauvegarder la couleur avant le déplacement

        disque.begin_fill()

        # Appliquer le dégradé en fonction de la position du disque
        position_relative = tour.index(nd) / len(tour)
        couleur_interpol = interpolate_color(couleur_debut, couleur_fin, position_relative)
        disque.fillcolor(couleur_interpol)

        for _ in range(2):
            disque.forward(largeur_disque)
            disque.left(90)
            disque.forward(hauteur_disque)
            disque.left(90)

        disque.end_fill()

        # Restaurer la couleur après le déplacement
        disque.restaurer_couleur()

    def effaceDisque(nd, plateau, n):
        largeur_plateau = 100 * n
        largeur_disque_max = 25 * n
        hauteur_disque = 25
        largeur_tour = 6
        hauteur_tour = n * 30

        positions_axes_tours = [(-largeur_plateau / 3+3.2, -150), (3.2, -150), (largeur_plateau / 3+3.2, -150)]

        for tour_index, tour in enumerate(plateau):
            if nd in tour:
                x, y_base = positions_axes_tours[tour_index]
                y = y_base + hauteur_disque * tour.index(nd)

                # Effacer le disque
                turtle.penup()
                if nd==n : #on ajuste la coordonnée vertical en fonction de nd
                    turtle.goto(x - (largeur_disque_max - (n - nd) * 20) / 2,y+1)
                else :
                    turtle.goto(x - (largeur_disque_max - (n - nd) * 20) / 2,y+1.5)
                #0.6 represente la bordure noire du disque du bas qu'on veut pas effacé
                turtle.pendown()
                turtle.color("white")
                turtle.fillcolor("white")
                turtle.begin_fill()
                for _ in range(2):
                    turtle.forward(largeur_disque_max+5)
                    turtle.left(90)
                    turtle.forward(hauteur_disque)
                    turtle.left(90)
                turtle.end_fill()

                # Redessiner l'axe de la tour
            # Après avoir effacé le disque
    # ...

                # Calculer la hauteur de début pour redessiner l'axe
                nombre_disques_sur_tour_apres_effacement = len(tour)-1
                if nombre_disques_sur_tour_apres_effacement > 0:
                    hauteur_debut_axe = y_base + hauteur_disque * nombre_disques_sur_tour_apres_effacement
                else:
                    hauteur_debut_axe = -150

                # Ajuster la longueur de l'axe redessiné
                longueur_axe_redessine = hauteur_tour - (hauteur_debut_axe + 150)

                # Redessiner l'axe de la tour
                axe_x, _ = positions_axes_tours[tour_index]
                turtle.penup()
                turtle.goto(axe_x, hauteur_debut_axe)
                turtle.pendown()
                turtle.color("black")
                turtle.begin_fill()
                for _ in range(2):
                    turtle.forward(largeur_tour)
                    turtle.left(90)
                    turtle.forward(longueur_axe_redessine)
                    turtle.left(90)
                turtle.end_fill()


    # ...




    def dessineConfig(plateau, n):
        dessinePlateau(n)
        for tour in plateau:
            for disq in tour :
                dessineDisque(disq,plateau,n)


    def effaceTout(plateau, n):
        for tour in plateau:
            for disq in tour:
                effaceDisque(disq,plateau,n)





    #C--------------------------------------------------------------------------------------------


    def lireCoords(plateau):

        while True:
            try:
                tour_depart = int(input("\033[92mTour de depart ? -1 pour abandonner : "))
                print("\033[0m")
                if tour_depart == -1:
                    print("Vous avez choisi d'abandonner la partie.")
                    return None, None
                elif tour_depart in [0, 1, 2]:
                    if TourVIDE(plateau, tour_depart):
                        print("\033[1;31;40mLa tour est vide. Veuillez réessayer.\033[0m")
                    else:
                        while True:
                            try:
                                tour_arrive = int(input("\033[94mTour d'arrivée ? -1 pour changer la tour de départ : "))
                                print("\033[0m")
                                if tour_arrive == -1:
                                    print("Retour au choix de la tour de départ.")
                                    break
                                elif tour_arrive in [0, 1, 2]:
                                    if verifDepl(plateau, tour_depart, tour_arrive):
                                        return tour_depart, tour_arrive
                                    else:
                                        print("\033[1;31;40mDéplacement non autorisé. Veuillez réessayer.\033[0m")
                                else:
                                    print("\033[1;31;40mNuméro de tour d'arrivée invalide (0,1,2). Veuillez réessayer.\033[0m")
                            except ValueError:
                                print("Veuillez entrer un nombre valide pour la tour d'arrivée.")
                else:
                    print("\033[1;31;40mNuméro de tour de départ invalide (0,1,2). Veuillez réessayer.\033[0m")
            except ValueError:
                print("Veuillez entrer un nombre valide pour la tour de départ.")



    def jouerUnCoup(plateau, n):
        # Récupérer les numéros des tours de départ et d'arrivée
        global coups
        tour_depart, tour_arrivee = lireCoords(plateau)
        if tour_arrivee is None and tour_depart is None :
            return None  #pour prevenir a la fonction bouclejeu que l'utilisateur a abandonner

        print(f"Deplacement du disque {plateau[tour_depart][-1]} de la tour {tour_depart} vers la tour {tour_arrivee}")

        # Récupérer le disque à déplacer (sommet de la tour de départ)


        # Effacer le disque de sa position actuelle
        effaceDisque(plateau[tour_depart][-1], plateau, n)

        disque = plateau[tour_depart].pop()

        # Ajouter le disque à la tour d'arrivée
        plateau[tour_arrivee].append(disque)

        # Dessiner le disque à sa nouvelle position
        dessineDisque(disque, plateau, n)

        coups[len(coups)] = [list(tour) for tour in plateau]  # Copie de l'état actuel
        return 0

    def afficherNombreCoups(coup, n):
        # Calculer les coordonnées
        x = (100 * n) / 2 - 40  # Ajuster en fonction de la largeur de votre plateau
        y = (60 * n) / 2 - 20   # Ajuster en fonction de la hauteur souhaitée

        turtle.up()
        turtle.goto(x, y)
        turtle.color("black")
        turtle.write(f"Coups: {coup}", align="right", font=("Arial", 16, "normal"))

    def afficherNombreCoupsenBlanc(coup, n):
        # Calculer les coordonnées
        x = (100 * n) / 2 - 40  # Ajuster en fonction de la largeur de votre plateau
        y = (60 * n) / 2 - 20   # Ajuster en fonction de la hauteur souhaitée

        turtle.up()
        turtle.goto(x, y)
        turtle.color("white")
        turtle.write(f"Coups: {coup}", align="right", font=("Arial", 16, "normal"))


    def dernierCoup(coups):
        # Vérifier si des coups ont été joués
        if not coups:
            return None

        # Trouver le numéro du dernier coup joué
        dernier_numero_coup = max(coups.keys())

        # Récupérer la configuration du plateau avant et après le dernier coup
        plateau_avant = coups[dernier_numero_coup - 1]
        plateau_apres = coups[dernier_numero_coup]

        # Trouver la différence entre les deux plateaux pour déterminer le dernier coup
        tour_depart, tour_arrivee = None, None
        for tour_index in range(3):  # Puisqu'il y a 3 tours
            if len(plateau_avant[tour_index]) < len(plateau_apres[tour_index]):
                # Un disque a été ajouté à cette tour (tour d'arrivée)
                tour_arrivee = tour_index
            elif len(plateau_avant[tour_index]) > len(plateau_apres[tour_index]):
                # Un disque a été retiré de cette tour (tour de départ)
                tour_depart = tour_index

        # S'assurer que les tours de départ et d'arrivée ont été trouvées
        if tour_depart is not None and tour_arrivee is not None:
            return tour_depart, tour_arrivee
        else:
            # Retourner None si le coup n'a pas pu être déterminé
            return None


    def annulerDernierCoup(coups):
        if len(coups) <= 1:
            return None, 0

        dernier_coup = dernierCoup(coups)
        if dernier_coup is None:
            return None, 0

        tour_depart, tour_arrivee = dernier_coup

        # Inverser le dernier coup
        disque_a_deplacer = coups[len(coups) - 1][tour_arrivee].pop()
        coups[len(coups) - 1][tour_depart].append(disque_a_deplacer)

        # Supprimer la dernière configuration du dictionnaire
        del coups[len(coups) - 1]

        # Décrémenter le compteur de coups
        nouveau_compteur_coup = len(coups) - 1

        return coups[nouveau_compteur_coup], nouveau_compteur_coup

# --------------------------------------------SCORES-------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
    def sauvScore(joueur, nb_disques, nb_coups, temps_jeu):
        global scores
        if joueur.lower() not in scores:
            scores[joueur.lower()] = []

        score_partie = {
            'nb_disques': nb_disques,
            'nb_coups': nb_coups,
            'temps_jeu': temps_jeu
        }

        # Ajoute la nouvelle partie à la liste des parties du joueur
        scores[joueur.lower()].append(score_partie)
        return scores


    def stat_defaite_victoire(scores, nb_defaite):
        global toutscores
        tout_scores = {}
        tout_defaite = {}
        retouche=False
        # Initialisez la variable tout_scores à une valeur par défaut
        if toutscores == True:
            scores_precedent, defaite_precedente = charger_scores()

            tout_defaite = fusionner_defaites(nb_defaite, defaite_precedente)
            tout_scores = fusionner_scores(scores, scores_precedent)
            toutscores = False
            retouche=True
        else:
            tout_scores=dict(scores)
            tout_defaite=dict(nb_defaite)

        # La suite de votre fonction continue ici en utilisant tout_scores correctement initialisée
        cmp_v = 0
        cmp_d = 0

        vic_def = {}

        # Compter les victoires pour chaque joueur
        for joueur in tout_scores:

            vic_def[joueur] = [len(tout_scores[joueur]), 0]  # Commence avec une victoire et zéro défaite

        # Compter les défaites pour chaque joueur
        for joueur in tout_defaite:
            if joueur in vic_def:
                vic_def[joueur][1] += tout_defaite[joueur]
            else:
                vic_def[joueur] = [0, tout_defaite[joueur]]  # Commence avec zéro victoire et le nombre de défaites actuel

        if retouche==True:
            for joueur, stats in vic_def.items():
                if joueur in scores:
                    vic_def[joueur][0] -= 1  # Soustraire 1 à la victoire
                if joueur in nb_defaite:
                    vic_def[joueur][1] -= 1  # Soustraire 1 à la défaite


        cmp_v = sum(valeurs[0] for valeurs in vic_def.values())
        cmp_d = sum(valeurs[1] for valeurs in vic_def.values())


        for joueur, resultats in vic_def.items():
            gagne, perdu = resultats
            print(f"joueur : {joueur.capitalize()} a gagné {gagne} partie(s) et en a perdu {perdu}")

        return cmp_d, cmp_v


    def pourcentage(cmp_d, cmp_v):

        total = cmp_d + cmp_v

        # Vérifie si le total est égal à zéro pour éviter la division par zéro
        if total != 0:
            pourcentage_victoire = round((cmp_v * 100) / total)
            pourcentage_defaite = round((cmp_d * 100) / total)
            return pourcentage_victoire, pourcentage_defaite
        else:
            # Gérer le cas où le total est égal à zéro (éviter la division par zéro)
            return 0, 0  # Ou tout autre valeur par défaut que vous souhaitez renvoyer




    def sauvegarder_scores(scores, nb_defaite):
        try:
            existing_scores, existing_defeats = charger_scores()

            # Fusionner les scores existants avec les nouveaux
            for player, new_games in scores.items():
                if player in existing_scores:
                    existing_scores[player].extend(new_games)
                else:
                    existing_scores[player] = new_games

            # Fusionner les défaites existantes avec les nouvelles
            for player, new_defeats in nb_defaite.items():
                if player in existing_defeats:
                    existing_defeats[player] += new_defeats
                else:
                    existing_defeats[player] = new_defeats

            data = {'scores': existing_scores, 'nb_defaite': existing_defeats}

            with open('scores.pkl', 'wb') as fichier_scores:
                pickle.dump(data, fichier_scores)
                print("Scores sauvegardés avec succès !")
        except (pickle.PickleError, IOError) as e:
            print(f"Erreur lors de la sauvegarde des scores : {e}")

    def charger_scores():
        try:
            with open('scores.pkl', 'rb') as fichier_scores:
                data = pickle.load(fichier_scores)
                scores = data['scores']
                nb_defaite = data['nb_defaite']
                return scores, nb_defaite
        except (pickle.PickleError, IOError, FileNotFoundError) as e:
            print(f"Erreur lors du chargement des scores : {e}")
            return {}, {}



    def fusionner_scores(scores1, scores2):
        scores_fusionnes = scores1.copy()  # Créer une copie du premier dictionnaire
        for joueur, parties in scores2.items():
            if joueur in scores_fusionnes:
                # Si le joueur existe déjà, fusionner les parties sans doublons
                parties_sans_doublons = []
                for partie in parties:
                    if partie not in scores_fusionnes[joueur]:
                        parties_sans_doublons.append(partie)
                scores_fusionnes[joueur].extend(parties_sans_doublons)
            else:
                # Si le joueur est nouveau, ajouter ses parties directement
                scores_fusionnes[joueur] = parties
        return scores_fusionnes



    def afficheScores(scores, nb_disques=None):
        # Création d'une liste pour stocker les scores triés
        global toutscores

        if toutscores== True:
            scores_precedent,defaite_precedente = charger_scores()
            tout_scores = fusionner_scores(scores, scores_precedent)
            toutscores=False
        else:
            tout_scores=dict(scores)

        scores_tries = []

        # Parcourir les scores pour chaque joueur
        for joueur, parties in tout_scores.items():
            for partie in parties:
                # Si nb_disques est spécifié, filtrer les scores selon ce critère
                if nb_disques is None or partie['nb_disques'] == nb_disques:
                    scores_tries.append((joueur, partie['nb_disques'], partie['nb_coups'], partie['temps_jeu']))

        # Tri des scores par nombre de coups (croissant)
        scores_tries.sort(key=lambda x: x[2])

        # Affichage des scores
        print("Meilleurs scores:")
        for score in scores_tries:
            joueur, disques, coups, temps = score
            if ':' in temps:
                temps += ' minutes'  # Ajout d'un espace avant "minutes"
            print(f"Joueur: {joueur}, Disques: {disques}, Coups: {coups}, Temps: {temps}")

    def afficheChronos(tout_scores):
        scores_trier = []
        global toutscores

        if toutscores== True:
            scores_precedent,defaite_precedente = charger_scores()
            tout_scores = fusionner_scores(scores, scores_precedent)
            toutscores=False
        else:
            tout_scores=dict(scores)

        # Convertir les différentes représentations de temps en secondes
        for joueur in tout_scores:
            temps = tout_scores[joueur][0]['temps_jeu']
            if 'secondes' in temps:
                # Si le temps est en secondes, ajouter le joueur avec le temps en secondes à la liste
                scores_trier.append((joueur, int(temps.split('.')[0])))
            else:
                # Si le temps est en format MM:SS, convertir en secondes et ajouter à la liste
                minutes, secondes = map(int, temps.split(':'))
                scores_trier.append((joueur, minutes * 60 + secondes))

        # Trier par temps de jeu (du plus court au plus long)
        scores_trier = sorted(scores_trier, key=lambda x: x[1])

        # Affichage des résultats
        print("Classement basé sur la durée de jeu (du plus court au plus long) ")
        for joueur, temps in scores_trier:
            print(f"{joueur} : {temps} secondes")

    def reflexionMoy(scores):
        temps_moyen_par_joueur = {}

        for joueur, parties in scores.items():
            temps_total_reflexion = 0
            total_coups = 0

            for partie in parties:
                total_coups += partie['nb_coups']
                temps_reflexion = partie['temps_jeu']

                if 'secondes' in temps_reflexion:
                    temps_total_reflexion += int(temps_reflexion.split('.')[0])
                else:
                    minutes, secondes = map(int, temps_reflexion.split(':'))
                    temps_total_reflexion += minutes * 60 + secondes

            temps_moyen = temps_total_reflexion / total_coups
            temps_moyen_par_joueur[joueur] = temps_moyen

        return temps_moyen_par_joueur


    def classementVitesseJeu(tout_scores):
        global toutscores

        if toutscores== True:
            scores_precedent,defaite_precedente = charger_scores()
            tout_scores = fusionner_scores(scores, scores_precedent)
            toutscores=False
        else:
            tout_scores=dict(scores)

        # Utilisation de la fonction reflexionMoy pour obtenir le temps moyen de réflexion par coup par joueur
        temps_moyen_reflexion = reflexionMoy(tout_scores)

        # Trier les joueurs en fonction du temps moyen de réflexion par coup (du moins au plus rapide)
        classement = sorted(temps_moyen_reflexion.items(), key=lambda x: x[1])

        # Afficher le classement des joueurs les plus rapides (moins de réflexion par coup)
        print("Classement des joueurs les plus rapides (moins de réflexion par coup):")
        for position, (joueur, temps_moyen) in enumerate(classement, start=1):
            print(f"{position}. {joueur}: {temps_moyen:.2f} secondes par coup en moyenne")


    def ajoute_defaite(nom):
        global nb_defaite
        if nom.lower() in nb_defaite:   #verifie si il a deja fait de defaites
            nb_defaite[nom.lower()]+=1
        else :          #cela veut dire que c'est sa premiere defaite
            nb_defaite[nom.lower()]=1



    def affiche_nb_defaite(nb_defaite):
        global toutscores

        if toutscores == True:
            # La fonction charger_scores() doit être définie pour utiliser cette ligne de code
            scores, defaite_precedente = charger_scores()
            tout_defaite = fusionner_defaites(nb_defaite, defaite_precedente)
            toutscores = False  # Modifie la variable globale toutscores
        else:
            tout_defaite=dict(nb_defaite)

        for nom, nb in tout_defaite.items():
            print(f"joueur : {nom} a perdu {nb} fois")


    def fusionner_defaites(defaites1, defaites2):
        defaites_fusionnees = defaites1.copy()  # Créer une copie du premier dictionnaire
        for joueur, nb_defaites in defaites2.items():
            if joueur in defaites_fusionnees:
                # Si le joueur existe déjà dans defaites_fusionnees, ajouter le nombre de défaites
                defaites_fusionnees[joueur] += nb_defaites
            else:
                # Si le joueur est nouveau, ajouter le joueur avec le nombre de défaites
                defaites_fusionnees[joueur] = nb_defaites

        return defaites_fusionnees


#---------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------






        #-------------------------------------------------------------------Menu---------------------------------------------------------------------

    def afficher_animation_intro(texte, delai=0.1):
        for caractere in texte:
            print(caractere, end="", flush=True)
            time.sleep(delai)
        print("\n")

    def effacer_ecran():
        os.system('cls' if os.name == 'nt' else 'clear')

    def afficher_bordure():
        print("\033[1;35;40m" + "-"*50 + "\033[0m")

    def afficher_menu(scores):
        global nb_defaite
        global toutscores
        effacer_ecran()
        afficher_animation_intro("Bienvenue dans le menu des scores", 0.05)
        time.sleep(1)
        while True:
            effacer_ecran()
            afficher_bordure()
            print("\033[1;36;40m*\033[0m Bienvenue dans le \033[1;33;40mMENU INTERACTIF\033[0m \033[1;36;40m-\033[0m".center(52))
            afficher_bordure()
            print("* 1. Afficher le classement des meilleurs scores                  *")
            print("* 2. Afficher le classement en duree de jeu                       *")
            print("* 3. Afficher  classement des joueurs qui jouent le plus vite     *")
            print("* 4. Afficher  nombre de defaite                                  *")
            print("* 5. statistique victoire defaite pour chaque joueur              *")
            print("* 6. Quitter                                                      *")


            afficher_bordure()

            choix = input("\nEntrez votre choix (1-4): ")

            if choix == '1':
                print("\033[1;34;40mOption 1 sélectionnée\033[0m")
                choix = input("Voulez-vous afficher les scores de la partie précédente ? (Oui/Non) ").lower()
                if choix in 'oui':
                    toutscores=True
                afficheScores(scores)
                retour_menu = input("Tapez 'OK' pour revenir: ")
                if retour_menu.lower() == 'ok':
                    continue
                else:
                    time.sleep(10)

            elif choix == '2':
                print("\033[1;34;40mOption 2 sélectionnée\033[0m")
                choix = input("Voulez-vous afficher les scores de la partie précédente ? (Oui/Non) ").lower()
                if choix in 'oui':
                    toutscores=True
                afficheChronos(scores)
                retour_menu = input("Tapez 'OK' pour revenir: ")
                if retour_menu.lower() == 'ok':
                    continue
                else:
                    time.sleep(10)
            elif choix == '3':
                print("\033[1;34;40mOption 3 sélectionnée\033[0m")
                choix = input("Voulez-vous afficher les scores de la partie précédente ? (Oui/Non) ").lower()
                if choix in 'oui':
                    toutscores=True
                classementVitesseJeu(scores)
                retour_menu = input("Tapez 'OK' pour revenir: ")
                if retour_menu.lower() == 'ok':
                    continue
                else:
                    time.sleep(10)
            elif choix== '4':
                print("\033[1;34;40mOption 4 sélectionnée\033[0m")
                choix = input("Voulez-vous afficher les scores de la partie précédente ? (Oui/Non) ").lower()
                if choix in 'oui':
                    toutscores=True
                affiche_nb_defaite(nb_defaite)
                retour_menu = input("Tapez 'OK' pour revenir: ")
                if retour_menu.lower() == 'ok':
                    continue
                else:
                    time.sleep(10)

            elif choix == '5':
                print("\033[1;34;40mOption 5 sélectionnée\033[0m")
                choix = input("Voulez-vous afficher les scores de la partie précédente ? (Oui/Non) ").lower()
                if choix in 'oui':
                    toutscores=True
                cmp_vic,cmp_def=stat_defaite_victoire(scores,nb_defaite)
                vic,deff=pourcentage(cmp_def,cmp_vic)
                print(f"pourcentage de parties gagnees : {vic} % \npourcentage de parties perdu : {deff} %")
                retour_menu = input("Tapez 'OK' pour revenir: ")
                if retour_menu.lower() == 'ok':
                    continue
                else:
                    time.sleep(10)
            elif choix == '6':
                print("\033[1;31;40mAu revoir !\033[0m")
                time.sleep(4)
                break
            else:
                print("\033[1;31;40mChoix invalide, veuillez réessayer.\033[0m")

#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------


    def boucleJeu(plateau, n):
        coup = 0
        abandon = False
        start_time = time.time()

        turtle.onscreenclick(click_handler)

        while not verifVictoire(plateau, n) and not abandon:
            afficherNombreCoupsenBlanc(coup - 1, n)
            afficherNombreCoups(coup, n)

            # Jouer le coup suivant
            resultat = jouerUnCoup(plateau, n)
            print(plateau)
            if resultat is None:  # Abandon
                abandon = True
            else:
                coup += 1
                # Enregistrer le coup
                coups[coup] = [list(tour) for tour in plateau]
                print("Coup numéro", coup)

            # Demander si l'utilisateur veut annuler le dernier coup
            if coup > 0 and not abandon:
                choix = input("Voulez-vous annuler le dernier coup ? (oui/non) ")
                if choix.lower() == "oui":
                    plateau, nouveau_coup = annulerDernierCoup(coups)
                    if plateau is not None:
                        coup = nouveau_coup
                        # Effacer l'affichage actuel et redessiner la dernière configuration
                        turtle.clear()
                        print(plateau)
                        dessineConfig(plateau, n)

        end_time = time.time()  # Fin du chronomètre
        duree_jeu = end_time - start_time  # Durée de la partie en secondes
        if duree_jeu < 60:
            temps_jeu = f"{duree_jeu:.2f} secondes"
        else:
            minutes = int(duree_jeu / 60)
            secondes = int(duree_jeu % 60)
            temps_jeu = f"{minutes}:{secondes}"

        # Effacer l'affichage du chronomètre
        turtle.clear()

        return coup, verifVictoire(plateau, n), abandon, temps_jeu

    def resultat(victoire, temps_de_jeu, n):
        global scores
        turtle.clearscreen()
        nom = turtle.textinput("joueur", "Entrez votre nom ")

        # Création de la fenêtre Tkinter
        resultat_window = tk.Tk()
        resultat_window.title("Résultats de la partie")

        # Fonction pour fermer la fenêtre
        def fermer_fenetre():
            resultat_window.destroy()

        # Affichage des résultats dans un label
        label_resultat = tk.Label(resultat_window, text="", font=("Arial", 14))
        label_resultat.pack(padx=10, pady=10)

        if victoire:
            resultat_texte = f"Bravo {nom} ! Vous avez gagné en {coup} coups.\nTemps : {temps_de_jeu}"
            scores=sauvScore(nom,n,coup,temps_de_jeu)
        elif abandon:
            resultat_texte = f"Abandon de la partie après {coup} coups."


        label_resultat.config(text=resultat_texte)

        # Bouton pour fermer la fenêtre
        bouton_fermer = tk.Button(resultat_window, text="Fermer", command=fermer_fenetre)
        bouton_fermer.pack(pady=10)





    def resoudreHanoi(n, tour_depart, tour_auxiliaire, tour_arrivee):
        if n == 1:
            # Déplacer un seul disque directement de la tour de départ à la tour d'arrivée
            return [(tour_depart, tour_arrivee)]
        else:
            # Étape 1: Déplacer n-1 disques de la tour de départ à la tour auxiliaire
            mouvements = resoudreHanoi(n-1, tour_depart, tour_arrivee, tour_auxiliaire)
            
            # Étape 2: Déplacer le dernier disque de la tour de départ à la tour d'arrivée
            mouvements.append((tour_depart, tour_arrivee))
            
            # Étape 3: Déplacer les n-1 disques de la tour auxiliaire à la tour d'arrivée
            mouvements += resoudreHanoi(n-1, tour_auxiliaire, tour_depart, tour_arrivee)
            
            return mouvements
    
    def afficherMouvements(mouvements):
        """ Affiche les mouvements dans une fenêtre Tkinter. """
        window = tk.Tk()
        window.title("Mouvements des Tours de Hanoï")

        # Créer un label pour chaque mouvement
        for i, (depart, arrivee) in enumerate(mouvements, start=1):
            label = tk.Label(window, text=f"Mouvement {i}: Déplacer de la tour {depart} vers {arrivee}")
            label.pack()

        # Bouton pour fermer la fenêtre
        close_button = tk.Button(window, text="Fermer", command=window.destroy)
        close_button.pack()

        window.mainloop()
    
    def ajuster_positions_boutons(n):
        espace_disponible = 360  # Largeur de l'écran (à ajuster selon vos besoins)
        largeur_bouton = min(50 * n / 2, espace_disponible / 5)  # Ajuster la taille maximale des boutons

        # Calculer l'espace entre les boutons en fonction de leur nombre
        espace_entre_boutons = (espace_disponible - 3 * largeur_bouton) / 4

        # Coordonnées et taille du bouton "Quitter"
        quitter_button_pos = (-180 + (largeur_bouton + espace_entre_boutons) * 0, 200)
        quitter_button_size = (largeur_bouton, largeur_bouton)

        # Coordonnées et taille du bouton "Acceuil"
        acceuil_button_pos = (-180 + (largeur_bouton + espace_entre_boutons) * 1, 200)
        acceuil_button_size = (largeur_bouton, largeur_bouton)

        # Coordonnées et taille du bouton "Solution"
        solution_button_pos = (-180 + (largeur_bouton + espace_entre_boutons) * 2, 200)
        solution_button_size = (largeur_bouton, largeur_bouton)

        return quitter_button_pos, quitter_button_size, acceuil_button_pos, acceuil_button_size, solution_button_pos, solution_button_size



    def click_handler(x, y):
            global abandon, coups,coup

            n=len(coups[0][0])

            quitter_button_pos, quitter_button_size, didacticiel_button_pos, didacticiel_button_size, solution_button_pos, solution_button_size = ajuster_positions_boutons(n)

            # Vérifie si le clic est sur le bouton "Quitter"
            if (quitter_button_pos[0] <= x <= quitter_button_pos[0] + quitter_button_size[0] and
                    quitter_button_pos[1] <= y <= quitter_button_pos[1] + quitter_button_size[1]):
                os.system('cls' if os.name == 'nt' else 'clear')
                turtle.bye()

            # Vérifie si le clic est sur le bouton "didacticiel"
            elif (didacticiel_button_pos[0] <= x <= didacticiel_button_pos[0] + didacticiel_button_size[0] and
                    didacticiel_button_pos[1] <= y <= didacticiel_button_pos[1] + didacticiel_button_size[1]):
                didacticiel()



            # Vérifie si le clic est sur le bouton "Solution"
            elif (solution_button_pos[0] <= x <= solution_button_pos[0] + solution_button_size[0] and
                    solution_button_pos[1] <= y <= solution_button_pos[1] + solution_button_size[1]):
                mouvements = resoudreHanoi(len(coups[0][0]), 0, 1, 2)
                afficherMouvements(mouvements)
                # Réinitialiser l'écoute de la touche espace après chaque clic sur un bouton

              
#-----------------------------------------------------------------------------------------------------------------------------------

    def main():
        
        global coups, scores, nb_defaite, abandon, coup
        jeu_en_cours=True
        while jeu_en_cours :
            turtle.clearscreen()
            wn=turtle.Screen()
            wn.setup(width=0.6, height=1.0)
            n=lecture_nombre_disque()




            # Configuration de Turtle
            coups = {0: init(n)}  # Initialisation avec l'état initial du             # Configuration de Turtle
            turtle.tracer(0, 0)
            wn = turtle.Screen()
            abandon=False
            # Initialisation du plateau
            plateau = init(n)
            ajusterVue(n)  # Ajuste la vue en fonction du nombre de disques
            # Dessiner le plateau et les disques
            dessinePlateau(n, "black", "black")
            dessineConfig(plateau, n)
            quitter_button_pos, quitter_button_size, acceuil_button_pos, acceuil_button_size, solution_button_pos, solution_button_size = ajuster_positions_boutons(n)

            button = Button("Quitter", pos=quitter_button_pos, size=quitter_button_size, color="lightblue")
            button1 = Button("Didacticiel", pos=acceuil_button_pos, size=acceuil_button_size, color="lightblue")
            button2 = Button("solution", pos=solution_button_pos, size=solution_button_size, color="lightblue")


            # Lancement de la boucle de jeu
            coup, victoire, abandon,temps_de_jeu = boucleJeu(plateau, n)
            resultat(victoire,temps_de_jeu,n)


            # Finalisation
            reponse = turtle.textinput("Nouveau joueur ?", "oui/o ou non/n")
            if reponse and reponse.lower() in ['o', 'oui']:
                turtle.clearscreen()  # Effacer l'écran pour la nouvelle partie
            else:
                sauvegarder_scores(scores,nb_defaite)
                turtle.bye()
                afficher_menu(scores)
                jeu_en_cours=False


        turtle.bye()  # Fermer la fenêtre Turtle et terminer le programme
    main()

def draw_background():
    """ Dessine le fond de l'écran. """
    screen = turtle.Screen()
    screen.bgcolor("lightblue")  # Définit la couleur de fond de l'écran



def didacticiel():
    turtle.clearscreen()
    turtle.setworldcoordinates(-turtle.window_width() / 2, -turtle.window_height() / 2,
                               turtle.window_width() / 2, turtle.window_height() / 2)
    class Disc(turtle.Turtle):
        def __init__(self, n, nmax):
            """ Initialise un disque. """
            super().__init__(shape="square", visible=False)
            self.speed(5)
            self.penup()
            self.shapesize(1.5, n*1.5, 2)  # Modifie la forme pour ressembler à un disque
            self.fillcolor(n / nmax, 0.5, 1 - n / nmax)  # Couleur dégradée pour chaque disque
            self.showturtle()

    class Tower(list):
        def __init__(self, x):
            """ Crée une tour vide à une position x spécifiée. """
            self.x = x

        def push(self, d):
            """ Ajoute un disque à la tour. """
            d.setx(self.x)
            d.sety(-150 + 34 * len(self))  # La position y est ajustée en fonction du nombre de disques
            self.append(d)

        def pop(self):
            """ Retire le disque supérieur de la tour et le renvoie. """
            d = list.pop(self)
            d.sety(150)
            return d

    def hanoi(n, from_, with_, to_, moves, move_counter):
        """ Effectue les mouvements selon l'algorithme des Tours de Hanoï. """
        if n > 0:
            hanoi(n - 1, from_, to_, with_, moves, move_counter)
            to_.push(from_.pop())
            moves[0] += 1
            move_counter.clear()
            move_counter.goto(0, turtle.window_height()/2 - 30)  # Position au milieu en haut
            move_counter.write(f"Mouvements: {moves[0]}", align="center", font=("Courier", 16, "bold"))
            hanoi(n - 1, with_, from_, to_, moves, move_counter)


    def start_game():
        """ Efface le message de début et lance le jeu. """
        start_message.clear()
        play()

    def play():
        """ Démarre le jeu des Tours de Hanoï. """
        turtle.onkey(None, "space")
        try:
            hanoi(diskSum, t1, t2, t3, moves, move_counter)
            move_counter.goto(0, -50)  # Nouvelle position pour le message de fin
            move_counter.write("Fin du didacticiel! Fermeture du programme dans 5 secondes...", align="center", font=("Courier", 10, "bold"))
            time.sleep(5)  # Attendre 5 secondes avant de fermer la fenêtre
            turtle.bye()  # Ferme la fenêtre
        except turtle.Terminator:
            pass  # Gère la fermeture du programme


    def main():
        """ Fonction principale pour démarrer le jeu. """
        global t1, t2, t3, diskSum, start_message, moves, move_counter
        diskSum = lecture_nombre_disque()
        turtle.hideturtle()
        t1 = Tower(-250 - diskSum * 30)
        t2 = Tower(0)
        t3 = Tower(250 + diskSum * 30)

        for i in range(diskSum, 0, -1):
            t1.push(Disc(i, diskSum))

        # Afficher le message de début
        start_message = turtle.Turtle()
        start_message.hideturtle()
        start_message.penup()
        start_message.goto(0, -turtle.window_height()/2 + 100)
        start_message.write("Espace pour commencer", align="center", font=("Courier", 16, "bold"))

        # Initialiser le compteur de mouvements
        moves = [0]
        move_counter = turtle.Turtle()
        move_counter.hideturtle()
        move_counter.penup()
        move_counter.goto(0, turtle.window_height()/2 - 30)

        turtle.onkey(start_game, "space")
        turtle.listen()

    if __name__ == "__main__":
        wn = turtle.Screen()
        wn.setup(width=1.0, height=1.00)
        draw_background()
        main()
        turtle.mainloop()


def on_didacticiel_click(x, y):
    # Code à exécuter pour le didacticiel
    print("Didacticiel")
    didacticiel()

def on_Notice_click(x,y):
    notice = """
    Bienvenue dans le Jeu des Tours de Hanoï! Le jeu propose deux modes passionnants: "Jouer" et "Didacticiel". Suivez ces instructions pour profiter pleinement de l'expérience.

    Mode "Jouer":

    1. Objectif du Jeu:
       - Déplacez tous les disques de la Tour de Départ à la Tour d'Arrivée, tout en respectant les règles du jeu.

    2. Règles du Jeu:
       - Vous pouvez déplacer un disque à la fois.
       - Un disque ne peut être placé que sur un disque plus grand ou sur une tour vide.
       - Utilisez les boutons en haut à gauche pour:             
         - voir la liste de mouvements optimaux.
         - Regarder l'animation des mouvement optimaux.
         - Quitter le jeu.

    3. Entrée des Mouvements:
       - Entrez les valeurs des tours de départ et d'arrivée (0, 1, ou 2) pour effectuer un déplacement.
       - Exemple: Entrez "0 2" pour déplacer un disque de la Tour 0 à la Tour 2.

    Mode "Didacticiel":

    1. Tutoriel Interactif:
       - Apprenez les règles du jeu des Tours de Hanoï de manière interactive.
       - Visualisez les meilleurs coups à effectuer.


    2. Conseils et Astuces:
       - Suivez attentivement le tutoriel pour maîtriser les mouvements optimaux.
       - Inspirez vous de ce tutoriel pour résoudre les situations délicates.

    Profitez de ce défi de logique captivant! 🎉
    """

    # Créer une fenêtre Tkinter pour afficher la notice
    notice_window = tk.Tk()
    notice_window.title("Notice du Jeu des Tours de Hanoï")

    # Créer un label pour afficher la notice
    label = tk.Label(notice_window, text=notice, justify=tk.LEFT)
    label.pack(padx=10, pady=10)

    # Bouton pour fermer la fenêtre
    close_button = tk.Button(notice_window, text="Fermer", command=notice_window.destroy)
    close_button.pack(pady=10)

    # Démarrer la boucle Tkinter
    notice_window.mainloop()

def acceuil():
    wn=turtle.Screen()
    wn.setup(width=0.6, height=0.6)
    # Pour garder la fenêtre ouverte
    turtle.clearscreen()
    draw_background()

    titre = turtle.Turtle()
    titre.hideturtle()
    titre.penup()
    titre.goto(0, 100)  # Position du titre en haut
    titre.color("blue")  # Couleur du texte du titre
    titre.write("Bienvenue dans le jeu de Hanoi", align="center", font=("Arial", 24, "bold"))

    # Créer un Turtle pour le sous-titre
    sous_titre = turtle.Turtle()
    sous_titre.hideturtle()
    sous_titre.penup()
    sous_titre.goto(0, 70)  # Position du sous-titre juste en dessous du titre
    sous_titre.color("green")  # Couleur du texte du sous-titre
    sous_titre.write("Choisissez un mode de jeu", align="center", font=("Arial", 18, "normal"))


    # Créer un Turtle pour le bouton Jouer
    btn_jouer = turtle.Turtle()
    btn_jouer.shape("circle")
    btn_jouer.color("purple")
    btn_jouer.shapesize(stretch_wid=1, stretch_len=2)
    btn_jouer.penup()
    btn_jouer.goto(-100, 0)
    btn_jouer.write("Jouer", align="center",font=("Times New Roman", 15, "bold"))
    btn_jouer.sety(-10)  # Déplacer légèrement pour le centrage du texte
    btn_jouer.onclick(on_jouer_click)

    # Créer un Turtle pour le bouton Didacticiel
    btn_didacticiel = turtle.Turtle()
    btn_didacticiel.shape("square")
    btn_didacticiel.color("red")
    btn_didacticiel.shapesize(stretch_wid=1, stretch_len=2)
    btn_didacticiel.penup()
    btn_didacticiel.goto(100, 0)
    btn_didacticiel.write("Didacticiel", align="center",font=("Times New Roman", 15, "bold"))
    btn_didacticiel.sety(-10)  # Déplacer légèrement pour le centrage du texte
    btn_didacticiel.onclick(on_didacticiel_click)

    # Créer un Turtle pour le bouton Notice
    btn_notice = turtle.Turtle()
    btn_notice.shape("arrow")
    btn_notice.color("black")
    btn_notice.shapesize(stretch_wid=1, stretch_len=2)
    btn_notice.penup()
    btn_notice.goto(0, 0)

    # Écrire le texte "Notice" au-dessus du bouton
    btn_notice.write("Notice", align="center", font=("Times New Roman", 15, "bold"))
    btn_notice.sety(-10)  # Déplacer légèrement pour le centrage du texte

    # Lier la fonction on_notice_click au clic sur le bouton
    btn_notice.onclick(on_Notice_click)

    wn.mainloop()

acceuil()