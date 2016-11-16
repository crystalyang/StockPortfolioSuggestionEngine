import quandl
import time
import datetime

while True:
    input = raw_input('Please enter a symbol: ')
    if input == 'exit':
        break
    quandl.ApiConfig.api_key = 'Vf8rgA91Rw4b2x_Lm3EJ'

    currentdate = datetime.datetime.now().date()
    try:
        data = quandl.get("WIKI/"+input+".11", start_date="2016-10-01", end_date=str(currentdate), collapse="none",
                          transform="none", returns="numpy")
        metadata = quandl.Dataset("WIKI/"+input).to_list()
        name = metadata[-1].split(',')[0]
        print time.ctime()
        print name
        today = data[-1][-1]
        last = data[-2][-1]
        print today, today - last, "{0:.2f}%".format((today - last) / last * 100)
    except Exception, e:
        print str(e).split(')')[-1]
