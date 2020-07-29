# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3
import mysql.connector
import pymongo

class ScrapyProjectPipeline(object):
	
	def __init__(self):
		self.DROP_TABLE_SCRIPT = 'DROP TABLE IF EXISTS products_tb'
		self.CREATE_TABLE_SCRIPT = '''CREATE TABLE products_tb (
			titles text, votes real, reviews int, prices real, image_links text
		)'''

		self.create_sqlite_connection()
		self.create_sqlite_table()

		self.create_mysql_connection()
		self.create_mysql_table()

		self.create_mongodb_database()

		
	def process_item(self, item, spider):
		self.INSERT_VALUES = (
			self.if_error(item['titles'], None), 
			self.if_error(item['votes'], None), 
			self.if_error(item['reviews'], None), 
			self.if_error(item['prices'], None),
			self.if_error(item['image_links'], None)
		)

		self.store_sqlite(item)
		self.store_mysql(item)
		self.store_mongodb(item)
		return item

	
	def if_error(self, item, value_if_error):
		try:
			return item[0]
		except:
			return value_if_error

		
	############## Store in SQLite3 ##############
	def create_sqlite_connection(self):
		self.conn_sqlite = sqlite3.connect('sqlite_database.db')
		self.curr_sqlite = self.conn_sqlite.cursor()

		
	def create_sqlite_table(self):
		self.curr_sqlite.execute(self.DROP_TABLE_SCRIPT)
		self.curr_sqlite.execute(self.CREATE_TABLE_SCRIPT)

		
	def store_sqlite(self, item):
		self.curr_sqlite.execute('INSERT INTO products_tb VALUES (?, ?, ?, ?, ?)', self.INSERT_VALUES)
		self.conn_sqlite.commit()

		
	############### Store in MySQL ###############
	def create_mysql_connection(self):
		self.conn_mysql = mysql.connector.connect(
			host = 'localhost',
			user = 'Quan Kun',
			passwd = '123',
			database = 'mysql_database'
		)
		self.curr_mysql = self.conn_mysql.cursor()

		
	def create_mysql_table(self):
		self.curr_mysql.execute(self.DROP_TABLE_SCRIPT)
		self.curr_mysql.execute(self.CREATE_TABLE_SCRIPT)

		
	def store_mysql(self, item):
		self.curr_mysql.execute('INSERT INTO products_tb VALUES (%s, %s, %s, %s, %s)', self.INSERT_VALUES)
		self.conn_mysql.commit()
	
	
	############## Store in MongoDB ##############
	def create_mongodb_database(self):
		self.conn_mongodb = pymongo.MongoClient('localhost', 27017)
		db = self.conn_mongodb['mongodb_database']
		self.collection = db['products_tb']

		
	def store_mongodb(self, item):
		self.collection.insert(dict(item))
