document.addEventListener("DOMContentLoaded", function () {
    //change controller type
    const buttonsRadio = document.getElementById('but-opt')
    const joystickRadio = document.getElementById('joy-opt')
    const controllerRadio = document.getElementById('ctr-opt')
    const butt = document.getElementById('buttons')
    const joys = document.getElementById('joystick-zone')
    const cont = document.getElementById('controller-controls')

    buttonsRadio.addEventListener('change', function () {
        butt.style.display = 'grid';
        joys.style.display = 'none';
        cont.style.display = 'none';
    });

    joystickRadio.addEventListener('change', function () {
        butt.style.display = 'none';
        joys.style.display = 'flex';
        cont.style.display = 'none';
    });

    controllerRadio.addEventListener('change', function () {
        butt.style.display = 'none';
        joys.style.display = 'none';
        cont.style.display = 'flex';
    });

    //buttons
    const buttons = document.querySelectorAll('.control-button');
    const speed = document.getElementById('speed')

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

    speed.addEventListener('input', (event) => {
        fetch('/speed', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ speed: event.target.value }),
        })
            .then(response => response.json())
            .then(data => console.log(data))
            .catch(error => console.error('Error:', error));
    })

    //joystick
    var joystick = nipplejs.create({
        zone: document.getElementById('joystick-zone'),
        mode: 'static',
        position: { left: '50%', top: '50%' },
        color: 'black',
        restJoystick: true,
        shape: 'square',
        dynamicPage: true,
        size: '200',
    });

    let joyMoveCounter = 0;

    joystick.on('move', function (evt, nipple) {
        x = nipple.position.x - startx;
        y = (nipple.position.y - starty) * -1;

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

    //controller
    const bllist = document.getElementById('list')
    
    on('blupdate', function (content){
        bllist.innerText = content;
    })

});
