#!/usr/bin/python

#import
import ionicsdk
import sys
import random
import os.path
import time
import os

#variables
responses = ["Not so sure", "42", "Most likely", "Absolutely not", "Outlook is good",
"I see good things happening", "Never", "Negative", "Could be", "Unclear, ask again",
"Yes", "No", "Possible, but not probable", "Ask Ken"]

logFile = "8ball_log.txt"

#Functions
def magic_answer():
    print("Let me dig deep into the waters of life, and find your answer")
    time.sleep(2)
    print("Hmmm")
    time.sleep(2)
    answer = random.choice(responses)
    return answer

def magic_question():
    try:
        read_file = open(logFile, "r")
    except IOError:
        read_file = open(logFile, "w")
        read_file.close()
        read_file = open(logFile, "r")

    userentry = input('Look deep inside and ask me your biggest question. \n')
    if userentry.lower() == "history":
        history_printout(logFile)
    elif userentry.lower() == "delete":
        deleteHist(logFile)
    else:
        response = magic_answer()
        encrypted_text_in_file = read_file.read()
        print(response)
        try:
            text_in_file = cipher.decryptstr(encrypted_text_in_file)
        except ionicsdk.exceptions.IonicException as e:
            print("Error decrypting: {0}".format(e.message))
            sys.exit(-2)

        read_file.close()
        all_text = text_in_file + " \n" + "Q: " + userentry + " \nA: " + response + "\n"
#    print(all_text)
#encryption
        try:
            ciphertext = cipher.encryptstr(all_text)
        except ionicsdk.exceptions.IonicException as e:
            print("Error encrypting: {0}".format(e.message))
            sys.exit(-2)

        write_file = open(logFile, "w")
        write_file.write(ciphertext)
        write_file.close()

def history_printout(fname): #This will print out the decrypted history of questions and answers.
    hist_file = open(fname, "r")
    encrypted_hist = hist_file.read()
    try:
        hist_text = cipher.decryptstr(encrypted_hist)
    except ionicsdk.exceptions.IonicException as e:
        print("Error encrypting: {0}".format(e.message))
        sys.exit(-2)
    hist_file.close()
    print(hist_text)

def deleteHist(fname):
    areYouSure = input("Are you sure you wan't to delete your question history? (Y/N)")
    while areYouSure.lower() != "y" and areYouSure.lower() != "n":
        print("\nAlthough I already know what your response will be, you did not enter it correctly. Please enter a 'Y' or an 'N'. \n")
        areYouSure = input("Are you sure you wan't to delete your question history? (Y/N)")
    if areYouSure.lower() == "y":
        writeTitleFile = open(fname, "w")
        try:
            encrypted_title = cipher.encryptstr("Question History:\n \n")
        except ionicsdk.exceptions.IonicException as e:
            print("Error encrypting title: {0}".format(e.message))
            sys.exit(-2)
        writeTitleFile.write(encrypted_title)
        writeTitleFile.close()

def emptyFileCheck(fname):
    if os.path.isfile(fname):
        if os.stat(fname).st_size == 0:
            writeTitleFile = open(fname, "w")
            try:
                encrypted_title = cipher.encryptstr("Question History:\n \n")
            except ionicsdk.exceptions.IonicException as e:
                print("Error encrypting title: {0}".format(e.message))
                sys.exit(-2)
            writeTitleFile.write(encrypted_title)
            writeTitleFile.close()
    else:
        writeTitleFile = open(fname, "w")
        try:
            encrypted_title = cipher.encryptstr("Question History:\n \n")
        except ionicsdk.exceptions.IonicException as e:
            print("Error encrypting title: {0}".format(e.message))
            sys.exit(-2)
        writeTitleFile.write(encrypted_title)
        writeTitleFile.close()


#main
#Initialize the Ionic Agent (must be done before most Ionic operations).
try:
  agent = ionicsdk.Agent()
except ionicsdk.exceptions.IonicException as e:
  print("Error initializing agent: {0}".format(e.message))
  sys.exit(-3)

# Check if there are profiles.
if not agent.hasanyprofiles() or not agent.hasactiveprofile():
  if not agent.hasanyprofiles():
    print("There are no device profiles on this device.")
  if not agent.hasactiveprofile():
    print("There is not an active device profile selected on this device.")
  print("Register (and select an active profile) this device before continuing.")
  sys.exit(-1)

# Initialize a Chunk Cipher for doing string encryption
cipher = ionicsdk.ChunkCipherAuto(agent)

# Make sure log file exists
emptyFileCheck(logFile)

#Start
print("I am the all-seeing magic 8 ball.\nAsk me your most pressing questions and I shall provide an answer.\nDon't worry though, I'll keep your questions a secret\n")
print("To see you question history, type 'history'\n")
magic_question()

#keep playing loop
keepPlaying = input("Would you like to ask the Wise One another question? Y/N: ")
while (keepPlaying.lower() != "y" and keepPlaying.lower() != "n"):
    print("\nAlthough I already know what your response will be, you did not enter it correctly. Please enter a 'Y' or an 'N'. \n")
    keepPlaying = input("Would you like to ask the Wise One another question? Y/N: ")

while keepPlaying.lower() == str("y"):
    magic_question()
    keepPlaying = (input("Would you like to ask the Wise One another question? Y/N: "))
    while keepPlaying.lower() != str("y") and keepPlaying.lower() != ("n"):
        print("\nAlthough I already know what your response will be, you did not enter it correctly. Please enter a 'Y' or an 'N'. \n")
        keepPlaying = (input("Would you like to ask the Wise One another question? Y/N: "))
print ("\nThanks for playing. Goodbye.")