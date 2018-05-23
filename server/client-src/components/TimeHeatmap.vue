<template>
    <div>
        <b-form-select v-model="crimeType" :options="types" class="mb-3" />
        <svg :width="width" :height="height">
            <g :style="{transform: `translate(${margin.left}px, ${margin.top}px)`}">
            </g>
        </svg>
    </div>
</template>


<script>
import * as d3 from 'd3';

import {getApi} from '../utils';

const props = {
  types: {
      type: Array,
      default: () => [],
  },
  selection: {
      type: Array,
      default: () => [],
  },
  margin: {
    type: Object,
    default: () => ({
      left: 40,
      right: 0,
      top: 20,
      bottom: 10,
    }),
  },
  ceil: {
    type: Number,
    default: 100,
  },
};

export default {
    name: 'TimeHeatmap',
    props,
    data: () => ({
        crimeType: '03',
        data: null,
        width: 0,
        height: 0,
        paths: {
            cells: ''
        },
        scaled: {
            x: null,
            y: null,
        },
        colors: ["#ffffd9","#edf8b1","#c7e9b4","#7fcdbb","#41b6c4","#1d91c0","#225ea8","#253494","#081d58"],
        months: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        times: ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"]

    }),
    computed: {
        padded() {
            const width = this.width - this.margin.left - this.margin.right;
            const height = this.height - this.margin.top - this.margin.bottom;
            return { width, height };
        },
        gridSize() {
            const {width, height} = this.padded;
            return {gridXSize: width / 12, gridYSize: height / 24};
        }
    },
    mounted() {
        window.addEventListener('resize', this.onResize);
        this.onResize();
    },
    beforeDestroy() {
        window.removeEventListener('resize', this.onResize);
    },
    watch: {
        crimeType: function typeChanged(newType, oldType) {
             getApi('/api/time?type='+newType)
                .then(data => {
                    this.data = data;
            });
        },
        data: function dataChanged(newData, oldData) {
            this.update();
        },
        width: function widthChanged() {
            this.update();
        },
    },
    methods: {
        onResize() {
            this.width = this.$el.offsetWidth;
            this.height = this.$el.offsetHeight;
        },
        update() {
            if(!this.data) return;
            this.colorScale = d3.scaleQuantile()
                .domain([0, d3.max(this.data, d => d.count)])
                .range(this.colors);
            let svg = d3.select('svg').select('g');

            const {gridXSize, gridYSize} = this.gridSize;
            const {width: paddedWidth, height: paddedHeight} = this.padded;

            var monthLabels = svg.selectAll(".monthLabel")
                .data(this.months)
                .enter().append("text")
                    .text(d => d)
                    .attr("y", paddedHeight)
                    .attr("x", (d, i) => i * gridXSize)
                    .style("text-anchor", "middle")
                    .attr("transform", "translate(" + gridXSize / 2 + ", -6)")
                    .attr("class", d => "monthLabel mono axis");

            var timeLabels = svg.selectAll(".timeLabel")
                .data(this.times)
                .enter().append("text")
                    .text(x => x)
                    .attr("x", 0)
                    .attr("y", (d, i) => paddedHeight - (i + 2) * gridYSize)
                    .style("text-anchor", "end")
                    .attr("transform", "translate(-6, " + gridYSize / 1.5 + ")")
                    .attr("class", d => "timeLabel mono axis");

            let cells = svg.selectAll('.hour')
                .data(this.data, d => d.month+':'+d.hour);
            
            cells.selectAll('title').remove();
            cells.append("title");
            cells.select('title').text(d => d.count);

            cells.enter().append('rect')
                .attr('x', d => (d.month - 1)  * gridXSize )
                .attr('y', d => paddedHeight - (d.hour + 2) * gridYSize)
                .attr('class', 'hour bordered')
                .attr('width', gridXSize)
                .attr('height', gridYSize)
                .style('fill', d => this.colorScale(d.count));

            cells.transition().duration(1000)
                .style('fill', d => this.colorScale(d.count));

            // cells.select('title').text(d => d.count);

            cells.exit().remove();
        }
    }
    
}
</script>


<style>
    rect.bordered {
        stroke: #e6e6e6;
        stroke-width:2px;   
      }

    text.mono {
        font-size: 9pt;
        font-family: Consolas, courier;
        fill: #111;
      }

</style>
