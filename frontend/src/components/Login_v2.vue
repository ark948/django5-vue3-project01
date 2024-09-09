<script setup>
    console.log("Login - V2")
    import { Form, Field } from 'vee-validate'
    import * as Yup from 'yup'

    import { ref } from 'vue'
    import useAuthStore from '../store/auth.store'

    const errorMessage = ref("")
    const schema = Yup.object().shape({
        email: Yup.string().email().required("Email is required."),
        password: Yup.string().required("Password is required.")
    });

    function handleSubmit(e) {
        e.preventDefault()
        console.log("Login form called.")
        const authStore = useAuthStore()
        const { email, password } = values

        return authStore.login(email, password)
            .catch(error => errorMessage.value = error)
    }

</script>

<template>
    <div class="container">
        <h2>Login</h2>
        <div @submit="handleSubmit" class="form-container" :validation-schema="schema">
            <form action="">
                <div class="form-group">
                    <label for="">Email:</label>
                    <Field name="email" type="text" class="form-control" />
                </div>
                <div class="form-group">
                    <label for="">Password:</label>
                    <Field name="password" type="text" class="form-control" />
                </div>
                <div class="form-group">
                    <button>Login</button>
                </div>
            </form>
        </div>
        <div class="error-container">
            <p class="error-text">{{ errorMessage }}</p>
        </div>
    </div>
</template>