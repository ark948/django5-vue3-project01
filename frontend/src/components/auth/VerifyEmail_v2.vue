<script setup>
    console.log('VerifyEmail');
    
    import { ref } from 'vue'
    import api from '@/api/api';
    import { useNotification } from '@kyvg/vue3-notification';
    import router from '@/router';

    const otp = ref('');
    const messageResponse = ref("")
    const { notify } = useNotification()

    const handleSubmit = async (e) => {
        e.preventDefault()

        // validation
        let otp_value = parseInt(otp.value)

        if (otp_value < 100_000 || otp_value > 999_999 || otp_value == NaN || otp_value.toString().length < 6) {
            messageResponse.value = "Incorrect value"
            return
        }

        const response = await api.post('auth/api/verify-email/', { 'otp' : otp_value })
        if (response.status === 200) {
            notify({
                title: "Thank you.",
                text: response.data.message
            })
            router.push({ name: 'home' })
        } else if (response.status === 204) {
            messageResponse.value = "204"
            otp.value = ""
        } else if (response.status === 404) {
            messageResponse.value = "404"
            otp.value = ""
        } else {
            messageResponse.value = response.data.message
            otp.value = ""
        }
    }
    
</script>

<template>
    <div class="container">
        <h3>Enter your OTP code to verify email:</h3>
        <form  @submit="handleSubmit" action="" class="form-container">
            <label for="otp">OTP:</label>
            <input v-model.trim="otp" type="number" name="otp">
            <button>Send</button>
        </form>
        <div class="container-message">
            <p>{{ messageResponse }}</p>
        </div>
        <div class="container-link">
            <RouterLink id="back" to='/'>Back to home</RouterLink>
        </div>
    </div>
</template>

<style scoped>
    .container {
        display: flex;  
        justify-content: center;  
        align-items: center;
        margin: 20px;
    }

    .container form {
        display: flex;
        flex-direction: row;
        justify-content: center;
        width: 100%;
    }

    .container form label {
        font-weight: 500;
    }

    .container input {
        width: 100%;
        border-radius: 16px;
        padding: 10px;
        border: 2px solid #42B883;
        margin-top: 20px;
    }

    .container button {
        width: 200px;
        height: 30px;
        border-radius: 8px;
        background-color: #42B883;
    }
    
</style>