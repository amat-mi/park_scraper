# coding: utf-8

import glob
import json
import re
import sys
import time

filenames = sorted(glob.glob("park_*.json"))
count = 0
for filename in filenames:
    print filename
    try:
        stampstr = re.search('^park_([0-9]{8}-[0-9]{6})\.json$', filename).group(1)
        print stampstr
        print time.strptime(stampstr,"%Y%m%d-%H%M%S")
        with open(filename) as f:
            parks = json.load(f)
            for park in parks:
                print u'  {}'.format(park)
            count += 1
    except AttributeError:
        print u'Invalid file name: {}'.format(filename)
print "======================"
print u"Number of files: {}".format(count)
print "======================"
