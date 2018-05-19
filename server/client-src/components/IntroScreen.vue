<template>
    <div class="screen intro-screen">
        <h1>Intro Screen test</h1>
        <router-link to="overview">Go to Overview</router-link>
    </div>
</template>

<script>
import { EventBus } from '../event-bus.js';

let startPoint = { center: [-87.6297, 41.8781], zoom: 13, pitch: 60, bearing: 0 };

export default {
    name: 'IntroScreen',
    beforeRouteEnter: function(to, from, next) {
        next(vm => {
            vm.start();
        })
    },
    beforeRouteLeave: function(to, from, next) {
        this.end();
        next();
    },
    methods: {
        start: function() {

        },

        end: function() {
        }
    }
}
</script>

<style scoped>
    .intro-screen {
        color: white;
    }
</style>
