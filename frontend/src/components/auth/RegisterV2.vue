<script setup>
import { onMounted } from 'vue';

onMounted(() => {
    console.log("[RegisterV2.vue] mounted.");
});

import api from '@/api/api';
import { reactive, ref } from 'vue';
import router from '@/router';
import { useNotification } from '@kyvg/vue3-notification';
import { Form, Field } from 'vee-validate';
import * as Yup from 'yup';

const schema = Yup.object().shape({
    email: Yup.string().email().required('Email is required.'),
    first_name: Yup.string().notRequired(),
    last_name: Yup.string().notRequired(),
    password: Yup.string().required('Password is required.'),
    password2: Yup.string().required("Password is required.")
})

const errorMessage = ref("")
const responseMessage = ref("")
const { notify } = useNotification()
const formdata = reactive({
    first_name: "",
    last_name: "",
    email: "",
    password: "",
    password2: ""
})

function handleSubmit() {
    const {email, first_name, last_name, password, password2} = formdata;
    try {
        if (!email || !first_name || !last_name || !password || !password2) {
            errorMessage.value = "All inputs are required."
            console.log("request blocked.")
            return
        }
    } catch (error) { console.log(error) }

    try {
        api.post('auth/api/register/', formdata)
            .then(response => {
                if (response.status === 201) {
                    console.log("Success")
                    // responseMessage.value = response.data.message
                    notify({
                        title: "Registration",
                        text: 'Successfully registered. Please check your email.'
                    })
                    router.push({ name: 'verify_email' })
                }
            })
            .catch(error => {
                console.log(error)
                errorMessage.value = error
            })
            .finally(() => {
                console.log(`${'-'.repeat(30)}`)
                for (let i in formdata) {
                    formdata[i] = ""
                }
            })
    } catch (error) {
        console.log(error)
        return
    }
}

function handleSubmitV2(values) {
        const { email, first_name, last_name, password, password2 } = values;
        api.post('auth/api/register/', {email, first_name, last_name, password, password2})
            .then((response) => {
                if (response.status === 201) {
                    console.log("Success");
                    notify({
                        title: "Registration",
                        text: 'Successfully registered. Please check your email.'
                    });
                    router.push({ name: 'verify_email' });
                }
            })
            .catch((e) => {
                errorMessage.value = e;
            })
            .finally(() => {
                console.log(`${'-'.repeat(30)}`)
                values = "";
            });
    }

</script>

<template>
    <div class="container">
        <h2>Registration</h2>
        <div class="form-container">
            <Form @submit="handleSubmitV2" :validation-schema="schema">
                <label class="form-label" for="email">Email:</label>
                <Field class="register-input-field" name="email" type="email" />
                <label class="form-label" for="first_name">First Name:</label>
                <Field class="register-input-field" name="first_name" type="text" />
                <label class="form-label" for="last_name">Last Name:</label>
                <Field class="register-input-field" name="last_name" type="text" />
                <label class="form-label" for="password">Password:</label>
                <Field class="register-input-field" name="password" type="password" />
                <label class="form-label" for="password2">Repeat password:</label>
                <Field class="register-input-field" name="password2" type="password" />
                <button class="form-button">Sign Up</button>
            </Form>
        </div>
        <p class="error-message">
            {{ errorMessage }}
        </p>
        <p class="response-message">
            {{ responseMessage }}
        </p>
        <div class="container">
            <RouterLink id="back" to='/'>Back to home</RouterLink>
        </div>
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

.register-input-field {
    width: 100%;
    padding: 8px;
    margin: 10px 0;
    border: 1px solid #42B883;
    border-radius: 6px;
    box-sizing: border-box;
}

.form-label {
    font-size: 15px;
}

.form-button {
    width: 100%;
    padding: 10px;
    margin: 20px 0;
    background-color: #42B883;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.2s ease-in-out;
    font-size: 15px;
}

.form-button:hover {
    background-color: #0056b3;
}
</style>