#!/usr/bin/python
# -*- coding: utf-8 -*-

# Requires internetarchive module (boto wrapper)
# To install:
# pip install internetarchive

import sys
import sqlite3
import internetarchive
import os
import os.path
import argparse

parser = argparse.ArgumentParser(
	description='Progromatically upload items to Internet Archive from sqlite database.',
	epilog="Sqlite database must have table or field called 'output' with the following fields: "
)
parser.add_argument('sqlitefile', metavar='filename', type=str, 
                   help='the sqlite database (see docs for fields)')
parser.add_argument('--accesskey', dest='accesskey', type=str,
                   help='Internet Archive access key')
parser.add_argument('--secretkey', dest='secretkey', type=str,
                   help='Internet Archive secret key')
parser.add_argument('--collection', dest='collection', type=str,
                   help='Destination Internet Archive collection')

args = parser.parse_args()
#print dir(args)

os.environ['AWS_ACCESS_KEY_ID']=args.accesskey
os.environ['AWS_SECRET_ACCESS_KEY']=args.secretkey

print 'Reading', str(args.sqlitefile)
con = sqlite3.connect(args.sqlitefile)
con.row_factory = sqlite3.Row

cur = con.cursor()
cur.execute('SELECT * FROM output')

for row in cur:
	if not os.path.isfile(row['path']):
		print row['parent_item_id'], '|','000', '|', row['ia_identifier'], '|', row['path']
	else:
		item = internetarchive.Item(row['ia_identifier'])
		result = item.upload(row['path'],
			metadata=dict(
				collection=args.collection,
				mediatype='audio',
				language='yid',
				title=row['item_title'],
				description=row['item_description'],
				author=row['item_author'],
#				title_yivo = row['title_yivo'],
#				author_last = row['author_last'],
#				author_first = row['author_first'],
#				reader_last = row['reader_last'],
#				reader_first = row['reader_first'],
#				author_last_eng = row['author_last_eng'],
#				author_first_eng = row['author_first_eng'],
#				reader_last_eng = row['reader_last_eng'],
#				reader_first_eng = row['reader_first_eng']
			)
		)
		print row['parent_item_id'], '|',result[0].status_code, '|', row['ia_identifier'], '|', row['path']

con.close()

