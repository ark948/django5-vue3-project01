<script setup>
import { RouterView } from 'vue-router';
import { useAuthStore } from '@/stores';
const authStore = useAuthStore();
</script>

<template>
    <div class="container">
        <notifications position="top" width="400"/>
        <RouterView />
    </div>
</template>

<style scoped>

</style>