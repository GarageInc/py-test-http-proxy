# -*- coding: utf-8 -*-

from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
import os
import re
import sys
import urllib2
import browser
import shutil

class PageParser(HTMLParser):

    def __init__(self, *args, **kwargs):
        HTMLParser.__init__(self)
        self.html = ""
	self.is_style = False

    def handle_starttag(self, tag, attrs):
        self.html += "<" + tag + " "

	if tag =="style":
            self.is_style = True
        
	for attr in attrs:
            self.html += attr[0] + "=\"" + attr[1] + "\" "
            
        self.html += ">"

    def handle_endtag(self, tag):

        self.html += "</" + tag + ">"

    def handle_startendtag(self, tag, attrs):
        self.html += "<" + tag + " "

        for attr in attrs:
            self.html += attr[0] + "=\"" + attr[1] + "\" "

        self.html += "/>"

    def handle_data(self, data):
	print "-------------------------------------"

        old_data = data.decode('utf-8')

	if self.is_style == True:
	    self.is_style = False
	    self.html += old_data
	    return 

	new_data = ""
	counter = 6

	ord_en_start = ord('A')
	ord_en_end = ord('z')
	ord_ru_start = ord('А'.decode('utf-8'))
	ord_ru_end = ord('я'.decode('utf-8'))

	is_word_end = False

	for symbol in old_data:

	    if is_word_end==True:
		is_word_end = False

		if counter == 0:
                    new_data += "*"
#                   new_data += "™".decode('utf-8')

		if counter <= 0:
		    counter = 6

	    new_data += symbol		
	    ordSymbol = ord(symbol)

	    if (counter<6 and symbol=='-') or (ord_en_start < ordSymbol and ordSymbol < ord_en_end) or (ord_ru_start < ordSymbol and ordSymbol < ord_ru_end):
		counter = counter - 1
	    else:
		is_word_end = True
		
        self.html += new_data

    def handle_entityref(self, name):
        c = unichr(name2codepoint[name])
        self.html += c

    def handle_charref(self, name):
        if name.startswith('x'):
            c = unichr(int(name[1:], 16))
        else:
            c = unichr(int(name))
        self.html += c

    def handle_decl(self, data):
        self.html += "<!" + data + ">"


class Page(object):

    def __init__(self, url, fp):
        self.url = url
        self.fp = fp
	dir = "site"
	shutil.rmtree( dir )
        self.fileRoot = dir
        self.siteRoot = "http://" + sys.argv[1]

    def save(self):
        url = self.url
        #add and update fp if necessary
        url = re.sub("{fp}", self.fp, url)
        last = url.rfind("/")
        self.fp = url[:last]
        #prep filepath
        filepath = url.split("/")
        #final url
        url = self.siteRoot +"/" + url
        #case for the index page

        if len(filepath) == 1 and not filepath[0]:
            filepath.append("index.html")
        filename = filepath[-1]

        #create filepath to save on disk
        if not filepath[0]:
            filepath = os.path.join(self.fileRoot, *filepath[1:-1])
        else:
            filepath = os.path.join(self.fileRoot, *filepath[:-1])

        if not os.path.exists(filepath):
            os.makedirs(filepath)

        #final write path
        filepath = os.path.join(filepath, filename)

        f = open(filepath, 'w')

        r = urllib2.urlopen(url)

        if ".html" in filename:
            parser = PageParser()

            parser.feed( r.read() )
            html = parser.html.encode('ascii', 'replace')

 	    f.write( html )
            f.close()
        else:
            f.write( r.read() )
            f.close()


if __name__ == '__main__':

    if len(sys.argv) == 2:

        page = Page("", "")

        page.save()
        
        print "End parsing"
        
        browser.Run()        
        
        print "Browser runned"
    else:

        print "Usage: python" , sys.argv[0], "www.example.com"

