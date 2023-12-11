from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver

driver = None
api_call_count = 0  # Track the number of API calls

@csrf_exempt
def dialpad_webhook(request):
    global driver  # Ensure you are using the global driver variable
    global api_call_count  # Track the number of API calls

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        # contact_number = '5108289999'
        # contact_number = '5107880048'
        # contact_number = '5108289549'
        contact_number = data['contact']['phone']
        if data['direction'] == 'outbound':
            contact_number = data['external_number']
        else:
            contact_number = data['internal_number']
        print('this is the number::', contact_number)

        if driver is None or not is_driver_active(driver):
            driver = webdriver.Chrome()
            driver.maximize_window()
            driver.get("https://bahousecleaning.maidcentral.com/Home/SalesDashboard")
            
            username_field = driver.find_element(By.ID, "Email")
            username_field.send_keys("tehseen_ullah786@hotmail.com")
            password_field = driver.find_element(By.ID, "Password")
            password_field.send_keys("Dialpad@123")
            password_field.send_keys(Keys.RETURN)
            save_webdriver_session(driver)  # Save session after successful setup
        else:
            driver = load_webdriver_session()

        api_call_count += 1

        # Open a new tab only if this is not the first API call
        if api_call_count > 1:
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[-1])

        # Perform the search in the new tab
        search_url = f"https://bahousecleaning.maidcentral.com/Customer/Search?id={contact_number}"
        driver.get(search_url)
        try:
            driver.find_element(By.XPATH, "//h2[text()='No results']")
            driver.get("https://bahousecleaning.maidcentral.com/Estimate/")   
        except:
            try:
                actions_button = WebDriverWait(driver, 1).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Actions')]"))
                )
                actions_button.click()
                WebDriverWait(driver, 1).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'note-modal-open')]"))
                ).click()
            except:
                pass

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'method not allowed'}, status=405)


def is_driver_active(driver):
    if driver is None:
        return False

    try:
        driver.current_url
        return True
    except WebDriverException:
        return False


def save_webdriver_session(driver):
    with open('webdriver_session.json', 'w') as file:
        session_info = {
            'session_id': driver.session_id,
            'executor_url': driver.command_executor._url
        }
        json.dump(session_info, file)



def load_webdriver_session():
    try:
        with open('webdriver_session.json', 'r') as file:
            session_info = json.load(file)
            return create_driver_session(session_info['session_id'], session_info['executor_url'])
    except (FileNotFoundError, WebDriverException, json.JSONDecodeError):
        # If any error occurs, return a new WebDriver instance
        return webdriver.Chrome()  # Or your preferred WebDriver

def create_driver_session(session_id, executor_url):
    original_execute = RemoteWebDriver.execute
    def new_command_execute(driver, command, params=None):
        if command == "newSession":
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return original_execute(driver, command, params)

    RemoteWebDriver.execute = new_command_execute
    driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
    RemoteWebDriver.execute = original_execute
    driver.session_id = session_id
    return driver







"""
@csrf_exempt
def dialpad_webhook(request):
    global driver

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        print(data)

        contact_number = '5107880048'

        print('this is the number::', contact_number)


        # Check if the driver is already initialized and active
        if driver is None or not is_driver_active(driver):
            driver = webdriver.Chrome()
            driver.maximize_window()
            driver.get("https://bahousecleaning.maidcentral.com/Home/SalesDashboard")
            username_field = driver.find_element(By.ID, "Email")
            username_field.send_keys("tehseen_ullah786@hotmail.com")
            password_field = driver.find_element(By.ID, "Password")
            password_field.send_keys("Dialpad@123")
            password_field.send_keys(Keys.RETURN)

        search_url = f"https://bahousecleaning.maidcentral.com/Customer/Search?id={contact_number}"
        driver.get(search_url)
        try:
            driver.find_element(By.XPATH, "//h2[text()='No results']")
            driver.get("https://bahousecleaning.maidcentral.com/Estimate/")   
        except:
            try:
                actions_button = WebDriverWait(driver, 1).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Actions')]"))
                )
                actions_button.click()
                WebDriverWait(driver, 1).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'note-modal-open')]"))
                ).click()
            except:
                pass
        # time.sleep(600)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'method not allowed'}, status=405)

"""