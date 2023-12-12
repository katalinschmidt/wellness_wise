import os
import requests

OPENAI_API_ENDPOINT = "https://api.openai.com/v1/engines/gpt-3.5-turbo/completions"


def generate_ai_response(user_message: str) -> str:
    ai_response = ""

    # Build request data
    api_key = os.getenv("OPENAI_API_KEY")
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }
    data = {
        'prompt': user_message,
    }

    # Make request
    response = requests.post(OPENAI_API_ENDPOINT, json=data, headers=headers)

    # Handle response
    if response.status_code == 200:
        ai_response = response.json().get('choices')[0]['text']
    # TODO: Add more robust handling, e.g 500 codes, unexpected JSON format, etc.

    return ai_response


# TODO: Fine tune prompt to get the output example below. Move comments to README.md when testing is complete.

"""
IDEAL OUTPUT: 

Water:
* Natural or Synthetic: Natural
* EU Regulation: Regulated
* FDA Regulation: Regulated
* CA Regulation: Regulated
* Purpose: Functions as a solvent.
* Health Concerns: None

Sodium Lauryl Sulfate:
* Natural or Synthetic: Synthetic
* EU Regulation: Regulated (Annex III/303 of the EU Cosmetics Regulation lists sodium lauryl sulfate with specific concentration limits based on the intended cosmetic use. For instance, in rinse-off hair products, the concentration limit is 1%.)
* FDA Regulation: Regulated (Considered safe when used in accordance with good manufacturing practices. FDA does not specify concentration limits for cosmetics containing sodium lauryl sulfate.)
* CA Regulation: Regulated (No specific restrictions mentioned for sodium lauryl sulfate in cosmetics under California regulations.)
* Purpose: Functions as a surfactant, foaming agent, and emulsifier.
* Health Concerns: Known to cause skin and eye irritation in some individuals. Some consumers opt for sulfate-free products due to concerns about potential drying effects on the skin and hair. However, scientific consensus on these concerns is not universal, and many products containing sulfates are considered safe for use.

Propylparaben:
* Natural or Synthetic: Synthetic
* EU Regulation: Limited to a concentration of 0.14% (regardless of whether mixture or single).
* FDA Regulation: Limited to 0.8% (as a mixture) and 0.4% (as a single paraben).
* CA Regulation: Banned as a food additive starting 2027 (California Food Safety Act)
* Purpose: Functions as a antimicrobial preservative. Commonly found in water-based products.
* Health Concerns: Parabens are known to be endocrine disruptors. It may negatively impact reproductive health and increase risk for malignant melanoma, one form of skin cancer (https://www.safecosmetics.org/chemicals/parabens/)

"""
