<script setup>
console.log("Register");

import api from '@/api';
import { reactive, ref } from 'vue';
import axios from 'axios'

const errorMessage = ref("")
const responseMessage = ref("")
const formdata = reactive({
    first_name: "",
    last_name: "",
    email: "",
    password: "",
    password2: ""
})

function handleSubmit(e) {
    e.preventDefault()
    const {email, first_name, last_name, password, password2} = formdata;
    try {
        if (!email || !first_name || !last_name || !password || !password2) {
            errorMessage.value = "All inputs are required."
            console.log("request blocked.")
            return
        }
    } catch (error) { console.log(error) }

    try {
        api.post('auth/register/', formdata)
            .then(response => {
                if (response.status === 201) {
                    console.log("Success")
                    responseMessage.value = response.data.message
                }
            })
            .catch(error => {
                console.log(error)
                errorMessage.value = error
            })
            .finally(() => console.log(`${'-'.repeat(30)}`))
    } catch (error) {
        console.log(error)
        return
    }
}

</script>

<template>
    <div class="container">
        <h2>Registration</h2>
        <div class="form-container">
            <form @submit="handleSubmit" action="">
                <label class="form-label" for="email">Email:</label>
                <input v-model.trim="formdata.email" class="form-input" id="email" type="text" name="email">
                <label class="form-label" for="first_name">First Name:</label>
                <input v-model.trim="formdata.first_name" class="form-input" id="first_name" type="text" name="first_name">
                <label class="form-label" for="last_name">Last Name:</label>
                <input v-model="formdata.last_name" class="form-input" id="last_name" type="text" name="last_name">
                <label class="form-label" for="password">Password:</label>
                <input v-model.trim="formdata.password" class="form-input" id="password" type="password" name="password">
                <label class="form-label" for="password2">Repeat password:</label>
                <input v-model.trim="formdata.password2" class="form-input" id="password2" type="password" name="password2">
                <button class="form-button">Submit</button>
            </form>
        </div>
        <p class="error-message">
            {{ errorMessage }}
        </p>
        <p class="response-message">
            {{ responseMessage }}
        </p>
    </div>
    <div class="container">
        <RouterLink id="back" to='/'>Back to home</RouterLink>
    </div>
</template>

<style scoped>
    /* FormStyles.css */
.form-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin: 50px auto;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    max-width: 400px;
}

.form-input {
    width: 90%;
    padding: 10px;
    margin: 10px 0;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-sizing: border-box;
}

.form-label {
    padding: 10px;
}

.form-button {
    width: 90%;
    padding: 10px;
    margin: 20px 0;
    background-color: #42B883;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.2s ease-in-out;
}

.form-button:hover {
    background-color: #0056b3;
}
</style>