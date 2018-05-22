<template>
    <div id="app">
        <b-navbar id="navbar" toggleable="md" type="dark" variant="crime">
            <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>
            <b-collapse is-nav id="nav_collapse">
                <b-navbar-nav class="ml-auto">
                    <b-nav-item right to="intro">Introduction</b-nav-item>
                    <b-nav-item right to="overview">Overview</b-nav-item>
                    <b-nav-item right to="time">Temporal</b-nav-item>
                    <b-nav-item right to="analysis">Analysis</b-nav-item>
                </b-navbar-nav>
            </b-collapse>
        </b-navbar>
        <!-- <div class="navbar">
            <div class="navbar-container">
                <router-link to="intro">Introduction</router-link>
                <router-link to="overview">Overview</router-link>
                <router-link to="time">Temporal</router-link>
                <router-link to="analysis">Analysis</router-link>
            </div>         
        </div> -->
        <div id="map-container">
            <div id="map"></div>
            <canvas id="deck-canvas" ref='deck'></canvas>
        </div>

        <div id="camera-debug">
            <textarea v-model="viewStateString" readonly ref="camera" cols=30 rows=10>
            </textarea>
            <button @click="copyCameraDebug">Copy</button>
        </div>

        <transition :name="transitionName">
            <router-view ref="views"></router-view>
        </transition>
    </div>
</template>

<script>
    import {Deck, GeoJsonLayer, HexagonLayer, MapController} from '@deck.gl/core';

    import Map from '../mapbox';
    import { EventBus } from '../event-bus';
    import { clamp } from '../utils';

    const mapboxToken = "pk.eyJ1IjoibXo4aSIsImEiOiJjamg0d2pxcDMxNXFzMnFwdG52aG81cTc5In0.CksGFWg2x0MiWRShMnYsxQ";
    const initialViewState = {
        longitude: -87.6297982,
        latitude:  41.8781136, // initial map center in [lon,lat]
        zoom: 10,
        bearing: 0,
        pitch: 0
    };

    let routeOrder = ['/intro', '/overview', '/time', '/analysis'];

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
            viewState: {},
            transitionName: 'slide-up',
            minZoom: 10,
            maxZoom: 17,
            minLat: 41.5,
            maxLat: 42.1,
            minLon: -88,
            maxLon: -87.3
        }),
        computed: {
            viewStateString: function() {
                return JSON.stringify(this.viewState, null, 2);
            }
        },
        watch: {
            '$route' (to, from) {
                let toOrder = routeOrder.indexOf(to.path);
                let fromOrder = routeOrder.indexOf(from.path);
                this.transitionName = fromOrder < toOrder ? 'slide-up' : 'slide-down';
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

            var vm = this;
            deckgl = new Deck({
                canvas: 'deck-canvas',
                width: '100%',
                height: '100%',
                viewState: initialViewState,
                controller: MapController,
                onViewportChange: viewState => {
                    const {maxZoom, minZoom, minLat, maxLat, minLon, maxLon} = vm;

                    if(viewState.zoom < minZoom) return;
                    viewState.latitude = clamp(viewState.latitude, minLat, maxLat);
                    viewState.longitude = clamp(viewState.longitude, minLon, maxLon);
                    viewState.zoom = clamp(viewState.zoom, minZoom, maxZoom);

                    // this is to avoid an infinite event loop and at the same time allow map.flyTo sync
                    ignoreNextMove = true;
                    

                    deckgl.setProps({viewState});
                    mapObj.setProps({viewState});
                    vm.setViewState(viewState);
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

            mapObj._map.on('style.load', () => EventBus.$emit('map-loaded'));
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
                mapObj._map.addSource(sourceName, sourceOptions);
            },
            addLayer: function(layerParams) {
                const [layerOptions, beforeLayer] = layerParams;
                mapObj._map.addLayer(layerOptions, beforeLayer);
            },

            removeLayer: function(id) {
                try {
                    mapObj._map.removeLayer(id);
                } catch(err) {
                    console.error(`The layer '${id}' does not exist.`);
                }
            },
            
            removeSource: function(id) {
                try{
                    mapObj._map.removeSource(id);
                } catch(err) {
                    console.error(`The source '${id}' does not exist.`)
                }
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
    .navbar {
        /* position: absolute; */
        z-index: 100;
        /* top:0;
        width: 100%;
        height: 40px; */
    }

    /* .navbar-container {
        float: right;
        width: 200px;
    }

    .navbar-container > * {
        margin-top: 10px;
        margin-bottom: 10px;
        margin-left: 20px;
        margin-right:20px;
    }

    .navbar :after {
        clear: right;
    } */

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
        height: 280px;
        position: absolute;
        bottom: 2px;
        right: 2px;
    }

    #deckgl-overlay {
        cursor: move; /* fallback if grab cursor is unsupported */
        cursor: grab;
        cursor: -moz-grab;
        cursor: -webkit-grab;
    }

 /* (Optional) Apply a "closed-hand" cursor during drag operation. */
    #deckgl-overlay:active { 
        cursor: grabbing;
        cursor: -moz-grabbing;
        cursor: -webkit-grabbing;
    }
</style>
