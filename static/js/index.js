document.addEventListener("DOMContentLoaded", function() {
    // Temperature Gauge Configurations
    var forceData = [{
        domain: {
            x: [0, 1],
            y: [0, 1]
        },
        value: 0,
        title: {
            text: "Force sensor"
        },
        type: "indicator",
        mode: "gauge+number+delta",
        delta: {
            reference: 90000
        },
        gauge: {
            axis: {
                range: [0, 200000]
            },
            steps: [{
                    range: [0, 80000],
                    color: "lightgray"
                },
                {
                    range: [80000, 150000],
                    color: "gray"
                }
            ],
            threshold: {
                line: {
                    color: "red",
                    width: 4
                },
                thickness: 0.75,
                value: 175000
            }
        }
    }];
    
     var speedData = [{
        domain: {
            x: [0, 1],
            y: [0, 1]
        },
        value: 0,
        title: {
            text: "Command motor - speed"
        },
        type: "indicator",
        mode: "gauge+number+delta",
        delta: {
            reference: 50
        },
        gauge: {
            axis: {
                range: [0, 200]
            },
            steps: [{
                    range: [0, 100],
                    color: "lightgray"
                },
                {
                    range: [100, 200],
                    color: "gray"
                }
            ],
            threshold: {
                line: {
                    color: "red",
                    width: 4
                },
                thickness: 0.75,
                value: 90
            }
        }
    }];

    
    // Layout object that set's the size of our Gauge
    var layout = {
        width: 400,
        height: 350,
        margin: {
            t: 0,
            b: 0
        }
    };
    
    // Create our two Gauge passing in the different configurations
    Plotly.newPlot('forceDiv', forceData, layout);
    Plotly.newPlot('speedDiv', speedData, layout);

});

// Callback function that will retrieve our latest sensor readings and redraw our Gauge with the latest readings
function updatePlot() {
    console.log("Updating chart");
    fetch(`/updateValues`)
        .then((response) => response.json())
        .then(data => {
            var force_update = {
                value: data[0]
            };

            Plotly.update("forceDiv", force_update);

        })
}

function updateSpeed() {
    console.log("Updating chart");
    fetch(`/updateSpeed`)
        .then((response) => response.json())
        .then(data => {
            var speed_update = {
                value: data[0]
            };

            Plotly.update("speedDiv", speed_update);

        })
}

function toggleButtonSwitch(e) {
  var switchButton = document.getElementById("switch");
  const led_state = document.getElementById('ledstate');
  //const btn = document.getElementById('btn');
  var toggleValue = "";
  
  if (switchButton.checked) {
    console.log("On!");
    toggleValue = "ON";
    //document.getElementById("ledDiv").innerHTML = 1;
  } else {
    console.log("Off!");
    toggleValue = "OFF"
    //document.getElementById("ledDiv").innerHTML = 0;
    //var h = JSON.parse(data);
  }
  fetch( `/toggle`)
  .then( response => {
    console.log(response);
    led_state.style.display = 'block';
    if (toggleValue=="ON")
    {document.getElementById("ledstate").innerHTML = "ON";}
    else
    {document.getElementById("ledstate").innerHTML = "OFF";}

    //btn.textContent = 'Hide div';
  } )
}

// Continuos loop that runs evry 3 seconds to update our web page with the latest sensor readings
(function loop() {
    setTimeout(() => {
        updatePlot()
        updateSpeed()
        /*toggleButtonSwitch(e)*/
        loop();
    }, 3000);
})();