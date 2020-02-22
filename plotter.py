import pandas as pd
import geopandas as gpd
from geopandas.tools import geocode
# import matplotlib
import matplotlib.pyplot as plt

# Script #5
# Plotter
# This is the longest script of all 5, it will be therefore splitted in several parts to explain what's done at each step
# Input : A gpkg file with Belgium borders (Pay attention to use this format, I initially started with a shapefile without any knowledge but it was shown later that this format is becoming obsolete)
# You also need the output from locator.py with the zipcodes locations and their intensity
# Output : A plotted bubble map that highlight the areas of high interest in exportation with colors used to seperate the different provinces (see the legend of the graph)
# In the meantime, badly located points are removed and corrected when it concerned more than 10 companies at the given zipcode (trade-off time-requested/interest in the analysis)

belgium_map_data = gpd.read_file(r".\5.Plots\gadm36_BEL_gpkg\gadm36_BEL.gpkg") #Find the up to date file at https://gadm.org/download_country_v3.html

belgium_projected = belgium_map_data.to_crs({'init': 'epsg:3395'}) #Transforming from the Robinson to the Mercator convention to obtain a more usual form of Belgium
# Pay attention it will be required to do the same with future data we'll add on the map ! If you used locator.py, it is already done.

## PART 1: IMPORT
# Import the x,y and intensity from 4.Locate (a dataframe there in a csv file)
locationsData=pd.read_csv(r".\4.Locate\LocationsAndIntensityWithAberations.csv")
x=locationsData["x"].tolist()
y=locationsData["y"].tolist()
intensity=locationsData["intensity"].tolist()
print("There are "+str(sum(intensity))+" companies in total")
postcodes=locationsData["Postcode"].tolist()


## PART 2: Cleaning and correcting mislocations

# print(min(x)) #debug (purposes in case of mislocation)
# print(min(y))
#Computing coordinates of what Nominatim (OSM) returns for "Belgium", it will help us if it did not read the postcode
#edit: I did not require it because nominatim was totally accurate or completely not, but a good way if you decide to choose another locator is to think about a circle around the middle of Belgium and remove all data outside
geo = geocode("Belgium", provider='nominatim')
geo_mercator=geo.to_crs({'init': 'epsg:3395'})
x_belgium=geo_mercator.loc[0,"geometry"].x
y_belgium=geo_mercator.loc[0,"geometry"].y

#Remove aberrant locations
count=0 #Number of postcodes
countCompanies=0 #Number of companies affected
badlyLocatedPostcode=[] #Will store the badly located postcode
badlyLocatedIntensity=[] #Will store the number of companies at the badly located postcode

iterator=0
end=len(x)
while iterator<end:
    #There are 2 types of error met : 1)Zipcode + Belgium = another place on Earth (usually the USA) ; 2)Zipcode + Belgium = Belgium for the interpreter, thus stacking points at the center of Belgium, we clean it and we'll re-add it later when sufficiently big
    if x[iterator] < 0 or y[iterator] < 0 or (abs(x[iterator]-x_belgium)<10^(0) and abs(y[iterator]-y_belgium)<10^(0)):
        print("------------------")
        print("Postcode:" +str(postcodes[iterator]))
        print("Number of companies concerned: "+str(intensity[iterator]))
        # print(abs(x[iterator]-x_belgium))
        # print(abs(y[iterator]-y_belgium))
        badlyLocatedPostcode.append(postcodes[iterator]) #We store what's wrong to quantify it and probably reuse it
        badlyLocatedIntensity.append(intensity[iterator]) #We store what's wrong to quantify it and probably reuse it

        countCompanies += intensity[iterator]
        del x[iterator]
        del y[iterator]
        del postcodes[iterator] #Do not forget this, it won't change the map but will change what's printed to say which location are missing !
        del intensity[iterator]
        count += 1
        iterator-=1#We will add 1 anyway, but we want not to move the index
        end-=1 #We cannot use a for loop because the list is reduced sometimes, so we avoid to look too far
    iterator+=1



print("Removed "+str(count)+" points which were badly located based on their postcode")
print(str(countCompanies)+" companies removed in the meantime") #number of companies that were removed from the dataset due to bad location of their postcode

#Manually adding mislocated places with >10 companies to reach a 99%+ accuracy
#Pay attention to take exactly a 3395 as the ID of the Mercator Convention used to convert !! (To stay consistent with everything as so plotting adequatly)
#7000,Mons,3.951958,50.4549568 #not managed by Nominatim
postcodes.append(7000)#Note it will directly be in the pool with the other ones from the same province
x.append(439929.95) #https://epsg.io/transform#s_srs=4326&t_srs=3857
y.append(6525442.35) #https://epsg.io/transform#s_srs=4326&t_srs=3857
intensity.append(292)

#The next ones are mainly the ones misinterpreted with the geographical center of Belgium according to Nominatim
#The most credible explanation of why we observed this problem at this place is linked with the history of Belgium: in the area around Louvain-la-Neuve (city created around 1970) a lot of companies emerged alongside the development of the new uni. All the old postal system did not take this major place into account and so probably the situation was the same for the maps with a mismatch of the exact locations

#7000,Wavre,50.7159° N, 4.6128° E
postcodes.append(1300)
x.append(513494.55) #through https://epsg.io/
y.append(6538099.78)
intensity.append(393)

#1325,Corroy-le-Grand,50.6621° N, 4.6746° E
postcodes.append(1325)
x.append(520374.09)
y.append(6528671.91)
intensity.append(74)

#1348,Ottignies-Louvain-la-Neuve,50.6681° N, 4.6118° E
postcodes.append(1348)
x.append(513383.23)
y.append(6529722.81)
intensity.append(363)

#1435,Mont-Saint-Guibert,50.6347° N, 4.6106° E
postcodes.append(1435)
x.append(513249.64)
y.append(6523874.53)
intensity.append(147)

#1450,Chastre,50.6081° N, 4.6357° E
postcodes.append(1450)
x.append(516043.76)
y.append(6519219.91)
intensity.append(31)

#1457,Walhain,50.6165° N, 4.6954° E
postcodes.append(1457)
x.append(522689.54)
y.append(6520689.50)
intensity.append(47)

#1490,Court-Saint-Étienne,50.6209° N, 4.5599° E
postcodes.append(1490)
x.append(507605.75)
y.append(6521459.40)
intensity.append(46)

#4317,Faimes,50.6618° N, 5.2601° E
postcodes.append(4317)
x.append(585551.65)
y.append(6528619.37)
intensity.append(14)

#4683,Oupeye,50.7085° N, 5.6468° E
postcodes.append(4683)
x.append(628598.90)
y.append(6536802.37)
intensity.append(22)

#5030,Gembloux,50.5652° N, 4.6884° E
postcodes.append(5030)
x.append(521910.30)
y.append(6511718.59)
intensity.append(159)


tosum=[i for i in badlyLocatedIntensity if i>10]#The ones I corrected
print("Recovered manually: "+str(sum(tosum)) + " Companies") #Quantification of what was corrected
print("Now we have only 1637-1588=49 companies missing out of 17249 (less than 0.3 % ; good enough rate)")#Could be automated, but i think that if it was wrong in the future, a deep manual analysis would be required again to spot the problem

#Reordering the postcodes AND the x,y, intensity lists to do not mismatch data

temp_components = {"Postcode" : postcodes, "x":x, "y":y, "intensity":intensity}
temp_df=pd.DataFrame(temp_components)
temp_df=temp_df.sort_values(by=["Postcode"]) #We sort the 4 "lists" by focusing on the postcode
postcodes=temp_df["Postcode"].tolist()
x=temp_df["x"].tolist()
y=temp_df["y"].tolist()
intensity=temp_df["intensity"].tolist()

#Now we know our data are finally cleaned, and ordered in a chronological postcode order


## PART 3: Slitting the data points by province in order to highlight procinves effect in our data

#Splitting the lists to plot in different colors based on the province
#Visit https://en.wikipedia.org/wiki/List_of_postal_codes_in_Belgium for more info

# Not needed anymore, because do not solve the problem of discontinued postcode for 1 province (particularity known for the Hainaut in our dataset)
# But I let it there anyway because it can be easily used again in another country without this particularity
# def splitIntList(toSplit,maxValue):
#     #This function will take as argument a list of increasing numbers and an integer representig the max value
#     #It will return the index of the highest value that is below or equal to the maxValue
#     iterator=0
#     while iterator+1<len(toSplit) and toSplit[iterator+1]<=maxValue:
#         iterator+=1
#     if iterator==0:
#         Print("Warning : The iterator did not move, maybe the value was already too big")
#     return iterator

# 1000–1299: Brussels Capital Region
# 1300–1499: Walloon Brabant
# 1500–1999: Flemish Brabant
# 2000–2999: Antwerp
# 3000–3499: Flemish Brabant (continued)
# 3500–3999: Limburg
# 4000–4999: Liège
# 5000–5999: Namur
# 6000–6599: Hainaut
# 6600–6999: Luxembourg
# 7000–7999: Hainaut (continued)
# 8000–8999: West Flanders
# 9000–9999: East Flanders

#Function which takes a list of postcodes (int/float) as argument and return a (string) list of same length with the corresponding province
def giveMeMyProvince(list_postcodes):
    toreturn=[""]*len(list_postcodes)
    current=list_postcodes[0]#prealloc
    for i in list(range(0,len(list_postcodes))):
        current=list_postcodes[i]
        if current < 1000:
            print("Warning: Please check the postcodes, there is a problem with a too low number")
        elif current < 1300:
            toreturn[i]="Brussels Capital Region"
        elif current < 1500:
            toreturn[i] = "Walloon Brabant"
        elif current < 2000:
            toreturn[i] = "Flemish Brabant"
        elif current < 3000:
            toreturn[i] = "Antwerp"
        elif current < 3500:
            toreturn[i] = "Flemish Brabant" #continued
        elif current < 4000:
            toreturn[i] = "Limburg"
        elif current < 5000:
            toreturn[i] = "Liège"
        elif current < 6000:
            toreturn[i] = "Namur"
        elif current < 6600:
            toreturn[i] = "Hainaut"
        elif current < 7000:
            toreturn[i] = "Luxembourg"
        elif current < 8000:
            toreturn[i] = "Hainaut" #continued
        elif current < 9000:
            toreturn[i] = "West Flanders"
        elif current < 10000:
            toreturn[i] = "East Flanders"
        else:
            print("Warning: Please check the postcodes, there is a problem with a too high number")
    return toreturn


#Merge the two "Hainaut" and the two "Flemish Brabant" due to discontinuity in postcode allocation in Belgium
#Todo
provinces=["Brussels Capital Region", "Walloon Brabant", "Flemish Brabant", "Antwerp", "Limburg", "Liège", "Namur", "Hainaut", "Luxembourg", "West Flanders", "East Flanders"]
provinces_of_postcodes=giveMeMyProvince(postcodes)

#Sort by province with a df, then convert to list, split in province again thanks to the solved discontinuity, then plot

temp_components = {"Postcode" : postcodes, "x":x, "y":y, "intensity":intensity, "Province":provinces_of_postcodes}
temp_df=pd.DataFrame(temp_components)
temp_df=temp_df.sort_values(by=["Province","Postcode"]) #We sort the 5 "lists" by focusing on the province first, then the exact postcode
postcodes=temp_df["Postcode"].tolist()
x=temp_df["x"].tolist()
y=temp_df["y"].tolist()
intensity=temp_df["intensity"].tolist()
provinces_of_postcodes=temp_df["Province"].tolist()

# brussels_max = splitIntList(postcodes,1299)
# walloon_brabant_max = splitIntList(postcodes,1499)
# flemish_brabant_max = splitIntList(postcodes,1999)
# antwerp_max = splitIntList(postcodes,2999)
# flemish_brabant_max_continued = splitIntList(postcodes,3499)#PAY ATTENTION
# limburg_max = splitIntList(postcodes,3999)
# liege_max = splitIntList(postcodes,4999)
# namur_max = splitIntList(postcodes,5999)
# hainaut_max = splitIntList(postcodes,6599)
# luxembourg_max = splitIntList(postcodes,6999)
# hainaut_max_continued = splitIntList(postcodes,7999)#PAY ATTENTION
#
# index_of_max=[brussels_max, walloon_brabant_max, flemish_brabant_max, antwerp_max, flemish_brabant_max_continued,
#               limburg_max, liege_max, namur_max, hainaut_max, luxembourg_max, hainaut_max_continued]

#Max by alphabetical order
brussels_max=max(loc for loc, val in enumerate(provinces_of_postcodes) if val == "Brussels Capital Region")
flemish_brabant_max = max(loc for loc, val in enumerate(provinces_of_postcodes) if val == "Flemish Brabant")
hainaut_max = max(loc for loc, val in enumerate(provinces_of_postcodes) if val == "Hainaut")
liege_max = max(loc for loc, val in enumerate(provinces_of_postcodes) if val == "Liège")
luxembourg_max = max(loc for loc, val in enumerate(provinces_of_postcodes) if val == "Luxembourg")
namur_max = max(loc for loc, val in enumerate(provinces_of_postcodes) if val == "Namur")
walloon_brabant_max = max(loc for loc, val in enumerate(provinces_of_postcodes) if val == "Walloon Brabant")

index_of_max=[brussels_max, flemish_brabant_max, hainaut_max, liege_max, luxembourg_max, namur_max, walloon_brabant_max]

print("Splitting based on postcodes and provinces: "+str(index_of_max))

# Prealloc + initialization of the first frame
postcodes_splitted=[postcodes[0:index_of_max[0]+1]] #init and first frame
x_splitted=[x[0:index_of_max[0]+1]] #init and first frame
y_splitted=[y[0:index_of_max[0]+1]] #init and first frame
intensity_splitted=[intensity[0:index_of_max[0]+1]] #init and first frame

# Filling the rest of the framing
for i in list(range(0,len(index_of_max)-1)):
    postcodes_splitted.append(postcodes[index_of_max[i]+1:index_of_max[i+1]+1])
    x_splitted.append(x[index_of_max[i] + 1:index_of_max[i + 1] + 1])
    y_splitted.append(y[index_of_max[i] + 1:index_of_max[i + 1] + 1])
    intensity_splitted.append(intensity[index_of_max[i] + 1:index_of_max[i + 1] + 1])


## Part 4: Plot

fig, ax = plt.subplots(figsize=(12,12))

belgium_projected["geometry"].plot(ax=ax,cmap='Oranges') #Printing the empty map with a light color

# 1000–1299: Brussels Capital Region
# 1300–1499: Walloon Brabant
# 1500–1999: Flemish Brabant
# 2000–2999: Antwerp
# 3000–3499: Flemish Brabant (continued)
# 3500–3999: Limburg
# 4000–4999: Liège
# 5000–5999: Namur
# 6000–6599: Hainaut
# 6600–6999: Luxembourg
# 7000–7999: Hainaut (continued)
# 8000–8999: West Flanders
# 9000–9999: East Flanders

provinces=["Brussels Capital Region", "Flemish Brabant", "Hainaut", "Liège", "Luxembourg", "Namur", "Walloon Brabant"]
colors=["tab:blue", "tab:brown", "tab:red", "tab:olive", "tab:grey", "tab:orange", "tab:purple", "tab:cyan", "tab:green"]

for i in list(range(0,len(x_splitted))):
    if provinces[i]=="Flemish Brabant": #highlighting flemish companies in walloon dataset
        plt.scatter(x_splitted[i], y_splitted[i], s=1000 * intensity_splitted[i], c=colors[i], label=provinces[i],
                    alpha=1.0)
    else:
        plt.scatter(x_splitted[i], y_splitted[i], s=1000 * intensity_splitted[i], c=colors[i], label=provinces[i], alpha=0.4)


plt.legend(loc = 'lower left', prop={'size': 12})
plt.axis('off')
plt.title("Firms Internationalization in Belgium: a Walloon Perspective", fontsize = 24)
plt.tight_layout()
plt.savefig(r".\5.Plots\Belgium_with_inner_borders.png")
plt.show()