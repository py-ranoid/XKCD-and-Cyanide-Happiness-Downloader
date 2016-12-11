import bs4
import urllib2
import urllib
import time
import sys
import os
import argparse

soup = bs4.BeautifulSoup

#	To retrieve ID of most recent comic

def getLastNum(com):
	if com == 'xkcd':
		html = soup(urllib2.urlopen('http://xkcd.com/').read(), "html.parser")
		t=html.find('a',attrs={'rel':'prev'}).get('href').split('/')[-2]
		prev = int(t)
	else:
		html = soup(urllib2.urlopen('http://explosm.net/comics/latest').read(), "html.parser")
		prev = int(html.find('a',attrs={'class':'previous-comic '}).get('href').split('/')[-2])
	return prev+1

parser = argparse.ArgumentParser()
parser.add_argument("-c","--com", help="XKCD(xkcd) or Cyanide and Happiness(CnH)",type=str)
parser.add_argument("-b","--begin", help="Comic number to begin from",type=int,default = 1)
parser.add_argument("-e","--end", help="Comic number to end at",type=int)
parser.add_argument("-p","--path", help="Path to store comic",type=str,default = os.getcwd())
args = parser.parse_args()

if args.com:
	com = args.com
	if com not in ['CnH','xkcd']:
		print 'Comic should be "CnH" or "xkcd".'
		exit()
	else:
		fpath=os.path.join(args.path, com)
		if com == 'CnH':
			url = 'http://explosm.net/comics/'
		else:
			url = 'http://xkcd.com/'
else:
	print 'Comic not specified.'
	exit()


#		Setting initial and final comic numbers
if args.end:
	end = args.end
else:
	end = getLastNum(com)
beg = args.begin


# 		Total number of comics expected
total = t = end-beg+1

# 		To keep track of total duration
start=time.time()


# 		Creates the folder path if it doesn't exist
if not os.path.exists(fpath):
	os.makedirs(fpath)


for x in xrange(beg,end+1):

	# 	Progress Bar
	percentage = 100*(x-beg+1)/total
	sys.stdout.write('\r')
	sys.stdout.flush()
	sys.stdout.write("Progress : [%-50s] %d%%" % ('='*(percentage/2), percentage))

	try:
		html = soup(urllib2.urlopen(url+str(x)+'/').read(), "html.parser")
	except urllib2.HTTPError:t-=1;continue
	#print html
	#		Use parsed HTML to extract
	#		 -> Image URL and Date for Cyanide and Happiness comics
	#		 -> Image URL for xkcd comics

	if com == 'CnH':
		Image = html.find('img', attrs={'id': "main-comic"})
		Date = html.find('h3', attrs={'class':'zeta small-bottom-margin past-week-comic-title'}).a.text
	else:
		Image = html.find('div', attrs={'id': "comic"}).find('img')

	#		Generates URL from img source
	#		Sets filename to
	#		 ->	<Date>. <Image Name> for Cyanide and Happiness comics
	#		 ->	<ComicNo>. <Alternate Text> for xkcd comics

	try:
		link='http:'+str(Image.get('src'))
		if com == 'CnH':
			temp = str(link.split('/')[-1])
			im =str(temp.split('?')[0])
			fname = Date+'. '+im
		else:
			fname = str(x) + '. ' + str(Image.get('title')) + link[-4:]
		impath = os.path.join(fpath, fname)
	except AttributeError:t-=1; continue

	#		Retrieve and store image from link to impath
	try:urllib.urlretrieve(link,  impath)
	except UnicodeEncodeError:urllib.urlretrieve(link, os.path.join(fpath, str(x)+link[-4:]))
	except IOError:t-=1

#		net = Total Duration
net= time.time()-start
if t==0:
	print '\nDownloaded 0 comics in',round(net,4),'seconds'
else:
	print '\nDownloaded',t,'comics in',round(net,4),'seconds @',str(round(net/t,4))+'s/comic'
