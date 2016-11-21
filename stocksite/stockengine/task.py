import time
import datetime
import pandas as pd
import numpy as np
import random
from pandas.tseries.offsets import BDay

from bokeh.io import show, output_file,save
from pandas_datareader import data, wb
import pandas_datareader.data as web



def getname(li):
    df = []
    for i in li:
        df.append(web.get_components_yahoo(i))
    return pd.concat(df)

def getnumshares(li, date, df_historical, singlestock):
    numshares={}
    for i in li:
        numshares[i] = singlestock/df_historical.loc[date]['Close'][i]
    return numshares

def getportfolio_value(numshares, stocklist, date, df_historical):
    portfolio_value = 0
    for i in stocklist:
        portfolio_value += numshares[i] * df_historical.loc[date]['Close'][i]
    return portfolio_value

def track_portfolio_value(startdate, delta, stocklist, df_historical,numshares):
    portfolio_values={}
    for i in range(delta):
        date = startdate + BDay(i)
        portfolio_values[str(date)] = getportfolio_value(numshares, stocklist, date, df_historical)
    return portfolio_values


def process_strategy(allotment, stockslist):
    singlestock = allotment / len(stockslist)
    enddate = datetime.datetime.now().date() - BDay(1)
    startdate = enddate - BDay(4)
    #getting historical data
    df = web.DataReader(stockslist, 'yahoo', enddate - BDay(4), enddate)
    df_historical = df.to_frame()

    #get latest quote
    df_today = web.get_quote_yahoo(stockslist)

    #get stock names
    df_info = getname(stockslist)

    # calculating shares acquired on Day1
    num_shares = getnumshares(stockslist, str(startdate), df_historical, singlestock)
    # build a dateframe to track historical portfolio value change
    df_portfolio = track_portfolio_value(startdate, 5, stockslist, df_historical, num_shares)
    df_values = pd.DataFrame(df_portfolio.items(), columns=['Date', 'totalvalue'])
    df_values.Date = pd.to_datetime(df_values.Date)

    from bokeh.models import HoverTool
    from bokeh.models import ColumnDataSource
    from bokeh.plotting import figure
    from bokeh.models import DatetimeTickFormatter, NumeralTickFormatter
    from bokeh.resources import CDN
    from bokeh.embed import components

    max = df_values.totalvalue.max() + df_values.totalvalue.std()
    min = df_values.totalvalue.min() - df_values.totalvalue.std()
    p = figure(plot_width=500, plot_height=300, x_axis_type="datetime", y_range=(min, max),
               title="Portfolio Total Value trend")
    p.line(df_values['Date'], df_values['totalvalue'], line_width=3)
    p.yaxis[0].formatter = NumeralTickFormatter(format="$0.00")
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Total value'
    script, div = components(p)

    return script, div

def gettoday_price(stockslist):
    df_today = web.get_quote_yahoo(stockslist)
    return df_today




