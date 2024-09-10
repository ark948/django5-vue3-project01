<script setup>
    console.log("Login")

    import api from '@/api';
    import router from '@/router';
    import { useNotification } from '@kyvg/vue3-notification';
    import { ref, reactive } from 'vue';
    // import useUserStore from '../store/user'

    
    const { notify } = useNotification()
    const loadingIndicator = ref("")
    const responseMessage = ref("")
    const logindata = reactive({
        email: "",
        password: ""
    })
    const user = reactive({
        email: "",
        full_name: ""
    })
    const access_token = ref("")
    const refresh_token = ref("")

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
                if (response.status === 200) {
                    // double checking status code
                    user.email = response.data.email
                    user.full_name = response.data.full_name
                    localStorage.setItem("user", JSON.stringify(user))
                    localStorage.setItem("access", JSON.stringify(response.data.access_token))
                    localStorage.setItem("refresh", JSON.stringify(response.data.refresh_token))
                }
                notify({
                    title: "Welcome",
                    text: `${response.data.full_name} have successfully logged in.`
                })
                router.push({ name: "profile" })
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
        <div class="message-container">
            <p>{{ responseMessage }}</p>
        </div>
        <div class="link-container">
            <RouterLink id="back" to='/'>Back to home</RouterLink>
        </div>
    </div>
</template>

<style scoped>

</style>