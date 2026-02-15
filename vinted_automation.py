#!/usr/bin/env python3
import os
import json
import time
import random
import glob
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class VintedBot:
    def __init__(self, config_path="config.json"):
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {}
        self.driver = None

    def start(self):
        print("Démarrage du navigateur sécurisé...")
        options = uc.ChromeOptions()
        self.driver = uc.Chrome(options=options)
        self.driver.set_window_size(1280, 800)

    def wait(self, a=2, b=5):
        time.sleep(random.uniform(a, b))

    def type_human(self, element, text):
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.12))
        self.wait(1, 2)

    def login(self):
        print("Navigation vers Vinted...")
        self.driver.get("https://www.vinted.fr")
        
        print("
" + "="*40)
        print("ACTION REQUISE : CONNEXION MANUELLE")
        print("1. Dans la fenêtre Chrome, connectez-vous à votre compte.")
        print("2. Une fois connecté et sur la page d'accueil, revenez ici.")
        print("="*40 + "
")
        
        input(">>> Appuyez sur ENTREE pour continuer le script...")
        self.wait(2, 4)
        return True

    def upload_as_draft(self, item):
        print(f"
--- Préparation de l'article : {item.get('title')} ---")
        try:
            self.driver.get("https://www.vinted.fr/items/new")
            self.wait(5, 8)

            # Photos
            photos = item.get('photos', [])
            if 'photos_folder' in item and os.path.exists(item['photos_folder']):
                photos = glob.glob(os.path.join(item['photos_folder'], "*"))
            
            if photos:
                print(f"Ajout de {len(photos[:5])} photos...")
                file_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
                )
                for p in photos[:5]:
                    file_input.send_keys(os.path.abspath(p))
                self.wait(3, 5)

            # Titre
            title_el = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "title"))
            )
            self.type_human(title_el, item.get('title', ''))
            
            # Description
            desc_el = self.driver.find_element(By.NAME, "description")
            description = f"{item.get('brand', '')} - {item.get('size', '')}
{item.get('description', 'Très bon état.')}"
            self.type_human(desc_el, description)

            # Prix
            price_el = self.driver.find_element(By.NAME, "price")
            self.type_human(price_el, str(item.get('price', '10')))
            
            self.wait(3, 5)

            # --- SAUVEGARDE EN BROUILLON ---
            print("Action : Enregistrement du brouillon...")
            try:
                # Tentative de clic sur le bouton fermer
                close_btn = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Quitter'], button[aria-label='Annuler']")
                close_btn.click()
                self.wait(2, 3)
                
                save_btn = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Enregistrer')]"))
                )
                save_btn.click()
                print("Succès : Article sauvegardé dans les brouillons.")
            except:
                print("Méthode de secours : Navigation forcée pour auto-save...")
                self.driver.get("https://www.vinted.fr/items/drafts")
                self.wait(4, 6)
            
            return True
        except Exception as e:
            print(f"Erreur lors de l'upload : {e}")
            return False

    def run(self):
        self.start()
        if self.login():
            items_file = "items.json"
            if os.path.exists(items_file):
                with open(items_file, "r", encoding='utf-8') as f:
                    items = json.load(f)
                
                for idx, item in enumerate(items, 1):
                    print(f"Traitement article {idx}/{len(items)}")
                    if self.upload_as_draft(item):
                        if idx < len(items):
                            wait_time = random.randint(120, 300)
                            print(f"Pause de {wait_time}s entre les articles...")
                            time.sleep(wait_time)
            else:
                print(f"Fichier {items_file} introuvable.")
            
            print("Travail terminé.")
            self.wait(5, 10)
            self.driver.quit()

if __name__ == '__main__':
    VintedBot().run()
