# Modèle de Temps de Trajet Réaliste en Milieu Urbain

## 📐 Problématique

Le modèle naïf de calcul du temps de trajet est :

$$t = \frac{d}{v}$$

Ce modèle présente plusieurs **défauts majeurs** :

1. **Temps nul pour distance nulle** : $t(0) = 0$ (irréaliste)
2. **Ignore le temps incompressible** : démarrage, arrêt, feux rouges
3. **Non réaliste en ville** : on ne roule jamais immédiatement à vitesse maximale

## ✅ Solution : Modèle avec Temps Incompressible

### Principe

En milieu urbain, tout trajet comporte deux phases :
1. **Phase statique** (temps incompressible) : démarrage, feux, arrêt
2. **Phase mobile** (temps de déplacement) : trajet à vitesse moyenne

### Modèle Mathématique

$$t(d) = t_0 + \frac{d}{v}$$

Où :
- $t_0$ : temps incompressible (en secondes)
- $d$ : distance parcourue (en km)
- $v$ : vitesse moyenne (en km/h)

## 📊 Paramètres Calibrés

| Moyen de transport | $v$ (km/h) | $t_0$ (s) | Justification |
|--------------------|------------|-----------|---------------|
| 🚗 Voiture         | 50         | 15        | Démarrage + 1 feu rouge + arrêt |
| 🚴 Vélo           | 15         | 8         | Plus agile (moins impacté par feux) |
| 🚶 À pied         | 5          | 5         | Démarrage quasi instantané |

### Justification des valeurs de $t_0$

**🚗 Voiture (15s) :**
- Démarrage moteur + mise en route : ~3s
- Passage d'un feu rouge moyen : ~8s
- Arrêt et stationnement : ~4s
- **Total : ≈ 15s**

**🚴 Vélo (8s) :**
- Démarrage (pied à terre → pédalage) : ~3s
- Moins impacté par les feux (peut contourner) : ~3s
- Arrêt : ~2s
- **Total : ≈ 8s**

**🚶 À pied (5s) :**
- Démarrage (immobile → marche) : ~2s
- Traversées de rues : ~2s
- Arrêt : ~1s
- **Total : ≈ 5s**

## 🧮 Exemples de Calcul

### Exemple 1 : Trajet court en voiture (31 m)

**Données :**
- $d = 0.031$ km
- $v = 50$ km/h
- $t_0 = 15$ s

**Calcul :**
$$t = 15 + \frac{0.031}{50} \times 3600 = 15 + 2.2 = 17.2 \text{ secondes}$$

✅ **Réaliste !** (temps de démarrer, rouler 31m, s'arrêter)

### Exemple 2 : Trajet moyen à pied (200 m)

**Données :**
- $d = 0.2$ km
- $v = 5$ km/h
- $t_0 = 5$ s

**Calcul :**
$$t = 5 + \frac{0.2}{5} \times 3600 = 5 + 144 = 149 \text{ secondes} \approx 2.5 \text{ minutes}$$

✅ **Cohérent !**

### Exemple 3 : Long trajet en vélo (5 km)

**Données :**
- $d = 5$ km
- $v = 15$ km/h
- $t_0 = 8$ s

**Calcul :**
$$t = 8 + \frac{5}{15} \times 3600 = 8 + 1200 = 1208 \text{ secondes} \approx 20.1 \text{ minutes}$$

✅ **Réaliste !**

## 📈 Propriétés Mathématiques

### 1. Continuité
La fonction $t(d)$ est **continue** et **dérivable** sur $\mathbb{R}^+$ :
$$t(d) \in C^{\infty}(\mathbb{R}^+)$$

### 2. Croissance stricte
$$\frac{dt}{dd} = \frac{1}{v} > 0, \quad \forall d \geq 0$$

Le temps croît **linéairement** avec la distance.

### 3. Ordonnée à l'origine
$$t(0) = t_0 > 0$$

Même pour un déplacement nul, il y a un temps minimum (réaliste).

### 4. Comportement asymptotique
Pour les longues distances :
$$\lim_{d \to \infty} \frac{t(d)}{d/v} = \lim_{d \to \infty} \frac{t_0 + d/v}{d/v} = 1$$

Le modèle converge vers le modèle naïf $t = d/v$ pour les grandes distances.

## 📊 Validation Numérique

### Test 1 : Cohérence entre moyens de transport

Pour une distance de **1 km** :

| Moyen | Calcul | Temps |
|-------|--------|-------|
| 🚶 À pied | $5 + 1/5 \times 3600 = 725$ s | **12.1 min** |
| 🚴 Vélo | $8 + 1/15 \times 3600 = 248$ s | **4.1 min** |
| 🚗 Voiture | $15 + 1/50 \times 3600 = 87$ s | **1.5 min** |

✅ **Ordre respecté** : Voiture < Vélo < À pied

### Test 2 : Proportionnalité pour longues distances

Pour la **voiture** sur différentes distances :

| Distance | Temps fixe | Temps trajet | Temps total |
|----------|------------|--------------|-------------|
| 1 km | 15s | 72s | 87s (1.5 min) |
| 2 km | 15s | 144s | 159s (2.7 min) |
| 5 km | 15s | 360s | 375s (6.3 min) |
| 10 km | 15s | 720s | 735s (12.3 min) |

✅ **Croissance linéaire** vérifiée

## 🎯 Avantages du Modèle

| Critère | Évaluation |
|---------|------------|
| **Simplicité** | ✅ Formule linéaire |
| **Réalisme** | ✅ Temps minimum incompressible |
| **Justification** | ✅ Physiquement cohérent |
| **Continuité** | ✅ Fonction continue et dérivable |
| **Calibrage** | ✅ Deux paramètres intuitifs ($v$, $t_0$) |
| **Proportionnalité** | ✅ Temps croît linéairement avec $d$ |

## 📚 Comparaison avec Modèle Précédent

### Modèle précédent (vitesse effective)
$$v_{\text{eff}}(d) = v_{\max} \times \min\left(1, \frac{d}{d_0}\right)$$
$$t = \frac{d}{v_{\text{eff}}(d)}$$

**Problème identifié :**
Pour $d < d_0$ :
$$t = \frac{d}{v_{\max} \times d/d_0} = \frac{d_0}{v_{\max}} = \text{constante}$$

❌ **Le temps ne dépend PAS de la distance !** (défaut majeur)

### Notre modèle (temps incompressible)
$$t = t_0 + \frac{d}{v}$$

✅ **Le temps croît TOUJOURS avec la distance**  
✅ **Plus simple mathématiquement**  
✅ **Plus facile à justifier physiquement**

## 🔬 Pistes d'Amélioration

### Version avancée : Temps incompressible variable

On pourrait affiner avec :
$$t_0(d) = t_{\text{min}} + k \times \left\lfloor \frac{d}{d_{\text{feu}}} \right\rfloor$$

Où :
- $t_{\text{min}}$ : temps de démarrage/arrêt
- $k$ : temps moyen par feu rouge
- $d_{\text{feu}}$ : distance moyenne entre deux feux

Mais cela complexifie le modèle sans gain majeur pour un projet BUT.

## 📝 Conclusion

Le modèle $t = t_0 + d/v$ offre le **meilleur compromis** :
- ✅ Simplicité mathématique
- ✅ Réalisme urbain
- ✅ Justification physique claire
- ✅ Facilité de calibrage

Il est **parfaitement adapté** à un projet BUT Informatique niveau S5.

---

**Auteurs :** Diallo Abdoulaye, Semih Taskin, Muller Arthur  
**Date :** Janvier 2026  
**Projet :** GPS Intelligent - Optimisation de trajets urbains


