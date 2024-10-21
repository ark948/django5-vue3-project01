<script>
    import api from '@/api/api'
    export default {
        data() {
            return {
                displayMessage: false,
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
            },
            updateMessage() {
                this.displayMessage = true;
                this.message = "This should exist now.";
            }
        },
    }

</script>

<template>
    <div class="container">
        <button id="btn" @click="updateMessage">Update message</button>
        <p id="msg" v-if="displayMessage">{{ message }}</p>
    </div>
</template>

<style scoped>

</style>