# -*- coding: utf-8 -*-

print 'Compute your profit'

stock_symbol = str(raw_input("please enter a stock symbol:"))


allotment = int(input("Enter Allotment:"))



final_share_p = float(input("Enter Final Share Price:"))
sellc = float(input("Enter Sell Commission:"))
init_share_p = float(input("Enter Initial Share Price:"))
buyc = float(input("Enter Buy Commision:"))
tax_rate = float(input("Enter Capital Gain Tax Rate(%):"))


proceeds = final_share_p * allotment
purchasecost = init_share_p * allotment
costbase = purchasecost + buyc + sellc
tax = (proceeds - costbase)*(tax_rate/100) if proceeds>costbase else 0
totalcost = costbase + tax
netprofit = proceeds - costbase - tax
roi = round(netprofit / (proceeds - netprofit),4)
breakevenp = costbase / allotment

print '\n'
print "PROFIT REPORT:"
print "Proceeds"
print '$ {:,.2f}'.format(proceeds)
print '\n'
print "Cost"
print '$ {:,.2f}'.format(totalcost)
print '\n'
print 'Cost Details:' + '\n' + 'Total Purchase Price'
print str(allotment) + ' x $' + str(init_share_p) + ' = $' + '{:,.2f}'.format(purchasecost)

print 'Buy Commission = ' + '${:.2f}'.format(buyc)
print 'Sell Commission = ' + '${:.2f}'.format(sellc)
print 'Tax on Capital Gain = ' + str(tax_rate) + '% of $' + '{:,.2f}'.format(proceeds - costbase) + ' = ' + '${:,.2f}'.format(tax) if proceeds > costbase else 'Tax on Capital Gain = ' + str(tax_rate) + '% of $' + str(0) + ' = $' + str(0)

print '\n'
print 'Net Profit' + '\n' + '$' + '{:,.2f}'.format(netprofit)
print '\n'
print 'Return on Investment' +'\n' + '{:.2%}'.format(roi)
print '\n'
print 'To break even, you should have a final share price of' + '\n$' + '{:,.2f}'.format(breakevenp)

