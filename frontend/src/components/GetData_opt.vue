<script>
    import api from '@/api'
    export default {
        data() {
            return {
                message: "message: "
            }
        },

        methods: {
            getData() {
                api.get('test/')
                    .then(response => {
                        this.message += response.data.info
                    })
                    .catch(error => {
                        this.message = error
                    })
                
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