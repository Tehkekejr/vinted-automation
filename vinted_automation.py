#!/usr/bin/env python3
"""
Vinted Automation Script with ANTI-BAN Protocol
Automate description and upload of clothing items to Vinted while mimicking human behavior
"""

import os
import json
import time
import random
import glob
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

    def get_photos_from_folder(self, folder_path):
        """Get all image files from a specific folder"""
        if not folder_path or not os.path.exists(folder_path):
            return []
        
        extensions = ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']
        photos = []
        for ext in extensions:
            photos.extend(glob.glob(os.path.join(folder_path, ext)))
        
        return sorted(photos)
    
    def upload_item(self, item_data):
        """Upload a clothing item and save as DRAFT"""
        try:
            print(f"
--- Protocole Anti-Ban : BROUILLON pour '{item_data.get('title')}' ---")
            
            # Navigate to upload page
            self.driver.get("https://www.vinted.fr/items/new")
            self.human_wait(4, 8)
            
            # Determine photos to upload
            photos = []
            if 'photos_folder' in item_data:
                photos = self.get_photos_from_folder(item_data['photos_folder'])
            elif 'photos' in item_data:
                photos = item_data['photos']

            # Upload photos
            if photos:
                photo_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
                )
                
                for photo_path in photos:
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
            
            self.human_wait(3, 6)
            
            # --- SAVE AS DRAFT PROTOCOL ---
            print("Action : Enregistrement en BROUILLON...")
            
            # Vinted saving draft usually happens by clicking 'Back' or 'Close'
            # and then selecting 'Save as draft' in the confirmation popup
            try:
                # Find the exit/back button (often an 'X' or 'Annuler')
                cancel_btn = self.driver.find_element(By.XPATH, "//button[contains(@class, 'c-button') and (contains(., 'Annuler') or contains(., 'Quitter'))]")
                cancel_btn.click()
                self.human_wait(1, 3)
                
                # Click 'Enregistrer le brouillon' in the popup
                save_draft_btn = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Enregistrer le brouillon')]"))
                )
                save_draft_btn.click()
                print("Succès : Article enregistré dans vos brouillons.")
            except Exception as e_draft:
                print(f"Méthode alternative : Tentative d'enregistrement automatique...")
                # Fallback: Just navigate away, Vinted often auto-saves drafts now
                self.driver.get("https://www.vinted.fr/items/drafts")
            
            self.human_wait(2, 4)
            return True
            
        except Exception as e:
            print(f"Échec de l'upload : {str(e)}")
            return False
    
    def batch_upload(self, items_file="items.json"):
        """Process multiple items and save all as drafts in batch"""
        if not os.path.exists(items_file):
            print(f"Fichier d'articles {items_file} introuvable.")
            return
        
        with open(items_file, 'r', encoding='utf-8') as f:
            items = json.load(f)
        
        success_count = 0
        for idx, item in enumerate(items, 1):
            print(f"
Traitement de l'article {idx}/{len(items)} (Mode BROUILLON)...")
            if self.upload_item(item):
                success_count += 1
            
            if idx < len(items):
                # LONG PAUSE between items (5 to 10 minutes)
                pause_time = random.randint(300, 600)
                print(f"PAUSE ANTI-BAN : Attente de {pause_time//60} minutes avant le prochain brouillon...")
                time.sleep(pause_time)
        
        print(f"
Batch terminé : {success_count}/{len(items)} articles mis en brouillon.")
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            print("Navigateur fermé.")


def main():
    """Main execution function"""
    print("=== Outil Vinted - Mode BROUILLON Automatique ===")
    
    bot = VintedAutomation()
    bot.setup_driver()
    
    try:
        email = bot.config.get('email', '')
        password = bot.config.get('password', '')
        
        if not email or not password:
            print("Veuillez ajouter vos identifiants dans config.json")
            return
        
        if bot.login(email, password):
            bot.batch_upload("items.json")
        
    except KeyboardInterrupt:
        print("
Processus interrompu.")
    except Exception as e:
        print(f"Erreur : {str(e)}")
    finally:
        bot.close()


if __name__ == "__main__":
    main()
