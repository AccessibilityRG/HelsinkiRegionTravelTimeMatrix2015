# -*- coding: iso-8859-1 -*-

import geopandas as gpd
from fiona.crs import from_epsg
import sys, time

#Suoritusinfot:
def Aloitus():
    aika = time.asctime()
    teksti = "Aloitus: " + aika
    print(teksti)

def Valmis():
    aika = time.asctime()
    teksti = "Valmis: " + aika
    print(teksti)

def msg(Message):
    print(Message)

def virhe(Virheilmoitus):
    print(Virheilmoitus)
    sys.exit()

def ExDel(haettava):
    if arcpy.Exists(haettava):
        arcpy.Delete_management(haettava)

def main(OutLines, Origins, Destinations):

    # Set Accumulation
    Accumulation = ["Digiroa_aa", "Kokopva_aa", "Keskpva_aa", "Ruuhka_aa", "Pituus"]

    # Set GDBCheck to False
    gdbCheck = False    

    # Read files to geopandas
    msg("----------------------")
    Aloitus()
    msg("Read files to geopandas")

    geoOutLines = gpd.read_file(OutLines) 
    crs_lines = geoOutLines.crs # Poimitaan crs talteen tulostiedoston tallennusta varten
    geoOrigins = gpd.read_file(Origins)
    geoDestinations = gpd.read_file(Destinations)

    Valmis()
    msg("----------------------")


    OrigColumns = ["NameO","Kavely_O_T", "KavelDistO", "Kavely_T_P", "KavelMatkO", "Digiroa_aa", "Kokopva_aa", "Keskpva_aa", "Ruuhka_aa", "ID_orig"]
    DestColumns = ["NameD","Kavely_T_D", "KavelDistD", "Kavely_P_T", "KavelMatkD", "Parkkiaika", "ID_dest"]

    # Join files
    msg("----------------------")
    Aloitus()
    msg("Make a table join between datasets")

    OutLinesO = geoOutLines.merge(geoOrigins[OrigColumns], left_on='LahtoNimi', right_on='NameO')
    OutLinesOD = OutLinesO.merge(geoDestinations[DestColumns], left_on='KohdeNimi', right_on='NameD') ##joinODtoLines(OutLines, Origins, Destinations)

    # Rename YKR_IDs to from_id and to_id
    OutLinesOD = OutLinesOD.rename(columns={'ID_orig': 'from_id', 'ID_dest': 'to_id'})

    # Drop unnecessary columns
    OutLinesOD = OutLinesOD.drop(["NameO", "NameD"], 1) # poistetaan turhat sarakkeet

    Valmis()
    msg("----------------------")


    ##    except: # Jos ei onnistu, käytetään arcGIS työkalua
    ##        print "Joining with arcpy.JoinField_management "
    ##
    ##        arcpy.JoinField_management(OutLines, "LahtoNimi", Origins, "NameO", ["Kavely_O_T", "KavelDistO", "Kavely_T_P", "KavelMatkO", "Digiroa_aa", "Kokopva_aa", "Keskpva_aa", "Ruuhka_aa"])
    ##        arcpy.JoinField_management(OutLines, "KohdeNimi", Destinations, "NameD", ["Kavely_T_D", "KavelDistD", "Kavely_P_T", "KavelMatkD", "Parkkiaika"])

    Valmis()
    ##arcpy.SetProgressorPosition(75)
    msg("----------------------")

    
    msg("Suoritetaan Kokonaismatkaketjun laskenta")
    ##arcpy.SetProgressorLabel("KOKONAISMATKAKETJUN LASKENTA...Suoritetaan Kokonaismatkaketjun laskenta...") 
    Aloitus()

    ###############################
    #LASKETAAAN KOKONAISMATKAKETJU
    ###############################

    if "Digiroa_aa" in Accumulation:

        #Kenttien nimet vaihtelevat riippuen ollaanko geodatabasessa vai ei!!!
        if gdbCheck == True:
            OutLinesOD['Digiroa_aa'] = OutLinesOD['Total_Digiroa_aa']
        else:
            OutLinesOD['Digiroa_aa'] = OutLinesOD['Total_Digi']

        OutLinesOD['TotDigiroa'] = OutLinesOD['Kavely_O_T'] + OutLinesOD['Kavely_T_P'] +  OutLinesOD['Digiroa_aa']+ OutLinesOD['Parkkiaika'] + OutLinesOD['Kavely_P_T']+ OutLinesOD['Kavely_T_D']
        #data type on nyt float!


    if "Kokopva_aa" in Accumulation:

        #Kenttien nimet vaihtelevat riippuen ollaanko geodatabasessa vai ei!!!
        if gdbCheck == True:
            OutLinesOD['Kokopva_aa'] = OutLinesOD['Total_Kokopva_aa']
        else:
            OutLinesOD['Kokopva_aa'] = OutLinesOD['Total_Koko']

        OutLinesOD['TotKokopva'] = OutLinesOD['Kavely_O_T'] + OutLinesOD['Kavely_T_P'] +  OutLinesOD['Kokopva_aa']+ OutLinesOD['Parkkiaika'] + OutLinesOD['Kavely_P_T']+ OutLinesOD['Kavely_T_D']

##    arcpy.SetProgressorPosition(80)

    if "Keskpva_aa" in Accumulation:

        #Kenttien nimet vaihtelevat riippuen ollaanko geodatabasessa vai ei!!!
        if gdbCheck == True:
            OutLinesOD['Keskpva_aa'] = OutLinesOD['Total_Keskpva_aa']
        else:
            OutLinesOD['Keskpva_aa'] = OutLinesOD['Total_Kesk']

        OutLinesOD['TotKeskpva'] = OutLinesOD['Kavely_O_T'] + OutLinesOD['Kavely_T_P'] +  OutLinesOD['Keskpva_aa']+ OutLinesOD['Parkkiaika'] + OutLinesOD['Kavely_P_T']+ OutLinesOD['Kavely_T_D']

    if "Ruuhka_aa" in Accumulation:

        #Kenttien nimet vaihtelevat riippuen ollaanko geodatabasessa vai ei!!!
        if gdbCheck == True:
            OutLinesOD['Ruuhka_aa'] = OutLinesOD['Total_Ruuhka_aa']
        else:
            OutLinesOD['Ruuhka_aa'] = OutLinesOD['Total_Ruuh']

        OutLinesOD['TotRuuhka'] = OutLinesOD['Kavely_O_T'] + OutLinesOD['Kavely_T_P'] +  OutLinesOD['Ruuhka_aa']+ OutLinesOD['Parkkiaika'] + OutLinesOD['Kavely_P_T']+ OutLinesOD['Kavely_T_D']
    if "Pituus" in Accumulation: #Lasketaan kokonaismatka ja siirretään attribuutit loogisesti taulun loppuun

        OutLinesOD['Pituus_O_T'] = OutLinesOD['KavelDistO']
        OutLinesOD['Pituus_T_P'] = OutLinesOD['KavelMatkO']

        #Kenttien nimet vaihtelevat riippuen ollaanko geodatabasessa vai ei!!!
        if gdbCheck == True:
            OutLinesOD['Pituus_Ajo'] = OutLinesOD['Total_Pituus']
        else:
            OutLinesOD['Pituus_Ajo'] = OutLinesOD['Total_Pitu']

        OutLinesOD['Pituus_P_E'] = OutLinesOD['Parkkiaika']*(20.0/60*1000)    #arcpy: arcpy.CalculateField_management(OutLinesOD, "Pituus_P_E", "((!Parkkiaika! / 60) / 20) * 1000", "PYTHON", "")
        OutLinesOD['Pituus_P_T'] = OutLinesOD['KavelMatkD']
        OutLinesOD['Pituus_T_D'] = OutLinesOD['KavelDistD']
        OutLinesOD['Pituus_TOT'] = OutLinesOD['Pituus_O_T'] + OutLinesOD['Pituus_T_P'] + OutLinesOD['Pituus_Ajo'] + OutLinesOD['Pituus_P_E'] + OutLinesOD['Pituus_P_T'] + OutLinesOD['Pituus_T_D']


    #Poistetaan turhat kentat tiedostosta:

    OutLinesFinal = OutLinesOD.drop(["OriginID", "Destinatio", "Destinat_1", "KavelDistO", "KavelMatkO", "KavelMatkD", "KavelDistD", "Total_Digi","Total_Koko","Total_Kesk","Total_Ruuh", "Total_Pitu"], 1) # poistetaan turhat sarakkeet
    ##OutLinesFinal = OutLinesOD 

    ## Varmistetaan, että geodataframe on maaritetty oikein

    #Testioutput:
    #OutFile = r"C:\HY-Data\VUOKKHEI\documents\MetropAccess\DigiroadTool\CSCTESTI\ArcGISServerTest\ArcGISServerTest\temp\Gpandas_tulos_tiistai.shp"
    OutLinesFinal = gpd.GeoDataFrame(OutLinesFinal, geometry=OutLinesFinal['geometry'], crs=crs_lines) 

    msg("Saving final results to disk --> %s" % OutLines)

    # Tallennetaan lopputulos 
    OutLinesFinal.to_file(OutLines) # Tallennus

    Valmis()
    ##arcpy.SetProgressorPosition(90)
    msg("----------------------")

    ##################################################################################################
    #Luodaan loki-tiedosto ajon parametreistä samaan sijaintiin johon tulostiedostokin muodostetaan
    ##################################################################################################

    msg("----------------------")
    msg("VALMIS! NYT VOIT HALUTESSASI EXPORTOIDA TULOKSET KOKONAISMATKALINESin KAUTTA!")
    msg("----------------------")
    return "Results saved to --> %s" % OutLines

if __name__ == "__main__":
    # Parse file paths
    OutLines, Origins, Destinations = sys.argv[1], sys.argv[2], sys.argv[3]
    # Run script
    main(OutLines, Origins, Destinations)
    
    
    
