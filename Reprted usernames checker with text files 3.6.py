from colorama import init, Fore
init(autoreset=True)
from colorama import init, Fore
init(autoreset=True)
import time
import os
from tkinter import Tk, Label, Entry, Button, filedialog, StringVar, IntVar
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from colorama import init, Fore, Back, Style
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from licensing.models import *
from licensing.methods import Key, Helpers
init(autoreset=True)
RSAPubKey = "<RSAKeyValue><Modulus>6e5kajLtB2HKJRoWoS/LJzpaUaiZza2oGK8KKmmMbBe2wLZWa19EypILzH6ig/IvPzgNVmEsOrYPVLRdBKOpfEpa6xuf3uHk9TcVDgLw7as2G7c8Oi2Fumk8VU3YIZsXavcK0rB4i0qayGV9ba+blu/wKgLgqsoHVXDAtAs4no9VdkRWmjQLt7uZ+bI2brNWamt3MnlHSyDsrp6jyVCs/3xqtc/j7QrQ07U9qdcB4CPT6s6gwCVQP48+Mq6VUFXEK6MOdlinA3zwM1G7bt8bV792+VYyVouApgSo/B8QW13aHYV2IBBPRxQcWfZdaDW+PpvSVukYovmJPADDQzi/Jw==</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>"
auth = "WyI5MjQwODIwNyIsIklrMUdPajNEZmhacFd1RzJYWFJGNlRMK3hTc3E2NTh0ZmZoTVV1eUEiXQ=="
temp_folder_path = "C:\\Windows\\Temp"
license_file_path = os.path.join(temp_folder_path, "license Twitter Bot.txt")

def create_temp_folder():
    if not os.path.exists(temp_folder_path):
        os.makedirs(temp_folder_path)
        print(Fore.YELLOW + "✨ Created a temporary folder. It's like a new home for our license! 🏠")

def read_or_prompt_license_key():
    create_temp_folder()
    try:
        with open(license_file_path, "r") as file:
            saved_license_key = file.read().strip()
            if saved_license_key:
                print(Fore.GREEN + "🔑 Found the saved license key! Time to party! 🎉")
                return saved_license_key
    except FileNotFoundError:
        print(Fore.RED + "❌ No saved license key found. It's like looking for a unicorn! 🦄")
    key = str(input(Fore.BLUE + "Enter Your License Key (No, it's not '1234'!): "))
    with open(license_file_path, "w") as file:
        file.write(key)
    print(Fore.CYAN + "📜 License key saved. Your secret is safe with me! 🤐")
    return key

def Authkey():
    key = read_or_prompt_license_key()
    result = Key.activate(token=auth,
                          rsa_pub_key=RSAPubKey,
                          product_id=27177,
                          key=key,
                          machine_code=Helpers.GetMachineCode())
    if result[0] is None or not Helpers.IsOnRightMachine(result[0]):
        print(Fore.RED + "💔 The license does not work: Maybe internet issue so try turning it off and on again? 🔄".format(result[1]))
        time.sleep(5)
        quit()
    else:
        print(Fore.GREEN + "✅ The license is valid! You're now officially awesome! 🌟")
        print()

Authkey()
# Initialize logging
print(Fore.MAGENTA + "📋 Initializing logging. Because if it's not logged, did it even happen? 🤔")

# Additional functionality for your bot can be added below
print(Fore.BLUE + "🔧 Bot setup complete. Ready to rock and roll! 🎸")
init(autoreset=True)
# Initialize colorama
init(autoreset=True)

# File paths for usernames
REPORTED_USERNAMES_FILE = "reported_usernames.txt"
SUSPENDED_USERNAMES_FILE = "suspended_usernames.txt"
RESTRICTED_USERNAMES_FILE = "restricted_usernames.txt"

# Load usernames from file
def load_usernames(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return [line.strip() for line in f if line.strip()]
    return []

# Save usernames to file
def save_username(file_path, username):
    with open(file_path, "a") as f:
        f.write(username + "\n")

# Remove processed username from the file
def remove_username(file_path, username):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            lines = f.readlines()
        with open(file_path, "w") as f:
            f.writelines(line for line in lines if line.strip() != username)

# Process each username and determine the appropriate action
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

def process_username(driver, username):
    short_wait = WebDriverWait(driver, 10)  # Short wait for the body
    long_wait = WebDriverWait(driver, 20)   # Longer wait for elements

    try:
        # Open the profile in a new tab
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])  # Switch to the new tab

        driver.get(f"https://x.com/{username}")
        print(Fore.YELLOW + f"Visiting: https://x.com/{username}")

        try:
            short_wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            print(Fore.GREEN + f"Body loaded for: {username}")
        except TimeoutException:
            print(Fore.RED + f"Timeout: Body did not load for {username}. Closing profile...")
            driver.close()  # Close the current tab
            driver.switch_to.window(driver.window_handles[0])  # Switch back to the main window
            return  # Move to the next profile

        # Wait for the specific XPath
        xpath_locator = '//*[@class="css-175oi2r r-f8sm7e r-13qz1uu r-1ye8kvj"]'
        element = long_wait.until(EC.presence_of_element_located((By.XPATH, xpath_locator)))
        text_content = element.text

        print(Fore.BLUE + f"Text found: {text_content}")

        if "Account suspended" in text_content:
            print(Fore.RED + f"Account suspended for {username}")
            save_username(SUSPENDED_USERNAMES_FILE, username)

        elif "Caution: This account is temporarily restricted" in text_content:
            print(Fore.YELLOW + f"Account temporarily restricted for {username}")
            save_username(RESTRICTED_USERNAMES_FILE, username)

        elif "followers" in text_content and "following" in text_content:
            print(Fore.GREEN + f"Account is active for {username}")
        else:
            print(Fore.MAGENTA + f"Unhandled case for {username}: {text_content}")

        # Remove the username from the reported list
        remove_username(REPORTED_USERNAMES_FILE, username)

    except Exception as e:
        print(Fore.RED + f"Error processing username {username}: {e}")
    finally:
        driver.close()  # Close the current tab
        driver.switch_to.window(driver.window_handles[0])  # Switch back to the main window
        print(Fore.BLUE + f"Finished processing {username}. Moving to the next profile...")


# Open the profile and process usernames
def open_profile_and_usernames(profile_path, profile_folder, service, options):
    options.add_argument("--user-data-dir=" + profile_path)
    driver = None
    try:
        driver = webdriver.Chrome(options=options, service=service)
        driver.get("https://x.com/")
        print(Fore.BLUE + f"Successfully opened profile: {profile_folder}")

        usernames = load_usernames(REPORTED_USERNAMES_FILE)
        print(Fore.GREEN + f"Total usernames fetched: {len(usernames)}")

        if not usernames:
            print(Fore.YELLOW + "No more usernames left to process.")
            return

        for username in usernames:
            process_username(driver, username)

    except Exception as e:
        print(Fore.RED + f"Error occurred with profile {profile_folder}: {e}")
    finally:
        if driver:
            driver.quit()

# Main function to start the profile opener
def start_opening_profiles():
    chrome_profile_path = folder_var.get()
    start_index = start_var.get()
    end_index = end_var.get()
    webdriver_path = r'C:\chromedriver.exe'
    chrome_binary_path = r'C:\chrome.exe'
    service = Service(webdriver_path)

    options = Options()
    options.binary_location = chrome_binary_path

    profile_folders = os.listdir(chrome_profile_path)
    total_profiles = len(profile_folders)
    print(Fore.BLUE + f"Total profiles found: {total_profiles}")

    end_index = min(end_index, total_profiles - 1)
    for index in range(start_index, end_index + 1):
        profile_folder = profile_folders[index]
        profile_path = os.path.join(chrome_profile_path, profile_folder)
        open_profile_and_usernames(profile_path, profile_folder, service, options)

    print(Fore.BLUE + "Finished opening all specified profiles.")

# GUI Configuration
root = Tk()
root.title("Reported Bot Confirmer")

folder_var = StringVar()
start_var = IntVar()
end_var = IntVar()

Label(root, text="Select Folder Containing Profiles:").grid(row=0, column=0, padx=10, pady=10)
Entry(root, textvariable=folder_var, state='readonly').grid(row=0, column=1, padx=10, pady=10)
Button(root, text="Browse", command=lambda: folder_var.set(filedialog.askdirectory(title="Select Folder Containing Profiles"))).grid(row=0, column=2, padx=10, pady=10)

Label(root, text="Start Index:").grid(row=1, column=0, padx=10, pady=10)
Entry(root, textvariable=start_var).grid(row=1, column=1, padx=10, pady=10)

Label(root, text="End Index:").grid(row=2, column=0, padx=10, pady=10)
Entry(root, textvariable=end_var).grid(row=2, column=1, padx=10, pady=10)

Button(root, text="Start Opening Profiles", command=start_opening_profiles).grid(row=4, column=0, columnspan=3, pady=20)

root.mainloop()