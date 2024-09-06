<script>
    export default {
        data() {
            return {
                message: "message: "
            }
        },

        methods: {
            getData() {
                // axios req
                this.message += "Button clicked."
            }
        },
    }

</script>

<template>
    <button @click="getData">Update message</button>
    <p>{{ message }}</p>
</template>

<style scoped>

</style>