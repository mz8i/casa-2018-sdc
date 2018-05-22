<template>
    <div class="screen analysis-screen">
        <h1>Analysis Screen test</h1>
        <router-link to="intro">Go to Intro</router-link>
        <br />
        <b-form-checkbox v-model="displayTransport" @change="updateLayerVisibility" >Transport</b-form-checkbox>
    </div>
</template>

<script>

import Vue from 'vue';
import {GeoJsonLayer, IconLayer} from '@deck.gl/core';

import {feature, featureCollection} from '@turf/helpers';
import wellknown from 'wellknown';

import {getApi} from '../utils';
import { EventBus } from '../event-bus';


let startPoint = { center: [-87.9074, 41.9742], zoom: 13, pitch: 0, bearing: 0 };

export default {
    name: 'AnalysisScreen',
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
        this.stopsLayer = null;
        this.routesLayer = null;
        this.datasets = {};
        console.log('created');
    },
    data: () => ({
        active: false,
        displayTransport: true
    }),
    methods: {
        start: function() {
            this.loadBeats();
            this.loadRoutes();
            this.loadStops();
        },
        end: function() {
            this.removeBeats();
            this.removeStops();
            this.removeRoutes();
        },
        updateLayerVisibility: function(){
            Vue.nextTick(() => {
                console.log('updating layer visibility')
                this.updateStops();
                this.updateRoutes();
            });
            // if(this.routesLayer){
            //     this.routesLayer.visibile = this.displayTransport;
            // }
        },
        loadBeats: function() {
            if(this.datasets.beats){
                this.updateBeats();
                return;
            }
            getApi('/api/beats')
                .then(data => {
                    let geojson = featureCollection(
                        data.map(x => feature(wellknown(x.wkt), {
                            beat_number: x.beat_number,
                            population: x.population
                        }))
                    );

                    this.datasets.beats = geojson;

                    Vue.nextTick(() => {
                        this.updateBeats();
                    });
                });
        },
        updateBeats: function() {
            if(!this.active || !this.datasets.beats) return;

            EventBus.$emit('add-source', {
                sourceName: 'beats',
                sourceOptions: {
                    type: 'geojson',
                    data: this.datasets.beats
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
        },
        removeBeats: function() {
            EventBus.$emit('remove-layer', 'beats-shape');
            EventBus.$emit('remove-layer', 'beats-outline');
            EventBus.$emit('remove-source', 'beats');
        },
        loadStops: function(){
            if(this.datasets.stops){
                this.updateStops();
                return;
            }
            getApi('/api/stops?type=Rail')
                .then(data => {
                    this.datasets.stops = data;
                    Vue.nextTick(() => {
                        this.updateStops();
                    });
                });
        },
        updateStops: function() {
            if(!this.active || !this.datasets.stops) return;

            var context = this;

            this.stopsLayer = new IconLayer({
                id: 'stop-icons',
                data: this.datasets.stops,
                visible: this.displayTransport,
                pickable: true,
                iconAtlas: 'static/images/icon-atlas.png',
                iconMapping: {
                    rail: {
                        x: 0,
                        y: 0,
                        width: 128,
                        height: 128,
                        anchorY: 128,
                        mask: true
                    }, 
                    bus: {
                        x: 128,
                        y: 0,
                        width: 128,
                        height: 128,
                        anchorY: 128,
                        mask: true
                    }, 
                },
                sizeScale: 15,
                getPosition: d => [d.lon, d.lat],
                getIcon: d => d.type.toLowerCase(),
                getSize: d => 5,
                getColor: d => [255, 255, 255, 255],
                getVisible: d => context.displayTransport
                //onHover: ({object}) => setTooltip(`${object.name}\n${object.address}`)
            });

            EventBus.$emit('add-deck-layer', this.stopsLayer);
        },
        removeStops: function() {
            EventBus.$emit('remove-deck-layer', 'stop-icons');
        },
        loadRoutes: function() {
            if(this.datasets.routes){
                this.updateRoutes();
                return;
            }
            getApi('/api/chicago/transit/wkt?type=Metro')
                .then(data => {
                    var context = this;

                    let geojson = featureCollection(
                        data.map(x => feature(wellknown(x.wkt)))
                    );
                    this.datasets.routes = geojson;

                    Vue.nextTick(() => {
                        this.updateRoutes();
                    })

                });
        },
        updateRoutes: function() {
            if(!this.active || !this.datasets.routes) return;

            var context = this;
            this.routesLayer = new GeoJsonLayer({
                id: 'routes',
                data: this.datasets.routes,
                visible: this.displayTransport,
                pickable: false,
                stroked: true,
                filled: false,
                extruded: false,
                lineWidthScale: 20,
                lineWidthMinPixels: 2,
                // getFillColor: d => [160, 160, 180, 200],
                getLineColor: d => [240, 240, 240, 255],
                // getRadius: d => 100,
                getLineWidth: d => 1,
                getVisible: d => context.displayTransport
                // getElevation: d => 30
            });

            EventBus.$emit('add-deck-layer', this.routesLayer);
        },
        removeRoutes: function() {
            EventBus.$emit('remove-deck-layer', 'routes');
        }
        
    }
}
</script>

<style scoped>
        .analysis-screen {
        color: white;
    }
</style>
