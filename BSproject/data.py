import whoosh
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
import pandas as pd
from whoosh.fields import Schema, TEXT
from whoosh import index
from whoosh import qparser
import getopt
import sys
import os, os.path
import sys
import csv

BOARDS = [
{"id":26073614,"name":"Al Pacino","photo":"https://placebear.com/342/479"}]


# import data into pandas df and create index schema
with open(r"SearchEngineData.csv") as csv_file:  
	  
	# read the csv file 
	csv_reader = csv.reader(csv_file, delimiter=',') 
	   
	# now we can use this csv files into the pandas 
	df = pd.DataFrame([csv_reader], index=None) 
	df.head() 

#schema of the search
schema = Schema(item=TEXT(stored=True), description=TEXT(stored=True), picture=TEXT(stored = True),type=TEXT(stored = True),brand=TEXT(stored = True),size=TEXT(stored = True),price=TEXT(stored = True),url=TEXT(stored = True),onsale=TEXT(stored = True),discount=TEXT(stored = True))



class wooshSearch(object):

	def __init__(self):
		super(wooshSearch,self).__init__()


	def populate_index(self,dirname, dataframe, schema):
		# Checks for existing index path and creates one if not present
		if not os.path.exists(dirname):
			os.mkdir(dirname)
		#print("Creating the Index")
		ix = index.create_in(dirname, schema)
		
		# Imports stories from pandas df
		
		
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
   
	# creates index searcher

	def index_search(self,dirname, search_fields):
		ix = index.open_dir(dirname)
		schema = ix.schema
		# Create query parser that looks through designated fields in index
		og = qparser.OrGroup.factory(0.9)
		mp = qparser.MultifieldParser(search_fields, schema, group = og)

		# This is the user query
		query = input("Please enter a Title, Year, Rating, IMDB tag, or some type of key word description:")
		q = mp.parse(query)
		threshold = int(input("How many results would you like?:"))
		# Actual searcher, prints top 10 hits
		with ix.searcher() as s:
			results = s.search(q, limit = threshold)	#user threshold
			print("Search Results: ")
			try:
				for i in range(threshold):
					print("\n RESULT #:",i+1 )			#prints resuts 
					print(results[i])
					print("\n")
			except IndexError:							#if it doesnt find x number of results it catches the error 
				pass									#program goes into the infinite while loop for another query
			

if __name__ == "__main__":

	wooshSearch().populate_index("Snowboard_Index", df,schema)


	#wooshSearch().index_search("Snowboard_Index", ['title', 'year','rating','description','Id','url'])




class MyWhooshSearch(object):
	"""docstring for MyWhooshSearch"""
	def __init__(self):
		super(MyWhooshSearch, self).__init__()

	def search(self, queryEntered):
		title = list()
		description = list()
		with self.indexer.searcher() as search:
			query = MultifieldParser(['title', 'description'], schema=self.indexer.schema)
			query = query.parse(queryEntered)
			results = search.search(query, limit=None)

			for x in results:
				title.append(x['title'])
				description.append(x['description'])

		return title, description
