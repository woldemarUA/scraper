# generate product pages

import json
import itertools
import urllib.parse

base_url = "https://www.printoclock.com/carte-de-correspondance?q={}&inputs=&q={}"

# Load product data from the JSON file
with open("../json_configs/product_data.json", 'r') as f:
    product_data = json.load(f)

def generate_links(json_obj, base_url):
    # Gather options for each step
    data = json_obj["optionValues"]
    steps = json_obj["steps"]
    options = {}

    # Build a dictionary of options by step codes
    for key, value in data.items():
        option_code = value.get('optionCode')
        if option_code not in options:
            options[option_code] = []
        options[option_code].append(key)

    # List to store each step’s options in the order of steps
    option_lists = []
    for key in sorted(steps.keys(), key=lambda x: int(x)):  # Ensure order by step number
        step_code = steps[key]['code']
        option_lists.append(options[step_code])

    # Generate all combinations of options across steps
    all_combinations = itertools.product(*option_lists)

    # Create URLs for each combination and print them
    urls = []
    for combination in all_combinations:
        # Join options with '/' for each combination (like '100x210/350DM/R/NOSUV/NOF/NOENV/CLA')
        option_string = "/".join(combination)

        # Encode the option string for the URL
        encoded_options = urllib.parse.quote(option_string)

        # Format into the base URL
        url = base_url.format(encoded_options, encoded_options)
        urls.append(url)
        print(url)

    return urls





# import json
# base_url = "https://www.printoclock.com/carte-de-correspondance"

# with open("../json_configs/product_data.json", 'r') as f:
#     product_data = json.load(f)

# def generate_links(json_obj, base_url):
#     # data = json_obj["priceOptionValues"]
#     data = json_obj["optionValues"]
#     steps = json_obj["steps"]
#     options = {}
#     for key, value in data.items():
#         option_code = value.get('optionCode')
       
#         if option_code not in options:
#             options[option_code]=[]
#         options[option_code].append(key)
#     print(options)   
#     # options = {key: value.get('optionCode') for key, value in data.items() } #priceOptionValues
#     # print(steps)
#     for key in steps:
#         print(f'key: {key} ')
#         print(f'\noptions for this step are {options[steps[key]['code']]}')
        # for step_options in steps[key]['code']:
        #     print(f'step options: {step_options}')

# import json
# import itertools

# base_url = "https://www.printoclock.com/variant-url/carte-de-correspondance?optionCodes={}&group=anonymous"

# with open("../json_configs/product_data.json", 'r') as f:
#     product_data = json.load(f)

# def generate_links(json_obj, base_url):
#     # Gather options for each step
#     data = json_obj["optionValues"]
#     steps = json_obj["steps"]
#     options = {}

#     # Build a dictionary of options by step codes
#     for key, value in data.items():
#         option_code = value.get('optionCode')
#         if option_code not in options:
#             options[option_code] = []
#         options[option_code].append(key)

#     # List to store each step’s options in the order of steps
#     option_lists = []
#     for key in sorted(steps.keys(), key=lambda x: int(x)):  # Ensure order by step number
#         step_code = steps[key]['code']
#         option_lists.append(options[step_code])

#     # Generate all combinations of options across steps
#     all_combinations = itertools.product(*option_lists)

#     # Create URLs for each combination and print them
#     urls = []
#     for combination in all_combinations:
#         option_codes = ",".join(combination)
#         url = base_url.format(option_codes)
#         urls.append(url)
#         print(url)

#     return urls

# Run the function to generate URLs
# generate_links(product_data, base_url)


# import json
# import itertools
# import urllib.parse

# base_url = "https://www.printoclock.com/carte-de-correspondance?q={}&q={}&inputs="

# with open("../json_configs/product_data.json", 'r') as f:
#     product_data = json.load(f)

# def generate_links(json_obj, base_url):
#     # Gather options for each step
#     data = json_obj["optionValues"]
#     steps = json_obj["steps"]
#     options = {}

#     # Build a dictionary of options by step codes
#     for key, value in data.items():
#         option_code = value.get('optionCode')
#         if option_code not in options:
#             options[option_code] = []
#         options[option_code].append(key)

#     # List to store each step’s options in the order of steps
#     option_lists = []
#     for key in sorted(steps.keys(), key=lambda x: int(x)):  # Ensure order by step number
#         step_code = steps[key]['code']
#         option_lists.append(options[step_code])

#     # Generate all combinations of options across steps
#     all_combinations = itertools.product(*option_lists)

#     # Create URLs for each combination and print them
#     urls = []
#     for combination in all_combinations:
#         # Join options with '/' for each combination
#         unencoded_options = "/".join(combination)
#         encoded_options = urllib.parse.quote(unencoded_options)
        
#         # Format into the base URL
#         url = base_url.format(unencoded_options, encoded_options)
#         urls.append(url)
#         # print(url)
#     print(urls[0])
#     return urls

# Run the function to generate URLs

# import json
# import itertools
# import urllib.parse

# base_url = "https://www.printoclock.com/variant-url/carte-de-correspondance?optionCodes={}&group=anonymous"

# with open("../json_configs/product_data.json", 'r') as f:
#     product_data = json.load(f)

# def generate_links(json_obj, base_url):
#     # Gather options for each step
#     data = json_obj["optionValues"]
#     steps = json_obj["steps"]
#     options = {}

#     # Build a dictionary of options by step codes
#     for key, value in data.items():
#         option_code = value.get('optionCode')
#         if option_code not in options:
#             options[option_code] = []
#         options[option_code].append(key)

#     # List to store each step’s options in the order of steps
#     option_lists = []
#     for key in sorted(steps.keys(), key=lambda x: int(x)):  # Ensure order by step number
#         step_code = steps[key]['code']
#         option_lists.append(options[step_code])

#     # Generate all combinations of options across steps
#     all_combinations = itertools.product(*option_lists)

#     # Create URLs for each combination and print them
#     urls = []
#     for combination in all_combinations:
#         # Join options with ',' for each combination
#         option_string = ",".join(combination)
#         encoded_options = urllib.parse.quote(option_string)

#         # Format into the base URL
#         url = base_url.format(encoded_options)
#         urls.append(url)
#         print(url)

#     return urls





if __name__ == "__main__":
    generate_links(product_data, base_url)