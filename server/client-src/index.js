import * as d3 from 'd3';
import mapboxgl from 'mapbox-gl';

mapboxgl.accessToken = 'pk.eyJ1IjoibXo4aSIsImEiOiJjamg0d2pxcDMxNXFzMnFwdG52aG81cTc5In0.CksGFWg2x0MiWRShMnYsxQ';

const map = new mapboxgl.Map({
    container: 'map', // container element id
    style: 'mapbox://styles/mz8i/cjh51i78x2p2e2squotdvm06f',
    center: [-87.6297982, 41.8781136], // initial map center in [lon, lat]
    zoom: 12
});

// // The 'building' layer in the mapbox-streets vector source contains building-height
// // data from OpenStreetMap.
// map.on('load', function () {
//     // Insert the layer beneath any symbol layer.
//     var layers = map.getStyle().layers;

//     var labelLayerId;
//     for (var i = 0; i < layers.length; i++) {
//         if (layers[i].type === 'symbol' && layers[i].layout['text-field']) {
//             labelLayerId = layers[i].id;
//             break;
//         }
//     }

//     map.addLayer({
//         'id': '3d-buildings',
//         'source': 'composite',
//         'source-layer': 'building',
//         'filter': ['==', 'extrude', 'true'],
//         'type': 'fill-extrusion',
//         'minzoom': 12,
//         'paint': {
//             'fill-extrusion-color': '#aaa',

//             // use an 'interpolate' expression to add a smooth transition effect to the
//             // buildings as the user zooms in
//             'fill-extrusion-height': ["get", "height"],
//             'fill-extrusion-opacity': .6
//         }
//     }, labelLayerId);
// });