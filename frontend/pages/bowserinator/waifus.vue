<template>
    <div>
        {{ averageAge }}<br>

        <h1>Waifus</h1><br>

        <p>
            This is an archive of waifus for Mudae (waifubot) as well as other characters Bowserinator likes.
            Characters are sorted on a scale from D to S (S being the best). The corresponding colors are gray,
            blue, purple, gold, and rainbow respectively.
        </p>

        <p>
            The search box supports chaining queries with <code>AND</code> and <code>OR</code> (case-sensitive).
            Note that OR operators are processed then AND, ie <code>A OR B AND C OR D</code>
            is <code>(A OR B) AND (C OR D)</code>. Currently parentheses are not supported.
        </p>

        <p>
            Use <code>series: series</code>, <code>gender: [M|F|MF]</code>, <code>rank: [sabcd]</code>,
            <code>age:[val | >val | &lt;val | val1-val2]</code>, and
            <code>tag: tag1,tag2,...</code> for more specific tag searching. Note: use <code>tagall: tag1, tag2</code>
            to enforce that the search result contains ALL and not just some of the listed tags.
        </p>

        <b>Examples:</b>
        <p>
            <ol>
                <li>White hair or kitsunemimi: <code>tag: shirokami,kitsune</code></li>
                <li>White haired kitsunemimi vtubers: <code>tagall: shirokami,kitsune,vtuber</code></li>
                <li>Legal waifus: <code>age:>18</code></li>
                <li>Not legal waifus: <code>age:&lt;18</code></li>
                <li>Age 20 to 30: <code>age:20-30</code></li>
                <li>Age exactly 15: <code>age:15</code></li>
                <li>S rank waifus: <code>rank:s</code></li>
                <li>Husbandos or gender ambiguous: <code>gender:m OR gender:mf</code></li>
            </ol>
        </p>

        <p>
            <b>Special tag alias:</b> <code>kemonomimi</code> is a shorthand for all kemonomimi tags.
        </p>

        <v-divider />
        <br>

        <!--
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

/**
 * Check if tag is in taglist with alias support
 * @param {Array} tagList List of tags for waifu
 * @param {string} tag Tag to check if in
 * @return {boolean} Is in tag list
 */
function tagCompare(tagList, tag) {
    tagList = tagList.map(x => x.toLowerCase().trim());
    let tagsToTest = [tag];

    if (['foxgirl', 'fox girl', 'kitsunemimi'].includes(tag))
        tagsToTest.push('kitsune');
    else if (['catgirl', 'cat girl', 'nekomimi'].includes(tag))
        tagsToTest.push('neko');
    else if (['virtual youtuber', 'virtualyoutuber'].includes(tag))
        tagsToTest.push('vtuber');
    else if (tag === 'kemonomimi')
        tagsToTest = tagsToTest.concat(['kitsune', 'neko', 'ookami']);
    else if (tag === 'white hair' || tag === 'whitehair')
        tagsToTest.push('shirokami');

    return tagsToTest.some(tag => tagList.some(t => t.toLowerCase().includes(tag)));
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
            const searchTerm = this.search.toLowerCase().trim();
            const sortBy = this.sortBy || 'Rating';
            const invert = this.sortOrder ? -1 : 1;

            const andTerms = this.search.split(' AND ');
            // { type: 'name|tag|etc...', search: 'search term', 'range': [] }
            const conditions = andTerms.map(term => term.split(' OR ').map(condition => {
                condition = condition.toLowerCase().trim();

                let tag = 'name';
                if (condition.includes(':') && !condition.endsWith(':')) {
                    tag = condition.substring(0, condition.indexOf(':'));
                    let query = condition.substring(condition.indexOf(':') + 1);

                    if (tag === 'series')
                        return { type: tag, query };
                    if (['tag', 'tags'].includes(tag))
                        return { type: 'tag', query: query.split(',').map(x => x.trim()) };
                    if (['tagall', 'tagsall'].includes(tag))
                        return { type: 'tagall', query: query.split(',').map(x => x.trim()) };

                    // Age: formats:
                    // 1. just a number: age:15
                    // 2. a numeric range: age:1-15
                    // 3. lt or gt: age:>15 or age:<15
                    if (tag === 'age') {
                        if (query.includes('-'))
                            query = query.split('-').map(x => +x);
                        else if (query.startsWith('>'))
                            query = [+query.substring(1), null];
                        else if (query.startsWith('<'))
                            query = [null, +query.substring(1)];
                        else
                            query = [+query];
                        if (query.length === 0) return null;
                        return { type: tag, query };
                    }

                    if (tag === 'gender') { // Returns 2 if MF, 0 if F, 1 if M
                        if (!['mf', 'fm', 'm', 'f'].includes(query)) return null;
                        query = (query === 'mf' || query === 'fm') ? 2 : ['f', 'm'].indexOf(query);
                        return { type: tag, query };
                    }
                    if (tag === 'rank') { // Must be sadbcd
                        if (!['s', 'a', 'b', 'c', 'd'].includes(query)) return null;
                        return { type: tag, query };
                    }
                }
                return { type: tag, query: condition };
            })).filter(x => x !== null);

            waifus.forEach(waifu => {
                let pass = searchTerm.length === 0;
                if (!pass) {
                    for (let orCondition of conditions) {
                        // Iterate until any or condition is true
                        let orResult = false;
                        for (let cond of orCondition) {
                            if (cond.type === 'name') {
                                orResult = waifu.name.toLowerCase().includes(cond.query) ||
                                    waifu.nicknames.some(x => x.toLowerCase().includes(cond.query));
                            } else if (cond.type === 'rank')
                                orResult = waifu.rank.toLowerCase() === cond.query;
                            else if (cond.type === 'series')
                                orResult = waifu.series.some(x => x.toLowerCase().includes(cond.query));
                            else if (cond.type === 'tag')
                                orResult = cond.query.some(x => tagCompare(waifu.tags, x));
                            else if (cond.type === 'tagall')
                                orResult = cond.query.every(x => tagCompare(waifu.tags, x));
                            else if (cond.type === 'gender') {
                                let waifuGender = ['mf', 'fm'].includes(waifu.gender.toLowerCase()) ?
                                    2 : ['f', 'm'].indexOf(waifu.gender.toLowerCase());
                                orResult = cond.query === waifuGender;
                            } else if (cond.type === 'age') {
                                if (waifu.age[0] < 0)
                                    orCondition = false;
                                else if (cond.query.length === 1)
                                    orResult = waifu.age.some(age => age === cond.query[0]);
                                else if (cond.query[0] === null)
                                    orResult = waifu.age.some(age => age < cond.query[1]);
                                else if (cond.query[1] === null)
                                    orResult = waifu.age.some(age => age > cond.query[0]);
                                else
                                    orResult = waifu.age.some(age => age >= cond.query[0] && age <= cond.query[1]);
                            }
                            if (orResult) break;
                        }

                        // AND failed: one was false
                        if (!orResult) {
                            pass = false;
                            break;
                        }
                        pass = true;
                    }
                }

                waifu.visible = pass;

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
    box-shadow: 0 5px 25px 5px rgba(0,0,0,0.5) !important;
}
</style>
