# park_scraper

# Installazione in Ubuntu

Installare il file di configurazione per upstart:

    sudo cp park_scraper.conf /etc/init/
    sudo chown root.root /etc/init/park_scraper.conf
    sudo chmod u=rw,go=r /etc/init/park_scraper.conf
    
e attivare il servizio con il comando:

    sudo initctl start park_scraper
    
Il log è visibile con il comando:

     sudo cat /var/log/upstart/park_scraper.log
     


    
