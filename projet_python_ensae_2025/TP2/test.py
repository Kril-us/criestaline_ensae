import matplotlib.pyplot as plt
import numpy as np
import random

# Définir les dimensions du tableau (par exemple, 5x5)
rows, cols = 5, 5

# Créer un tableau de nombres aléatoires pour chaque case
tableau = np.random.randint(1, 100, size=(rows, cols))

# Créer un tableau pour les couleurs des cases (blanc, vert, rouge, bleu ou noir)
colors = np.random.choice(['white', 'green', 'red', 'blue', 'black'], size=(rows, cols))

# Tracer l'image du tableau avec matplotlib
fig, ax = plt.subplots()
ax.set_xticks(np.arange(cols + 1) - 0.5, minor=True)
ax.set_yticks(np.arange(rows + 1) - 0.5, minor=True)
ax.grid(which='minor', color='black', linestyle='-', linewidth=2)

# Dessiner les cases avec les couleurs correspondantes
for i in range(rows):
    for j in range(cols):
        ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, color=colors[i, j]))
        ax.text(j, i, str(tableau[i, j]), ha='center', va='center', color='white' if colors[i, j] != 'black' else 'black')

# Suppression des axes
ax.set_xticks([])
ax.set_yticks([])

# Afficher le tableau
plt.show()