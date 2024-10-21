<script setup>
import axios from "axios";
import { ref } from "vue";

const message = ref("");

function get_data() {
  axios.get('http://127.0.0.1:8000/test/')
    .then((response) => {
      if (response.status === 200) {
        message.value = response.data.info;
      } else {
        console.log("Error");
      }
    })
    .catch(e => {
      console.log("Internal Error");
    })
}

function mock_message() {
  message.value = 'Hello';
}
</script>

<template>
  <div class="container">
    <h2 data-test="title">Data:</h2>
    <div data-test="msg">{{ message }}</div>
    <button data-test="btn" @click="mock_message">Request data</button>
  </div>
</template>

<style scoped>
.container {
  margin: 50px;
}
</style>