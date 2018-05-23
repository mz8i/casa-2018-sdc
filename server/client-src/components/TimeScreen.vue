<template>
    <b-container fluid id="time-background" type="light">
        <div id="time-container">
            <b-row>
                <b-col md="6" offset-md="3">
                    <time-heatmap class="time-map" :types="crimeTypes"></time-heatmap>
                </b-col>
                <b-col md="3" class="sidepanel">
                    <div class="sidepanel-container">
                        <h5>Some text here</h5>
                    </div>
                </b-col>
            </b-row>
        </div>
    </b-container>
</template>

<script>

import {getApi} from '../utils';
import TimeHeatmap from './TimeHeatmap.vue';

export default {
    name: 'TimeScreen',
    components: {TimeHeatmap},
    beforeRouteLeave: function(to, from, next) {
        this.end();
        next();
    },
    created: function() {
        this.start();
    },
    data: () => ({
        crimeTypes: []
    }),
    methods: {
        start: function() {
            var vm = this;
            getApi('/api/crimes/types')
                .then(data => {
                    vm.crimeTypes = data.map(d => ({value: d.code, text: d.type}));
                });
        },

        end: function() {
        }
    }
}
</script>

<style scoped>
    #time-background {
        position: absolute;
        top: 0;
        bottom: 0;
        left: 0;
        right: 0;

        background-color: whitesmoke;

    }

    #time-container {
        margin-top: 100px;
    }

    .time-map {
        height: 400px;
    }


</style>
