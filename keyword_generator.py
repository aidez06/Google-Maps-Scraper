combine_data = {}
keywords = [
    "solar wholesaler",
    "solar wholesale",
    "solar distributor",
    "solar supplier",
    "solar store",
    "solar shop",
    "solar retailer",
    "solar retail",
    "solar reseller",
    "solar bulk sale",
    "bulk solar purchase",
    "solar bulk buying",
    "solar bulk supply",
    "solar dealer",
    "solar vendor",
    "solar sales",
    "solar purchasing",
    "solar supply",
    "solar trade",
    "solar distribution",
    "solar merchandise",
    "solar stockist",
    "solar inventory",
    "solar business",
    "solar trade",
    "solar commerce",
    "solar outlet",
    "solar outlet store",
    "solar showroom",
    "solar warehouse",
    "solar bulk retailer",
    "solar bulk seller",
    "solar bulk dealer",
    "solar bulk vendor",
    "solar bulk trade",
    "solar bulk supplier",
    "solar bulk distributor",
    "solar bulk supplier",
    "solar bulk inventory",
    "solar bulk business",
    "solar bulk commerce",
    "solar bulk outlet",
    "solar bulk outlet store",
    "solar bulk showroom",
    "solar bulk warehouse",
]
locations_dict = {
    "Western Australia": [
        "Bunbury",
        "Broome",
        "Busselton",
        "Albany",
        "Esperance",
        "Geraldton",
        "Port Hedland",
        "Kalgoorlie - Boulder",
        "Karratha",
        "Bridgetown",
        "Tom Price",
        "Kununurra",
        "Derby",
        "Newman",
        "Mandurah",
        "Carnarvon",
        "Binningup",
        "Merredin",
        "Boulder",
        "Boddington",
        "Margaret River",
        "Narrogin",
        "Northam",
        "Katanning",
        "Pinjarra",
        "Manjimup",
        "Donnybrook",
        "Dampier",
        "Dunsborough",
        "Kalbarri",
        "York",
        "City of Wanneroo",
        "Harvey",
        "Waroona",
        "Denmark",
        "Dongara",
        "Paraburdoo",
        "Fitzroy Crossing",
        "Exmouth",
        "Wagin",
        "Fremantle",
        "Capel",
        "Kwinana Beach",
        "Halls Creek",
        "Augusta",
        "Wickham",
        "Byford",
        "City of Melville",
        "City of Armadale",
        "Drummond Cove"
    ]
}

def keyword_loc():
    for location in locations_dict["Western Australia"]:
        combine_data[location] = keywords
    return combine_data

