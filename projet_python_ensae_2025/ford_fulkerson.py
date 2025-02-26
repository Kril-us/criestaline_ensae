from collections import defaultdict

# Explication des structures de données utilisées dans la suite:
#   - On représente un graphe orienté par une tâble de hachage (dict en python)
#     qui à chaque sommet associe un ensemble de sommets auquel il est relié.
#   - Les arcs sont représentés par des couples de sommets.
#   - Une fonction de capacité ou de flot sur un réseau est représenté par une 
#     fonction de hachage (dict en python) qui à chaque arc d'un graphe associe
#     une quantité correspondante.

def caca():
    if 0>1:
        return "prout"

def construire_réseau(liste):
    """Aide à construire la structure de graphe orienté et de capacité.
    
    Entrée: une liste de couples (arc, capacité)
    Valeur renvoyé: un graphe et une capacité sur ce graphe
                                                            2             3
    example d'utilisation pour construire le graphe 's' --------> 'u' --------> 't' :
    (graphe, capacité) = construire_réseau([(('s','u'), 2), (('u', 't'), 3)])
    """
    capacité = dict(liste)
    graphe = defaultdict(set)
    for ((i, j), _) in liste:
        graphe[i].add(j)
        graphe[j].add(i)
    return (graphe, capacité)


def ford_fulkerson(graphe, capacité, s, t):
    """Renvoie un flot maximal en utilisant la méthode de Ford-Fulkerson."""
    flot = { a: 0 for (a, _) in capacité.items() } # on commence avec un flot nul partout
    chemin_améliorant = trouver_chemin_améliorant(graphe, capacité, flot, s, t)
    while chemin_améliorant:
        arcs_à_augmenter = chemin_améliorant[0]
        arcs_à_réduire = chemin_améliorant[1]
        delta = min([ capacité[a] - flot[a] for a in arcs_à_augmenter ]
                     + [ flot[a] for a in arcs_à_réduire ])
        flot.update({ a: (flot[a] + delta) for a in arcs_à_augmenter })
        flot.update({ a: (flot[a] - delta) for a in arcs_à_réduire })
        chemin_améliorant = trouver_chemin_améliorant(graphe, capacité, flot, s, t)
    return flot


def trouver_chemin_améliorant(graphe, capacité, flot, s, t):
    """Trouve un chemin améliorant
    Renvoie un couple d'ensembles d'arcs d'un chemin améliorant (arcs à augmenter et arcs à réduire)
    si un tel chemin est trouvé ou renvoie la valeur None si aucun chemin améliorant est trouvé.
    Note: L'algorithme utilisé est un parcours en profondeur.
          Voir https://fr.wikipedia.org/wiki/Algorithme_de_parcours_en_profondeur
          pour plus d'explication.
    """
    def dfs(sommets_visités, sommet_actuel, arcs_à_augmenter, arcs_à_réduire):
        if sommet_actuel == t:
            return arcs_à_augmenter, arcs_à_réduire
        voisins_accessibles_sortant = [ i for i in graphe.get(sommet_actuel, [])
                                        if i not in sommets_visités
                                        and (sommet_actuel, i) in capacité
                                        and (capacité[(sommet_actuel, i)] > flot[(sommet_actuel, i)]) ]
        voisins_accessibles_entrant = [ i for i in graphe.get(sommet_actuel, [])
                                        if i not in sommets_visités
                                        and (i, sommet_actuel) in capacité
                                        and flot[(i, sommet_actuel)] > 0 ]
        for i in voisins_accessibles_sortant:
            foo = dfs(sommets_visités | set(i), i, arcs_à_augmenter | {(sommet_actuel, i)}, arcs_à_réduire)
            if foo:
                return foo
        for i in voisins_accessibles_entrant:
            foo = dfs(sommets_visités | set(i), i, arcs_à_augmenter, arcs_à_réduire | {(i, sommet_actuel)})
            if foo:
                return foo
    return dfs(set(s), s, set(), set())


# Exemple de réseau.
(graphe, capacité) = construire_réseau([(('s','a'), 16),
                                        (('s','b'), 13),
                                        (('a','b'), 10),
                                        (('a','c'), 12),
                                        (('b','a'),  4),
                                        (('b','d'), 14),
                                        (('c','b'),  9),
                                        (('c','t'), 20),
                                        (('d','c'),  7),
                                        (('d','t'),  4)])

# Calcul et affiche un flot maximal du réseau précédent.
flot_maximum = ford_fulkerson(graphe, capacité, 's', 't')
print(flot_maximum)

# La suite du code permet de sauvegarder une image de notre
# résultat en utilisant la librairie graphviz.
# Il faut bien sûr que le package graphviz soit installé:
# https://graphviz.readthedocs.io/en/stable/manual.html#installation

try:
    from graphviz import Digraph

    def afficher_flot(graphe, capacité, flot):
        dot = Digraph(format='png',)
        for (i, j) in capacité.keys():
            dot.edge(i, j, label=str(flot[(i, j)]) + " / " + str(capacité[(i, j)]))
        print("Représentation sauvegardé dans le fichier " + 
              dot.render('flot-maximal', view=True, cleanup=True))

    afficher_flot(graphe, capacité, flot_maximum)
except:
    pass # graphviz n'est pas installé :(