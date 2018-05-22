<template>
    <div id='time-background'>
        <h1>Time Analysis</h1>
        <router-link to="analysis">Go to Analysis</router-link>
    </div>
</template>

<script>
export default {
    name: 'TimeScreen',
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
    #time-background {
        position: absolute;
        top: 0;
        bottom: 0;
        left: 0;
        right: 0;

        background-color: white;

        color: '#111';
    }
</style>
