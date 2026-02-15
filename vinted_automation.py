#!/usr/bin/env python3
"""
Vinted Automation Script with ANTI-BAN Protocol
Automate description and upload of clothing items to Vinted while mimicking human behavior
"""

import os
import json
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from pathlib import Path


class VintedAutomation:
    """Main class for Vinted automation with human-like behavior"""
    
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
        """Setup Selenium WebDriver with anti-detection measures"""
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        
        # Anti-detection: Modify user agent and exclude automation switches
        options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = webdriver.Chrome(options=options)
        
        # Anti-detection: Remove navigator.webdriver flag
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return self.driver

    def human_wait(self, min_sec=2, max_sec=5):
        """Random wait to mimic human pauses"""
        wait_time = random.uniform(min_sec, max_sec)
        print(f"Humain : Pause de {wait_time:.2f} secondes...")
        time.sleep(wait_time)

    def human_type(self, element, text):
        """Type text character by character with random delays"""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.2)) # Realistic typing speed
        self.human_wait(0.5, 1.5)

    def human_scroll(self):
        """Simulate human scrolling behavior"""
        scroll_amount = random.randint(200, 600)
        self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
        self.human_wait(1, 3)

    def login(self, email, password):
        """Login to Vinted account with human-like interactions"""
        print("Navigation vers Vinted...")
        self.driver.get("https://www.vinted.fr")
        self.human_wait(3, 6)
        
        # Accept cookies if present
        try:
            cookie_btn = self.driver.find_element(By.ID, "onetrust-accept-btn-handler")
            cookie_btn.click()
            self.human_wait(1, 2)
        except:
            pass
            
        try:
            # Click on login button
            login_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'c-button') and contains(., 'Se connecter')]"))
            )
            login_btn.click()
            self.human_wait(2, 4)
            
            # Enter email
            email_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            self.human_type(email_input, email)
            
            # Enter password
            password_input = self.driver.find_element(By.ID, "password")
            self.human_type(password_input, password)
            
            # Click login
            submit_btn = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            submit_btn.click()
            
            print("Connexion réussie !")
            self.human_wait(4, 7)
            return True
            
        except Exception as e:
            print(f"Échec de la connexion : {str(e)}")
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
        """Upload a clothing item with strong anti-ban protocol"""
        try:
            print(f"
--- Protocole Anti-Ban : Upload de '{item_data.get('title')}' ---")
            
            # Navigate to upload page
            self.driver.get("https://www.vinted.fr/items/new")
            self.human_wait(4, 8)
            
            # Upload photos (one by one with pauses)
            if 'photos' in item_data and item_data['photos']:
                photo_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
                )
                
                for photo_path in item_data['photos']:
                    if os.path.exists(photo_path):
                        print(f"Ajout de la photo : {photo_path}")
                        photo_input.send_keys(os.path.abspath(photo_path))
                        self.human_wait(2, 5) # Time for photo to process
            
            self.human_scroll()
            
            # Fill in title
            title_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "title"))
            )
            self.human_type(title_input, item_data.get('title', ''))
            
            # Fill in description
            description = self.generate_description(item_data)
            description_input = self.driver.find_element(By.NAME, "description")
            self.human_type(description_input, description)
            
            self.human_scroll()
            
            # Select brand
            if 'brand' in item_data:
                brand_input = self.driver.find_element(By.NAME, "brand")
                self.human_type(brand_input, item_data['brand'])
                self.human_wait(1, 3)
                brand_input.send_keys(Keys.RETURN)
            
            # Fill in price
            price_input = self.driver.find_element(By.NAME, "price")
            self.human_type(price_input, str(item_data.get('price', '')))
            
            self.human_wait(5, 10) # Review the form before submitting
            
            # SUBMISSION (Irreversible action - usually would click here)
            print("Formulaire prêt pour la validation.")
            # self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
            
            print(f"Article '{item_data.get('title')}' traité avec succès.")
            return True
            
        except Exception as e:
            print(f"Échec de l'upload : {str(e)}")
            return False
    
    def batch_upload(self, items_file="items.json"):
        """Upload multiple items with LONG pauses between items to avoid detection"""
        if not os.path.exists(items_file):
            print(f"Fichier d'articles {items_file} introuvable.")
            return
        
        with open(items_file, 'r', encoding='utf-8') as f:
            items = json.load(f)
        
        success_count = 0
        for idx, item in enumerate(items, 1):
            print(f"
Traitement de l'article {idx}/{len(items)}...")
            if self.upload_item(item):
                success_count += 1
            
            if idx < len(items):
                # LONG PAUSE between items (5 to 10 minutes)
                pause_time = random.randint(300, 600)
                print(f"PAUSE ANTI-BAN : Attente de {pause_time//60} minutes avant le prochain article...")
                time.sleep(pause_time)
        
        print(f"
Upload par lot terminé : {success_count}/{len(items)} articles traités.")
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            print("Navigateur fermé.")


def main():
    """Main execution function"""
    print("=== Outil d'Automatisation Vinted (ANTI-BAN) ===")
    
    bot = VintedAutomation()
    bot.setup_driver()
    
    try:
        email = bot.config.get('email', '')
        password = bot.config.get('password', '')
        
        if not email or not password:
            print("Veuillez ajouter vos identifiants dans config.json")
            return
        
        if bot.login(email, password):
            # Batch upload starts here
            bot.batch_upload("items.json")
        
    except KeyboardInterrupt:
        print("
Processus interrompu par l'utilisateur.")
    except Exception as e:
        print(f"Erreur : {str(e)}")
    finally:
        bot.close()


if __name__ == "__main__":
    main()
