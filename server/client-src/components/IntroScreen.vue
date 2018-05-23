<template>
    <div class="screen intro-screen">

    </div>
</template>

<script>
import { EventBus } from '../event-bus.js';

let startPoint = {
    "longitude": -87.68073116413068,
    "latitude": 41.842710569130205,
    "zoom": 9.5,
    "bearing": -93.046875,
    "pitch": 58.029633843623536
};


export default {
    name: 'IntroScreen',
    beforeRouteEnter: function(to, from, next) {
        next(vm => {
            vm.start();
        })
    },
    beforeRouteLeave: function(to, from, next) {
        this.end();
        next();
    },
    created: function() {
        this.animationFrame = null;
    },
    methods: {
        start: function() {
            EventBus.$emit('add-layer', {
                'id': '3d-buildings',
                'source': 'composite',
                'source-layer': 'building',
                'filter': ['==', 'extrude', 'true'],
                'type': 'fill-extrusion',
                'minzoom': 15,
                'paint': {
                    'fill-extrusion-color': '#aaa',

                    // use an 'interpolate' expression to add a smooth transition effect to the
                    // buildings as the user zooms in
                    // 'fill-extrusion-height': [
                    //     "interpolate", ["linear"], ["zoom"],
                    //     15, 0,
                    //     15.05, ["get", "height"]
                    // ],
                    // 'fill-extrusion-base': [
                    //     "interpolate", ["linear"], ["zoom"],
                    //     15, 0,
                    //     15.05, ["get", "min_height"]
                    // ],
                    'fill-extrusion-opacity': 1
                }
            });
            setTimeout(() => EventBus.$emit('fly-to', startPoint), 2000);

            setTimeout(() => {
                this.animationFrame = requestAnimationFrame(this.animate);
                this.startTime = Date.now();
            }, 3000);
        },

        end: function() {
            EventBus.$emit('remove-layer', '3d-buildings');
            cancelAnimationFrame(this.animationFrame);
        },
        animate: function(timestamp) {
            let progress = timestamp - this.startTime;
            let bearing = (startPoint.bearing + progress / 500) % 360;
            let newView = Object.assign({}, startPoint, {bearing});
            EventBus.$emit('jump-to', newView);
            this.animationFrame = requestAnimationFrame(this.animate);
        }
    }
}
</script>

<style scoped>
    .intro-screen {
        color: white;
    }
</style>
