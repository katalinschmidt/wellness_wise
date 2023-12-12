import base64
import os
from .api_client import generate_ai_response
from .tesseract_utils import clean_img_text_for_ingredient_list, parse_text_from_image
from io import BytesIO
from flask import Blueprint, request, jsonify
from PIL import Image


# Create a Blueprint for routes with a name and opt package name, and register it in server.py
# Blueprints are a way to organize and structure the application into smaller, reusable components
# Common uses are authentication/user management, admin panel, API endpoints, etc.
main_bp = Blueprint('main', __name__)


# Define routes and views
# Routes are URL patterns or endpoints that define how the server should respond to specific client requests
# Views are Python functions or methods that are executed when a particular route is accessed
@main_bp.route('/')
def home():
    # TODO: Update return value when polishing interface
    return 'Welcome to the homepage!'


@main_bp.route('/upload', methods=['POST'])
def upload():
    # TODO: Remove following block of code after testing is complete.
    # Construct absolute path using working dir
    image_directory = 'app/temp_dir'
    # image_filename = 'cetaphil_cleanser.png'
    # image_filename = 'ogx_keratin_shampoo.png'
    # image_filename = 'dove_beauty_bar_1.png'
    image_filename = 'dove_beauty_bar_2.png'
    image_path = os.path.abspath(os.path.join(os.getcwd(), image_directory, image_filename))
    image = Image.open(image_path)

    # TODO: Uncomment following block of code when testing frontend functionality.
    # encoded_image_data = request.json.get('encodedImageStr')
    # if not encoded_image_data:
    #     # TODO: Decide appropriate response here.
    #     return {"is_upload_successful": False}
    #
    # # TODO: Implement file type validation and virus scanning
    #
    # # Decode & create PIL Image object from binary data
    # decoded_image_data = base64.b64decode(encoded_image_data)
    # image = Image.open(BytesIO(decoded_image_data))

    raw_text = parse_text_from_image(image)
    cleaned_list = clean_img_text_for_ingredient_list(raw_text)

    # TODO: Decide appropriate response here.
    #  Call OpenAI endpoint here?
    return {"is_upload_successful": True}


@main_bp.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('user_message')
    ai_response = generate_ai_response(user_message)

    if ai_response is not None:
        return jsonify({'ai_response': ai_response})
    else:
        return jsonify({'error': 'Failed to generate response'})
