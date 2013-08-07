import twittersearchscore, companies, mlmysql, math, time, re, companiesv2

clist = companiesv2.companies_list
cdict = companiesv2.companies_dict
scrape_and_score = twittersearchscore.sentiment
max_id = mlmysql.max_id
min_id = mlmysql.min_id
write = mlmysql.write_to_db

# partition the list to run up to the limit
length = len(clist)
limit = 180
partitions = math.ceil(float(length)/float(limit))
marker = length/partitions

# run this bad boy 7 times
for i in range(1,4):
	for j in range(1,8):
		print 'Run %s,%s ...' % (str(i),str(j))
		
		# original
		for p in range(1,int(partitions+1)):
			end = int(marker*p)
			beg = int(marker*p-marker)
			for cidx in range(beg,end):
				company_id = clist[cidx]
				company = cdict[company_id]['name']
				since_id = max_id(company_id)
				maxid = min_id(company_id)
				query = cdict[company_id]['filter']
				tweets = scrape_and_score(company_id,company,since_id,maxid,query)
				for tweet in tweets:
					write(tweet)
				print 'Done with %s ...' % company
			if p > 1:
				print 'Waiting approx 15 min to reset twitter API limits ...'
				time.sleep(910) # break for 15 min to reset the twitter limit
		# if j > 1:
			# print 'Waiting approx 15 min to reset twitter API limits ...'
			# time.sleep(910) # break for 15 min to reset the twitter limit
		
		
		j += 1
	print 'Waiting approx 15 min to reset twitter API limits ...'
	time.sleep(910) # break for 15 min to reset the twitter limit
	i += 1