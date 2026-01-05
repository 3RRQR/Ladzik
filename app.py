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
@app.route('/speed', methods=['POST'])
def speedUpdate():
    global speed
    data = request.get_json()
    speed = int(data.get('speed')) * 10
    
    return jsonify({'status': 'success'})


@app.route('/buttons', methods=['POST'])
def buttonsUpdate():
    global speed
    speed = 100
    data = request.get_json()
    button = data.get('button')
    is_pressed = data.get('isPressed')
    button_states[button] = is_pressed
    

    if button == "up":
        drive.forward(speed)
    elif button == "down":
        drive.backward(speed)
    elif button == "left":
        drive.left(speed)
    elif button == "right":
        drive.right(speed)
    elif button == "left-cat":
        drive.leftAlt(speed)
    elif button == "right-cat":
        drive.rightAlt(speed)
    elif button == "left-cat-back":
        drive.leftAltBack(speed)
    elif button == "right-cat-back":
        drive.rightAltBack(speed)

    if button == "stop" or is_pressed is False:
        drive.stop()

    return jsonify({'status': 'success'})


@app.route('/joystick', methods=['POST'])
def JoystickUpdate():
    data = request.get_json()
    x = data.get("x")
    y = data.get("y")
    startx = data.get("startx")
    starty = data.get("starty")

    print(x, y, startx, starty)
   
    return jsonify({'status': 'success'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, threaded=True)
