<script setup>
    console.log('[Login_v4.vue]')
    import { Form, Field } from 'vee-validate';
    import * as Yup from 'yup';

    import { useAuthStore } from '@/stores';

    const schema = Yup.object().shape({
        email: Yup.string().required('Email is required.'),
        password: Yup.string().required('Password is required.')
    });

    function onSubmit(values) {
        console.log('[Login_v4.vue] onSubmt called.')
        const authStore = useAuthStore();
        const { email, password } = values;
        
        return authStore.new_login(email, password)
            .catch(error => console.log('[Login_v4.vue] Error: ', error))
    }

</script>

<template>
    <div>
        <h2>Login</h2>
        <div class="form-container">
        <Form @submit="onSubmit" :validation-schema="schema">
            <label class="form-label" for="email">Email:</label>
            <Field class="form-input" name="email" type="text" />
            <label class="form-label" for="password">Password</label>
            <Field class="form-input" name="password" type="password" />
            <button class="form-button">Login</button>
        </Form>
        </div>
        <h4>Do you want to sign up?</h4>
        <p><RouterLink to="/register">Register</RouterLink></p>
        <p><RouterLink to="/forgot-password">Forgot passsword?</RouterLink></p>
        <p><RouterLink to="/">Home</RouterLink></p>
    </div>
</template>



<style scoped>

    .form-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: 50px auto;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        max-width: 400px;
    }

    .form-input {
        width: 100%;
        padding: 8px;
        margin: 10px 0;
        border: 1px solid #42B883;
        border-radius: 8px;
        box-sizing: border-box;
    }

    .form-label {
        font-size: 15px;
        padding: 10px;
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