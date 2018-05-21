<template>
    <div class="screen analysis-screen">
        <h1>Analysis Screen test</h1>
        <router-link to="intro">Go to Intro</router-link>
    </div>
</template>

<script>

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
    data: () => ({
        active: false
    }),
    methods: {
        start: function() {
            this.addBeats();
            this.addTransport();
            EventBus.$emit('deck-on');
        },
        end: function() {
            EventBus.$emit('deck-off');
            this.removeBeats();
            this.removeTransport();
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

                    const beats = new GeoJsonLayer({
                        id: 'beats',
                        data: geojson,
                        pickable: false,
                        stroked: true,
                        filled: true,
                        extruded: false,
                        lineWidthScale: 20,
                        lineWidthMinPixels: 2,
                        getFillColor: d => [160, 160, 180, 200],
                        getLineColor: d => [20, 20, 20, 255],
                        getRadius: d => 100,
                        getLineWidth: d => 1,
                        getElevation: d => 30
                    });
                    const outlines = new GeoJsonLayer({
                        id: 'outlines',
                        data: geojson,
                        pickable: false,
                        stroked: true,
                        filled: true,
                        extruded: false,
                        lineWidthScale: 20,
                        lineWidthMinPixels: 2,
                        getFillColor: d => [160, 160, 180, 200],
                        getLineColor: d => [20, 20, 20, 255],
                        getRadius: d => 100,
                        getLineWidth: d => 1,
                        getElevation: d => 30
                    });

                    // EventBus.$emit('add-deck-layer', layer);
                    EventBus.$emit('add-deck-layer', beats);

                    // EventBus.$emit('add-source', {
                    //     sourceName: 'beats',
                    //     sourceOptions: {
                    //         type: 'geojson',
                    //         data: dataGeojson
                    //     }
                    // });

                    // EventBus.$emit('add-layer', [{
                    //     id: 'beats-shape',
                    //     type: 'fill',
                    //     source: 'beats',
                    //     paint: {
                    //         'fill-color':
                    //         [
                    //             'interpolate',
                    //             ['linear'],
                    //             ['get', 'population'],
                    //             0, '#fff',
                    //             27000, '#f00'
                    //         ],
                    //         'fill-opacity': 0.5
                    //     }
                    // }, 'waterway-label']);

                    // EventBus.$emit('add-layer', [{
                    //     id: 'beats-outline',
                    //     type: 'line',
                    //     source: 'beats',
                    //     paint: {
                    //         'line-color': '#222',
                    //         'line-width': 2 
                    //     }
                    // }, 'waterway-label']);
                });
        },
        removeBeats: function() {
            // EventBus.$emit('remove-deck-layer', 'beats');
            EventBus.$emit('remove-deck-layer', 'beats');
            // EventBus.$emit('remove-layer', 'beats-shape');
            // EventBus.$emit('remove-layer', 'beats-outline');
            // EventBus.$emit('remove-source', 'beats');
        },
        addTransport: function() {
            getApi('/api/stops')
                .then(data => {
                    // let geo = featureCollection(data.map(x => point([x.lon, x.lat], {
                    //     beat: x.beat,
                    //     type: x.type,
                    //     name: x.name
                    // })));

                    const layer = new IconLayer({
                        id: 'stop-icons',
                        data: data.filter(x => x.type =='Rail'),
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
                        getColor: d => [255, 255, 255, 255]
                        //onHover: ({object}) => setTooltip(`${object.name}\n${object.address}`)
                    });

                    EventBus.$emit('add-deck-layer', layer);
                })
        },
        removeTransport: function() {
            EventBus.$emit('remove-deck-layer', 'stop-icons');
        }
        
    }
}
</script>

<style scoped>
        .analysis-screen {
        color: white;
    }
</style>
