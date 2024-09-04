<script setup>
    import api from '@/api';
    import axios from 'axios';
    import { ref } from 'vue';

    const message = ref("")

    const get_data = () => {
        try {
            api.get('/api/test/')
                .then(function (response) {
                    console.log("SUCCESS")
                    message.value = response.data.info
                })
                .catch(function (error) {
                    console.log(error)
                    message.value = "ERROR"
                })
                .finally(() => {
                    console.log("DONE")
                })
        } catch (error) {
            console.log(error);
        }
    }
    
</script>

<template>
    <div class="container">
        <h2>Data:</h2>
        <div class="data">{{ message }}</div>
        <button @click="get_data">Request data</button>
    </div>
</template>

<style scoped>

</style>