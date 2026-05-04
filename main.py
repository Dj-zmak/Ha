import os
import time
import random
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class HoneygainBot:
    def __init__(self):
        self.driver = None
        self.base_url = "https://join.honeygain.com/ARAFA987D3"
        self.upload_api = "https://cloud-production-1ba6.up.railway.app/upload"
        
    def upload_file(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                files = {'file': (os.path.basename(file_path), f)}
                response = requests.post(self.upload_api, files=files, timeout=15)
                return response.json().get('url') if response.status_code == 200 else None
        except: return None
    
    def take_screenshot(self, name):
        try:
            filename = f"{name}_{int(time.time())}.png"
            self.driver.save_screenshot(filename)
            url = self.upload_file(filename)
            if os.path.exists(filename): os.remove(filename)
            print(f"📸 Screenshot: {url}")
        except: pass

    def setup_driver(self):
        try:
            options = Options()
            options.add_argument('--headless=new')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')
            options.add_argument('--incognito')
            
            # Railway standard chromium path
            options.binary_location = "/usr/bin/chromium" 
            
            self.driver = webdriver.Chrome(options=options)
            self.driver.delete_all_cookies()
            return True
        except Exception as e:
            print(f"Driver error: {e}")
            return False

    def fill_input_field(self, field, value):
        try:
            field.clear()
            field.send_keys(value)
            self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', {bubbles: true}));", field)
            return True
        except: return False

    def run_signup(self):
        if not self.setup_driver(): return False
        try:
            self.driver.get(self.base_url)
            time.sleep(5)
            
            # Accept cookies JS
            self.driver.execute_script("var btns=document.querySelectorAll('button');for(var i=0;i<btns.length;i++){if(btns[i].innerText.toLowerCase().includes('accept')){btns[i].click();break;}}")
            
            wait = WebDriverWait(self.driver, 15)
            
            # Accept Invite
            try:
                btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept invite')]")))
                self.driver.execute_script("arguments[0].click();", btn)
            except:
                self.driver.execute_script("var btns=document.querySelectorAll('button, a');for(var i=0;i<btns.length;i++){var t=btns[i].innerText.toLowerCase();if(t.includes('accept')&&t.includes('invite')){btns[i].click();}}")
            
            time.sleep(3)
            
            # Email & Password
            email_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']")))
            email = f"arafat{random.randint(100000, 999999)}@gmail.com"
            self.fill_input_field(email_field, email)
            
            pwd_field = self.driver.find_element(By.CSS_SELECTOR, "input[type='password']")
            password = f"Arafat{random.randint(100, 999)}"
            self.fill_input_field(pwd_field, password)
            
            time.sleep(2)
            
            # Submit
            submitted = False
            for selector in ["//button[normalize-space()='Continue with email']", "//button[contains(text(), 'Continue')]", "button[type='submit']"]:
                try:
                    target = self.driver.find_element(By.XPATH, selector) if "//" in selector else self.driver.find_element(By.CSS_SELECTOR, selector)
                    self.driver.execute_script("arguments[0].click();", target)
                    submitted = True
                    break
                except: continue
            
            if submitted:
                time.sleep(5)
                print(f"✅ Success: {email}")
                return True
            return False
        finally:
            if self.driver: self.driver.quit()

if __name__ == "__main__":
    bot = HoneygainBot()
    while True:
        bot.run_signup()
        wait = random.randint(30, 60)
        print(f"Waiting {wait}s for next account...")
        time.sleep(wait)
