from google_images_search import GoogleImagesSearch
import os
from dotenv import load_dotenv
load_dotenv() # take environment variables from .env.


# you can provide API key and CX using arguments,
# or you can set environment variables: GCS_DEVELOPER_KEY, GCS_CX
gis = GoogleImagesSearch(os.environ.get("API_KEY"), os.environ.get("GCS_CX"))

# define search params
# option for commonly used search param are shown below for easy reference.
# For param marked with '##':
#   - Multiselect is currently not feasible. Choose ONE option only
#   - This param can also be omitted from _search_params if you do not wish to define any value
_search_params = {
    'q': 'potato early bright disease',
    'num': 100,
    'fileType': 'jpeg',
    'imgType': 'photo', 
}

# this will only search for images:
gis.search(search_params=_search_params)

# this will search and download:
gis.search(search_params=_search_params, path_to_dir='./download/')

# this will search, download and resize:
gis.search(search_params=_search_params, path_to_dir='./download/', width=500, height=500)


# search first, then download and resize afterwards:
gis.search(search_params=_search_params)
for image in gis.results():
    print("downloading image")
    image.url  # image direct url
    image.referrer_url  # image referrer url (source) 
    
    image.download('./download/')  # download image
    

    image.path  # downloaded local file path