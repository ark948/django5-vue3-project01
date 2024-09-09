<script setup>
import api from "@/api";
import { ref } from "vue";

const message = ref("");

function get_data() {
  try {
    api
      .get("test/")
      .then((response) => {
        console.log("Success");
        message.value = response.data.info;
      })
      .catch((error) => console.log(error))
      .finally(() => console.log("Done"));
  } catch (error) {
    console.log(error);
  }
}
</script>

<template>
  <div class="container">
    <h2>Data:</h2>
    <div class="data">{{ message }}</div>
    <button @click="get_data">Request data</button>
    <div class="link-container">
      <RouterLink id="back" to="/">Back to home</RouterLink>
    </div>
  </div>
</template>

<style scoped>
.container {
  margin: 50px;
}
</style>