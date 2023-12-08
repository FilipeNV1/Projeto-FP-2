import requests


base_url = "https://api.geoapify.com/v2/places?"
api_key = "54201da1292642cba162e8375fba069d"


def main():
    
    location = input("Enter your latitude and longitude split by comma: ")
    lat, lon = location.split(",")

    radiusMeters = input("Enter the radius(m): ")

    categories = input("Enter the categories split by comma: ")

    url = base_url + "categories=" + categories + "&filter=circle:" + lon + "," + lat + "," + radiusMeters + "&apiKey=" + api_key

    response = requests.get(url)
    print(response.json())


if __name__ == "__main__":
    main()