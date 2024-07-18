
import json 
from sentence_transformers import util
import numpy as np
import torch
from transformers import BertTokenizer, BertModel

# Return a python dictionary of website categories : list of [website name, website url]
def get_websites(): 
    # Read in website + area pairs
    with open('captcha_check/website_list.txt', 'r') as f:
        website_file_lines = f.readlines()

    # Filter out website names and categorize them by area
    website_area_info = [ i.strip().split(", ") for i in website_file_lines ]

    # Capitilize area (keys)
    website_area_info = ["https://www." + web_info[2] + "/" for web_info in website_area_info]

    return website_area_info

if __name__ == "__main__":
    print(get_websites())

  

    
    

    
    




    

