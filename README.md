# Analizzatore Finanziario NASDAQ 100

Questo script Python analizza tutti i titoli del NASDAQ 100, calcolando vari indicatori finanziari e tecnici per supportare l'analisi degli investimenti.

## Caratteristiche

- Analisi automatica di tutti i titoli del NASDAQ 100
- Calcolo di indicatori finanziari chiave:
  - Beta
  - Sharpe Ratio
  - Volatilità
  - Alpha di Jensen
  - Ratio di Treynor
- Indicatori tecnici:
  - Medie Mobili (20 e 50 giorni)
  - RSI (Relative Strength Index)
  - MACD (Moving Average Convergence Divergence)
- Output in formato CSV per facile analisi

## Prerequisiti 

bash
pip install yfinance pandas numpy talib-binary


## Utilizzo

1. Clona il repository o scarica i file
2. Installa le dipendenze
3. Esegui lo script:

bash
python financial_analyzer.py


Lo script genererà un file `nasdaq100_analysis.csv` contenente tutti i risultati.

## Output

Il file CSV contiene le seguenti colonne:
- Stock: Simbolo del titolo
- Data: Data dell'analisi
- Daily Variation: Variazione giornaliera
- Sharpe Ratio: Indice di Sharpe
- Volatility: Volatilità annualizzata
- Jensen Alpha: Alpha di Jensen
- Treynor Ratio: Indice di Treynor
- MA20: Media mobile a 20 giorni
- MA50: Media mobile a 50 giorni
- RSI: Relative Strength Index
- MACD: Moving Average Convergence Divergence
- Beta: Beta del titolo

## Gestione degli Errori

- Lo script continua l'esecuzione anche se alcuni titoli generano errori
- In caso di interruzione, viene salvato un file `nasdaq100_analysis_partial.csv` con i risultati parziali
- Vengono mostrati messaggi di progresso durante l'analisi

## Note

- I dati vengono recuperati da Yahoo Finance
- Il tasso risk-free è impostato di default al 5%
- L'indice di riferimento utilizzato è l'S&P 500 (^GSPC)
- L'analisi utilizza dati storici dell'ultimo anno

## Limitazioni

- La disponibilità dei dati dipende da Yahoo Finance
- Alcuni titoli potrebbero non avere tutti gli indicatori disponibili
- Le performance passate non garantiscono risultati futuri

## Contributi

Sentiti libero di contribuire al progetto attraverso pull request o segnalando eventuali problemi.

## Licenza

Questo progetto è distribuito con licenza MIT.