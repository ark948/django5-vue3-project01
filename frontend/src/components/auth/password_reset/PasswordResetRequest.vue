<script setup>

    async function handleSubmit() {
        console.log("Sending request...");
    }


</script>


<template>
    <div class="container">
        <div class="form-container">
            <div class="password-reset-request-container">
                <div class="password-reset-request-form-container">
                    <form onsubmit.prevent="handleSubmit">
                        Enter your email:
                        <input type="email">
                        <input type="submit" value="Send request">
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>


<style scoped>

</style>