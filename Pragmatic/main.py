from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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
        self.driver.get('https://www.smashup.com/')
        with open('config.json') as configFile:
            self.config = json.load(configFile)
        sleep(3)

    def data_load(self):
        self.array_history = []
        self.old_array_history = []
        self.last_results = []
    
    def login(self):
        if len(self.driver.find_elements(By.CSS_SELECTOR, '.logout__btn')) < 1:
            while len(self.driver.find_elements(By.CSS_SELECTOR, 'a.login-tab')) < 1:
                sleep(1)
            self.driver.find_element(By.CSS_SELECTOR, 'a.login-tab').click()
            for i in range(0, 30) : self.driver.find_elements(By.CSS_SELECTOR, '.input-group input')[0].send_keys(Keys.BACKSPACE)
            self.driver.find_elements(By.CSS_SELECTOR, '.input-group input')[0].send_keys(self.config['login'])
            sleep(1)
            for i in range(0, 30) : self.driver.find_elements(By.CSS_SELECTOR, '.input-group input')[1].send_keys(Keys.BACKSPACE)
            self.driver.find_elements(By.CSS_SELECTOR, '.input-group input')[1].send_keys(self.config['password'])
            sleep(1)
            self.driver.find_elements(By.CSS_SELECTOR, '.input-group input')[1].send_keys(Keys.ENTER)     
            sleep( 10 )
            
        self.driver.get('https://www.smashup.com/?target=%2Flive-casino.html')
        self.driver.get('https://player.smashup.com/player_center/goto_common_game/5632/101?_ga=2.35116968.883245065.1669592766-138296240.1669592766')
        while len(self.driver.find_elements(By.CSS_SELECTOR, '.tabLiDv')) < 1:
            sleep(1)
        self.driver.find_elements(By.CSS_SELECTOR, '.tabLiDv')[1].click()
           
    def get_history_evolution(self):
        self.link = 'https://player.smashup.com/player_center/goto_common_game/5632/101?_ga=2.35116968.883245065.1669592766-138296240.1669592766'
        self.array_history = []
        sleep( 2 )
        self.driver.execute_script('window.scroll(0, 1000)')
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        roulettes = soup.select('.table-stats table, .table-stats ul')
        self.roulettes_title = [x.get_attribute('title') for x in self.driver.find_elements(By.CSS_SELECTOR, '.tableName')]  
        for i, roulette in enumerate(roulettes):
            last_numbers = roulette.select('li, tr td')
            history = []
            for number in last_numbers:
                if 'x' in number.text or 'X' in number.text :
                    x = number.text.split(' ')
                    if len(x) > 1 :
                        history.append(x[0])
                    else:
                        history.append(x[0].split('x')[1])
                    continue             
                history.append(number.text)
            self.array_history.append(history)
            
        if self.old_array_history == [] :
            self.old_array_history = self.array_history
            for i, history in enumerate(self.array_history):
                self.last_results.append(self.array_history[i])
    
    def compare_history(self):
        for i, history in enumerate(self.old_array_history):
            if history == self.array_history[i] : continue
            self.old_array_history[i] = self.array_history[i]
            self.last_results[i].insert(0, self.array_history[i][0])
            if len(self.last_results[i]) > 20 :
                self.last_results[i].pop()
            Validador.v_main(Validador, self.last_results[i], self.roulettes_title[i], self.link, 'Pragmatic')
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
            except Exception as err:
                print(str(err))
                self.driver.quit()
                sleep(1)
                continue            
        
Bot.main(Bot)
        
    