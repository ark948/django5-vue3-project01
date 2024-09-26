<script setup>
    import api from '@/api/api';
    import { ref } from 'vue';
    import router from '@/router';

    const email = ref("");
    const responseMessage = ref("");

    async function handleSubmit() {
        console.log("Sending request...");

        const email_input = email.value;
        const res = api.post('auth/password-reset/', { email: email_input })
            .then((response) => {
                if (response.status === 200) {
                    console.log("Success.");
                    responseMessage.value = "Please check your email for reset link.";
                    // router.push({ name: 'reset_password' });
                } else {
                    console.log("NOT 200");
                    responseMessage.value = "An error occurred. Sorry. Please try again in a few minutes.";
                }
            })
            .catch(
                (error) => {
                    console.log("ERROR: ", error.message);
                    responseMessage.value = "An error occurred. Sorry. Please try again in a few minutes.";
                }
            )
            .finally(() => { console.log("Request complete.") });

    }


</script>


<template>
    <div class="container">
        <div class="form-container">
            <div class="password-reset-request-container">
                <div class="password-reset-request-form-container">
                    <form @submit.prevent="handleSubmit">
                        Enter your email:
                        <input v-model="email" type="email" id="email" name="email">
                        <input type="submit" value="Send request">
                    </form>
                </div>
            </div>
        </div>
        <div class="message-container">
            <p>
                {{ responseMessage }}
            </p>
        </div>
    </div>
</template>


<style scoped>

</style>