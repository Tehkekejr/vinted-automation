import os, json, time, random, glob
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class VintedBot:
    def __init__(self, config_path='config.json'):
        self.config = json.load(open(config_path)) if os.path.exists(config_path) else {}
        self.driver = None
    def start(self):
        self.driver = uc.Chrome()
        self.driver.set_window_size(1280, 800)
    def wait(self, a=2, b=5): time.sleep(random.uniform(a, b))
    def login(self):
        self.driver.get('https://www.vinted.fr')
        print('')
        print('='*40)
        print('ACTION REQUISE : CONNEXION MANUELLE')
        print('1. Connectez-vous dans Chrome')
        print('2. Revenez ici une fois sur accueil Vinted')
        print('='*40)
        print('')
        input('>>> Appuyez sur ENTREE pour continuer...')
        return True
    def upload_as_draft(self, item):
        try:
            self.driver.get('https://www.vinted.fr/items/new')
            self.wait(5, 8)
            photos = item.get('photos', [])
            if 'photos_folder' in item: photos = glob.glob(os.path.join(item['photos_folder'], '*'))
            if photos:
                file_input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
                for p in photos[:5]: file_input.send_keys(os.path.abspath(p))
                self.wait(3, 5)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, 'title'))).send_keys(item.get('title', ''))
            desc_val = item.get('brand', '') + ' - ' + item.get('size', '') + ' ' + item.get('description', 'Bon etat')
            self.driver.find_element(By.NAME, 'description').send_keys(desc_val)
            self.driver.find_element(By.NAME, 'price').send_keys(str(item.get('price', '10')))
            self.wait(3, 5)
            try:
                self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Quitter']").click()
                self.wait(1, 2)
                WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Enregistrer')]"))).click()
            except: self.driver.get('https://www.vinted.fr/items/drafts')
            return True
        except Exception as e:
            print('Erreur: ' + str(e))
            return False
    def run(self):
        self.start()
        if self.login():
            if os.path.exists('items.json'):
                items = json.load(open('items.json', encoding='utf-8'))
                for idx, item in enumerate(items, 1):
                    print('Article ' + str(idx) + '/' + str(len(items)))
                    if self.upload_as_draft(item) and idx < len(items): time.sleep(random.randint(60, 120))
        self.driver.quit()

if __name__ == '__main__': VintedBot().run()
