<script setup>
    import { RouterLink } from 'vue-router'
    console.log("Home");
    
</script>

<template>
    <div class="container">
        <h1>This is home</h1>
        <p><RouterLink to="/register">Register</RouterLink></p>
        <p><RouterLink to="/get-data">Send test request to backend</RouterLink></p>
        <p><RouterLink to="/post-data">Send test data to client</RouterLink></p>
    </div>
</template>

<style scoped>
    .container {
        margin: 20px;
    }
    .container p {
        margin: 20px;
    }
</style>