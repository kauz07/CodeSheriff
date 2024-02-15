import requests
from telebot import types
from requests.exceptions import Timeout, ConnectionError
import telebot
import subprocess
import os
from collections import defaultdict

bot = telebot.TeleBot("6441202113:AAGRdz_hsC0cwyGwS_1QefU3mvpqeCn2CGA")

temp_file_info = {}



@bot.message_handler(content_types=['document'])
def handle_document(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        
        # Store file information in the global variable
        temp_file_info[message.from_user.id] = file_info
        
        # Ask the user what they would like to do
        markup = types.InlineKeyboardMarkup()
        about_button = types.InlineKeyboardButton(text="About", callback_data="about")
        scan_button = types.InlineKeyboardButton(text="Scan", callback_data="scan")
        markup.row(about_button, scan_button)

        bot.reply_to(message, "What would you like me to do?", reply_markup=markup)
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {str(e)}")

@bot.callback_query_handler(func=lambda call: call.data == "scan")
def scan_callback(call,message):
    try:
        user_id = call.from_user.id
        file_info = bot.get_file(message.document.file_id)
        
        if file_info:
            # Extract the file extension from the file_path
            file_path = file_info.file_path
            file_extension = os.path.splitext(file_info.file_name)[-1].lower()
            
            if file_extension in file_extensions:
                # Download the file first
                downloaded_file = bot.download_file(file_path)
                
                # Save the downloaded file with the original file name
                with open(file_info.file_name, 'wb') as file:
                    file.write(downloaded_file)
                
                # Analyze the downloaded file by passing file_info.file_name as a parameter
                tool = file_extensions[file_extension]
                analysis_result = run_analysis_tool(tool, file_info.file_name)
                bot.send_message(call.message.chat.id, f"Analysis result:\n{analysis_result}")
            else:
                bot.send_message(call.message.chat.id, f"Unsupported file type: {file_extension}")
        else:
            bot.send_message(call.message.chat.id, "No file information available.")
    except Exception as e:
        bot.send_message(call.message.chat.id, f"An error occurred: {str(e)}")

def download_file_and_scan(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        file_path = file_info.file_path
        downloaded_file = bot.download_file(file_path)
        file_extension = os.path.splitext(message.document.file_name)[-1].lower()

        with open(message.document.file_name, 'wb') as file:
            file.write(downloaded_file)

        bot.reply_to(message, "Analyzing the file for vulnerabilities...")

        if file_extension in file_extensions:
            tool = file_extensions[file_extension]
            analysis_result = run_analysis_tool(tool, message.document.file_name)
            bot.send_message(message.chat.id, f"Analysis result:\n{analysis_result}")
        else:
            bot.send_message(message.chat.id, f"Unsupported file type: {file_extension}")
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {str(e)}")

def run_analysis_tool(tool, file_name):
    try:
        if tool == 'py':
            analysis_output = subprocess.getoutput(f" -r {file_name}")
            return analysis_output
        elif tool == 'php':
            analysis_output = subprocess.getoutput(f" -n {file_name}")
            return analysis_output
        elif tool == 'cpp':
            analysis_output = subprocess.getoutput(f"  {file_name}")
            return analysis_output
        elif tool == 'bash':
            analysis_output = subprocess.getoutput(f" {file_name}")
            return analysis_output    
        else:
            return f"Unsupported "
    except Exception as e:
        return f"An error occurred during code analysis:\n{str(e)}"
 


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data:
        if call.data == "about":
            about_message = "I am CodeSherrif, your code scanning companion. I can help you scan code for vulnerabilities."
            bot.send_message(call.message.chat.id, about_message)
        elif call.data == "author":
            author_info = "This bot was created by:\nKausal \nAravind \nMoulush."
            bot.send_message(call.message.chat.id, author_info, parse_mode="Markdown")



bot.polling()


#import telebot
#import subprocess
#
#bot = telebot.TeleBot("6441202113:AAGRdz_hsC0cwyGwS_1QefU3mvpqeCn2CGA")
#
#@bot.message_handler(content_types=['document'])
#
#def handle_document(message):
#file_info = bot.get_file(message.document.file_id)
#	file_path = file_info.file_path
#	downloaded_file = bot.download_file(file_path)
#	
#	with open(message.document.file_name,"wb") as file:
#		file.write(downloaded_file)
#		
#	bot.reply_to(message,"Analysing the file for vulnerabilities.....")
#	analysis_output = subprocess.getoutput(f"bandit -r {message.document.file_name}}")
#	
#	bot.reply_to(message,f"Analysis result:\n{analysis_output}")
#	
#bot.polling()
