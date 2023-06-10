import csv
from dotenv import load_dotenv, dotenv_values
from collections import Counter
import logging
import os
import folium

################## Config settings ####################

config = dotenv_values(
    "/home/tom/Developpement/Git/CaaavMap/v1/Src/Config/.env.dir_config"
)

configFileName = "carte_codeP-lieux_vie_et_naissance.csv"
# configFileName = "cp_vie_cp_naissance.csv"

# configFileName = (
#     "/home/tom/Bureau/Developpement/Git/CaaavMap/v1/Test/cp_vie_cp_naissance.csv"
# )

defaultMapPosition = [47.98867581, 0.200118821]

################# ENd of config settings ##############


def generate_user_zipcode_dict(csvfile: str) -> list:
    livingZipcode = []
    livingCity = []
    birthZipcode = []
    birthCity = []

    with open(csvfile, "r") as infile:
        csvStream = csv.DictReader(
            infile,
            delimiter=",",
            quotechar='"',
        )
        for row in csvStream:
            if row["Code Postal habitation"] != "":
                livingZipcode.append(row["Code Postal habitation"])
                livingCity.append(row["Commune"])
                birthZipcode.append(row["Code Postal naissance"])
                birthCity.append(row["Commune_naissance"])

    return [livingZipcode, livingCity, birthZipcode, birthCity]


def zipcode_to_Geolocalisation(csvfile: str) -> dict:
    zipcodesDict = {}

    with open(csvfile, "r") as infile:
        csvStream = csv.DictReader(
            infile,
            delimiter=";",
            quotechar='"',
        )
        for row in csvStream:
            geoCoords = row["coordonnees_geographiques"].split(",")
            if row["code_postal"] not in zipcodesDict.keys():
                zipcodesDict[row["code_postal"]] = [
                    float(geoCoords[0]),
                    float(geoCoords[1]),
                ]

    return zipcodesDict


def userPopup(livingCity: str, cityName: str, birthZipcode: int) -> folium.Popup:
    """ "
    Sets up the popup to be shown when Marker is clicked, showing city of birth
    """

    line0 = f"Résidence: {livingCity} <br><br>"
    line1 = f"Naissance: {cityName} <br>"
    line2 = f"({birthZipcode}) <br>"

    htmlPopup = line0 + line1 + line2
    iframe = folium.IFrame(htmlPopup, width=250, height=125)
    popup = folium.Popup(iframe, max_width=250)

    return popup


pathToUserCsvFile = os.path.join(config["ZIPCODES_FILES_DIRECTORY"], configFileName)
pathToZipcodeDBFile = config["ZIPCODES_DB_FILE"]

zipcodesDict = zipcode_to_Geolocalisation(pathToZipcodeDBFile)

livingZipcodes, livingCities, birthZipcodes, birthCities = generate_user_zipcode_dict(
    pathToUserCsvFile
)

my_map = folium.Map(location=defaultMapPosition, zoom_start=9)

for i, zipcode in enumerate(livingZipcodes):
    # feature_group = boatsFeatureGroup[boatName]

    # boatPolyline = folium.PolyLine(boatCoords[boatName][:], color=fleetColor[i])

    popup = userPopup(livingCities[i], birthCities[i], birthZipcodes[i])

    userMarker = folium.Marker(zipcodesDict[zipcode], popup=popup).add_to(my_map)

    # boatPolyline.add_to(my_map)
    # feature_group.add_to(my_map)

# folium.LayerControl().add_to(my_map)

my_map.save(config["PATH_TO_INDEX_HTML"])
