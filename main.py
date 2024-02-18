#!/usr/bin/python

from PCA9685 import PCA9685

Dir = [ 	#index
    'forward',	#0
    'backward',	#1
]
pwm = PCA9685(0x40, debug=False)
pwm.setPWMFreq(100)

class MotorDriver():
    def __init__(self):
        self.PWMA = 0
        self.AIN1 = 1
        self.AIN2 = 2
        self.PWMB = 5
        self.BIN1 = 3
        self.BIN2 = 4

    def MotorRun(self, motor, index, speed):
        if speed > 100:
            #print("prędkość mniejsza niż 100")
            return
        
        if(motor == 0): #silnik lewy
            pwm.setDutycycle(self.PWMA, speed)
            if(index == Dir[0]):
                #print ("lewy przód")
                pwm.setLevel(self.AIN1, 0)
                pwm.setLevel(self.AIN2, 1)
            else:
                #print ("lewy tył")
                pwm.setLevel(self.AIN1, 1)
                pwm.setLevel(self.AIN2, 0)
        else:		#silnik prawy
            pwm.setDutycycle(self.PWMB, speed)
            if(index == Dir[0]):
                #print ("prawy przód")
                pwm.setLevel(self.BIN1, 1)
                pwm.setLevel(self.BIN2, 0)
            else:
                #print ("prawy tył")
                pwm.setLevel(self.BIN1, 0)
                pwm.setLevel(self.BIN2, 1)

    def MotorStop(self, motor):
        if (motor == 0):
            #print("lewy stop")
            pwm.setDutycycle(self.PWMA, 0)
        else:
            #print("prawy stop")
            pwm.setDutycycle(self.PWMB, 0)

class driving():        
    def forward(speed):
        Motor.MotorRun(0, 'forward', speed)
        Motor.MotorRun(1, 'forward', speed)

    def backward(speed):
        Motor.MotorRun(0, 'backward', speed)
        Motor.MotorRun(1, 'backward', speed)

    def left(speed):
        Motor.MotorRun(0, 'forward', speed)
        Motor.MotorRun(1, 'backward', speed)

    def right(speed):
        Motor.MotorRun(0, 'backward', speed)
        Motor.MotorRun(1, 'forward', speed)

    def leftAlt(speed):
        Motor.MotorRun(0, 'forward', speed)
    
    def rightAlt(speed):
        Motor.MotorRun(1, 'forward', speed)

    def leftAltBack(speed):
        Motor.MotorRun(0, 'backward', speed)
    
    def rightAltBack(speed):
        Motor.MotorRun(1, 'backward', speed)


    
    def stop():
        Motor.MotorStop(0)
        Motor.MotorStop(1)
    
    def kill():
        quit()



Motor = MotorDriver()