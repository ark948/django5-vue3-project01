<script setup>
    import { ref } from 'vue';
    import api from '@/api';

    // not used yet
    const message_input = ref("")

    function handleSubmit(e) {
        e.preventDefault()
        try {
            const answer = document.getElementById('messageId').value
            if (answer == null || answer == "" || !answer) {
                console.log("Empty answer")
                return
            }
        api.post('http://127.0.0.1:8000/test-post/', {'message': answer})
            .then((response) => {
                document.getElementById('res').innerText = response.data.Answer
                console.log(response.data.Answer)
            })
            .catch((error) => console.log(error))
            .finally(() => console.log("-".repeat(30)))
        } catch (error) {
            console.log(error)
        }
    }
</script>

<template>
    <div class="container">
        <h4>Send test data to baceknd (POST)</h4>
        <form @submit="handleSubmit" action="">
            <p>
                <label for="messageId">Message:</label>
                <input type="text" name="message" id="messageId">
                <button>Submit</button>
            </p>
        </form>
        <div class="response">
            <p id="res"></p>
        </div>
    </div>
</template>