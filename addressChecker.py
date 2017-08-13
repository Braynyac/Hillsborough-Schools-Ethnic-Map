from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

geolocator = Nominatim()


while True:
    my_address = input("Address: ")

    try:
        location = geolocator.geocode(my_address, timeout=10)
        print(location.latitude, location.longitude)
    except GeocoderTimedOut as e:
        print("Error: geocode failed on input %s with message %s"%(my_address, e.message))
