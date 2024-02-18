document.addEventListener("DOMContentLoaded", function () {
    //change controller type
    const buttonsRadio = document.getElementById('but-opt')
    const joystickRadio = document.getElementById('joy-opt')
    const butt = document.getElementById('buttons')
    const joys = document.getElementById('joystick')
    const warn = document.getElementById('warning')

    buttonsRadio.addEventListener('change', function () {
        butt.style.display = 'grid';
        joys.style.display = 'none';
        warn.style.display = 'none';
    });

    joystickRadio.addEventListener('change', function () {
        butt.style.display = 'none';
        joys.style.display = 'flex';
        warn.style.display = 'block';
    });

    //LIVEFEED CONTROLS

    //top - checkboxes
    const showInfo = document.getElementById('info')
    const rotation = document.querySelectorAll('input[name="RT"]')

    showInfo.addEventListener('input', () => {
        sleep(2000)
        fetch('/chckbox', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ showInfo: showInfo.checked }),
        })
            .then(response => response.json())
            .then(data => console.log(data))
            .catch(error => console.error('Error:', error));
    })

    rotation.forEach((radio, switchNumber) => {
        sleep(2000)
        radio.addEventListener('change', () => {
            fetch('/chckbox', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ rotation: switchNumber }),
            })
                .then(response => response.json())
                .then(data => console.log(data))
                .catch(error => console.error('Error:', error));
        });
    })

    //middle - sliders
    const qualitySlider = document.getElementById('quality')
    const zoomSilder = document.getElementById('zoom')
    const framesSlider = document.getElementById('frames')

    qualitySlider.addEventListener('input', (event) => {
        fetch('/sliders', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ quality: event.target.value }),
        })
            .then(response => response.json())
            .then(data => console.log(data))
            .catch(error => console.error('Error:', error));
    })

    zoomSilder.addEventListener('input', (event) => {
        fetch('/sliders', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ zoom: event.target.value }),
        })
            .then(response => response.json())
            .then(data => console.log(data))
            .catch(error => console.error('Error:', error));
    })

    framesSlider.addEventListener('input', (event) => {
        fetch('/sliders', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ frames: event.target.value }),
        })
            .then(response => response.json())
            .then(data => console.log(data))
            .catch(error => console.error('Error:', error));
    })

    //STEERING


    //buttons
    const buttons = document.querySelectorAll('.control-button');

    buttons.forEach(button => {
        button.addEventListener('mousedown', function () {
            sendCommand(button.getAttribute('data-button-id'), 1);
        });

        button.addEventListener('mouseup', function () {
            sendCommand(button.getAttribute('data-button-id'), false);
        });
    });

    function sendCommand(button, isPressed) {
        fetch('/buttons', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ button: button, isPressed: isPressed }),
        })
            .then(response => response.json())
            .then(data => console.log(data))
            .catch(error => console.error('Error:', error));
    }

    //joystick
    var joystick = nipplejs.create({
        zone: document.getElementById('joystick'),
        mode: 'static',
        position: { left: '50%', top: '50%' },
        color: 'black',
        restJoystick: true,
        shape: 'square',
        dynamicPage: true,
        size: '100',
    });

    let joyMoveCounter = 0;

    joystick.on('move', function (evt, nipple) {
        x = nipple.position.x - startx;
        y = nipple.position.y - starty;

        joyMoveCounter++;

        if (joyMoveCounter % 10 === 0) {

            fetch('/joystick', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ x: x, y: y, startx: startx, starty: starty }),
            })
                .then(response => response.json())
                .then(data => console.log(data))
                .catch(error => console.error('Error:', error));
        }
    }).on('start', function (evt, nipple) {
        startx = nipple.position.x;
        starty = nipple.position.y;

    }).on('end', function (evt) {
        x = 0;
        y = 0;

        fetch('/joystick', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ x: x, y: y, startx: startx, starty: starty }),
        })
            .then(response => response.json())
            .then(data => console.log(data))
            .catch(error => console.error('Error:', error));

    });
});
