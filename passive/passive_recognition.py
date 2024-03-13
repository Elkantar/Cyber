import argparse
import os
import requests
import json
from ipwhois import IPWhois
import requests
from ipwhois import IPWhois
import ipaddress
from ipwhois.exceptions import IPDefinedError


# struct de mes lien de resaux sociaux

social_media = {
    "youtube": "https://www.youtube.com/{}",
    "facebook": "https://www.facebook.com/{}",
    "twitter": "https://www.twitter.com/{}",
    "instagram": "https://www.instagram.com/{}",
    "linkedin": "https://www.linkedin.com/in/{}",
    "github": "https://www.github.com/{}"
}


# Fonction pour rechercher le nom complet
def search_full_name(full_name):
    # Implémentation de la recherche en ligne
    # Remplacez cette partie avec une requête à une API ou un site Web approprié
    # Voici un exemple de requête GET à une API fictive (ceci est un exemple générique, vous devrez trouver une API réelle) :
    response = requests.get(f"https://api.example.com/search?full_name={full_name}")
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

# Fonction pour rechercher l'adresse IP
def get_location(ip_address):
    response = requests.get(f'http://ip-api.com/json/{ip_address}')
    data = response.json()
    return data

def get_operator(ip):
    try:
        # Check if the IP address is loopback
        if ipaddress.ip_address(ip).is_loopback:
            return "Loopback Address"
        
        # If not loopback, proceed with IPWhois lookup
        obj = IPWhois(ip)
        results = obj.lookup_rdap()
        return results['asn_description']
    except ipaddress.AddressValueError:
        return "Invalid IP Address"
    except IPDefinedError:
        return "IP Address already defined as Loopback via RFC 1122, Section 3.2.1.3."
    except Exception as e:
        return str(e)



def search_ip(ip):
    # Implémentation de la recherche en ligne
    # Remplacez cette partie avec une requête à une API ou un site Web approprié
    # Voici un exemple de requête GET à une API fictive (ceci est un exemple générique, vous devrez trouver une API réelle) :

    # comment a partir de l'ip je doit retrouver la localistaion de l'ip et l'herbergeur
    location = get_location(ip)
    operator = get_operator(ip)
    if location and operator:
        return {"city": location, "isp": operator}
    else:
        return None
    
# Fonction pour rechercher les liens de réseaux sociaux
def search_social_media(username):

    results = {}
    for platform, url in social_media.items():
        response = requests.get(url.format(username))
        results[platform] = response.status_code == 200
    return results

# Fonction pour rechercher le nom d'utilisateur
def search_username(username):
    # Implémentation de la recherche en ligne
    # si le username contient un _ le remplacer par - pour les liens de reseaux sociaux
    username = username.replace("_", "-")
    social_media_results = search_social_media(username)
    data = {}  # Initialize the "data" variable
    data["social_media"] = social_media_results

    # dans data remplacer les true par des yes et les false par des no
    for platform, value in data["social_media"].items():
        data["social_media"][platform] = "Yes" if value else "No"
    print(data)
    

# Fonction pour enregistrer le résultat dans un fichier
def save_result(filename, result):
    mode = 'a' if os.path.exists(filename) else 'w'
    with open(filename, mode) as file:
        file.write(result + "\n")

# Fonction principale
def main():
    parser = argparse.ArgumentParser(description="Outil de reconnaissance passive")
    parser.add_argument("-fn", "--full-name", help="Rechercher par nom complet", metavar="FULL_NAME")
    parser.add_argument("-ip", "--ip-address", help="Rechercher par adresse IP", metavar="IP_ADDRESS")
    parser.add_argument("-u", "--username", help="Rechercher par nom d'utilisateur", metavar="USERNAME")
    args = parser.parse_args()

    if args.full_name:
        result = search_full_name(args.full_name)
        if result:
            print(f"First name: {args.full_name.split()[0]}")
            print(f"Last name: {args.full_name.split()[1]}")
            print(f"Address: {result['address']}")
            print(f"Number: {result['number']}")
            save_result("result.txt", f"Full name: {args.full_name}\nAddress: {result['address']}\nNumber: {result['number']}")
        else:
            print("Aucune information trouvée pour le nom complet fourni.")

    elif args.ip_address:
        result = search_ip(args.ip_address)
        if result:
            print(f"ISP: {result['isp']}")
            print(f"City Lat/Lon: {result['city']}")
            save_result("result2.txt", f"IP address: {args.ip_address}\nISP: {result['isp']}\nCity Lat/Lon: {result['city']}")
        else:
            print("Aucune information trouvée pour l'adresse IP fournie.")

    elif args.username:
        result = search_username(args.username)
        if result:
            for platform, value in result.items():
                print(f"{platform}: {value}")
            save_result("result3.txt", f"Username: {args.username}\n{json.dumps(result, indent=4)}")
        else:
            print("Aucune information trouvée pour le nom d'utilisateur fourni.")

if __name__ == "__main__":
    main()
