from src.TelegramBot import TelegramBot
import json 

class Validador:
    def v_grupo(historico, roleta, link, quantidade, pares, mensagem, site):
        grupo = 0
        for number in historico[::-1]:
            if int(number) in pares:
                grupo+=1
            else:
                grupo = 0
        if grupo > (quantidade-1) :
            if roleta == 'Double Ball Roulette' : return 0
            TelegramBot.send_signal(TelegramBot, grupo, roleta, mensagem, link, site)
        
    def v_main(self, historico, roleta, link, site):
        with open('config.json', encoding='utf8') as configFile:
            sequencias = (json.load(configFile))['sequencias']
            configFile.close()
        self.v_grupo(historico, roleta, link, sequencias['pares'], [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36], 'nos pares', site)
        self.v_grupo(historico, roleta, link, sequencias['impares'], [0, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35], 'nos impares', site)
        self.v_grupo(historico, roleta, link, sequencias['1 a 18'], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18], 'de 1 a 18', site)
        self.v_grupo(historico, roleta, link, sequencias['19 a 36'], [0, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36], 'de 19 a 36', site)
        self.v_grupo(historico, roleta, link, sequencias['vermelhos'], [0, 1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36], 'nos vermelhos', site)
        self.v_grupo(historico, roleta, link, sequencias["pretos"], [0, 2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35], 'nos pretos', site)
        self.v_grupo(historico, roleta, link, sequencias["primeira dúzia"], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 'na primeira dúzia', site)
        self.v_grupo(historico, roleta, link, sequencias["segunda dúzia"], [0, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24], 'na segunda dúzia', site)
        self.v_grupo(historico, roleta, link, sequencias["terceira dúzia"], [0, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36], 'na terceira dúzia', site)
        self.v_grupo(historico, roleta, link, sequencias["primeira fileira"], [0, 1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34], 'na primeira fileira', site)
        self.v_grupo(historico, roleta, link, sequencias["segunda fileira"], [0, 2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35], 'na segunda fileira', site)
        self.v_grupo(historico, roleta, link, sequencias["terceira fileira"], [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36], 'na terceira fileira', site)
            
                    
            