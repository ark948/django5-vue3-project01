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
    </div>
</template>