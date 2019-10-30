
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

function max(a, b) {
    if (a > b)
        return a;
    return b;
}

function sendInfo() {
    angle = max(0, parseFloat(document.getElementById("angle").value));
    height = max(0, parseFloat(document.getElementById("height").value));
    ratio = max(0, parseFloat(document.getElementById("ratio").value));
    or = max(0, parseFloat(document.getElementById("overlapping").value));
    battery = max(0, parseFloat(document.getElementById("battery").value));
    photo = max(0, parseFloat(document.getElementById("photo").value));
    if (!angle || !height || !ratio || !or ||  !battery || !photo || height > 500 || angle > 170 || or > 0.9) {
        alert("Incorrect info!");
        return;
    }
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
    var val = []
    val.push(angle);
    val.push(height);
    val.push(ratio);
    val.push(or);
    val.push(battery);
    val.push(photo);
    var data = JSON.stringify(val);
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
            var ddd = JSON.parse(xhr.responseText);
            path = ddd[0];
            var can = ddd[1];
            console.log(path)
            console.log(points)
            if (path.length == 2) {
                alert("Incorrect input");
                clearShit();
                return;
            }
            if (flightPlan) {
                flightPlan.setMap(null);
            }
            flightPlan = new google.maps.Polyline({
                path: path,
                geodesic: true,
                strokeColor: '#00FF00',
                strokeOpacity: 1.0,
                strokeWeight: 2
            });
            flightPlan.setMap(map);
            if (!can)
                alert("You don't have enough power!!!");
        }
    };
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
