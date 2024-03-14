import argparse
import exifread
import cv2
from PIL import Image
import pytesseract
from stegano import lsb

def get_location(image_path):
    with open(image_path, 'rb') as file:
        tags = exifread.process_file(file)
        lat_ref = tags.get('GPS GPSLatitudeRef')
        lat = tags.get('GPS GPSLatitude')
        lon_ref = tags.get('GPS GPSLongitudeRef')
        lon = tags.get('GPS GPSLongitude')

        if lat_ref and lat and lon_ref and lon:
            lat_degrees = lat.values[0].num / lat.values[0].den
            lat_minutes = lat.values[1].num / lat.values[1].den
            lat_seconds = lat.values[2].num / lat.values[2].den

            lon_degrees = lon.values[0].num / lon.values[0].den
            lon_minutes = lon.values[1].num / lon.values[1].den
            lon_seconds = lon.values[2].num / lon.values[2].den

            lat_direction = lat_ref.values
            lon_direction = lon_ref.values

            latitude = lat_degrees + (lat_minutes / 60.0) + (lat_seconds / 3600.0)
            longitude = lon_degrees + (lon_minutes / 60.0) + (lon_seconds / 3600.0)

            if lat_direction == 'S':
                latitude *= -1
            if lon_direction == 'W':
                longitude *= -1

            latitude = "{:.2f}".format(latitude)
            longitude = "{:.2f}".format(longitude)

            return latitude, longitude
    return None, None

def get_pgp_key(image_path):
    with open(image_path, 'rb') as file:  # Ouvrez le fichier en mode binaire ('rb')
        key_data = file.read().decode('latin-1')  # Décodez le contenu avec l'encodage approprié (latin-1)
        # Trouver l'indice de début et de fin de la clé publique
        begin_index = key_data.find('-----BEGIN PGP PUBLIC KEY BLOCK-----')
        end_index = key_data.find('-----END PGP PUBLIC KEY BLOCK-----') + len('-----END PGP PUBLIC KEY BLOCK-----')
        
        # Extraire la clé publique
        public_key = key_data[begin_index:end_index]
        return public_key



def main():
    parser = argparse.ArgumentParser(description='Image Inspector')
    parser.add_argument('image_path', type=str, help='Path to the image file')
    parser.add_argument('-map', action='store_true', help='Show the location where the photo was taken')
    parser.add_argument('-steg', action='store_true', help='Show the PGP key hidden in the image')
    args = parser.parse_args()

    if args.map:
        location = get_location(args.image_path)
        if location is not None:
            print(f'Lat/Lon:\t({location[0]}) / ({location[1]})')
        else:
            print('Location information not found in the image')

    if args.steg:
        pgp_key = get_pgp_key(args.image_path)
        if pgp_key is not None:
            print(pgp_key)
        else:
            print('PGP key not found in the image')

if __name__ == '__main__':
    main()