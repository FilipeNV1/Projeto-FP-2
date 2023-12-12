import requests
import json

base_url = "https://api.geoapify.com/v2/places?"
api_key = "54201da1292642cba162e8375fba069d"

def readfile(): # Lê o ficheiro e adiciona todas as categorias numa lista
    categorylist=[]
    with open ('categories.txt', 'r') as file:
        for category in file:                                     
            category = category.rstrip('\n').lower().strip()
            categorylist.append(category)
    return categorylist

def validateCategory(userinput, validcategories): # Verifica se a categoria introduzida está presente na lista de categorias, se sim, adiciona a uma lista de categorias verificadas
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
    lat, lon = location.split(",") # Separa a latitude e a longitude, de modo a ter ambas separadas

    radiusMeters = input("Enter the radius(m): ")

    usercategories = input("Enter the categories split by comma: ")
    
    categorylist = readfile()
    valid_user_categories = validateCategory(usercategories, categorylist)

    while not valid_user_categories: # Enquanto o utilizador não introduzir uma categoria válida, o programa não avança
        usercategories = input("Enter the categories split by comma: ")
        valid_user_categories = validateCategory(usercategories, categorylist)
        
    valid_user_categories_str = ','.join(valid_user_categories)

    url = base_url + "categories=" + valid_user_categories_str + "&filter=circle:" + lon + "," + lat + "," + radiusMeters + "&apiKey=" + api_key

    response = requests.get(url)
    data = response.json()
    for item in data['features']:
        properties = item['properties']
        print(f"Name: {properties['name']}" if 'name' in properties else "Name: Not available") # Apresenta o nome (adicionamos o if/else para evitar um erro)
        print(f"Country: {properties['country']}" if 'country' in properties else "Country: Not available") # Apresenta o país se o mesmo estiver disponível na base de dados (para evitar erros)
        print(f"Country Code: {properties['country_code']}" if 'country_code' in properties else "Country code: Not available")
        print(f"County: {properties['county']}" if 'county' in properties else "County: Not available") # Apresenta o município se o mesmo estiver disponível na base de dados (para evitar erros)
        print(f"City: {properties['city']}" if 'city' in properties else "City: Not available") # Apresenta a cidade se a mesma estiver disponível na base de dados (para evitar erros)
        print(f"Postcode: {properties['postcode']}" if 'postcode' in properties else "Postcode: Not available") # Apresenta o código postal se o mesmo estiver disponível na base de dados (para evitar erros)
        print(f"District: {properties['district']}" if 'district' in properties else "District: Not available") # Apresenta o distrito se o mesmo estiver disponível na base de dados (para evitar erros)
        print(f"Street: {properties['street']}" if 'street' in properties else "Street: Not available") # Apresenta a rua, se disponível na base de dados, (para evitar erros)
        print(f"Longitude: {properties['lon']}" if 'lon' in properties else "Longitude: Not available") # Apresenta a longitude, se disponível na base de dados, (para evitar erros)
        print(f"Latitude: {properties['lat']}" if 'lat' in properties else "Latitude: Not available") # Apresenta a latitude, se disponível na base de dados, (para evitar erros)
        print(f"Formatted Address: {properties['formatted']}" if 'formatted' in properties else "Formated Address: Not available") # Apresenta o endereço completo, formatado, se disponível na base de dados, (para evitar erros)
        print(f"Address Line 1: {properties['address_line1']}" if 'address_line1' in properties else "Address line 1: Not available") # Apresenta a 1ª linha do endereço, se disponível na base de dados, (para evitar erros)
        print(f"Address Line 2: {properties['address_line2']}" if 'address_line2' in properties else "Address line 2: Not available") # Apresenta a 2ª linha do endereço, se disponível na base de dados, (para evitar erros)
        print(f"Categories: {', '.join(properties['categories'])}") # Apresenta a categoria de cada "feature"
        print("\n-------------------------\n") # Separa cada cidade com traços, de modo a ficar mais visível

if __name__ == "__main__":
    main()
    