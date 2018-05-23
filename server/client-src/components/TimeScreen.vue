<template>
    <b-container fluid id="time-background" type="light">
        <div id="time-container">
            <b-row>
                <b-col md="6" offset-md="3">
                    <time-heatmap class="time-map" :types="crimeTypes"></time-heatmap>
                </b-col>
                <b-col md="3">
                    <h1> Each crime type is the result of many different factors. With our grouped data by hour and month,
                    aggregated for 17 years, you can now look in which time periods and seasons it happens.
                    As you can see in the example, Robbery crimes happen earlier at night in winter and significantly
                    later in summer. Overall they mostly happen at night. They follow closely the sunset time and
                    rarely happens between 4 am and 9 am.

                    Try with different types of crimes to see if this pattern changes! </h1>
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

        background-color: white;

    }

    #time-container {
        margin-top: 100px;
    }

    .time-map {
        height: 400px;
    }


</style>
