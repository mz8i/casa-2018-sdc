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
import mapStore from '../map-communication';


let datasets = {};

let startPoint = { center: [-87.9074, 41.9742], zoom: 13, pitch: 0, bearing: 0 };

export default {
    name: 'AnalysisScreen',
    // beforeRouteEnter: function(to, from, next) {
    //     next(vm => {
    //         vm.active = true;
    //         vm.start();
    //     })
    // },
    beforeRouteLeave: function(to, from, next) {
        this.end();
        this.active = false;
        next();
    },
    created: function() {
        this.stopsLayer = null;
        this.routesLayer = null;

        this.active = true;
        this.start();
    },
    data: () => ({
        active: false,
        displayTransport: true,
        hoveredBeat: null,
        selectedBeat: null
    }),
    methods: {
        start: function() {
            EventBus.$on('analysis-select-beat', this.selectBeat);

            Vue.nextTick(() => {
                this.loadBeats();
                this.loadRoutes();
                this.loadStops();
            });
        },
        end: function() {
            this.removeBeats();
            this.removeStops();
            this.removeRoutes();
        },
        selectBeat: function(beatNumber) {
            if(beatNumber) {
                if(this.selectedBeat == beatNumber) {
                    this.setBeatSelection(null);
                } else {
                    this.setBeatSelection(beatNumber);
                }
            }
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
            if(datasets.beats){
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

                    datasets.beats = geojson;

                    Vue.nextTick(() => {
                        this.updateBeats();
                    });
                });
        },
        updateBeats: function() {
            if(!this.active || !datasets.beats) return;

            EventBus.$emit('add-source', {
                sourceName: 'beats',
                sourceOptions: {
                    type: 'geojson',
                    data: datasets.beats
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

            EventBus.$emit('add-layer', [{
                id: 'beats-selection-outline',
                type: 'line',
                source: 'beats',
                paint: {
                    'line-color': '#fff',
                    'line-width': 4
                },
                filter: ["==", "beat_number", ""]
            }, 'waterway-label']);

            EventBus.$emit('add-layer', [{
                id: 'beats-hover-outline',
                type: 'line',
                source: 'beats',
                paint: {
                    'line-color': '#fff',
                    'line-width': 2
                },
                filter: ["==", "beat_number", ""]
            }, 'waterway-label']);

            var vm = this;
            let transparentLayer = new GeoJsonLayer({
                id: 'beats-picker',
                pickable: true,
                data: datasets.beats,
                extruded: false,
                stroked: false,
                filled: true,
                getFillColor: x => [255, 255, 255, 0],
                onHover: ({object}) => vm.onBeatHover(object),
                onClick: ({object}) => vm.selectBeat(object && object.properties.beat_number)
            });

            EventBus.$emit('add-deck-layer', transparentLayer);
        },
        onBeatHover: function(o) {
            if(o) {
                if(!this.hoveredBeat || o.properties.beat_number != this.hoveredBeat) {
                    this.setBeatHoverFilter(o.properties.beat_number);
                }
            } else if(this.hoveredBeat){
                this.setBeatHoverFilter(null);
            }
        },
        setBeatHoverFilter: function(beatNumber) {
            console.log('sent hover event');

            // mapStore.mapFilters['beats-hover-outline'] = ["==", "beat_number", beat_number || ""];

            this.hoveredBeat = beatNumber;
        },
        setBeatSelection: function(beatNumber) {
            EventBus.$emit('map-filter', ['beats-selection-outline', ['==', 'beat_number', beatNumber || '']]);
            this.selectedBeat = beatNumber;
        },
        removeBeats: function() {
            EventBus.$emit('remove-layer', 'beats-shape');
            EventBus.$emit('remove-layer', 'beats-outline');
            EventBus.$emit('remove-layer', 'beats-hover-outline');
            EventBus.$emit('remove-layer', 'beats-selection-outline');
            
            EventBus.$emit('remove-source', 'beats');
            EventBus.$emit('remove-deck-layer', 'beats-picker');
        },
        loadStops: function(){
            if(datasets.stops){
                this.updateStops();
                return;
            }
            getApi('/api/stops?type=Rail')
                .then(data => {
                    datasets.stops = data;
                    Vue.nextTick(() => {
                        this.updateStops();
                    });
                });
        },
        updateStops: function() {
            if(!this.active || !datasets.stops) return;

            var context = this;

            this.stopsLayer = new IconLayer({
                id: 'stop-icons',
                data: datasets.stops,
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
                getSize: d => 3,
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
            if(datasets.routes){
                this.updateRoutes();
                return;
            }
            getApi('/api/chicago/transit/wkt?type=Metro')
                .then(data => {
                    var context = this;

                    let geojson = featureCollection(
                        data.map(x => feature(wellknown(x.wkt)))
                    );
                    datasets.routes = geojson;

                    Vue.nextTick(() => {
                        this.updateRoutes();
                    })

                });
        },
        updateRoutes: function() {
            if(!this.active || !datasets.routes) return;

            var context = this;
            this.routesLayer = new GeoJsonLayer({
                id: 'routes',
                data: datasets.routes,
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
