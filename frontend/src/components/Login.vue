<script setup>
    console.log("Login")

    import api from '@/api';
    import router from '@/router';
    import { useNotification } from '@kyvg/vue3-notification';
    import { ref, reactive } from 'vue';

    const { notify } = useNotification()
    const loadingIndicator = ref("")
    const responseMessage = ref("")
    const logindata = reactive({
        email: "",
        password: ""
    })

    const handleSubmit = async (e) => {
        e.preventDefault()

        // validation
        const { email, password } = logindata
        if (!email || !password) {
            responseMessage.value = "Both values are required."
            return
        }

        api.post('auth/login/', { email: email, password: password})
            .then(response => {
                console.log(response.status) // 200
                console.log(response.data.access_token)
                notify({
                    title: "Welcome",
                    text: `${response.data.full_name} have successfully logged in.`
                })
                router.push({ name: "home" })
            })
            .catch(error => {
                if (error.response) console.log("response contains error")
                else if (error.request) console.log("no response")
                else console.log("error in setting up the request")
            })
    }

</script>

<template>
    <div class="container">
        <h3>Login</h3>
        <form @submit="handleSubmit" action="" class="form-container">
            <label for="email">Email:</label>
            <input v-model.trim="logindata.email" type="email">
            <label for="password">Password:</label>
            <input v-model="logindata.password" type="password">
            <button>Login</button>
        </form>
    </div>
    <div class="message-container">
        <p>{{ responseMessage }}</p>
    </div>
</template>

<style scoped>

</style>