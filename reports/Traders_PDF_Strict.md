# Traders PDF-Strict — Reglas EXACTAS de los PDFs

Universo: 14 | trader_setups: 7 | resultados: 54

## Reglas aplicadas

| trader_setup | SL inicial | Partials | Trail | Time-stop | Max hold |
|---|---|---|---|---|---|
| Minervini_VCP | 7.5% fijo | 25%@2R + 25%@4R | SMA10 D1 | – | 60 d |
| Zanger_FLAG | 8% fijo | 50%@+15% | SMA20 D1 | 2 d | 30 d |
| Zanger_CUP | 8% fijo | 50%@+15% | SMA20 D1 | 3 d | 40 d |
| Qulla_HTF | 1×ATR_D1 | 30%@d3 + 20%@d5 | SMA50 D1 | – | 40 d |
| Qulla_EP | 1×ATR_D1 | 30%@d3 + 20%@d5 | SMA50 D1 | – | 40 d |
| Qulla_ORB | **Range Low** | 30%@d3 + 20%@d5 | SMA50 D1 | – | 10 d |
| Ryan_ANTS | 7% fijo | 15%@+22% + 15%@+40% | SMA50 D1 (exit si close<SMA50) | – | 80 d |

## Resultados por (symbol, trader_setup)

| symbol | trader_setup | n_trades | wr | pf | exp_r | max_dd_r | tpy | sum_r | wf_pf_is | wf_pf_oos | wf_deg_wr_pct | mc_ruin_pct | mc_p95_dd | decay_label | robustness | flags |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| XAUUSD | Qulla_ORB | 1442 | 0.148 | 1.553 | 0.577 | 61.180 | 172.900 | 832.150 | 1.573 | 1.533 | 18.640 | 100.000 | 109.270 | ESTABLE | MUERTA | ruin>5%, WF deg WR>15% |
| USDJPY | Qulla_ORB | 1437 | 0.183 | 1.454 | 0.494 | 61.360 | 172.500 | 710.600 | 1.418 | 1.490 | -5.320 | 100.000 | 109.140 | ESTABLE | MUERTA | ruin>5% |
| XAGUSD | Qulla_ORB | 1419 | 0.241 | 1.553 | 0.495 | 41.000 | 170.200 | 703.150 | 1.504 | 1.604 | 1.300 | 99.100 | 72.470 | ESTABLE | MUERTA | ruin>5% |
| BRENT | Qulla_ORB | 1601 | 0.130 | 1.379 | 0.408 | 112.450 | 192.100 | 653.820 | 1.346 | 1.412 | -1.810 | 100.000 | 146.790 | ESTABLE | MUERTA | ruin>5% |
| GBPJPY | Qulla_ORB | 1454 | 0.192 | 1.416 | 0.426 | 69.200 | 174.300 | 618.770 | 1.604 | 1.226 | 0.710 | 100.000 | 105.170 | ESTABLE | MUERTA | ruin>5% |
| GBPUSD | Qulla_ORB | 1463 | 0.163 | 1.289 | 0.306 | 107.480 | 175.400 | 447.570 | 1.463 | 1.119 | 16.270 | 100.000 | 127.800 | ESTABLE | MUERTA | ruin>5%, WF deg WR>15% |
| GBPAUD | Qulla_ORB | 1452 | 0.163 | 1.273 | 0.286 | 143.200 | 174.100 | 415.880 | 1.259 | 1.286 | -7.890 | 100.000 | 142.140 | ESTABLE | MUERTA | ruin>5% |
| NASDAQ100 | Qulla_ORB | 1758 | 0.152 | 1.173 | 0.228 | 160.430 | 210.800 | 401.030 | 1.131 | 1.215 | 3.680 | 100.000 | 219.550 | ESTABLE | MUERTA | ruin>5%, PF<1.2 |
| WTI | Qulla_ORB | 1540 | 0.206 | 1.236 | 0.228 | 71.350 | 184.700 | 351.680 | 1.187 | 1.286 | -4.520 | 100.000 | 118.300 | ESTABLE | MUERTA | ruin>5% |
| EURJPY | Qulla_ORB | 1501 | 0.167 | 1.163 | 0.175 | 78.900 | 179.900 | 263.390 | 1.191 | 1.132 | -18.100 | 100.000 | 169.650 | MEJORANDO | MUERTA | ruin>5%, WF deg WR>15%, PF<1.2 |
| EURUSD | Qulla_ORB | 1493 | 0.152 | 1.132 | 0.146 | 103.340 | 179.000 | 217.990 | 1.168 | 1.096 | 14.050 | 100.000 | 174.360 | ESTABLE | MUERTA | ruin>5%, PF<1.2 |
| XAGUSD | Qulla_HTF | 300 | 0.423 | 2.299 | 0.666 | 26.360 | 40.900 | 199.790 | 2.507 | 2.084 | -4.840 | 0.110 | 20.410 | ESTABLE | FUERTE |  |
| XAUUSD | Minervini_VCP | 328 | 0.588 | 2.236 | 0.329 | 41.580 | 45.800 | 107.870 | 0.794 | 6.831 | -71.830 | 0.000 | 8.710 | MEJORANDO | ACEPTABLE | WF deg WR>15% |
| XAUUSD | Qulla_HTF | 231 | 0.390 | 1.514 | 0.259 | 37.430 | 34.200 | 59.850 | 1.050 | 2.154 | -55.790 | 0.200 | 21.520 | MEJORANDO | ACEPTABLE | WF deg WR>15% |
| WTI | Qulla_HTF | 427 | 0.354 | 1.222 | 0.127 | 61.030 | 53.200 | 54.270 | 0.905 | 1.567 | -15.170 | 25.700 | 39.870 | MEJORANDO | MUERTA | ruin>5%, WF deg WR>15% |
| BRENT | Qulla_HTF | 351 | 0.339 | 1.129 | 0.072 | 56.080 | 44.100 | 25.400 | 0.709 | 1.592 | -42.050 | 26.870 | 40.030 | MEJORANDO | MUERTA | ruin>5%, WF deg WR>15%, PF<1.2 |
| XAGUSD | Minervini_VCP | 164 | 0.402 | 1.235 | 0.152 | 62.200 | 23.900 | 25.020 | 0.604 | 2.352 | -188.240 | 0.740 | 24.140 | MEJORANDO | ACEPTABLE | WF deg WR>15% |
| NATGAS | Minervini_VCP | 33 | 0.576 | 1.086 | 0.060 | 14.370 | 5.000 | 1.970 |  |  |  | 0.000 | 13.600 | N/A | DEBIL | PF<1.2 |
| BRENT | Minervini_VCP | 82 | 0.476 | 0.923 | -0.048 | 20.360 | 15.900 | -3.930 | 1.011 | 0.833 | -5.260 | 0.010 | 19.760 | MEJORANDO | MUERTA | MC P5<0, PF OOS<1, net-, PF<1.2 |
| EURUSD | Zanger_FLAG | 15 | 0.000 | 0.000 | -0.344 | 4.690 | 3.100 | -5.170 |  |  |  | 100.000 | 999.000 | N/A | MUERTA | ruin>5%, net-, PF<1.2 |
| XAUUSD | Ryan_ANTS | 16 | 0.312 | 0.412 | -0.323 | 7.270 | 2.500 | -5.170 |  |  |  | 100.000 | 999.000 | N/A | MUERTA | ruin>5%, net-, PF<1.2 |
| USDJPY | Qulla_HTF | 30 | 0.400 | 0.702 | -0.176 | 17.450 | 11.500 | -5.290 |  |  |  | 0.000 | 11.650 | N/A | MUERTA | MC P5<0, net-, PF<1.2 |
| GBPUSD | Qulla_HTF | 21 | 0.191 | 0.445 | -0.320 | 6.970 | 7.900 | -6.730 |  |  |  | 100.000 | 999.000 | N/A | MUERTA | ruin>5%, net-, PF<1.2 |
| GBPAUD | Zanger_FLAG | 23 | 0.000 | 0.000 | -0.307 | 6.720 | 3.300 | -7.070 |  |  |  | 100.000 | 999.000 | N/A | MUERTA | ruin>5%, net-, PF<1.2 |
| GBPUSD | Zanger_FLAG | 28 | 0.000 | 0.000 | -0.283 | 7.620 | 5.100 | -7.930 |  |  |  | 100.000 | 999.000 | N/A | MUERTA | ruin>5%, net-, PF<1.2 |
| EURJPY | Zanger_FLAG | 30 | 0.000 | 0.000 | -0.332 | 9.620 | 4.900 | -9.950 |  |  |  | 0.000 | 9.790 | N/A | MUERTA | MC P5<0, net-, PF<1.2 |
| EURUSD | Minervini_VCP | 32 | 0.219 | 0.070 | -0.367 | 12.040 | 5.700 | -11.760 |  |  |  | 0.000 | 12.040 | N/A | MUERTA | MC P5<0, net-, PF<1.2 |
| AUDUSD | Qulla_HTF | 35 | 0.257 | 0.571 | -0.367 | 18.950 | 5.600 | -12.850 |  |  |  | 0.000 | 20.830 | N/A | MUERTA | MC P5<0, net-, PF<1.2 |
| GBPJPY | Qulla_HTF | 29 | 0.138 | 0.120 | -0.538 | 17.010 | 5.200 | -15.590 |  |  |  | 100.000 | 999.000 | N/A | MUERTA | ruin>5%, net-, PF<1.2 |
| GBPJPY | Zanger_FLAG | 61 | 0.000 | 0.000 | -0.282 | 16.970 | 9.700 | -17.190 | 0.000 | 0.000 | 0.000 | 0.000 | 17.060 | ESTABLE | MUERTA | MC P5<0, PF OOS<1, net-, PF<1.2 |
| GBPUSD | Minervini_VCP | 44 | 0.000 | 0.000 | -0.405 | 17.260 | 7.100 | -17.800 | 0.000 | 0.000 | 0.000 | 0.000 | 17.770 | ESTABLE | MUERTA | MC P5<0, PF OOS<1, net-, PF<1.2 |
| AUDUSD | Zanger_FLAG | 59 | 0.000 | 0.000 | -0.320 | 18.700 | 8.100 | -18.880 | 0.000 | 0.000 | 0.000 | 0.000 | 18.790 | ESTABLE | MUERTA | MC P5<0, PF OOS<1, net-, PF<1.2 |
| XAGUSD | Zanger_FLAG | 159 | 0.270 | 0.339 | -0.120 | 19.420 | 19.900 | -19.020 | 0.384 | 0.295 | -13.560 | 0.000 | 21.290 | DEGRADANDO | MUERTA | MC P5<0, PF OOS<1, decay-, net-, PF<1.2 |
| USDJPY | Zanger_FLAG | 68 | 0.000 | 0.000 | -0.343 | 23.030 | 11.400 | -23.310 | 0.000 | 0.000 | 0.000 | 0.000 | 23.120 | ESTABLE | MUERTA | MC P5<0, PF OOS<1, net-, PF<1.2 |
| USDJPY | Minervini_VCP | 120 | 0.350 | 0.343 | -0.220 | 30.900 | 19.900 | -26.450 | 0.583 | 0.061 | 64.520 | 0.370 | 28.550 | DEGRADANDO | MUERTA | MC P5<0, WF deg WR>15%, PF OOS<1, WF PF drop >40%, decay-, net-, PF<1.2 |
| WTI | Minervini_VCP | 141 | 0.362 | 0.759 | -0.189 | 44.930 | 18.800 | -26.660 | 0.793 | 0.727 | 12.360 | 78.150 | 42.820 | MEJORANDO | MUERTA | ruin>5%, MC P5<0, PF OOS<1, net-, PF<1.2 |
| GBPAUD | Minervini_VCP | 72 | 0.139 | 0.053 | -0.384 | 26.380 | 11.000 | -27.650 | 0.001 | 0.177 | -800.000 | 0.000 | 28.000 | MEJORANDO | MUERTA | MC P5<0, WF deg WR>15%, PF OOS<1, net-, PF<1.2 |
| EURJPY | Minervini_VCP | 118 | 0.263 | 0.185 | -0.253 | 29.310 | 23.700 | -29.820 | 0.177 | 0.195 | 27.780 | 32.860 | 30.600 | DEGRADANDO | MUERTA | ruin>5%, MC P5<0, WF deg WR>15%, PF OOS<1, decay-, net-, PF<1.2 |
| XAUUSD | Zanger_FLAG | 174 | 0.149 | 0.077 | -0.174 | 30.130 | 25.400 | -30.320 | 0.052 | 0.110 | -125.000 | 87.900 | 30.540 | MEJORANDO | MUERTA | ruin>5%, MC P5<0, WF deg WR>15%, PF OOS<1, net-, PF<1.2 |
| BRENT | Zanger_FLAG | 181 | 0.215 | 0.160 | -0.189 | 34.430 | 22.800 | -34.120 | 0.219 | 0.103 | 31.200 | 100.000 | 34.700 | DEGRADANDO | MUERTA | ruin>5%, MC P5<0, WF deg WR>15%, PF OOS<1, decay-, net-, PF<1.2 |
| GBPJPY | Minervini_VCP | 129 | 0.302 | 0.255 | -0.275 | 34.180 | 22.700 | -35.470 | 0.017 | 0.696 | -281.540 | 100.000 | 37.040 | MEJORANDO | MUERTA | ruin>5%, MC P5<0, WF deg WR>15%, PF OOS<1, net-, PF<1.2 |
| AUDUSD | Minervini_VCP | 95 | 0.190 | 0.090 | -0.379 | 38.110 | 16.200 | -36.050 | 0.283 | 0.000 | 100.000 | 100.000 | 36.530 | DEGRADANDO | MUERTA | ruin>5%, MC P5<0, WF deg WR>15%, PF OOS<1, WF PF drop >40%, decay-, net-, PF<1.2 |
| WTI | Zanger_FLAG | 234 | 0.179 | 0.115 | -0.214 | 50.470 | 29.500 | -50.110 | 0.130 | 0.102 | 9.090 | 100.000 | 50.590 | DEGRADANDO | MUERTA | ruin>5%, MC P5<0, PF OOS<1, decay-, net-, PF<1.2 |
| NASDAQ100 | Qulla_HTF | 504 | 0.276 | 0.598 | -0.311 | 179.800 | 61.600 | -156.960 | 0.482 | 0.714 | -13.850 | 100.000 | 171.370 | MEJORANDO | MUERTA | ruin>5%, MC P5<0, PF OOS<1, net-, PF<1.2 |
| NATGAS | Zanger_FLAG | 79 | 0.000 | 0.000 | -2.121 | 165.570 | 10.100 | -167.580 | 0.000 | 0.000 | 0.000 | 100.000 | 166.180 | ESTABLE | MUERTA | ruin>5%, MC P5<0, PF OOS<1, net-, PF<1.2 |
| NASDAQ100 | Minervini_VCP | 448 | 0.397 | 0.352 | -0.385 | 170.810 | 58.600 | -172.380 | 0.361 | 0.340 | 10.640 | 100.000 | 176.110 | DEGRADANDO | MUERTA | ruin>5%, MC P5<0, PF OOS<1, decay-, net-, PF<1.2 |
| NASDAQ100 | Zanger_FLAG | 360 | 0.003 | 0.000 | -0.518 | 185.750 | 44.000 | -186.350 | 0.000 | 0.000 | -55.560 | 100.000 | 186.060 | ESTABLE | MUERTA | ruin>5%, MC P5<0, WF deg WR>15%, PF OOS<1, net-, PF<1.2 |
| SP500 | Qulla_HTF | 271 | 0.243 | 0.269 | -0.804 | 224.570 | 33.300 | -218.010 | 0.171 | 0.363 | -52.710 | 100.000 | 223.160 | MEJORANDO | MUERTA | ruin>5%, MC P5<0, WF deg WR>15%, PF OOS<1, net-, PF<1.2 |
| AUDUSD | Qulla_ORB | 1465 | 0.123 | 0.850 | -0.173 | 398.910 | 175.700 | -252.860 | 1.120 | 0.593 | 29.340 | 100.000 | 390.560 | ESTABLE | MUERTA | ruin>5%, MC P5<0, WF deg WR>15%, PF OOS<1, net-, PF<1.2 |
| SP500 | Zanger_FLAG | 285 | 0.000 | 0.000 | -0.959 | 272.000 | 34.800 | -273.160 | 0.000 | 0.000 | 0.000 | 100.000 | 272.420 | ESTABLE | MUERTA | ruin>5%, MC P5<0, PF OOS<1, net-, PF<1.2 |
| SP500 | Minervini_VCP | 389 | 0.033 | 0.005 | -0.807 | 312.960 | 54.800 | -313.960 | 0.006 | 0.003 | -16.070 | 100.000 | 313.930 | ESTABLE | MUERTA | ruin>5%, MC P5<0, WF deg WR>15%, PF OOS<1, net-, PF<1.2 |
| NATGAS | Qulla_HTF | 210 | 0.167 | 0.216 | -1.552 | 322.550 | 25.600 | -325.810 | 0.147 | 0.286 | -5.880 | 100.000 | 333.690 | DEGRADANDO | MUERTA | ruin>5%, MC P5<0, PF OOS<1, decay-, net-, PF<1.2 |
| SP500 | Qulla_ORB | 1723 | 0.153 | 0.855 | -0.243 | 537.590 | 206.600 | -418.800 | 0.913 | 0.797 | 8.140 | 100.000 | 615.840 | ESTABLE | MUERTA | ruin>5%, MC P5<0, PF OOS<1, net-, PF<1.2 |
| NATGAS | Qulla_ORB | 1299 | 0.175 | 0.412 | -1.493 | 1936.230 | 155.800 | -1939.490 | 0.426 | 0.398 | 8.540 | 100.000 | 1974.000 | ESTABLE | MUERTA | ruin>5%, MC P5<0, PF OOS<1, net-, PF<1.2 |

## Agregado por trader_setup

| trader_setup | syms_ok | n_total | avg_wr | avg_pf | sum_r_total | avg_tpy |
|---|---|---|---|---|---|---|
| Qulla_ORB | 14 | 21047 | 0.167 | 1.197 | 3004.880 | 180.286 |
| Ryan_ANTS | 1 | 16 | 0.312 | 0.412 | -5.170 | 2.500 |
| Qulla_HTF | 11 | 2409 | 0.314 | 1.009 | -401.930 | 29.373 |
| Minervini_VCP | 14 | 2195 | 0.322 | 0.649 | -567.070 | 23.507 |
| Zanger_FLAG | 14 | 1756 | 0.086 | 0.070 | -850.160 | 16.579 |
