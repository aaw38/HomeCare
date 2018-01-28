import RPi.GPIO as GPIO, time

import logging
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
from subprocess import call

GPIO.setmode(GPIO.BCM)

app = Flask(__name__)
ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

def RCtime (PiPin):
	measurement = 0
	# Discharge capacitor
	GPIO.setup(PiPin, GPIO.OUT)
	GPIO.output(PiPin, GPIO.LOW)
	time.sleep(0.1)

	GPIO.setup(PiPin, GPIO.IN)
	# Count loops until voltage across
	# capacitor reads high on GPIO
	while (GPIO.input(PiPin) == GPIO.LOW):
		measurement += 1
		if (measurement > 10000):
			return False
	return True

@ask.launch

def start():
    print "start"
    return statement("Welcome");

@ask.intent("CheckAwakeIntent")

def check_awake():

    print "check awake"

    #check here whether the input pin is 1/0 for now use rand 
    inbed =  RCtime(17)

    if inbed == False:
	yes = render_template("yes_awake")
        return statement(yes)
    else:
        no = render_template("no_asleep")
        return question(no)

@ask.intent("CheckAsleepIntent")

def check_asleep():

    #check here whether the input pin is 1/0 for now use rand 
    inbed = RCtime(17)

    if inbed == True:
        yes = render_template("yes_asleep")
        return question(yes)
    else:
        no = render_template("no_awake")
        return statement(no)

@ask.intent("YesIntent")

def soundalarm():
    print "soundalarm"

    call(["aplay", "./alarm.wav"])
    sound = render_template("alarm_sounded")
    return statement(sound);

@ask.intent("NoIntent")

def noalarm():
    print "no alarm"
    sleep = render_template("sleep_on")
    return statement(sleep);

if __name__ == '__main__':

    app.run(debug=True)
