# 📸 Images de l'Application Web

## Instructions pour ajouter les captures d'écran

Sauvegarde les 5 captures d'écran dans ce dossier avec les noms suivants :

### 1. `webapp_accueil.png`
- **Capture** : Première image - Carte interactive avec tous les points bleus
- **Description** : Vue d'ensemble de la carte de Paris avec le réseau routier

### 2. `webapp_parametres.png`
- **Capture** : Deuxième image - Panneau latéral avec les options
- **Description** : Configuration (type de carte OSM, algorithme A*, transport Voiture)

### 3. `webapp_selection.png`
- **Capture** : Troisième image - Points de départ/arrivée sélectionnés
- **Description** : Sélection des intersections 311 (départ) et 184 (arrivée)

### 4. `webapp_resultat.png`
- **Capture** : Quatrième image - Trajet calculé affiché en rouge
- **Description** : Résultat avec distance 1.7415 km, temps 2.3 min, 21 étapes

### 5. `webapp_comparaison.png`
- **Capture** : Cinquième image - Popup de comparaison des 3 algorithmes
- **Description** : Comparaison Dijkstra (0.69ms, 333 sommets) vs A* (0.33ms, 50 sommets) vs Bellman-Ford (192.58ms, 491 sommets)

## Comment sauvegarder

1. Sauvegarde chaque capture d'écran depuis le chat
2. Renomme-les avec les noms exacts ci-dessus
3. Place-les dans ce dossier : `docs/figures/webapp/`
4. Vérifie que les noms correspondent exactement (sensible à la casse)

## Vérification

Après avoir sauvegardé, vérifie avec :
```bash
ls -l docs/figures/webapp/
```

Tu devrais voir :
- webapp_accueil.png
- webapp_parametres.png
- webapp_selection.png
- webapp_resultat.png
- webapp_comparaison.png
