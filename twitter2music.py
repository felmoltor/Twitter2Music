#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lib.Musificator import Musificator
import time
import sys
import twitter
import RPi.GPIO as GPIO


# From https://en.wikipedia.org/wiki/Morse_code
# "... Each character (letter or numeral) is represented by a unique sequence of dots and dashes. 
# The duration of a dash is three times the duration of a dot. 
# Each dot or dash is followed by a short silence, equal to the dot duration. 
# The letters of a word are separated by a space equal to three dots (one dash), and the words 
# are separated by a space equal to seven dots. 
# The dot duration is the basic unit of time measurement in code transmission.[1] ...

POLLTIME = 180 
MUSICPIN = 12
LEDPIN = 10
    
# http://www.oomlout.com/oom.php/products/ardx/circ-06

def playTone(frecuency,seconds):
    i = 0.0
    while i < seconds:
        GPIO.output(MUSICPIN,GPIO.HIGH)
        GPIO.output(LEDPIN,GPIO.HIGH)
        time.sleep(1.0/frecuency)
        GPIO.output(MUSICPIN,GPIO.LOW)
        GPIO.output(LEDPIN,GPIO.LOW)
        time.sleep(1.0/frecuency)
        i += (1.0/frecuency) * 2

def toBuzzer(freqs,durations):
    GPIO.setmode(GPIO.BOARD) #numbering scheme that corresponds to breakout board and pin layout
    GPIO.setup(MUSICPIN,GPIO.OUT) #replace MUSICPIN with whatever pin you used, this sets up that pin as an output
    GPIO.setup(LEDPIN,GPIO.OUT) #replace MUSICPIN with whatever pin you used, this sets up that pin as an output
    count = 0
    while count < len(freqs):
        playTone(freqs[count],durations[count])
        time.sleep(0.05)
        count += 1            
        GPIO.output(MUSICPIN,GPIO.LOW)
        GPIO.output(LEDPIN,GPIO.LOW)
        
    GPIO.cleanup()

def main():
    
    # Each 30 seconds, request the last mention from your twitter account
    api = twitter.Api(
                consumer_key='<YOUR CONSUMER KEY HERE>',
                consumer_secret='<YOUR CONSUMER SECRET HERE>', 
		access_token_key='<YOUR ACCESS TOKEN HERE>', 
		access_token_secret='<YOUR ACCESS SECRET HERE>')
    
    # print api.VerifyCredentials()
    # status = api.PostUpdate('I love python-twitter!')
    
    m = Musificator()
    
    while True:
        try:
            mentions = api.GetMentions()
            
            maxmentionid = 0    
            freqs = durations = []    
            
            mf = open("lastmentionid.txt","r")
            lastmentionid = int(mf.readlines()[0])
            
            for mention in mentions:
                print "========"
                print "From %s (%s)" % (mention.user.screen_name,mention.user.name) 
                print "Geo: %s" % mention.geo
                print "Text: %s" % mention.text
                print "Tweet id: %s" % mention.id
                print "Tweet created at: %s" % mention.created_at
                
                if mention.id > lastmentionid:
                    tomusificate = mention.text.replace("@tw2morse","")
                    tomusificate = tomusificate.strip()
                    print "Musificating the message: %s" % tomusificate
                    (freqs,durations) = m.musificate(tomusificate)
                    print "Freqs: %s, Durations: %s " % (freqs,durations)
                    if len(freqs) > 0 and (len(freqs) == len(durations)):
                        toBuzzer(freqs,durations)
                    else:
                        print "Not musificating the mention. It has wrong characters."
                else:
                    print "Ignoring this mention. It was already explored"
                
                if maxmentionid < mention.id:
                    maxmentionid = mention.id
            
            mf.close()
            mf = open("lastmentionid.txt","w")
            mf.write(maxmentionid.__str__())
            mf.close()
            time.sleep(POLLTIME)
        except TwitterError as e:
            print "There was an error with Twitter: %s" % e
        
    
    # sys.stdout.write("Escribe mensaje> ")
    # msg = raw_input()
    # while len(msg) > 0:
    #     print "Deleting non aplphabet characters found in the message..."
    #     msg = replaceNonAlphabetChars(msg)
    #     print "Filtered message is: %s" % msg
    #     code = m.morsificate(msg)
    #     toBuzzer(code)
    #     # toInternalBeeper(code)
        
    #     # Request again the message to the user
    #     sys.stdout.write("Escribe mensaje> ")
    #     msg = raw_input()            
        

if __name__ == "__main__":
    main()
