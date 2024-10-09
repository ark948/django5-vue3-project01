<script setup>
    console.log('[ProfileView.vue]')
    import { storeToRefs } from 'pinia';
    import { useAuthStore } from '@/stores';

    const authStore = useAuthStore();
    const { email: authEmail } = storeToRefs(authStore);
</script>

<template>
    <div>
        <h1>Hi, {{ authEmail }}</h1>
        <h1>Hi (2), {{ authStore.email }}</h1>
        <h6>access:{{ authStore.access_token }} </h6>
        <h6>refresh: {{ authStore.refresh_token }}</h6>
        <div class="link-container">
            <RouterLink id="back" to="/">Back to home</RouterLink>
        </div>
        <div class="link-container">
            <a @click="authStore.logout()">Logout</a>
        </div>
    </div>
</template>