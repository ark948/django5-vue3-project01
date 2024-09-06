<script setup>
    import Login from '@/components/Login.vue';
    import { RouterLink } from 'vue-router'
    console.log("Home");
    
</script>

<template>
    <div class="container">
        <h1>This is home</h1>
        <p><RouterLink to="/register">Register</RouterLink></p>
        <p><RouterLink to="/get-data">Send get request to backend</RouterLink></p>
        <p><RouterLink to="/post-data">Send test data to backend</RouterLink></p>
        <p><RouterLink to="/get-data-opt">get data (options API)</RouterLink></p>
        <p><RouterLink to="/verify-email">Verify Email address</RouterLink></p>
        <p><RouterLink to="/login">Login</RouterLink></p>
        <p><RouterLink to="/profile">Profile page</RouterLink></p>
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