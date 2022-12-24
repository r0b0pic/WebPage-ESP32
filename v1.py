from microdot_asyncio import Microdot, Response, send_file
from microdot_utemplate import render_template
from machine import Pin
import ujson
from time import sleep
from hx711 import HX711
from machine import Pin, PWM
from dcmotor import DCMotor       
   
frequency = 15000       
pin1 = Pin(27, Pin.OUT)    
pin2 = Pin(26, Pin.OUT)     
enable = PWM(Pin(14), frequency)  
dc_motor = DCMotor(pin1, pin2, enable)      
dc_motor = DCMotor(pin1, pin2, enable, 350, 1023) 
speed = 0
forceempty = 90000
forcesoft = 110000
forcehard = 150000


app = Microdot()
Response.default_content_type = 'text/html'


sensorhx = HX711(18,5,1)
sensorhx.power_on()

def measure_force():
    measure=sensorhx.read(True)
    print(f"Force: {measure:.2f}")
    sleep(2)
    return(measure)


@app.route('/')
async def index(request):
    return render_template('index.html')


@app.route('/updateValues')
async def get_force_reads(request):
    print("Receive get values request!")
    sensor_reads = measure_force()

    if ((sensor_reads >= forceempty) and (sensor_reads < forcesoft)):
            speed=50
    elif ((sensor_reads >= forcesoft) and (sensor_reads < forcehard)):
            speed=100
    else :
            speed = 0
    
    dc_motor.forward(speed)    
    sleep(5)        
    dc_motor.stop() 
    print(speed)
    return ujson.dumps({"reading" : sensor_reads})



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






