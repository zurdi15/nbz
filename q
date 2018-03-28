[0;1;32m●[0m apache2.service - The Apache HTTP Server
   Loaded: loaded (/lib/systemd/system/apache2.service; enabled; vendor preset: enabled)
  Drop-In: /lib/systemd/system/apache2.service.d
           └─apache2-systemd.conf
   Active: [0;1;32mactive (running)[0m since Mon 2018-03-26 18:36:19 CEST; 13min ago
  Process: 2481 ExecStop=/usr/sbin/apachectl stop (code=exited, status=0/SUCCESS)
  Process: 2487 ExecStart=/usr/sbin/apachectl start (code=exited, status=0/SUCCESS)
 Main PID: 2492 (apache2)
    Tasks: 55 (limit: 4915)
   CGroup: /system.slice/apache2.service
           ├─2492 /usr/sbin/apache2 -k start
           ├─2493 /usr/sbin/apache2 -k start
           └─2494 /usr/sbin/apache2 -k start

mar 26 18:36:19 zurdi-server systemd[1]: Starting The Apache HTTP Server...
mar 26 18:36:19 zurdi-server apachectl[2487]: AH00558: apache2: Could not reliably determine the server's fully qualified domain name, using 127.0.1.1. Set the 'ServerName' directive globally to suppress this message
mar 26 18:36:19 zurdi-server systemd[1]: Started The Apache HTTP Server.
