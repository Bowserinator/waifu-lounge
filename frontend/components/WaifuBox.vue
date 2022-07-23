<template>
    <p>{{waifu.name}}</p>
</template>

<script>
export default {
    name: 'WaifuBox',
    props: {
        waifu: {
            type: Object,
            required: true
        }
    }
};
</script>


<style scoped>

</style>
