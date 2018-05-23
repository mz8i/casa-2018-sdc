<template>
    <div id="app">
        <story-navigation></story-navigation>
        <b-navbar id="navbar" toggleable="md" :type="bgType" class="bg-transparent">
            <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>
            <b-collapse is-nav id="nav_collapse">
                <b-navbar-nav class="ml-auto">
                    <b-nav-item right to="/">Introduction</b-nav-item>
                    <b-nav-item right to="overview">Overview</b-nav-item>
                    <b-nav-item right to="time">Temporal</b-nav-item>
                    <b-nav-item right to="analysis">Analysis</b-nav-item>
                </b-navbar-nav>
            </b-collapse>
        </b-navbar>
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
    import StoryNavigation from './StoryNavigation.vue';
    import { EventBus } from '../event-bus';
    import { clamp } from '../utils';
    import mapStore from '../map-communication';

    const mapboxToken = 'pk.eyJ1IjoianVsaWFuaG9mZm1hbm5hbnRvbiIsImEiOiJjamhlcHM2a2Iwd3d2M2RxdnBzbmY5bm5qIn0.PL5CUOX7N6PVtFt838hZsg';//"pk.eyJ1IjoibXo4aSIsImEiOiJjamg0d2pxcDMxNXFzMnFwdG52aG81cTc5In0.CksGFWg2x0MiWRShMnYsxQ";
    const initialViewState = {
        longitude: -87.6297982,
        latitude:  41.8781136, // initial map center in [lon,lat]
        zoom: 10,
        bearing: 0,
        pitch: 0
    };

    let routeOrder = ['/', '/overview', '/time', '/analysis'];

    let mapObj = null;
    let deckgl = null;

    let deckLayers = {};

    export default {
        name: 'App',
        components: {StoryNavigation},
        created: function() {
            this.mapFilters = {};


            EventBus.$on('fly-to', this.flyTo);
            EventBus.$on('jump-to', this.jumpTo);
            EventBus.$on('add-source', this.addSource);
            EventBus.$on('add-layer', this.addLayer);
            EventBus.$on('remove-layer', this.removeLayer);
            EventBus.$on('remove-source', this.removeSource);
            EventBus.$on('deck-on', this.deckOn);
            EventBus.$on('deck-off', this.deckOff);
            EventBus.$on('add-deck-layer', this.addDeckLayer);
            EventBus.$on('remove-deck-layer', this.removeDeckLayer);
            EventBus.$on('map-filter', this.mapFilter);
        },
        data: () => ({
            viewState: {},
            transitionName: 'slide-up',
            minZoom: 10,
            maxZoom: 15,
            minLat: 41.5,
            maxLat: 42.1,
            minLon: -88,
            maxLon: -87.3,
            bgType: 'dark'
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
                this.bgType = to.meta.style;
            }
        },
        mounted: function() {
            mapObj = new Map({
                mapboxApiAccessToken: mapboxToken,
                container: 'map',
                style: 'mapbox://styles/julianhoffmannanton/cjhhmqpsj5t6y2smi6zx69rkn',//'mapbox://styles/mz8i/cjh51i78x2p2e2squotdvm06f',
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

            requestAnimationFrame(this.updateAnimation);
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
            jumpTo: function(jumpOptions){
                if(mapObj) {
                    mapObj._map.jumpTo(jumpOptions);
                }
            },
            addSource: function(sourceParams) {
                const {sourceName, sourceOptions} = sourceParams;
                mapObj._map.addSource(sourceName, sourceOptions);
            },
            addLayer: function(layerParams) {
                const [layerOptions, beforeLayer] = layerParams;
                try{
                    mapObj._map.addLayer(layerOptions, beforeLayer);
                } catch(error) {
                    mapObj._map.removeLayer(layerOptions.id);
                    mapObj._map.addLayer(layerOptions, beforeLayer);
                }
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

            mapFilter: function(filterParams) {
                const [layerId, condition] = filterParams;
                mapObj._map.setFilter(layerId, condition);
                this.mapFilters[layerId] = condition;
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

            updateAnimation: function() {
                requestAnimationFrame(this.updateAnimation);

                for(const [key, value] of  Object.entries(mapStore.mapFilters)) {
                    mapObj._map.setFilter(key, value);
                }
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
