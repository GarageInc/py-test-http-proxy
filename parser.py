# -*- coding: utf-8 -*-
#!/usr/bin/env python

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

        old_data = data

	if self.is_style == True:
	    self.is_style = False
	    self.html += old_data
	    return 

	new_data = u""
	WORD_MAX_LENGTH = 6
	word_length = 0

	ord_en_start = ord('A')
	ord_en_end = ord('z')
	ord_ru_start = ord('А'.decode('utf-8'))
	ord_ru_end = ord('я'.decode('utf-8'))

	is_word_end = False

	for symbol in old_data:

	    ordSymbol = ord(symbol)

	    if (word_length < WORD_MAX_LENGTH and symbol == '-') or (ord_en_start < ordSymbol and ordSymbol < ord_en_end) or (ord_ru_start < ordSymbol and ordSymbol < ord_ru_end):
		word_length = word_length + 1
	    else:
                if word_length == WORD_MAX_LENGTH:
                    new_data += u'™'

                word_length = 0

	    new_data += symbol
		
        self.html += new_data

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
        url = re.sub("{fp}", self.fp, url)
        last = url.rfind("/")
        
        self.fp = url[:last]
        
        filepath = url.split("/")

        if len(filepath) == 1 and not filepath[0]:
            filepath.append("index.html")
        filename = filepath[-1]

        if not filepath[0]:
            filepath = os.path.join(self.fileRoot, *filepath[1:-1])
        else:
            filepath = os.path.join(self.fileRoot, *filepath[:-1])

        if not os.path.exists(filepath):
            os.makedirs(filepath)

        filepath = os.path.join(filepath, filename)

        f = open(filepath, 'w')

        r = urllib2.urlopen(self.siteRoot +"/" + url)

        if ".html" in filename:
            parser = PageParser()

            parser.feed( r.read() )
#            html = parser.html.encode('ascii', 'ignore')
	    html = parser.html.encode('utf-8')

 	    f.write( html )
            f.close()
        else:
            f.write( r.read() )
            f.close()


if __name__ == '__main__':

    if len(sys.argv) == 2:

        page = Page("", "")

        page.save()
        
        browser.Run()        
    else:

        print "Usage: python" , sys.argv[0], "www.example.com"

