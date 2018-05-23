<template>
    <div class="screen overview-screen">
        <div class="sidepanel">
            <div class="sidepanel-section">
                <label for="yearInput">Year: {{year}}</label>
                <b-form-input id="yearInput" type="range" v-model="year" :min="minYear" :max="maxYear" step="1" @input="_onYearSliderInput"></b-form-input>
                <br />
                <div>
                    <label for="crimeTypeInput">Crime category:</label>
                    <b-form-select id="crimeTypeInput" v-model="crimeType" @input="onCrimeInputChange" :options="crimeOptions"></b-form-select>
                </div>
                <div>
                    <b-form-checkbox variant="warning" v-model="normaliseGlobal" @input="onCrimeInputChange">Normalise globally</b-form-checkbox>
                </div>
            </div>
        
            <!-- <br />
            <label><input v-model="normaliseGlobal" type="checkbox" @input="onCrimeInputChange">Normalise globally</label>
            <br /> -->
            <transition name="fade">
                <div class="sidepanel-section" v-if="tooltipText" v-html="tooltipText">
                </div>
            </transition>
        </div>
    </div>
</template>

<script>
import Vue from 'vue';
import vueSlider from 'vue-slider-component';
import { HexagonLayer } from '@deck.gl/core';
import wellknown from 'wellknown';
// import tag from '@turf/tag';
import {point, feature, featureCollection} from '@turf/helpers';
import work from 'webworkify-webpack';

import {getApi, chicagoCenter, hexToDeckColor, getStyle, interpolateArr} from '../utils';
import { EventBus } from '../event-bus';

var datasets = {
    crimes: {},
    hexCommunityAreas: {}
};
var downloading = {
    crimes: {}
}
var processing = {
    hexCommunityAreas: {}
};

let communityAreas = null;

function getCrimesKey(year, type){
    return ''+year+'|'+ (type || 'All');
}

export default {
    name: 'OverviewScreen',
    components: {},
    data: () => ({
        year: 2017,
        minYear: 2001,
        maxYear: 2017,
        crimeType: 'All',
        crimeTypes: [],
        crimeOptions: ['All'],
        tooltipText: '',
        normaliseGlobal: true,
        active: false
    }),
    created: function() {
        this.style = {};
        this.hexLayer = null;
        this.datasets = datasets;
        this.yearTimeout = null;
        this.active = true;
        this.start();

        EventBus.$on('overview-choose-crime-type', this.chooseCrimeType);
        EventBus.$on('overview-choose-year', this.chooseYear);
    },
    beforeRouteLeave: function(to, from, next) {
        this.active = false;
        this.end();
        next();
    },
    watch: {
        crimeTypes: function(newTypes, oldTypes) {
            console.log('update options');
            this.crimeOptions = [{value: 'All', text: 'All'}, ...newTypes.map(x => ({value: x.code, text: x.type}))];
        }
    },
    methods: {
        start: function() {
            var vm = this;
            getStyle().then(data => {
                vm.style = data;
                Vue.nextTick(() => {
                    this.loadCrimeTypes();
                    this.loadCrimes(this.year, this.crimeType);
                    this.addChicagoOutline();
                    this.loadCommunityOutlines();
                    
                });
            });
        },
        end: function() {
            this.removeHexagons();
            this.removeChicagoOutline();
        },
        chooseYear: function(year) {
            this.year = year;
        },
        chooseCrimeType: function(type) {
            this.crimeType = type;
        },
        addChicagoOutline: function(){
            getApi('/api/chicago/wkt')
                .then(data => {
                    console.log('wkt', data);
                    let geojson = wellknown(data[0].wkt);
                    console.log('geojson', geojson);

                    let outlineSource = {
                        type: 'geojson',
                        data: geojson
                    };
                    let outline = {
                        id: 'chicago-outline',
                        type: 'line',
                        source: 'chicago-outline',
                        paint: {
                            'line-color': this.style['overview-chicago-outline-color'],
                            'line-width': 2
                        }
                    };

                    if(this.active) {
                        EventBus.$emit('add-source', {
                            sourceName: 'chicago-outline',
                            sourceOptions: outlineSource
                        });
                        EventBus.$emit('add-layer', [outline, 'waterway-label']);
                    }
                });
        },
        removeChicagoOutline: function() {
            EventBus.$emit('remove-layer', 'chicago-outline');
            EventBus.$emit('remove-source', 'chicago-outline');
        },
        loadCommunityOutlines: function() {
            getApi('/api/chicago/communities/wkt')
                .then(data => {
                    communityAreas = featureCollection(
                        data.map(c => feature(wellknown(c.wkt), {
                            community: c.community
                        })));
                });
        },
        loadCrimeTypes: function() {
            getApi('/api/crimes/types')
                .then(data => {
                    this.crimeTypes = data;
                    console.log('crime types', data);
                    console.log('Updated crime types');
                });
        },
        onCrimeInputChange: function() {
            Vue.nextTick(() => this.loadCrimes(this.year, this.crimeType));
        },
        loadCrimes: function(year, type){
            let key = getCrimesKey(year, type);

            if(datasets.crimes[key]) {
                this.updateHexagons();
                return;
            }
            if(downloading.crimes[key]) return;
            let query = `?year=${year}` + ((!type || type == 'All') ? "" : `&type=${type}`);
            downloading.crimes[key] = true;
            getApi(`/api/crimes/coordinates${query}`)
                .then(data => {
                    datasets.crimes[key] = data;
                    downloading.crimes[key] = false;
                    console.log('downloaded crimes data', data);
                    Vue.nextTick(() => this.updateHexagons());
                });
        },
        updateHexagons: function() {
            let key = getCrimesKey(this.year, this.crimeType);
            if(!this.active || !datasets.crimes[key]) return;

            var vm = this;
            let colors = interpolateArr(hexToDeckColor(this.style['overview-bar-color-min']), hexToDeckColor(this.style['overview-bar-color-max']), 20);
            console.log(colors);
            let hexOptions = {
                id: 'crimes-3d',
                data: datasets.crimes[key].filter(x => 
                    x.Longitude && x.Latitude),
                pickable: true,
                extruded: true,
                radius: 200,
                elevationScale: 4,
                colorRange: colors,
                opacity: 0.5,
                autoHighlight: true,
                highlightColor: hexToDeckColor(this.style['overview-bar-highlight-color']),
                getPosition: d => [d.Longitude, d.Latitude],
                onHover: ({object}) => {

                    vm.setTooltip(vm.getTooltipText(object));
                }
            };

            if(this.normaliseGlobal) hexOptions.elevationDomain = [0, 2000];

            this.hexLayer = new HexagonLayer(hexOptions);
            EventBus.$emit('add-deck-layer', this.hexLayer);

            Vue.nextTick(() => this.loadHexCommunityAreas(this.year, this.crimeType));
        },
        loadHexCommunityAreas: function(year, type) {
            let key = getCrimesKey(year, type);
            if(!this.active || datasets.hexCommunityAreas[key]) return;

            if(!this.hexLayer.state){
                console.log('Hex layer state is empty, skipping hexagon calculation');
                return;
            }
            
            let pointCollection = featureCollection(
                this.hexLayer.state.hexagons.map(x => point(x.centroid, {index: x.index}))
            );
            let tagWorker = work(require.resolve('../tag-worker.js'));

            tagWorker.addEventListener('message', event => {
                console.log('worker finished processing for key '+key);
                let matched = event.data;
                datasets.hexCommunityAreas[key] = {};
                for(let match of matched.features){
                    datasets.hexCommunityAreas[key][""+match.properties.index] = match.properties.communityName;
                }
                processing.hexCommunityAreas[key] = false;
            });
            console.log('starting worker process for key '+key)
            processing.hexCommunityAreas[key] = true;
            tagWorker.postMessage([pointCollection, communityAreas, 'community', 'communityName']);
        },
        clearCrimesCache: function() {
            datasets.crimes = {};
        },
        getCommunityArea: function(index) {
            let key = getCrimesKey(this.year, this.crimeType);
            let community = "Loading areas...";
            if(this.datasets.hexCommunityAreas[key]){
                community = this.datasets.hexCommunityAreas[key][""+index];
            }
            return community;
        },
        _onYearSliderInput: function() {
            var year = this.year;
            clearTimeout(this.yearTimeout);

            this.yearTimeout = setTimeout(() => {
                this.loadCrimes(this.year, this.crimeType);
            }, 1000);
        },
        removeHexagons: function(){
            EventBus.$emit('remove-deck-layer', 'crimes-3d');
        },
        getTooltipText: function(hoveredBar) {
            if(!hoveredBar) return "";

            return `<p>Area: ${this.getCommunityArea(hoveredBar.index)} </p> <p> Crimes: ${hoveredBar.points.length}</p>`;
        },
        setTooltip: function(text){
            this.tooltipText = text;
        } 
        
    }
}
</script>

<style scoped>
    /* .overview-screen {
        color: white;
    } */

    .screen-control {
        position: absolute;
        right: 0;
        width: 300px;
    }
</style>
