#!/usr/bin/env python3
"""
Vinted Automation Script
Automate description and upload of clothing items to Vinted
"""

import os
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from pathlib import Path


class VintedAutomation:
    """Main class for Vinted automation"""
    
    def __init__(self, config_file="config.json"):
        """Initialize the automation bot"""
        self.config = self.load_config(config_file)
        self.driver = None
        
    def load_config(self, config_file):
        """Load configuration from JSON file"""
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            print(f"Config file {config_file} not found. Using defaults.")
            return {}
    
    def setup_driver(self):
        """Setup Selenium WebDriver"""
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        # Uncomment to run headless
        # options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)
        return self.driver
    
    def login(self, email, password):
        """Login to Vinted account"""
        print("Navigating to Vinted...")
        self.driver.get("https://www.vinted.fr")
        time.sleep(2)
        
        try:
            # Click on login button
            login_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Se connecter')]"))
            )
            login_btn.click()
            time.sleep(1)
            
            # Enter email
            email_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            email_input.send_keys(email)
            
            # Enter password
            password_input = self.driver.find_element(By.ID, "password")
            password_input.send_keys(password)
            
            # Click login
            submit_btn = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            submit_btn.click()
            
            print("Login successful!")
            time.sleep(3)
            return True
            
        except Exception as e:
            print(f"Login failed: {str(e)}")
            return False
    
    def generate_description(self, item_data):
        """Generate item description from data"""
        template = """
{brand} - {type}

Taille: {size}
Couleur: {color}
État: {condition}

{description}

Prix: {price}€
"""
        return template.format(**item_data)
    
    def upload_item(self, item_data):
        """Upload a clothing item to Vinted"""
        try:
            print(f"Uploading item: {item_data.get('title', 'Unknown')}")
            
            # Navigate to upload page
            self.driver.get("https://www.vinted.fr/items/new")
            time.sleep(2)
            
            # Upload photos
            if 'photos' in item_data and item_data['photos']:
                photo_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
                )
                
                for photo_path in item_data['photos']:
                    if os.path.exists(photo_path):
                        photo_input.send_keys(os.path.abspath(photo_path))
                        time.sleep(1)
            
            # Fill in title
            title_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "title"))
            )
            title_input.send_keys(item_data.get('title', ''))
            
            # Fill in description
            description = self.generate_description(item_data)
            description_input = self.driver.find_element(By.NAME, "description")
            description_input.send_keys(description)
            
            # Fill in price
            price_input = self.driver.find_element(By.NAME, "price")
            price_input.send_keys(str(item_data.get('price', '')))
            
            # Select category (simplified - needs proper implementation)
            # This would require navigating through Vinted's category system
            
            # Select brand
            if 'brand' in item_data:
                brand_input = self.driver.find_element(By.NAME, "brand")
                brand_input.send_keys(item_data['brand'])
                time.sleep(1)
                brand_input.send_keys(Keys.RETURN)
            
            # Select size
            if 'size' in item_data:
                size_input = self.driver.find_element(By.NAME, "size")
                size_input.send_keys(item_data['size'])
            
            print(f"Item '{item_data.get('title')}' uploaded successfully!")
            return True
            
        except Exception as e:
            print(f"Upload failed: {str(e)}")
            return False
    
    def batch_upload(self, items_file="items.json"):
        """Upload multiple items from a JSON file"""
        if not os.path.exists(items_file):
            print(f"Items file {items_file} not found.")
            return
        
        with open(items_file, 'r', encoding='utf-8') as f:
            items = json.load(f)
        
        success_count = 0
        for idx, item in enumerate(items, 1):
            print(f"\nProcessing item {idx}/{len(items)}...")
            if self.upload_item(item):
                success_count += 1
            time.sleep(3)  # Wait between uploads
        
        print(f"\nBatch upload complete: {success_count}/{len(items)} items uploaded successfully.")
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            print("Browser closed.")


def main():
    """Main execution function"""
    print("=== Vinted Automation Tool ===")
    
    # Initialize automation
    bot = VintedAutomation()
    bot.setup_driver()
    
    try:
        # Login (credentials should be in config.json)
        email = bot.config.get('email', '')
        password = bot.config.get('password', '')
        
        if not email or not password:
            print("Please add your credentials to config.json")
            return
        
        if bot.login(email, password):
            # Upload items
            bot.batch_upload("items.json")
        
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        bot.close()


if __name__ == "__main__":
    main()
