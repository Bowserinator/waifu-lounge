<template>
    <div
        class="wrapper"
        :style="{
            'maxWidth': `${maxWidth}px`,
        }"
    >
        <div class="bars">
            <div
                v-for="(bin, index) in bins.bins"
                :key="index"
                class="bar"
                :style="{
                    'height': `${bin.value * barHeight / bins.max}px`,
                    'backgroundColor': barColor
                }"
            />
        </div>

        <div class="bars">
            <div
                v-for="(bin, index) in bins.bins"
                :key="index"
                class="bar-label"
            >
                {{ bin.range }}
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'HistogramView',
    props: {
        data: {
            type: Array,
            required: true,
            validator: val => val.every(v => typeof v === 'number')
        },
        // Max width of histogram (entire)
        maxWidth: {
            type: Number,
            default: 800,
            validator: val => val > 0
        },
        barHeight: {
            type: Number,
            default: 200,
            validator: val => val > 0
        },
        binSize: {
            type: Number,
            default: 1,
            validator: val => val % 1 === 0 && val >= 1
        },
        hideEmptyBins: {
            type: Boolean,
            default: false
        },
        logY: {
            type: Boolean,
            default: false
        },
        barColor: {
            type: String,
            default: 'white'
        }
    },
    computed: {
        bins() {
            const data = [...this.data].sort((a, b) => a - b);
            const bins = [];
            let currentBin = 0;
            let i = data[0];
            let j = 0;
            let max = 0;

            while (i <= data[data.length - 1] + this.binSize + 1) {
                if (i <= data[j] && data[j] < i + this.binSize) {
                    currentBin++;
                    j++;
                } else {
                    if (currentBin || !this.hideEmptyBins) {
                        let range = this.binSize === 1 ? '' + i : `${i}-${i + this.binSize - 1}`;
                        if (this.logY) currentBin = Math.log10(currentBin);
                        bins.push({ value: currentBin, range });
                    }
                    if (currentBin > max)
                        max = currentBin;

                    currentBin = [];
                    i = this.hideEmptyBins ?
                        data[j] - data[j] % this.binSize : i + this.binSize;
                }
            }
            return { bins, max };
        }
    }
};
</script>

<style lang="scss" scoped>
$bar-width: 16px;
$bar-margin: 1px;

.wrapper {
    padding: 8px;
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 2px;
    background-color: rgba(0, 0, 0, 0.1);
    overflow-x: auto;
}

.bars {
    white-space: nowrap;
    text-align: center;

    & > div {
        width: $bar-width;
        display: inline-block;
        margin: 0 $bar-margin;
    }

    .bar {
        border-radius: 2px 2px 0 0;
    }

    .bar-label {
        vertical-align: top;
        writing-mode: vertical-rl;
        text-orientation: mixed;
        font-size: $bar-width * 0.7;
    }
}
</style>
