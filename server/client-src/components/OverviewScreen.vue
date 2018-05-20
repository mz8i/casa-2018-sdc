<template>
    <div class="screen overview-screen">
        <h1>Overview Screen test</h1>
        <router-link to="time">Go to Time</router-link>
        <div class="screen-control">
            <input v-model="year" type="range" :min="minYear" :max="maxYear" step="1" @input="_onYearSliderInput" >
            {{year}}
            <br />
            <select v-model="crimeType" @input="updateHexagons">
                <option value="All">All</option>
                <option v-for="ct in crimeTypes" :key="ct.code" :value="ct.code"> {{ct.type}} </option>
            </select>
            <br />
            <label><input v-model="normaliseGlobal" type="checkbox" @input="updateHexagons">Normalise globally</label>
            <br />
            <span v-html="tooltipText"></span>
        </div>
    </div>
</template>

<script>
import Vue from 'vue';
import vueSlider from 'vue-slider-component';
import { HexagonLayer } from '@deck.gl/core';
import wellknown from 'wellknown';
import tag from '@turf/tag';
import {point, feature, featureCollection} from '@turf/helpers';

import {getApi, chicagoCenter} from '../utils';
import { EventBus } from '../event-bus';

let crimesCache = {};
let communityAreas = null;
let hexCommunityMatches = null;

export default {
    name: 'OverviewScreen',
    data: () => ({
        year: 2017,
        minYear: 2001,
        maxYear: 2017,
        crimeType: 'All',
        crimeTypes: [],
        tooltipText: '',
        normaliseGlobal: true,
        active: false
    }),
    beforeRouteEnter: function(to, from, next) {
        next(vm => {
            vm.active = true;
            vm.start();
        })
    },
    beforeRouteLeave: function(to, from, next) {
        this.active = false;
        this.end();
        next();
    },
    methods: {
        start: function() {
            this.loadCrimeTypes();

            this.updateHexagons();
            this.addChicagoOutline();
            this.loadCommunityOutlines();

            EventBus.$emit('deck-on');
        },
        end: function() {
            EventBus.$emit('deck-off');
            this.removeHexagons();
            this.removeChicagoOutline();
        },
        addChicagoOutline: function(){
            getApi('/api/chicago/wkt')
                .then(data => {
                    console.log('wkt', data);
                    let geojson = wellknown(data[0].wkt);
                    console.log('geojson', geojson);
                    let outline = {
                        id: 'chicago-outline',
                        type: 'line',
                        source: {
                            type: 'geojson',
                            data: geojson
                        },
                        paint: {
                            'line-color': '#eee',
                            'line-width': 2
                        }
                    };

                    if(this.active) EventBus.$emit('add-layer', [outline, 'waterway-label']);
                });
        },
        removeChicagoOutline: function() {
            EventBus.$emit('remove-layer', 'chicago-outline');
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
        getCrimesData: function(year, type){
            if(!type) type = 'All';
            console.log([year, type]);
            var key = ''+year+'|'+type;

            console.log(key);
            if(key in crimesCache) {
                return Promise.resolve(crimesCache[key]);
            } else {
                let query = `?year=${year}` + (type == 'All' ? "" : `&type=${type}`);
                return getApi(`/api/crimes/coordinates${query}`)
                    .then(data => {
                        crimesCache[key] = data;
                        return data;
                    });
            }
        },
        clearCrimesDataCache: function() {
            crimesCache = {};
        },
        getCommunityArea: function(index) {
            let community = "";
            if(hexCommunityMatches){
                community = hexCommunityMatches[String(index)];
            }
            return community;
        },
        _onYearSliderInput: function() {
            var year = this.year;
            setTimeout(() => {
                if(this.year == year) this.updateHexagons();
            }, 1000);
        },
        updateHexagons: function() {
            var context = this;
            Vue.nextTick(function(){
                context.getCrimesData(context.year, context.crimeType)
                .then(data => {
                    context.removeHexagons();
                    context.addHexagons(data);
                });
            });
        },
        addHexagons: function(data) {
            var context = this;
            let hexOptions = {
                id: 'crimes-3d',
                data: data.filter(x => x.Longitude && x.Latitude),
                pickable: true,
                extruded: true,
                radius: 200,
                elevationScale: 4,
                opacity: 0.5,
                getPosition: d => [d.Longitude, d.Latitude],
                onHover: ({object}) => context.setTooltip(context.getTooltipText(object))
            };

            if(this.normaliseGlobal) hexOptions.elevationDomain = [0, 2000];

            var hexLayer = new HexagonLayer(hexOptions);

            Vue.nextTick(function() {
                if(!hexLayer.state){
                    console.log('Hex layer state is empty, skipping hexagon calculation');
                    return;
                }
                
                let pointCollection = featureCollection(
                    hexLayer.state.hexagons.map(x => point(x.centroid, {index: x.index}))
                );
                console.log(pointCollection);
                console.log(communityAreas);
                let matched = tag(pointCollection, communityAreas, 'community', 'communityName');
                console.log(matched);
                hexCommunityMatches = {};

                for(let match of matched.features){
                    hexCommunityMatches[""+match.properties.index] = match.properties.communityName;
                }
            });

            if(context.active) EventBus.$emit('add-deck-layer', hexLayer);
        },
        removeHexagons: function(){
            EventBus.$emit('remove-deck-layer', 'crimes-3d');
            hexCommunityMatches = null;
        },
        getTooltipText: function(hoveredBar) {
            if(!hoveredBar) return "";

            return `${this.getCommunityArea(hoveredBar.index)} \n Count: ${hoveredBar.points.length}`;
        },
        setTooltip: function(text){
            this.tooltipText = text;
        } 
        
    }
}
</script>

<style scoped>
    .overview-screen {
        color: white;
    }

    .screen-control {
        position: absolute;
        right: 0;
        width: 300px;
    }
</style>
