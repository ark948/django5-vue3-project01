<script setup>
    console.log('VerifyEmail');
    
    import { ref } from 'vue'
    import api from '@/api';
    import { useNotification } from '@kyvg/vue3-notification';

    const otp = ref('');
    const messageResponse = ref("")
    const { notify } = useNotification()

    const validateOTP = (otp) => {
        let otp_value = parseInt(otp)
        if (otp_value == NaN || otp_value == "" || otp_value < 100_000 || otp_value > 999_999 || otp_value.toString().length != 6) {
            return 0
        }
        return otp_value
    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        // validation
        let otp_value = validateOTP(otp.value)
        if (otp_value == 0) {
            console.log("Blocked")
            return
        }

        try {
            api.post('auth/verify-email/', { 'otp': otp_value })
                .then(response => {
                    if (response.status === 200) {
                        console.log("200 - Success")
                        // messageResponse.value = response.data.message
                        notify({
                        title: "Email Verification",
                        text: 'Your email was successfully verified. You can now use our app without limitations.'
                        })
                    // router.push({ name: 'login' })
                    } else if (response.status === 204) {
                        console.log("204 - Problem with Code.")
                        messageResponse.value = response.data.message
                    } else if (response.status === 404) {
                        console.log("404 - OTP Not Found.")
                        messageResponse.value = response.data.message
                    } else {
                        console.log("Unknown Error.")
                        messageResponse.value = "Unknown error occurred"
                    }
                })
                .catch(error => {
                    console.log("An error occurred.")
                    messageResponse.value = "Incorrect OTP."
                })
                .finally(() => console.log("_".repeat(50)))
        } catch (error) {
            console.log("Error caught.")
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
    </div>
    <div class="container-message">
        <p>{{ messageResponse }}</p>
    </div>
    <div class="container-link">
        <RouterLink id="back" to='/'>Back to home</RouterLink>
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