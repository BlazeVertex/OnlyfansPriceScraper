<a id="English-updates"></a>
## Fixes in V2.8.2
- [x] # Version 2.8.2 - Release Update
> [!NOTE]
> After years a new update

We are pleased to announce some significant improvements and new features in this release of our project. Here is an overview of the changes:

## 🚀 Version 2.8.2 – Release Update

### ✨ Key Changes

#### 1. Free Trial Detection
Profiles with a free trial subscription (e.g. "Subscribe FREE for 30 days") are now correctly detected and recorded as **$0.00** instead of being skipped.

#### 2. Split Price Columns
The **Price** column has been split into:
- **Current Price** – what you pay right now (including trials)
- **Regular Price** – the normal monthly price after the trial ends

#### 3. Offers Left Column
The "X offers left" information from limited offers is now saved in its own dedicated column instead of being included in the limited offer text.

#### 4. Offer Ends Column
Offer expiry dates (e.g. "Offer ends May 1") are now stored in a separate column.

#### 5. Dollar Sign in Price Columns
Prices are now displayed with a **$ sign** (e.g. `$9.99`) for clear monetary formatting in Excel.

#### 6. Single Driver Instance
Firefox is now opened once and reused for all URLs instead of opening and closing for each profile, significantly improving performance.

#### 7. Progress Bar
A **tqdm progress bar** now shows scraping progress in the terminal.

#### 8. Timestamped Output Files
Output files now include a timestamp in the filename (e.g. `output_2024-03-06_14-30-00.xlsx`) to prevent overwriting.

#### 9. Append Mode
A new `append_mode` setting in `Settings.ini` allows merging new results with previous output instead of always starting fresh.

#### 10. Configurable Page Wait
Page load wait time is now configurable via `page_load_wait` in `Settings.ini` instead of being hardcoded.

#### 11. Script Renamed
The main script is now `OnlyfansPriceScraper.py`, with the version tracked internally using `__version__` instead of in the filename.

