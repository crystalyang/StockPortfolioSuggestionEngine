import time
import datetime
import pandas as pd
import numpy as np
import random
from pandas.tseries.offsets import BDay

from bokeh.io import show, output_file,save
from pandas_datareader import data, wb
import pandas_datareader.data as web
from stocksite import settings
# from sqlalchemy import create_engine


def getname(li):
    df = []
    for i in li:
        df.append(web.get_components_yahoo(i))
    return pd.concat(df)

def getnumshares(li, date, df_historical, singlestock):
    numshares={}
    for i in li:
        numshares[i] = singlestock[i]/df_historical.loc[date]['Close'][i]
    return numshares

def getportfolio_value(numshares, stocklist, date, df_historical):
    portfolio_value = 0
    for i in stocklist:
        portfolio_value += numshares[i] * df_historical.loc[date]['Close'][i]
    return portfolio_value

def track_portfolio_value(datelist, stocklist, df_historical,numshares):
    portfolio_values={}
    for i in datelist:
        portfolio_values[i] = getportfolio_value(numshares, stocklist, i, df_historical)
    return portfolio_values


def process_strategy(allotment, stockslist):
    # process the data and return a dataframe representing the portfolio trends and html tables
    singlestock = allotment / len(stockslist)
    #use a random distribution figuring out the allocation among stocks
    singlestock = np.mean(np.random.dirichlet(np.ones(len(stockslist)), 10), axis=0) * allotment
    # create a dictionary to map stock to their corresponding distribution
    stockallocation = dict(zip(stockslist, singlestock))
    enddate = datetime.datetime.now().date() - BDay(1)
    startdate = enddate - BDay(5)
    #getting historical data
    df = web.DataReader(stockslist, 'yahoo', enddate - BDay(6), enddate)
    df_historical = df.to_frame()

    #do the datelist calculation to figure out the last 5 active trading days
    last5dayindex = list(df_historical.index.levels[0][-5:])
    firstdayindex = df_historical.index.levels[0][-5]

    #get stock names
    # df_info = getname(stockslist)

    # calculating shares acquired on Day1
    num_shares = getnumshares(stockslist, firstdayindex, df_historical, stockallocation)
    # build a dateframe to track historical portfolio value change
    df_portfolio = track_portfolio_value(last5dayindex,stockslist, df_historical, num_shares)
    df_values = pd.DataFrame(df_portfolio.items(), columns=['Date', 'totalvalue'])
    df_values.Date = pd.to_datetime(df_values.Date)
    df_values.sort('Date', inplace=True)
    df_allocation = pd.DataFrame(stockallocation.items(), columns=['Stocks', 'Allocation'],
                                 index=stockallocation.keys())

    return df_allocation, df_values, stock_htmltable(stockallocation, stockslist)

def gettoday_price(stockslist):
    df_today = web.get_quote_yahoo(stockslist)
    return df_today

def stock_htmltable(stockallocation, stockslist):
    df_allocation = pd.DataFrame(stockallocation.items(), columns=['Stocks', 'Allocation'],
                                 index=stockallocation.keys())
    # get latest quote
    df_today = gettoday_price(stockslist)
    df_stocktoday = df_today.join(df_allocation, how='right')
    df_stocktoday['allocation_ratio'] = df_stocktoday.Allocation / df_stocktoday.Allocation.sum()
    stockinfo = {'exchange': {u'AAPL': u'NMS',
                              u'AMZN': u'NMS',
                              u'COST': u'NMS',
                              u'CRM': u'NYQ',
                              u'DIS': u'NYQ',
                              u'FB': u'NMS',
                              u'HD': u'NYQ',
                              u'MSFT': u'NMS',
                              u'NFLX': u'NMS',
                              u'NVDA': u'NMS',
                              u'PBW': u'PCX',
                              u'SCTY': u'NMS',
                              u'SPY': u'PCX',
                              u'TSLA': u'NMS',
                              u'TWLO': u'NYQ',
                              u'VBR': u'PCX',
                              u'VTI': u'PCX',
                              u'VWO': u'PCX',
                              u'XOM': u'NYQ'},
                 'name': {u'AAPL': u'Apple Inc.',
                          u'AMZN': u'Amazon.com, Inc.',
                          u'COST': u'Costco Wholesale Corporation',
                          u'CRM': u'Salesforce.com Inc Common Stock',
                          u'DIS': u'Walt Disney Company (The) Commo',
                          u'FB': u'Facebook, Inc.',
                          u'HD': u'Home Depot, Inc. (The) Common S',
                          u'MSFT': u'Microsoft Corporation',
                          u'NFLX': u'Netflix, Inc.',
                          u'NVDA': u'NVIDIA Corporation',
                          u'PBW': u'PowerShares WilderHill Clean En',
                          u'SCTY': u'SolarCity Corporation',
                          u'SPY': u'SPDR S&P 500',
                          u'TSLA': u'Tesla Motors, Inc.',
                          u'TWLO': u'Twilio Inc. Class A Common Stoc',
                          u'VBR': u'Vanguard Small-Cap Value ETF - ',
                          u'VTI': u'Vanguard Total Stock Market ETF',
                          u'VWO': u'Vanguard FTSE Emerging Markets ',
                          u'XOM': u'Exxon Mobil Corporation Common '}}
    df_stockinfo = pd.DataFrame(stockinfo)
    df_stocktoday = df_stocktoday.join(df_stockinfo, how='left')
    df_stocktodayhtml = df_stocktoday[['PE', 'last', 'time', 'Allocation', 'allocation_ratio', 'exchange', 'name']]
    df_stocktodayhtml.columns = ['PE', 'Latest Price', 'Last Quote Time', 'Holdings Value', 'Holdings ratio',
                                 'Exchange', 'Company Name']
    stocktable = df_stocktodayhtml.to_html(formatters={'Latest Price':'${:,.2f}'.format, 'Holdings Value':'${:,.2f}'.format, 'Holdings ratio':'{:,.2%}'.format})
    return stocktable



from bokeh.models import HoverTool
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.models import DatetimeTickFormatter, NumeralTickFormatter
from bokeh.embed import components
from bokeh.charts import Donut, show, output_file
def draw_portfoliochart(df_values):
    #calculate change column
    df_values['DOD Change'] = df_values['totalvalue'].pct_change()
    df_values['change'] = df_values['DOD Change'].map('{:.2%}'.format)
    max = df_values.totalvalue.max() + df_values.totalvalue.std()
    min = df_values.totalvalue.min() - df_values.totalvalue.std()
    value = list(df_values.totalvalue)
    change = list(df_values.change)
    date = list(df_values.Date)
    source = ColumnDataSource(data=dict(
        x=date,
        y=value,
        change=change,
    ))
    hover = HoverTool(
        tooltips=[
            ("Value", "@y{$1.11}"),
            ("Change vs Previous day", "@change"),
        ]
    )
    TOOLS = 'box_zoom,box_select,resize,reset'
    p = figure(plot_width=500, plot_height=300, x_axis_type="datetime", y_range=(min, max), tools=[hover, TOOLS])
    p.circle('x', 'y', size=15, source=source)
    p.line('x', 'y', line_width=3, source=source)

    p.yaxis[0].formatter = NumeralTickFormatter(format="$0.00")
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Total value'
    script, div = components(p)
    return script, div

def draw_piechart(df_allocation):
    TOOLS = 'box_zoom,box_select,resize,reset'
    df_allocation['percent'] = ['{:0.2%}'.format(a / sum(df_allocation['Allocation'])) for a in
                                df_allocation['Allocation']]
    d = Donut(df_allocation, label=['Stocks', 'percent'], values='Allocation',
              text_font_size='8pt', hover_text='Allocation', tools=TOOLS)
    script, div = components(d)
    return script, div


def stockprice_todb():
    fullstocklist = ['TSLA',
 'PBW',
 'SCTY',
 'AAPL',
 'CRM',
 'TWLO',
 'NVDA',
 'FB',
 'XOM',
 'COST',
 'HD',
 'AMZN',
 'MSFT',
 'NFLX',
 'DIS',
 'SPY',
 'VTI',
 'VWO',
 'VBR']
    enddate = datetime.datetime.now().date() - BDay(1)
    startdate = enddate - BDay(4)
    df = web.DataReader(fullstocklist, 'yahoo', enddate - BDay(4), enddate)
    df_historical = df.to_frame()
    df_historical = df_historical.reset_index()
    df_historical.rename(columns={'minor': 'ticker', 'Date': 'date', 'Adj Close': 'close', 'Volume': 'volume'},
                         inplace=True)
    df_sqlready = df_historical[['date', 'ticker', 'volume', 'close']]
    user = settings.DATABASES['default']['USER']
    password = settings.DATABASES['default']['PASSWORD']
    database_name = settings.DATABASES['default']['NAME']
    database_url = 'mysql://{user}:{password}@localhost/{database_name}'.format(
        user=user,
        password=password,
        database_name=database_name,
    )
    engine = create_engine(database_url, echo=False)
    df_sqlready.to_sql('stockportfolio_historical', con=engine, if_exists='replace')


from django.db import connection

def check_db():
    try:
        query = 'SELECT date from stockportfolio_historical order by date desc limit 1'
        with connection.cursor() as c:
            c.execute(query)
            latestdate = c.fetchall()
        enddate = datetime.datetime.now().date() - BDay(1)
        if latestdate[0][0].date() == enddate.date() :
            return 'Stock historical data is up-to-date'
        else:
            stockprice_todb()
            return 'Updating datebase'
    except:
        stockprice_todb()
        return 'Updating datebase'




