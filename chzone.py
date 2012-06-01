import json,cherrypy 
import ConfigParser,string,os,sys,commands 





class chzone:
	@cherrypy.expose
	def ReceivedIP(self,name, *ip):
	##--init conf args--
	    cf = ConfigParser.ConfigParser()
	    cf.read("nameserver.conf")
	    dnszonefile = cf.get("file","dnszonefile")
	    rfcmd = cf.get("cmd","reflushcmd")
	    zonejson = cf.get("file","jsonfile")
	    domainname = cf.get("domain","domainname")

	##--read jsonfile--    
	    openjson = open(zonejson,'r') # open
	    readjson = openjson.readlines()
	    jsonfile = readjson[0]
	    openjson.close()

	    dictfile = json.loads(jsonfile)

	##--print dict info--
	#    print "good"
	#    for i in dictfile.keys():
	#        c = dictfile[i]
	#        for j in c:
	#            print (j)
	#    print "test"


	#    print "dictfile"

	##--add ip to name
	#    for i in ip:
	    print "dictfile"
	    dictfile[name] = ip
	    print dictfile[name]

	##--add one by one--
	##    d = dictfile[name]
	##    for i in ip:
	##        d[0:0] = [i]
	##    e = d[0]
	##    print e


	##--renew zone file

	##--init dnszonefile--
	    dnszone_init = '''$TTL    86400
@               IN SOA  @       root (
                                        42              ; serial (d. adams)
                                        3H              ; refresh
                                        15M             ; retry
                                        1W              ; expiry
                                        1D )            ; minimum

                IN NS           127.0.0.1
                IN A            127.0.0.1
                IN AAAA         ::1'''

	    dnszone = open(dnszonefile,'w') # open
	    dnszone.write(dnszone_init,)
	    dnszone.close()
	    for i in dictfile.keys():
		c = dictfile[i]
		for j in c:
		    oneip = (j)
	            addip = str(oneip)
		    addname = i
		    print addip
	            record = "\n"+addname+"           IN A            "+addip
		    dnszone = open(dnszonefile,'a') # open
		    dnszone.write(record,)
		    dnszone.close()


	##--print dict keys--
	#    for i in dictfile.keys():
	#        print dictfile[i]


	##--renew jsonfile
	    g = json.dumps(dictfile)
	    f = open(zonejson,'w') # open
	    f.write(g,) # write
	    f.close() #close
	    
	    op = commands.getstatusoutput(rfcmd)
	    print op
	    lookupnewrecord = "nslookup "+name+"."+domainname
	    print lookupnewrecord
	    newrecord = commands.getoutput(lookupnewrecord)
	    return newrecord
#ReceivedIP("test20","0.2.3.4","0,3,4,5","03.2.3.2")
#chzone.ReceivedIP("test20","03.2.3.2")
cherrypy.config.update({'server.socket_host':'0.0.0.0','server.socket_port':8055})
cherrypy.quickstart(chzone())
