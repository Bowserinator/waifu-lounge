<template>
    <div>
        {{ averageAge }}<br>

        <h1>Waifus</h1>

        <p>This is an archive of waifus for Mudae (waifubot) as well as other characters Bowserinator likes.</p>

        <p>
            The search box supports chaining queries with <code>AND</code> and <code>OR</code> (case-sensitive). Use
            <code>series: series</code>, <code>gender: [M|F|MF]</code>, <code>rank: [sabcd]</code>, and
            <code>tag: tag1,tag2,...</code> for more specific tag searching.
        </p>

        <v-divider />
        <br>

        <!--
- auto cluster by properties
- oclor chart + age chart + count
        -->
        <v-card class="search-header">
            <v-text-field
                v-model="search"
                label="Search" dense solo
                filled
                style="max-width: 800px; border-radius: 0"
            >
                <template slot="prepend-inner">
                    <v-icon color="white">
                        mdi-magnify
                    </v-icon>
                </template>
            </v-text-field>

            <div class="sort-options">
                <v-label>Sort:</v-label>

                <v-select
                    v-model="sortBy"
                    label="Sort by"
                    dense filled solo
                    :items="['Rating', 'Name', 'Age', 'Color Hue', 'Color Lightness', 'Name Length']"
                />

                <v-btn-toggle
                    v-model="sortOrder" dense tile borderless
                >
                    <v-btn><v-icon>mdi-trending-up</v-icon></v-btn>
                    <v-btn><v-icon>mdi-trending-down</v-icon></v-btn>
                </v-btn-toggle>
            </div>
        </v-card>
        <br>

        <WaifuBox v-for="waifu in waifus" v-show="waifu.visible" :key="waifu.index" :waifu="waifu" />
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
    obj['visible'] = true;
    return obj;
});

let i = 0;
waifus.forEach(w => w.index = ++i);

/**
 * Convert RGB color to HSV
 * @param {Array} color [R, G, B]
 * @return {Array} [H, S, V] tuple
 */
function rgb2hsv(color) {
    let [r, g, b] = color;
    let v = Math.max(r, g, b); let c = v - Math.min(r, g, b);
    let h = c && ((v === r) ? (g - b) / c :
        ((v === g) ? 2 + (b - r) / c : 4 + (r - g) / c));
    return [60 * (h < 0 ? h + 6 : h), v && c / v, v];
}


export default {
    name: 'WaifusPage',
    data() {
        return {
            search: '',
            sortBy: 'Rating',
            sortOrder: false
        };
    },
    computed: {
        waifus() {
            // TODO: search format like series: test AND name AND todo OR etc...
            const searchTerm = this.search.toLowerCase().trim();
            const sortBy = this.sortBy || 'Rating';
            const invert = this.sortOrder ? -1 : 1;

            waifus.forEach(waifu => {
                waifu.visible = waifu.name.toLowerCase().includes(searchTerm);
                if (sortBy === 'Age') // Don't show waifus without an age
                    waifu.visible = waifu.visible && waifu.age[0] >= 0;
            });
            return waifus.sort((a1, b1) => {
                const property = {
                    'Rating': 'rank',
                    'Name': 'name',
                    'Age': 'age',
                    'Color Hue': 'palette',
                    'Color Lightness': 'palette',
                    'Name Length': 'name'
                }[sortBy];
                const postFunction = {
                    'Name': x => x.toLowerCase(),
                    'Name Length': x => x.length,
                    'Age': x => x[0] || -1,
                    'Rating': x => 'sabcd'.indexOf(x.toLowerCase()),
                    'Color Hue': x => {
                        x = x.map(y => {
                            // Only compute hue of color with highest saturation
                            let maxSaturation = -1;
                            let hue = 0;

                            for (let c of y.slice(0, 2)) {
                                let [h, s, _] = rgb2hsv(c);
                                if (s > maxSaturation) {
                                    maxSaturation = s;
                                    hue = h;
                                }
                            }
                            return hue;
                        });
                        return x.reduce((a, b) => a + b) / x.length;
                    },
                    'Color Lightness': x => {
                        x = x.map(y => {
                            // Only compute lightness of first 2 dominant colors
                            y = y.slice(0, 2);
                            return y.map(c => c[0] + c[1] + c[2]).reduce((a, b) => a + b) / y.length;
                        });
                        return x.reduce((a, b) => a + b) / x.length;
                    }
                }[sortBy] || (x => x);

                let a = postFunction(a1[property]);
                let b = postFunction(b1[property]);

                if (a === b) return invert * a1.name.localeCompare(b1.name);
                return invert * (a < b ? -1 : 1);
            });
        },
        averageAge() {
            let filteredAges = waifus.filter(w => w.age[0] >= 0);

            filteredAges = filteredAges.map(w => w.age[0]);
            filteredAges.sort();
            return waifus.filter(w => w.age[0] > 0 && w.age[0] < 15).map(w => w.name);
        }
    }
};
</script>


<style lang="scss">
@import './assets/global.scss';

.sort-options {
    $sort-line-height: 40px;

    margin-top: -16px;
    display: flex;

    & > * {
        margin-right: 6px !important;
        max-width: 200px;
        border-radius: 2px;
        height: $sort-line-height !important;
        display: inline-block;
    }

    & > label {
        line-height: $sort-line-height !important;
        display: block;
        margin-right: 12px !important;
    }
}

.search-header {
    position: sticky;
    top: 0;
    padding: 10px;
    z-index: 99999;
    max-width: calc(800px + 20px); // search bar + padding

    // Override card style
    border-radius: 2px !important;
    background-color: #2a2a2a !important;
    box-shadow: 0px 5px 25px 5px rgba(0,0,0,0.75) !important;
}
</style>
