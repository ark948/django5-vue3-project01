<script setup>
    import { ref, watch } from 'vue';
    import { useRoute } from 'vue-router';
    import router from '@/router';
    import api from '@/api/api';

    console.log("Reset Form.");

    const route = useRoute();
    const uidb64 = ref("");
    const token = ref("");
    const responseHolder = ref("");

    const password_input = ref("");
    const password_confirm_input = ref("");

    uidb64.value = router.currentRoute.value.params['uidb64'];
    token.value = router.currentRoute.value.params['token'];

    watch(
        () => route.params.id,
        () => {
            console.log("Route changed.");
        }
    )

    function handleSubmit() {
        console.log("Sending request...");
        const password = password_input.value;
        const confirm_password = password_confirm_input.value;
        const uidb64_input = uidb64.value;
        const token_input = token.value;

        const res = api.patch('auth/set-new-password/', 
            {
                password: password,
                confirm_password: confirm_password,
                uidb64: uidb64_input,
                token: token_input,
            }
        )
        .then((response) => {
            if (response.status === 200) {
                console.log("Success.");
                responseHolder.value = "Your password has been successfully changed. \nPlease login with your new password.";
            } else {
                console.log("NOT 200");
                responseHolder.value = "An error occurred.";
            }
        })
        .catch(
            (err) => {
                console.log("ERROR: ", err.message);
                responseHolder.value = "An error occurred.";
            }
        )
        .finally(() => { console.log("done.") });
    }
</script>


<template>
    <div class="container">
        <div class="form-container">
            <div class="password-reset-form-container">
                <form @submit.prevent="handleSubmit">
                    <label for="newPassword">New Password:</label>
                    <input v-model="password_input" type="password" name="newPassword" id="new_password">
                    <label for="NewPasswordConfirm">Confirm Password:</label>
                    <input v-model="password_confirm_input" type="password" name="NewPasswordConfirm" id="new_password_confirm">
                    <input type="submit" value="Confirm">
                </form>
            </div>
        </div>
        <div class="info-container">
            <p>uidb64 {{ $route.params.uidb64 }}</p>
            <p>Token: {{ $route.params.token }}</p>
            ----------------***----------------
            <p>uidb64 {{ uidb64 }}</p>
            <p>Token: {{  token }}</p>
        </div>
        <div class="response-message-container">
            <p>{{ responseHolder }}</p>
        </div>
        <div class="link-container">
            <RouterLink id="back" to='/'>Home</RouterLink>
            <RouterLink to="/login">Login</RouterLink>
        </div>
    </div>
</template>


<style scoped>
.response-message-container p {
    font-weight: bold;
}
</style>