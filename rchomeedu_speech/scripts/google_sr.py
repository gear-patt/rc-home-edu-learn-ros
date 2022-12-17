#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from std_msgs.msg import String
import speech_recognition as sr
from gtts import gTTS
import os

def callback(data):
    rospy.loginfo("Input: %s", data.data)

    text = data.data
    tts = gTTS(text, lang='en')
    

    tts.save("speech.mp3")
    os.system("mpg321 speech.mp3")
    os.remove("speech.mp3")

def googlesr():
    rospy.init_node('googlesr', anonymous=True)
    rospy.Subscriber("result", String, callback)
    pub = rospy.Publisher('result', String, queue_size=10)
    pub2 = rospy.Publisher('/take_photo', String, queue_size=10)
    pub3 = rospy.Publisher('take_me_to', String, queue_size=10)

    while not rospy.is_shutdown():
        # obtain audio from the microphone
        r = sr.Recognizer()
        
        with sr.Microphone() as source:
            print(">>> Say something!")
            #audio = r.listen(source)
            audio = r.record(source, duration=5)
            
        # recognize speech using Google Speech Recognition
        try:
            result = r.recognize_google(audio, language='th')
            print("SR result: " + result)
            if result == 'what is your name':
                pub.publish("my name is max")
            if result == 'can you take a photo':
                pub2.publish("take photo")
            if result == 'take me to bedroom' or result == u"ไปห้องนอน":
                pub3.publish("1")
                pub.publish("heading to the bedroom")
            if result == 'take me to bathroom' or result == u"ไปห้องน้ำ":
                pub3.publish("2")
                pub.publish("heading to the bathroom")

        except sr.UnknownValueError:
            print("SR could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        
        #pub.publish(result)

if __name__ == '__main__':
    try:
        googlesr()
    except rospy.ROSInterruptException:
        pass