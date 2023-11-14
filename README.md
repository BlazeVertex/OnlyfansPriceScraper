# OnlyfansPriceScraperV2.4
This repository houses a Python script that employs Selenium for web scraping. The script extracts pricing details from specified profiles, allowing users to choose between English and Dutch via a command-line interface. It navigates through provided profile URLs, extracts price and limited offer information, and outputs the results to a CSV file.

# Nederlandse Repositorium Beschrijving:
Deze repository bevat een Python-script dat Selenium gebruikt voor webscraping-doeleinden. Het script haalt prijsinformatie op uit opgegeven profielen. Gebruikers kiezen een taal (Engels of Nederlands) via een command-line interface. Het script navigeert vervolgens door opgegeven profiel-URL's, haalt prijs- en limited offer-informatie op en geeft de resultaten uit naar een CSV-bestand.


# Usage
**English**:

You need [GeckoDriver](https://github.com/mozilla/geckodriver/releases)
To use this script, you'll need to add the GeckoDriver to your system's PATH. GeckoDriver is a link between your Selenium tests and the Firefox browser, which is used in this script. Here's how you can do it:

    Download the appropriate version of GeckoDriver for your system from the releases page on GitHub.
    Extract the downloaded file to get the GeckoDriver executable.
    Add the directory containing the GeckoDriver executable to your system's PATH. 
    On Windows, you can do this by opening the System Properties, clicking on Environment Variables, selecting Path under System variables, and then clicking on Edit.
    Click on New, paste the path to the GeckoDriver directory, and then click on OK.

You'll also need to add a user agent to the settings file. This is a string that your browser sends to websites to tell them information about the browser and operating system. You can add it to the Settings.ini file in your script's directory with the following format:

``[Settings]
user_agent = your_user_agent_here``

``Replace your_user_agent_here with the user agent string you want to use.``

**Dutch**:

je hebt dit nodig [GeckoDriver](https://github.com/mozilla/geckodriver/releases)
Om dit script te gebruiken, moet u de GeckoDriver toevoegen aan het pad van uw systeem. GeckoDriver is een link tussen uw Selenium-tests en de Firefox-browser, die in dit script wordt gebruikt. Hier is hoe u dit kunt doen:

    Download de juiste versie van GeckoDriver voor uw systeem van de releases-pagina op GitHub.
    Pak het gedownloade bestand uit om het GeckoDriver-uitvoerbare bestand te krijgen.
    Voeg de map die het GeckoDriver-uitvoerbare bestand bevat toe aan het pad van uw systeem.
    Op Windows kunt u dit doen door de Systeemeigenschappen te openen, op Environment Variables te klikken, onder Systeemvariabelen Path te selecteren en vervolgens op             Bewerken te klikken. 
    Klik op Nieuw, plak het pad naar de map met het GeckoDriver-uitvoerbare bestand en klik vervolgens op OK.

U moet ook een user agent toevoegen aan het instellingenbestand. Dit is een string die uw browser naar websites stuurt om informatie over de browser en het besturingssysteem te geven. U kunt deze toevoegen aan het Settings.ini-bestand in de directory van uw script met de volgende opmaak:

``[Settings]
user_agent = uw_user_agent_hier``

``Vervang uw_user_agent_hier door de user agent string die u wilt gebruiken.``
