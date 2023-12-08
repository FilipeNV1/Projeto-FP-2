import requests


base_url = "https://api.geoapify.com/v2/places?"
api_key = "54201da1292642cba162e8375fba069d"

def readfile():
    categorylist=[]
    with open ('categories.txt', 'r') as file:
        for category in file:
            category = category.rstrip('\n').lower().strip()
            categorylist.append(category)
    return categorylist

def validateCategory(userinput, validcategories):
    valid_user_categories = []
    for category in userinput.split(','):
        category = category.lower().strip()
        if category not in validcategories:
            print (category , "is a invalid category, moving on!")
        else:
            valid_user_categories.append(category)
    return valid_user_categories

def main():
    location = input("Enter your latitude and longitude split by comma: ")
    lat, lon = location.split(",")

    radiusMeters = input("Enter the radius(m): ")

    usercategories = input("Enter the categories split by comma: ")
    
    categorylist = readfile()
    valid_user_categories = validateCategory(usercategories, categorylist)

    while not valid_user_categories:
        usercategories = input("Enter the categories split by comma: ")
        valid_user_categories = validateCategory(usercategories, categorylist)

    url = base_url + "categories=" + usercategories + "&filter=circle:" + lon + "," + lat + "," + radiusMeters + "&apiKey=" + api_key

    response = requests.get(url)
    print(response.json())


if __name__ == "__main__":
    main()