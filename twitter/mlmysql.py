import MySQLdb as mdb
import sys
import re
from datetime import date, timedelta, datetime

con = None

host = '127.0.0.1'
user = 'root'
password = 'password'
database = 'mlmfan'

# write results
def write_to_db(record):
	con = mdb.connect(host,user,password,database);
	cur = con.cursor()
	values = (record[0],record[1],record[2],record[3],record[4],record[5],record[6],record[7],record[8],record[9],record[10])
	#print values
	SQL = 'INSERT INTO tweets(company_id,company,tweeter,tweet,datetime,followers,retweets,score,geo,terms,tweet_id) values(%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r)' % (values) # write each row before commit
	cur.execute(SQL)
	con.commit() # don't forget this little bugger
	con.close()
	
# returns latest tweet id (use as twitter search "since_id" parameter)	
def max_id(company_id):
	SQL = "Select max(tweet_id) from tweets where company_id = %s;" % str(company_id)
	con = mdb.connect(host,user,password,database);
	cur = con.cursor()
	cur.execute(SQL)
	maxid = cur.fetchone()[0] # get the maxid
	if maxid is None:
		maxid = 0
	con.close()
	return maxid
	
# returns oldest tweet id (use as twitter search "max_id" parameter)
def min_id(company_id):
	SQL = "Select min(tweet_id) from tweets where company_id = %s;" % str(company_id)
	con = mdb.connect(host,user,password,database);
	cur = con.cursor()
	cur.execute(SQL)
	minid = cur.fetchone()[0] # get the minid
	if minid is None:
		minid = 0
	else:
		minid = minid - 1 # to not include this tweet again
	con.close()
	return minid



