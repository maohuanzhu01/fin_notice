import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Tuple
import talib  # Per gli indicatori tecnici

class FinancialAnalyzer:
    def __init__(self, ticker, benchmark_ticker='^GSPC', risk_free_rate=0.05):
        self.ticker = ticker
        self.benchmark_ticker = benchmark_ticker
        self.risk_free_rate = risk_free_rate
        self.stock = yf.Ticker(ticker)
        self.benchmark = yf.Ticker(benchmark_ticker)
        
    def get_historical_data(self, period='1y'):
        """Ottiene i dati storici"""
        stock_data = self.stock.history(period=period)
        benchmark_data = self.benchmark.history(period=period)
        return stock_data, benchmark_data
    
    def calculate_daily_returns(self, data):
        """Calcola i rendimenti giornalieri"""
        return data['Close'].pct_change().dropna()
    
    def calculate_volatility(self, returns):
        """Calcola la volatilità annualizzata"""
        return returns.std() * np.sqrt(252)
    
    def calculate_beta(self, period='1y'):
        """Calcola il beta"""
        stock_data, benchmark_data = self.get_historical_data(period)
        stock_returns = self.calculate_daily_returns(stock_data)
        benchmark_returns = self.calculate_daily_returns(benchmark_data)
        
        covariance = np.cov(stock_returns, benchmark_returns)[0][1]
        benchmark_variance = np.var(benchmark_returns)
        return covariance / benchmark_variance
    
    def calculate_sharpe_ratio(self, returns):
        """Calcola lo Sharpe Ratio"""
        excess_returns = returns - (self.risk_free_rate / 252)
        return np.sqrt(252) * (excess_returns.mean() / returns.std())
    
    def calculate_jensen_alpha(self, stock_returns, benchmark_returns):
        """Calcola l'Alpha di Jensen"""
        beta = self.calculate_beta()
        stock_return_mean = stock_returns.mean() * 252
        benchmark_return_mean = benchmark_returns.mean() * 252
        return stock_return_mean - (self.risk_free_rate + beta * (benchmark_return_mean - self.risk_free_rate))
    
    def calculate_treynor_ratio(self, returns):
        """Calcola il Ratio di Treynor"""
        beta = self.calculate_beta()
        return (returns.mean() * 252 - self.risk_free_rate) / beta
    
    def calculate_technical_indicators(self, data):
        """Calcola gli indicatori tecnici"""
        close_prices = data['Close']
        
        # Medie mobili (20 e 50 giorni)
        ma20 = talib.SMA(close_prices, timeperiod=20)[-1]
        ma50 = talib.SMA(close_prices, timeperiod=50)[-1]
        
        # RSI
        rsi = talib.RSI(close_prices, timeperiod=14)[-1]
        
        # MACD
        macd, signal, _ = talib.MACD(close_prices)
        current_macd = macd[-1]
        
        return ma20, ma50, rsi, current_macd
    
    def get_analysis(self) -> Dict:
        """Esegue l'analisi completa"""
        stock_data, benchmark_data = self.get_historical_data()
        stock_returns = self.calculate_daily_returns(stock_data)
        benchmark_returns = self.calculate_daily_returns(benchmark_data)
        
        ma20, ma50, rsi, macd = self.calculate_technical_indicators(stock_data)
        daily_variation = stock_returns.iloc[-1]
        
        return {
            'Stock': self.ticker,
            'Data': datetime.now().strftime('%Y-%m-%d'),
            'Daily Variation': daily_variation,
            'Sharpe Ratio': self.calculate_sharpe_ratio(stock_returns),
            'Volatility': self.calculate_volatility(stock_returns),
            'Jensen Alpha': self.calculate_jensen_alpha(stock_returns, benchmark_returns),
            'Treynor Ratio': self.calculate_treynor_ratio(stock_returns),
            'MA20': ma20,
            'MA50': ma50,
            'RSI': rsi,
            'MACD': macd,
            'Beta': self.calculate_beta()
        }

def get_nasdaq100_symbols():
    """Ottiene i simboli del NASDAQ 100"""
    nasdaq100_symbols = [
        'AAPL', 'MSFT', 'AMZN', 'NVDA', 'META', 'GOOGL', 'GOOG', 'AVGO', 'TSLA', 'AMD',
        'ADBE', 'COST', 'CSCO', 'PEP', 'NFLX', 'TMUS', 'CMCSA', 'INTC', 'INTU', 'QCOM',
        'TXN', 'AMD', 'HON', 'AMAT', 'ISRG', 'BKNG', 'SBUX', 'MDLZ', 'ADI', 'REGN',
        'GILD', 'VRTX', 'ADP', 'LRCX', 'PANW', 'KLAC', 'SNPS', 'CDNS', 'MU', 'ASML',
        'MELI', 'ATVI', 'ORLY', 'ABNB', 'CHTR', 'MAR', 'FTNT', 'KHC', 'PYPL', 'MNST',
        'CTAS', 'MCHP', 'PAYX', 'ADSK', 'ODFL', 'BIIB', 'CPRT', 'ROST', 'IDXX', 'EXC',
        'KDP', 'VRSK', 'DXCM', 'FANG', 'WBD', 'BKR', 'FAST', 'EA', 'XEL', 'EBAY',
        'ZS', 'ILMN', 'PCAR', 'DLTR', 'CTSH', 'WDAY', 'SIRI', 'DDOG', 'TEAM', 'ANSS',
        'SGEN', 'ALGN', 'MTCH', 'ZM', 'LCID', 'CRWD', 'RIVN', 'TTD', 'OKTA', 'MRNA',
        'JD', 'PDD', 'DASH', 'CVNA', 'DOCU', 'ROKU', 'MRVL', 'NXPI', 'WBA', 'CSX'
    ]
    print(f"Lista dei titoli NASDAQ 100 caricata ({len(nasdaq100_symbols)} titoli)")
    return nasdaq100_symbols

def main():
    results = []
    try:
        print("Ottenendo la lista dei titoli NASDAQ 100...")
        nasdaq100_symbols = get_nasdaq100_symbols()
        print(f"Trovati {len(nasdaq100_symbols)} titoli da analizzare")
        
        for i, symbol in enumerate(nasdaq100_symbols, 1):
            try:
                print(f"[{i}/100] Analizzando {symbol}...")
                analyzer = FinancialAnalyzer(symbol)
                analysis = analyzer.get_analysis()
                results.append(analysis)
            except Exception as e:
                print(f"Errore nell'analisi di {symbol}: {str(e)}")
                continue
        
        df = pd.DataFrame(results)
        df.to_csv('nasdaq100_analysis.csv', index=False)
        print("\nAnalisi completata e salvata in 'nasdaq100_analysis.csv'")
        print(f"Analizzati con successo {len(results)} titoli su {len(nasdaq100_symbols)}")
        
    except Exception as e:
        print(f"Errore durante l'esecuzione del programma: {str(e)}")
        if results:  # Salva comunque i risultati parziali se ce ne sono
            df = pd.DataFrame(results)
            df.to_csv('nasdaq100_analysis_partial.csv', index=False)
            print("Risultati parziali salvati in 'nasdaq100_analysis_partial.csv'")

if __name__ == "__main__":
    main() 