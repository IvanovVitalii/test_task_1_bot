import telebot
import whois
import socket
import ssl
from datetime import datetime
from settings import TOKEN


TOKEN = TOKEN
bot = telebot.TeleBot(TOKEN, parse_mode=None)


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    try:
        hostname = message.text
        mes_text = ''

        domain = whois.whois(hostname)

        now = datetime.now()

        if type(domain.expiration_date) is list:
            end = str(domain.expiration_date[0]).split()[0]
        else:
            end = str(domain.expiration_date).split()[0]

        expiration_date = datetime(int(end.split('-')[0]), int(end.split('-')[1]), int(end.split('-')[2]))

        mes_text += f'expiration_date - {end} \n'
        mes_text += f'days_left - {str(expiration_date - now).split()[0]} \n'

        try:
            context = ssl.create_default_context()
            with socket.create_connection((hostname, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:

                    sst_info_notAfter = ssock.getpeercert()["notAfter"].split()
                    m, d, y = sst_info_notAfter[0], sst_info_notAfter[1], sst_info_notAfter[3]
                    sst_date_input = f'{d}-{m}-{y}'
                    sst_date_notAfter = datetime.strptime(sst_date_input, '%d-%b-%Y')

                    mes_text += f'ssl_status - Yes \n'
                    mes_text += f'sst_days_left - {str(sst_date_notAfter - now).split()[0]} \n'

        except:
            mes_text += f'ssl_status - No \n'
    except:
            mes_text += f'something wrong \n'

    bot.reply_to(message, mes_text)


bot.polling()
