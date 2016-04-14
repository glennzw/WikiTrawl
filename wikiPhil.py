#!/usr/bin/python
# @glennzw 2012
# Small project to enact XKCD's Wikipedia philosophy loop: http://xkcd.com/903/
import urllib2
import httplib2
from BeautifulSoup import BeautifulSoup
import re
import time
import sys
import MySQLdb

http=httplib2.Http()
br_headers={'cache-control':'no-cache', 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)', 'host':'en.wikipedia.org'} #, 'Range':'bytes=1-15000'}
base='http://en.wikipedia.org/wiki/'

dbhost=""
dbuser=""
dbpass=""
dbdb=""

dbtable="wiki"

db = MySQLdb.connect(dbhost, dbuser, dbpass, dbdb)
cursor = db.cursor()

class wikiphil:
	def fetch_page(self,_url):
		self._url=_url
		self.retries=0
		while(self.retries<3):
			self.headers, self.page = http.request(self._url, method='GET', headers=br_headers)
			if(self.headers['status'][:2] != "20" ):
				print "[!] Bad HTTP status - %s" %(headers['status'])
				self.retries=self.retries+1
				time.sleep(4)
			else:
				#Remove all parenthesis content
				#Dirty hack
				self.soup = BeautifulSoup(self.page)
				for a in self.soup.findAll('a', href=True):
					a['href'] = re.sub('\(', 'a753f5654d61da8', a['href'])
					a['href'] = re.sub('\)', '1faf6cbe04a753f', a['href'])

				self.tmp=re.sub(r'\([^)]*\)', '', unicode(self.soup))
				self.tmp=re.sub('a753f5654d61da8','(',self.tmp)
				self.tmp=re.sub('1faf6cbe04a753f',')',self.tmp)
				self.soup = BeautifulSoup(self.tmp)

				return self.soup
		print "[!] Could not retrieve page"
		return None

	def fetch_links(self,_wikisoup):
		self._wikisoup=_wikisoup
		self.link_list=[]
		self.content = self._wikisoup.find("div",{"class":"mw-content-ltr"})

		#Remove tables
		for i in self.content.findAll('table'):
			i.extract()

		self.paragraphs = self.content.findAll("p")
		if (not self.paragraphs):
	#		print "[?] Tricky article, will just grab first decent looking link in page"
			self.paragraphs=[self.content]

		for para in self.paragraphs:
			self.links = para.findAll("a")
			for link in self.links:
				u=link["href"]
				if (u[0:6] == "/wiki/" and u.find("#")==-1 and u.find(":")==-1 and u.find("?")==-1):
					self.link_list.append(link)

		if (not self.link_list):
	#                print "[??] Tricky article, will just grab first decent looking link in page"
		        self.links = self.content.findAll("a")
		        for link in self.links:
		                u=link["href"]
		                if (u[0:6] == "/wiki/" and u.find("#")==-1 and u.find(":")==-1 and u.find("?")==-1):
		                        self.link_list.append(link)

		if not self.link_list:
			print "[!] Could not find link."
			return None
		else:
			return self.link_list

	@staticmethod
	def get_next(term):

#		if( term == "RANDOM_TERM"):
#			headers,page=http.request("http://en.wikipedia.org/wiki/Special:Random",method='GET', headers=br_headers))
#			soup=BeautifulSoup(page)
#			print soup.title
#			exit(-1)

		cursor.execute("SELECT node,neighbour FROM wiki WHERE node=%s", (term) )
		result=cursor.fetchone()

		if ( result==None ):
			print "%s not found, looking it up and inserting to db" %term
			wobj=wikiphil()
			soup = wobj.fetch_page(base+term)
			links = wobj.fetch_links(soup)

			next=re.sub('^.*\/','',links[0]["href"])
			cursor.execute('INSERT IGNORE INTO wiki SET node=%s,neighbour=%s', (term,next))
			return [1,next]
		else:
			return [0,result[1]]



if __name__ == "__main__":
	print wikiphil.get_next(sys.argv[1])
