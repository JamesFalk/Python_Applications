import yfinance as yf
import pandas as pd
import numpy as np


#TICKER TABLE LISTS#

#tckrX - HOOD CRYPTOs
tckr0= ['AAVE-USD', 'ADA-USD', 'AVAX-USD',  'BCH-USD', 'BTC-USD', 
'COMP5692-USD', 'DOGE-USD', 'ETC-USD', 'ETH-USD', 'LINK-USD', 'LTC-USD', 
'SHIB-USD', 'SOL-USD', 'UNI-USD', 'XLM-USD', 'XRP-USD', 'XTZ-USD']

#tckrY -- BARCHART 40-100% OPINION STOCKS
tckr01 = ['AAL', 'ACHR', 'ATGL', 'AZO', 'BARK', 'COCO',  'CODA', 'COIN', 'COST', 'CVNA', 'DDD', 'ENR', 'ERIC', 'FVRR', 'GAMB', 'GDYN', 'GME', 'HLT', 'HPE', 'IBM', 'JBLU', 'LPTH', 'LQDT', 'LUV', 'LWAY']
tckr02 = ['LZ', 'MOB', 'MSFT', 'MTTR', 'NGS', 'NOK', 'NTDOY', 'OB', 'ORLA', 'ORLY', 'QBTS', 'QUBT', 'SAM', 'FUN', 'SONY', 'SOUN', 'U', 'UEC', 'UMAC', 'UPST', 'UTI', 'WDAY', 'WH', 'WIX', 'ZM']
tckr03 =['AMZN', 'BBW', 'BROS', 'CAT', 'CMG', 'CRM', 'DAL', 'DASH', 'DE', 'DKNG', 'DLB', 'EA', 'EBAY', 'EXPE', 'FDX', 'FICO', 'FOX', 'GDDY', 'GOOG', 'GTLB', 'H', 'HD', 'HOOD', 'IHG', 'JCI']
tckr04 = ['LZB', 'MAR', 'META', 'NET', 'NFLX', 'PLTR', 'PYPL', 'RDDT', 'ROKU', 'SFM', 'SHAK', 'SHOP', 'SN', 'SQ', 'TMUS', 'TSLA', 'TWLO', 'WKEY', 'WMT', 'WOOF', 'XEL', 'YELP', 'Z']

#tckZZZ -3x BEAR/BULL ETFs'
tckr666 = ['BITI', 'DRIP', 'DRV',  'FAZ', 'FNGD', 'LABD', 'SDOW', 'SETH', 'SOXS', 'SPXS',
           'SPXU', 'SQQQ', 'SRTY', 'TMV', 'TZA',  'YANG']    
tckr777 = ['BITX', 'BTFX', 'DPST', 'DRN', 'FNGU', 'GUSH', 'JETU', 'LABU', 'SHNY', 'SOXL', 
'SPXL', 'SPYU', 'TECL', 'TMF', 'TNA', 'TQQQ', 'UDOW', 'UPRO', 'WTIU', 'YINN' ]


#tckr9999 - HOTTEST TICKERS LIST
tckr9999 = ['AAVE-USD', 'ADA-USD', 'ATGL', 'BITX',  'BTFX', 'CVNA', 
'DOGE-USD', 'DPST', 'GAMB', 'HOOD', 'LQDT', 'LWAY', 
'QBTS', 'QUBT', 'RGTI', 'TSLA', 'UPST', 'UTI',  'WKEY', 
'XLM-USD', 'XRP-USD', 'ACHR', 'GDYN', 'MOB', 'PLTR', 'RDDT', 'UMAC'] 
           
tickers = tckr9999



def get_market_indicators(tickers=['SPY', 'QQQ', 'DIA', 'BTC-USD', 'ETH-USD']):
    results = {}
   
    for ticker in tickers: 
        display_ticker = ticker.replace('-USD', '¤')
    
        stock = yf.Ticker(ticker)     
        
        # Fetch historical data
        hist = stock.history(period="3mo")
        # Calculate daily returns
        daily_returns = hist['Close'].pct_change()
        # Determine up, down, and neutral days
        up_days = daily_returns[daily_returns > 0.007].count()  # 0.7% threshold for up%
        down_days = daily_returns[daily_returns < -0.004].count()  # 0.4% threshold for dn%
        neutral_days = daily_returns.where((daily_returns <= 0.007) & (daily_returns >= -0.004)).count()    
        
        if up_days > down_days and up_days > neutral_days: odds = ' up '
        elif down_days > up_days and down_days > neutral_days: odds = ' dn '
        else: odds = 'ntrl'
        
        # Calculate RSI
        delta = hist['Close'].diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()
        rs = avg_gain / avg_loss
        rsi = 1 - (1 / (1 + rs))
        # Get the last RSI value
        last_rsi = rsi.iloc[-1]
        
        # Categorize RSI
        if last_rsi > 0.85: mktgrav = 'Crash'
        elif last_rsi > 0.67: mktgrav = 'Fall'
        elif last_rsi > 0.33: mktgrav = 'Hover'
        elif last_rsi > 0.15: mktgrav = 'Rise'
        else: mktgrav = 'Blast'
        
        results[display_ticker] = {
            'Up': f'{round(up_days / len(daily_returns) * 100, 1):.0f}%',
            'Ntr': f'{round(neutral_days / len(daily_returns) * 100, 1):.0f}%',
            'Dwn': f'{round(down_days / len(daily_returns) * 100, 1):.0f}%',
            'Chance': odds,
            'RSI Gravity': f'{round(last_rsi, 2)} ({mktgrav})' }
    
    # Convert to DataFrame for clean tabular display
    df = pd.DataFrame.from_dict(results, orient='index')
    
    # Adjust column order and width
    df = df[['Up', 'Ntr', 'Dwn', 'Chance', 'RSI Gravity']]
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    return df

class MonteCarloMultiTicker:
    def __init__(self, tickers, period='6MO'):
        self.tickers = tickers; self.period = period
        self.period_map = {'1MO': '1mo', '3MO': '3mo', '6MO': '6mo', '1YR': '1y', '5YR': '5y'}

    def fetch_stock_data(self, ticker):
        """Batch fetch stock data for multiple tickers"""
        try:
            stock = yf.Ticker(ticker)
            hist_data = stock.history(period=self.period_map[self.period])
            if hist_data.empty:
                return None
            return hist_data
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            return None

    def calculate_rsi(self, data, period=14):
        """Calculate RSI"""
        if data is None or len(data) < period: return np.nan
        delta = data['Close'].diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()
        rs = avg_gain / avg_loss
        rsi = 1 - (1 / (1.0 + rs))
        return rsi.iloc[-1]

    def calculate_perc_mean_val(self, data):
        """Calculate percent of mean value"""
        if data is None or len(data) == 0:
            return np.nan
        
        mean_close = data['Close'].mean()
        recent_close = data['Close'].iloc[-1]
        perc_of_mean = (recent_close / mean_close) * 100
        return perc_of_mean

    def calculate_relative_volume(self, data):
        """Calculate relative volume"""
        if data is None or len(data) == 0: return np.nan
        
        avg_volume = data['Volume'].mean()
        recent_volume = data['Volume'].iloc[-1]
        relative_volume = (recent_volume / avg_volume) * 100
        return relative_volume

    def monte_carlo_simulation(self, data, days_to_simulate=30):
        """Perform Monte Carlo simulation"""
        if data is None or len(data) == 0:
            return np.nan, np.nan
        
        # Calculate daily returns
        returns = data['Close'].pct_change().dropna()
        initial_price = data['Close'].iloc[-1]
        
        # Calculate mean and standard deviation of returns
        mean_return = returns.mean()
        std_return = returns.std()
        
        # Run a single simulation
        num_simulations = 2000
        simulations = np.zeros((num_simulations, days_to_simulate))
        
        for i in range(num_simulations):
            daily_returns = np.random.normal(mean_return, std_return, days_to_simulate)
            price_path = initial_price * (1 + daily_returns).cumprod()
            simulations[i, :] = price_path
        
        # Get the median projection's end point
        median_projection = np.percentile(simulations, 50, axis=0)
        WinPo = median_projection[-1] / initial_price
        future_price = median_projection[-1]
        
        return WinPo, future_price

    def analyze_tickers(self):
     """Analyze multiple tickers and return a sorted DataFrame"""
     results = []
    
     for ticker in self.tickers:
        if ticker == '---':
            continue  # Skip placeholder tickers when sorting
        
        try:
            # Remove -USD suffix for display
            display_ticker = ticker.replace('-USD', '¤').replace('5692', '')
            # Fetch historical data
            hist_data = self.fetch_stock_data(ticker)
            
            if hist_data is None:
                continue
            
            # Calculate metrics
            rel_vol = self.calculate_relative_volume(hist_data)
            win_potential, future_price = self.monte_carlo_simulation(hist_data)
            rsi = self.calculate_rsi(hist_data)
            perc_mean_val = self.calculate_perc_mean_val(hist_data)
            current_price = hist_data['Close'].iloc[-1]
            
            results.append({
                'Ticker': display_ticker,  'RelVol': f'{rel_vol:.0f}%', 
                 'WinPo': f'{win_potential:.1f}x',
                'RSI': f'{rsi:.2f}', 
                '%MnVal': f'{perc_mean_val:.0f}%',
                'Current': f'${current_price:.2f}',
                'Future': f'${future_price:.2f}'})
            
        except Exception as e:
            print(f"Error processing {ticker}: {e}")
    
    # Convert to DataFrame and sort by RelVol (converting back to numeric for sorting)
     df = pd.DataFrame(results)
    
    # Convert RelVol back to numeric for sorting (removing % sign)
     df['RelVol_Numeric'] = df['RelVol'].str.rstrip('%').astype(float)
    
    # Sort by RelVol in descending order and drop the temporary sorting column
     df_sorted = df.sort_values('RelVol_Numeric', ascending=False)
     df_final= df_sorted.drop('RelVol_Numeric', axis=1).reset_index(drop=True)
     return df_final
     

def highlight_high_potential_tickers(df):
    # Convert string columns to numeric for comparison
    df_numeric = df.copy()
    df_numeric['RelVol_Numeric'] = df_numeric['RelVol'].str.rstrip('%').astype(float)
    df_numeric['WinPo_Numeric'] = df_numeric['WinPo'].str.rstrip('x').astype(float)
    df_numeric['RSI_Numeric'] = df_numeric['RSI'].astype(float)
    
    # Create a hidden flag column for high potential tickers
    df['_high_potential'] = (
        (df_numeric['RelVol_Numeric'] >= 165) & 
        (df_numeric['WinPo_Numeric'] >= 1.2) & 
        (df_numeric['RSI_Numeric'] < 0.71))
    
    return df


def main():
    # First, print market indicators
    print("MARKET INDICATORS:")
    market_indicators = get_market_indicators()
    print(market_indicators)
    print("\n" + "="*50 + "\n")  # Separator
    
    # Then proceed with ticker analysis
    print("TICKER ANALYSIS TABLE:")
    analyzer = MonteCarloMultiTicker(tickers)
    results = analyzer.analyze_tickers()
    
    # Apply highlighting and identification
    results_with_highlight = highlight_high_potential_tickers(results)
    
    # Custom print function to highlight high potential tickers
    def print_results(df):
        for index, row in df.iterrows():
            if row['_high_potential']:
                # Print high potential tickers in green
                print("\033[92m" + " | ".join(map(str, row.drop('_high_potential'))) + "\033[0m")
            else:
                # Print other tickers in default color
                print(" | ".join(map(str, row.drop('_high_potential'))))
                
     # Print the results
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    
    # When printing DataFrame, the internal column will be hidden
    print(results_with_highlight.drop('_high_potential', axis=1))
    
    # Separate console print for colored output
    print_results(results_with_highlight)

if __name__ == "__main__":
    main()