<script setup>
console.log("Post (test)")
import { ref } from 'vue';
import api from '@/api';
import axios from 'axios';

const answer_input = ref("")
const answer_response = ref("")

function handleSubmit(e) {
    e.preventDefault()
    try {
        const answer = document.getElementById('messageId').value
        if (answer == null || answer == "" || !answer) {
            console.log("Empty answer")
            return
        }
        api.post('http://127.0.0.1:8000/test-post/', { 'message': answer })
            .then(response => {
                document.getElementById('res').innerText = response.data.Answer
                console.log(response.data.Answer)
            })
            .catch(error => console.log(error))
            .finally(() => console.log("-".repeat(30)))
    } catch (error) {
        console.log(error)
    }
}

function sendAsnwer(e) {
    e.preventDefault()
    answer_response.value = ""

    // validation
    if (answer_input.value.length < 1) {
        answer_response.value = "Wrong or empty"
        console.log("request Blocked.")
        return
    }
    
    // submitting
    try {
        api.post('http://127.0.0.1:8000/test-post/', {'message': answer_input.value})
            .then(response => {
                answer_response.value = response.data.Answer
            })
            .catch(error => console.log(error))
            .finally(() => {
                console.log(`END${'='.repeat(30)}END`)
            })
    } catch (error) {
        console.log(error)
    }
    answer_input.value = ""
}

</script>

<template>
    <div class="container">
        <h4>Send test data to baceknd (POST)</h4>
        <form @submit="sendAsnwer" action="">
            <p>
                <label for="messageId">Message:</label>
                <input v-model="answer_input" type="text" name="message" id="messageId">
                <button>Submit</button>
            </p>
        </form>
        <div class="response">
            <p>{{ answer_response }}</p>
        </div>
    </div>
</template>