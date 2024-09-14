<script setup>
console.log("ManualTokenRefresh.vue");
import { ref } from "vue";
import api from "@/api/api"
import { useAuthStore } from "@/stores";

const refresh_input_value = ref("");
const responseHolder = ref("[response place holder]");
const authStore = useAuthStore();
const refresh_token = localStorage.getItem('refresh_token') ? JSON.parse(localStorage.getItem('refresh_token')) : "";

async function handleSubmit() {
  console.log("[..MnTknRrf..vue] Manual refresh form called.");
  const res = await api
    .post("auth/token/refresh/", { refresh: refresh_input_value.value })
    .then((res) => {
      if (res.status === 200) {
        console.log("SUCCESS")
        responseHolder.value = res.data.access;
      }
    })
    .catch((error) => {
      console.log("[..MnTknRfr..vue] resposne returned with error.");
      console.log(error.message);
    });
}

function handleClickPlaceCode() {
  refresh_input_value.value = authStore.refresh_token;
}

function handleClickClear() {
  refresh_input_value.value = "";
}
</script>

<template>
  <div class="container">
    <h3>Manually refresh token:</h3>
    <div class="form-container">
      <form @submit.prevent="handleSubmit" action="">
        Submit your refresh token here:
        <textarea
          v-model="refresh_input_value"
          name="refresh_input"
          rows="5"
          cols="50"
        ></textarea>
        <input type="submit" value="Send" />
      </form>
    </div>
    <div class="store-container">
      <p>Your current refresh token:</p>
      <p style="word-break: break-all">{{ authStore.refresh_token }}</p>
    </div>
    <div class="response-container">
      <p>{{ responseHolder }}</p>
    </div>
    <button @click="handleClickPlaceCode">Place code</button>
    <button @click="handleClickClear">Clear</button>
  </div>
</template>

<style scoped>
.response-container {
  margin: 200px;
  word-break: break-all;
}

.form-container input[type='submit'] {
    margin: 50px;
    border-radius: 8px;
    font-size: 16px;
    border: none;
    width: 120px;
    height: 30px;
    border-color: green;
    cursor: pointer;
    color: rgb(60, 174, 123);
}

button {
    margin: 20px;
    border-radius: 8px;
    font-size: 16px;
    border: none;
    width: 120px;
    height: 30px;
    border-color: green;
    cursor: pointer;
    color: rgb(60, 174, 123);
}
</style>