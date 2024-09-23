<script setup>
// this component uses PrimeVue library
import { ref, onMounted, reactive } from "vue";
import api from "@/api/api";
import { useRouter } from "vue-router";

const responseHolder = ref("");
const errorHolder = ref("");
const all_bookmarks = ref([]);
const insideRouter = useRouter();

// primevue
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import ColumnGroup from "primevue/columngroup"; // optional
import Row from "primevue/row"; // optional
import Paginator from "primevue/paginator";

const selectedItem = ref();

// frontend pagination
// get all data from backend, paginate in frontend
const page_number = ref(1);

// new bookmark item functionality
import Dialog from "primevue/dialog";
import Button from "primevue/button";
const visible = ref(false);
const new_item_title = ref("");
const new_item_url = ref("");

// delete functionality
const selected_items = ref([]);
import { watch } from "vue";

// delete confirm dialog
const confirm = ref(false);

watch(() => selectedItem.value, async () => {
    document.getElementById('del_btn').disabled = false;
    responseHolder.value = "Selected items: ";
    for (let i in selectedItem.value) {
      responseHolder.value += `${selectedItem.value[i].id}, `;
    }
  }
);

watch(() => selectedItem.value, async () => {
    if (selectedItem.value.length === 0) {
      document.getElementById('del_btn').disabled = true;
      responseHolder.value = "";
    }
  }
);

onMounted(() => {
  console.log("[BookmarksList.vue] - mounted.");
  get_bookmarks();
});

async function get_bookmarks() {
  console.log("[BookmarksList.vue] Getting the list...");
  // const res = await api.get(`bookmarker/api/?page=${page_number.value}`)
  const res = await api
    .get("bookmarker/api/no-paginate/")
    .then((response) => {
      if (response.status === 200) {
        console.log("Response 200");
        for (let i = 0; i < response.data.length; i++) {
          // console.log(response.data[i]);
          all_bookmarks.value.push(response.data[i]);
        }
      } else {
        console.log("[BookmarksList.vue] Response NOT 200", response.status);
      }
    })
    .catch((error) => {
      console.log("ERROR");
      console.log(`[BookmarksList.vue] => ${error.message}`);
    })
    .finally(() => {
      console.log(`Total of ${all_bookmarks.value.length} items.`);
    });
};

async function handleNewBookmarkSubmit() {
    console.log("[BookmarksList.vue] Adding new...");
    responseHolder.value = "";
    const res = await api.post('bookmarker/api/no-paginate/', { title: new_item_title.value, url: new_item_url.value })
    .then((response) => {
        if (response.status === 201) {
            console.log('[BookmarksList.vue] New item successfully added.');
        } else {
            console.log("ERROR IN ADDING NEW ITEM.");
            visible.value = false;
            responseHolder.value = "Something went wrong...";
        }
    })
    .catch((error) => {
      console.log("ERROR IN ADDING NEW ITEM (2)");
      console.log(`[BookmarksList.vue] => ${error.message}`);
    })
    .finally(() => {
      console.log("REFRESHING THE TABLE NOW...");
      all_bookmarks.value.length = 0;
      get_bookmarks();
      visible.value = false;
      new_item_title.value = "";
      new_item_url.value = "";
    });
}

async function handleSingleDeletion() {
  console.log("Performing Delete request (Single)...");
  for (let i in selectedItem.value) {
    console.log(`Deleting item ${selectedItem.value[i].id}`)
    const res = await api.delete(`bookmarker/api/${selectedItem.value[i].id}/`)
    .then((response) => {
      if (response.status === 204) {
        console.log("Delete OK");
      } else {
        console.log("Delete Not OK");
      }
    })
    .catch((e) => {
      console.log("Delete Error");
      console.log(e.message);
    })
    .finally(() => {
      console.log("Delete process complete for one item.");
    });
  }
    console.log("REFRESHING THE TABLE NOW...");
    all_bookmarks.value.length = 0;
    get_bookmarks();
    visible.value = false;
}

async function handleMultipleDeletion() {
  console.log("Performing mulitple deletion...");
  let selected = [];
  for (let i in selectedItem.value) {
    selected.push(selectedItem.value[i]['id'])
  }
  selected = selected.toString();
  const res = api.post('bookmarker/api/multiple-delete/', { list_of_ids: selected })
    .then((response) => {
      console.log("Sending request...");
      if (response.status === 200) {
        console.log("Multiple Delete OK");
      } else {
        console.log("Response code not 200")
      }
    })
    .catch((e) => {
      console.log("Delete Error");
      console.log(e.message);
    })
    .finally(() => {
      console.log("Request complete.");
      console.log("REFRESHING THE TABLE NOW...");
      all_bookmarks.value.length = 0;
      get_bookmarks();
      confirm.value = false;
    });
}

const dt = ref();

const exportCSV = async () => {
  dt.value.exportCSV();
}

const shit = ref('fuck');
import { FilterMatchMode } from '@primevue/core/api';
import { useToast } from 'primevue/usetoast';

function getstuff(item) {
  console.log(item);
}

const edit_modal_visible = ref(false);
const edit_item = reactive({
  id: 0,
  title: "",
  url: ""
});
function editItem(item) {
  edit_item.id = item.id;
  edit_item.title = item.title;
  edit_item.url = item.url;
  edit_modal_visible.value = true;
}

function handleEdit() {
  console.log("Invoking update...");
  const res = api.put(`bookmarker/api/${edit_item.id}/`, { title: edit_item.title, url: edit_item.url})
  .then((response) => {
    if (response.status === 200) {
      console.log("UPDATE SUCCESSFUL.");
      responseHolder.value = "Update successful.";
    } else {
      console.log("NOT 200");
      responseHolder.value = "An error occurred. sorry.";
    }
  })
  .catch((error) => {
    console.log(error.message);
  })
  .finally(() => {
    console.log("Edit complete. Refreshing now...");
    all_bookmarks.value.length = 0;
    get_bookmarks();
    edit_modal_visible.value = false;
  });
}

function confirmDeleteProduct(item) {
  const res = api.delete(`bookmarker/api/${item['id']}/`)
    .then((response) => {
      if (response.status === 204 || response.status === 200) {
        console.log("Delete successful = 200 or 204");
      } else {
        console.log("NOT 200 or 204");
        responseHolder.value = 'An error occurred.';
      }
    })
    .catch((e) => {
      console.log(e.message);
    })
    .finally(() => {
      console.log("Single delete complete. Refreshing now...");
      all_bookmarks.value.length = 0;
      get_bookmarks();
    })
}
</script>

<template>
  <div class="container">
    <div class="card">
      <DataTable
        v-model:selection="selectedItem"
        :value="all_bookmarks"
        ref="dt"
        paginator
        :rows="10"
        :rowsPerPageOptions="[5, 10, 20, 50]"
        showGridlines
        stripedRows
        :size="'small'"
        dataKey="id"
        tableStyle="min-width: 50rem"
        steteStorage="local"
        >
        <Column selectionMode="multiple" headerStyle="width: 3rem"></Column>
        <Column field="title" header="Title"></Column>
        <Column field="url" header="URL"></Column>
        <Column field="icon" header="Icon"></Column>
        <Column :exportable="false" style="min-width: 12rem">
          <template #body="slotProps">
            <Button label="Edit" outlined rounded class="mr-2" @click="editItem(slotProps.data)" />
            <Button label="Delete" outlined rounded severity="danger" @click="confirmDeleteProduct(slotProps.data)" />
          </template>
        </Column>
        <template #footer>
          <div style="text-align: right">
            <Button icon="pi pi-external-link" label="Export" @click="exportCSV($event)" />
          </div>
        </template>
      </DataTable>
    </div>
    <div class="response-message-container">
      <p>{{ responseHolder }}</p>
    </div>
    <Dialog v-model:visible="visible" modal header="Add new">
        <span>Add new bookmark</span>
        <div class="form-container">
            <form action="" @submit.prevent="handleNewBookmarkSubmit">
                <label for="title">Title:</label>
                <input v-model="new_item_title" type="text" name="title">
                <label for="url"></label>
                <textarea v-model="new_item_url" name="url" rows="5" cols="50"></textarea>
                <input type="submit" value="Add">
            </form>
        </div>
        <div class="flex justify-end gap-2">
            <Button type="button" label="Cancel" severity="secondary" @click="visible = false"></Button>
            <Button type="button" label="Save" @click="visible = false"></Button>
        </div>
    </Dialog>
    <Dialog v-model:visible="confirm">
        <span>Are you sure about this?</span>
        <div class="flex justify-end gap-2">
          <Button type="button" label="Confirm" @click="handleMultipleDeletion"></Button>
          <Button type="button" label="Cancel" severity="secondary" @click="confirm = false"></Button>
        </div>
    </Dialog>
    <Dialog v-model:visible="edit_modal_visible">
      <form action="" @submit.prevent="handleEdit">
          <label for="title">Title:</label>
          <input type="text" name="title" v-model="edit_item.title">
          <label for="url">URL:</label>
          <textarea name="url" id="url" rows="5" cols="50" v-model="edit_item.url"></textarea>
          <input type="submit" value="Confirm">
        </form>
    </Dialog>
    <Button label="Add" @click="visible=true" />
    <Button @click="confirm=true" id="del_btn" label="Delete" disabled></Button>
  </div>
</template>

<style scoped>
Button {
  height: 30px;
}
.form-container form {
    padding: 20px;
    margin: 30px;
}

.form-container form input[type='text'] {
    margin: 20px;
    width: 300px;
}

.form-container form input textarea {
    margin: 20px;
}

.form-container form input[type='submit'] {
    margin-left: 20px;
    width: 80px;
}
</style>