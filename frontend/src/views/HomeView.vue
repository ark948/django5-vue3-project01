<script setup>
    import { RouterLink } from 'vue-router'
    console.log("Home");
    import { useAuthStore } from '@/stores';

    const authStore = useAuthStore();
    
</script>

<template>
    <div class="container">
        <h1>This is home</h1>
        <div v-if="authStore.access_token" class="link-container">
            <p><RouterLink to="/bookmarks-list">Bookmarks</RouterLink></p>
            <!-- <p><RouterLink to="/bookmarks-list-v2">Bookmarks (v2)</RouterLink></p> -->
            <p><RouterLink to="/profile">Profile page</RouterLink></p>
            <p><RouterLink to="/manual-refresh">Manual token refresh</RouterLink></p>
            <p>
                Hello, {{ authStore.full_name }}
                <a @click="authStore.logout()">Logout</a>
            </p>
        </div>
        <div v-else class="link-container">
            <p><RouterLink to="/register">Register</RouterLink></p>
            <p><RouterLink to="/verify-email">Verify Email address</RouterLink></p>
            <p><RouterLink to="/login">Login</RouterLink></p>
            <p><RouterLink to="/forgot-password">Forgot Password?</RouterLink></p>
        </div>
        <div class="user-status-container">
            
        </div>
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