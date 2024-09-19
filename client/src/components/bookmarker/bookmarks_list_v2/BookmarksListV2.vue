<script setup>
// this component uses Vuetify.js library
// imports
import { onMounted } from "vue";
import { ref } from 'vue';
import api from "@/api/api";
import * as data from '@/components/bookmarker/bookmarks_list_v2/data';
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

// bookmarks state variables
const all_bookmarks = ref([]);
const selected_item = ref(null);
const selected_items = ref([]);
const test_data_holder = ref("");


onMounted(() => {
  console.log("[bookmarksListV2 mounted.]");
  get_all_bookmark_items();
});

// functions
async function get_all_bookmark_items() {
    console.log("Aquiring list...");
    const res = await api
      .get("bookmarker/api/no-paginate/")
      .then((response) => {
        if (response.status === 200) {
            console.log('SUCCESS-200')
          for (let i = 0; i < response.data.length; i++) {
            console.log(response.data[i]);
            all_bookmarks.value.push(response.data[i]);
          }
        } else {
            console.log('ERROR-', response.status);
        }
      })
      .catch((error) => {
        console.log('Error occurred. > ', error.message);
      })
      .finally(() => {
        console.log('Request finished.');
      });
  }

</script>


<template>
  <div class="container">
    <div class="items-container">
      <h3>Your bookmarks:</h3>
        <div class="items-table-container">
          <v-data-table :items="all_bookmarks"></v-data-table>
        </div>
    </div>
    <div class="test-message-container">
      <p></p>
    </div>
  </div>
</template>



<style scoped>
</style>