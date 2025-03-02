from collections import defaultdict, deque

def construire_réseau(liste):
    capacité = dict(liste)
    graphe = defaultdict(set)
    for ((i, j), _) in liste:
        graphe[i].add(j)
        graphe[j].add(i)
    return (graphe, capacité)

def ford_fulkerson(graphe, capacité, s, t):
    """Renvoie un flot maximal en utilisant la méthode de Ford-Fulkerson avec un DFS itératif."""
    flot = {a: 0 for a in capacité}
    
    def trouver_chemin_améliorant():
        """Trouve un chemin augmentant en utilisant une pile (DFS itératif)."""
        pile = [(s, set(), [], [])]  # (noeud courant, sommets visités, arcs à augmenter, arcs à réduire)
        
        while pile:
            sommet_actuel, visités, arcs_plus, arcs_moins = pile.pop()
            if sommet_actuel == t:
                return arcs_plus, arcs_moins
            
            for voisin in graphe[sommet_actuel]:
                if voisin not in visités:
                    if (sommet_actuel, voisin) in capacité and capacité[(sommet_actuel, voisin)] > flot[(sommet_actuel, voisin)]:
                        pile.append((voisin, visités | {voisin}, arcs_plus + [(sommet_actuel, voisin)], arcs_moins))
                    elif (voisin, sommet_actuel) in capacité and flot[(voisin, sommet_actuel)] > 0:
                        pile.append((voisin, visités | {voisin}, arcs_plus, arcs_moins + [(voisin, sommet_actuel)]))
        
        return None
    
    chemin = trouver_chemin_améliorant()
    while chemin:
        arcs_plus, arcs_moins = chemin
        delta = min([capacité[a] - flot[a] for a in arcs_plus] + [flot[a] for a in arcs_moins])
        for a in arcs_plus:
            flot[a] += delta
        for a in arcs_moins:
            flot[a] -= delta
        chemin = trouver_chemin_améliorant()
    
    return flot


