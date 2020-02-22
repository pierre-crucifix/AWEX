import requests
from random import uniform
from time import sleep

# RUN THE SCRIPTS IN THE ORDER STATED

# Script #1

# Script which automates (smartly) a bunch of HTTP requests to the website where there is the database to counter the limit of 200 companies by request
# Will store the data extracted in xls (old Excel system) files that will have to merged later

### DISCLAIMER ###
# Web-scrapping, even processed gently (by using timers to delay the requests, avoiding to process several times the same request, etc) on freely available data can be on the edge of legality.
# So before executing this script, make sure that nothing forbids you to do so on http://www.awex-export.be/en/legal-notice , http://www.awex-export.be/en/privacy-policy , https://www.awex-export.be/robots.txt or any other legally valid place where AWEX would stipulate that web-scraping of its database is prohibited.
### End of disclaimer ###

### My secret sauce:
### 1) With Wireshark, inspected several traces corresponding to requests to the AWEX database through their website to observe which were the http requests sent in order to automate a massive extraction (and thus bypass the max 200 companies limit set up by AWEX's database manager/web developer). This 200 limit is the main challenge of the extraction
### 2) Simplified the request system to avoid using names by discovering each company has an (hidden for normal users) unique integer. Note that not all the integers are used in a successive chronological order (a lot of numbers does not correspond to anything)
### 3) Automation of this massive extraction coded below


url = "http://database.awex-export.be/export.php" #faudra réinspecter si cette URL est bonne ou pas ; edit:ça a marché!

#Small scale trials:
#data = {"sample_1_length" : "3", "CompanyExported[]" : "232", "CompanyExported[]" : "239", "CompanyExported[]" : "240", "export" : "excel"}#Focntionne mais retient que la derniere valeur de companyexported
#data = {"sample_1_length" : "3", "CompanyExported[]" : ["232", "239", "240"], "export" : "excel"}#Fonctionne totalement, juste on récupère les trucs dans un autre ordre que celui affiché autrement


companies_id=list(range(1,201))#Integer List from 1 to 200
data = {"sample_1_length" : "200", "CompanyExported[]" : companies_id, "export" : "excel"}#Created before the loop to improve perf
end_of_iteration=1000 #To change by a big enough number; edit: today it goes towards 46.000/200 = 230 for today (30/01/2020)

for i in list(range(0,end_of_iteration+1)):
    sleep(uniform(1,3)) #Be a gentleman while doing a massive extraction #Pour mettre du délai histoire de pas surcharger le serveur, c'est entre 1 et 3sec
    companies_id=list(range(1+i*200,201+i*200))
    data["CompanyExported[]"] = companies_id
    #print(data)

    tab_excel=requests.post(url,data) #Processing the request
    #print(tab_excel)
    if tab_excel.status_code==200: #If everything went well, we will reveive a 200 status code (look at HTTP requests theory if needed)
        output=open(r".\1.Results_from_AWEX_website\Results"+str(i*200+1)+"_"+str((i+1)*200)+".xls","wb")
        output.write(tab_excel.content)
        output.close()
    else: #In case we receive another status code, we will just print the number where it failed to reprocess it manually later. I did not observe any problem so there is no real need to automate the "exception" handling
        print("\nProblem encountered while processing the HTTP request for i="str(i)". Status code : "+str(tab_excel.status_code))#Will allow us to track if everything is going fine, and if not where is any problem