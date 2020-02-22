import pandas as pd
# import geopandas as gpd
from geopandas.tools import geocode
from random import uniform
from time import sleep

# Script #4
# Locator


# Retrieving the postcodes from our database
df=pd.read_excel(r".\3.Analyses\AllCompanyInfosSortedByPostCodeWithoutDuplicate.xls")
occurences=df["Postcode"].value_counts()
print(occurences.head(5))
postcodes=df["Postcode"]
postcodes = postcodes.drop_duplicates(keep = "last")
#postcodes=postcodes.head(3) #For small scale tests (ulrta useful to not waste time/not requiring a lot of same data again and again to nominatim (OpenStreetMap locator)
list_postcodes=postcodes.tolist()

#At the end also put the next line in try except so that a problem can be solved #edit: not necessary because you have to stay in front when you run it (at the begining at least)
geo = geocode("3000 belgium", provider='nominatim') #Prealloc before the loop
sleep(2) #timer

list_long_lat=list(range(0,len(list_postcodes))) #Preallocation of a list which will contain the coordinates of the different postcodes

for i,j in zip(list_postcodes,list(range(0,len(list_postcodes)))):
    k=5 #k seconds to wait in case of error
    if i%25==0:
        sleep(2)

    sleep(uniform(1.5,3))#1.5 à 3 sec break to time between requests ; PAY attention that it is forbidden to be below 1

    while True: #Will re-try indefinitely when encountering an error to process the request for the long&lat
        try:
            # do stuff
            geo = geocode(str(i) + " Belgium", provider='nominatim')  # Precise be so that the search will stay in Belgium
        except:
            print("Error happened - waiting " +str(k)+" seconds before trying again")
            sleep(k)#Maybe the error was due to too many requests in a short time => delay
            k*=2 #It will increase the wait by 2 times for the current postcode (exponential behavior)
            continue#Re-try
        break#Break the while if everything was ok

    print("postcode number "+str(j)+" : "str(i))
    list_long_lat[j] = geo.to_crs({'init': 'epsg:3395'}) #Here is a tricky line. We convert the received coordinated in the Mercator representation of the world (coming from the Robinson. The conversion is done at several places of the code to offer finally a coherent Mercator view of belgium which is the most boradly used on map focusing on Belgium (and not at World level)


x=list(range(0,len(list_long_lat)))
y=list(range(0,len(list_long_lat)))
for i in list(range(0,len(list_long_lat))):
    x[i]=list_long_lat[i].loc[0,"geometry"].x
    y[i]=list_long_lat[i].loc[0,"geometry"].y

intensity=occurences.sort_index().tolist() #Will be useful for the s of the scatter function to represent the intensity at a given postcode

#We finally save all the computations in a csv file that we will use later to plot the results
locations=pd.DataFrame()
locations["Postcode"]=list_postcodes
locations["x"]=x
locations["y"]=y
locations["intensity"]=intensity
locations.to_csv(r".\4.Locate\LocationsAndIntensityWithAberations.csv")


##########################################################################################
## END OF SCRIPT: code below is still there in case my method with nominatim does not work anymore in the future
##########################################################################################
# EDIT: I FINALLY DO NOT USE IT BECAUSE NOT ALL POSTCODES ARE IN IT... But I let it anyway here to have a starting point next time in case my finally chosen solution does not work anymore.
# ### This new script will use a mapping already done between the Belgian Postcodes and their location (Job done by Jean-Francois Monfort) ; I let anyway below my old code in comments that can be easily reused in case this mapping would not be available anymore, or simply if the same job has to be done for another region of the World.
#
# # Recup des postcode
# df=pd.read_excel(r".\3.Analyses\AllCompanyInfosSortedByPostCodeWithoutDuplicate.xls")
# occurences=df["Postcode"].value_counts()
# print(occurences.head(5))
# postcodes=df["Postcode"]
# postcodes = postcodes.drop_duplicates(keep = "last")
# #postcodes=postcodes.head(3) #A virer à la fin, je fais ça pour gagner du temps
# list_postcodes=postcodes.tolist()
#
# #df_locator=pd.read_csv(r".\4.Locate\zipcode-belgium.csv", header=None)
# df_locator=pd.read_csv(r".\4.Locate\zipcode-belgium.csv", names=["Postcode","City","Longitude","Latitude"])
# df_locator = df_locator.drop_duplicates(subset ="Postcode", keep = "first")#In Belgium, several (super close) areas get the same Postcode
# df_locator.set_index("Postcode",drop=True,inplace=True)#We replace the index of rows (0,1,2...) by the postcode directly (to facilitate the next operations)
#
#
# #print(df_locator.head())
# current=df_locator.loc[[1000,1020,1030]]
#
# # longitudes=[]
# # latitudes=[]
# #
# # for i in postcodes:
# #     print("a")
# #     current=df_locator.iloc[i]#df_locator[df_locator["Postcode"]==i]
# #     print(i)
# #     longitudes.append(current.loc["Longitude"])
# #     latitudes.append(current.loc["Latitude"])
#
# # for i in postcodes:
# #     df_locator["Postcode"==i]
# #     longitudes.append()
# #
# #     list_long_lat[j] = geo.to_crs({'init': 'epsg:3395'}) #On traduit dans les coordonnées sur la carte de Mercator
# #
# #
# #
# # x=list(range(0,len(list_long_lat)))
# # y=list(range(0,len(list_long_lat)))
# # for i in list(range(0,len(list_long_lat))):
# #     x[i]=list_long_lat[i].loc[0,"geometry"].x
# #     y[i]=list_long_lat[i].loc[0,"geometry"].y
# #
# # intensity=occurences.sort_index().tolist() #Va servir pour faire le s du scatter
# #
# #
# # locations=pd.DataFrame()
# # locations["Postcode"]=list_postcodes
# # locations["x"]=x
# # locations["y"]=y
# # locations["intensity"]=intensity
# # locations.to_csv(r".\4.Locate\LocationsAndIntensityWithAberations.csv")


### The finally chosen solution does not work SUPER well (~3% errors because I could not enforce the country while doing the request to nominatim using Python (the problem is easily solved with other languages, and I realized in the meantime another developer [Jean-Francois Monfort] already did this kind of job for Belgium so I could reuse his work ; edit: not all postcodes are present in his work => I stay with my sol
### I therefore chose to use the data found online without apparent errors (with cross-checking of the 97% I know I got right)
