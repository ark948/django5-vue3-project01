<script setup>
    console.log("Register");

    import api from '@/api';
    import { ref } from 'vue';

    const formdata = ref({
        first_name: "",
        last_name: "",
        email: "",
        password: "",
        password2: ""
    })

    function handleChange(e) {

    }

    function handleSubmit(e) {
        e.preventDefault()
        console.log("Form submitted -=>")
        formdata_no_bind = {
            first_name: ""
        }
    }
    
</script>

<template>
    <div>
        <h2>Registration</h2>
        <form action="">
            <label for="email">Email:</label>
            <input id="email" type="text" name="email">
            <br>
            <label for="first_name">First Name:</label>
            <input id="first_name" type="text" name="first_name">
            <br>
            <label for="last_name">Last Name:</label>
            <input id="last_name" type="text" name="last_name">
            <br>
            <label for="password">Password:</label>
            <input id="password" type="password" name="password">
            <br>
            <label for="password2">Repeat password:</label>
            <input id="password2" type="password" name="password2">
            <br>
            <button v-on:click="handleLogin">Submit</button>
        </form>
    </div>
</template>

<style scoped>

</style>