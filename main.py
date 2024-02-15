import requests
from telebot import types
from requests.exceptions import Timeout, ConnectionError
import telebot
import subprocess
import os
import datetime


bot = telebot.TeleBot("6441202113:AAGRdz_hsC0cwyGwS_1QefU3mvpqeCn2CGA")
# Global variable to store the received document
received_message = None


# Define a dictionary to map file extensions to analysis tools
file_extensions = {
    '.py': 'bandit',  # Python files will be analyzed with Bandit
    '.php': 'phpcs', 
    '.c': 'cppcheck', 
    '.sh': 'shellcheck',# PHP files will be analyzed with PHP_CodeSniffer
    # Add more extensions and corresponding tools as needed
}

def run_analysis_tool(tool, file_name):
    try:
        if tool == 'bandit':
            analysis_output = subprocess.getoutput(f"bandit -r {file_name}")
            return analysis_output
        elif tool == 'phpcs':
            analysis_output = subprocess.getoutput(f"phpcs -n {file_name}")
            return analysis_output
        elif tool == 'cppcheck':
            analysis_output = subprocess.getoutput(f"cppcheck --enable=all --inconclusive  {file_name}")
            return analysis_output
        elif tool == 'shellcheck':
            analysis_output = subprocess.getoutput(f"shellcheck {file_name}")
            return analysis_output    
        # Add more tools and their execution commands as needed
        else:
            return f"Unsupported analysis tool: {tool}"
    except Exception as e:
        return f"An error occurred during code analysis:\n{str(e)}"

def download_file_and_scan():
    global received_message
    try:
        if received_message is not None:
            file_info = bot.get_file(received_message.document.file_id)
            file_path = file_info.file_path
            downloaded_file = bot.download_file(file_path)
            file_extension = os.path.splitext(received_message.document.file_name)[-1].lower()

            with open(received_message.document.file_name, 'wb') as file:
                file.write(downloaded_file)

            bot.send_message(received_message.chat.id, "Analyzing the file for vulnerabilities...")

            if file_extension in file_extensions:
                tool = file_extensions[file_extension]
                analysis_result = run_analysis_tool(tool, received_message.document.file_name)
                bot.send_message(received_message.chat.id, f"Analysis result:\n{analysis_result}")
            else:
                bot.send_message(received_message.chat.id, f"Unsupported file type: {file_extension}")
    except Exception as e:
        bot.reply_to(received_message, f"An error occurred: {str(e)}")

def get_file_info():
    global received_message
    file_name = received_message.document.file_name
    file_size = received_message.document.file_size
    creation_date = datetime.datetime.fromtimestamp(received_message.date).strftime('%Y-%m-%d %H:%M:%S')
    
    # Determine the programming language (you can add more extensions and languages)
    file_extension = os.path.splitext(file_name)[-1].lower()

    return f"File Name: {file_name}\nFile Size: {file_size} bytes\nProgramming Language: {file_extension}\nSent Time: {creation_date}"


@bot.message_handler(content_types=['document'])
def handle_document(message):
    global received_message 
    received_message = message
    keyboard = types.InlineKeyboardMarkup()
    about_button = types.InlineKeyboardButton(text="File Info", callback_data="info")
    scan_button = types.InlineKeyboardButton(text="Scan", callback_data="scan")
    keyboard.row(about_button, scan_button)
    bot.send_message(message.chat.id, f"What would you like me to do? :)",reply_markup=keyboard)
    
@bot.callback_query_handler(func=lambda call: call.data == "scan",)
def handle_scan_button_click(call):
    # Handle the "scan" button click
    download_file_and_scan()

    
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data:
        global received_message
        if call.data == "info":
            file_info = get_file_info()
            bot.send_message(call.message.chat.id, f"File Information:\n{file_info}")
        elif call.data == "author":
            author_info = "This bot was created by:\nKausal \nAravind \nMoulish."
            bot.send_message(call.message.chat.id, author_info, parse_mode="Markdown")
        elif call.data == "about":
            about_info = "CodeSheriff is your code scanning companion. With the power to analyze code files for vulnerabilities, it helps you ensure the security and quality of your code.\n It supports various programming languages and offers a quick and easy way to enhance the reliability of your code. Stay secure and code with confidence with CodeSheriff! "
            bot.send_message(call.message.chat.id, about_info, parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_name = message.from_user.first_name
    welcome_message = f"Hi {user_name}, Welcome!\nI am CodeSherrif, your code scanning companion."
    #bot.send_photo(message.chat.id, open('/home/ubuntu/CodeSheriff/wumpus welcome.png', 'rb'), caption="")
    sticker = '/home/ubuntu/CodeSheriff/discord-wumpus.gif'
    # Create inline buttons
    keyboard = telebot.types.InlineKeyboardMarkup()
    # Button for "about" with a small description
    about_button = telebot.types.InlineKeyboardButton(text="About", callback_data="about")
    # Button for "Author" with information about the author
    author_button = telebot.types.InlineKeyboardButton(text="Author", callback_data="author")
    keyboard.add(about_button, author_button)
    bot.send_message(message.chat.id, welcome_message, reply_markup=keyboard)

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
