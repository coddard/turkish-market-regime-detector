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
