from django.shortcuts import render
from django.http import HttpResponse

from django import forms
from django.template import loader
from task import process_strategy, gettoday_price

# Create your views here.

def test(request):
	return HttpResponse("Hello, world")

Portfolio_strategies=(('ethical','Ethical Investing'),('growth','Growth Investing'),('index','Index Investing'),('quality','Quality Investing'),('value','Value Investing'))
Stocks = {'ethical':['TSLA','PBW','SCTY','AAPL'], 'growth':['CRM','TWLO','NVDA'], 'index':['SPY','VTI','VWO','VBR'], 'quality':['FB', 'XOM','COST','HD'],'value':['AMZN','MSFT','NFLX','DIS']}
class selectionform(forms.Form):
    strategies = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, required=True, choices=Portfolio_strategies, help_text='Please select investment strategy')
    # strategies = forms.ChoiceField(required=True, choices=Portfolio_strategies)
    allotment = forms.DecimalField(required=True, help_text='Total amount to be invested(minimum $5000 USD)',min_value=5000)


def portfolio(request):
    form = selectionform()
    if request.POST:
        form = selectionform(request.POST)
        if form.is_valid():
            params = request.POST.copy()
            allotment = float(params['allotment'])
            choice = params.getlist('strategies')
            #choice represents the investment strategies selected
            stocklist =[]
            for i in choice:
                stocklist += Stocks[i]
            # data = gettoday_price(stocklist)
            # data = data.to_html()
                script, div = process_strategy(allotment, stocklist)
                print script
                print div
        return render(request, 'result.html', {'the_script':script, 'the_div':div})

        return render(request, 'result.html', {'data':data})

    return render(request,'base.html', {'form':form})


def Cal(request):
    form = simpleform()
    if request.POST:
        form = simpleform(request.POST)
        if form.is_valid():
            params = request.POST.copy()
            intkeys = params.keys()
            for key in intkeys:
                if params[key].isdigit():
                    params[key] = int(params[key])
            proceeds = params['allotment'] * params['finalprice']
            totalpurchaseprice = params['allotment'] * params['iniprice']
            buycom = params['bcommission']
            selcom = params['scommission']

            capgaintax = (params['tax']/100.0)*(params['finalprice']*params['allotment'] - totalpurchaseprice - buycom - selcom)
            cost = totalpurchaseprice + buycom + selcom + capgaintax
            netprofit = proceeds - cost
            roi = round(netprofit/float(cost),4)*100
            breakeven = (totalpurchaseprice + buycom + selcom)/float(params['allotment'])

            return render(request, 'result.html',{'proceeds':proceeds, 'cost':"{:,}".format(cost), 'purchase_price':"{:,}".format(totalpurchaseprice), 'buycom':buycom, 'selcom':selcom, 'tax':"{:,}".format(capgaintax), 'netprofit':"{:,}".format(netprofit), 'roi':roi, 'breakeven':breakeven,'allotment':params['allotment'],
                                                  'bprice':params['iniprice'], 'taxbasis':(params['finalprice']*params['allotment'] - totalpurchaseprice - buycom - selcom), 'taxrate':params['tax']})
    return render(request, 'base.html', {'form':form})