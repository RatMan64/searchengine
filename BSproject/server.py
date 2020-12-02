#from flask_bootstrap import Bootstrap
import sys
import os, os.path

from flask import Flask, render_template, redirect, url_for, request
#from flask_bootstrap import Bootstrap
#from flask_wtf import FlaskForm
#from wtforms.validators import DataRequired

import whoosh
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
from whoosh import qparser


import pandas as pd
from whoosh.fields import Schema, TEXT
from whoosh import index
import sys
import csv








app = Flask(__name__)

#app.config['SECRET_KEY'] = 'NOJERRYSALLOWEDbcSHBXUXs2123'

#bootstrap =Bootstrap(app)

@app.route('/', methods=['GET', 'POST'])
def index():
	print('HEya')
	return render_template('welcome_page.html')


@app.route('/results/', methods=['GET', 'POST'])
def results():
	global mysearch
	if request.method == 'POST':
		data = request.form
	else:
		data = request.args

	keywordquery = data.get('searchterm')
	

	print('Keyword Query is: ' + keywordquery)


	#titles, description = mysearch.search(keywordquery)

	item, description, picture, productType, brand, size, price, url, onsale, discount = mysearch.index_search(keywordquery)
	

	return render_template('results.html', query=keywordquery, results=zip(item,description,picture,productType,brand,size,price,url,onsale,discount))



#approutes=============================================================================
	


#class NameForm(FlaskForm):
   # name = StringField('Which actor is your favorite?', validators=[DataRequired()])
  #  submit = SubmitField('Submit')



# import data into pandas df and create index schema

class wooshSearch(object):

	def __init__(self):
		super(wooshSearch,self).__init__()


	def index(self):
		
		with open(r"SearchEngineData2.csv") as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			df = pd.DataFrame([csv_reader], index=None) 
			df.head() 
		schema = Schema(item=TEXT(stored=True), description=TEXT(stored=True), picture=TEXT(stored = True),productType=TEXT(stored = True),brand=TEXT(stored = True),size=TEXT(stored = True),price=TEXT(stored = True),url=TEXT(stored = True),onsale=TEXT(stored = True),discount=TEXT(stored = True))
		
		ix = create_in('exampleIndex', schema)
		
		# Imports stories from pandas df
		
		
		for i in range(len(list(df))):		#go the length of the index

			for val in list(df[i]):

				writer = ix.writer() 		#add documents

				writer.add_document(item =(val[0]),	#val[] are the positions in the index piping it to the schema
						   description =(val[1]),
						   picture =(val[2]),
						   productType =(val[3]),
						   brand =(val[4]),
						   size =(val[5]),
						   price =(val[6]),
						   url =(val[7]),
						   onsale =(val[8]),
						   discount =(val[9]))

				writer.commit()
				self.ix = ix

				print ("writing doc")

										#commit the document
   
	# creates index searcher

	def index_search(self,queryEntered):
		item = list()
		description = list()
		picture= list()
		productType= list()
		brand= list()
		size= list()
		price= list()
		url= list()
		onsale= list()
		discount= list()


		
		
		# Create query parser that looks through designated fields in index
		#og = qparser.OrGroup.factory(0.9)
		#mp = qparser.MultifieldParser(['item', 'description','picture','productType','brand','size','price','url','onsale','discount'], schema=self.ix.schema, group = og)

		# This is the user query
		#query = input("Please enter a Board or gear you would like:")
		#query = (queryEntered)
		#q = mp.parse(query)
		#threshold = int(input("How many results would you like?:"))
		# Actual searcher, prints top 10 hits
		with self.ix.searcher() as s:
			query = MultifieldParser(['item', 'description','picture','productType','brand','size','price','url','onsale','discount'], schema=self.ix.schema)
			query = query.parse(queryEntered)

			results = s.search(query, limit = None)

			for i in results:
				item.append(i['item'])
				description.append(i['description'])
				picture.append(i['picture'])
				productType.append(i['productType'])
				brand.append(i['brand'])
				price.append(i['price'])
				url.append(i['url'])
				onsale.append(i['onsale'])
				discount.append(i['discount'])

		
											#program goes into the infinite while loop for another query
		return  item, description, picture, productType, brand, size, price, url, onsale, discount


if __name__ == '__main__':
	
	global mysearch
	
	mysearch = wooshSearch()

	mysearch.index()

	#print("\n\n Welcome to the Snowboard search engine")

	#wooshSearch().index_search("Snowboard_Index", ['item', 'description','picture','productType','brand','size','price','url','onsale','discount'],keywordquery)

	app.run(debug=True)
	
	
