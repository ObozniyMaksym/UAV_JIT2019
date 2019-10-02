let points = [];
var uluru = {lat: 49.8643077, lng: 36.4920603};
let map;
let border, flightPlan;
let markers = []
let HomeMarker, angle, height, ratio
let iconBase =
            'https://developers.google.com/maps/documentation/javascript/examples/full/images/';
state = 0


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
    if (state != 0)
        state = 0;
    var xhr = new XMLHttpRequest();
    var url = "/sendInfo";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
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
    state = 1;
    alert(state);
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
            var path = ddd[0];
            var can = ddd[1];
            console.log(path)
            console.log(points)
            if (path.length == 2) {
                alert("Incorrect input, you are a stupid son of a bitch");
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
                alert("You don't have enough power!!!((");
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


//It is useless, but don't delete it
function drawLine() {
    if (points.length < 3)
        return;
    var xhr = new XMLHttpRequest();
    var url = "/sort";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            points = JSON.parse(xhr.responseText);
            console.log(points)
            points.push(points[0]);
            if (border) {
                border.setMap(null)
            }
            border = new google.maps.Polyline({
                path: points,
                geodesic: true,
                strokeColor: '#FF0000',
                strokeOpacity: 1.0,
                strokeWeight: 2
            });
            border.setMap(map);
            points.pop()
        }
    };
    var data = JSON.stringify(points);
    xhr.send(data);
}
function initMap() {
    map = new google.maps.Map(
    document.getElementById('map'), {zoom: 15, center: uluru, mapTypeId: google.maps.MapTypeId.SATELLITE});
    google.maps.event.addListener(map, 'click', function(e) {
        var location = e.latLng;
        if (state == 0)
            return;
        if (state == 1) {
            console.log(1)
            var marker = new google.maps.Marker({
                position: location,
                map: map,
                icon: iconBase + 'parking_lot_maps.png'
            });  
            marker.setMap(map)
            HomeMarker = marker
            sendHomePoint(location)
            state = 2
            return;
        }
        var marker = new google.maps.Marker({
                position: location,
                map: map
        }); 
        markers.push(marker)
        var lat = marker.getPosition().lat();
        var lng = marker.getPosition().lng();
        points.push({lat: lat, lng: lng});        
        addPoint();
    })
}