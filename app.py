from flask import Flask, render_template, request, jsonify
import io
import threading
app = Flask(__name__)
button_states = {}

#   WEBSITE

@app.route('/download')
def down():
    return render_template('down.html')


@app.route('/')
def index():
    return render_template('index.html')


#   STEERING


#buttons
@app.route('/buttons', methods=['POST'])
def buttonsUpdate():
    data = request.get_json()
    button = data.get('button')
    is_pressed = data.get('isPressed')
    button_states[button] = is_pressed
    
    if button == "up":
        print(button, is_pressed)
    elif button == "down":
        print(button, is_pressed)
    elif button == "left":
        print(button, is_pressed)
    elif button == "right":
        print(button, is_pressed)
    elif button == "left-cat":
        print(button, is_pressed)
    elif button == "right-cat":
        print(button, is_pressed)
    elif button == "left-cat-back":
        print(button, is_pressed)
    elif button == "right-cat-back":
        print(button, is_pressed)
    
        
    return jsonify({'status': 'success'})


#joystick
@app.route('/joystick', methods=['POST'])
def JoystickUpdate():
    data = request.get_json()
    posX = round(data.get("x") * 2)
    posY = round(data.get("y") * -2) 
    turnspeed = 0

    print("STR JOY", posX, posY, turnspeed)

    if abs(posY) - abs(posX) > 0:
        turnspeed = abs(posY) - abs(posX)
    else:
        turnspeed = 0

    if posX < 20 and posX > -20 and posY > 0:
        print("STR JOY forward")
    if posX < 20 and posX > -20 and posY < 0:
        print("STR JOY backward")
    if posX < 0 and posY > -20 and posY < 20:
        print("STR JOY left")
    if posX > 0 and posY > -20 and posY < 20:
        print("STR JOY right")


    return jsonify({'status': 'success'})

    
#   LIVEFEED CONTROLS


#checkboxes
@app.route('/chckbox', methods=['POST'])
def checkboxes():
    data = request.get_json()
    showInfo = data.get("showInfo")
    rotation = data.get("rotation")

    print("CHECKBOXES", showInfo, rotation)

    return jsonify({'status': 'success'})


#sliders
@app.route('/sliders', methods=['POST'])
def sliders():
    data = request.get_json()
    quality = data.get("quality")
    zoom = data.get("zoom")
    frames = data.get("frames")

    print("SLIDERS", quality, zoom, frames)

    return jsonify({'status': 'success'})


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8000, threaded=True)



