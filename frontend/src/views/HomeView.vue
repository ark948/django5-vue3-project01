<script setup>
    import { RouterLink } from 'vue-router'
    console.log("Home");
    import { useAuthStore } from '@/stores';

    const authStore = useAuthStore();
    
</script>

<template>
    <div class="container">
        <h1>This is home</h1>
        <p><RouterLink to="/bookmarks-list">Bookmarks</RouterLink></p>
        <p><RouterLink to="/register">Register</RouterLink></p>
        <p><RouterLink to="/get-data">Send get request to backend</RouterLink></p>
        <p><RouterLink to="/post-data">Send test data to backend</RouterLink></p>
        <p><RouterLink to="/get-data-opt">get data (options API)</RouterLink></p>
        <p><RouterLink to="/verify-email">Verify Email address</RouterLink></p>
        <p><RouterLink to="/login">Login</RouterLink></p>
        <p><RouterLink to="/profile">Profile page</RouterLink></p>
        <p><RouterLink to="/test-auth">Test Authenticated view</RouterLink></p>
        <p><RouterLink to="/secret">Secret Path</RouterLink></p>
        <p><RouterLink to="/manual-refresh">Manual token refresh</RouterLink></p>
        <p><a @click="authStore.logout()">Logout</a></p>
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