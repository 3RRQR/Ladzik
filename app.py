from flask import Flask, Response, render_template, request, jsonify
import io
import threading
import picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput
from libcamera import Transform

from main import driving, MotorDriver

app = Flask(__name__)
drive = driving
Motor = MotorDriver()
button_states = {}

picam2 = picamera2.Picamera2()


class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = threading.Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()


@app.route('/stream.mjpg')
def video_feed():
    output = StreamingOutput()

    config = picam2.create_video_configuration(
        main={"size": (1280, 720)},
        controls={"FrameRate": (30.0)},
        transform=Transform(vflip=True)
    )

    try:
        picam2.stop()
        picam2.stop_recording()
        picam2.configure(config)
        picam2.start_recording(JpegEncoder(), FileOutput(output))
    except Exception as e:
        print(e)
        return Response(status=500)

    def generate():
        while True:
            with output.condition:
                output.condition.wait()
                frame = output.frame
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/download')
def down():
    return render_template('down.html')


@app.route('/')
def index():
    return render_template('index.html')


#   STEERING

@app.route('/buttons', methods=['POST'])
def buttonsUpdate():
    data = request.get_json()
    button = data.get('button')
    is_pressed = data.get('isPressed')
    button_states[button] = is_pressed

    if button == "up":
        drive.forward(100)
    elif button == "down":
        drive.backward(100)
    elif button == "left":
        drive.left(100)
    elif button == "right":
        drive.right(100)
    elif button == "left-cat":
        drive.leftAlt(100)
    elif button == "right-cat":
        drive.rightAlt(100)
    elif button == "left-cat-back":
        drive.leftAltBack(100)
    elif button == "right-cat-back":
        drive.rightAltBack(100)

    if button == "stop" or is_pressed is False:
        drive.stop()

    return jsonify({'status': 'success'})


@app.route('/joystick', methods=['POST'])
def JoystickUpdate():
    data = request.get_json()
    posX = round(data.get("x") * 2)
    posY = round(data.get("y") * -2)
    turnspeed = 0

    if abs(posY) - abs(posX) > 0:
        turnspeed = abs(posY) - abs(posX)

    if posX < 0 and posY > 0:
        Motor.MotorRun(0, 'forward', turnspeed)
        Motor.MotorRun(1, 'forward', posY)
    elif posX > 0 and posY > 0:
        Motor.MotorRun(0, 'forward', posY)
        Motor.MotorRun(1, 'forward', turnspeed)
    elif posX < 0 and posY < 0:
        Motor.MotorRun(0, 'backward', turnspeed)
        Motor.MotorRun(1, 'backward', abs(posY))
    elif posX > 0 and posY < 0:
        Motor.MotorRun(0, 'backward', abs(posY))
        Motor.MotorRun(1, 'backward', turnspeed)
    elif -20 < posX < 20 and posY > 0:
        drive.forward(posY)
    elif -20 < posX < 20 and posY < 0:
        drive.backward(abs(posY))
    elif posX < 0 and -20 < posY < 20:
        drive.left(abs(posX))
    elif posX > 0 and -20 < posY < 20:
        drive.right(abs(posX))

    if posX == 0 and posY == 0:
        Motor.MotorStop(0)
        Motor.MotorStop(1)

    return jsonify({'status': 'success'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, threaded=True)
