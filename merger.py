import pandas as pd

# Script #2

###########################################################################
### The Following code will merge the different xls tables in a big one ###
###########################################################################

### IMPORTANT REMARK ###
# To make the following code working, you need to go on the 427th line of compdoc.py [xlrd package] ; this line is the following one:
# raise CompDocError("%s corruption: seen[%d] == %d" % (qname, s, self.seen[s]))
# The xlrd package is used by pandas to manage the excel files
# Otherwise you will encounter the error for sure and you will get stuck
# NB: If you find any proper solution please ping me!

#workbook = xlrd.open_workbook(r".\1.Results_from_AWEX_website\Results1_200.xls", on_demand = True)

number_of_inputs=250

df = pd.read_excel(r".\1.Results_from_AWEX_website\Results1_200.xls")
appended_df = pd.read_excel(r".\1.Results_from_AWEX_website\Results1_200.xls") #Init before the loop

for i in list(range(1,number_of_inputs)):
    df2 = pd.read_excel(r".\1.Results_from_AWEX_website\Results"+str(i*200+1)+"_"+str((i+1)*200)+ ".xls")
    appended_df=pd.concat([appended_df, df2])


appended_df.to_excel(r".\2.Big_table\AllCompanyInfos.xls", index=False) #Pour exporter à la fin vers un seul fichier xlsx ; EDIT: au final j'ai fais xls car la covnersion détruit un peu des caractères dans certaines cellules autrement

#This script does not do anything else except merging to do one thing at a time