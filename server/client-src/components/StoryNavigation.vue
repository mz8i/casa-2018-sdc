<template>
    <div id="story" class="" role="tablist">
        <div id="hamburger">
            <b-btn @click="onHamburgerClick">S</b-btn>
        </div>
        <b-card no-body class="mb-1">
            <!-- <b-card-header header-tag="header" class="p-1" role="tab"> -->
                <h5 v-b-toggle.accordion-intro> Introduction </h5>
            <!-- </b-card-header> -->
            <b-collapse id="accordion-intro" visible accordion="story-accordion" role="tabpanel">
                <b-card-body>
                    <p class="card-text">
                        Travel through time and space discovering the crime patterns in Chicago:
                        From the big picture of more than a decade of spatial trends,
                        to the daily distribution of a specific type of crime and through its seasonal evolution.
                    </p>
                    <p class="card-text">
                        How have crime trends in Chicago changed over the last 15 years?
                        What characterizes the spatio-temporal relationships of crimes in Chicago?

                        Go to the Overview to start this journey!
                    </p>
                    <a href="#" @click="goToOverview" v-b-toggle.accordion-overview variant="info">Go to overview</a>
                </b-card-body>

            </b-collapse>
        </b-card>

        <b-card no-body class="mb-1">
            <h5 v-b-toggle.accordion-overview> Overview </h5>
            <b-collapse id="accordion-overview" accordion="story-accordion" role="tabpanel">
                <b-card-body>
                    <p class="card-text">
                        Chicago (Illinois) has witnessed high crime rates for over 50 years
                        and has been deemed as particularly dangerous among big cities in the United States
                        coming to the spotlight due to its violent nature. Explore spatio-temporal patterns
                        through the analysis of over 6.000.000 geo-located crimes in the city.

                    </p>
                    <p class="card-text">
                      Even though crime numbers are descending through the years, a few areas seem to remain as hotspots throughout time.
                      Higher density of delinquency is observed around the middle eastern part of the city (Downtown)####
                      throughout all the years. Moreover, crime seems to accumulate also in the <a href='#' @click="goToMidwesternOverview">midwestern</a>
                      and <a href='#' @click="goToSouthernOverview">southern</a> parts of the city.
                    </p>
                    <p class="card-text">
                      Now, take a look at crimes catalogued as Larceny and then select those classified as Drug Abuse.
                      They show profound differences in their spatial distribution!
                    </p>
                        <a href="#" @click="goToTemporal" v-b-toggle.accordion-time variant="info">Go to temporal analysis</a>
                </b-card-body>
            </b-collapse>
        </b-card>

        <b-card no-body class="mb-1">
            <h5 v-b-toggle.accordion-time> Temporal heatmap </h5>
            <b-collapse id="accordion-time" accordion="story-accordion" role="tabpanel">
                <b-card-body>
                    <p class="card-text">
                        Crime patterns are affected by time throughout the day and year, and also by the availability of light.
                    </p>
                        <a href="#" @click="goToCluster" v-b-toggle.accordion-analysis variant="info">Go to cluster analysis</a>
                </b-card-body>
            </b-collapse>
        </b-card>

        <b-card no-body class="mb-1">
            <h5 v-b-toggle.accordion-analysis> Analysis </h5>
            <b-collapse id="accordion-analysis" accordion="story-accordion" role="tabpanel">
                <b-card-body>
                    <p class="card-text">
                        At this point you already know different spatio-temporal patterns of crime in Chicago.
                        All this information together adds up to finding groups with similarities along several characteristics.
                        From the 7 groups in the map, let's take 'Hotspots' as an example.
                        This group present some of the most severe crimes (simple and aggravated assaults and battery, drug abuse, weapons violation)
                        in an area that is well connected to public facilities. Its percentage of arrested crimes is on average high.

                        Can you characterize the rest of the groups?
                        *Hint: think on the crime severity and commonness, density of population and connectivity to public facilities.


                    </p>
                        <a href="#" v-b-toggle.accordion-intro variant="info">Go back to start</a>
                </b-card-body>
            </b-collapse>
        </b-card>
    </div>
</template>

<script>

let overviewFirstFly = {
    center: [-87.63910300089432, 41.8200475628504],
"zoom": 10.88618617155909,
"bearing": -76.875,
"pitch": 59.870860830890294,
speed: 0.5
};

let overviewMidwestern = {
   center:[ -87.72582011248245,41.88565159836172],
  "zoom": 11.506349861577503,
  "bearing": 40.642776341305826,
  "pitch": 47.89794514978476,
  speed: 0.5
}

let overviewSouthern = {
    center:[-87.64282874000602, 41.76180654465469],
  "zoom": 12.126513551595915,
  "bearing": 3.0603587588882424,
  "pitch": 39.89983739395454,
  speed: 0.5
};

import Icon from 'vue-awesome';

import { EventBus } from '../event-bus';

export default {
    name: 'StoryNavigation',
    components: {Icon},
    data: () => ({}),
    created: function() {

    },
    methods: {
        onHamburgerClick: function(){
            document.getElementById('story').classList.toggle('collapsed');
        },

        goToOverview: function() {
            EventBus.$emit('route-push', '/overview');
            EventBus.$emit('fly-to', overviewFirstFly);
        },
        goToSouthernOverview: function() {
            EventBus.$emit('fly-to', overviewSouthern);
        },
        goToMidwesternOverview: function() {
            EventBus.$emit('fly-to', overviewMidwestern);
        },
        goToTemporal: function() {
            EventBus.$emit('route-push', '/time');
        },
        goToCluster: function() {
            EventBus.$emit('route-push', '/analysis');
        }

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

    #hamburger button {
        color: #222;
        background-color: rgba(0,0,0,0);
        border: none;
    }
</style>
