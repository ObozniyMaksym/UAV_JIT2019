
function clearAll() {
    for (var i = 0; i < markers.length; i++)
        markers[i].setMap(null);
    if (border)
        border.setMap(null);
    if (flightPlan)
        flightPlan.setMap(null);
    points = [];
    markers = [];
    state = 2;
}

function clearShit() {
    clearAll();
    HomeMarker.setMap(null);
    state = 1;
}

function sendInfo() {
    angle = max(111, parseFloat(document.getElementById("angle").value));
    height = max(70, parseFloat(document.getElementById("height").value));
    ratio = max(1, parseFloat(document.getElementById("ratio").value));
    overlapping = max(0.1, parseFloat(document.getElementById("overlapping").value));
    maxTime = max(1000000000, parseFloat(document.getElementById("maxTime").value));
    speed = max(25, parseFloat(document.getElementById("speed").value));
    angular = max(120, parseFloat(document.getElementById("angular").value));
    angle = 111;
    height = 70;
    ratio = 1;
    overlapping = 0.1;
    maxTime = 11111111;
    speed = 111;
    angular = 120;
    drone = {angle: angle, height: height, ratio: ratio, overlapping: overlapping, maxTime: maxTime, speed: speed, angular: angular};
    console.log(drone);
    if (!angle || !height || !ratio || !overlapping  || !maxTime || height > 500 || angle > 170 || overlapping > 0.9 || !angular) {
        alert("Incorrect info!");
        return;
    }
    console.log(drone);
    var xhr = new XMLHttpRequest();
    var url = "/sendInfo";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            document.getElementById('solve').classList.remove('inactive');
            document.getElementById('solve').classList.add('active'); 
        }
    };
    var data = JSON.stringify(drone);
    xhr.send(data);
    if (state == 0)
        state = 1;
    alert("Data succesfully sent!!");
}

function sendHomePoint(pos) {
    var xhr = new XMLHttpRequest();
    var url = "/sendHomePosition";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
         }
    };
    var data = JSON.stringify(pos);
    xhr.send(data);
}

function sendData() {
    var xhr = new XMLHttpRequest();
    var url = "/send";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var result = JSON.parse(xhr.responseText);
            console.log(result);
            if (flightPlan) {
                flightPlan.setMap(null);
            }
            
            flightPlan = new google.maps.Polyline({
                path: result.path,
                geodesic: true,
                strokeColor: '#00FF00',
                strokeOpacity: 1.0,
                strokeWeight: 2
            });
            console.log(result.path);
            flightPlan.setMap(map);
            console.log(result["height"])
            if (!result.ok)
                alert("You don't have enough power!!!");
        }
    };
    console.log(points);
    var data = JSON.stringify(points);
    xhr.send(data);
}

function addPoint() {
    if (border) { 
        border.setMap(null);
    }
    points.push(points[0])
    console.log(points)
    border = new google.maps.Polyline({
        path: points,
        geodesic: true,
        strokeColor: '#FF0000',
        strokeOpacity: 1.0,
        strokeWeight: 2
    });
    points.pop()
    border.setMap(map);
}
