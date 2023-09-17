import time
import os
import telebot
import aspose.pdf as ap
from fpdf import FPDF
bot = telebot.TeleBot('6520930244:AAGlB84F8JzrBV_Fx4TrPa_IDGWLqmTZn9I')
photo_list = []

def add_images(images, path):
    pdf = FPDF()
    for p in images:
        pdf.add_page()
        pdf.image(p, x=30, y=0, w=140)

    pdf.output(path)




@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, 'ку')

@bot.message_handler(commands=['bogdan'])
def maind(message):
    bot.send_message(message.chat.id, 'BOGDAN ALERT!!')
# @bot.message_handler(content_types=['photo'])
# def get_user_pics(message):
#     if message.photo[-1].file_id not in photo_list:
#         photo_list.append(message.photo[-1].file_id)
#         if len(photo_list) == 1:
#             send = bot.send_message(message.from_user.id, "Photos received...")
#             print(photo_list)



@bot.message_handler(content_types=['document']) # list relevant content types
def addfile(message):
    file_name = message.document.file_name
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open('photos/'+file_name, 'wb') as new_file:
        new_file.write(downloaded_file)
    photo_list.append('photos/'+file_name)
    bot.send_message(message.chat.id, f'{len(photo_list)} | {file_name} загружен | Размер: {round(file_info.file_size / 1024)} КБ')

@bot.message_handler(commands=['z'])
def createPdf(message):
    if photo_list:
        title = message.text.replace('/z ', '').replace('/z','')
        if title == '':
            title = 'Untitled'
        path = 'pdfs/'+title+'.pdf'
        add_images(photo_list, path)
        bot.send_document(message.chat.id, open(path, 'rb'))
        photo_list.clear()
        imgDir = 'photos'
        for f in os.listdir(imgDir):
            os.remove(os.path.join(imgDir, f))
        pdfDir = 'pdfs'
        for f in os.listdir(pdfDir):
            os.remove(os.path.join(pdfDir, f))
    else:
        bot.send_message(message.chat.id, 'Сначала загрузи фото')


bot.polling(none_stop=True)




