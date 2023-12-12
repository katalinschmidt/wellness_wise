from typing import List
from PIL import Image
import pytesseract
import re


def parse_text_from_image(image: Image) -> str:
    # TODO: See if parsing can be improved.
    #   OGX Keratin Shampoo ingredients results are very incomplete:
    #       Expected - 'Ingredients: Water(Aqua), Cetearyl Alcohol, Cetyl Alcohol, Behentrimonium Chloride, Glycerin, Hydrolyzed Keratin, Cocos Nucifera (Coconut) Oil, Persea Gratissima (Avocado) Oil, Theobroma Cacao (Cocoa) Seed Butter, Aloe Barbadensis Leaf Juice, Glycol Stearate, Glycol Distearate, Ceteareth-20, Isopropyl Alcohol, Dimethicone, Cyclotetrasiloxane, Citric Acid, Cyclopentasiloxane, Panthenol, Tetrasodium EDTA, DMDM Hydantoin, Methylchloroisothiazolinone, Red 40 (CI 16035), Yellow 5 (CI 19140), Blue 1 (CI42090), Fragrance (Parfum).'
    #       Actual - 'Cee ONS EO ee\npost-consumer resin.\n\n: Water (Aqua), Cetearyl Alcohol, Cetyl Alcohol,\nSes nt oes an ea) |\n\nmustiore '\n\nUae Leal doe, Ghvcl Stewie Ghosl Gleieenie!\nactonais ice Dieteenane }\nCeteareth-20, Isopropyl Alcohol, Dimethicone, _\nCyclotetrasiloxane, Citric Acid, Cyclopentasiloxane, —\nPanthenol, Tetrasodium EDTA, DMDM Hydantoin,\nMethyichioroisothiaz\n\n‘olinone,\n40 (Ci 16035), Yellow 5 (Cl 18140), Be 1 (0 42000),\nFragrance (Parfum).\n'
    #   Dove Beauty Bar ingredients results are very incomplete (first line only):
    #       Expected - 'INGREDIENTES: SODIUM LAUROYL ISETHIONATE, STEARIC ACID, SODIUM PALMITATE, LAURIC ACID, AQUA, SODIUM ISETHIONATE, SODIUM STEARATE, COCAMIDOPROPYL BETAINE, SODIUM PALM KERNELATE, GLYCERIN, PARFUM, SODIUM CHLORIDE, ZINC OXIDE, TETRASODIUM EDTA, TETRASODIUM ETIDRONATE, ALUMINIA, ALPHA-ISOMETHYL IONONE, BENZYL ALCOHOL, BUTYLPHENYL, METHYLPROPIONAL, CITRONELLOL, COUMARIN, HEXYL CINNAMAL, LIMONENE, LINALOOL, CI 77891.'
    #       Actual - 'INGREDIENTES: SODIUM LAUROYL ISETHIONATE, STEARIC ACID, SODIUM PALMITATE, LAURIC ACID, AQUA, SODIUM ISETHIONATE, SODIUM STEARATE,'

    return pytesseract.image_to_string(image)


def clean_img_text_for_ingredient_list(raw_text) -> List[str]:
    cleaned_ingredients_list =[]

    # Ingredients are typically separated by a comma
    raw_list = raw_text.lower().split(',')

    is_begin_ingredients = False
    for raw_item in raw_list:
        # Search for 'ingredients:' keyword to ignore it and anything before it
        if result := re.search(r':(.*)', raw_item):
            raw_item = result.group(1)
            is_begin_ingredients = True

        if is_begin_ingredients and raw_item:
            # FIXME: Create a list of chars_to_remove ?
            #   Examples from OGX Keratin Shampoo: '_\ncyclotetrasiloxane', '-\npanthenol'
            # Remove period from last ingredient on label, remove unnecessary whitespace, and replace newline char
            clean_item = raw_item.strip('.').strip().replace('\n', ' ')
            cleaned_ingredients_list.append(clean_item)

    return cleaned_ingredients_list
