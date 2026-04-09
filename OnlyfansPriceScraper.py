"""
OnlyfansPriceScraper - V2.8.2
Captures both the current (trial/free) price AND the regular price in separate
Excel columns, so a "Free for 30 days / Regular price $10" profile is fully recorded.
"""

__version__ = "2.8.2"

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException, WebDriverException
import configparser
import os
import re
import json
import warnings
import argparse
import time
from datetime import datetime
from urllib.parse import urlparse

import pandas as pd
from openpyxl import load_workbook
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from tqdm import tqdm

warnings.filterwarnings("error", category=FutureWarning)

# ---------------------------------------------------------------------------
# Language selection
# ---------------------------------------------------------------------------

SUPPORTED_LANGUAGES = ['english', 'dutch', 'french', 'german', 'spanish']

parser = argparse.ArgumentParser(description='OnlyfansPriceScraper - select language.')
parser.add_argument(
    '-l', '--language',
    type=str,
    required=False,
    default='dutch',
    help='Language (english / dutch / french / german / spanish)'
)
args = parser.parse_args()

language_completer = WordCompleter(SUPPORTED_LANGUAGES, ignore_case=True)
session = PromptSession()

language_input = session.prompt(
    'Select language by using tab (default is "dutch"): ',
    completer=language_completer
)
args.language = language_input.strip().lower() if language_input.strip() else 'dutch'

# ---------------------------------------------------------------------------
# Load language strings
# ---------------------------------------------------------------------------

with open('Language.json', encoding='utf-8') as f:
    language_dict = json.load(f)

if args.language in language_dict:
    lang = language_dict[args.language]
    print(lang['language_set'])
else:
    print(f"Unknown language '{args.language}'. Defaulting to Dutch.")
    args.language = 'dutch'
    lang = language_dict['dutch']
    print(lang['language_set'])

# ---------------------------------------------------------------------------
# Load settings
# ---------------------------------------------------------------------------

config = configparser.ConfigParser()
config.read('Settings.ini')

user_agent      = config.get('Settings',     'user_agent',       fallback='')
high_price_first = config.getboolean('Settings', 'high_price_first', fallback=False)
low_price_first  = config.getboolean('Settings', 'low_price_first',  fallback=False)
append_mode      = config.getboolean('Settings', 'append_mode',      fallback=False)
page_load_wait   = config.getint('Settings',    'page_load_wait',    fallback=5)

if high_price_first and low_price_first:
    print("[WARNING] Both high_price_first and low_price_first are True. "
          "Defaulting to high_price_first.")
    low_price_first = False

# ---------------------------------------------------------------------------
# Load & validate URLs
# ---------------------------------------------------------------------------

config.read('Linkconfig.ini')
raw_urls = [config.get('URLs', key) for key in config['URLs']]

valid_urls, skipped = [], []
for url in raw_urls:
    parsed = urlparse(url)
    if (parsed.netloc
            and 'onlyfans.com' in parsed.netloc
            and parsed.path.strip('/') not in ('', 'example', 'profilename1',
                                               'profilename2', 'profilename3')):
        valid_urls.append(url)
    elif url:
        skipped.append(url)

if skipped:
    print(f"[INFO] Skipped {len(skipped)} invalid/placeholder URL(s).")
if not valid_urls:
    print("[ERROR] No valid OnlyFans URLs found in Linkconfig.ini. Exiting.")
    exit(1)

print(f"[INFO] {len(valid_urls)} valid URL(s) loaded.")

# ---------------------------------------------------------------------------
# Output setup
# ---------------------------------------------------------------------------

output_dir = "output"
os.makedirs(output_dir, exist_ok=True)
timestamp   = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_file = os.path.join(output_dir, f"output_{timestamp}.xlsx")

# ---------------------------------------------------------------------------
# Helper: extract price from scraped text
# ---------------------------------------------------------------------------

def extract_price(text: str):
    """
    Return a float price from text:
      - 'free' anywhere  → 0.0
      - '$9.99' pattern  → 9.99
      - otherwise        → None
    """
    if re.search(r'\bfree\b', text, re.IGNORECASE):
        return 0.0
    match = re.search(r'\$([0-9]+(?:[.,][0-9]+)?)', text)
    if match:
        return float(match.group(1).replace(',', '.'))
    return None

# ---------------------------------------------------------------------------
# Scraping — single driver reused across all URLs
# ---------------------------------------------------------------------------

options = Options()
options.add_argument("--headless")
if user_agent:
    options.add_argument(f"user-agent={user_agent}")

print("[INFO] Starting Firefox driver...")
try:
    driver = webdriver.Firefox(options=options)
except WebDriverException as e:
    print(f"[ERROR] Could not start Firefox/GeckoDriver: {e}")
    exit(1)

driver.implicitly_wait(10)
rows = []

try:
    for url in tqdm(valid_urls, desc=lang.get('progress_label', 'Scraping'), unit='profile'):
        try:
            driver.get(url)
            time.sleep(page_load_wait)

            price_element         = None
            regular_price_element = None
            limited_offer_element = None

            # --- Current / trial price button ---
            for class_name in ('b-wrap-btn-text', 'b-offer-join'):
                try:
                    price_element = driver.find_element(By.CLASS_NAME, class_name)
                    break
                except NoSuchElementException:
                    continue

            if price_element is None:
                tqdm.write(f"[SKIP] No price element found at: {url}")
                continue

            # --- Regular price label (only present when a trial/discount is active) ---
            # HTML: <span class="b-users__item__subscription-date__label">
            #           Regular price $10 /month
            #       </span>
            try:
                regular_price_element = driver.find_element(
                    By.CLASS_NAME, 'b-users__item__subscription-date__label'
                )
            except NoSuchElementException:
                pass

            # --- Limited offer: description line ---
            # HTML: <div class="b-offer-join__details">Limited offer - Free trial for 30 days!</div>
            limited_offer_desc = lang['no_limited_offer']
            try:
                desc_el = driver.find_element(By.CLASS_NAME, 'b-offer-join__details')
                limited_offer_desc = desc_el.text.strip()
            except NoSuchElementException:
                pass

            # --- Offer end date & offers left ---
            # HTML: multiple <div class="b-offer-join__left-time__el"> inside b-offer-join__left-time
            offer_end_date = '-'
            offers_left    = '-'
            try:
                time_els = driver.find_elements(By.CLASS_NAME, 'b-offer-join__left-time__el')
                for el in time_els:
                    text = el.text.strip()
                    if re.search(r'\d+\s+offers?\s+left', text, re.IGNORECASE):
                        offers_left = text
                    elif re.search(r'offer\s+ends', text, re.IGNORECASE):
                        offer_end_date = text
            except NoSuchElementException:
                pass

            # Parse current (trial/active) price
            price_text    = price_element.text.strip().replace('\n', ' ')
            current_price = extract_price(price_text)

            if current_price is None:
                tqdm.write(f"[SKIP] Could not parse price from '{price_text}' at: {url}")
                continue

            # Parse regular price — falls back to current price when no trial is active
            if regular_price_element:
                reg_text      = regular_price_element.text.strip().replace('\n', ' ')
                regular_price = extract_price(reg_text)
                if regular_price is None:
                    regular_price = current_price
            else:
                regular_price = current_price

            rows.append({
                'Link':          url,
                'Current Price': current_price,
                'Regular Price': regular_price,
                'Limited Offer': limited_offer_desc,
                'Offer Ends':    offer_end_date,
                'Offers Left':   offers_left,
            })

            tqdm.write(
                f"{lang['price_found']} {url}: "
                f"current=${current_price:.2f} / regular=${regular_price:.2f}"
            )
            tqdm.write(f"{lang['limited_offer_found']} {url}: {limited_offer_desc} | {offer_end_date} | {offers_left}")

        except WebDriverException as e:
            tqdm.write(f"[ERROR] Driver error on {url}: {e}")
            continue

finally:
    driver.quit()
    print("[INFO] Driver closed.")

# ---------------------------------------------------------------------------
# Build & sort DataFrame
# ---------------------------------------------------------------------------

if not rows:
    print("[WARNING] No data collected. Output file will not be created.")
    exit(0)

df = pd.DataFrame(rows, columns=['Link', 'Current Price', 'Regular Price', 'Limited Offer', 'Offer Ends', 'Offers Left'])

# Sorting is done on the numeric Regular Price column
sort_col = 'Regular Price'
if high_price_first:
    df = df.sort_values(by=sort_col, ascending=False)
elif low_price_first:
    df = df.sort_values(by=sort_col, ascending=True)

# Format both price columns with $ sign AFTER sorting
df['Current Price'] = df['Current Price'].apply(lambda p: f"${p:.2f}")
df['Regular Price'] = df['Regular Price'].apply(lambda p: f"${p:.2f}")

# ---------------------------------------------------------------------------
# Append mode
# ---------------------------------------------------------------------------

if append_mode:
    existing_files = sorted(
        [f for f in os.listdir(output_dir)
         if f.startswith('output_') and f.endswith('.xlsx')
         and f != os.path.basename(output_file)],
        reverse=True
    )
    if existing_files:
        latest = os.path.join(output_dir, existing_files[0])
        try:
            old_df = pd.read_excel(latest)
            for col in ('Current Price', 'Regular Price'):
                if col in old_df.columns:
                    old_df[col] = (old_df[col].astype(str)
                                              .str.replace('$', '', regex=False)
                                              .astype(float))
            df_numeric = df.copy()
            for col in ('Current Price', 'Regular Price'):
                df_numeric[col] = (df_numeric[col].astype(str)
                                                   .str.replace('$', '', regex=False)
                                                   .astype(float))
            merged = pd.concat([old_df, df_numeric], ignore_index=True)
            merged = merged.drop_duplicates(subset='Link', keep='last')
            for col in ('Current Price', 'Regular Price'):
                merged[col] = merged[col].apply(lambda p: f"${p:.2f}")
            df = merged
            print(f"[INFO] Append mode: merged with {latest}")
        except Exception as e:
            print(f"[WARNING] Could not read previous file for append: {e}")

# ---------------------------------------------------------------------------
# Save to Excel & auto-adjust column widths
# ---------------------------------------------------------------------------

df.to_excel(output_file, index=False)

wb = load_workbook(output_file)
ws = wb.active

for col in ws.columns:
    max_length = 0
    col_letter = col[0].column_letter
    for cell in col:
        try:
            cell_len = len(str(cell.value)) if cell.value is not None else 0
            if cell_len > max_length:
                max_length = cell_len
        except TypeError:
            pass
    ws.column_dimensions[col_letter].width = max_length + 4

wb.save(output_file)

print(f"\n[DONE] Results saved to: {output_file}")
print(f"[INFO] {len(df)} profile(s) written.")
