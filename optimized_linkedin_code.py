from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
import time
import os
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install())) 


# LinkedIn login
driver.get("https://www.linkedin.com/login")
username = driver.find_element(By.ID, "username")
password = driver.find_element(By.ID, "password")

username.send_keys("jastinbrendon@gmail.com")  # replace with your email
password.send_keys("aslanemil0616//") 
password.send_keys(Keys.RETURN)
time.sleep(3)

# Search smth
search_input = driver.find_element(By.CSS_SELECTOR, '.search-global-typeahead__input')
search_input.clear()
search_input.send_keys(Keys.RETURN)

time.sleep(5)



# Click the "People" button
people_input = driver.find_element(By.TAG_NAME, "button") 
for button in driver.find_elements(By.TAG_NAME, "button"):
    if button.text == "People":
        people_input = button
        break

if people_input:
    people_input.click()
else:
    print("Button with text 'People' not found.")

time.sleep(5)

list_universities = [ 
    "Abu Dhabi University",
    "Emirates College for Advanced Education",
    "Higher Colleges of Technology",
    
]

list_last_names =["Menezes","Joseph","Thomas","George", "Paul", "Kuriakose", "Francis", "John", "Vas", 
                  "Almeida", "Fernandes", "Rodrigues", "Silva", "Gomes", "Pereira", "Dias", "Mathew"
]

# Function to scrape profiles
def scrape_linkedin_profiles(driver, school, last_name, output_file):
    # Wait for the results to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "search-results-container"))
    )

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    links = set()
    for tag in soup.find_all('a', attrs={"data-test-app-aware-link": True}):
        href = tag.get("href")
        if href and "/in/" in href:
            links.add(href.split('?')[0]) 

    names = []
    for tag in soup.select("a span[aria-hidden='true']"):
        name_text = tag.get_text(strip=True)
        if name_text:
            names.append(name_text)

    # Combine names and URLs (safely)
    scraped_data = []
    for name, url in zip(names, links):
        name_parts = name.split()
        first_name = next((part for part in name_parts if part.lower() != last_name.lower()), None)

        scraped_data.append({
            "First Name": first_name,
            "Last Name": last_name,
            "Name of University": school,
            "LinkedIn URL": url
        })

    if not scraped_data:
        print(f"No data found for {last_name} at {school}")
        return

    # Save to Excel
    df_new = pd.DataFrame(scraped_data)
    chunk_size = 1000

    if os.path.exists(output_file):
        df_existing = pd.read_excel(output_file)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_new

    try:
        with pd.ExcelWriter(output_file, engine='openpyxl', mode='w') as writer:
            startrow = 0
            for chunk in np.array_split(df_combined, max(1, len(df_combined) // chunk_size)):
                chunk.to_excel(writer, sheet_name='Sheet1', startrow=startrow, header=(startrow == 0), index=False)
                startrow += len(chunk)
        print(f"Data has been updated in {output_file}")
    except Exception as e:
        print(f"Failed to write to Excel: {e}")


# Loop through universities and last names
for school in list_universities:
    for last_name in list_last_names:
        # Click 'Show all filters' button
        all_filters_button = driver.find_element(By.XPATH, "//button[@aria-label='Show all filters. Clicking this button displays all available filter options.']")
        all_filters_button.click()
        driver.execute_script("arguments[0].scrollIntoView(true);", all_filters_button)
        time.sleep(2)

        # Add location (You can skip this if the location is constant)
        add_location_button = driver.find_element(By.XPATH, "//button[span[text()='Add a location']]")
        add_location_button.click()

        location_input = driver.find_element(By.XPATH, "//input[@placeholder='Add a location']")
        location_input.clear()  
        location_input.send_keys("United Arab Emirates")
        time.sleep(2)
        driver.find_element(By.XPATH, "//input[@aria-label='Add a location']").click()

        actions = ActionChains(driver) #classa vory kataruma mkniki kam steexnashari knopkeqy
        actions.send_keys(Keys.DOWN).perform() #perform ogt vor et gorcoxutyuny katarelu hamar
        actions.send_keys(Keys.ENTER).perform()
        time.sleep(2)

        # Find and click 'Add a school' button
        dialog = driver.find_element(By.CSS_SELECTOR, "div[role='dialog']")
        add_school_button = dialog.find_element(By.XPATH, "//button[span[text()='Add a school']]")
        add_school_button.click()

        school_input = dialog.find_element(By.XPATH, "//input[@placeholder='Add a school']")
        school_input.clear()
        school_input.send_keys(school)
        time.sleep(2)
        dialog.find_element(By.XPATH, "//input[@aria-label='Add a school']").click()

        school_actions = ActionChains(driver)
        school_actions.send_keys(Keys.DOWN).perform()
        school_actions.send_keys(Keys.ENTER).perform()
        time.sleep(2)

        # Scroll to and fill 'Last name'
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", dialog)
        time.sleep(1)

        input_field = dialog.find_element(By.CSS_SELECTOR, "ul.display-flex:nth-child(2) > li:nth-child(2) input")
        input_field.clear()
        input_field.send_keys(last_name)
        time.sleep(2)

        # Press 'Show results' button
        show_results = dialog.find_element(By.XPATH, "//button[@aria-label='Apply current filters to show results']")
        show_results.click()

        # Wait for the results to load
        time.sleep(5)

        # (Optional) You can add logic here to extract data from the results
        scrape_linkedin_profiles(driver, school, last_name, "linkedin_scraped_data.xlsx")
        # Reset filters
        time.sleep(15)
        reset_button = driver.find_element(By.XPATH, "//button[@aria-label='Reset applied filters']")
        reset_button.click()
        time.sleep(2)


driver.quit()
