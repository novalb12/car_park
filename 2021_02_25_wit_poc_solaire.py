import requests, json
import RPi.GPIO as GPIO
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(18,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)
GPIO.setup(14,GPIO.IN, pull_up_down=GPIO.PUD_UP)

from time import sleep
import time

from multiprocessing import Process


uid=0
track1=0
track2=0

headers={"Authorization": "Basic YWRtaW5pc3RyYXRvcjptYW5hZ2U="}



url="https://SVQPLT.solaireresort.com:9777/ws/PatronCarWhiteList_VS/1.0/Solaire_CarPark/resources/v1/PatronCarWhiteList"


def cardSwipe():
    global track1
    track1=input("Swipe Card Track 1: \n")
    track2=input("Swipe Card Track 2: \n")
    #print(x)
    #uid_new=uids[0]
    return track1

def filterData():
    global uid
    try:
        cardSwipe()
        if track1[0]=="%" and track1[-1]=="?":
            #print("Track 1")
            #uid=track1[1:-1]
            uid = ''.join([n for n in track1 if n.isdigit()])
            print(uid)
            
        elif track2[0]==";"and track2[-1]=="?":
            #print("Track 2")
            #uid2=track2[1:-1]
            uid2 = ''.join([n for n in track2 if n.isdigit()])
#         else:
#             uid=0
#             print("Not input from a Reader")
    except:
        print("Swipe Error")
        
#%100017330722?
#213241?
    
def getData():
    filterData()
    if uid == "100017330722": #silver Member
        payload={"deviceId":"CASINO_ENTRY_1",
                 "patronNumber":"300914009"}
        #jsonPretty=json.dumps(data, indent=4, sort_keys=True)
        try:
            req=requests.post(url,data=payload,headers=headers,verify = False)
            body=json.loads(req.text)
            print(body)
            if body['status'] == "Yes":
                print("Close Gate, Doesn't Have Access")
                print("Tier: SILVER")
                print("Member: ACTIVE")
                sleep(5)
        except:
            print("No connection")

    elif uid == "9990012232433868": #ruby Member
        payload={"deviceId":"CASINO_ENTRY_1",
                 "patronNumber":"32131"}
        try:
            req=requests.post(url,data=payload,headers=headers,verify = False)
            body=json.loads(req.text)
            print(body)
            if body['status'] == "Yes":
                GPIO.output(18,GPIO.HIGH)
                GPIO.output(15,GPIO.HIGH)
                print("Open Gate, No Access to Solaire Club Park")
                print("Tier: Ruby")
                print("Member: ACITVE")
                sleep(5)
        except:
            print("No connection")
    elif uid == "60130101060429802301120000000000000000339000000":  #Diamond Member
        payload={"deviceId":"CASINO_ENTRY_1",
                 "patronNumber":"300914009"}
        try:
            req=requests.post(url,data=payload,headers=headers,verify = False)
            print(req)
            body=json.loads(req.text)
            print(body)
            if body['status'] == "Yes":
                GPIO.output(18,GPIO.HIGH)
                GPIO.output(15,GPIO.HIGH)
                print("Open Gate, Welcome to Solaire Club Parking")
                print("Tier: DIAMOND")
                print("Member: ACTIVE")                
                sleep(5)
        except:
            print("No connection")
    else:
        print("Not Detected")

            
        
def button():
    while True:
        
        GPIO.wait_for_edge(14, GPIO.RISING)
        start=time.time()
        time.sleep(0.2)
        
        while GPIO.input(14) == GPIO.LOW:
            time.sleep(0.01)
        length = time.time() -start
        if length > 0.21:
            print (length)
            GPIO.output(18,GPIO.HIGH)
            GPIO.output(15,GPIO.HIGH)
            print("button pressed")
            sleep(5)
            GPIO.output(18,GPIO.LOW)
            GPIO.output(15,GPIO.LOW)

if __name__ == "__main__":
    Process(target=button).start()
    while True:
        if track1=="exit":
            break
        GPIO.output(18,GPIO.LOW)
        GPIO.output(15,GPIO.LOW)
        getData()



    
