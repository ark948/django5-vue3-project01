<script>
    import {useUserStore} from "../store/user";
    export default {
        mounted() {
            console.log('Login_v3 - mounted.')
        },
        
        setup() {
            const userStore = useUserStore()
            return {
                userStore
            };
        },
        
        data() {
            return {
                email: "",
                password: "",
                response: "",
            };
        },
        

        methods: {
            async handleLogin() {
                console.log("[Login_v2] handleLogin called.")
                await this.userStore.login(this.email, this.password)
            },
        },
    }

</script>

<template>
    <div class="container">
        <form @submit.prevent="handleLogin">
            Email: <input type="email" name="email" v-model="email">
            <br>
            Password: <input type="password" name="password" v-model="password">
            <button type="submit">Login</button>
        </form>
        <p>{{ response }}</p>
    </div>
</template>