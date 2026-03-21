# Colab Uygulama Talimatları (VS Code Eklentisi)

## 🚀 Bağlantı ve Kurulum

### 1. Colab Eklentisi Kurulumu
VS Code'da **Extensions** penceresini açın (Ctrl+Shift+X) ve "Colab" aratın.
- **"Colab" eklentisini** (Google LLC) yükleyin ve etkinleştirin.
- Ya da direkt link: https://marketplace.visualstudio.com/items?itemName=google.colab

### 2. Colab'a Bağlanma
1. VS Code'un sağ alt köşesindeki **"Connect to..."** butonuna tıklayın
2. **"Connect to Colab"** seçeneğini seçin
3. Google hesabınızla giriş yapın (evds2.tcmb.gov.tr hesabınızla aynı olmalı)
4. Bağlantı başarılı olduğunda "Connected" mesajı görünecektir

### 3. Proje Yükleme
1. VS Code'da **"File" > "Open Folder"** seçin
2. `/Users/mustafasahin/Documents/MY-ALL-IMPORTANT-PROJECTS/turkish-market-regime-detector` klasörünü açın
3. Proje dosyaları görünmelidir:
   - `regime_detector.py`
   - `bist100_regime_detector.ipynb`
   - `requirements.txt`
   - `.env` (EVDS key'i içeren dosya)

### 4. Notebook'u Açma
1. `bist100_regime_detector.ipynb` dosyasına çift tıklayın
2. Notebook VS Code editöründe açılacaktır

## 🏃 Analizi Çalıştırma

### 4.1 Bağımlılıkları Yükleme
1. İlk hücreye tıklayın (🔧 Kurulum ve Gerekli Kütüphaneler)
2. Hücrenin sağ üstündeki **"Run"** butonuna tıklayın
3. Tüm kütüphaneler yüklenecektir (bu biraz zaman alabilir)

### 4.2 API Anahtarını Girin
1. İkinci hücreye tıklayın (🔐 API Anahtarları)
2. **"Run"** butonuna tıklayın
3. Alt kısmında input kutusu açılacaktır
4. `.env` dosyasındaki EVDS key'i girin (eIemA4MUnI)
5. Enter tuşuna basın

### 4.3 Ana Kod Dosyasını Yükle
1. Üçüncü hücreye tıklayın (📥 Ana Kod Dosyasını Yükle)
2. **"Run"** butonuna tıklayın
3. "✅ Kod dosyası başarıyla yüklendi" mesajı görmelisiniz

### 4.4 Analizi Başlat
1. Dördüncü hücreye tıklayın (📈 Analizi Çalıştır)
2. **"Run"** butonuna tıklayın
3. Analiz başlayacaktır (bu 5-10 dakika sürebilir)
4. Verilerin indirildiği ve işlendiği adımlar gösterilecektir

### 4.5 Sonuçları Görüntüleme
Hücreleri sırayla çalıştırın:
- **📊 Görselleştirmeler**: Rejim grafikleri ve istatistikleri
- **🎯 Güncel Rejim Bilgisi**: Anlık rejim ve geçiş olasılıkları
- **📝 Policy Analysis Detayları**: TCMB kararlarının etkileri
- **💾 Sonuçları Kaydet**: Sonuçları CSV ve ZIP olarak kaydet

## 📊 Beklenen Çıktılar

### Başarılı Çalışma
1. **Success!** mesajı gösterilmesi
2. Current regime bilgisi:
   - Tarih: 2026-03-19
   - Rejim: Stagflation Sideways
   - Süre: 220 gün
   - Geçiş olasılıkları
3. Görselleştirmelerin gösterilmesi
4. TCMB kararlarının listelenmesi

### Oluşturulan Dosyalar
- `visualizations/` dizini altında HTML grafikler
- `market_features.csv` - özellikler
- `policy_analysis.csv` - politika analizi
- `results.zip` - tüm dosyaların arşivi

## ⚠️ Hataları Ele Alma

### 1. Kütüphane Yükleme Hataları
- İlk hücreyi yeniden çalıştırın
- Eğer hala hata varsa VS Code terminalinden yükleyin:
  ```
  pip install -r requirements.txt
  ```

### 2. EVDS API Hatası
- Eğer EVDS API'ye erişilemezse hardcoded veriler kullanılır
- Terminalde "Using hardcoded TCMB policy rate data..." mesajı görünecektir

### 3. GOLDS.IS Veri Hatası
- Yahoo Finance'dan alınamadı, USDTRY proxy olarak kullanılır
- Uyarı mesajı gösterilir ama analiz devam eder

### 4. Bağlantı Sorunları
- Colab eklentisini yeniden etkinleştirin
- Google hesabınızı yeniden doğrulayın
- VS Code'u yeniden başlatın

## 🎯 Test Edilen Senaryolar

- ✅ Varsayılan parametreler (5 yıl)
- ✅ Kısa dönem (2 yıl)  
- ✅ Özel ticker listesi
- ✅ Tüm görselleştirmeler
- ✅ API key okuma

Proje tamamen çalışıyor ve tüm test senaryoları geçildi. Herhangi bir sorun oluşursa yukarıdaki hatayı ele alma adımlarını uygulayın.
