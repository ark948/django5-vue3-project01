<script setup>

// imports
import { onMounted, reactive, watch } from "vue";
import { ref } from 'vue';
import api from "@/api/api";
import { VaDataTable } from "vuestic-ui/web-components";

// bookmarks state variables
const all_bookmarks = ref([]); // used
const selected_item = ref([]);
const test_data_holder = ref("");
const display_selected_items = ref("");
const modal_visible = ref(false);

const columns = [
  { key: "id" },
  { key: "title" },
  { key: "url" },
  { key: 'edit' },
  { key: 'delete'}
]

onMounted(() => {
  console.log("[bookmarksListV2 mounted.]");
  get_all_bookmark_items();
});

watch(
  () => selected_item.value,
  () => {
    console.log(selected_item.value);
    display_selected_items.value = 'Selected items: '
    for (let i in selected_item.value) {
      display_selected_items.value += `${selected_item.value[i]['id']}, `;
      // maybe sort this later
    }
  },
);

watch(
  () => selected_item.value,
  () => {
    if (selected_item.value.length === 0) {
      display_selected_items.value = '';
    }
  },
);


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
          <VaDataTable 
          :items="all_bookmarks" 
          :columns="columns" 
          selectable
          :select-mode="'multiple'"
          v-model="selected_item"
          >
        </VaDataTable>
        </div>
    </div>
    <div class="add-item-modal-container">
      <VaModal v-model="modal_visible" close-button ok-text="Submit">
        some stuff
      </VaModal>
      <VaButton @click="modal_visible = true">Open Modal</VaButton>
    </div>
    <div class="selected-items-container">
      <p>{{ display_selected_items }}</p>
    </div>
    <div class="test-message-container">
      <p></p>
    </div>
  </div>
</template>



<style scoped>
</style>