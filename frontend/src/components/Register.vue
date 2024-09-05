<script setup>
    console.log("Register.vue");
    
</script>

<template>
    <div>
        <h2>Registration</h2>
        <form action="">
            <label for="email">Email:</label>
            <input id="email" type="text" name="email">
            <label for="first_name">First Name:</label>
            <input id="first_name" type="text" name="first_name">
            <label for="last_name">Last Name:</label>
            <input id="last_name" type="text" name="last_name">
            <label for="password">Password:</label>
            <input id="password" type="password" name="password">
            <label for="password2">Repeat password:</label>
            <input id="password2" type="password" name="password2">
            <button>Submit</button>
        </form>
    </div>
</template>

<style scoped>

</style>