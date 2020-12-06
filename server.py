import sys
import os, os.path

from flask import Flask, render_template, redirect, url_for, request

from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

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
import math











app = Flask(__name__)

app.config['SECRET_KEY'] = 'NOJERRYSALLOWEDbcSHBXUXs2123'

bootstrap =Bootstrap(app)

@app.route('/', methods=['GET', 'POST'])
def index():

	return render_template('welcome_page.html')



@app.route('/next/<qp>/<pp>' , methods=["GET", "POST"])
def next(qp,pp):
	data = request.form

	print (qp)
	print(pp)
	keywordquery = qp
	int(pp)

	page = int(pp)

	

	print(page)
	item, description, picture, productType, brand, size, price, url, onsale, discount, page = mysearch.index_search(keywordquery,page+1)
	return  render_template('results.html', query=keywordquery, len = len(item), pag = math.ceil(len(item)/10) , page = page, item =item, description= description, picture =picture, productType = productType, brand = brand, size = size, price =price, url =url, onsale = onsale, discount =discount)

@app.route('/previous/<q>/<p>' , methods=["GET", "POST"])
def previous(q,p):
	data = request.form

	print (q)
	print(p)
	keywordquery = q
	int(p)

	page = int(p)

	if page <=1:
		page==2
		item, description, picture, productType, brand, size, price, url, onsale, discount, page = mysearch.index_search(keywordquery,page-1)
		return  render_template('results.html', query=keywordquery, len = len(item), pag = math.ceil(len(item)/10) , page = page, item =item, description= description, picture =picture, productType = productType, brand = brand, size = size, price =price, url =url, onsale = onsale, discount =discount)
	else:
		print(page)
		item, description, picture, productType, brand, size, price, url, onsale, discount, page = mysearch.index_search(keywordquery,page-1)
		return  render_template('results.html', query=keywordquery, len = len(item), pag = math.ceil(len(item)/10) , page = page, item =item, description= description, picture =picture, productType = productType, brand = brand, size = size, price =price, url =url, onsale = onsale, discount =discount)
	


@app.route('/results/', methods=['GET', 'POST'])
def results():
	global mysearch
	page = 1
	if request.method == 'POST':
		data = request.form
		if request.form['Previous_Page'] =='Previous Page':
			 print('Previous page')
			 page-=1
			 keywordquery = data.get('searchterm')
			 item, description, picture, productType, brand, size, price, url, onsale, discount = mysearch.index_search(keywordquery,page)
			 return render_template('results.html', query=keywordquery, len = len(item), pag = math.ceil(len(item)/10) , item =item, description= description, picture =picture, productType = productType, brand = brand, size = size, price =price, url =url, onsale = onsale, discount =discount)


		if request.form['Next_Page'] =='Next Page':
			 print('next page')
			 page+=1
			 keywordquery = data.get('searchterm')
			 item, description, picture, productType, brand, size, price, url, onsale, discount = mysearch.index_search(keywordquery,page)
			 return render_template('results.html', query=keywordquery, len = len(item), pag = math.ceil(len(item)/10) , item =item, description= description, picture =picture, productType = productType, brand = brand, size = size, price =price, url =url, onsale = onsale, discount =discount)


	else:
		data = request.args

	keywordquery = data.get('searchterm')
	

	#print('Keyword Query is: ' + keywordquery)


	#titles, description = mysearch.search(keywordquery)

	item, description, picture, productType, brand, size, price, url, onsale, discount, page = mysearch.index_search(keywordquery,page)
	

	return render_template('results.html', query=keywordquery, len = len(item), pag = math.ceil(len(item)/10) , page = page, item =item, description= description, picture =picture, productType = productType, brand = brand, size = size, price =price, url =url, onsale = onsale, discount =discount)



#approutes=============================================================================
	



# import data into pandas df and create index schema

class wooshSearch(object):

	def __init__(self):
		super(wooshSearch,self).__init__()


	def index(self):
		
		with open(r"SearchEngineData3.csv") as csv_file:
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

				print ("writing doc",i)

										#commit the document
   
	# creates index searcher

	def index_search(self,queryEntered,page):

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

		ix = open_dir('exampleIndex')
		schema = ix.schema
		# Create query parser that looks through designated fields in index
		og = qparser.OrGroup.factory(0.9)
		mp = qparser.MultifieldParser(['item', 'description','picture','productType','brand','size','price','url','onsale','discount'], schema =self.ix.schema, group = og)

		# This is the user query
		#query = input("Please enter a Title, Year, Rating, IMDB tag, or some type of key word description:")
		q = mp.parse(queryEntered)
		#threshold = int(input("How many results would you like?:"))
		# Actual searcher, prints top 10 hits
		with ix.searcher() as s:
			results = s.search_page(q, page)	#user threshold
			print("Search Results: ")
			try:
				for i in results:
					#print("\n RESULT #:",i+1 )			#prints resuts 
					#print(results[i])
					#print("\n")

					item.append(i['item'])
					description.append(i['description'])
					picture.append(i['picture'])
					productType.append(i['productType'])
					brand.append(i['brand'])
					size.append(i['size'])
					price.append(i['price'])
					url.append(i['url'])
					onsale.append(i['onsale'])
					discount.append(i['discount'])

			except IndexError:							#if it doesnt find x number of results it catches the error 
				pass									#program goes into the infinite while loop for another query
		return  item, description, picture, productType, brand, size, price, url, onsale, discount, page


if __name__ == '__main__':
	
	global mysearch
	
	mysearch = wooshSearch()

	mysearch.index()

	#print("\n\n Welcome to the Snowboard search engine")

	#wooshSearch().index_search("Snowboard_Index", ['item', 'description','picture','productType','brand','size','price','url','onsale','discount'],keywordquery)

	app.run(debug=True, use_reloader =False)
	
	
