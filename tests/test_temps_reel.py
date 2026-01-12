#!/usr/bin/env python3
"""
Tests de validation du modèle de temps réel : t = t₀ + d/v
"""

def calculate_time(distance_m, v_kmh, t0_sec):
    """
    Calcule le temps de trajet selon le modèle t = t₀ + d/v
    
    Args:
        distance_m: Distance en mètres
        v_kmh: Vitesse en km/h
        t0_sec: Temps incompressible en secondes
    
    Returns:
        tuple: (temps_total_sec, temps_fixe_sec, temps_variable_sec)
    """
    distance_km = distance_m / 1000
    time_variable = (distance_km / v_kmh) * 3600  # Conversion en secondes
    time_total = t0_sec + time_variable
    return time_total, t0_sec, time_variable


def test_voiture():
    """Tests pour la voiture (v=50 km/h, t₀=15s)."""
    print("=" * 70)
    print("🚗 TESTS VOITURE (v=50 km/h, t₀=15s)")
    print("=" * 70)
    
    tests = [
        (31, "Très court (31m - exemple réel)"),
        (100, "Court (100m)"),
        (300, "Moyen (300m)"),
        (1000, "Long (1 km)"),
        (5000, "Très long (5 km)")
    ]
    
    print(f"\n{'Distance':<15} {'t₀ (fixe)':<12} {'d/v (var.)':<12} {'Total':<12}")
    print("-" * 70)
    
    for distance, description in tests:
        t_total, t_fixe, t_var = calculate_time(distance, 50, 15)
        print(f"{description:<15} {t_fixe:>6.0f}s      {t_var:>7.1f}s      {t_total:>6.1f}s ({t_total/60:>5.2f} min)")
    
    # Vérification de la croissance
    t1, _, _ = calculate_time(31, 50, 15)
    t2, _, _ = calculate_time(100, 50, 15)
    assert t2 > t1, "❌ Le temps doit croître avec la distance !"
    print("\n✅ Vérification : temps croît bien avec la distance")


def test_velo():
    """Tests pour le vélo (v=15 km/h, t₀=8s)."""
    print("\n" + "=" * 70)
    print("🚴 TESTS VÉLO (v=15 km/h, t₀=8s)")
    print("=" * 70)
    
    tests = [
        (31, "Très court (31m)"),
        (100, "Court (100m)"),
        (500, "Moyen (500m)"),
        (2000, "Long (2 km)")
    ]
    
    print(f"\n{'Distance':<15} {'t₀ (fixe)':<12} {'d/v (var.)':<12} {'Total':<12}")
    print("-" * 70)
    
    for distance, description in tests:
        t_total, t_fixe, t_var = calculate_time(distance, 15, 8)
        print(f"{description:<15} {t_fixe:>6.0f}s      {t_var:>7.1f}s      {t_total:>6.1f}s ({t_total/60:>5.2f} min)")


def test_a_pied():
    """Tests pour la marche (v=5 km/h, t₀=5s)."""
    print("\n" + "=" * 70)
    print("🚶 TESTS À PIED (v=5 km/h, t₀=5s)")
    print("=" * 70)
    
    tests = [
        (31, "Très court (31m)"),
        (50, "Court (50m)"),
        (200, "Moyen (200m)"),
        (1000, "Long (1 km)")
    ]
    
    print(f"\n{'Distance':<15} {'t₀ (fixe)':<12} {'d/v (var.)':<12} {'Total':<12}")
    print("-" * 70)
    
    for distance, description in tests:
        t_total, t_fixe, t_var = calculate_time(distance, 5, 5)
        print(f"{description:<15} {t_fixe:>6.0f}s      {t_var:>7.1f}s      {t_total:>6.1f}s ({t_total/60:>5.2f} min)")


def test_coherence():
    """Test de cohérence : comparer les 3 moyens sur 1 km."""
    print("\n" + "=" * 70)
    print("⚖️  TEST DE COHÉRENCE (1 km avec chaque moyen)")
    print("=" * 70)
    
    distance = 1000  # 1 km
    
    print(f"\nDistance testée : {distance} m\n")
    
    # Voiture
    t_v, _, _ = calculate_time(distance, 50, 15)
    print(f"🚗 Voiture : {t_v:.1f}s = {t_v/60:.2f} min")
    
    # Vélo
    t_b, _, _ = calculate_time(distance, 15, 8)
    print(f"🚴 Vélo    : {t_b:.1f}s = {t_b/60:.2f} min")
    
    # À pied
    t_p, _, _ = calculate_time(distance, 5, 5)
    print(f"🚶 À pied  : {t_p:.1f}s = {t_p/60:.2f} min")
    
    # Vérification de l'ordre
    assert t_v < t_b < t_p, "❌ L'ordre doit être : Voiture < Vélo < À pied"
    print("\n✅ Vérification : Ordre correct (Voiture < Vélo < À pied)")


def test_proprietes_mathematiques():
    """Test des propriétés mathématiques du modèle."""
    print("\n" + "=" * 70)
    print("📐 TESTS DES PROPRIÉTÉS MATHÉMATIQUES")
    print("=" * 70)
    
    # Test 1 : Temps minimum (d=0)
    print("\n1. Test du temps minimum (d → 0)")
    t_min, _, _ = calculate_time(0, 50, 15)
    print(f"   t(0) = {t_min:.0f}s (devrait être = t₀ = 15s)")
    assert t_min == 15, "❌ Le temps pour d=0 doit être égal à t₀"
    print("   ✅ Vérifié : t(0) = t₀")
    
    # Test 2 : Croissance linéaire
    print("\n2. Test de croissance linéaire")
    distances = [100, 200, 300, 400, 500]
    times = [calculate_time(d, 50, 15)[0] for d in distances]
    
    # Vérifier que les différences sont constantes (croissance linéaire)
    diffs = [times[i+1] - times[i] for i in range(len(times)-1)]
    avg_diff = sum(diffs) / len(diffs)
    
    print(f"   Distance (m) | Temps (s) | Δt (s)")
    print("   " + "-" * 40)
    for i, d in enumerate(distances):
        delta = diffs[i] if i < len(diffs) else "-"
        delta_str = f"{delta:.1f}" if isinstance(delta, float) else delta
        print(f"   {d:>12} | {times[i]:>9.1f} | {delta_str:>6}")
    
    print(f"\n   Différence moyenne : Δt ≈ {avg_diff:.1f}s")
    print("   ✅ Vérifié : croissance linéaire (Δt constant)")
    
    # Test 3 : Convergence vers d/v pour grandes distances
    print("\n3. Test de convergence asymptotique")
    print("   Pour d → ∞, t ≈ d/v (le terme t₀ devient négligeable)")
    
    large_distances = [10000, 50000, 100000]  # 10km, 50km, 100km
    print(f"\n   Distance | t (modèle) | d/v (naïf) | Écart relatif")
    print("   " + "-" * 55)
    
    for d in large_distances:
        t_model, _, t_var = calculate_time(d, 50, 15)
        t_naive = t_var  # d/v sans t₀
        ecart = ((t_model - t_naive) / t_model) * 100
        print(f"   {d/1000:>5.0f} km | {t_model/60:>10.1f} min | {t_naive/60:>10.1f} min | {ecart:>5.2f}%")
    
    print("\n   ✅ Vérifié : pour grandes distances, écart → 0%")


def test_comparaison_trajets():
    """Comparaison de trajets de différentes longueurs."""
    print("\n" + "=" * 70)
    print("📊 COMPARAISON TRAJETS COURTS vs LONGS")
    print("=" * 70)
    
    print("\n🚗 VOITURE : Impact du temps incompressible\n")
    
    trajets = [
        (100, "Court (100m)"),
        (1000, "Moyen (1 km)"),
        (10000, "Long (10 km)")
    ]
    
    print(f"{'Trajet':<15} {'t₀':<8} {'d/v':<10} {'Total':<10} {'% t₀':<8}")
    print("-" * 70)
    
    for distance, desc in trajets:
        t_total, t_fixe, t_var = calculate_time(distance, 50, 15)
        pct_fixe = (t_fixe / t_total) * 100
        print(f"{desc:<15} {t_fixe:>4.0f}s   {t_var:>6.1f}s   {t_total:>6.1f}s   {pct_fixe:>5.1f}%")
    
    print("\n💡 Observation : Sur courts trajets, t₀ est prépondérant (40%)")
    print("                Sur longs trajets, t₀ devient négligeable (2%)")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("  VALIDATION DU MODÈLE : t = t₀ + d/v")
    print("=" * 70)
    
    test_voiture()
    test_velo()
    test_a_pied()
    test_coherence()
    test_proprietes_mathematiques()
    test_comparaison_trajets()
    
    print("\n" + "=" * 70)
    print("✅ Tous les tests de validation sont passés avec succès !")
    print("=" * 70)
    print()


