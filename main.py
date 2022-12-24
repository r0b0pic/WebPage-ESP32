from microdot_asyncio import Microdot, Response, send_file
from microdot_utemplate import render_template
from machine import Pin
import ujson
from time import sleep
from hx711 import HX711
from machine import Pin, PWM
from dcmotor import DCMotor
import network, utime
from led_module import LEDModule

frequency = 15000       
pin1 = Pin(27, Pin.OUT)    
pin2 = Pin(26, Pin.OUT)     
enable = PWM(Pin(14), frequency)
dc_motor = DCMotor(pin1, pin2, enable)      
dc_motor = DCMotor(pin1, pin2, enable, 350, 1023)
speed = 0

sensorhx = HX711(18,5,1)
forceempty = 0
forcesoft = 50000
forcehard = 150000

# Our LED Module
led_module = LEDModule(23)
led_state = 0


app = Microdot()
Response.default_content_type = 'text/html'

def send_speed():
    sensor_reads = sensorhx.get_values()
    measure_force = sensorhx.measure()
    led_value=led_module.get_value()
    if(led_value == 1):
        
        if ((measure_force>= forceempty) and (measure_force < forcesoft)):
                speed=50
                
        elif ((measure_force>= forcesoft) and (measure_force < forcehard)):
                speed=100
        else :
                speed = 0
    else:
        speed = 0
    return speed, speed



@app.route('/')
async def index(request):
    return render_template('index.html', led_value=led_module.get_value())


@app.route('/toggle')
async def toggle_led(request):
    print("Receive Toggle Request!")
    led_module.toggle()
    led_value=led_module.get_value()
    print("Ledvalue:", led_value)

    return "OK"

@app.route('/updateSpeed')
async def get_speed_reads(request):
    print("Receive get speed request!")
    #sensor_reads = dht_sensor.get_values()
    data_speed = send_speed()

    return ujson.dumps(data_speed)


@app.route('/updateValues')
async def get_force_reads(request):
    print("Receive get values request!")
    #sensor_reads = dht_sensor.get_values()
    sensor_reads = sensorhx.get_values()
    measure_force = sensorhx.measure()
    led_value=led_module.get_value()
    
    if(led_value==1):
        
        if ((measure_force>= forceempty) and (measure_force < forcesoft)):
                speed=50
                dc_motor.forward(speed)
        elif ((measure_force>= forcesoft) and (measure_force < forcehard)):
                speed=100
                dc_motor.forward(speed)
        else :
                speed = 0
                dc_motor.forward(speed)
    else:
        speed = 10
        dc_motor.stop()
   
    return ujson.dumps(sensor_reads)


@app.route('/shutdown')
async def shutdown(request):
    request.app.shutdown()
    return 'The server is shutting down...'


@app.route('/static/<path:path>')
def static(request, path):
    if '..' in path:
        # directory traversal is not allowed
        return 'Not found', 404
    return send_file('static/' + path)

app.run()