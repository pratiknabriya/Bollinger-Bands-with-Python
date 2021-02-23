#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def plot_bollinger_bands(stock_symbol, start_date, end_date, MA_period = 20, num_stdev = 2):
    '''
    stock_symbol:  (str)stock ticker as on Yahoo finance. Eg: 'ULTRACEMCO.NS' 
    start_date:    (str)start analysis from this date (format: 'YYYY-MM-DD') Eg: '2018-01-01'
    end_date:      (str)end analysis on this date (format: 'YYYY-MM-DD') Eg: '2020-01-01'
    MA_period:     (int)moving average window period (Usually we take 20).
    num_stdev:     (int)number of standard deviations (Most commonly 2 std devs are considerd). 
    
    '''
    start = datetime.datetime(*map(int, start_date.split('-')))
    end = datetime.datetime(*map(int, end_date.split('-'))) 
    stock_df = web.DataReader(stock_symbol, 'yahoo', start = start, end = end)['Close']
    stock_df = pd.DataFrame(stock_df)
    stock_df.columns = {'Close Price'} 
    stock_df.dropna(axis = 0, inplace = True) 
    
    # compute the datapoints for moving average, upper band and the lower band
    def bollinger_band(price, MA_period, num_stdev):
        mean_price = price.rolling(MA_period).mean()
        stdev = price.rolling(MA_period).std()
        upband = mean_price + num_stdev*stdev
        dwnband = mean_price - num_stdev*stdev
        return np.round(mean_price, 3), np.round(upband, 3), np.round(dwnband, 3)

    stock_df['Moving_avg'], stock_df['Upper_band'], stock_df['Lower_band'] = bollinger_band(stock_df['Close Price'], 
                                                                                            MA_period, num_stdev)
    
    # plotting and visualization of bollinger bands
    stock_df['Close Price'].plot(c = 'k', figsize = (20,10), lw = 2, fontsize = 12)
    stock_df['Moving_avg'].plot(c = 'b', figsize = (20, 10), lw = 1)
    stock_df['Upper_band'].plot(c = 'g', figsize = (20, 10), lw = 1) 
    stock_df['Lower_band'].plot(c = 'r', figsize = (20, 10), lw = 1)

    # show plot
    plt.title('Bollinger Bands: {}'.format(stock_symbol), fontsize = 20)
    plt.ylabel('Price in INR(₹)',fontsize = 15 )
    plt.xlabel('Date', fontsize = 15 )
    plt.legend()
    plt.grid()
    plt.show()

