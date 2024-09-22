<script setup>

// imports
import { onMounted, reactive, watch } from "vue";
import { ref } from 'vue';
import api from "@/api/api";
import { VaDataTable } from "vuestic-ui/web-components";

// bookmarks state variables
const all_bookmarks = ref([]); // used
const selected_item = ref([]);
const message_holder = ref("");
const display_selected_items = ref("");
const add_modal_visible = ref(false);
const edit_modal_visible = ref(false);
const delete_modal_visible = ref(false);
const edit_item = reactive({
  id: 0,
  title: "",
  url: ""
});

const add_item = reactive({
  title: "",
  url: "",
});

const delete_item = reactive({
  id: 0,
  title: "",
  url: "",
})

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
  all_bookmarks.value = [];
    console.log("Aquiring list...");
    const res = await api
      .get("bookmarker/api/no-paginate/")
      .then((response) => {
        if (response.status === 200) {
            console.log('SUCCESS-200')
          for (let i = 0; i < response.data.length; i++) {
            console.log("data added.");
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

function openModalToEditItemById(id) {
  // aquire item id upon selection (done)
  // open modal (done)
  // pre-fill the modal content using the entire id (done)
  // let user edit -> handleEdit
  // send put/patch request upon confirm ()
  const item_id = id['rowData']['id'];
  let entire_item = null;
  edit_modal_visible.value = true;

  entire_item = id['rowData'];

  edit_item.id = item_id;
  edit_item.title = entire_item.title;
  edit_item.url = entire_item.url;
}

function openModalToDeleteItemById(id) {
  console.log("Deleting item...");
  const item_id = id['rowData']['id'];
  delete_item.id = item_id;
  delete_item.title = id['rowData']['title'];
  delete_item.url = id['rowData']['url'];
  delete_modal_visible.value = true;
}

function handleEdit() {
  console.log("Invoking update...");
  const res = api.put(`bookmarker/api/${edit_item.id}/`, { title: edit_item.title, url: edit_item.url})
  .then((response) => {
    if (response.status === 200) {
      console.log("UPDATE SUCCESSFUL.");
      message_holder.value = "Update successful.";
      get_all_bookmark_items();
    } else {
      console.log("NOT 200");
      message_holder.value = "An error occurred. sorry.";
    }
  })
  .catch((error) => {
    console.log(error.message);
  })
  .finally(() => {
    edit_modal_visible.value = false;
  });
}

function handleAdd() {
  console.log("Adding item...")
  message_holder.value = "";
  const res = api.post('bookmarker/api/', { title: add_item.title, url: add_item.url })
  .then((response) => {
    if (response.status === 201) {
      console.log("ADD SUCCESS");
      message_holder.value = "Successfully added item.";
      get_all_bookmark_items();
    } else {
      console.log("NOT 200");
      message_holder.value = "An error occurred. sorry.";
    }
  })
  .catch((error) => {
    console.log(error.message);
    message_holder.value = "There was a problem.";
  })
  .finally(() => {
    add_modal_visible.value = false;
  })
}

function handleDelete() {
  console.log("Deleting item...");
  const res = api.delete(`bookmarker/api/${delete_item.id}/`)
  .then((response) => {
    if (response.status === 204) {
      console.log("DELETE SUCCESS");
      message_holder.value = "Item successfully deleted.";
      get_all_bookmark_items();
    } else {
      console.log("NOT 200");
      message_holder.value = "An error occurred. sorry.";
    }
  })
  .catch((error) => {
    console.log(error.message);
    message_holder.value = "There was a problem.";
  })
  .finally(() => {
    delete_modal_visible.value = false;
  })
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
          :select-mode="'multiple'"
          selectable
          v-model="selected_item"
          >
          <template #cell(edit)="selected_item">
            <VaButton
              preset="plain"
              icon="edit"
              @click="openModalToEditItemById(selected_item)"
            />
          </template>
          <template #cell(delete)="selected_item">
            <VaButton
            preset="plain"
            icon="delete"
            @click="openModalToDeleteItemById(selected_item)"
            />
          </template>
          </VaDataTable>
        </div>
    </div>
    <div class="add-item-modal-container">
      <VaModal v-model="add_modal_visible" close-button ok-text="Submit">
        <form action="" @submit.prevent="handleAdd">
          <label for="title">Title:</label>
          <input type="text" name="title" v-model="add_item.title">
          <label for="url">URL:</label>
          <textarea name="url" id="url" rows="5" cols="50" v-model="add_item.url"></textarea>
          <input type="submit" value="Add">
        </form>
      </VaModal>
      <VaButton @click="add_modal_visible = true">Add manually</VaButton>
    </div>
    <div class="edit-item-modal-container">
      <VaModal v-model="edit_modal_visible" close-button ok-text="OK">
        <form action="" @submit.prevent="handleEdit">
          <label for="title">Title:</label>
          <input type="text" name="title" v-model="edit_item.title">
          <label for="url">URL:</label>
          <textarea name="url" id="url" rows="5" cols="50" v-model="edit_item.url"></textarea>
          <input type="submit" value="Confirm">
        </form>
      </VaModal>
    </div>
    <div class="delete-item-modal-container">
      <VaModal v-model="delete_modal_visible" close-button ok-text="OK">
        <form action="" @submit.prevent="handleDelete">
          <h4>Are you sure about this?</h4>
          <p>{{ delete_item.title }}</p>
          <p>{{ delete_item.url }}</p>
          <input type="submit" value="Confirm">
        </form>
      </VaModal>
    </div>
    <div class="selected-items-container">
      <p>{{ display_selected_items }}</p>
    </div>
    <div class="test-message-container">
      <p>{{ message_holder }}</p>
    </div>
  </div>
</template>



<style scoped>
</style>