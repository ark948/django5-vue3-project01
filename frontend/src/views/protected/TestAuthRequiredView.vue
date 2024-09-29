<script setup>
    import api from '@/api/api';
    import { ref } from 'vue';


    const responseMessage = ref("");

    async function handleSubmit() {
        api.get('auth/api/auth-required')
            .then(res => {
                if (res.status === 200) {
                    console.log("[TestAuthRequiredView.vue] Response code 200")
                    responseMessage.value = res.data.msg
                }
            })
            .catch(error => {
                console.log("Error");
                responseMessage.value = error
            })
    }
</script>

<template>
  <div class="container">
    <h4>Click on button to send request to auth required view</h4>
    <form @submit.prevent="handleSubmit">
        <button>Click to get secret</button>
    </form>
    <div class="response-container">
        <p>{{ responseMessage }}</p>
    </div>
    <div class="link-container">
            <RouterLink id="back" to="/">Back to home</RouterLink>
    </div>
  </div>
</template>

<style>

</style>