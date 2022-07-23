<template>
    <div>
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

    for (let header of headers) {
        obj[header] = line[headers.indexOf(header)];
    }
    return obj;
});


export default {
    name: 'WaifusPage',
    waifus: waifus
};
</script>
