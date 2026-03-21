#!/usr/bin/env python3
"""
Test script for BIST100 regime detector
"""

from regime_detector import run_analysis

print("=== BIST100 Rejim Tespiti Testleri ===\n")

# Test 1: Default parameters (5 years)
print("1. Test: Varsayılan Parametreler (5 Yıl)")
try:
    results1 = run_analysis(period="5y")
    print("✅ Başarılı!")
    print(f"   Rejim: {results1['current_regime']['regime']}")
    print(f"   Süre: {results1['current_regime']['duration_days']} gün")
except Exception as e:
    print(f"❌ Hata: {e}")

print("\n" + "-"*50 + "\n")

# Test 2: Short period (2 years)
print("2. Test: Kısa Dönem (2 Yıl)")
try:
    results2 = run_analysis(period="2y")
    print("✅ Başarılı!")
    print(f"   Rejim: {results2['current_regime']['regime']}")
    print(f"   Süre: {results2['current_regime']['duration_days']} gün")
except Exception as e:
    print(f"❌ Hata: {e}")

print("\n" + "-"*50 + "\n")

# Test 3: Custom tickers
print("3. Test: Özel Ticker Listesi")
try:
    custom_tickers = ["XU100.IS", "XBANK.IS", "XUSIN.IS", "USDTRY=X", "EEM"]
    results3 = run_analysis(tickers=custom_tickers, period="3y")
    print("✅ Başarılı!")
    print(f"   Rejim: {results3['current_regime']['regime']}")
    print(f"   Süre: {results3['current_regime']['duration_days']} gün")
except Exception as e:
    print(f"❌ Hata: {e}")

print("\n" + "-"*50 + "\n")

# Test 4: Verify visualizations are created
print("4. Test: Görselleştirmeler Kontrolü")
try:
    from pathlib import Path
    
    viz_dir = Path("visualizations")
    required_files = ["main_plot.html", "stats_heatmap.html", "transition_matrix.html", "sector_performance.html"]
    
    all_files_exist = all((viz_dir / file).exists() for file in required_files)
    
    if all_files_exist:
        print("✅ Tüm görselleştirmeler oluşturuldu!")
        for file in required_files:
            size = (viz_dir / file).stat().st_size / 1024
            print(f"   {file}: {size:.1f} KB")
    else:
        print("❌ Bazı görselleştirmeler eksik!")
        missing = [file for file in required_files if not (viz_dir / file).exists()]
        print(f"   Eksik: {', '.join(missing)}")
        
except Exception as e:
    print(f"❌ Hata: {e}")

print("\n=== Test Tamamlandı ===")
