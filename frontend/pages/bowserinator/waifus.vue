<template>
    <div>
        {{ averageAge }}<br>

        <WaifuBox v-for="(waifu, index) in $options.waifus" :key="index" :waifu="waifu" />
    </div>
</template>

<script>
import waifuData from '../../data/waifus.data';

// Parse data
const waifuLines = waifuData.split('\n');
const headers = waifuLines[0].split(',');
const waifus = waifuLines.slice(1).map(line => {
    let obj = {};
    line = JSON.parse(line);

    for (let header of headers)
        obj[header] = line[headers.indexOf(header)];
    return obj;
});


export default {
    name: 'WaifusPage',
    waifus: waifus,
    computed: {
        averageAge() {
            let filteredAges = waifus.filter(w => w.age[0] >= 0);
            return filteredAges.map(w => w.age[0]) // .reduce((a, b) => a + b) / w.age.length
                .reduce((a, b) => a + b) / filteredAges.length;
        }
    }
};
</script>
