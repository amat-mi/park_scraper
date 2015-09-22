# coding: utf-8

import requests
import re
import json
import time
from datetime import datetime
import pytz
from bs4 import BeautifulSoup

def run():
    pattern = re.compile('[Uu]ltimo\W+[Aa]ggiornamento\W*\:*\W*([0-9]{2}\/[0-9]{2}/[0-9]{4}\W[0-9]{2}[^0-9]{1}[0-9]{2}[^0-9]{1}[0-9]{2})')
    cet_timezone = pytz.timezone('CET')      #timezone locale (CET for CEnTral Europe)
    with requests.Session() as session:
        while True:
            utcnow = datetime.utcnow()
            naivenow = datetime.now() 
            nowstampstr = pytz.utc.localize(utcnow).isoformat()
        
            print naivenow,
            try:        
                r = session.get('http://www.webalice.it/antoniotib/SSF.html')
            
                print '.',
                content = r.text
                #estrae dall'HTML l'ultimo istante di aggiornamento, lo converte da stringa a datetime naive,
                #lo setta sul timezone locale, lo converte in UTC,
                #lo memorizza come string in formato ISO (adatto a JavaScript, anche se non ha la 'Z' finale)
                webstampstr = re.search(pattern,content).group(1)
                webstamp = datetime.strptime(webstampstr,"%d/%m/%Y %H.%M.%S")    
                webstampstr = cet_timezone.localize(webstamp).astimezone(pytz.utc).isoformat()    
                #estrae dall'HTML solo la parte con "<table>...</table>" e ne fa il parsing
                #ogni <tr> dopo il primo contiene i dati di un parcheggio (l'ultimo contiene i dati del TOTALE)
                content = '<table' + re.split('(table)',content)[2] + 'table>'
                soup = BeautifulSoup(content,"html.parser")
                parks = []
                for tr in soup("tr")[1:]:
                    tds = [x.string for x in tr("td")]
                    parks.append({
                        'name': tds[0],
                        'capacity': int(tds[1]),
                        'full': int(tds[2]),
                        'free': int(tds[3]),
                    })
                
                current = json.dumps(parks)
                try:
                    with open('parklast.json','r') as f:
                        last = f.read()
                        changed = current != last
                except IOError:
                    changed = True
                
                print '.',
                if changed:
                    print 'changed',
                    with open('parklast.json','w') as f:
                        f.write(current)
                    #se richiesto scrive i dati correnti anche in un file con l'istante attuale (nel timezone locale) nel nome
                    timestr = naivenow.strftime("%Y%m%d-%H%M%S")
                    with open('park_{}.json'.format(timestr),'w') as f:
                        f.write(current)
                    #se richiesto invia i dati di ogni parcheggio come una separata PUT in formato JSON 
                    for park in parks:
                        park['webstamp'] = webstampstr      #must set them here, because if wrote to the file, they'll make        
                        park['nowstamp'] = nowstampstr      #a false positive for a change of data with previous iteration            
                        print park
            #             r = requests.put("http://127.0.0.1:8000/park/parkdata/upload/", json=park)
                        r = requests.put("https://dati.amat-mi.it/park/parkdata/upload/", json=park)
                        print r.text
            except Exception, exc:
                print str(exc)
                
            print    
            time.sleep(10)

if __name__ == '__main__':
    run()
