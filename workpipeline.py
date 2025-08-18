from fetch_page import *
from msphi3 import get_reponse
import json 


def dict_to_json(data_dict, file_path=None, indent=4):
    """
    Convert a Python dictionary to JSON format.
    
    Args:
        data_dict (dict): The dictionary to convert
        file_path (str, optional): Path to save JSON file. If None, returns JSON string
        indent (int): Number of spaces for indentation (default: 4)
    
    Returns:
        str: JSON string if file_path is None
        None: If file_path is provided (saves to file)
    """
    if file_path:
        with open(file_path, 'w') as f:
            json.dump(data_dict, f, indent=indent)
    else:
        return json.dumps(data_dict, indent=indent)

def json_to_dict(json_input):
    """
    Convert JSON to Python dictionary.
    
    Args:
        json_input (str): Either a JSON string or path to JSON file
    
    Returns:
        dict: Python dictionary from JSON data
    """
    if json_input.endswith('.json') or '/' in json_input or '\\' in json_input:
        with open(json_input, 'r') as f:
            return json.load(f)
    else:
        return json.loads(json_input)

def extract_save_info(url):
    try:
    # Example usage - get clean text from a webpage
        clean_text = get_clean_page_text(url)
        # print(clean_text[:5000])
        n = 5000
        resp = get_reponse("""Extract information about the researcher from this text. I want the following information in a dictionary,{"name": "name with designation" ,"email": "email address of the person","university" : "name of the university","department": "name of department", "research": "a small paragraph about their research" ,"prospective_students" : "any information on the page about how procepective students should approach them"}. Do not use any quotes, single or double inside any of the strings in the dictionary. Reply only with the dictionary written in a single line in python legal format nothing more.\n"""+clean_text[:n])
        resp_dict = eval(resp.strip())
        resp_dict["url"] = url
        json_name = resp_dict["name"].replace(" ","")
        dict_to_json(resp_dict,"saved_json/{}.json".format(json_name))
    
        
    except RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    url_lst = ["https://sites.google.com/view/sanjay-shakkottai/","https://www.cs.utexas.edu/people/faculty-researchers/kristen-grauman","https://www.cs.utexas.edu/people/faculty-researchers/david-harwath"]
    for url in url_lst:
        extract_save_info(url)
    