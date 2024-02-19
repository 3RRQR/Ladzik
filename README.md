# Ladzik - remote controlled robot using web browser
<p>robot named "Ladzik" is really just a raspberry pi on crawler platform. It has an attached a raspberry pi camera v2 on front and a lipo battery mounted underneath a platform for vision and power. For a computer that drives everything I opted for raspberry pi zero W but you can use for example:</p> 
<ul>
<li>rasberry pi 4 - it is set in parallel with platform and in my case I used rubberbands to secure it</li>
<li>arduino - not tested but manufacturer of the platform shows arduino uno is supported and has a holes for it</li>
<li>any other microcontroller - I couldn't test it, I don't have any</li>
</ul>

<p>for creating your own Ladzik you will need:</p>
<ul>
    <li>raspberry pi zero 2 W - main computer</li>
    <li>DFRobot Black Gladiator ROB0153 - crawler platform</li>
    <li>dual channel DC motor driver HAT - I used Waveshare 15364 but of course you can use other</li>
    <li>raspberry pi camera V2 - or any other you like/have</li>
    <li>case for camera - I used Adafruit 3253 but WARNING! Do not use it with original raspberry pi camera v2 it dosen't fit and because of that focus is destroyed</li>
    <li>in some cases you will need an adapter for raspberry pi zero camera output, it is smaller than ribbon cable that pi camera comes with.</li>
</ul>
<p>Additionally, you will need bare wires to connect the dc motors from the pi's HAT and a male connector to the lipo battery, in my case it was a small tamiya, but now lipo batteries come with a T-connect or even a large tamiya. Of course, you can use 18650, AA or even a powerbank, but remember that powerbanks have overload protection and if you draw too much current, the powerbank will cut off the power.</p>


<p>some rambling about powering a Ladzik using powerbank. When doing that use USB breakout board or even bare usb plug for soldering, check what pins are 5V and ground and solder wires accordingly. that is easiest way of getting power from powerbank to pi's HAT. after that I recommend using 5V to 12V step up converter because that what is needed in pi's motor driver HAT. That will not bypass powerbank's internal overload protection but will supply 12V with 0.5A max. For more ampers you will need to enable quick charge over usb if your powerbank support's it. In short, I do not recommend powerbanks for this project at all. </p>


<p>Here are some photos when the robot had a powerbank as power supply and without camera:</p>
<img src="photos/build1.jpg">
<p>front</p>
<img src="photos/build2.jpg">
<p>back</p>
<img src="photos/build3.jpg">
<p>top</p>
<img src="photos/build4.jpg">
<p>underneath</p>
<img src="photos/build5.jpg">
<p>without powerbank</p>

<p>and here are some photos of the current state:</p>
<img src="photos/build6.jpg">
<p>front</p>
<img src="photos/build7.jpg">
<p>back</p>
<img src="photos/build8.jpg">
<p>top</p>
<img src="photos/build9.jpg">
<p>underneath</p>


<p>and after it when a computer was a raspberry pi 4 and power was comming from powerbank</p>

<h2>PCA9685.py and main.py are based on/copied from code published on https://www.waveshare.com/wiki/Motor_Driver_HAT in section "Demo".</h2>
<p>that code is for controlling HAT attachment on raspberry pi zero 2 w that drives motors of a robot.</p>
