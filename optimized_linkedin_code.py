from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os
import pandas as pd
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from selenium.webdriver.support import expected_conditions as EC


# Initialize the WebDriver for Firefox
options = Options()
options.headless = False  # Run in headless mode (no GUI)


service = Service()
driver = webdriver.Firefox(service=service, options=options)

# LinkedIn login
driver.get("https://www.linkedin.com/login")
username = driver.find_element(By.ID, "username")
password = driver.find_element(By.ID, "password")

username.send_keys("aslanemil008@gmail.com")
password.send_keys("aslankaren27+")
password.send_keys(Keys.RETURN)


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
    "INSEAD",
    "Khalifa University",
    "New York University Abu Dhabi",
    "Paris-Sorbonne University Abu Dhabi",
    "Syscoms Institute",
    "United Arab Emirates University",
    "Zayed University",
    "Higher Colleges of Technology",
    "University of Dubai",
    "Al Dar University College",
    "Al Ghurair University",
    "American College of Dubai",
    "American University in Dubai",
    "American University in the Emirates",
    "Amity University Dubai",
    "British University in Dubai",
    "Canadian University Of Dubai",
    "Dubai Medical College for Girls",
    "The Emirates Academy of Hospitality Management",
    "Emirates Aviation University",
    "Emirates College for Management & Information Technology",
    "Hamdan Bin Mohammed Smart University",
    "Institute of Management Technology, Dubai",
    "International Horizons College",
    "Middlesex University Dubai",
    "MODUL University Dubai",
    "Murdoch University Dubai",
    "Rochester Institute of Technology, Dubai",
    "S P Jain School of Global Management",
    "Skyline University College",
    "Synergy University Dubai",
    "University of Dubai",
    "University of Wollongong in Dubai",
    "American University of Sharjah",
    "Higher Colleges of Technology",
    "Khalifa University",
    "University of Sharjah",
    "Ajman University",
    "Gulf Medical University",   
    "American University of Ras Al Khaimah",
    "Bolton University of Ras Al Khaimah",
    "London American City College",
    "RAK Medical & Health Sciences University"
]

list_last_names =[
    "Menezes", "Joseph", "Thomas", "George", "Paul", "Kuriakose", "Francis", "John", "Vas", 
    "Almeida", "Fernandes", "Rodrigues", "Silva", "Gomes", "Pereira", "Dias", "Mathew"
]

# Function to scrape profiles
def scrape_linkedin_profiles(driver, school, last_name, output_file):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "search-results-container")))
    scraped_data = []

    # Locate profiles and extract information
    try:
        search_results_container = driver.find_element(By.CLASS_NAME, "search-results-container")
        ul_element = search_results_container.find_element(By.TAG_NAME, 'ul')
        li_elements = ul_element.find_elements(By.CSS_SELECTOR, "li.reusable-search__result-container")

        for profile in li_elements:
            name = profile.find_element(By.CSS_SELECTOR, "span[aria-hidden='true']").text
            profile_title = profile.find_element(By.CSS_SELECTOR, "div.entity-result__primary-subtitle").text
            linkedin_element = profile.find_element(By.CSS_SELECTOR, "a.app-aware-link")
            linkedin_url = linkedin_element.get_attribute("href").split('?')[0]

            first_name = name.split()[0] if name.split()[0].lower() != last_name.lower() else None

            scraped_data.append({
                "First Name": first_name,
                "Last Name": last_name,
                "University": school,
                "Profession": profile_title,
                "LinkedIn URL": linkedin_url
            })

    except Exception as e:
        print(f"Error occurred while scraping: {e}")
        return

    # Save data to Excel
    df_new = pd.DataFrame(scraped_data)
    if os.path.exists(output_file):
        df_existing = pd.read_excel(output_file)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_new

    df_combined.to_excel(output_file, index=False)
    print(f"Data has been updated in {output_file}")

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

        actions = ActionChains(driver)
        actions.send_keys(Keys.DOWN).perform()
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
        time.sleep(5)
        reset_button = driver.find_element(By.XPATH, "//button[@aria-label='Reset applied filters']")
        reset_button.click()
        time.sleep(2)


driver.quit()



--------------------------------------------------------------------------------
def scrape_linkedin_profiles(driver, school, last_name, output_file):
    # Wait for the results container to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "search-results-container"))
    )
    scraped_data = []
    # Locate the search results container and ul element
    search_results_container = driver.find_element(By.CLASS_NAME, "search-results-container")

    try:
        ul_element = search_results_container.find_element(By.TAG_NAME, 'ul')
    except:
        # Exit the function if the 'ul' element is not found
        return

    
    # Get all 'li' elements (profiles)
    li_elements = ul_element.find_elements(By.CSS_SELECTOR, "li.reusable-search__result-container")
    
    # Loop through each profile and extract information
    for profile in li_elements:
        # time.sleep(20)
        # print(profile)
        name = profile.find_element(By.CSS_SELECTOR, "span[aria-hidden='true']").text  
        name_parts = name.split()
        first_name = next((part for part in name_parts if part.lower() != last_name.lower()), None)  # Get first name excluding last name

        profile_title = profile.find_element(By.CSS_SELECTOR, "div.entity-result__primary-subtitle").text  # Adjusted for job title
        linkedin_element = profile.find_element(By.CSS_SELECTOR, "a.app-aware-link")
        linkedin_url = linkedin_element.get_attribute("href")

        linkedin_url = linkedin_url.split('?')[0]
       
        scraped_data.append({
                "First Name": first_name,
                "Last Name": last_name,
                "Name of University": school,
                "Current Profession": profile_title,
                "LinkedIn URL": linkedin_url
        })

    df_new = pd.DataFrame(scraped_data)  # Assuming scraped_data is already defined

    chunk_size = 1000  # Set a chunk size (adjust as needed)

        # Check if the file already exists
    if os.path.exists(output_file):
            # Load the existing data from the Excel file
        df_existing = pd.read_excel(output_file)
            # Append the new data to the existing data
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
            # If the file does not exist, use the new data only
        df_combined = df_new

        # Write the combined DataFrame to the Excel file in chunks
    try:
        with pd.ExcelWriter(output_file, engine='openpyxl', mode='w') as writer:
            startrow = 0
            for chunk in np.array_split(df_combined, max(1, len(df_combined) // chunk_size)):
                chunk.to_excel(writer, sheet_name='Sheet1', startrow=startrow, header=(startrow == 0), index=False)
                startrow += len(chunk)  # Update the starting row for the next chunk
        print(f"Data has been updated in {output_file}")
    except Exception as e:
        print(f"Failed to write to Excel: {e}")