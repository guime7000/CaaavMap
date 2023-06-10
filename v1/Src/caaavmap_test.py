from caaavmap import generate_user_zipcode_dict, zipcode_to_Geolocalisation

from dotenv import dotenv_values
import os


config = dotenv_values(
    "/home/tom/Developpement/Git/CaaavMap/v1/Src/Config/.env.dir_config"
)
configFileName = "cp_vie_cp_naissance.csv"

pathToCsvUserFile = os.path.join(config["ZIPCODES_FILES_DIRECTORY"], configFileName)

pathToZipcodeDBFile = config["ZIPCODES_DB_FILE"]


def test_parsing_user_zipcode_dict() -> None:
    """Verifying 2 first living and born zipcodes in csv_test_file"""

    livingZipcode, livingCities, bornZipcodes, birthCities = generate_user_zipcode_dict(
        pathToCsvUserFile
    )

    assert livingZipcode[0] == "72000"
    assert bornZipcodes[0] == "72000"
    assert birthCities[0] == "Le Mans"

    assert livingZipcode[1] == "13260"
    assert bornZipcodes[1] == "75001"
    assert birthCities[1] == "Paris"


def test_skip_empty_zipcode() -> None:
    """Should skip line when empty living zipcode encountered"""
    livingZipcode, livingCities, bornZipcodes, birthCities = generate_user_zipcode_dict(
        pathToCsvUserFile
    )

    assert livingZipcode[2] == "72160"
    assert bornZipcodes[2] == "38000"
    assert birthCities[2] == "Grenoble"


def test_generating_zipcode_dict() -> None:
    """01400 zipcode should be paired with (46.153721024
    , 4.925850148)"""
    zipcodeDict = zipcode_to_Geolocalisation(pathToZipcodeDBFile)
    assert (zipcodeDict["01400"]) == [46.153721024, 4.925850148]
