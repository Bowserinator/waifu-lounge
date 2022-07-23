<template>
    <v-app dark>
        <!-- Main content -->
        <v-main>
            <v-container class="main-container">
                <Nuxt />
            </v-container>

            <!-- Footer -->
            <v-footer>
                <span>Hellomouse &copy; {{ new Date().getFullYear() }}</span>
            </v-footer>
        </v-main>
    </v-app>
</template>

<script>
export default {
    name: 'DefaultLayout'
};
</script>


<style lang="scss" scoped>
    // Make the main container always tall enough to
    // push the footer out of view
    .main-container {
        min-height: 100vh;
    }
</style>
