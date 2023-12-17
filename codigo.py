#Autores 119192 ; 119253

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

def is_float(value): # Função utilizada para validar a latitude e longitude definidas abaixo
    try:
        float(value) 
        return True
    except ValueError: # Se não for possível passar o valor introduzido a float, dá return False
        return False

def continue_program(): # Função que permite ao utilizador procurar outras atrações ou sair
    while True:
        user_choice = input("Enter 'restart' to restart with new location or 'enter' to exit: ")
        if user_choice.lower() == 'restart':
            return True
        else:
            return False

def main():
    while True: # O código representado abaixo, basicamente pede uma latitude e uma longitude ao utilizador e verifica se consegue passar a mesma para float, se conseguir, é porque o valor introduzido não é string
        location = input("Enter your latitude and longitude, split by comma: ")
        if ',' not in location:
            print("Invalid input. Please enter a valid latitude/longitude.")
            continue
        lat, lon = location.replace(' ', '').split(",")  
        lat, lon = location.replace(' ', '').split(",")  # Separa a latitude e a longitude, de modo a ter ambas separadas, sem espaços (caso o utilizador tenha introduzido um)
        if is_float(lat) and is_float(lon): # Se ambas forem validadas como números(negativo ou positivo) o programa para com esta função e avança à seguinte
            break
        else:
            print("Invalid input. Please enter a valid latitude/longitude.")

    radiusMeters = input("Enter the radius(m): ")
    while (radiusMeters.isdigit() or radiusMeters.replace('.', '').isdigit()) == False: # Caso a distância seja um número negativo ou uma string, o programa não avança
        radiusMeters = input("Enter a valid radius(m): ")

    usercategories = input("Enter the categories split by comma: ")
    
    categorylist = readfile() # Guarda todas as categorias lidas no ficheiro numa lista
    valid_user_categories = validateCategory(usercategories, categorylist) # Guarda todas as categorias válidas numa lista

    while not valid_user_categories: # Enquanto o utilizador não introduzir uma categoria válida, o programa não avança
        usercategories = input("Enter the categories split by comma: ")
        valid_user_categories = validateCategory(usercategories, categorylist)
        
    valid_user_categories_str = ','.join(valid_user_categories) # Esta parte guarda todas as categorias da lista numa única string, separadas por vírgulas através da função join

    url = base_url + "categories=" + valid_user_categories_str + "&filter=circle:" + lon + "," + lat + "," + radiusMeters + "&apiKey=" + api_key
    n = 0
    response = requests.get(url)
    data = response.json()
    for item in data['features']:
        n+=1
        print ('Recomendação Número',n,':', end='\n')
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
        input("Press Enter to continue...") # Sistema para mostrar sujestão a sujestão, em que o utilizador pressionar enter o programa mostra a seguinte sugestão
        if n == len(data['features']):
            print('You found', len(data['features']), 'locations')
            if continue_program():
                main()
            else:
                break

if __name__ == "__main__":
    main()
    