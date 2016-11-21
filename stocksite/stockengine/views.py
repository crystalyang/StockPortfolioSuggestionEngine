from django.shortcuts import render
from django.http import HttpResponse

from django import forms
from django.template import loader
from task import process_strategy, gettoday_price, check_db

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


    return render(request,'base.html', {'form':form})


def refresh(request):
    msg = check_db()
    form = selectionform()
    return render(request, 'base.html', {'msg':msg, 'form':form})

