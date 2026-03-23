# turkish-market-regime-detector
Market regime detection for BIST100 using KMeans &amp; HMM — integrated with TCMB monetary policy data to classify Turkish equity market conditions as Risk-On, Carry Unwind, or Stagflation Sideways.


🇬🇧 English

## About This Project

This project detects and visualizes market regimes for **BIST100**
(Turkish Stock Exchange) using unsupervised machine learning.
By combining **KMeans clustering** and **Hidden Markov Models (HMM)**
with technical indicators (RSI, volatility, moving averages) and
**TCMB (Central Bank of Turkey) monetary policy data**, it classifies
the market into three regimes:

- 🟢 **Risk-On** — Bullish trend, foreign inflow, TL stable
- 🔴 **Carry Unwind** — Bearish pressure, TL depreciation, capital outflow
- 🔵 **Stagflation Sideways** — High inflation, low growth, directionless market

The goal is to help traders and analysts better understand Turkish
market dynamics and time their decisions around TCMB policy shifts.

-------------------
🇹🇷 Türkçe

## Proje Hakkında

Bu proje, **BIST100** için piyasa rejimlerini gözetimsiz makine öğrenmesi
yöntemleriyle tespit eder ve görselleştirir.
**KMeans kümeleme** ve **Gizli Markov Modeli (HMM)** algoritmalarını
teknik göstergeler (RSI, volatilite, hareketli ortalamalar) ve
**TCMB para politikası verileriyle** birleştirerek piyasayı
üç rejime sınıflandırır:

- 🟢 **Risk-On** — Yükseliş trendi, yabancı girişi, TL güçlü
- 🔴 **Carry Unwind** — Düşüş baskısı, TL değer kaybı, sermaye çıkışı
- 🔵 **Stagflasyon Sideways** — Yüksek enflasyon, düşük büyüme, yatay piyasa

Amaç; trader ve analistlerin Türkiye piyasa dinamiklerini daha iyi
anlamasına ve TCMB politika değişikliklerine göre kararlarını
zamanlamasına yardımcı olmaktır.

-
## Risk-On
**TR:** Yatırımcıların küresel ekonomiye dair iyimser beklentilerle hareket ettiği ve yüksek getiri amacıyla güvenli limanlardan çıkıp hisse senedi, kripto para gibi riskli varlıklara yöneldiği piyasa ortamıdır. [heygotrade](https://www.heygotrade.com/en/blog/understanding-risk-on-risk-off-market)

**EN:** An optimistic market environment where investors feel confident about economic growth and move capital away from safe-haven assets into higher-yielding, riskier assets like equities and cryptocurrencies. [capital](https://capital.com/en-int/learn/glossary/risk-on-risk-off-definition)

## Carry Unwind
**TR:** Düşük faizli bir para biriminden borçlanılarak yüksek getirili varlıklara yapılan yatırımların (carry trade), piyasadaki panik veya artan volatilite sebebiyle hızla satılıp borcun kapatılması sürecidir. [tastyfx](https://www.tastyfx.com/news/how-the-carry-trade-works-and-position-unwinds-explained/)

**EN:** The rapid reversal of carry trades, where investors quickly sell off high-yielding risk assets to buy back the low-yielding borrowed currency, usually triggered by market panic or rising volatility. [ebc](https://www.ebc.com/forex/yen-carry-trade-unwind-could-it-trigger-the-next-market-crash)

## Stagflation Sideways
**TR:** Ekonomik durgunluk ile yüksek enflasyonun aynı anda yaşandığı (stagflasyon) ve bu belirsizlik nedeniyle varlık fiyatlarının uzun süre belirgin bir trend oluşturmadan dar bir bantta yatay (sideways) dalgalandığı piyasa koşuludur. [heygotrade](https://www.heygotrade.com/en/blog/understanding-risk-on-risk-off-market)

**EN:** A period of economic uncertainty combining stagnant growth with high inflation (stagflation), causing asset prices to fluctuate within a narrow, directionless range (sideways) for an extended period. [capital](https://capital.com/en-int/learn/glossary/risk-on-risk-off-definition)

---

# 📖 Quick Start Guide / Hızlı Başlangıç Rehberi

## 🇬🇧 English

### 1. Installation / Kurulum

```bash
# Clone the project
git clone https://github.com/yourusername/turkish-market-regime-detector.git
cd turkish-market-regime-detector

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Requirements / Gereksinimler

The following packages are required:
- `yfinance` - Yahoo Finance data fetching
- `pandas` - Data manipulation
- `numpy` - Numerical computing
- `scikit-learn` - Machine learning (K-Means)
- `hmmlearn` - Hidden Markov Models (optional)
- `plotly` - Interactive visualizations
- `requests` - HTTP requests

Install all:
```bash
pip install yfinance pandas numpy scikit-learn hmmlearn plotly requests
```

### 3. Running the Project / Projeyi Çalıştırma

#### Option A: Python Script
```python
from src import run_analysis

# Run analysis with default settings
results = run_analysis(period="2y", n_regimes=3)
print(results['current_regime'])
```

#### Option B: Using Modules Directly
```python
from src.data.yfinance_fetcher import YFinanceFetcher
from src.data.processor import DataProcessor
from src.models.kmeans_model import KMeansRegimeModel

# Fetch data
fetcher = YFinanceFetcher(period="2y")
prices = fetcher.fetch_multiple_tickers(["THYAO.IS", "GARAN.IS", "AKBNK.IS"])

# Create features
processor = DataProcessor()
features = processor.create_features(prices)
features_norm = processor.normalize_features(features)

# Train model
model = KMeansRegimeModel(n_regimes=3)
model.fit(features_norm)
regimes = model.predict(features_norm)

print(f"Regime distribution: {dict(zip(*np.unique(regimes, return_counts=True)))}")
```

#### Option C: Google Colab
Open `colab_regime_detector.ipynb` in Google Colab and run the cells.

### 4. Project Structure / Proje Yapısı

```
turkish-market-regime-detector/
├── src/                          # Main package
│   ├── __init__.py              # Package init + backward compatibility
│   ├── config/                  # Configuration
│   │   ├── constants.py         # REGIME_LABELS, TCMB_POLICY_DECISIONS
│   │   └── settings.py         # Settings dataclass
│   ├── data/                    # Data fetching & processing
│   │   ├── yfinance_fetcher.py # Yahoo Finance data fetcher
│   │   ├── evds_fetcher.py     # TCMB EVDS data fetcher
│   │   └── processor.py        # Feature engineering
│   ├── models/                  # ML models
│   │   ├── base.py             # Base model class
│   │   ├── kmeans_model.py     # K-Means clustering
│   │   └── hmm_model.py        # Hidden Markov Model
│   ├── visualization/           # Plotting
│   │   ├── plots.py            # Plotly charts
│   │   └── export.py           # Export utilities
│   └── backtesting/             # Backtesting (optional)
│       ├── engine.py           # Backtest engine
│       └── strategies.py       # Trading strategies
├── tests/
│   └── test_suite.py           # Unit tests
├── colab_regime_detector.ipynb # Google Colab notebook
├── regime_detector.py          # Legacy code (backward compatible)
├── requirements.txt            # Dependencies
└── README.md                   # This file
```

### 5. Running Tests / Testleri Çalıştırma

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test class
python -m pytest tests/test_suite.py::TestKMeansModel -v

# Run with coverage
python -m pytest tests/ --cov=src
```

Test Results: **43 passed** (all tests)

### 6. Usage Examples / Kullanım Örnekleri

#### Example 1: Basic Regime Detection
```python
import pandas as pd
from src.data.yfinance_fetcher import YFinanceFetcher
from src.data.processor import DataProcessor
from src.models.kmeans_model import KMeansRegimeModel

# 1. Fetch data
fetcher = YFinanceFetcher(period="2y")
prices = fetcher.fetch_multiple_tickers(["THYAO.IS", "GARAN.IS"])

# 2. Create features
processor = DataProcessor()
features = processor.create_features(prices)
features_norm = processor.normalize_features(features)

# 3. Train model
model = KMeansRegimeModel(n_regimes=3, random_state=42)
model.fit(features_norm)

# 4. Predict
regimes = model.predict(features_norm)
print(f"Regimes: {regimes[:10]}")
```

#### Example 2: Backtesting
```python
from src.backtesting.engine import run_backtest

# Run backtest with regime strategy
result = run_backtest(prices, regimes, strategy="regime")
print(f"Total Return: {result.total_return:.2%}")
print(f"Sharpe Ratio: {result.sharpe_ratio:.2f}")
```

#### Example 3: Visualization
```python
from src.visualization.plots import RegimePlotter

plotter = RegimePlotter()
fig = plotter.plot_prices_with_regimes(prices, regimes)
fig.show()  # Opens interactive plot
```

### 7. Environment Variables / Ortam Değişkenleri

For TCMB EVDS data (optional):
```bash
export EVDS_API_KEY="your_api_key_here"
```

Or in Python:
```python
import os
os.environ["EVDS_API_KEY"] = "your_api_key"
```

---

## 🇹🇷 Türkçe

### 1. Kurulum

```bash
# Projeyi klonla
git clone https://github.com/yourusername/turkish-market-regime-detector.git
cd turkish-market-regime-detector

# Sanal ortam oluştur (önerilen)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya: venv\Scripts\activate  # Windows

# Bağımlılıkları yükle
pip install -r requirements.txt
```

### 2. Gereksinimler

Aşağıdaki paketler gereklidir:
- `yfinance` - Yahoo Finance veri çekme
- `pandas` - Veri işleme
- `numpy` - Sayısal hesaplama
- `scikit-learn` - Makine öğrenmesi (K-Means)
- `hmmlearn` - Gizli Markov Modelleri (opsiyonel)
- `plotly` - İnteraktif görselleştirme
- `requests` - HTTP istekleri

Tümünü yükle:
```bash
pip install yfinance pandas numpy scikit-learn hmmlearn plotly requests
```

### 3. Projeyi Çalıştırma

#### Seçenek A: Python Betiği
```python
from src import run_analysis

# Varsayılan ayarlarla analiz çalıştır
results = run_analysis(period="2y", n_regimes=3)
print(results['current_regime'])
```

#### Seçenek B: Modülleri Doğrudan Kullanma
```python
from src.data.yfinance_fetcher import YFinanceFetcher
from src.data.processor import DataProcessor
from src.models.kmeans_model import KMeansRegimeModel

# Veri çek
fetcher = YFinanceFetcher(period="2y")
prices = fetcher.fetch_multiple_tickers(["THYAO.IS", "GARAN.IS", "AKBNK.IS"])

# Özellikler oluştur
processor = DataProcessor()
features = processor.create_features(prices)
features_norm = processor.normalize_features(features)

# Model eğit
model = KMeansRegimeModel(n_regimes=3)
model.fit(features_norm)
regimes = model.predict(features_norm)

print(f"Rejim dağılımı: {dict(zip(*np.unique(regimes, return_counts=True)))}")
```

#### Seçenek C: Google Colab
`colab_regime_detector.ipynb` dosyasını Google Colab'da açın ve hücreleri çalıştırın.

### 4. Proje Yapısı

```
turkish-market-regime-detector/
├── src/                          # Ana paket
│   ├── __init__.py              # Paket başlatma + geriye dönük uyumluluk
│   ├── config/                  # Konfigürasyon
│   │   ├── constants.py         # REGIME_LABELS, TCMB_POLICY_DECISIONS
│   │   └── settings.py         # Settings veri sınıfı
│   ├── data/                    # Veri alma ve işleme
│   │   ├── yfinance_fetcher.py # Yahoo Finance veri çekici
│   │   ├── evds_fetcher.py     # TCMB EVDS veri çekici
│   │   └── processor.py        # Özellik mühendisliği
│   ├── models/                  # ML modelleri
│   │   ├── base.py             # Temel model sınıfı
│   │   ├── kmeans_model.py     # K-Means kümeleme
│   │   └── hmm_model.py        # Gizli Markov Modeli
│   ├── visualization/           # Görselleştirme
│   │   ├── plots.py            # Plotly grafikleri
│   │   └── export.py           # Dışa aktarma araçları
│   └── backtesting/             # Geriye test (opsiyonel)
│       ├── engine.py           # Geriye test motoru
│       └── strategies.py       # Ticaret stratejileri
├── tests/
│   └── test_suite.py           # Birim testleri
├── colab_regime_detector.ipynb # Google Colab notebook
├── regime_detector.py          # Eski kod (geriye dönük uyumlu)
├── requirements.txt            # Bağımlılıklar
└── README.md                   # Bu dosya
```

### 5. Testleri Çalıştırma

```bash
# Tüm testleri çalıştır
python -m pytest tests/ -v

# Belirli test sınıfını çalıştır
python -m pytest tests/test_suite.py::TestKMeansModel -v

# Coverage ile çalıştır
python -m pytest tests/ --cov=src
```

Test Sonuçları: **43 geçti** (tüm testler)

### 6. Kullanım Örnekleri

#### Örnek 1: Temel Rejim Tespiti
```python
import pandas as pd
from src.data.yfinance_fetcher import YFinanceFetcher
from src.data.processor import DataProcessor
from src.models.kmeans_model import KMeansRegimeModel

# 1. Veri çek
fetcher = YFinanceFetcher(period="2y")
prices = fetcher.fetch_multiple_tickers(["THYAO.IS", "GARAN.IS"])

# 2. Özellikler oluştur
processor = DataProcessor()
features = processor.create_features(prices)
features_norm = processor.normalize_features(features)

# 3. Model eğit
model = KMeansRegimeModel(n_regimes=3, random_state=42)
model.fit(features_norm)

# 4. Tahmin yap
regimes = model.predict(features_norm)
print(f"Rejimler: {regimes[:10]}")
```

#### Örnek 2: Geriye Test
```python
from src.backtesting.engine import run_backtest

# Rejim stratejisi ile geriye test çalıştır
result = run_backtest(prices, regimes, strategy="regime")
print(f"Toplam Getiri: {result.total_return:.2%}")
print(f"Sharpe Oranı: {result.sharpe_ratio:.2f}")
```

#### Örnek 3: Görselleştirme
```python
from src.visualization.plots import RegimePlotter

plotter = RegimePlotter()
fig = plotter.plot_prices_with_regimes(prices, regimes)
fig.show()  # İnteraktif grafik açar
```

### 7. Ortam Değişkenleri

TCMB EVDS verileri için (opsiyonel):
```bash
export EVDS_API_KEY="api_anahtarınız"
```

Veya Python'da:
```python
import os
os.environ["EVDS_API_KEY"] = "api_anahtarınız"
```

---

## 📊 API Reference / API Referansı

### Main Functions / Ana Fonksiyonlar

| Function | Description | Açıklama |
|----------|-------------|-----------|
| `run_analysis()` | Run full analysis | Tam analiz çalıştır |
| `YFinanceFetcher` | Fetch Yahoo Finance data | Yahoo Finance verisi çek |
| `DataProcessor` | Create technical features | Teknik özellikler oluştur |
| `KMeansRegimeModel` | K-Means clustering | K-Means kümeleme |
| `HMMRegimeModel` | Hidden Markov Model | Gizli Markov Modeli |
| `RegimePlotter` | Create visualizations | Görselleştirme oluştur |
| `run_backtest()` | Run backtesting | Geriye test çalıştır |

---

## ⚠️ Troubleshooting / Sorun Giderme

### Common Issues / Yaygın Sorunlar

1. **hmmlearn not found**
   ```bash
   pip install hmmlearn
   ```

2. **Yahoo Finance rate limit**
   - Add delays between requests
   - Use fewer tickers

3. **Module not found**
   ```bash
   # Add project to Python path
   export PYTHONPATH="${PYTHONPATH}:$(pwd)"
   ```

---

## 📝 License

MIT License - See LICENSE file for details.

---

**Happy Trading! / İyi Ticaretler! 🎯**
