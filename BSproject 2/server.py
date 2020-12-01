from flask_bootstrap import Bootstrap
import sys
import os, os.path

from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from flask import Flask, render_template, url_for, request
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
import os, os.path
from whoosh import index
from whoosh import qparser
import getopt
import sys
import csv

from data import BOARDS
from modules import get_names, get_board, get_id


app = Flask(__name__)

app.config['SECRET_KEY'] = 'NOJERRYSALLOWEDbcSHBXUXs2123'

bootstrap =Bootstrap(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    names = get_names(BOARDS)
    # you must tell the variable 'form' what you named the class, above
    # 'form' is the variable name used in this template: index.html
    form = NameForm()
    message = ""
    if form.validate_on_submit():
        name = form.name.data
        if name.lower() in names:
            # empty the form field
            form.name.data = ""
            id = get_id(BOARDS, name)
            # redirect the browser to another route and template
            return redirect( url_for('actor', id=id) )
        else:
            message = "That board is not in our database."
    return render_template('index.html', names=names, form=form, message=message)


@app.route('/actor/<id>')
def actor(id):
    # run function to get actor data based on the id in the path
    id, name, photo = get_board(BOARDS, id)
    if name == "Unknown":
        # redirect the browser to the error template
        return render_template('404.html'), 404
    else:
        # pass all the data for the selected actor to the template
        return render_template('results.html', id=id, name=name, photo=photo)


@app.route('/my-link/')
def my_link():
	print('clicked')
	return 'Click'

@app.route('/results/', methods=['GET', 'POST'])
def results():
	global mysearch
	if request.method == 'POST':
		data = request.form
	else:
		data = request.args

	keywordquery = data.get('searchterm')
	test = data.get('test')

	print('Keyword Query is: ' + keywordquery)
	print('Test Query is: ' + test)

	titles, description = mysearch.search(keywordquery)
	return render_template('results.html', query=keywordquery, results=zip(item, description,picture,productType,brand,size,price,url,onsale,discount))



#approutes=============================================================================
	
with open(r"SearchEngineData.csv") as csv_file:  
	  
	# read the csv file 
	csv_reader = csv.reader(csv_file, delimiter=',') 
	   
	# now we can use this csv files into the pandas 
	df = pd.DataFrame([csv_reader], index=None) 
	df.head() 

class NameForm(FlaskForm):
    name = StringField('Which actor is your favorite?', validators=[DataRequired()])
    submit = SubmitField('Submit')



class MyWhooshSearch(object):
	"""docstring for MyWhooshSearch"""
	def __init__(self):
		super(MyWhooshSearch, self).__init__()

	def search(self, queryEntered):
		title = list()
		description = list()
		with self.indexer.searcher() as search:
			query = MultifieldParser(['item', 'description','picture','productType','brand','size','price','url','onsale','discount'], schema=self.indexer.schema)
			query = query.parse(queryEntered)
			results = search.search(query, limit=None)

			for x in results:
				title.append(x['title'])
				description.append(x['description'])
				picture.append(x['picture'])
				productType.append(x['productType'])
				brand.append(x['brand'])
				size.append(x['size'])
				price.append(x['price'])
				onsale.append(x['onsale'])
				discount.append(x['discount'])
				


		return title, description

	def index(self):
		schema = Schema(item=TEXT(stored=True), description=TEXT(stored=True), picture=TEXT(stored = True),productType=TEXT(stored = True),brand=TEXT(stored = True),size=TEXT(stored = True),price=TEXT(stored = True),url=TEXT(stored = True),onsale=TEXT(stored = True),discount=TEXT(stored = True))
		indexer = create_in('searchindex', schema)
		writer = indexer.writer()


		
		for i in range(len(list(df))):		#go the length of the index

			for val in list(dataframe[i]):

				writer = ix.writer() 		#add documents

				writer.add_document(item =(val[0]),	#val[] are the positions in the index piping it to the schema
						   description =(val[1]),
						   picture =(val[2]),
						   type =(val[3]),
						   brand =(val[4]),
						   size =(val[5]),
						   price =(val[6]),
						   url =(val[7]),
						   onsale =(val[8]),
						   discount =(val[9]))

				writer.commit()							#commit the document
				self.indexer = indexer

		writer.commit()

		self.indexer = indexer

if __name__ == '__main__':
	global mysearch
	app.run(debug=True)
	mysearch = MyWhooshSearch()
	mysearch.index()
	app.run(debug=True)
