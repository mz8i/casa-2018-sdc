<template>
    <div id="app">
        
        <mapbox ref="map"
            access-token="pk.eyJ1IjoibXo4aSIsImEiOiJjamg0d2pxcDMxNXFzMnFwdG52aG81cTc5In0.CksGFWg2x0MiWRShMnYsxQ"
            :map-options="{
                 style: 'mapbox://styles/mz8i/cjh51i78x2p2e2squotdvm06f',
                 center: [-87.6297982, 41.8781136], // initial map center in [lon,lat]
                 zoom: 12
            }">
        </mapbox>

        <transition name="slide">
            <router-view ref="views"></router-view>
        </transition>
    </div>
</template>

<script>
    import Mapbox from 'mapbox-gl-vue';

    export default {
        components: { Mapbox }
    }
</script>