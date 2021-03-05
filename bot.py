import telebot
import whois
import socket
import ssl
from datetime import date
TOKEN = '1692301833:AAGf7IKnhoXMNwd_4jyykQFfSQ13opPL1AM'
bot = telebot.TeleBot(TOKEN, parse_mode=None)


@bot.message_handler(func=lambda m: True)
def echo_all(message):

    hostname = message.text
    mes_text = ''

    domain = whois.whois(hostname)
    try:
        start = str(domain.creation_date[0]).split()[0]
        end = str(domain.expiration_date[0]).split()[0]
        creation_date = date(int(start.split('-')[0]), int(start.split('-')[1]), int(start.split('-')[2]))
        expiration_date = date(int(end.split('-')[0]), int(end.split('-')[1]), int(end.split('-')[2]))

        mes_text += f'creation_date - {start} \n'
        mes_text += f'expiration_date - {end} \n'
        mes_text += f'days_left - {str(expiration_date - creation_date).split()[0]} \n'

        try:
            context = ssl.create_default_context()
            with socket.create_connection((hostname, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    mes_text += f'ssl_status - Yes \n'
                    mes_text += f'ssl_notBefore - {ssock.getpeercert()["notBefore"]} \n'
                    mes_text += f'ssl_notAfter - {ssock.getpeercert()["notAfter"]} \n'
        except:
            mes_text += f'ssl_status - No \n'
    except:
        mes_text += 'something wrong'

    bot.reply_to(message, mes_text)


bot.polling()
