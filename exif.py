"""Disclaimer: most of this file is copied from my group's work on our
in-class assignment to work on this problem. I've adapted it to work
for my code, but I do understand how it's all working""" 

import exifread
import reverse_geocoder as rg
  


def get_timestamp(file):
    with open(file, "rb") as image:
        tags = exifread.process_file(image)
            

    date = tags.get("EXIF DateTimeOriginal")
    if date:
        return date
    else:
        return None

def get_coordiantes(file):
    with open(file, "rb") as image:
        tags = exifread.process_file(image)

    if not tags:
        return None, None

    latitude = tags.get("GPS GPSLatitude")
    longitude = tags.get("GPS GPSLongitude")

    latref = tags.get("GPS GPSLatitudeRef")
    longref = tags.get("GPS GPSLongitudeRef")

    return convert_to_decimal(latitude, latref), convert_to_decimal(longitude, longref)

def convert_to_decimal(dms, reference):
    degrees = dms.values[0]
    minutes = dms.values[1]
    seconds = dms.values[2]

    decimal = int(degrees) + int(minutes)/60 + float(seconds)/3600
    if str(reference) == "S" or str(reference) == "W":
        decimal*= -1

    return decimal


def convert_to_location(lat, long):
    coordinates = (lat, long)
    loc_data= rg.search(coordinates)[0]

    city = loc_data["name"]
    state = loc_data["admin1"]
    country = loc_data["cc"]

    return (city, state, country)


def exif_to_location(file):
    lat, long = get_coordiantes(file)
    if lat and long:
        return convert_to_location(lat, long)
    else:
        return None