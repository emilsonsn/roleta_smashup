from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import subprocess
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from src.validador import Validador
from bs4 import BeautifulSoup
import os
import json

class Bot:

    def start(self):
        subprocess.Popen(
       '"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --log-level=3 --remote-debugging-port=9222', shell=True)
        sleep(1)
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        self.options.add_argument("--start-maximized")
        self.options.add_argument("disable-infobars")
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()) ,options=self.options)
        self.driver.maximize_window()
        self.temporizador = 0
        self.driver.get('https://www.smashup.com/iframe/auth/google_login')
        with open('config.json') as configFile:
            self.config = json.load(configFile)
        sleep(3)
    
    def data_load(self):
        self.array_history = []
        self.old_array_history = []
        self.last_results = []
        
    def login(self):
        if len(self.driver.find_elements(By.CSS_SELECTOR, '.logout__btn')) < 1:
            while len(self.driver.find_elements(By.CSS_SELECTOR, 'ul li')) < 1:
                sleep(1)
            self.driver.find_element(By.CSS_SELECTOR, 'ul li').click()
            sleep( 10 )
        self.driver.get('https://player.smashup.com/player_center/goto_common_game/5941/1000003')
        self.driver.get('https://ezugi.evo-games.com/frontend/evo/r2/#category=roulette')
           
    def get_history_evolution(self):
        self.link = 'https://player.smashup.com/player_center/goto_common_game/5941/1000000?_ga=2.70435859.2041366927.1669749356-161162237.1669588933'
        self.array_history = []
        sleep( 5 )
        self.driver.execute_script('window.scroll(0, 1000)')
        sleep( 2 )
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        roulettes = soup.select('li[data-role="grid-list-item"]')
        self.roulettes_title = [] 
        for roulette in roulettes:
            try:
                roulette_ = roulette.select('div[data-role="history-grid"]')[0]
                self.roulettes_title.append(roulette.select('p')[0].text)
            except:
                continue
            last_numbers = roulette_.select('text')
            history = []
            for number in last_numbers:
                if 'x' in number.text or 'X' in number.text : continue
                history.append(number.text)
            self.array_history.append(history)
            
        if self.old_array_history == [] :
            self.old_array_history = self.array_history
            for i, history in enumerate(self.array_history):
                self.last_results.append(self.array_history[i])
    
    def compare_history(self):
        for i, history in enumerate(self.old_array_history):
            try:
                if history == self.array_history[i] : continue
                self.old_array_history[i] = self.array_history[i]
                self.last_results[i].insert(0, self.array_history[i][0])
                if len(self.last_results[i]) > 20 :
                    self.last_results[i].pop()
                Validador.v_main(Validador, self.last_results[i], self.roulettes_title[i], self.link, 'Evolution')
            except Exception as err:
                print(err)
                continue
        sleep( 5 )
        
    def main(self):
        self.data_load(self)
        while True:
            try:
                self.start(self)
                self.login(self)
                while True:
                    self.get_history_evolution(self)
                    self.compare_history(self)
                    self.temporizador+=1
                    if self.temporizador >= 200:
                        self.driver.quit()
                        sleep(1)
                        break  
            except Exception as err:
                print(str(err))
                self.driver.quit()
                sleep(1)
                continue       
        
Bot.main(Bot)
        
    