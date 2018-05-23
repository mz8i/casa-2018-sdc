<template>
    <div class="screen intro-screen">

    </div>
</template>

<script>
import { EventBus } from '../event-bus.js';

let startPoint = {
    "longitude": -87.68073116413068,
    "latitude": 41.842710569130205,
    "zoom": 13,
    "bearing": -93.046875,
    "pitch": 58.029633843623536,
    speed: 0.3
};


export default {
    name: 'IntroScreen',
    beforeRouteEnter: function(to, from, next) {
        next(vm => {
            vm.active = true;
            vm.start();
        })
    },
    beforeRouteLeave: function(to, from, next) {
        this.end();
        this.active = false;
        next();
    },
    created: function() {
        this.animationFrame = null;
    },
    data: () => ({
        active: false
    }),
    methods: {
        start: function() {
            EventBus.$emit('jump-to', startPoint);

            // setTimeout(() => {
                // this.animationFrame = requestAnimationFrame(this.animate);
                // this.startTime = Date.now();

                // EventBus.$emit('add-layer', [{
                //     'id': '3d-buildings',
                //     'source': 'composite',
                //     'source-layer': 'building',
                //     'filter': ['==', 'extrude', 'true'],
                //     'type': 'fill-extrusion',
                //     'minzoom': 9,
                //     'paint': {
                //         'fill-extrusion-color': '#aaa',

                //         // use an 'interpolate' expression to add a smooth transition effect to the
                //         // buildings as the user zooms in
                //         'fill-extrusion-height': [
                //             // "interpolate", ["linear"], ["zoom"],
                //             // 15, 0,
                //             // 15.05, 
                //             ["get", "height"]
                //         ],
                //         // 'fill-extrusion-base': [
                //         //     "interpolate", ["linear"], ["zoom"],
                //         //     15, 0,
                //         //     15.05, ["get", "min_height"]
                //         // ],
                //         'fill-extrusion-opacity': 1
                //     }
                // }, 'waterway-label']);
            // }, 7000);
        },

        end: function() {
            cancelAnimationFrame(this.animationFrame);
            EventBus.$emit('remove-layer', '3d-buildings');
        },
        animate: function(timestamp) {
            if(this.active) this.animationFrame = requestAnimationFrame(this.animate);
            let progress = timestamp - this.startTime;
            let bearing = (startPoint.bearing + progress / 500) % 360;
            let newView = Object.assign({}, startPoint, {bearing});
            EventBus.$emit('jump-to', newView);
        }
    }
}
</script>

<style scoped>
    .intro-screen {
        color: white;
    }
</style>
