from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import configparser
import time
from selenium.common.exceptions import NoSuchElementException
import os
import csv
import argparse
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter

# Maak een ArgumentParser object
parser = argparse.ArgumentParser(description='Select the language for your Python project.')

# Voeg een argument toe voor de taal
parser.add_argument('-l', '--language', type=str, required=False, default='dutch', help='Select the language (for example. "english" or "dutch")')

# Parse de argumenten
args = parser.parse_args()

# Maak een WordCompleter voor de taalargumenten
language_completer = WordCompleter(['english', 'dutch'], ignore_case=True)

# Maak een PromptSession
session = PromptSession()

# Vraag de gebruiker om de taal in te voeren
language = session.prompt('Select language by using tab (default is "dutch"): ', completer=language_completer)
args.language = language if language else 'dutch'

# Taalondersteuning
language_dict = {
 'english': {
    'language_set': 'Language is set on English',
    'no_limited_offer': 'No limited offer found.'
 },
 'dutch': {
    'language_set': 'Taal is ingesteld op Nederlands',
    'no_limited_offer': 'Geen limited offer gevonden.'
 }
}

# Controleer de geselecteerde taal
if args.language in language_dict:
  print(language_dict[args.language]['language_set'])
else:
  print("Unknown language selected. Language is set to Dutch as default.")
  print(language_dict['dutch'])

def get_onlyfans_prices(profile_url):
   options = Options()
   options.add_argument("--headless")
   driver = webdriver.Firefox(options=options)

   driver.get(profile_url)

   time.sleep(5)

   driver.implicitly_wait(10)

   price_element = None
   limited_offer_element = None

   try:
       price_element = driver.find_element(By.CLASS_NAME, 'b-wrap-btn-text')
   except NoSuchElementException:
       try:
           price_element = driver.find_element(By.CLASS_NAME, 'b-offer-join')
       except NoSuchElementException:
           print(f"Geen van de elementen gevonden op {profile_url}")
           return profile_url, 'Prijs niet gevonden op de opgegeven URL.', 'Geen limited offer opgegeven.'

   try:
       limited_offer_element = driver.find_element(By.CLASS_NAME, 'b-offer-join__content')
   except NoSuchElementException:
       pass

   if price_element:
       price = price_element.text.strip()
   else:
       price = 'Prijs niet gevonden op de opgegeven URL.'

   if limited_offer_element:
       limited_offer = limited_offer_element.text.strip()
   else:
       limited_offer = language_dict[args.language]['no_limited_offer']

   driver.quit()

   return profile_url, price, limited_offer


config = configparser.ConfigParser()
config.read('Settings.ini')

user_agent = config.get('Settings', 'user_agent')

options = Options()
options.add_argument(f"user-agent={user_agent}")

config.read('Linkconfig.ini')

urls = [config.get('URLs', url) for url in config['URLs'] if url != 'user_agent']

output_dir = "output"
if not os.path.exists(output_dir):
 try:
    os.mkdir(output_dir)
    print(f"Successfully created the directory {output_dir}")
 except OSError:
    print(f"Creation of the directory {output_dir} failed")
else:
 print(f"Directory {output_dir} already exists")

output_file = os.path.join(output_dir, "output.csv")

if os.path.isfile(output_file):
 os.remove(output_file)
 print(f"Old data in {output_file} removed")
else:
 print(f"No old data to remove in {output_file}")

with open(output_file, 'w', newline='') as f:
 writer = csv.writer(f, delimiter=',')
 writer.writerow([language_dict.get('link', 'Link'), 
                   language_dict.get('price', 'Price'), 
                   language_dict.get('limited_offer', 'Limited Offer')])

 for url in urls:
   profile_url, price, limited_offer = get_onlyfans_prices(url)
   if args.language == 'english':
       print('Price found at {}: {}'.format(url, price))
       print('Limited Offer found at {}: {}'.format(url, limited_offer))
   else:
     if args.language == 'dutch':
       print('Prijs gevonden op {}: {}'.format(url, price))
       print('Limited Offer gevonden op {}: {}'.format(url, limited_offer))
   writer.writerow([profile_url, price, limited_offer])
