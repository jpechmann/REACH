import arcpy
import pandas as pd
import os

"""
This script creates summary tables for each priority need by sector. It then creates the fields needed for the maps, and joins the tables to geospatial layers. 
"""

###CHANGE THESE INPUTS MONTHLY##
roundNumber = '40'
monthYear = 'October2018'

#admin3 feature layer
admin3 = "Z:\SYR\Common_Geodatabase\HSOS\HSOS_Geodatabase.gdb\Admin3"
admin3_joinField = 'admin3Pcod'
#Allow for overwriting
arcpy.env.overwriteOutput = True

OriginalinputCSV = r'Z:\\SYR\\Projects\\13BVJ_AoO\\Activities\\Round{0}_{1}\\GIS\\PriorityNeeds_Maps\\HSOS_Round{0}_{1}_Dataset_Final_PriorityNeedsMaps.csv'.format(roundNumber,monthYear)

#If gdb does not exist for round, create it.
var = arcpy.Exists(r'Z:\\SYR\\Projects\\13BVJ_AoO\\Activities\\Round{0}_{1}\\GIS\\PriorityNeeds_Maps\\HSOS_Round{0}_PriorityNeeds_DataProcessing.gdb'.format(roundNumber,monthYear))
if not var:
    gdbFolder = r'Z:\\SYR\\Projects\\13BVJ_AoO\\Activities\\Round{0}_{1}\\GIS\\PriorityNeeds_Maps'.format(roundNumber,monthYear)
    gdbName = 'HSOS_Round{0}_PriorityNeeds_DataProcessing.gdb'.format(roundNumber)
    arcpy.CreateFileGDB_management(gdbFolder,gdbName)

#SET WORKSPACE
arcpy.env.workspace = r'Z:\\SYR\\Projects\\13BVJ_AoO\\Activities\\Round{0}_{1}\\GIS\\PriorityNeeds_Maps\\HSOS_Round{0}_PriorityNeeds_DataProcessing.gdb'.format(roundNumber,monthYear)
workspace =  r'Z:\\SYR\\Projects\\13BVJ_AoO\\Activities\\Round{0}_{1}\\GIS\\PriorityNeeds_Maps\HSOS_Round{0}_PriorityNeeds_DataProcessing.gdb'.format(roundNumber,monthYear)

#Allow for overwriting
arcpy.env.overwriteOutput = True

print("Yalla!!")

##FOOD##
dataFrame = pd.DataFrame.from_csv(OriginalinputCSV)

#Aggregate to subdistrict and count records listing Yes for food
tups = [('count', 'size'), ('Food_security', lambda x: (x=='Yes').sum())]
dataFrame = dataFrame.groupby('Subdistrict_Assessed_location')['Food_security'].agg(tups).reset_index()
#export to csv
dataFrame.to_csv(r'Z:\\SYR\\Projects\\13BVJ_AoO\\Activities\\Round{0}_{1}\\GIS\\PriorityNeeds_Maps\PriorityNeeds_Round{0}_Food.csv'.format(roundNumber,monthYear))

#Create table in gdb
inputCSV = r'Z:\\SYR\\Projects\\13BVJ_AoO\\Activities\\Round{0}_{1}\\GIS\\PriorityNeeds_Maps\PriorityNeeds_Round{0}_Food.csv'.format(roundNumber,monthYear)
arcpy.TableToTable_conversion(inputCSV,workspace,"Food_Table")

#add empty fields for percentages - numeric percentage and string fraction (for table frame)
field = "Food_Percent"
type = "DOUBLE"
table = "Food_Table"
arcpy.AddField_management(table,field,type)
field = "Food_Fraction"
type = "TEXT"
arcpy.AddField_management(table,field,type)

#Calcualte fields
Percentage_Expression = "!Food_security! / !count!"
Fraction_Expression = "'!Food_security!' +'/'+ '!count!'"
arcpy.CalculateField_management(table,"Food_Percent",Percentage_Expression)
arcpy.CalculateField_management(table,"Food_Fraction",Fraction_Expression)
print("Food table created")

##Water##
dataFrame = pd.DataFrame.from_csv(OriginalinputCSV)

#Aggregate to subdistrict and count records listing Yes for Water_access
tups = [('count', 'size'), ('Water_access', lambda x: (x=='Yes').sum())]
dataFrame = dataFrame.groupby('Subdistrict_Assessed_location')['Water_access'].agg(tups).reset_index()
#export to csv
dataFrame.to_csv(r'Z:\\SYR\\Projects\\13BVJ_AoO\\Activities\\Round{0}_{1}\\GIS\\PriorityNeeds_Maps\PriorityNeeds_Round{0}_Water.csv'.format(roundNumber,monthYear))

#Create table in gdb
inputCSV = r'Z:\\SYR\\Projects\\13BVJ_AoO\\Activities\\Round{0}_{1}\\GIS\\PriorityNeeds_Maps\PriorityNeeds_Round{0}_Water.csv'.format(roundNumber,monthYear)
arcpy.TableToTable_conversion(inputCSV,workspace,"Water_Table")

#add empty fields for percentages - numeric percentage and string fraction (for table frame)
field = "Water_Percent"
type = "DOUBLE"
table = 'Water_Table'
arcpy.AddField_management(table,field,type)
field = "Water_Fraction"
type = "TEXT"
arcpy.AddField_management(table,field,type)

#Calcualte fields
Percentage_Expression = "!Water_access! / !count!"
Fraction_Expression = "'!Water_access!' +'/'+ '!count!'"
arcpy.CalculateField_management(table,"Water_Percent",Percentage_Expression)
arcpy.CalculateField_management(table,"Water_Fraction",Fraction_Expression)
print("Water table created")

##Hygiene_sanitation##
dataFrame = pd.DataFrame.from_csv(OriginalinputCSV)

#Aggregate to subdistrict and count records listing Yes for Water_access
tups = [('count', 'size'), ('Hygiene_sanitation', lambda x: (x=='Yes').sum())]
dataFrame = dataFrame.groupby('Subdistrict_Assessed_location')['Hygiene_sanitation'].agg(tups).reset_index()
#export to csv
dataFrame.to_csv(r'Z:\\SYR\\Projects\\13BVJ_AoO\\Activities\\Round{0}_{1}\\GIS\\PriorityNeeds_Maps\PriorityNeeds_Round{0}_Hygiene.csv'.format(roundNumber,monthYear))

#Create table in gdb
inputCSV = r'Z:\\SYR\\Projects\\13BVJ_AoO\\Activities\\Round{0}_{1}\\GIS\\PriorityNeeds_Maps\PriorityNeeds_Round{0}_Hygiene.csv'.format(roundNumber,monthYear)
arcpy.TableToTable_conversion(inputCSV,workspace,"Hygiene_Table")

#add empty fields for percentages - numeric percentage and string fraction (for table frame)
field = "Hygiene_Percent"
type = "DOUBLE"
table = 'Hygiene_Table'
arcpy.AddField_management(table,field,type)
field = "Hygiene_Fraction"
type = "TEXT"
arcpy.AddField_management(table,field,type)

#Calcualte fields
Percentage_Expression = "!Hygiene_sanitation! / !count!"
Fraction_Expression = "'!Hygiene_sanitation!' +'/'+ '!count!'"
arcpy.CalculateField_management(table,"Hygiene_Percent",Percentage_Expression)
arcpy.CalculateField_management(table,"Hygiene_Fraction",Fraction_Expression)
print("Hygiene table created")

##Healthcare##
dataFrame = pd.DataFrame.from_csv(OriginalinputCSV)

#Aggregate to subdistrict and count records listing Yes for Water_access
tups = [('count', 'size'), ('Healthcare', lambda x: (x=='Yes').sum())]
dataFrame = dataFrame.groupby('Subdistrict_Assessed_location')['Healthcare'].agg(tups).reset_index()
#export to csv
dataFrame.to_csv(r'Z:\\SYR\\Projects\\13BVJ_AoO\\Activities\\Round{0}_{1}\\GIS\\PriorityNeeds_Maps\PriorityNeeds_Round{0}_Healthcare.csv'.format(roundNumber,monthYear))

#Create table in gdb
inputCSV = r'Z:\\SYR\\Projects\\13BVJ_AoO\\Activities\\Round{0}_{1}\\GIS\\PriorityNeeds_Maps\PriorityNeeds_Round{0}_Healthcare.csv'.format(roundNumber,monthYear)
arcpy.TableToTable_conversion(inputCSV,workspace,"Healthcare_Table")

#add empty fields for percentages - numeric percentage and string fraction (for table frame)
field = "Healthcare_Percent"
type = "DOUBLE"
table = 'Healthcare_Table'
arcpy.AddField_management(table,field,type)
field = "Healthcare_Fraction"
type = "TEXT"
arcpy.AddField_management(table,field,type)

#Calcualte fields
Percentage_Expression = "!Healthcare! / !count!"
Fraction_Expression = "'!Healthcare!' +'/'+ '!count!'"
arcpy.CalculateField_management(table,"Healthcare_Percent",Percentage_Expression)
arcpy.CalculateField_management(table,"Healthcare_Fraction",Fraction_Expression)
print("Healthcare table created")

##Education##
dataFrame = pd.DataFrame.from_csv(OriginalinputCSV)

#Aggregate to subdistrict and count records listing Yes for Water_access
tups = [('count', 'size'), ('Education', lambda x: (x=='Yes').sum())]
dataFrame = dataFrame.groupby('Subdistrict_Assessed_location')['Education'].agg(tups).reset_index()
#export to csv
dataFrame.to_csv(r'Z:\\SYR\\Projects\\13BVJ_AoO\\Activities\\Round{0}_{1}\\GIS\\PriorityNeeds_Maps\PriorityNeeds_Round{0}_Education.csv'.format(roundNumber,monthYear))

#Create table in gdb
inputCSV = r'Z:\\SYR\\Projects\\13BVJ_AoO\\Activities\\Round{0}_{1}\\GIS\\PriorityNeeds_Maps\PriorityNeeds_Round{0}_Education.csv'.format(roundNumber,monthYear)
arcpy.TableToTable_conversion(inputCSV,workspace,"Education_Table")

#add empty fields for percentages - numeric percentage and string fraction (for table frame)
field = "Education_Percent"
type = "DOUBLE"
table = 'Education_Table'
arcpy.AddField_management(table,field,type)
field = "Education_Fraction"
type = "TEXT"
arcpy.AddField_management(table,field,type)

#Calcualte fields
Percentage_Expression = "!Education! / !count!"
Fraction_Expression = "'!Education!' +'/'+ '!count!'"
arcpy.CalculateField_management(table,"Education_Percent",Percentage_Expression)
arcpy.CalculateField_management(table,"Education_Fraction",Fraction_Expression)
print("Education table created")

##Shelter##
dataFrame = pd.DataFrame.from_csv(OriginalinputCSV)

#Aggregate to subdistrict and count records listing Yes for Water_access
tups = [('count', 'size'), ('Shelter', lambda x: (x=='Yes').sum())]
dataFrame = dataFrame.groupby('Subdistrict_Assessed_location')['Shelter'].agg(tups).reset_index()
#export to csv
dataFrame.to_csv(r'Z:\\SYR\\Projects\\13BVJ_AoO\\Activities\\Round{0}_{1}\\GIS\\PriorityNeeds_Maps\PriorityNeeds_Round{0}_Shelter.csv'.format(roundNumber,monthYear))

#Create table in gdb
inputCSV = r'Z:\\SYR\\Projects\\13BVJ_AoO\\Activities\\Round{0}_{1}\\GIS\\PriorityNeeds_Maps\PriorityNeeds_Round{0}_Shelter.csv'.format(roundNumber,monthYear)
arcpy.TableToTable_conversion(inputCSV,workspace,"Shelter_Table")

#add empty fields for percentages - numeric percentage and string fraction (for table frame)
field = "Shelter_Percent"
type = "DOUBLE"
table = 'Shelter_Table'
arcpy.AddField_management(table,field,type)
field = "Shelter_Fraction"
type = "TEXT"
arcpy.AddField_management(table,field,type)

#Calcualte fields
Percentage_Expression = "!Shelter! / !count!"
Fraction_Expression = "'!Shelter!' +'/'+ '!count!'"
arcpy.CalculateField_management(table,"Shelter_Percent",Percentage_Expression)
arcpy.CalculateField_management(table,"Shelter_Fraction",Fraction_Expression)
print("Shelter table created")

##NFI##
dataFrame = pd.DataFrame.from_csv(OriginalinputCSV)

#Aggregate to subdistrict and count records listing Yes for Water_access
tups = [('count', 'size'), ('NFI', lambda x: (x=='Yes').sum())]
dataFrame = dataFrame.groupby('Subdistrict_Assessed_location')['NFI'].agg(tups).reset_index()
#export to csv
dataFrame.to_csv(r'Z:\\SYR\\Projects\\13BVJ_AoO\\Activities\\Round{0}_{1}\\GIS\\PriorityNeeds_Maps\PriorityNeeds_Round{0}_NFI.csv'.format(roundNumber,monthYear))

#Create table in gdb
inputCSV = r'Z:\\SYR\\Projects\\13BVJ_AoO\\Activities\\Round{0}_{1}\\GIS\\PriorityNeeds_Maps\PriorityNeeds_Round{0}_NFI.csv'.format(roundNumber,monthYear)
arcpy.TableToTable_conversion(inputCSV,workspace,"NFI_Table")

#add empty fields for percentages - numeric percentage and string fraction (for table frame)
field = "NFI_Percent"
type = "DOUBLE"
table = 'NFI_Table'
arcpy.AddField_management(table,field,type)
field = "NFI_Fraction"
type = "TEXT"
arcpy.AddField_management(table,field,type)

#Calcualte fields
Percentage_Expression = "!NFI! / !count!"
Fraction_Expression = "'!NFI!' +'/'+ '!count!'"
arcpy.CalculateField_management(table,"NFI_Percent",Percentage_Expression)
arcpy.CalculateField_management(table,"NFI_Fraction",Fraction_Expression)
print("NFI table created")

##Protection##
dataFrame = pd.DataFrame.from_csv(OriginalinputCSV)

#Aggregate to subdistrict and count records listing Yes for Water_access
tups = [('count', 'size'), ('Protection', lambda x: (x=='Yes').sum())]
dataFrame = dataFrame.groupby('Subdistrict_Assessed_location')['Protection'].agg(tups).reset_index()
#export to csv
dataFrame.to_csv(r'Z:\\SYR\\Projects\\13BVJ_AoO\\Activities\\Round{0}_{1}\\GIS\\PriorityNeeds_Maps\PriorityNeeds_Round{0}_Protection.csv'.format(roundNumber,monthYear))

#Create table in gdb
inputCSV = r'Z:\\SYR\\Projects\\13BVJ_AoO\\Activities\\Round{0}_{1}\\GIS\\PriorityNeeds_Maps\PriorityNeeds_Round{0}_Protection.csv'.format(roundNumber,monthYear)
arcpy.TableToTable_conversion(inputCSV,workspace,"Protection_Table")

#add empty fields for percentages - numeric percentage and string fraction (for table frame)
field = "Protection_Percent"
type = "DOUBLE"
table = 'Protection_Table'
arcpy.AddField_management(table,field,type)
field = "Protection_Fraction"
type = "TEXT"
arcpy.AddField_management(table,field,type)

#Calcualte fields
Percentage_Expression = "!Protection! / !count!"
Fraction_Expression = "'!Protection!' +'/'+ '!count!'"
arcpy.CalculateField_management(table,"Protection_Percent",Percentage_Expression)
arcpy.CalculateField_management(table,"Protection_Fraction",Fraction_Expression)
print("Protection table created")

##Nutrition##
dataFrame = pd.DataFrame.from_csv(OriginalinputCSV)

#Aggregate to subdistrict and count records listing Yes for Water_access
tups = [('count', 'size'), ('Nutrition', lambda x: (x=='Yes').sum())]
dataFrame = dataFrame.groupby('Subdistrict_Assessed_location')['Nutrition'].agg(tups).reset_index()
#export to csv
dataFrame.to_csv(r'Z:\\SYR\\Projects\\13BVJ_AoO\\Activities\\Round{0}_{1}\\GIS\\PriorityNeeds_Maps\PriorityNeeds_Round{0}_Nutrition.csv'.format(roundNumber,monthYear))

#Create table in gdb
inputCSV = r'Z:\\SYR\\Projects\\13BVJ_AoO\\Activities\\Round{0}_{1}\\GIS\\PriorityNeeds_Maps\PriorityNeeds_Round{0}_Nutrition.csv'.format(roundNumber,monthYear)
arcpy.TableToTable_conversion(inputCSV,workspace,"Nutrition_Table")

#add empty fields for percentages - numeric percentage and string fraction (for table frame)
field = "Nutrition_Percent"
type = "DOUBLE"
table = 'Nutrition_Table'
arcpy.AddField_management(table,field,type)
field = "Nutrition_Fraction"
type = "TEXT"
arcpy.AddField_management(table,field,type)

#Calcualte fields
Percentage_Expression = "!Nutrition! / !count!"
Fraction_Expression = "'!Nutrition!' +'/'+ '!count!'"
arcpy.CalculateField_management(table,"Nutrition_Percent",Percentage_Expression)
arcpy.CalculateField_management(table,"Nutrition_Fraction",Fraction_Expression)
print("Nutrition table created")

#Join tables to admin3
layerName = "admin3_Layer"
outFeature= "admin3_AllJoined"

arcpy.MakeFeatureLayer_management(admin3,layerName)
arcpy.AddJoin_management(layerName,admin3_joinField,"Education_Table","Subdistrict_Assessed_location","KEEP_ALL")
arcpy.AddJoin_management(layerName,admin3_joinField,"Food_Table","Subdistrict_Assessed_location","KEEP_ALL")
arcpy.AddJoin_management(layerName,admin3_joinField,"Healthcare_Table","Subdistrict_Assessed_location","KEEP_ALL")
arcpy.AddJoin_management(layerName,admin3_joinField,"Hygiene_Table","Subdistrict_Assessed_location","KEEP_ALL")
arcpy.AddJoin_management(layerName,admin3_joinField,"NFI_Table","Subdistrict_Assessed_location","KEEP_ALL")
arcpy.AddJoin_management(layerName,admin3_joinField,"Nutrition_Table","Subdistrict_Assessed_location","KEEP_ALL")
arcpy.AddJoin_management(layerName,admin3_joinField,"Protection_Table","Subdistrict_Assessed_location","KEEP_ALL")
arcpy.AddJoin_management(layerName,admin3_joinField,"Shelter_Table","Subdistrict_Assessed_location","KEEP_ALL")
arcpy.AddJoin_management(layerName,admin3_joinField,"Water_Table","Subdistrict_Assessed_location","KEEP_ALL")
print("All tables joined")

## Remove fields that are not needed
listEventsTables = arcpy.ListTables(layerName)
fieldMappings = arcpy.FieldMappings()

for table in listEventsTables:
    fieldMappings.addTable(table)

#remove fields that are not needed
for field in fieldMappings.fields:
    if field.name not in ["admin1Name","admin1Pcod","admin2Name","admin2Pcod","admin3Name","admin3Pcod","Region","Subdistrict_Assessed_location","count","Education","Education_Percent","Education_Fraction"]:
        fieldMappings.removeFieldMap(fieldMappings.findFieldMapIndex(field.name))

print(fieldMappings)

#arcpy.CopyFeatures_management(layerName,outFeature)
arcpy.FeatureClassToFeatureClass_conversion(layerName,workspace,outFeature,None,fieldMappings)

arcpy.Delete_management(layerName)

print(outFeature+" Exported!")
