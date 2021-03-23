from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/history/IDR/USD/T')
soup = BeautifulSoup(url_get.content,"html.parser")

tbody = soup.find('table',attrs={'class':"table table-striped table-hover table-hover-solid-row table-simple history-data"})
tr = tbody.find_all('tr', attrs={'class':""})

temp = [] #initiating a tuple

for i in range(1, len(tr)):
#insert the scrapping process here
	row = tbody.find_all('tr',attrs={'class':""})[i]
	#get tanggal
	Date = row.find_all('td')[0].text
	Date = Date.strip()
	#get hari
	Day = row.find_all('td')[1].text
	Day = Day.strip()
    
	#get nilai uang
	IDR = row.find_all('td')[2].text
	IDR = IDR.strip()
    
    #get tulisan
	Note = row.find_all('td')[3].text
	Note = Note.strip()
	
	temp.append((Date, Day, IDR, Note))
     

temp = temp[::-1]

#change into dataframe
data = pd.DataFrame(temp, columns = ('Date','Day','IDR','Note'))
data['IDR'] = data['IDR'].replace('IDR','',regex=True).replace(',',"",regex=True)
data['IDR'] = data['IDR'].astype('float64')
data['Date'] = data['Date'].astype('datetime64')

#insert data wrangling here
Exchanges = data[['IDR']].set_index(data.Date).sort_values(by='Date', ascending=False)


#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'USD {Exchanges["IDR"].mean()}'

	# generate plot
	ax = Exchanges.plot(figsize = (10,9))

	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]


	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)
