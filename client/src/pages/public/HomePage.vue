<script setup>
    import { RouterLink } from 'vue-router';
    import { onMounted } from 'vue';
    onMounted(() => {
        console.log("Home mounted.");
    });
</script>


<template>
    <div class="container">
        <div class="link-contaienr">
            <p><RouterLink to="/">Home</RouterLink></p>
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