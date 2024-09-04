<script setup>
    import { RouterLink } from 'vue-router'
    console.log("HomeView.vue");
    
</script>

<template>
    <div>
        <h1>This is home</h1>
        <RouterLink to="/register">
            Register
        </RouterLink>
        <RouterLink to="/get-data">
            send test request to backend
        </RouterLink>
    </div>
</template>