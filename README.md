# Linkedin Special Data Scraping

## Introduction
This repository contains the code and the XLSX file where the scraped results are stored.
The code scrapes university pages on LinkedIn using a list of university names and last names provided in the code.
It collects and stores data for matching individuals, including:

- First Name

- Last Name

- University

- Profession

- LinkedIn URL

## Getting Started  
### Usage

<b>1. First, clone this repository:</b>
```bash
git clone https://github.com/AslanEmil008/LinkedIn-Special-Data-Scraping.git
cd LinkedIn-Special-Data-Scraping
```
<b>2. Install the required packages:</b>
```bash
pip install -r requirements.txt
```

## How to Run
<b>1. In the code, locate these lines:</b>
```bash
username.send_keys("email")   # replace with your email  
password.send_keys("password")   # replace with your password
```
<b>Change them to your actual LinkedIn email and password.</b>

<b>2. If you want to run this code for your specific universities, locate and modify this list:</b>

```bash
list_universities = [ 
    "Abu Dhabi University",
    "Emirates College for Advanced Education",
    "Higher Colleges of Technology",
    ...
]
```
<b>Replace the universities with your own list.</b>


<b>3. If you want to search for people with specific last names, change this list:</b>

```bash
list_last_names = [
    "Menezes", "Joseph", "Thomas", "George", "Paul", "Kuriakose", 
    "Francis", "John", "Vas", "Almeida", "Fernandes", "Rodrigues", 
    "Silva", "Gomes", "Pereira", "Dias", "Mathew"
]
```
<b>4. After making the changes, run the code:</b>

```bash
python3 optimized_linkedin_code.py
```



