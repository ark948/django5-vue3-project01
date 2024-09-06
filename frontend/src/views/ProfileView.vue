<script setup>
    console.log("Profile")
</script>

<template>
    <div class="container">
        <h3>This is a protected route</h3>
    </div>
    <div class="link-container">
        <RouterLink id="back" to='/'>Back to home</RouterLink>
    </div>
</template>