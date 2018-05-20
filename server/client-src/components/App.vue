<template>
    <div id="app">
        
        <div id="map-container">
            <div id="map"></div>
            <canvas id="deck-canvas" ref='deck'></canvas>
        </div>

        <div id="camera-debug">
            <textarea v-model="viewStateString" readonly ref="camera" cols=30 rows=10>
            </textarea>
            <br />
            <button @click="copyCameraDebug">Copy</button>
        </div>

        <transition name="slide-up">
            <router-view ref="views"></router-view>
        </transition>
    </div>
</template>

<script>
    import Map from '../mapbox';
    import {Deck, GeoJsonLayer, HexagonLayer, MapController} from '@deck.gl/core';
    import { EventBus } from '../event-bus';

    const mapboxToken = "pk.eyJ1IjoibXo4aSIsImEiOiJjamg0d2pxcDMxNXFzMnFwdG52aG81cTc5In0.CksGFWg2x0MiWRShMnYsxQ";
    const initialViewState = {
        longitude: -87.6297982,
        latitude:  41.8781136, // initial map center in [lon,lat]
        zoom: 9,
        bearing: 0,
        pitch: 0
    };

    let mapObj = null;
    let deckgl = null;

    let deckLayers = {};

    export default {
        created: function() {
            EventBus.$on('fly-to', this.flyTo);
            EventBus.$on('add-source', this.addSource);
            EventBus.$on('add-layer', this.addLayer);
            EventBus.$on('remove-layer', this.removeLayer);
            EventBus.$on('remove-source', this.removeSource);
            EventBus.$on('deck-on', this.deckOn);
            EventBus.$on('deck-off', this.deckOff);
            EventBus.$on('add-deck-layer', this.addDeckLayer);
            EventBus.$on('remove-deck-layer', this.removeDeckLayer);
        },
        data: () => ({
            viewState: {}
        }),
        computed: {
            viewStateString: function() {
                return JSON.stringify(this.viewState, null, 2);
            }
        },
        mounted: function() {
            mapObj = new Map({
                mapboxApiAccessToken: mapboxToken,
                container: 'map',
                style: 'mapbox://styles/mz8i/cjh51i78x2p2e2squotdvm06f',
                viewState: initialViewState
            });

            var ignoreNextMove = false;

            var context = this;
            deckgl = new Deck({
                canvas: 'deck-canvas',
                width: '100%',
                height: '100%',
                viewState: initialViewState,
                controller: MapController,
                onViewportChange: viewState => {
                    ignoreNextMove = true;
                    deckgl.setProps({viewState});
                    // if(!viewState.stopPropagation) {
                        mapObj.setProps({viewState});
                    // }
                    context.setViewState(viewState);
                }
            });

            mapObj._map.on('move', e => {
                if(!ignoreNextMove) {
                    const {lng, lat} = e.target.getCenter();

                    let viewState = {
                        longitude: lng,
                        latitude: lat,
                        zoom: e.target.getZoom(),
                        bearing: e.target.getBearing(),
                        pitch: e.target.getPitch()
                    }
                    deckgl.setProps({viewState});
                }
                ignoreNextMove = false;
            });

            this.$refs.deck.addEventListener('contextmenu', e => e.preventDefault());

            EventBus.$emit('map-loaded');
        },
        methods: {
            setViewState: function(viewState) {
                const {longitude, latitude, zoom, bearing, pitch} = viewState;
                this.viewState = {
                    longitude, latitude, zoom, bearing, pitch
                };
            },
            copyCameraDebug: function() {
                this.$refs.camera.select();
                document.execCommand('copy');
            },
            flyTo: function(flyOptions){
                if(mapObj) {
                    mapObj._map.flyTo(flyOptions);
                }
            },
            addSource: function(sourceParams) {
                const {sourceName, sourceOptions} = sourceParams;
                console.log('Adding source to map');

                mapObj._map.addSource(sourceName, sourceOptions);
            },
            addLayer: function(layerParams) {
                const [layerOptions, beforeLayer] = layerParams;
                console.log('Adding layer to map');
                console.log(layerOptions);
                mapObj._map.addLayer(layerOptions, beforeLayer);
            },

            removeLayer: function(id) {
                mapObj._map.removeLayer(id);
            },
            
            removeSource: function(id) {
                mapObj._map.removeSource(id);
            },

            deckOn: function(){
                document.getElementById('deckgl-overlay').style.display = 'block';
            },

            deckOff: function() {
                 document.getElementById('deckgl-overlay').style.display = 'none';
            },

            addDeckLayer: function(layer) {
                deckLayers[layer.id] = layer;
                this.updateDeckLayers();
            },
            removeDeckLayer: function(id) {
                delete deckLayers[id];
                this.updateDeckLayers();
            },

            updateDeckLayers: function() {
                let layers = Object.values(deckLayers);
                deckgl.setProps({layers});
            },

            addChicagoOutline: function() {
                
            }
        }
    }
</script>

<style scoped>
    #map-container {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
    }

    #map-container > * {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
    }

    #camera-debug {
        background-color: rgba(100, 100, 100, 0.5);
        width: 250px;
        height: 200px;
        position: absolute;
        bottom: 2px;
        right: 2px;
    }
</style>
