<template>
    <div class="everything-wrapper">
        <div>
            <v-card :class="[ 'waifu-card', rankClass ]" :max-width="cardWidth" outlined>
                <v-card-text>
                    <p class="waifu-name truncate">
                        <b>{{ waifu.name }}</b>
                    </p>

                    <div class="info-container">
                        <!-- Gender + series -->
                        <v-tooltip bottom open-delay="500">
                            <template #activator="{ on, attrs }">
                                <div
                                    class="truncate" v-bind="attrs"
                                    v-on="on"
                                >
                                    <span v-if="waifu.gender.toLowerCase().includes('f')" class="gender female">♀</span>
                                    <span v-if="waifu.gender.toLowerCase().includes('m')" class="gender male">♂</span>
                                    {{ waifu.series.join(', ') }}<br>
                                </div>
                            </template>
                            <span>
                                <div v-for="(name, index) in waifu.series" :key="index">
                                    {{ name }}
                                </div>
                            </span>
                        </v-tooltip>

                        <!-- Details -->
                        <div>{{ details }}</div>

                        <!-- Nicknames -->
                        <v-tooltip bottom open-delay="500">
                            <template #activator="{ on, attrs }">
                                <div
                                    class="truncate"
                                    v-bind="attrs"
                                    v-on="on"
                                >
                                    <i>{{ waifu.nicknames.join(', ') }}</i>
                                </div>
                            </template>
                            <span>
                                <div v-for="(name, index) in waifu.nicknames" :key="index">
                                    {{ name }}
                                </div>
                            </span>
                        </v-tooltip>
                    </div>

                    <v-img
                        :src="'/waifu_images/' + waifu.images[imageIndex]"
                        :height="imageHeight()"
                        :width="imageWidth()"
                        class="waifu-image"
                    />

                    <div class="d-flex">
                        <div
                            v-for="(color, index) in waifu.palette[imageIndex]" :key="index"
                            :style="{ backgroundColor: `rgb(${color.join(',')})` }" class="palette-color"
                        />
                    </div>

                    <small style="float: right">{{ imageIndex + 1 }} / {{ waifu.images.length }}</small>

                    <div class="tag-container">
                        <v-chip
                            v-for="(tag, index) in waifu.tags" :key="index" x-small class="mr-1"
                        >
                            {{ tag }}
                        </v-chip>
                    </div>
                </v-card-text>
            </v-card>

            <div class="button-wrapper">
                <v-btn color="gray" small @click="imageLeft">
                    🡄
                </v-btn>
                <v-btn color="gray" small @click="imageRight">
                    🡆
                </v-btn>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'WaifuBox',
    props: {
        waifu: {
            type: Object,
            required: true
        }
    },
    data() {
        return {
            imageIndex: 0
        };
    },
    computed: {
        rankClass() {
            const rank = this.waifu.rank.toUpperCase();
            if (['A', 'B', 'C', 'D', 'E', 'S'].includes(rank))
                return rank;
            return '';
        },
        gender() {
            return '♀️';
        },
        details() {
            let details = [];
            let ages = this.waifu.age.filter(age => age >= 0);
            if (ages.length)
                details.push(`Age${this.waifu.age.length > 1 ? 's' : ''}: ${this.waifu.age.join(', ')}`);
            if (this.waifu.height !== 'Unknown')
                details.push(`Height: ${this.waifu.height}`);
            if (this.waifu.birthday !== 'Unknown')
                details.push(`Birthday: ${this.waifu.birthday}`);
            return details.join(' • ');
        },
        cardWidth() {
            const size = this.waifu.im_sizes[this.imageIndex];
            return Math.min(300, Math.round(200 * size[0] / size[1] + 96));
        }
    },
    methods: {
        imageLeft() {
            this.imageIndex--;
            if (this.imageIndex < 0)
                this.imageIndex = this.waifu.images.length - 1;
        },
        imageRight() {
            this.imageIndex++;
            if (this.imageIndex > this.waifu.images.length - 1)
                this.imageIndex = 0;
        },
        imageHeight() {
            return 280;
        },
        imageWidth() {
            const size = this.waifu.im_sizes[this.imageIndex];
            return Math.round(Math.min(360, size[0] / size[1] * this.imageHeight()));
        }
    }
};
</script>


<style lang="scss" scoped>
.everything-wrapper {
    display: inline-block;
    margin: 5px;
}

.button-wrapper {
    margin-top: 10px;
}

.waifu-card {
    border-radius: 0;
    border-left: 2px solid gray;
    transition: background-color 0.2s;

    &:hover {
        background-color: #282828;
    }

    // S rank gets fancy animated rainbow border
    &.S {
        border-left: 2px solid transparent;
        position: relative;

        &:after {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 2px;
            height: 100%;
            background: linear-gradient(0deg,
                rgba(161,177,255,1) 0%, rgba(255,161,180,1) 15%, rgba(247,184,255,1) 30%,
                rgba(202,158,255,1) 46%, rgba(123,245,196,1) 63%, rgba(255,238,190,1) 82%,
                rgba(255,202,213,1) 100%) 0 0/100% 200%;
            animation: scroll 2s linear infinite;

            @keyframes scroll {
                to { background-position: 0 -200% }
            }
        }
    }
    &.A { border-left: 2px solid #FFB74D; }
    &.B { border-left: 2px solid #E040FB; }
    &.C { border-left: 2px solid #42A5F5; }
    &.D { border-left: 2px solid gray; }
    &.E { border-left: 2px solid #F44336; }
}


.info-container {
    margin-bottom: 7px;
}

.waifu-image {
    border-radius: 3px 3px 0 0;
    max-width: 100%;
    object-fit: cover;
    background: white;
    background-position: left center;
}

.palette-color {
    height: 2px;
    width: 100%;
}

.waifu-name {
    opacity: 1;
    color: white;
    margin-bottom: 5px;
}

.gender {
    font-weight: bold;
    opacity: 1;
    font-size: 12pt;

    &.female { color: #FF5252; }
    &.male { color: #42A5F5; }
}

.truncate {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.tag-container {
    margin-top: 7px;
    min-height: 12px;
}
</style>
