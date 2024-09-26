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
        
        return authStore.login(email, password)
            .catch(error => console.log('[Login_v4.vue] Error: ', error))
    }

</script>

<template>
    <div>
        <h2>Login</h2>
        <Form @submit="onSubmit" :validation-schema="schema">
            <label for="">Email:</label>
            <Field name="email" type="text" />
            <label for="">Password</label>
            <Field name="password" type="password" />
            <button>Login</button>
        </Form>
        <h4>Do you want to sign up?</h4>
        <p><RouterLink to="/register">Register</RouterLink></p>
        <p><RouterLink to="/forgot-password">Forgot passsword?</RouterLink></p>
    </div>
</template>
