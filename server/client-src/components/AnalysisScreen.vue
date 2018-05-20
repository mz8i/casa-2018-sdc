<template>
    <div class="screen analysis-screen">
        <h1>Analysis Screen test</h1>
        <router-link to="intro">Go to Intro</router-link>
    </div>
</template>

<script>

import {feature, featureCollection} from '@turf/helpers';
import wellknown from 'wellknown';

import { EventBus } from '../event-bus.js';


let startPoint = { center: [-87.9074, 41.9742], zoom: 13, pitch: 0, bearing: 0 };

export default {
    name: 'AnalysisScreen',
    beforeRouteEnter: function(to, from, next) {
        next(vm => {
            this.active = true;
            vm.start();
        })
    },
    beforeRouteLeave: function(to, from, next) {
        this.end();
        this.active = false;
        next();
    },
    data: () => ({
        active: false
    }),
    methods: {
        start: function() {
            this.loadBeats();
        },
        end: function() {
            this.removeBeats();
        },
        addBeats: function() {
            getApi('/api/beats')
                .then(data => {
                    let geojson = featureCollection(
                        data.map(x => feature(wellknown(x.wkt), {
                            beat_number: x.beat_number,
                            population: x.population
                        }))
                    );

                    let geojsonLayer = new 

                    EventBus.$emit('add-source', {
                        sourceName: 'beats',
                        sourceOptions: {
                            type: 'geojson',
                            data: dataGeojson
                        }
                    });

                    EventBus.$emit('add-layer', [{
                        id: 'beats-shape',
                        type: 'fill',
                        source: 'beats',
                        paint: {
                            'fill-color':
                            [
                                'interpolate',
                                ['linear'],
                                ['get', 'population'],
                                0, '#fff',
                                27000, '#f00'
                            ],
                            'fill-opacity': 0.5
                        }
                    }, 'waterway-label']);

                    EventBus.$emit('add-layer', [{
                        id: 'beats-outline',
                        type: 'line',
                        source: 'beats',
                        paint: {
                            'line-color': '#222',
                            'line-width': 2 
                        }
                    }, 'waterway-label']);
                });
        },
        removeBeats: function() {
            EventBus.$emit('remove-layer', 'beats-shape');
            EventBus.$emit('remove-layer', 'beats-outline');
            EventBus.$emit('remove-source', 'beats');
        }
        
    }
}
</script>

<style scoped>
        .analysis-screen {
        color: white;
    }
</style>
