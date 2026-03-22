# BIST100 Regime Detector Edge Case Test Report

**Generated:** 2026-03-22 19:36:30
**Total Tests:** 10
**Passed:** 2
**Failed:** 8
**Success Rate:** 20.0%

## Test Results

### yfinance Version Check

Status: ✅ PASSED
Duration: 0.00s
Result: {'version': '1.2.0', 'expected': '1.2.0', 'match': True}

---

### Insufficient Data (1 Year)

Status: ❌ FAILED
Duration: 0.00s

#### Error Details
```
Eğitim için yeterli veri noktası bulunamadı.
```

#### Stack Trace
```
Traceback (most recent call last):
  File "/Users/mustafasahin/Documents/MY-ALL-IMPORTANT-PROJECTS/turkish-market-regime-detector/edge_case_tests.py", line 25, in run_test
    result = test_function(**kwargs)
  File "/Users/mustafasahin/Documents/MY-ALL-IMPORTANT-PROJECTS/turkish-market-regime-detector/regime_detector.py", line 1028, in run_analysis
    kmeans, scaler, features_list, kmeans_regimes = train_kmeans(features)
                                                    ~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/mustafasahin/Documents/MY-ALL-IMPORTANT-PROJECTS/turkish-market-regime-detector/regime_detector.py", line 423, in train_kmeans
    raise ValueError("Eğitim için yeterli veri noktası bulunamadı.")
ValueError: Eğitim için yeterli veri noktası bulunamadı.

```

---

### Feature Engineering (Minimum Data)

Status: ❌ FAILED
Duration: 0.00s

#### Error Details
```
Eğitim için yeterli veri noktası bulunamadı.
```

#### Stack Trace
```
Traceback (most recent call last):
  File "/Users/mustafasahin/Documents/MY-ALL-IMPORTANT-PROJECTS/turkish-market-regime-detector/edge_case_tests.py", line 25, in run_test
    result = test_function(**kwargs)
  File "/Users/mustafasahin/Documents/MY-ALL-IMPORTANT-PROJECTS/turkish-market-regime-detector/regime_detector.py", line 1028, in run_analysis
    kmeans, scaler, features_list, kmeans_regimes = train_kmeans(features)
                                                    ~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/mustafasahin/Documents/MY-ALL-IMPORTANT-PROJECTS/turkish-market-regime-detector/regime_detector.py", line 423, in train_kmeans
    raise ValueError("Eğitim için yeterli veri noktası bulunamadı.")
ValueError: Eğitim için yeterli veri noktası bulunamadı.

```

---

### Invalid Period (0 Days)

Status: ❌ FAILED
Duration: 0.00s

#### Error Details
```
Geçersiz dönem formatı: '0d'. Geçerli formatlar: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max veya sayı+d (örn: 180d)
```

#### Stack Trace
```
Traceback (most recent call last):
  File "/Users/mustafasahin/Documents/MY-ALL-IMPORTANT-PROJECTS/turkish-market-regime-detector/edge_case_tests.py", line 25, in run_test
    result = test_function(**kwargs)
  File "/Users/mustafasahin/Documents/MY-ALL-IMPORTANT-PROJECTS/turkish-market-regime-detector/regime_detector.py", line 992, in run_analysis
    raise ValueError(f"Geçersiz dönem formatı: '{period}'. Geçerli formatlar: {', '.join(valid_periods)} veya sayı+d (örn: 180d)")
ValueError: Geçersiz dönem formatı: '0d'. Geçerli formatlar: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max veya sayı+d (örn: 180d)

```

---

### Small Custom Period (180 Days)

Status: ❌ FAILED
Duration: 0.00s

#### Error Details
```
Eğitim için yeterli veri noktası bulunamadı.
```

#### Stack Trace
```
Traceback (most recent call last):
  File "/Users/mustafasahin/Documents/MY-ALL-IMPORTANT-PROJECTS/turkish-market-regime-detector/edge_case_tests.py", line 25, in run_test
    result = test_function(**kwargs)
  File "/Users/mustafasahin/Documents/MY-ALL-IMPORTANT-PROJECTS/turkish-market-regime-detector/regime_detector.py", line 1028, in run_analysis
    kmeans, scaler, features_list, kmeans_regimes = train_kmeans(features)
                                                    ~~~~~~~~~~~~^^^^^^^^^^
  File "/Users/mustafasahin/Documents/MY-ALL-IMPORTANT-PROJECTS/turkish-market-regime-detector/regime_detector.py", line 423, in train_kmeans
    raise ValueError("Eğitim için yeterli veri noktası bulunamadı.")
ValueError: Eğitim için yeterli veri noktası bulunamadı.

```

---

### Long Period Analysis (10 Years)

Status: ✅ PASSED
Duration: 12.16s
Result: {'features':               bist_close   banka_close  ...  rate_momentum  real_return
Date                                    ...                            
2020-04-17    981.792786   1222.409058  ...          -2.25     2.005939
2020-04-20    989.453735   1224.297974  ...          -2.25     0.780302
2020-04-21    976.184814   1199.797974  ...          -2.25    -1.341035
2020-04-22    981.704834   1194.634033  ...          -2.25     0.565469
2020-04-24    987.584778   1204.390991  ...          -3.75    15.983568
...                  ...           ...  ...            ...          ...
2026-03-13  13092.900391  16664.500000  ...           0.00    -1.454145
2026-03-16  12956.700195  16675.199219  ...           0.00    -1.040260
2026-03-17  13217.599609  17203.800781  ...           0.00     2.013625
2026-03-18  13115.099609  17005.599609  ...           0.00    -0.775481
2026-03-19  13047.719727  16693.039062  ...           0.00    -0.513758

[1424 rows x 20 columns], 'kmeans': {'model': KMeans(n_clusters=3, n_init=10, random_state=42), 'regimes': Date
2020-04-17    Stagflation Sideways
2020-04-20    Stagflation Sideways
2020-04-21    Stagflation Sideways
2020-04-22    Stagflation Sideways
2020-04-24    Stagflation Sideways
                      ...         
2026-03-13            Carry Unwind
2026-03-16            Carry Unwind
2026-03-17            Carry Unwind
2026-03-18            Carry Unwind
2026-03-19            Carry Unwind
Name: kmeans_regime, Length: 1424, dtype: object}, 'hmm': {'model': GaussianHMM(covariance_type='full', n_components=3, n_iter=1000,
            random_state=42), 'regimes': Date
2020-04-17    Stagflation Sideways
2020-04-20    Stagflation Sideways
2020-04-21    Stagflation Sideways
2020-04-22    Stagflation Sideways
2020-04-24            Carry Unwind
                      ...         
2026-03-13    Stagflation Sideways
2026-03-16    Stagflation Sideways
2026-03-17    Stagflation Sideways
2026-03-18    Stagflation Sideways
2026-03-19    Stagflation Sideways
Name: hmm_regime, Length: 1424, dtype: object}, 'policy_analysis':          date  policy_rate  ...  after_Carry Unwind after_Stagflation Sideways
0  2020-04-23         8.25  ...            0.333333                   0.666667
1  2020-06-18         8.25  ...                 NaN                   1.000000
2  2020-07-23         8.25  ...                 NaN                   1.000000
3  2020-08-27         8.25  ...                 NaN                   1.000000
4  2020-09-24         8.25  ...                 NaN                   1.000000
5  2020-10-22         8.25  ...                 NaN                   1.000000
6  2020-11-19         8.25  ...                 NaN                   1.000000
7  2020-12-17         8.25  ...                 NaN                   1.000000
8  2021-03-18        19.00  ...                 NaN                   1.000000
9  2021-04-15        19.00  ...                 NaN                   1.000000
10 2021-06-17        19.00  ...                 NaN                   1.000000
11 2021-08-19        19.00  ...                 NaN                   1.000000
12 2021-09-23        18.00  ...                 NaN                   1.000000
13 2021-10-21        16.00  ...                 NaN                   0.666667
14 2021-11-18        15.00  ...                 NaN                        NaN
15 2021-12-16        14.00  ...                 NaN                        NaN
16 2022-03-17        14.00  ...                 NaN                   1.000000
17 2022-07-21        14.00  ...                 NaN                   1.000000
18 2022-09-22        14.00  ...                 NaN                   1.000000
19 2022-10-27        15.00  ...                 NaN                   1.000000
20 2022-11-24        24.00  ...            0.333333                   0.666667
21 2023-03-23         8.50  ...            1.000000                        NaN
22 2023-07-20        15.00  ...                 NaN                   1.000000
23 2023-08-24        25.00  ...                 NaN                   1.000000
24 2023-09-21        30.00  ...                 NaN                   1.000000
25 2023-10-26        35.00  ...                 NaN                   1.000000
26 2023-11-23        40.00  ...            0.333333                   0.666667
27 2024-03-21        42.50  ...                 NaN                   1.000000
28 2024-08-22        30.00  ...                 NaN                   1.000000
29 2024-09-19        27.50  ...                 NaN                   1.000000
30 2024-11-21        22.50  ...                 NaN                   1.000000
31 2024-12-19        20.00  ...                 NaN                   1.000000

[32 rows x 13 columns], 'current_regime': {'date': '2026-03-19', 'regime': 'Stagflation Sideways', 'duration_days': 283, 'transition_probabilities': {'Risk-On': 0.0025917297750353294, 'Stagflation Sideways': 0.9764372193500304, 'Carry Unwind': 0.020971050874934432}, 'last_policy': date           2025-01-16 00:00:00
policy_rate                   17.5
change_bps                    -250
Name: 60, dtype: object}, 'visualizations': {'main_plot': Figure({
    'data': [{'line': {'color': '#1f2937', 'width': 2},
              'mode': 'lines',
              'name': 'BIST100',
              'type': 'scatter',
              'x': array(['2020-04-17T00:00:00.000000000', '2020-04-20T00:00:00.000000000',
                          '2020-04-21T00:00:00.000000000', ..., '2026-03-17T00:00:00.000000000',
                          '2026-03-18T00:00:00.000000000', '2026-03-19T00:00:00.000000000'],
                         dtype='datetime64[ns]'),
              'y': {'bdata': ('AAAAoFeujkAAAABAoeuOQAAAAIB6gY' ... 'DM0MlAAAAAwIydyUAAAAAg3HvJQA=='),
                    'dtype': 'f8'}},
             {'fill': 'tozeroy',
              'fillcolor': '#10b981',
              'line': {'width': 0},
              'mode': 'lines',
              'name': 'Risk-On',
              'opacity': 0.2,
              'type': 'scatter',
              'x': array(['2020-11-10T00:00:00.000000000', '2020-11-11T00:00:00.000000000',
                          '2020-11-12T00:00:00.000000000', '2021-10-22T00:00:00.000000000',
                          '2021-11-17T00:00:00.000000000', '2021-11-18T00:00:00.000000000',
                          '2021-11-19T00:00:00.000000000', '2021-11-22T00:00:00.000000000',
                          '2021-11-23T00:00:00.000000000', '2021-11-24T00:00:00.000000000',
                          '2021-11-26T00:00:00.000000000', '2021-11-29T00:00:00.000000000',
                          '2021-11-30T00:00:00.000000000', '2021-12-01T00:00:00.000000000',
                          '2021-12-02T00:00:00.000000000', '2021-12-03T00:00:00.000000000',
                          '2021-12-06T00:00:00.000000000', '2021-12-07T00:00:00.000000000',
                          '2021-12-08T00:00:00.000000000', '2021-12-09T00:00:00.000000000',
                          '2021-12-10T00:00:00.000000000', '2021-12-13T00:00:00.000000000',
                          '2021-12-14T00:00:00.000000000', '2021-12-15T00:00:00.000000000',
                          '2021-12-16T00:00:00.000000000', '2021-12-17T00:00:00.000000000',
                          '2021-12-20T00:00:00.000000000', '2021-12-21T00:00:00.000000000',
                          '2021-12-22T00:00:00.000000000', '2021-12-23T00:00:00.000000000',
                          '2021-12-27T00:00:00.000000000', '2021-12-28T00:00:00.000000000',
                          '2021-12-29T00:00:00.000000000', '2021-12-30T00:00:00.000000000',
                          '2021-12-31T00:00:00.000000000', '2022-01-03T00:00:00.000000000',
                          '2022-01-04T00:00:00.000000000', '2022-01-05T00:00:00.000000000',
                          '2022-01-06T00:00:00.000000000', '2022-01-07T00:00:00.000000000',
                          '2022-01-10T00:00:00.000000000', '2022-01-11T00:00:00.000000000',
                          '2022-01-12T00:00:00.000000000', '2022-01-13T00:00:00.000000000',
                          '2022-01-14T00:00:00.000000000', '2022-01-18T00:00:00.000000000',
                          '2022-01-19T00:00:00.000000000', '2022-01-20T00:00:00.000000000',
                          '2022-01-21T00:00:00.000000000', '2022-01-24T00:00:00.000000000',
                          '2022-01-25T00:00:00.000000000', '2023-05-30T00:00:00.000000000',
                          '2023-05-31T00:00:00.000000000', '2023-06-01T00:00:00.000000000',
                          '2023-06-02T00:00:00.000000000', '2023-06-05T00:00:00.000000000',
                          '2023-06-06T00:00:00.000000000', '2023-06-07T00:00:00.000000000',
                          '2023-06-08T00:00:00.000000000', '2023-06-09T00:00:00.000000000',
                          '2023-06-12T00:00:00.000000000', '2023-06-13T00:00:00.000000000',
                          '2023-06-14T00:00:00.000000000', '2023-06-15T00:00:00.000000000',
                          '2023-06-16T00:00:00.000000000', '2023-06-20T00:00:00.000000000',
                          '2023-06-21T00:00:00.000000000', '2023-06-22T00:00:00.000000000',
                          '2023-06-23T00:00:00.000000000', '2023-06-26T00:00:00.000000000',
                          '2023-06-27T00:00:00.000000000', '2023-07-03T00:00:00.000000000',
                          '2023-07-05T00:00:00.000000000'], dtype='datetime64[ns]'),
              'y': [0, 14259.900390625]},
             {'fill': 'tozeroy',
              'fillcolor': '#ef4444',
              'line': {'width': 0},
              'mode': 'lines',
              'name': 'Carry Unwind',
              'opacity': 0.2,
              'type': 'scatter',
              'x': array(['2020-04-24T00:00:00.000000000', '2021-01-21T00:00:00.000000000',
                          '2021-03-18T00:00:00.000000000', '2021-09-23T00:00:00.000000000',
                          '2021-10-21T00:00:00.000000000', '2022-10-27T00:00:00.000000000',
                          '2022-11-25T00:00:00.000000000', '2022-12-22T00:00:00.000000000',
                          '2022-12-23T00:00:00.000000000', '2022-12-27T00:00:00.000000000',
                          '2022-12-28T00:00:00.000000000', '2022-12-29T00:00:00.000000000',
                          '2022-12-30T00:00:00.000000000', '2023-01-03T00:00:00.000000000',
                          '2023-01-04T00:00:00.000000000', '2023-01-05T00:00:00.000000000',
                          '2023-01-06T00:00:00.000000000', '2023-01-09T00:00:00.000000000',
                          '2023-01-10T00:00:00.000000000', '2023-01-11T00:00:00.000000000',
                          '2023-01-12T00:00:00.000000000', '2023-01-13T00:00:00.000000000',
                          '2023-01-17T00:00:00.000000000', '2023-01-18T00:00:00.000000000',
                          '2023-01-19T00:00:00.000000000', '2023-01-20T00:00:00.000000000',
                          '2023-01-23T00:00:00.000000000', '2023-01-24T00:00:00.000000000',
                          '2023-01-25T00:00:00.000000000', '2023-01-26T00:00:00.000000000',
                          '2023-01-27T00:00:00.000000000', '2023-01-30T00:00:00.000000000',
                          '2023-01-31T00:00:00.000000000', '2023-02-01T00:00:00.000000000',
                          '2023-02-02T00:00:00.000000000', '2023-02-03T00:00:00.000000000',
                          '2023-02-06T00:00:00.000000000', '2023-02-07T00:00:00.000000000',
                          '2023-02-08T00:00:00.000000000', '2023-02-15T00:00:00.000000000',
                          '2023-02-16T00:00:00.000000000', '2023-02-17T00:00:00.000000000',
                          '2023-02-21T00:00:00.000000000', '2023-02-22T00:00:00.000000000',
                          '2023-02-23T00:00:00.000000000', '2023-02-24T00:00:00.000000000',
                          '2023-02-27T00:00:00.000000000', '2023-02-28T00:00:00.000000000',
                          '2023-03-01T00:00:00.000000000', '2023-03-02T00:00:00.000000000',
                          '2023-03-03T00:00:00.000000000', '2023-03-06T00:00:00.000000000',
                          '2023-03-07T00:00:00.000000000', '2023-03-08T00:00:00.000000000',
                          '2023-03-09T00:00:00.000000000', '2023-03-10T00:00:00.000000000',
                          '2023-03-13T00:00:00.000000000', '2023-03-14T00:00:00.000000000',
                          '2023-03-15T00:00:00.000000000', '2023-03-16T00:00:00.000000000',
                          '2023-03-17T00:00:00.000000000', '2023-03-20T00:00:00.000000000',
                          '2023-03-21T00:00:00.000000000', '2023-03-22T00:00:00.000000000',
                          '2023-03-23T00:00:00.000000000', '2023-03-24T00:00:00.000000000',
                          '2023-03-27T00:00:00.000000000', '2023-03-28T00:00:00.000000000',
                          '2023-03-29T00:00:00.000000000', '2023-03-30T00:00:00.000000000',
                          '2023-07-20T00:00:00.000000000', '2023-08-24T00:00:00.000000000',
                          '2023-09-21T00:00:00.000000000', '2023-10-26T00:00:00.000000000',
                          '2023-11-24T00:00:00.000000000', '2023-12-21T00:00:00.000000000',
                          '2024-01-18T00:00:00.000000000', '2024-03-21T00:00:00.000000000',
                          '2024-04-18T00:00:00.000000000', '2024-05-23T00:00:00.000000000',
                          '2024-06-20T00:00:00.000000000', '2024-07-18T00:00:00.000000000',
                          '2024-08-22T00:00:00.000000000', '2024-09-19T00:00:00.000000000',
                          '2024-10-24T00:00:00.000000000', '2024-11-21T00:00:00.000000000',
                          '2024-12-19T00:00:00.000000000', '2025-01-16T00:00:00.000000000'],
                         dtype='datetime64[ns]'),
              'y': [0, 14259.900390625]},
             {'fill': 'tozeroy',
              'fillcolor': '#3b82f6',
              'line': {'width': 0},
              'mode': 'lines',
              'name': 'Stagflation Sideways',
              'opacity': 0.2,
              'type': 'scatter',
              'x': array(['2020-04-17T00:00:00.000000000', '2020-04-20T00:00:00.000000000',
                          '2020-04-21T00:00:00.000000000', ..., '2026-03-17T00:00:00.000000000',
                          '2026-03-18T00:00:00.000000000', '2026-03-19T00:00:00.000000000'],
                         dtype='datetime64[ns]'),
              'y': [0, 14259.900390625]}],
    'layout': {'annotations': [{'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2020-04-23: 8.25% (-150bps)',
                                'x': Timestamp('2020-04-23 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2020-05-21: 8.25% (+0bps)',
                                'x': Timestamp('2020-05-21 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2020-06-18: 8.25% (+0bps)',
                                'x': Timestamp('2020-06-18 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2020-07-23: 8.25% (+0bps)',
                                'x': Timestamp('2020-07-23 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2020-08-27: 8.25% (+0bps)',
                                'x': Timestamp('2020-08-27 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2020-09-24: 8.25% (+0bps)',
                                'x': Timestamp('2020-09-24 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2020-10-22: 8.25% (+0bps)',
                                'x': Timestamp('2020-10-22 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2020-11-19: 8.25% (+0bps)',
                                'x': Timestamp('2020-11-19 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2020-12-17: 8.25% (+0bps)',
                                'x': Timestamp('2020-12-17 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2021-01-21: 17.00% (+875bps)',
                                'x': Timestamp('2021-01-21 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2021-02-18: 17.00% (+0bps)',
                                'x': Timestamp('2021-02-18 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2021-03-18: 19.00% (+200bps)',
                                'x': Timestamp('2021-03-18 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2021-04-15: 19.00% (+0bps)',
                                'x': Timestamp('2021-04-15 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2021-05-13: 19.00% (+0bps)',
                                'x': Timestamp('2021-05-13 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2021-06-17: 19.00% (+0bps)',
                                'x': Timestamp('2021-06-17 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2021-07-22: 19.00% (+0bps)',
                                'x': Timestamp('2021-07-22 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2021-08-19: 19.00% (+0bps)',
                                'x': Timestamp('2021-08-19 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2021-09-23: 18.00% (-100bps)',
                                'x': Timestamp('2021-09-23 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2021-10-21: 16.00% (-200bps)',
                                'x': Timestamp('2021-10-21 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2021-11-18: 15.00% (-100bps)',
                                'x': Timestamp('2021-11-18 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2021-12-16: 14.00% (-100bps)',
                                'x': Timestamp('2021-12-16 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2022-01-20: 14.00% (+0bps)',
                                'x': Timestamp('2022-01-20 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2022-02-17: 14.00% (+0bps)',
                                'x': Timestamp('2022-02-17 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2022-03-17: 14.00% (+0bps)',
                                'x': Timestamp('2022-03-17 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2022-04-14: 14.00% (+0bps)',
                                'x': Timestamp('2022-04-14 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2022-05-26: 14.00% (+0bps)',
                                'x': Timestamp('2022-05-26 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2022-06-23: 14.00% (+0bps)',
                                'x': Timestamp('2022-06-23 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2022-07-21: 14.00% (+0bps)',
                                'x': Timestamp('2022-07-21 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2022-08-25: 14.00% (+0bps)',
                                'x': Timestamp('2022-08-25 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2022-09-22: 14.00% (+0bps)',
                                'x': Timestamp('2022-09-22 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2022-10-27: 15.00% (+100bps)',
                                'x': Timestamp('2022-10-27 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2022-11-24: 24.00% (+900bps)',
                                'x': Timestamp('2022-11-24 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2022-12-22: 9.00% (-1500bps)',
                                'x': Timestamp('2022-12-22 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2023-01-19: 9.00% (+0bps)',
                                'x': Timestamp('2023-01-19 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2023-02-23: 9.00% (+0bps)',
                                'x': Timestamp('2023-02-23 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2023-03-23: 8.50% (-50bps)',
                                'x': Timestamp('2023-03-23 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2023-04-27: 8.50% (+0bps)',
                                'x': Timestamp('2023-04-27 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2023-05-25: 8.50% (+0bps)',
                                'x': Timestamp('2023-05-25 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2023-06-22: 8.50% (+0bps)',
                                'x': Timestamp('2023-06-22 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2023-07-20: 15.00% (+650bps)',
                                'x': Timestamp('2023-07-20 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2023-08-24: 25.00% (+1000bps)',
                                'x': Timestamp('2023-08-24 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2023-09-21: 30.00% (+500bps)',
                                'x': Timestamp('2023-09-21 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2023-10-26: 35.00% (+500bps)',
                                'x': Timestamp('2023-10-26 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2023-11-23: 40.00% (+500bps)',
                                'x': Timestamp('2023-11-23 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2023-12-21: 42.50% (+250bps)',
                                'x': Timestamp('2023-12-21 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2024-01-18: 45.00% (+250bps)',
                                'x': Timestamp('2024-01-18 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2024-02-15: 45.00% (+0bps)',
                                'x': Timestamp('2024-02-15 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2024-03-21: 42.50% (-250bps)',
                                'x': Timestamp('2024-03-21 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2024-04-18: 40.00% (-250bps)',
                                'x': Timestamp('2024-04-18 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2024-05-23: 37.50% (-250bps)',
                                'x': Timestamp('2024-05-23 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2024-06-20: 35.00% (-250bps)',
                                'x': Timestamp('2024-06-20 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2024-07-18: 32.50% (-250bps)',
                                'x': Timestamp('2024-07-18 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2024-08-22: 30.00% (-250bps)',
                                'x': Timestamp('2024-08-22 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2024-09-19: 27.50% (-250bps)',
                                'x': Timestamp('2024-09-19 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2024-10-24: 25.00% (-250bps)',
                                'x': Timestamp('2024-10-24 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2024-11-21: 22.50% (-250bps)',
                                'x': Timestamp('2024-11-21 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2024-12-19: 20.00% (-250bps)',
                                'x': Timestamp('2024-12-19 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'},
                               {'arrowhead': 2,
                                'font': {'size': 10},
                                'showarrow': True,
                                'text': '2025-01-16: 17.50% (-250bps)',
                                'x': Timestamp('2025-01-16 00:00:00'),
                                'y': 14259.900390625,
                                'yanchor': 'bottom'}],
               'height': 700,
               'hovermode': 'x unified',
               'legend': {'title': {'text': 'Rejimler'}},
               'shapes': [{'line': {'color': '#10b981', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2020-04-23 00:00:00'),
                           'x1': Timestamp('2020-04-23 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#6b7280', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2020-05-21 00:00:00'),
                           'x1': Timestamp('2020-05-21 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#6b7280', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2020-06-18 00:00:00'),
                           'x1': Timestamp('2020-06-18 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#6b7280', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2020-07-23 00:00:00'),
                           'x1': Timestamp('2020-07-23 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#6b7280', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2020-08-27 00:00:00'),
                           'x1': Timestamp('2020-08-27 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#6b7280', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2020-09-24 00:00:00'),
                           'x1': Timestamp('2020-09-24 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#6b7280', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2020-10-22 00:00:00'),
                           'x1': Timestamp('2020-10-22 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#6b7280', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2020-11-19 00:00:00'),
                           'x1': Timestamp('2020-11-19 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#6b7280', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2020-12-17 00:00:00'),
                           'x1': Timestamp('2020-12-17 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#ef4444', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2021-01-21 00:00:00'),
                           'x1': Timestamp('2021-01-21 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#6b7280', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2021-02-18 00:00:00'),
                           'x1': Timestamp('2021-02-18 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#ef4444', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2021-03-18 00:00:00'),
                           'x1': Timestamp('2021-03-18 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#6b7280', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2021-04-15 00:00:00'),
                           'x1': Timestamp('2021-04-15 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#6b7280', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2021-05-13 00:00:00'),
                           'x1': Timestamp('2021-05-13 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#6b7280', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2021-06-17 00:00:00'),
                           'x1': Timestamp('2021-06-17 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#6b7280', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2021-07-22 00:00:00'),
                           'x1': Timestamp('2021-07-22 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#6b7280', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2021-08-19 00:00:00'),
                           'x1': Timestamp('2021-08-19 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#10b981', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2021-09-23 00:00:00'),
                           'x1': Timestamp('2021-09-23 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#10b981', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2021-10-21 00:00:00'),
                           'x1': Timestamp('2021-10-21 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#10b981', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2021-11-18 00:00:00'),
                           'x1': Timestamp('2021-11-18 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#10b981', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2021-12-16 00:00:00'),
                           'x1': Timestamp('2021-12-16 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#6b7280', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2022-01-20 00:00:00'),
                           'x1': Timestamp('2022-01-20 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#6b7280', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2022-02-17 00:00:00'),
                           'x1': Timestamp('2022-02-17 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#6b7280', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2022-03-17 00:00:00'),
                           'x1': Timestamp('2022-03-17 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#6b7280', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2022-04-14 00:00:00'),
                           'x1': Timestamp('2022-04-14 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#6b7280', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2022-05-26 00:00:00'),
                           'x1': Timestamp('2022-05-26 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#6b7280', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2022-06-23 00:00:00'),
                           'x1': Timestamp('2022-06-23 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#6b7280', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2022-07-21 00:00:00'),
                           'x1': Timestamp('2022-07-21 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#6b7280', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2022-08-25 00:00:00'),
                           'x1': Timestamp('2022-08-25 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#6b7280', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2022-09-22 00:00:00'),
                           'x1': Timestamp('2022-09-22 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#ef4444', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2022-10-27 00:00:00'),
                           'x1': Timestamp('2022-10-27 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#ef4444', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2022-11-24 00:00:00'),
                           'x1': Timestamp('2022-11-24 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#10b981', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2022-12-22 00:00:00'),
                           'x1': Timestamp('2022-12-22 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#6b7280', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2023-01-19 00:00:00'),
                           'x1': Timestamp('2023-01-19 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#6b7280', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2023-02-23 00:00:00'),
                           'x1': Timestamp('2023-02-23 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#10b981', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2023-03-23 00:00:00'),
                           'x1': Timestamp('2023-03-23 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#6b7280', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2023-04-27 00:00:00'),
                           'x1': Timestamp('2023-04-27 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#6b7280', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2023-05-25 00:00:00'),
                           'x1': Timestamp('2023-05-25 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#6b7280', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2023-06-22 00:00:00'),
                           'x1': Timestamp('2023-06-22 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#ef4444', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2023-07-20 00:00:00'),
                           'x1': Timestamp('2023-07-20 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#ef4444', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2023-08-24 00:00:00'),
                           'x1': Timestamp('2023-08-24 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#ef4444', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2023-09-21 00:00:00'),
                           'x1': Timestamp('2023-09-21 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#ef4444', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2023-10-26 00:00:00'),
                           'x1': Timestamp('2023-10-26 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#ef4444', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2023-11-23 00:00:00'),
                           'x1': Timestamp('2023-11-23 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#ef4444', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2023-12-21 00:00:00'),
                           'x1': Timestamp('2023-12-21 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#ef4444', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2024-01-18 00:00:00'),
                           'x1': Timestamp('2024-01-18 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#6b7280', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2024-02-15 00:00:00'),
                           'x1': Timestamp('2024-02-15 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#10b981', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2024-03-21 00:00:00'),
                           'x1': Timestamp('2024-03-21 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#10b981', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2024-04-18 00:00:00'),
                           'x1': Timestamp('2024-04-18 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#10b981', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2024-05-23 00:00:00'),
                           'x1': Timestamp('2024-05-23 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#10b981', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2024-06-20 00:00:00'),
                           'x1': Timestamp('2024-06-20 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#10b981', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2024-07-18 00:00:00'),
                           'x1': Timestamp('2024-07-18 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#10b981', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2024-08-22 00:00:00'),
                           'x1': Timestamp('2024-08-22 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#10b981', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2024-09-19 00:00:00'),
                           'x1': Timestamp('2024-09-19 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#10b981', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2024-10-24 00:00:00'),
                           'x1': Timestamp('2024-10-24 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#10b981', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2024-11-21 00:00:00'),
                           'x1': Timestamp('2024-11-21 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#10b981', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2024-12-19 00:00:00'),
                           'x1': Timestamp('2024-12-19 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'},
                          {'line': {'color': '#10b981', 'dash': 'dot', 'width': 2},
                           'type': 'line',
                           'x0': Timestamp('2025-01-16 00:00:00'),
                           'x1': Timestamp('2025-01-16 00:00:00'),
                           'xref': 'x',
                           'y0': 0,
                           'y1': 1,
                           'yref': 'y domain'}],
               'template': '...',
               'title': {'text': 'BIST100 Rejim Tespiti'},
               'xaxis': {'title': {'text': 'Tarih'}},
               'yaxis': {'title': {'text': 'Fiyat (TL)'}}}
}), 'stats_heatmap': Figure({
    'data': [{'coloraxis': 'coloraxis',
              'hovertemplate': 'x: %{x}<br>hmm_regime: %{y}<br>Değer: %{z}<extra></extra>',
              'name': '0',
              'type': 'heatmap',
              'x': array(['bist_return', 'bist_volatility', 'usdtry_change', 'rsi', 'ma_ratio',
                          'days_count', 'days_pct', 'sharpe_ratio'], dtype=object),
              'xaxis': 'x',
              'y': array(['Carry Unwind', 'Risk-On', 'Stagflation Sideways'], dtype=object),
              'yaxis': 'y',
              'z': {'bdata': ('ukkMAisHP0B56SYxCExEQPyp8dJNYp' ... 'AAAAC8k0Aj2/l+aixWQC2yne+nxvs/'),
                    'dtype': 'f8',
                    'shape': '3, 8'}}],
    'layout': {'coloraxis': {'colorbar': {'title': {'text': 'Değer'}},
                             'colorscale': [[0.0, '#440154'], [0.1111111111111111,
                                            '#482878'], [0.2222222222222222,
                                            '#3e4989'], [0.3333333333333333,
                                            '#31688e'], [0.4444444444444444,
                                            '#26828e'], [0.5555555555555556,
                                            '#1f9e89'], [0.6666666666666666,
                                            '#35b779'], [0.7777777777777778,
                                            '#6ece58'], [0.8888888888888888,
                                            '#b5de2b'], [1.0, '#fde725']]},
               'height': 600,
               'margin': {'t': 60},
               'template': '...',
               'title': {'text': 'Rejim Bazlı İstatistikler'},
               'xaxis': {'anchor': 'y', 'constrain': 'domain', 'domain': [0.0, 1.0], 'scaleanchor': 'y', 'tickangle': 45},
               'yaxis': {'anchor': 'x',
                         'autorange': 'reversed',
                         'constrain': 'domain',
                         'domain': [0.0, 1.0],
                         'title': {'text': 'hmm_regime'}}}
}), 'transition_matrix': Figure({
    'data': [{'coloraxis': 'coloraxis',
              'hovertemplate': 'x: %{x}<br>y: %{y}<br>Olasılık: %{z}<extra></extra>',
              'name': '0',
              'texttemplate': '%{z:.2%}',
              'type': 'heatmap',
              'x': array(['State 0 (Risk-On)', 'State 1 (Stagflation Sideways)',
                          'State 2 (Carry Unwind)'], dtype=object),
              'xaxis': 'x',
              'y': array(['State 0 (Risk-On)', 'State 1 (Stagflation Sideways)',
                          'State 2 (Carry Unwind)'], dtype=object),
              'yaxis': 'y',
              'z': {'bdata': ('uZ6Dz0Uy7j99FMYHo9usP+PxrrwnXI' ... 'ftpSKmgz9xYg2vxrfSP+mZ4R2EVeY/'),
                    'dtype': 'f8',
                    'shape': '3, 3'}}],
    'layout': {'coloraxis': {'colorbar': {'title': {'text': 'Olasılık'}},
                             'colorscale': [[0.0, 'rgb(247,251,255)'], [0.125,
                                            'rgb(222,235,247)'], [0.25,
                                            'rgb(198,219,239)'], [0.375,
                                            'rgb(158,202,225)'], [0.5,
                                            'rgb(107,174,214)'], [0.625,
                                            'rgb(66,146,198)'], [0.75,
                                            'rgb(33,113,181)'], [0.875,
                                            'rgb(8,81,156)'], [1.0,
                                            'rgb(8,48,107)']]},
               'height': 600,
               'margin': {'t': 60},
               'template': '...',
               'title': {'text': 'Rejim Geçiş Matrisi (HMM)'},
               'xaxis': {'anchor': 'y', 'constrain': 'domain', 'domain': [0.0, 1.0], 'scaleanchor': 'y', 'tickangle': 45},
               'yaxis': {'anchor': 'x', 'autorange': 'reversed', 'constrain': 'domain', 'domain': [0.0, 1.0]}}
}), 'sector_performance': Figure({
    'data': [{'name': 'BIST100',
              'type': 'bar',
              'x': array(['Carry Unwind', 'Risk-On', 'Stagflation Sideways'], dtype=object),
              'y': {'bdata': 'mZ4mVRsHP0Cexrwbs/xlQGaskP1lGEZA', 'dtype': 'f8'}},
             {'name': 'BIST Banka',
              'type': 'bar',
              'x': array(['Carry Unwind', 'Risk-On', 'Stagflation Sideways'], dtype=object),
              'y': {'bdata': 'm0wx/YmhTkAQk2DGeMxnQABbRap8kUdA', 'dtype': 'f8'}},
             {'name': 'BIST Sınai',
              'type': 'bar',
              'x': array(['Carry Unwind', 'Risk-On', 'Stagflation Sideways'], dtype=object),
              'y': {'bdata': '5hsD/VvPOUB/3Xc3u/JjQJc0TP1wtkZA', 'dtype': 'f8'}}],
    'layout': {'barmode': 'group',
               'height': 600,
               'template': '...',
               'title': {'text': 'Sektörel Performans (Yıllık Ortalama)'},
               'yaxis': {'title': {'text': 'Yıllık Getiri (%)'}}}
})}}

---

### Invalid Ticker Symbols

Status: ❌ FAILED
Duration: 0.00s

#### Error Details
```
Gerekli hisse senedi verisi bulunamadı: XU100.IS
```

#### Stack Trace
```
Traceback (most recent call last):
  File "/Users/mustafasahin/Documents/MY-ALL-IMPORTANT-PROJECTS/turkish-market-regime-detector/edge_case_tests.py", line 25, in run_test
    result = test_function(**kwargs)
  File "/Users/mustafasahin/Documents/MY-ALL-IMPORTANT-PROJECTS/turkish-market-regime-detector/regime_detector.py", line 1024, in run_analysis
    features = create_features(price_data, policy_data)
  File "/Users/mustafasahin/Documents/MY-ALL-IMPORTANT-PROJECTS/turkish-market-regime-detector/regime_detector.py", line 331, in create_features
    raise ValueError(f"Gerekli hisse senedi verisi bulunamadı: {ticker}")
ValueError: Gerekli hisse senedi verisi bulunamadı: XU100.IS

```

---

### Missing Ticker Data

Status: ❌ FAILED
Duration: 0.00s

#### Error Details
```
Gerekli hisse senedi verisi bulunamadı: XBANK.IS
```

#### Stack Trace
```
Traceback (most recent call last):
  File "/Users/mustafasahin/Documents/MY-ALL-IMPORTANT-PROJECTS/turkish-market-regime-detector/edge_case_tests.py", line 25, in run_test
    result = test_function(**kwargs)
  File "/Users/mustafasahin/Documents/MY-ALL-IMPORTANT-PROJECTS/turkish-market-regime-detector/regime_detector.py", line 1024, in run_analysis
    features = create_features(price_data, policy_data)
  File "/Users/mustafasahin/Documents/MY-ALL-IMPORTANT-PROJECTS/turkish-market-regime-detector/regime_detector.py", line 331, in create_features
    raise ValueError(f"Gerekli hisse senedi verisi bulunamadı: {ticker}")
ValueError: Gerekli hisse senedi verisi bulunamadı: XBANK.IS

```

---

### Single Ticker Analysis

Status: ❌ FAILED
Duration: 0.00s

#### Error Details
```
Gerekli hisse senedi verisi bulunamadı: XBANK.IS
```

#### Stack Trace
```
Traceback (most recent call last):
  File "/Users/mustafasahin/Documents/MY-ALL-IMPORTANT-PROJECTS/turkish-market-regime-detector/edge_case_tests.py", line 25, in run_test
    result = test_function(**kwargs)
  File "/Users/mustafasahin/Documents/MY-ALL-IMPORTANT-PROJECTS/turkish-market-regime-detector/regime_detector.py", line 1024, in run_analysis
    features = create_features(price_data, policy_data)
  File "/Users/mustafasahin/Documents/MY-ALL-IMPORTANT-PROJECTS/turkish-market-regime-detector/regime_detector.py", line 331, in create_features
    raise ValueError(f"Gerekli hisse senedi verisi bulunamadı: {ticker}")
ValueError: Gerekli hisse senedi verisi bulunamadı: XBANK.IS

```

---

### Empty Ticker List

Status: ❌ FAILED
Duration: 0.00s

#### Error Details
```
En az bir hisse senedi sembolü girilmelidir.
```

#### Stack Trace
```
Traceback (most recent call last):
  File "/Users/mustafasahin/Documents/MY-ALL-IMPORTANT-PROJECTS/turkish-market-regime-detector/edge_case_tests.py", line 25, in run_test
    result = test_function(**kwargs)
  File "/Users/mustafasahin/Documents/MY-ALL-IMPORTANT-PROJECTS/turkish-market-regime-detector/regime_detector.py", line 1009, in run_analysis
    raise ValueError("En az bir hisse senedi sembolü girilmelidir.")
ValueError: En az bir hisse senedi sembolü girilmelidir.

```

---

## Summary

⚠️ **8 tests failed!** The following edge cases need attention:

- **Insufficient Data (1 Year)**: Eğitim için yeterli veri noktası bulunamadı.
- **Feature Engineering (Minimum Data)**: Eğitim için yeterli veri noktası bulunamadı.
- **Invalid Period (0 Days)**: Geçersiz dönem formatı: '0d'. Geçerli formatlar: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max veya sayı+d (örn: 180d)
- **Small Custom Period (180 Days)**: Eğitim için yeterli veri noktası bulunamadı.
- **Invalid Ticker Symbols**: Gerekli hisse senedi verisi bulunamadı: XU100.IS
- **Missing Ticker Data**: Gerekli hisse senedi verisi bulunamadı: XBANK.IS
- **Single Ticker Analysis**: Gerekli hisse senedi verisi bulunamadı: XBANK.IS
- **Empty Ticker List**: En az bir hisse senedi sembolü girilmelidir.