
""" Parcours DFS, BFS et DFS récursif avec mesures expérimentales """

from notation_polonaise_inverse import *


# Génération des opérations possibles entre deux nombres
def successeurs(cartons):

    resultats = []

    for i in range(len(cartons)):
        for j in range(i + 1, len(cartons)):

            a, expr_a = cartons[i]
            b, expr_b = cartons[j]

            restants = [cartons[k] for k in range(len(cartons))
                        if k != i and k != j]

            operations = [
                (a + b, expr_a + expr_b + ['+']),
                (a * b, expr_a + expr_b + ['*'])
            ]

            if a > b:
                operations.append((a - b, expr_a + expr_b + ['-']))
            if b > a:
                operations.append((b - a, expr_b + expr_a + ['-']))

            if b != 0 and a % b == 0:
                operations.append((a // b, expr_a + expr_b + ['/']))
            if a != 0 and b % a == 0:
                operations.append((b // a, expr_b + expr_a + ['/']))

            for resultat, expression in operations:
                resultats.append(restants + [(resultat, expression)])

    return resultats


# Mesure de la largeur de l'arbre
def largeur_max(largeurs):
    return max(largeurs) if largeurs else 0


# Affichage des mesures
def afficher_mesures(nom, nb_noeuds, taille_max,
                     hauteur_max, largeurs):

    print("\n---", nom, "---")
    print("Nombre de noeuds parcourus :", nb_noeuds)
    print("Taille maximale de la structure :", taille_max)
    print("Hauteur maximale :", hauteur_max)
    print("Largeur maximale :", largeur_max(largeurs))


# --------------------------------------------------
# DFS : parcours en profondeur itératif
# --------------------------------------------------

def parcours_DFS(cartons, cible):

    initial = [(c, [c]) for c in cartons]

    pile = [(initial, 0)]
    nb_noeuds = 1
    taille_max = 1
    hauteur_max = 0
    largeurs = [1]
    vus = {tuple(sorted(cartons))}

    while pile:

        etat, profondeur = pile.pop()

        for nombre, expression in etat:
            if nombre == cible:
                afficher_mesures("DFS", nb_noeuds, taille_max,
                                 hauteur_max, largeurs)
                return expression, nb_noeuds

        for nouvel_etat in successeurs(etat):

            nb_noeuds += 1

            cle = tuple(sorted(x[0] for x in nouvel_etat))

            if cle not in vus:

                vus.add(cle)
                nouvelle_profondeur = profondeur + 1

                while len(largeurs) <= nouvelle_profondeur:
                    largeurs.append(0)

                largeurs[nouvelle_profondeur] += 1

                if nouvelle_profondeur > hauteur_max:
                    hauteur_max = nouvelle_profondeur

                pile.append((nouvel_etat, nouvelle_profondeur))

                if len(pile) > taille_max:
                    taille_max = len(pile)

    afficher_mesures("DFS", nb_noeuds, taille_max,
                     hauteur_max, largeurs)

    return [], nb_noeuds


# --------------------------------------------------
# BFS : parcours en largeur itératif
# --------------------------------------------------

def parcours_BFS(cartons, cible):

    initial = [(c, [c]) for c in cartons]

    file = [(initial, 0)]
    nb_noeuds = 1
    taille_max = 1
    hauteur_max = 0
    largeurs = [1]
    vus = {tuple(sorted(cartons))}

    while file:

        etat, profondeur = file.pop(0)

        for nombre, expression in etat:
            if nombre == cible:
                afficher_mesures("BFS", nb_noeuds, taille_max,
                                 hauteur_max, largeurs)
                return expression, nb_noeuds

        for nouvel_etat in successeurs(etat):

            nb_noeuds += 1

            cle = tuple(sorted(x[0] for x in nouvel_etat))

            if cle not in vus:

                vus.add(cle)
                nouvelle_profondeur = profondeur + 1

                while len(largeurs) <= nouvelle_profondeur:
                    largeurs.append(0)

                largeurs[nouvelle_profondeur] += 1

                if nouvelle_profondeur > hauteur_max:
                    hauteur_max = nouvelle_profondeur

                file.append((nouvel_etat, nouvelle_profondeur))

                if len(file) > taille_max:
                    taille_max = len(file)

    afficher_mesures("BFS", nb_noeuds, taille_max,
                     hauteur_max, largeurs)

    return [], nb_noeuds


# --------------------------------------------------
# DFS récursif
# --------------------------------------------------

def parcours_DFS_recursif(cartons, cible):

    initial = [(c, [c]) for c in cartons]

    nb_noeuds = 1
    hauteur_max = 0
    largeurs = [1]
    vus = {tuple(sorted(cartons))}
    meilleure_expression = []

    def parcours_DFSR_aux(etat, profondeur):

        nonlocal nb_noeuds
        nonlocal hauteur_max
        nonlocal meilleure_expression

        for nombre, expression in etat:
            if nombre == cible:
                meilleure_expression = expression
                return True

        for nouvel_etat in successeurs(etat):

            nb_noeuds += 1

            cle = tuple(sorted(x[0] for x in nouvel_etat))

            if cle not in vus:

                vus.add(cle)
                nouvelle_profondeur = profondeur + 1

                while len(largeurs) <= nouvelle_profondeur:
                    largeurs.append(0)

                largeurs[nouvelle_profondeur] += 1

                if nouvelle_profondeur > hauteur_max:
                    hauteur_max = nouvelle_profondeur

                if parcours_DFSR_aux(nouvel_etat,
                                     nouvelle_profondeur):
                    return True

        return False

    parcours_DFSR_aux(initial, 0)

    afficher_mesures("DFS récursif", nb_noeuds, 0,
                     hauteur_max, largeurs)

    return meilleure_expression, nb_noeuds


# --------------------------------------------------
# PROGRAMME PRINCIPAL
# --------------------------------------------------

if __name__ == "__main__":

   import time

if __name__ == "__main__":
    cartons = [9, 8, 4, 75, 9, 1]
    cible = 402

    # DFS
    debut = time.perf_counter()
    parcours_DFS(cartons, cible)
    fin = time.perf_counter()
    print("Temps DFS :", fin - debut, "secondes")

    # BFS
    debut = time.perf_counter()
    parcours_BFS(cartons, cible)
    fin = time.perf_counter()
    print("Temps BFS :", fin - debut, "secondes")

    # DFS récursif
    debut = time.perf_counter()
    parcours_DFS_recursif(cartons, cible)
    fin = time.perf_counter()
    print("Temps DFS récursif :", fin - debut, "secondes")