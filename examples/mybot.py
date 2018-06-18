#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telebot
from telebot import types
import time
import os
TOKEN = "TOKEN"             #Token obtained from @BotFather

userStep = {}               #Dictionary which contains users' ID and current menu number
knownUsers = []             #List of conected users

#Class color to print on the screen
class color:
    RED     =   '\033[91m'
    BLUE    =   '\033[94m'
    GREEN   =   '\033[32m'
    ENDC    =   '\033[0m'
    BOLD    =   '\033[1m'

#Function that checks if the user connected is new or not
def get_user_step(uid):
    if uid in userStep:             #If the user has entered before, it returns its ID
        return userStep[uid]
    else:                           #If the user has never entered before
        knownUsers.append(uid)      #Append ID to the list
        userStep[uid]=0             #Assign step number 0
        print(color.RED) + "NEW USER!!!" + color.ENDC

#The next step is to create the essential bot functions:
#   *Listener: receives the messages from the users
#   *Start
#   *Help


#LISTENER
def listener(messages):
    for m in messages:
        if m.content_type == 'text':     #Check if it is a text message
            #print the message received by the user
            print("["+str(m.chat.id)+"] " + str(m.chat.first_name)+": "+m.text)

bot = telebot.TeleBot(TOKEN)
bot.set_update_listener

#START
@bot.message_handler(commands=['start'])
def command_start(m):
    cid= m.chat.id                      #Obtains user ID
    userStep[cid] = 0                   #Assign step number 0 to the user

    #The bot sends a message
    bot.send_message(cid, "Wake up "+ str(m.chat.first_name)+ '...')
    time.sleep(1)                       #Wait for a second
    bot.send_message(cid, "Fwhibbit has you ...")
    time.sleep(1)
    bot.send_message(cid, "Follow the white rabbit ... \n", reply_markup=menu)

#Dictionary which contains bot commands
commands ={
    'start' : 'Start the bot',
    'help' : 'Show available commands',
    'exec' : 'Execute a command'
}

#HELP
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    #Creating a variable with help message
    help_text = "Available commands: \n"
    for key in commands:
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)        #Send help message

menu = types.ReplyKeyboardMarkup()
menu.add("RPinfo", "Camera")                #Menu buttons

@bot.message_handler(func=lambda message:get_user_step(message.chat.id)==0)
def main_menu(m):                           #Main menu function
    cid = m.chat.id
    text=m.text
    if text == "RPiInfo":                   #If user has pressed RPinfo button
        bot.send_message(cid, "Available info ", reply_markup=info_menu)
        userStep[cid] = 1                   #Changes button number
    else:                                   #If none of the previous ones, show help
        command_help(m)


#RPINFO MENU

info_menu = types.ReplyKeyboardMarkup()
info_menu.add("TEMP", "HD")
info_menu.add("RAM", "CPU")
info_menu.add("BACK")


#Files to open

cpu_temperature_file = ""
gpu_temperature_file = ""

@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 1)
def info_opt(m):
    cid = m.chat.id                         #User ID
    txt = m.text                            #Received message
    if txt == "TEMP":                       #Temperature
        bot.send_message(cid,"[+] TEMPERATURE")
        print(color.BLUE + "[+] TEMPERATURE" + color.ENDC)
        #Getting CPU temperature algorithm
        tempFile = open(cpu_temperature_file)
        cpu_temp = tempFile.read()
        tempFile.close()
        cpu_temp = round(float(cpu_temp) / 1000)
        bot.send_message(cid, "[1]  CPU: %s " %cpu_temp) #Send the message with the CPU temperature
        print(color.GREEN + "[1] CPU: %s" %cpu_temp + color.ENDC)
        #Getting GPU temperature
        gpu_temp = os.popen(gpu_temperature_file).read().split("=")[1][:3]
        bot.send_message(cid, "[i]   GPU: %s" %gpu_temp) #Send the message with the GPU temperature
        print(color.GREEN + "[1] GPU: %s" %gpu_temp + color.ENDC)
    elif txt == "HD":
        pass
    elif txt == "RAM":
        pass
    elif txt == "CPU":
        pass
    elif txt == "BACK":
        userStep[cid] = 0
        bot.send_message(cid, "Main menu", reply_markup=menu)
    else:
        command_help(m)