<script setup>
    import { RouterLink } from 'vue-router'
    console.log("Home");
    import { useAuthStore } from '@/stores';
    import Toast from 'primevue/toast';
    import { useToast } from 'primevue/usetoast';
    const authStore = useAuthStore();
    const toast = useToast();
    
</script>

<template>
    <div class="container">
        <h1>This is home</h1>
        <Toast />
        <div v-if="authStore.access_token" class="link-container">
            <p id="bookmarks_link"><RouterLink to="/bookmarks-list">Bookmarks</RouterLink></p>
            <p><RouterLink to="/profile">Profile page</RouterLink></p>
            <p><RouterLink to="/manual-refresh">Manual token refresh</RouterLink></p>
            <p><RouterLink to="/bmk">bmk</RouterLink></p>
            <div class="user-logged-in-status-container">
                <p>
                    Hello, {{ authStore.full_name }}
                    <a @click="authStore.logout()">Logout</a>
                </p>
            </div>
        </div>
        <div v-else class="link-container">
            <p><RouterLink to="/register">Register</RouterLink></p>
            <p><RouterLink to="/verify-email">Verify Email address</RouterLink></p>
            <p><RouterLink to="/login">Login</RouterLink></p>
            <p><RouterLink to="/forgot-password">Forgot Password?</RouterLink></p>
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