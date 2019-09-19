let points = [];
var uluru = {lat: 49.8643077, lng: 36.4920603};
let map;
let border, flightPlan;

function sendData() {
    var xhr = new XMLHttpRequest();
    var url = "/send";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var path = JSON.parse(xhr.responseText);
            console.log(path)
            console.log(points)
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
        }
    };
    var data = JSON.stringify(points);
    xhr.send(data);
}


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
        var marker = new google.maps.Marker({
            position: location,
            map: map
        });
        var lat = marker.getPosition().lat();
        var lng = marker.getPosition().lng();
        points.push({lat: lat, lng: lng});        
    })
}