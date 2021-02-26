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

x=0
uids =[]
deviceId="CASINO_ENTRY_1" #for diamond entry only
#device_Tier="DIAMOND"

headers={"Authorization": "Basic YWRtaW5pc3RyYXRvcjptYW5hZ2U="}



url="https://SVQPLT.solaireresort.com:9777/ws/PatronCarWhiteList_VS/1.0/Solaire_CarPark/resources/v1/PatronCarWhiteList"


def cardSwipe():
    global x
    x=input("Swipe Card Track 1: \n")
    y=input("Swipe Card Track 2: \n")
    #print(x)
    #uid_new=uids[0]
    return x

def filterData():
    global uid
    try:
        cardSwipe()
        #print(type(x))
        if x[0]=="%" and x[-1]=="?":
            #print("Track 1")
            delLast=x[:-1]
            uid=delLast[1:]
            #print(uid)
            
        elif x[0]==";"and x[-1]=="?":
            #print("Track 2")
            delLast=x[:-1]
            uid2=delLast[1:]
            uid=0
            #print(uid2)
            #print(patronNumberT2)
#         else:
#             uid=0
#             print("Not input from a Reader")
        #return patronNumber
    except:
        uid=0
        print("Swipe Error")
#%100017330722?
;213241?
    
def getData():
    filterData()
    if uid == "100017330722":
        payload={"deviceId":deviceId,
                 "patronNumber":"300914009"}
        #jsonPretty=json.dumps(data, indent=4, sort_keys=True)
        try:
            r=requests.post(url,data=payload,headers=headers)
            body=json.loads(r.text)
            print(body)
            if body['status'] == "Yes":
                GPIO.output(18,GPIO.HIGH)
                GPIO.output(15,GPIO.HIGH)
                print("patronNumber Track 1")
                print("Open Gate")
                sleep(5)
            
        except:
            print("No connection")
    else:
        print("Not Detected")

            
        
def buttonku():
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
    Process(target=buttonku).start()
    try:
        while True:
            
            GPIO.output(18,GPIO.LOW)
            GPIO.output(15,GPIO.LOW)
            getData()
    except KeyboardInterrupt:
        GPIO.cleanup()



    
