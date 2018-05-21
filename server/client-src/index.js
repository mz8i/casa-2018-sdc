// import * as d3 from 'd3';
import Vue from 'vue';
import VueRouter from 'vue-router';
import BootstrapVue from 'bootstrap-vue'


import App from './components/App.vue';
import IntroScreen from './components/IntroScreen.vue';
import OverviewScreen from './components/OverviewScreen.vue';
import TimeScreen from './components/TimeScreen.vue';
import AnalysisScreen from './components/AnalysisScreen.vue';
import {EventBus} from './event-bus';

Vue.use(VueRouter);
Vue.use(BootstrapVue);

import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';

const router = new VueRouter({
    routes: [
        { path: '/intro', component: IntroScreen},
        { path: '/overview', component: OverviewScreen},
        { path: '/time', component: TimeScreen},
        { path: '/analysis', component: AnalysisScreen}
    ]
});

// EventBus.$on('map-loaded', function () {
//     router.push('/intro');
// });

let vm = new Vue({
    router,
    render: function(createElem) { return createElem(App)}
}).$mount("#app-container");



// const map = new mapboxgl.Map({
//     container: 'map', // container element id
//     style: 'mapbox://styles/mz8i/cjh51i78x2p2e2squotdvm06f',
//     center: [-87.6297982, 41.8781136], // initial map center in [lon, lat]
//     zoom: 12
// });



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