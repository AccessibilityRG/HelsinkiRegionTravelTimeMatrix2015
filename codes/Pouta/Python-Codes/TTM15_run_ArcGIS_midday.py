# -*- coding: iso-8859-1 -*-
#------------------------------
# METROPACCESS-DIGIROAD
# MetropAccess-tutkimushanke
# HELSINGIN YLIOPISTO
# Koodi: Henrikki Tenkanen
#-------------------------------
# 4. Kokonaismatkaketjun Laskentatyökalu (sis. pysäköinti)
#-------------------------------

##
## MATRIISIAJOT 2015
## Set temp - directory in a NON-geodatabase location (output will be a shapefile)
## Works with ArcGIS 10.2. Pyhton , requires pandas, geopandas, fiona, numpy, gdal (+ all other dependencies)

####################################################################################
#MetropAccess-Digiroad, työkalu Digiroad-aineiston muokkaukseen MetropAccess-hankkeen menetelmän mukaisesti
#    Copyright (C) 2014  MetropAccess (Tenkanen). For MetropAccess-project and contact details, please see http://blogs.helsinki.fi/accessibility/
# 
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
###################################################################################

import arcpy, sys, time, string, os
from arcpy import env

def main(OriginFile):
 
    # Tarkistetaan tarvittavat Lisenssit
    arcpy.CheckOutExtension("Network")

    # ------------------------------------------
    # ArcGIS Serverille kovakoodatut parametrit
    # ------------------------------------------

    #fileNumber = [x for x in range(286,294)]


    #for fileindex in fileNumber:

    ##########################
    #Määritetään tiedostopolut
    ##########################

    Origins = OriginFile   #r"/home/MY_USERNAME/TTM/OD/Subsets/%s_Car_Matrix2015_Origs_KKJ2.shp" % fileindex
    Destinations = r"/home/MY_USERNAME/TTM/OD/Car_Matrix2015_Dest_KKJ2.shp"
    NetworkData = r"/home/MY_USERNAME/TTM/Digiroad/MetropAccess_Digiroad.gdb/MetropAccess_NetworkDataset/MetropAccess_NetworkDataset_ND"
    LiikenneElementit = r"/home/MY_USERNAME/TTM/Digiroad/MetropAccess_Digiroad.gdb/MetropAccess_NetworkDataset/METROPACCESS_DIGIROAD_LIIKENNE_ELEMENTTI"
    origin_fn = os.path.basename(Origins)[:-15]
    TulosNimi = "CarTT_Ruuhka_%s" % origin_fn
    Impedanssi = "Keskpva_aa"
    LaskKohteet = "ALL"
    Pysakointityyppi = ""
    Pysakointikentta = ""
    Kavelynopeus = 70.0
    Grafiikka = "false"

    #Environment määritykset:
    temp = r"/mnt/TTM_Results"


    print("---------------\nProcessing file: %s\n---------------" % os.path.basename(Origins))

    ElemKansio = os.path.dirname(NetworkData)
    OrigKansio = os.path.dirname(Origins)
    DestKansio = os.path.dirname(Destinations)
    arcpy.overwriteOutputs = True

    #Tsekataan onko temp geodatabase vai tavallinen kansio:
    if ".gdb" in temp or ".mdb" in temp:
        gdbCheck = True
        #Etsitään geodatabasen 'juuri'
        try:
            pos = temp.index('.gdb')
        except:
            pos = temp.index('.mdb')
        temp = temp[:pos+4]
    else:
        gdbCheck = False

    #Tsekataan sisältääkö TulosNimi välilyöntejä
    TulosNimi = TulosNimi.replace(" ", "_")

    ##############
    #METODIT
    ##############

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


    msg("------------------------------")
    msg("METROPACCESS-DIGIROAD")
    msg("MetropAccess-tutkimushanke")
    msg("HELSINGIN YLIOPISTO")
    msg("-------------------------------")
    msg("4. Kokonaismatkaketjun laskenta (sis. pysäköinti)")
    msg("-------------------------------")

    time.sleep(2.5)

    ################################################
    #TARKISTUKSET ENNEN LASKENTAA
    ################################################

    Aloitus()
    msg("TARKISTUKSET:")
    ##arcpy.SetProgressor("step", "KOKONAISMATKAKETJUN LASKENTA...Tarkistukset ennen laskentaa...", 0, 100, 5) #Luodaan suoritusinfopalkki

    #Tarkistetaan, että aineisto on joko EurefFinissä tai KKJ:ssa
    Desc = arcpy.Describe(NetworkData)
    NDProjektio = Desc.spatialReference.factoryCode

    msg("Tarkistetaan liikenneverkon projektio.")
    if NDProjektio == 3067 or NDProjektio == 2391 or NDProjektio == 2392 or NDProjektio == 2393 or NDProjektio == 2394 or NDProjektio == 104129:
        True
    else:
        virhe("Tieverkkoaineiston tulee olla projisoituna joko EUREF_FIN_TM35FIN:iin, GCS_EUREF_FIN:iin tai Finland_Zone_1, 2, 3 tai -4:ään (KKJ). Muuta Liikenne_elementti.shp projektio johonkin näistä Project -työkalulla, luo uusi Network Dataset perustuen tähän uuteen projisoituun LiikenneElementti -tiedostoon ja aja työkalu uudelleen.")
        
    #Tarkistetaan pysäköintikentän löytyminen:
    msg("Tarkistetaan pysäköintikentän löytyminen")
    if Pysakointityyppi == 5:
        fieldList = arcpy.ListFields(Destinations, Pysakointikentta)
        fieldCount = len(fieldList)
        if fieldCount == 1:
            teksti = "Käyttäjän määrittelemä pysäköintikenttä!"
            msg(teksti)
        elif Pysakointikentta == "":
            virhe("VIRHE! Pysäköintityypin määrittävää kenttää ei ole määritetty!")
        else:
            virhe("VIRHE! Pysäköintityypin määrittävää kenttää ei löydy taulusta! Tarkista, että pysäköintikenttä on luotu kohdetauluun ja että kirjoitusasu on oikein.")
    if Pysakointikentta == "":
        PysKenttaLog = "NONE"
            
    Valmis()

    #Tarkistetaan mitkä aikasakkolaskennan parametrit löytyvät NetworkDatasetistä:
    msg("Tarkistetaan kustannusparametrit")
    Aloitus()

    desc = arcpy.Describe(NetworkData)
    attributes = desc.attributes
    NDparams = []
    for attribute in attributes:
        NDparams.append(attribute.name)

    Haettava = ["Digiroa_aa", "Kokopva_aa", "Keskpva_aa", "Ruuhka_aa", "Pituus"]
    Nro = 0
    Accumulation = []
    for x in range(5):
        if Haettava[Nro] in NDparams:
            Accumulation.append(Haettava[Nro])
            Nro += 1
        else:
            Nro += 1
    Valmis()

    #Tarkistetaan löytyykö Impedanssi Accumulation taulusta, onko impedanssimuuttuja olemassa:
    msg("Tarkistetaan, että impedanssiatribuutti löytyy Network Datasetistä")
    Aloitus()

    if Impedanssi in NDparams:
        msg("Impedanssi määritetty!")
    else:
        virhe("VIRHE! Määriteltyä impedanssia ei ole määritelty Network Datasettiin. Tarkista, että muuttuja on todella olemassa\nja että Impedanssikentän kirjoitusasu täsmää käytettävän muuttujan kanssa. ")

    NDPath = desc.path
    NDsource = desc.edgeSources[0].name
    LE = os.path.join(NDPath, "%s.shp" % NDsource) #Parsitaan sourcedatan (Liikenne_Elementit) polku ja nimi
    del desc

    desc = arcpy.Describe(LiikenneElementit)
    basename = desc.baseName
    del desc

    if basename != NDsource: #Tarkistetaan onko inputiksi määritelty LiikenneElementti -tiedosto Network Datan todellinen source-layer:
        msg("LiikenneElementti -tiedosto ei ollut Network Datan source-layer. Vaihdettiin LiikenneElementti -tiedosto Network Datan Edge-sourceksi.")
        LiikenneElementit = LE
        
    if not Impedanssi in Accumulation:
        Accumulation.append(Impedanssi)
        msg("Käyttäjän määrittelemä impedanssi lisättiin Accumulation arvoihin!")
        
    #Tarkistetaan laskettavien kohteiden lukumäärä:
    LaskKohteet.replace(" ","")
    if LaskKohteet == "" or LaskKohteet == "ALL" or LaskKohteet == "all" or LaskKohteet == "All":
        LaskKohteet = ""
        LaskLogi = "ALL"
    elif LaskKohteet == "0":
        virhe("Laskettavia kohteita tulee olla vähintään yksi!")
    else:
        LaskKohteet = LaskKohteet
    Valmis()
    ##arcpy.SetProgressorPosition(5)
    msg("----------------------")


    #####################################################
    #***************************************************#
    # LASKENTA                                         *#
    #***************************************************#
    #####################################################

    msg("ALOITETAAN LASKENTA")
    msg("Luodaan tarvittavat attribuutit")
    ##arcpy.SetProgressorLabel("KOKONAISMATKAKETJUN LASKENTA...Luodaan tarvittavat attribuutit...")
    Aloitus()

    ################################################        
    #Tehdään tiedostoihin tarvittavat attribuutit
    ################################################

    #Origins:
    arcpy.AddField_management(Origins, "NameO", "TEXT")
    arcpy.AddField_management(Origins, "Kavely_O_T", "DOUBLE") #Kävelyaika lähtöpaikasta lähimpään tieverkkoon 
    arcpy.AddField_management(Origins, "Kavely_T_P", "DOUBLE") #Kävelyaika tieverkosta parkkipaikalle 

    #Ajoaika kentät:
    if "Digiroa_aa" in Accumulation:
        arcpy.AddField_management(Origins, "Digiroa_aa", "DOUBLE")
    if "Kokopva_aa" in Accumulation:
        arcpy.AddField_management(Origins, "Kokopva_aa", "DOUBLE")
    if "Keskpva_aa" in Accumulation:
        arcpy.AddField_management(Origins, "Keskpva_aa", "DOUBLE")
    if "Ruuhka_aa" in Accumulation:
        arcpy.AddField_management(Origins, "Ruuhka_aa", "DOUBLE")
    if Impedanssi in Accumulation:                                  #Tehdään jos käyttäjä on haluaa käyttää jotain omaa impedanssiaan
        arcpy.AddField_management(Origins, Impedanssi, "DOUBLE")

    if "Pituus" in Accumulation:
        arcpy.AddField_management(Origins, "KavelMatkO", "DOUBLE") #Matka lähtöpaikasta parkkipaikalle kaupungin alueella/kaupungin ulkopuolella
        arcpy.AddField_management(Origins, "KavelDistO", "DOUBLE") #Kävelymatka lähtöpaikasta lähimpään tieverkkopisteeseen

    #Destinations:
    ##arcpy.AddField_management(Destinations, "NameD", "TEXT")
    ##arcpy.AddField_management(Destinations, "Parkkiaika", "DOUBLE") #Parkkipaikan etsintään kuluva aika 
    ##arcpy.AddField_management(Destinations, "Kavely_P_T", "DOUBLE") #Kävelyaika parkkipaikalta lähimpään tieverkkoon 
    ##arcpy.AddField_management(Destinations, "Kavely_T_D", "DOUBLE") #Kävelyaika lähimmästä tieverkkopisteestä kohteeseen 
    ##
    ##if "Pituus" in Accumulation:
    ##    arcpy.AddField_management(Destinations, "KavelMatkD", "DOUBLE") #Kävelymatka parkkipaikalta lähimpään tieverkkopisteeseen
    ##    arcpy.AddField_management(Destinations, "KavelDistD", "DOUBLE") #Kävelymatka lähimmästä tieverkkopisteestä kohteeseen kantakaupungin alueella/kaupungin ulkopuolella

    Valmis()
    ##arcpy.SetProgressorPosition(10)
    msg("----------------------")

    #Tehdään id-kentät
    msg("Luodaan ID-kentät")
    ##arcpy.SetProgressorLabel("KOKONAISMATKAKETJUN LASKENTA...Luodaan ID-kentät...")
    Aloitus()

    #Rivi_id ei täsmää geodatabasessa ja shapefileessä!! Tsekataan onko tiedostot mdb:ssä tai gdb:ssä
    if ".mdb" in Origins or ".gdb" in Origins:
        OrigNameID = "'O' + str(!OBJECTID!)"
    else:
        OrigNameID = "'O' + str(!FID!)"

    if ".mdb" in Destinations or ".gdb" in Destinations:
        DestNameID = "'D' + str(!OBJECTID!)"
    else:
        DestNameID = "'D' + str(!FID!)"

    arcpy.CalculateField_management(Origins, "NameO", OrigNameID, "PYTHON", "")
    ##arcpy.CalculateField_management(Destinations, "NameD", DestNameID, "PYTHON", "")

    Valmis()
    ##arcpy.SetProgressorPosition(15)
    msg("----------------------")

    ###############################################
    #Lasketaan pisteiden etäisyydet tieverkostosta
    ###############################################

    msg("Lasketaan kävelyaika ja matka tieverkostosta")
    ##arcpy.SetProgressorLabel("KOKONAISMATKAKETJUN LASKENTA...Lasketaan kävelyaika ja matka tieverkostosta...")
    Aloitus()

    arcpy.Near_analysis(Origins, LiikenneElementit, "3000 Meters", "NO_LOCATION", "NO_ANGLE")
    ##arcpy.Near_analysis(Destinations, LiikenneElementit, "3000 Meters", "NO_LOCATION", "NO_ANGLE")

    #Lasketaan kävelyaika ja matka tieverkostosta:
    OrigReader = arcpy.UpdateCursor(Origins)
    ##DestReader = arcpy.UpdateCursor(Destinations)

    for row in OrigReader:
        row.Kavely_O_T = row.NEAR_DIST / Kavelynopeus
        row.KavelDistO = row.NEAR_DIST
        OrigReader.updateRow(row)
        del row

    ##for row in DestReader:
    ##    row.Kavely_T_D = row.NEAR_DIST / Kavelynopeus
    ##    row.KavelDistD = row.NEAR_DIST
    ##    DestReader.updateRow(row)
    ##    del row

    del OrigReader
    ##del DestReader

    Valmis()
    ##arcpy.SetProgressorPosition(20)
    msg("----------------------")

    ####################################################################################
    #Lasketaan parkkipaikan etsintään menevä aika perustuen käyttäjän parametreihin
    ####################################################################################

    # Pysäköintityypit - etsintäaika (minuuteissa):
    # 0: Ei oteta huomioon 
    # 1: Keskiarvo - 0.42 (oletus)
    # 2: Kadunvarsipaikka - 0.73
    # 3: Pysäköintitalo - 0.22
    # 4: Erillisalueet - 0.16
    # 5: Pysäköintityyppi löytyy käyttäjän määrittämästä kentästä
    # Pysakointikentta: <String> - Käyttäjän määrittämä kenttä, josta löytyy pysäköintityyppi
    #------------------------------------------------------------------------------------------

    msg("Lasketaan pysäköintipaikan etsintään kuluva aika")
    ##arcpy.SetProgressorLabel("KOKONAISMATKAKETJUN LASKENTA...Lasketaan pysäköintipaikan etsintään kuluva aika...")
    Aloitus()

    if Pysakointityyppi == 0:
        arcpy.CalculateField_management(Destinations, "Parkkiaika", "0 ", "PYTHON")
    elif Pysakointityyppi == 1:
        arcpy.CalculateField_management(Destinations, "Parkkiaika", "0.42 ", "PYTHON")

    elif Pysakointityyppi == 2:
        arcpy.CalculateField_management(Destinations, "Parkkiaika", "0.73 ", "PYTHON")

    elif Pysakointityyppi == 3:
        arcpy.CalculateField_management(Destinations, "Parkkiaika", "0.22 ", "PYTHON")

    elif Pysakointityyppi == 4:
        arcpy.CalculateField_management(Destinations, "Parkkiaika", "0.16 ", "PYTHON")

    elif Pysakointityyppi == 5: #Käyttäjä määritellyt pysäköintityypin Kohdepiste-tiedostoon
        DestReader = arcpy.UpdateCursor(Destinations)
        for row in DestReader:
            if row.getValue(Pysakointikentta) == 0:
                row.Parkkiaika = 0
            elif row.getValue(Pysakointikentta) == 1:
                row.Parkkiaika = 0.42
            elif row.getValue(Pysakointikentta) == 2:
                row.Parkkiaika = 0.73
            elif row.getValue(Pysakointikentta) == 3:
                row.Parkkiaika = 0.22
            elif row.getValue(Pysakointikentta) == 4:
                row.Parkkiaika = 0.16
            else:
                row.Parkkiaika = 0
                msg("Kohteelle asetettu pysäköintityypin arvo on sallittujen arvojen (0-4) ulkopuolella! Kohteen pysäköintityyppiä ei oteta huomioon.")
            DestReader.updateRow(row)
            del row
        del DestReader

    Valmis()
    ##arcpy.SetProgressorPosition(25)
    msg("----------------------")

    #######################################################
    #Kantakaupunki polygonin luominen laskentaa varten:
    #######################################################

    msg("Luodaan kantakaupunkipolygoni")
    ##arcpy.SetProgressorLabel("KOKONAISMATKAKETJUN LASKENTA...Luodaan kantakaupunkipolygoni...")
    Aloitus()


    env.workspace = temp

    coordList = [[387678.024778,6675360.99039],[387891.53396,6670403.35286],[383453.380944,6670212.21613],[383239.871737,6675169.85373],[387678.024778,6675360.99039]] #Koordinaatit ovat EUREF_FIN_TM35FIN:issä

    point = arcpy.Point()
    array = arcpy.Array()

    #Lisätään koordinaatit Arrayhin:
    for coordPair in coordList:
        point.X = coordPair[0]
        point.Y = coordPair[1]
        array.add(point)

    Kantakaupunki = arcpy.Polygon(array)

    #Määritetään Spatial Reference:
    sr = arcpy.SpatialReference()
    sr.factoryCode = 3067 #EUREF_FIN_TM35FIN
    sr.create()

    #Luodaan kantakaupunki tiedosto:
    if gdbCheck == True:
        Kantis = os.path.join(temp,"Kantakaupunki")
    else:
        Kantis = os.path.join(temp,"Kantakaupunki.shp")
        
    ExDel(Kantis)
    arcpy.Select_analysis(Kantakaupunki, Kantis)

    #Määritetään kantakaupungille projektio:
    arcpy.DefineProjection_management(Kantis, sr)

    msg("Luotiin kantakaupunki")
    Valmis()
    ##arcpy.SetProgressorPosition(30)
    msg("----------------------")

    ###################################################
    #MÄÄRITETÄÄN TIEDOSTOT SAMAAN KOORDINAATISTOON
    ###################################################

    msg("Määritetään tiedostot samaan koordinaatistoon")
    ##arcpy.SetProgressorLabel("KOKONAISMATKAKETJUN LASKENTA...Määritetään tiedostot samaan koordinaatistoon...")
    Aloitus()

    #Destinations:
    DDesc = arcpy.Describe(Destinations)
    DestProjektio = DDesc.spatialReference.Name
    DFactCode = DDesc.spatialReference.factoryCode
    DProj = DestProjektio[:8]

    if gdbCheck == True:
        KohdePath = os.path.join(temp, "DestinationsProj")
        LahtoPath = os.path.join(temp, "OriginsProj")
        KantisPath = os.path.join(temp, "KantisProj")

    else:
        KohdePath = os.path.join(temp, "DestinationsProj.shp")
        LahtoPath = os.path.join(temp, "OriginsProj.shp")
        KantisPath = os.path.join(temp, "KantisProj.shp")

    ExDel(KohdePath)
    ExDel(LahtoPath)
    ExDel(KantisPath)

    #Origins:
    ODesc = arcpy.Describe(Origins)
    OrigProjektio = ODesc.spatialReference.Name
    OFactCode = ODesc.spatialReference.factoryCode
    OProj = OrigProjektio[:8]

    #Luodaan spatial reference perustuen NetworkDatan SR:een:
    del sr
    sr = arcpy.SpatialReference()
    if NDProjektio == 3067: #EurefFin
        sr.factoryCode = 3067
        sr.create()
    elif NDProjektio == 104129: #GCS_EurefFIN
        sr.factoryCode = 104129
        sr.create()
    elif NDProjektio == 2391: #KKJ1
        sr.factoryCode = 2391
        sr.create()
    elif NDProjektio == 2392: #KKJ2
        sr.factoryCode = 2392
        sr.create()
    elif NDProjektio == 2393: #KKJ3
        sr.factoryCode = 2393
        sr.create()
    elif NDProjektio == 2394: #KKJ4
        sr.factoryCode = 2394
        sr.create()

    #Määritetään Kohteille ja Lähtöpaikoille oikea projektio, jos NetworkData on EUREF_FIN_TM35FIN:issä tai GCS_EUREF_FIN:issä::
    if NDProjektio == 3067 or NDProjektio == 104129:
        if NDProjektio == 104129:
            arcpy.Project_management(Kantis, KantisPath, sr, "") #Määritetään kantakaupunki samaan koordinaatistoon
            Kantakaupunki = KantisPath

    #Destinations:
        if NDProjektio != DFactCode: #Jos Network Data ja Destinationit ovat eri koordinaatistossa:
            if DFactCode >= 2391 and DFactCode <= 2394:
                Dtransform_method = "KKJ_To_EUREF_FIN"
            elif DFactCode == 3067:
                Dtransform_method = ""
            elif DProj == "WGS_1984" or DFactCode == 4326: #Projected WGS_1984 tai GCS_WGS_1984
                Dtransform_method = "EUREF_FIN_To_WGS_1984"
            elif DProj == "ETRS_198":
                Dtransform_method = "EUREF_FIN_To_ETRS_1989"
            else:
                virhe("Kohdepisteet tulee olla projisoituna johonkin seuraavista koordinaatistoista:")
                virhe("KKJ, EUREF_FIN, WGS_1984, ETRS_1989")
                   
            arcpy.Project_management(Destinations, KohdePath, sr, Dtransform_method) #Määritetään Destinationit samaan koordinaatistoon
            Destinations = KohdePath
            msg("Kohdepaikkojen projektio vaihdettiin samaksi kuin Network Datalla. Luotiin kopio tiedostosta.")

    #Origins:
        if NDProjektio != OFactCode: #Jos Network Data ja Originit ovat eri koordinaatistossa:
            if OFactCode >= 2391 and OFactCode <= 2394:
                Otransform_method = "KKJ_To_EUREF_FIN"
            elif OFactCode == 3067:
                Otransform_method = ""
            elif OProj == "WGS_1984" or OFactCode == 4326: #Projected WGS_1984 tai GCS_WGS_1984
                Otransform_method = "EUREF_FIN_To_WGS_1984"
            elif OProj == "ETRS_198":
                Otransform_method = "EUREF_FIN_To_ETRS_1989"
            else:
                virhe("Lähtöpisteet tulee olla projisoituna johonkin seuraavista koordinaatistoista:")
                virhe("KKJ, EUREF_FIN, WGS_1984, ETRS_1989")
            
            arcpy.Project_management(Origins, LahtoPath, sr, Otransform_method) #Määritetään Destinationit samaan koordinaatistoon
            Origins = LahtoPath
            msg("Lähtöpaikkojen projektio vaihdettiin samaksi kuin Network Datalla. Luotiin kopio tiedostosta.")

    #Määritetään Kohteille ja Lähtöpaikoille oikea projektio, jos NetworkData on KKJ:ssa:
    elif NDProjektio == 2391 or NDProjektio == 2392 or NDProjektio == 2393 or NDProjektio == 2394:
        arcpy.Project_management(Kantis, KantisPath, sr, "KKJ_To_EUREF_FIN") #Määritetään kantakaupunki samaan koordinaatistoon
        Kantakaupunki = KantisPath
        
        if NDProjektio != DFactCode: #Jos NetworkData ja kohdepisteet ovat eri KKJ:ssa projisoidaan ne samaan.
            if DFactCode >= 2391 and DFactCode <= 2394:
                Dtransform_method = ""
            elif DProj == "WGS_1984" or DFactCode == 4326: #Projected WGS_1984 tai GCS_WGS_1984
                Dtransform_method = "KKJ_To_WGS_1984_2_JHS153"
            elif DProj == "ETRS_198":
                Dtransform_method = "KKJ_To_ETRS_1989_2"
            else:
                virhe("Kohdepisteet tulee olla projisoituna johonkin seuraavista koordinaatistoista:")
                virhe("KKJ, EUREF_FIN, WGS_1984, ETRS_1989")
            
            arcpy.Project_management(Destinations, KohdePath, sr, Dtransform_method) #Määritetään Destinationit samaan koordinaatistoon
            Destinations = KohdePath
            msg("Kohdepaikkojen projektio vaihdettiin samaksi kuin Network Datalla. Luotiin kopio tiedostosta.")

        if NDProjektio != OFactCode: #Jos NetworkData ja kohdepisteet ovat eri KKJ:ssa projisoidaan ne samaan.
            if OFactCode >= 2391 and OFactCode <= 2394:
                Otransform_method = ""
            elif OProj == "WGS_1984" or OFactCode == 4326: #Projected WGS_1984 tai GCS_WGS_1984
                Otransform_method = "KKJ_To_WGS_1984_2_JHS153"
            elif OProj == "ETRS_198":
                Otransform_method = "KKJ_To_ETRS_1989_2"
            else:
                virhe("Lähtöpisteet tulee olla projisoituna johonkin seuraavista koordinaatistoista:")
                virhe("KKJ, EUREF_FIN, WGS_1984, ETRS_1989")

            arcpy.Project_management(Origins, LahtoPath, sr, Otransform_method) #Määritetään Destinationit samaan koordinaatistoon
            Origins = LahtoPath
            msg("Lähtöpaikkojen projektio vaihdettiin samaksi kuin Network Datalla. Luotiin kopio tiedostosta.")

    Valmis()
    ##arcpy.SetProgressorPosition(35)
    msg("----------------------")

    ##################################
    #LASKETAAN KÄVELYYN KULUVA AIKA
    ##################################
        
    #Tehdään Feature Layerit spatiaalista valintaa varten:
    Orig_lyr = "Orig_lyr"
    Dest_lyr = "Dest_lyr"
    OrigPath = Orig_lyr + ".lyr"
    DestPath = Dest_lyr + ".lyr"

    env.workspace = OrigKansio


    ExDel(Orig_lyr)   #Varmistetaan ettei FeatureLayeria ole jo olemassa

    env.workspace = DestKansio

    ExDel(Dest_lyr)   #Varmistetaan ettei FeatureLayeria ole jo olemassa
        
    arcpy.MakeFeatureLayer_management(Origins, Orig_lyr, "", OrigKansio)
    arcpy.MakeFeatureLayer_management(Destinations, Dest_lyr, "", DestKansio)

    #Valitaan kohteet, jotka ovat kantakaupungin sisällä:
    arcpy.SelectLayerByLocation_management(Orig_lyr, "INTERSECT", Kantakaupunki, "", "NEW_SELECTION")
    ##arcpy.SelectLayerByLocation_management(Dest_lyr, "INTERSECT", Kantakaupunki, "", "NEW_SELECTION")

    #Lasketaan aika ja matka lähtöpaikasta parkkipaikalle/parkkipaikalta kohteeseen kantakaupungin alueella:
    #Kantakaupungissa matka autolle on 180 metriä

    msg("Lasketaan aika ja matka lähtöpaikasta parkkipaikalle/parkkipaikalta kohteeseen kantakaupungin alueella")
    ##arcpy.ResetProgressor()
    ##arcpy.SetProgressor("step", "KOKONAISMATKAKETJUN LASKENTA...Lasketaan aika ja matka lähtöpaikasta parkkipaikalle/parkkipaikalta kohteeseen kantakaupungin alueella...", 0, 100, 5)
    ##arcpy.SetProgressorPosition(40)
    Aloitus()

    # Calculate walking times with Field Calculator
    expression = "180.0 / %s" % Kavelynopeus
    arcpy.CalculateField_management(Orig_lyr, "Kavely_T_P", expression, "PYTHON", "")
    expression2 = "180.0"
    arcpy.CalculateField_management(Orig_lyr, "KavelMatkO", expression2, "PYTHON", "")

    ##OrigReader = arcpy.UpdateCursor(Orig_lyr)
    ##DestReader = arcpy.UpdateCursor(Dest_lyr)

    ##for row in OrigReader:
    ##    row.Kavely_T_P = 180.0 / Kavelynopeus
    ##    row.KavelMatkO = 180.0
    ##    OrigReader.updateRow(row)
    ##    del row

    ##for row in DestReader:
    ##    row.Kavely_P_T = 180.0 / Kavelynopeus
    ##    row.KavelMatkD = 180.0
    ##    DestReader.updateRow(row)
    ##    del row

    ##del OrigReader
    ##del DestReader

    Valmis()
    ##arcpy.SetProgressorPosition(40)
    msg("----------------------")

    #Vaihdetaan valinta kantakaupungin ulkopuolisille alueille:
    arcpy.SelectLayerByAttribute_management(Orig_lyr, "SWITCH_SELECTION", "")
    ##arcpy.SelectLayerByAttribute_management(Dest_lyr, "SWITCH_SELECTION", "")

    #Lasketaan aika ja matka lähtöpaikasta parkkipaikalle/parkkipaikalta kohteeseen kantakaupungin ulkopuolella:
    #Kantakaupungin ulkopuolella matka autolle on 135 metriä

    msg("Lasketaan aika ja matka lähtöpaikasta parkkipaikalle/parkkipaikalta kohteeseen kantakaupungin ulkopuolella")
    ##arcpy.SetProgressorLabel("KOKONAISMATKAKETJUN LASKENTA...Lasketaan aika ja matka lähtöpaikasta parkkipaikalle/parkkipaikalta kohteeseen kantakaupungin ulkopuolella...")
    Aloitus()

    # Calculate walking times with Field Calculator
    expression = "135.0 / %s" % Kavelynopeus
    arcpy.CalculateField_management(Orig_lyr, "Kavely_T_P", expression, "PYTHON", "")
    expression2 = "135.0"
    arcpy.CalculateField_management(Orig_lyr, "KavelMatkO", expression2, "PYTHON", "")


    ##OrigReader = arcpy.UpdateCursor(Orig_lyr)
    ##DestReader = arcpy.UpdateCursor(Dest_lyr)

    ##for row in OrigReader:
    ##    row.Kavely_T_P = 135.0 / Kavelynopeus
    ##    row.KavelMatkO = 135.0
    ##    OrigReader.updateRow(row)
    ##    del row

    ##for row in DestReader:
    ##    row.Kavely_P_T = 135.0 / Kavelynopeus
    ##    row.KavelMatkD = 135.0
    ##    DestReader.updateRow(row)
    ##    del row

    ##del OrigReader
    ##del DestReader

    #Poistetaan valinnat:
    arcpy.SelectLayerByAttribute_management(Orig_lyr, "CLEAR_SELECTION", "")
    ##arcpy.SelectLayerByAttribute_management(Dest_lyr, "CLEAR_SELECTION", "")


    #####################################
    #REITITYS: OD-COST MATRIX LASKENTA
    #####################################

    #Tarkistetaan onko aiempia OD-Cost-Matrixeja ja luodaan uniikki nimi:
    env.workspace = temp
    ODnimi = "Kokonaismatkaketju_ODC_MATRIX"
    ODPath = ODnimi + ".lyr"

    ExDel(ODnimi)
        
    Valmis()
    ##arcpy.SetProgressorPosition(45)
    msg("----------------------")

    #Tehdään OD Cost Matrix Layer:
    msg("Tehdään OD Cost Matrix Layer")
    ##arcpy.SetProgressorLabel("KOKONAISMATKAKETJUN LASKENTA...Tehdään OD-Cost-Matrix Layer...")
    Aloitus()

    if Grafiikka == "true" or "True":
        GrafOut = "STRAIGHT_LINES"
    else:
        GrafOut = "NO_LINES"

    if "Hierarkia" in NDparams:
        Hierarkia = "USE_HIERARCHY"
    else:
        Hierarkia = "NO_HIERARCHY"

    arcpy.MakeODCostMatrixLayer_na(NetworkData, ODnimi, Impedanssi, "", LaskKohteet, Accumulation, "ALLOW_DEAD_ENDS_ONLY", "", Hierarkia, "", GrafOut)

    #Lisätään OD cost matrix Locationit ja määritetään parametrit:
    msg("Lisätään OD cost matrix Locationit")
    Aloitus()

    Lahtopaikat = Orig_lyr
    Kohdepaikat = Dest_lyr

    ##arcpy.SetProgressorLabel("KOKONAISMATKAKETJUN LASKENTA...Lisätään OD-cost-matrix Lähtöpaikat...Tässä menee hetki...")                                                                            
    arcpy.AddLocations_na(ODnimi, "Origins", Lahtopaikat, "Name NameO #", "5000 Meters", "", "", "MATCH_TO_CLOSEST", "APPEND", "NO_SNAP", "", "EXCLUDE", "")
    ##arcpy.SetProgressorPosition(55)
    ##arcpy.SetProgressorLabel("KOKONAISMATKAKETJUN LASKENTA...Lisätään OD-cost-matrix Kohdepaikat...Tässä menee hetki...") 
    arcpy.AddLocations_na(ODnimi, "Destinations", Kohdepaikat, "Name NameD #", "5000 Meters", "", "", "MATCH_TO_CLOSEST", "APPEND", "NO_SNAP", "", "EXCLUDE", "")

    ##arcpy.SetProgressorPosition(65)
    Valmis()
    msg("----------------------")

    #Suoritetaan OD cost matrix laskenta:
    msg("Suoritetaan OD-cost-matrix laskenta")
    ##arcpy.SetProgressorLabel("KOKONAISMATKAKETJUN LASKENTA...Suoritetaan OD-cost-matrix laskenta...") 
    Aloitus()

    arcpy.Solve_na(ODnimi, "SKIP", "TERMINATE")
    Valmis()
    ##arcpy.SetProgressorPosition(70)
    msg("----------------------")

    ################################################################################
    #JOINATAAN KOKONAISMATKOIHIN TIEDOT KOHDE/LÄHTÖPISTEISTÄ (kävelyyn kuluva aika)
    ################################################################################

    #Valitaan muokattavaksi OD C M:n Lines layer:
    arcpy.SelectData_management(ODnimi, "Lines")
    Lines = ODnimi + "/" + "Lines"

    #Lisätään Lines_lyr:iin tarvittavat kentät Joinin mahdollistamiseksi:
    arcpy.AddFieldToAnalysisLayer_na(ODnimi, "Lines", "LahtoNimi", "TEXT")
    arcpy.AddFieldToAnalysisLayer_na(ODnimi, "Lines", "KohdeNimi", "TEXT")

    #Muodostetaan Joinin id-kentät:
    arcpy.CalculateField_management(Lines, "LahtoNimi", "!Name!.split(\" -\")[0]", "PYTHON_9.3")
    arcpy.CalculateField_management(Lines, "KohdeNimi", "!Name!.split(\"- \")[1]", "PYTHON_9.3")

    #Eksportataan Line-feature shapeksi, jotta Join saadaan toimimaan:
    if gdbCheck == True:

        #Geodatabasessa tiedostonimessä ei saa olla tiedostomuodon päätettä (.shp)
        if ".shp" in TulosNimi:
            OutLineNimi = TulosNimi[:-4] 
        else:
            OutLineNimi = TulosNimi
    else:
        if not ".shp" in TulosNimi:
            OutLineNimi = TulosNimi + ".shp"
        else:
            OutLineNimi = TulosNimi
            
    env.workspace = temp
    nameCheck = os.path.join(temp, OutLineNimi)

    if arcpy.Exists(nameCheck):
        unique = arcpy.CreateUniqueName(nameCheck)
        OutLines = unique
        Outnimi = string.split(unique, ".")[0]
        LogName = Outnimi
        
    else:
        OutLines = nameCheck
        Outnimi = nameCheck

    # Save Lines to disk
    msg("----------------------")
    Aloitus()
    msg("Save preliminary results to disk")
    arcpy.Select_analysis(Lines, OutLines)
    Valmis()
    msg("----------------------")

    #Poistetaan väliaikaistiedostot:
    env.workspace = temp
    ExDel(KohdePath)
    ExDel(LahtoPath)
    ExDel(KantisPath)
    ExDel(Kantis)

    # Return filepath to Shapefile
    return [OutLines, Origins, Destinations]

if __name__ == "__main__":
    inputFile = sys.argv[1]
    main(inputFile)
    
