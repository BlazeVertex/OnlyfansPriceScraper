> [!NOTE]
> I used Python version 3.12.0

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

Todo list:
- [ ] Make in settings.ini that you are able to choose if you want to create every time a new file or either way keep as is. (overwrites old data every time)

# OnlyfansPriceScraperV2.6.1
This repository houses a Python script that employs Selenium for web scraping. The script extracts pricing details from specified profiles, allowing users to choose between English and Dutch via a command-line interface. It navigates through provided profile URLs, extracts price and limited offer information, and outputs the results to a Excel file.

# Nederlandse Beschrijving:
Deze repository bevat een Python-script dat Selenium gebruikt voor webscraping-doeleinden. Het script haalt prijsinformatie op uit opgegeven profielen. Gebruikers kiezen een taal (Engels of Nederlands) via een command-line interface. Het script navigeert vervolgens door opgegeven profiel-URL's, haalt prijs- en limited offer-informatie op en geeft de resultaten uit naar een excel bestand.

## Fixes in V2.6.1
- [x] Excel Conversion: All data is now converted to Excel format instead of CSV, enhancing compatibility.
Updated README on GitHub.

## Verbeteringen in V2.6.1
- [x] Excel Conversie: Alle gegevens worden nu omgezet naar het Excel-formaat in plaats van CSV, wat de compatibiliteit verbetert.
README bijgewerkt op GitHub.

# Usage
**English**:

You need Firefox and [GeckoDriver](https://github.com/mozilla/geckodriver/releases)
To use this script, you'll need to add the GeckoDriver to your system's PATH. GeckoDriver is a link between your Selenium tests and the Firefox browser, which is used in this script. Here's how you can do it:

>   Download the appropriate version of GeckoDriver for your system from the releases page on GitHub.
    Extract the downloaded file to get the GeckoDriver executable.
    Add the directory containing the GeckoDriver executable to your system's PATH. 
    On Windows, you can do this by opening the System Properties, clicking on Environment Variables, selecting Path under System variables, and then clicking on Edit.
    Click on New, paste the path to the GeckoDriver directory, and then click on OK.

You'll also need to add a user agent to the settings file. This is a string that your browser sends to websites to tell them information about the browser and operating system. You can add it to the Settings.ini file in your script's directory with the following format:

``[Settings]
user_agent = your_user_agent_here``

``Replace your_user_agent_here with the user agent string you want to use.``

Open a terminal or command prompt.

Navigate to the directory containing your requirements.txt file:

bash

``cd path/to/your/project``

Install the required packages with this command:

bash

    pip install -r requirements.txt

That's it! Pip will now install all the required packages as specified in the requirements.txt file.

To use the program, make sure you are in the correct directory using the terminal or command prompt. Then, type the following command:

bash

``python project_name.py``

Replace "project_name.py" with the actual name of your Python file. This command will execute the Python script, and the program should run as intended.

Side note: **For now, the Excel file is overwritten after each scan. Copy it elsewhere for safety if needed.**

``It is a well-known limitation of Excel that hyperlinks are not directly active. This is a security measure to prevent potentially harmful hyperlinks from opening automatically. The user needs to perform a second click to activate the hyperlink. This is a default setting in Excel.``

**Dutch**:

je hebt Firefox nodig en [GeckoDriver](https://github.com/mozilla/geckodriver/releases)
Om dit script te gebruiken, moet u de GeckoDriver toevoegen aan het pad van uw systeem. GeckoDriver is een link tussen uw Selenium-tests en de Firefox-browser, die in dit script wordt gebruikt. Hier is hoe u dit kunt doen:

>   Download de juiste versie van GeckoDriver voor uw systeem van de releases-pagina op GitHub.
    Pak het gedownloade bestand uit om het GeckoDriver-uitvoerbare bestand te krijgen.
    Voeg de map die het GeckoDriver-uitvoerbare bestand bevat toe aan het pad van uw systeem.
    Op Windows kunt u dit doen door de Systeemeigenschappen te openen, op Environment Variables te klikken, onder Systeemvariabelen Path te selecteren en vervolgens op            Bewerken te klikken. 
    Klik op Nieuw, plak het pad naar de map met het GeckoDriver-uitvoerbare bestand en klik vervolgens op OK.

U moet ook een user agent toevoegen aan het instellingenbestand. Dit is een string die uw browser naar websites stuurt om informatie over de browser en het besturingssysteem te geven. U kunt deze toevoegen aan het Settings.ini-bestand in de directory van uw script met de volgende opmaak:

``[Settings]
user_agent = uw_user_agent_hier``

``Vervang uw_user_agent_hier door de user agent string die u wilt gebruiken.``

Dan open je een terminal of command prompt.

Navigeer naar de map met je requirements.txt:

bash

``cd pad/naar/je/project``

Installeer de vereiste pakketten met dit commando:

bash

    pip install -r requirements.txt

Dat is het! Pip zal nu alle vereiste pakketten installeren zoals gespecificeerd in het requirements.txt bestand.

Om het programma te gebruiken, zorg ervoor dat je in de juiste map bent via de terminal of opdrachtprompt. Typ vervolgens het volgende commando:

bash

``python project_naam.py``

Vervang "project_naam.py" door de daadwerkelijke naam van je Python-bestand. Met dit commando wordt het Python-script uitgevoerd, en het programma zou zoals bedoeld moeten worden uitgevoerd.

Ter info: **Verloopig word de Excel na elke scan herschreven en kopieer voor de zekerheid ergens anders indien nodig**

``Het is een bekende beperking van Excel dat hyperlinks niet direct actief zijn. Dit is een veiligheidsmaatregel om te voorkomen dat mogelijk schadelijke hyperlinks automatisch worden geopend. De gebruiker moet een tweede klik uitvoeren om de hyperlink te activeren. Dit is een standaardinstelling in Excel.``
