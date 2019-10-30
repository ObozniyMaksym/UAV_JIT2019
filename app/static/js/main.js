let points = [];
var uluru = {lat: 49.8643077, lng: 36.4920603};
var map;
let border, flightPlan;
let markers = []
let HomeMarker;
let iconBase =
            'https://developers.google.com/maps/documentation/javascript/examples/full/images/';
let state = 0;
let droneParametrs = {};
let drones = [];

function max(a, b) {
    if (a > b)
        return a;
    return b;
}

