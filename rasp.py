import RPi.GPIO as GPIO #rasp import
import time

TRIG = 23
ECHO = 24
MOTOR_FORWARD = 17   
MOTOR_BACKWARD = 18  
MOTOR_ENABLE = 22     

LED_GREEN = 27        
LED_RED = 25       
BUZZER = 5            

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(MOTOR_FORWARD, GPIO.OUT)
GPIO.setup(MOTOR_BACKWARD, GPIO.OUT)
GPIO.setup(MOTOR_ENABLE, GPIO.OUT)
GPIO.setup(LED_GREEN, GPIO.OUT)
GPIO.setup(LED_RED, GPIO.OUT)
GPIO.setup(BUZZER, GPIO.OUT)

pwm = GPIO.PWM(MOTOR_ENABLE, 100)
pwm.start(0) 

def get_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.01)
    GPIO.output(TRIG, False)

    # Echo time
    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(ECHO) == 0:
        start_time = time.time()
        
    while GPIO.input(ECHO) == 1:
        stop_time = time.time()

    # distance
    elapsed_time = stop_time - start_time
    distance = (elapsed_time * 34300) / 2  # Speed of sound in cm/s
    return distance

try:
    while True:
        distance = get_distance()
        print(f"Distance: {distance:.2f} cm")

        if distance < 60:  # 2 feet = 60 cm
            GPIO.output(MOTOR_FORWARD, False)
            GPIO.output(MOTOR_BACKWARD, False)
            pwm.ChangeDutyCycle(0) 
        
            GPIO.output(LED_RED, True)  
            GPIO.output(LED_GREEN, False)  
            GPIO.output(BUZZER, True)  
            print("Robot stopped due to proximity!")
        else:
            #forward
            GPIO.output(MOTOR_FORWARD, True)
            GPIO.output(MOTOR_BACKWARD, False)
            pwm.ChangeDutyCycle(100)  #Speed
            
            # Feedback
            GPIO.output(LED_GREEN, True)  
            GPIO.output(LED_RED, False)  
            GPIO.output(BUZZER, False)  
            print("Robot moving forward.")

        time.sleep(0.5)  

except KeyboardInterrupt:
    print("Measurement stopped by user")
finally:
    GPIO.cleanup()
