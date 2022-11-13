# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 14:27:20 2022

@author: theja
"""

from google_images_search import GoogleImagesSearch

#API key and CX information (in that order)
#AIzaSyCEUrQCpyHvV9crC6mOnXQWi3dFmwu_H2o
#409f2a1ba9a2a4dd4

'''
Code provided by Google if we want a search bar on the HTML page (I think we can make the website functional without this)
<script async src="https://cse.google.com/cse.js?cx=409f2a1ba9a2a4dd4">
</script>
<div class="gcse-search"></div>
'''

#setup api connection
gis = GoogleImagesSearch('AIzaSyCEUrQCpyHvV9crC6mOnXQWi3dFmwu_H2o', '409f2a1ba9a2a4dd4')

#defined search parameters (Taken from API site example and modified slightly)
_search_params = {
    'q': 'dog',
    'num': 2,
    'fileType': 'jpg|gif|png',
    'rights': 'cc_publicdomain|cc_attribute|cc_sharealike|cc_noncommercial|cc_nonderived',
    'safe': 'active', ##
    'imgType': 'photo' ##
}

# search for images based on the search parameters
gis.search(search_params=_search_params)

#
for image in gis.results():
    image.url  # image direct url
    image.referrer_url  # image referrer url (source) 
    
    #Change this to your file path :D
    image.download("C:/Users/theja/Documents/photo app test/photo storage")  # download image
    
    #image.resize(500, 500)  # resize downloaded image (this is possible, but I did not use)

    image.path  # downloaded local file path
    print(image.path)       #This was to test it saved to the correct location on my pc