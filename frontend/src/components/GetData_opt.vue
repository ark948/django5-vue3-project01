<script>
    import api from '@/api/api'
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
    <div class="container">
        <button @click="getData">Update message</button>
        <p>{{ message }}</p>
    </div>
</template>

<style scoped>

</style>