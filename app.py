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
    data = request.get_json()
    speed = int(data.get('speed'))
    print(speed * 10)
    
    return jsonify({'status': 'success'})


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
    x = data.get("x", 0.0)
    y = data.get("y", 0.0)

    x = max(-1, min(1, x))
    y = max(-1, min(1, -y))


    MAX_SPEED = 100
    DEAD_ZONE = 0.1
    SCALE = 2


    if abs(x) < DEAD_ZONE: x = 0
    if abs(y) < DEAD_ZONE: y = 0


    left = y + x
    right = y - x


    max_val = max(abs(left), abs(right), 1)
    left /= max_val
    right /= max_val


    left_speed = int(left * MAX_SPEED / SCALE)
    right_speed = int(right * MAX_SPEED / SCALE)


    def set_motor(motor_id, speed):
        if speed > 0:
            Motor.MotorRun(motor_id, 'forward', abs(speed))
        elif speed < 0:
            Motor.MotorRun(motor_id, 'backward', abs(speed))
        else:
            Motor.MotorStop(motor_id)

    set_motor(0, left_speed)
    set_motor(1, right_speed)


    if x == 0 and y == 0:
        Motor.MotorStop(0)
        Motor.MotorStop(1)

    return jsonify({'status': 'success'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, threaded=True)
