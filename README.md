# BuildingConnected Employee Data Extractor

![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![Selenium](https://img.shields.io/badge/selenium-4.0%2B-orange)

A Python script to automate login and extract employee data from BuildingConnected's directory.

## Installation

### Prerequisites

-- Python 3.7 or higher - Download from [python.org](https://www.python.org/downloads/)

-- Chrome Browser - Latest version installed

-- ChromeDriver - Download the version matching your Chrome browser from [chromedriver.chromium.org](https://chromedriver.chromium.org/downloads)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Deepraj-chawda/Scraper/buildingconnected-scraper.git
   cd buildingconnected-scraper
   
2. Install dependencies:

   ```bash
   pip install selenium requests csv json

3. Place ChromeDriver in your PATH:
   Place chromedriver.exe in your Python Scripts folder
Download ChromeDriver from [chromedriver.chromium.org](https://developer.chrome.com/docs/chromedriver/downloads) and add to PATH

## Usage Instructions

###1. Run the script:
   
   ```bash
    python buildingconnected_scraper.py 
```

### 2. Enter credentials when prompted:

i) BuildingConnected email

ii) BuildingConnected password

iii) Verification code(when asked)

### 3. Output files:

`buildingconnected_data.json` - Full dataset in JSON format

`buildingconnected_data.csv` - Same data in CSV format
