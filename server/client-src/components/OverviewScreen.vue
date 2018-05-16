<template>
    <div class="screen overview-screen">
        <h1>Overview Screen test</h1>
        <router-link to="intro">Go to Intro</router-link>
    </div>
</template>

<script>

import { EventBus } from '../event-bus.js';

let startPoint = { center: [-87.9074, 41.9742], zoom: 13, pitch: 0 };

export default {
    name: 'OverviewScreen',
    beforeRouteEnter: function(to, from, next) {
        next(vm => {
            vm.start();
        })
    },
    methods: {
        start: function() {
            EventBus.$emit('fly-to', startPoint);
        }
    }
}
</script>

<style scoped>
    .overview-screen {
        color: white;
    }
</style>
