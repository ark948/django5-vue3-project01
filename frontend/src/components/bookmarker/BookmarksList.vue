<script setup>

// vue imports
import { ref, onMounted, reactive, watch, provide } from "vue";

// 3rd party imports
import Select from "primevue/select";
import Dialog from "primevue/dialog";
import Button from "primevue/button";
import { useToast } from 'primevue/usetoast';

// local imports
import { useAuthStore } from "@/stores";
import api from '@/api/api';
import * as utils from '@/components/bookmarker/utils.js';
import router from "@/router";
import Table from "@/components/bookmarker/data_table/Table.vue";
import Toast from "primevue/toast";
import FileUpload from 'primevue/fileupload';

// events
const emit = defineEmits(['reloadThisList']);

// refs
const responseHolder = ref("");
const refreshTableKey = ref(0);
const all_bookmarks = ref([]);
const fileupload = ref();
// get all data from backend, paginate in frontend
const page_number = ref(1);
// new bookmark item functionality
const visible = ref(false);
const new_item_title = ref("");
const new_item_url = ref("");
// delete functionality
const selected_items = ref([]);
// delete confirm dialog
const confirm = ref(false);
// Category
const all_categories = ref([]);
const selectedCategory = ref({id:0, title:''});
const edit_modal_visible = ref(false);
const fileInput = ref(null);
const files = ref();
const sizeOptions = ref([
    { label: 'Small', value: 'small' },
    { label: 'Normal', value: 'null' },
    { label: 'Large', value: 'large' }
]);
const edit_item = reactive({
  id: 0,
  title: "",
  url: "",
  category_id: 0,
});


const toast = useToast();
const showSuccess = () => {
    toast.add({ severity: 'success', summary: 'عملیات موفق', detail: 'عملیات با موفقیت انجام شد.', life: 3000 });
};
const onUpload = () => {
    toast.add({ severity: 'info', summary: 'آپلود فایل', detail: 'فایل با موفقیت دریافت شد.', life: 3000 });
};


onMounted(() => {
  setTimeout(() => {
    get_bookmarks();
    get_categories();
  }, 300);
});

// watchers
watch(
  () => selected_items.value,
  async () => {
    document.getElementById('del_btn').disabled = false;
    responseHolder.value = "Selected items: ";
    for (let i in selected_items.value) {
      responseHolder.value += `${selected_items.value[i].count}, `;
    }
  }
)

const forceRerender = () => {
  refreshTableKey.value += 1;
};


// manual auth header added
function get_categories() {
  const authStore = useAuthStore();
  const authStr = `Bearer ${authStore.access_token}`;
  api.get('bookmarker/api/category-list/', { headers: { Authorization: authStr}})
    .then(response => {
      if (response.status === 200) {
        for (let i = 0; i < response.data.length; i++) {
          all_categories.value.push(response.data[i]);
        }
      } else {
        console.log("Categories list NOT 200.", response.status);
      }
    })
    .catch(error => {
      console.log("Error", error.message);
    })
}


// manual auth header added
function get_bookmarks() {
  console.log("[BookmarksList.vue] Getting the list...");
  // const res = await api.get(`bookmarker/api/?page=${page_number.value}`)
  const authStore = useAuthStore()
  const authStr = `Bearer ${authStore.access_token}`
  api.get('bookmarker/api/no-paginate/', { headers: {Authorization: authStr}})
    .then((response) => {
      if (response.status === 200) {
        console.log("Response 200");
        let count = 1;
        for (let i = 0; i < response.data.length; i++) {
          response.data[i].count = count;
          all_bookmarks.value.push(response.data[i]);
          count++;
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
      // replacing category ids with actual category title (not anymore, this got updated)
    });
};


// manual auth header added
async function handleNewBookmarkSubmit() {
    const authStore = useAuthStore()
    const authStr = `Bearer ${authStore.access_token}`
    console.log("[BookmarksList.vue] Adding new...");
    responseHolder.value = "";
    new_item_url.value = utils.prepend_https(new_item_url.value);
    await api.post('bookmarker/api/no-paginate/', { title: new_item_title.value, url: new_item_url.value, category_id: selectedCategory.value.id }, { headers: {Authorization: authStr}})
    .then((response) => {
        if (response.status === 201) {
            console.log('[BookmarksList.vue] New item successfully added.');
            showSuccess();
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


// manual auth header added
async function handleMultipleDeletion() {
  console.log("Performing mulitple deletion...");
  const authStore = useAuthStore()
  const authStr = `Bearer ${authStore.access_token}`
  let selected = [];
  for (let i in selected_items.value) {
    selected.push(selected_items.value[i]['id'])
  }
  selected = selected.toString();
  await api.post('bookmarker/api/multiple-delete/', { list_of_ids: selected }, { headers: {Authorization: authStr}})
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
      all_bookmarks.value.length = 0
      confirm.value = false;
      get_bookmarks();
      clearDeleteInput();
      forceRerender();
    });
}


function editItem(item) {
  edit_item.id = item.id;
  edit_item.title = item.title;
  edit_item.url = item.url;
  edit_item.category_id = item.category_id;
  edit_modal_visible.value = true;
}


// process: editItem -> edit_modal_visible -> handleEdit
// manual auth header added
function handleEdit() {
  console.log("Invoking update...");
  const authStore = useAuthStore()
  const authStr = `Bearer ${authStore.access_token}`
  api.put(`bookmarker/api/${edit_item.id}/`, { title: edit_item.title, url: edit_item.url, category_id: selectedCategory.value.id }, { headers: {Authorization: authStr}})
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


// manual auth header added
function confirmDeleteProduct(item) {
  const authStore = useAuthStore()
  const authStr = `Bearer ${authStore.access_token}`
  api.delete(`bookmarker/api/${item['id']}/`, { headers: {Authorization: authStr}})
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

function handleFileChange() {
  files.value = fileInput.value?.files
}


// manual auth header added
function handleCSVImport(file) {
  const authStore = useAuthStore()
  const authStr = `Bearer ${authStore.access_token}`
  const formData = new FormData();
  formData.append("uploaded_file", file);
  console.log("Sending file...");
  api.post('bookmarker/api/file-upload/', formData, {
    headers: {
      Authorization: authStr,
      "Content-Type": 'multipart/form-data'
    }
  })
    .then((response) => {
      if (response.status === 200) {
        toast.add({ severity: 'success', summary: 'فایل دریافت شد.', detail: 'فایل با موفقیت دریافت شد.', life: 3000});
      } else {
        console.log("NOT 200");
      }
    })
    .catch((e) => {
      toast.add({ severity: 'error', summary: 'خطا', detail: 'خطایی در دریافت فایل رخ داد.', life: 3000})
    })
    .finally(() => {
      console.log("CSV import done. Refreshing table now...");
      all_bookmarks.value.length = 0;
      get_bookmarks();
    })
}


function handleReload() {
  console.log("Reloading ...");
  fileupload.value = null;
  router.push({ name: 'bookmarks' });
}

const onClearTemplatingUpload = (clear) => {
    clear();
    totalSize.value = 0;
    totalSizePercent.value = 0;
};


function clearDeleteInput() {
  document.getElementById('del_btn').disabled = true;
  responseHolder.value = '';
}


const upload = () => {
    // handleCSVImport(fileupload.value.files[0]);
    // fileupload.value = null;
    // upload data to CsvImport by using provide and inject
    openCsvDialog();

};


// dynammic dialog
// can load a second component
import DynamicDialog from 'primevue/dynamicdialog';
import { useDialog } from 'primevue/usedialog';
import CsvImport from "./data_table/CsvImport.vue";

const dialog = useDialog();

const openCsvDialog = () => {
  if (fileupload.value.files[0] === undefined) {
    toast.add({ severity: 'error', summary: 'خطا', detail: '.فایلی انتخاب نشده است', life: 3000});
    return
  }
  dialog.open(CsvImport, {
    data: {
      csv_file: fileupload.value.files[0]
    },
    onClose: (e) => {
      emit('reloadThisList');
    }
  });
}

</script>



<template>
  <div class="container">
    <div class="notification-container">
      <Toast />
    </div>
    <div class="card">
      <Table
      :key="refreshTableKey"
      :data="all_bookmarks" 
      @editItem="(item) => editItem(item)" 
      @confirmDeleteItem="(item) => confirmDeleteProduct(item)"
      @Selected="(items) => selected_items = items"
      @SelectedIsEmpty="() => clearDeleteInput()"
      @DeleteSingleItem="(item) => confirmDeleteProduct(item)"
      @editSingleItem="(item) => editItem(item)"
      />
    </div>
    <div class="response-message-container">
      <p>{{ responseHolder }}</p>
    </div>
    <Dialog v-model:visible="visible" modal header="Add new">
        <span>Add new bookmark</span>
        <div class="form-container">
            <form action="" @submit.prevent="handleNewBookmarkSubmit">
                <label class="form-label" for="title">Title:</label>
                <input class="form-input" v-model="new_item_title" type="text" name="title">
                <label class="form-label" for="url"></label>
                <textarea class="form-input" v-model="new_item_url" name="url" rows="5" cols="50"></textarea>
                <label class="form-input" for="category-select">Category:</label>
                <Select name="category-select" v-model="selectedCategory" :options="all_categories" optionLabel="title" placeholder="Select a Category" class="w-full md:w-56" />
                <input class="form-button" type="submit" value="Add">
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
          <label class="form-label" for="title">Title:</label>
          <input class="form-input" type="text" name="title" v-model="edit_item.title">
          <label class="form-label" for="url">URL:</label>
          <textarea class="form-input" name="url" id="url" rows="5" cols="50" v-model="edit_item.url"></textarea>
          Current Category: {{ edit_item.category_id }}
          <br>
          Set New Category <Select name="category-select" v-model="selectedCategory" :options="all_categories" optionLabel="title" placeholder="Select a Category" class="w-full md:w-56" />
          <input class="form-button" type="submit" value="Confirm">
        </form>
    </Dialog>
    <DynamicDialog />
    <Button class="action-button" label="Add" @click="visible=true" />
    <Button class="action-button" @click="confirm=true" id="del_btn" label="Delete" disabled></Button>
    <div class="file-upload-form-container">
      Import from CSV file:
      <FileUpload ref="fileupload" mode="basic" accept=".csv" :maxFileSize="1000000" @upload="onUpload" style="height: 30px;"/>
      <Button id="fileUploadBtn" class="action-button" label="Upload" @click="upload" severity="secondary"/>
    </div>
    <Button class="action-button" label="Reload" @click="handleReload" />
  </div>
</template>



<style scoped>
    .form-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: 50px auto;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        max-width: 400px;
    }

    .form-input {
        width: 100%;
        padding: 8px;
        margin: 10px 0;
        border: 1px solid #42B883;
        border-radius: 8px;
        box-sizing: border-box;
    }

    .form-label {
        font-size: 15px;
        padding: 10px;
    }

    .form-button {
        width: 100%;
        padding: 10px;
        margin: 20px 0;
        background-color: #42B883;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.2s ease-in-out;
        font-size: 15px;
    }

    .form-button:hover {
        background-color: #0056b3;
    }

    .action-button {
      width: 70px;
      height: 30px;
      margin: 20px 5px;
      padding: 10px;
    }

    .p-datatable-table {
      width: 100%;
      border-spacing: 0;
      font-size: 1px;
    }
</style>