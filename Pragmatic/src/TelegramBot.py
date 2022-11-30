import telebot
from time import sleep
from datetime import datetime
import json

class TelegramBot:
    
    @staticmethod
    def send_signal(self, quantidade, roleta, mensagem, link, site):
        bot = telebot.TeleBot('5792672199:AAF5L70wljq46P9Rthm2g_k_m5_fH4os_eM')                 
        bot.send_message('-1001612195936' , f"⚠️{int(quantidade)} repetições {mensagem}\n➖➖➖➖➖➖➖➖\n🎰{roleta} - {site}\n➖➖➖➖➖➖➖➖\n{link}")

