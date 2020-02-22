import pandas as pd

# Script #3
# Cleaner and Analyzer

## PART 1: cleaning

df = pd.read_excel(r".\2.Big_table\AllCompanyInfos.xls")

print(df.shape)

df= df.astype({"Company":"str"})#Cast everything to str so that we can work on the column by comparison

print(df.shape)

df = df.drop_duplicates(subset ="Company", keep = "last") #Remove duplicates and maintain the last occurence (supposing the list was created by chronological order)
print(df.shape)

df=df.sort_values("Company")
df=df[df["Company"]!="False"] #We just have to hope that noone called his company "False" in Wallonia.
df=df[df["Company"]!="nan"] #Same here that noone called his company "nan", "-" or "---"
df=df[df["Company"]!="-"]
df=df[df["Company"]!="---"]

print(df.shape)

## PART 2 : Saving
#Save all the companies sorted by alphabetical order
df.to_excel(r".\3.Analyses\AllCompanyInfosSortedByAlphabeticalOrderWithoutDuplicate.xls")

print(df["Postcode"].value_counts())

#Save all the companies sorted by postcode (increasingly)
df=df.sort_values("Postcode")
df=df[df["Postcode"]!=0] #Loose 100 out of 17349 (=> 17249 left) so that stay consistent with what's plotted later
df.to_excel(r".\3.Analyses\AllCompanyInfosSortedByPostCodeWithoutDuplicate.xls")

print(df.shape)

## PART 3: Analyzing the cleaned collected data
numberOfCompanies=df.shape[0]

#Investigating the legal structure behind the companies
legalType=df["Type"].value_counts()
proportions_legalType=df["Type"].value_counts("S.A.")

#Counting how many companies provide a website to visit
numberOfCompaniesWithWebsite=df["Web Site"].count()
print("Number of websites given: "+str(numberOfCompaniesWithWebsite)) #number of non-nan values in a series https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.count.html#pandas.Series.count

#Counting how many websites given end by .be or .be/ to offer an overview of domain choices
mask=df["Web Site"].str.endswith((".be",".be/"), na=False)#We do not forget to allow an URL ending by "/" (which recover 6436-6417 URL, so not that much in our case)
df_temp=df[mask]
numberOfCompaniesWithWebsiteEndingByDotbe=df_temp.shape[0]
print("Number of websites ending with .be: "+str(numberOfCompaniesWithWebsiteEndingByDotbe))

#Counting how many companies provide an email to be contacted
numberOfCompaniesWithEmail=df["E-Mail"].count()
print("Number of emails retrieved: "+str(numberOfCompaniesWithEmail))

#Counting how many companies provide a phone number to call
df_temp=df[df["Phone"]!="32-(0)"]
numberOfCompaniesWithValidPhoneNumber=df_temp.shape[0]
print("Number of valid phone numbers: "+str(numberOfCompaniesWithValidPhoneNumber))

#Giving stats
proportionWithWebsite = round(numberOfCompaniesWithWebsite/numberOfCompanies, 2)
#proportionWithWebsiteEndingByDotbe = round(numberOfCompaniesWithWebsiteEndingByDotbe/numberOfCompanies, 2)
proportionOfWebsiteEndingByDotbe = round(numberOfCompaniesWithWebsiteEndingByDotbe/numberOfCompaniesWithWebsite,2)
proportionWithValidPhoneNumber = round(numberOfCompaniesWithValidPhoneNumber/numberOfCompanies,2)
proportionWithEmail = round(numberOfCompaniesWithEmail/numberOfCompanies,2)

print("Proportion of companies which provide a website: "+str(proportionWithWebsite))
#print("Proportion of companies with websites ending by .be: "+str(proportionWithWebsiteEndingByDotbe))
print("Proportion of websites ending by .be: "+str(proportionOfWebsiteEndingByDotbe))
print("Proportion of companies which provide an email: "+str(proportionWithEmail))
print("Proportion of companies which provide a phone number: "+str(proportionWithValidPhoneNumber))

proportion_SA= round(proportions_legalType["S.A."],4)
proportion_SPRL= round(proportions_legalType["S.P.R.L."],4)
proportion_PersonnePhysique= round(proportions_legalType["Personne Physique"],4)
proportion_ASBL= round(proportions_legalType["A.S.B.L."],4)
proportion_Autre= round(1-proportion_SA-proportion_SPRL-proportion_PersonnePhysique-proportion_ASBL,4)

print("\nIn the dataset, there is \n\t"+str(proportion_SA*100)+"% of S.A.,\n\t"
                                                           ""+str(proportion_SPRL*100)+"% of S.P.R.L.,\n\t"
                                                                                     ""+str(proportion_PersonnePhysique*100)+"% of Personne Physique,\n\t"
                                                                                                               ""+str(proportion_ASBL*100)+"% of ASBL,\n\t"
                                                                                                                                         ""+str(proportion_Autre*100)+"% of Other legal structure")

\print("End of stats")