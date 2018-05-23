<template>
    <div id="story" class="" role="tablist">
        <div id="hamburger">
            <b-btn class="glyphicon glyphicon-menu-hamburger" @click="onHamburgerClick">S</b-btn>
        </div>
        <b-card no-body class="mb-1">
            <!-- <b-card-header header-tag="header" class="p-1" role="tab"> -->
                <h5 v-b-toggle.accordion-intro> Introduction </h5>
            <!-- </b-card-header> -->
            <b-collapse id="accordion-intro" visible accordion="story-accordion" role="tabpanel">
                <b-card-body>
                    <p class="card-text">
                        Some story introduction here
                    </p>
                    <p class="card-text">
                        More story introduction here
                    </p>
                    <a href="#" v-b-toggle.accordion-overview variant="info">Go to overview</a>
                </b-card-body>

            </b-collapse>
        </b-card>

        <b-card no-body class="mb-1">
            <h5 v-b-toggle.accordion-overview> Overview </h5>
            <b-collapse id="accordion-overview" accordion="story-accordion" role="tabpanel">
                <b-card-body>
                    <p class="card-text">
                        Some overview text here
                    </p>
                    <p class="card-text">
                        More overview text here
                    </p>
                    <p class="card-text">
                        And some more overview text here
                    </p>
                        <a href="#" v-b-toggle.accordion-time variant="info">Go to temporal analysis</a>
                </b-card-body>
            </b-collapse>
        </b-card>

        <b-card no-body class="mb-1">
            <h5 v-b-toggle.accordion-time> Temporal heatmap </h5>
            <b-collapse id="accordion-time" accordion="story-accordion" role="tabpanel">
                <b-card-body>
                    <p class="card-text">
                        Some overview text here

                    </p>
                        <a href="#" v-b-toggle.accordion-analysis variant="info">Go to temporal analysis</a>
                </b-card-body>
            </b-collapse>
        </b-card>

        <b-card no-body class="mb-1">
            <h5 v-b-toggle.accordion-analysis> Analysis </h5>
            <b-collapse id="accordion-analysis" accordion="story-accordion" role="tabpanel">
                <b-card-body>
                    <p class="card-text">
                        Some analysis text here
                    </p>
                        <a href="#" v-b-toggle.accordion-intro variant="info">Go to back to start</a>
                </b-card-body>
            </b-collapse>
        </b-card>
    </div>
</template>

<script>

import { EventBus } from '../event-bus';

export default {
    name: 'StoryNavigation',
    data: () => ({}),
    created: function() {

    },
    methods: {
        onHamburgerClick: function(){
            document.getElementById('story').classList.toggle('collapsed');
        },

    }
}
</script>

<style>
    #story {
        position: absolute;
        top:0;
        bottom:0;
        left: 0;

        transition: left 1s;

        width: 400px;

        background-color: whitesmoke;

        z-index: 1000;
    }

    #story.collapsed {
        left: -400px;
    }

    #story h5 {
        margin: 10px;
        cursor: pointer;
    }



    #hamburger {
        position: absolute;
        top: 40px;
        right: -40px;

        width: 40px;
        height: 40px;
        display: inline-block;
        vertical-align: middle;
        border-top-right-radius: 4px;
        border-bottom-right-radius: 4px;

        background-color: whitesmoke;
    }
</style>
