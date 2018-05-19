<template>
    <div class="screen analysis-screen">
        <h1>Analysis Screen test</h1>
        <router-link to="intro">Go to Intro</router-link>
    </div>
</template>

<script>

import parse from 'wellknown';

import { EventBus } from '../event-bus.js';


let startPoint = { center: [-87.9074, 41.9742], zoom: 13, pitch: 0, bearing: 0 };

export default {
    name: 'AnalysisScreen',
    beforeRouteEnter: function(to, from, next) {
        next(vm => {
            vm.start();
        })
    },
    beforeRouteLeave: function(to, from, next) {
        this.end();
        next();
    },
    mounted: function() {
        console.log('Analysis screen mounted');
    },
    methods: {
        start: function() {
            EventBus.$emit('fly-to', startPoint);

            fetch('/api/beats')
                .then(response => response.json())
                .then(data => {
                    //let dataGeojson = GeoJSON.parse(data, {Point: ['Latitude', 'Longitude']});

                    let dataGeojson = {
                        type: 'FeatureCollection',
                        features: data.map(function(x){
                            return {
                                type: 'Feature',
                                geometry: parse(x.wkt),
                                properties: {
                                    beat_number: x.beat_num,
                                    population: x['TOTAL POPULATION']
                                }
                            }
                        })
                    };

                    EventBus.$emit('add-source', {
                        sourceName: 'beats',
                        sourceOptions: {
                            type: 'geojson',
                            data: dataGeojson
                        }
                    });

                    EventBus.$emit('add-layer', [{
                        "id": 'beats-shape',
                        "type": 'fill',
                        "source": 'beats',
                        "paint": {
                            'fill-color': //'#e00',
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
                        "id": 'beats-outline',
                        "type": 'line',
                        "source": 'beats',
                        "paint": {
                            'line-color': '#222',
                            'line-width': 2 
                        }
                    }, 'waterway-label']);
                });
        },
        end: function() {
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
