from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

# --- 1. SETUP ---
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 20)

try:
    # --- 2. LOGIN SEQUENCE ---
    driver.get("https://atlas.heart.org/")

    # Click initial Sign In
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='login-logout-button1']"))).click()

    # Enter credentials
    wait.until(EC.visibility_of_element_located((By.NAME, "Email"))).send_keys("Sacstatecpr@outlook.com")
    driver.find_element(By.NAME, "Password").send_keys("ssCPR123*")
    driver.find_element(By.ID, "btnSignIn").click()

    print("Login submitted...")

    # --- 3. CLICK USER PROFILE ---
    user_btn = wait.until(EC.element_to_be_clickable((By.ID, "Sac")))
    user_btn.click()

    # --- 4. HOVER AND NAVIGATE ---
    classes_button = wait.until(EC.visibility_of_element_located((By.ID, "Classes")))
    actions = ActionChains(driver)
    actions.move_to_element(classes_button).perform()

    sub_menu_item = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Training Site Classes')]")))
    driver.execute_script("arguments[0].click();", sub_menu_item)

    # --- 5. SELECT ORGANIZATION ---
    org_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@aria-label='Organization']")))
    org_input.click()
    org_input.send_keys("Sac State")
    time.sleep(1.5)
    org_input.send_keys(Keys.ENTER)

    # --- 6. SELECT INSTRUCTOR ---
    time.sleep(2)
    instructor_container = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(normalize-space(),'Instructor')]/ancestor::div[1]")))
    arrow_icon = instructor_container.find_element(By.XPATH, ".//i[contains(@class,'aha-icon-down-arrow-thin')]")
    driver.execute_script("arguments[0].click();", arrow_icon)
    
    option = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='26027755195 / Sac State']")))
    driver.execute_script("arguments[0].click();", option)

    # --- 7. DATE RANGE SELECTION ---
    print("Opening Calendar...")

    # CLICK ON THE DATE RANGE BOX
    date_range_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Choose a Date Range']")))
    date_range_box.click()

    # Target March 11th specifically based on the HTML you provided
    march_11_xpath = "//div[contains(@aria-label, 'March 11th, 2026')]"
    
    # Wait for the day to be visible
    day_11 = wait.until(EC.visibility_of_element_located((By.XPATH, march_11_xpath)))

    print("Selecting March 11...")
    # Click for Start Date
    driver.execute_script("arguments[0].click();", day_11)
    
    # Short wait for the React transition to "End Date" mode
    time.sleep(0.7)
    
    # Click again for End Date (using the same element)
    try:
        driver.execute_script("arguments[0].click();", day_11)
        print("March 11 confirmed as Start and End date.")
    except:
        # If the element refreshed and became 'stale', find it again and click
        day_11_retry = driver.find_element(By.XPATH, march_11_xpath)
        driver.execute_script("arguments[0].click();", day_11_retry)

    print("Selection complete.")
    time.sleep(5)

except Exception as e:
    print(f"Error occurred: {e}")
