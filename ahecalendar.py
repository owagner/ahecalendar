# -*- coding: utf-8 -*-
#
# Download des AHE-Abfallkalenders im JSON-Forma 
#
# Gibt entweder die Rohdaten aus, oder mit der Option --next
# die jeweils nächsten Abfuhrtermine pro Containertyp
#

from __future__ import print_function
import argparse
import urllib
import urllib2
import json
import sys
import time

parser = argparse.ArgumentParser(description='AHE Abfallkalender downloader')
parser.add_argument("plz",metavar="PLZ",type=int,help="Postleitzahl")
parser.add_argument("street",metavar="Straße",help="Straße")
parser.add_argument("no",metavar="Hausnummer",type=int,help="Hausnummer")
parser.add_argument("--next",action='store_true',help="Nächste Abfuhren ausgeben")

args=parser.parse_args()

# "district" bestimmen
req={"v":1,"city_zipcode":args.plz,"street":args.street,"house_number":args.no}
data=json.loads(urllib2.urlopen("http://ahe-afk.app.remondis.de/district?"+urllib.urlencode(req)).read())
if data["status"]!=1:
	print("Abholbereich nicht gefunden oder sonstiger Fehler",None,file=sys.stderr)
	sys.exit(1)
	
# Kalender holen
req={"v":1,"district_id":data["id"]}
cal=json.loads(urllib2.urlopen("http://ahe-afk.app.remondis.de/schedule?"+urllib.urlencode(req)).read())
if args.next:
	now=time.time()
	percontainer={}
	# Test
	for s in cal:
		when=time.mktime(time.strptime(s["scheduled_date"].split(" ")[0],"%Y-%m-%d"))
		if when>now:
			cont=s["container_long_name"]
			if not cont in percontainer or percontainer[cont]>when:
				percontainer[cont]=when
	for c in percontainer:
		percontainer[c]=time.strftime("%Y-%m-%d",time.localtime(percontainer[c]))
	print(json.dumps(percontainer))
else:
	print(cal)
