#!/usr/bin/python

#import
import ionicsdk
import sys
import random
import os.path
import time

#variables
responses = ["Not so sure", "42", "Most likely", "Absolutely not", "Outlook is good",
"I see good things happening", "Never", "Negative", "Could be", "Unclear, ask again",
"Yes", "No", "Possible, but not probable", "Ask Ken"]

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
        read_file = open("8ball_log.txt", "r")
    except IOError:
        read_file = open("8ball_log.txt", "w")
        read_file.close()
        read_file = open("8ball_log.txt", "r")

    userentry = input('Look deep inside and ask me your biggest question. \n')
    response = magic_answer()
    print(response)
    encrypted_text_in_file = read_file.read()

    try:
        text_in_file = cipher.decryptstr(encrypted_text_in_file)
    except ionicsdk.exceptions.IonicException as e:
        print("Error encrypting: {0}".format(e.message))
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

    write_file = open("8ball_log.txt", "w")
    write_file.write(ciphertext)
    write_file.close()

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

#Start
print("I am the all-seeing magic 8 ball.\nAsk me your most pressing questions and I shall provide an answer.\nDon't worry though, I'll keep your questions a secret\n")
magic_question()

keepPlaying = (input("Would you like to ask the Wise One another question? Y/N: "))
while keepPlaying.lower() == str("y"):
    magic_question()
    keepPlaying = (input("Would you like to ask the Wise One another question? Y/N: "))