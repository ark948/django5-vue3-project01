<script setup>
import DataFromStore from '@/components/bookmarker/DataFromStore.vue';
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';
import Select from 'primevue/select';
import { reactive, ref } from "vue";
import { useBookmarksStore } from '@/stores';
import { prepend_https } from '@/components/bookmarker/utils';

const componentKey = ref(0);
const bookmarkStore = useBookmarksStore();
const new_item_title = ref("");
const new_item_url = ref("");
const new_item_category_id = ref(0);
const all_categories = ref([]);
all_categories.value = bookmarkStore.categories_list;

const new_item_modal_visible = ref(false);

const emit = defineEmits(['reloadThisPage']);
function reloadData() {
    console.log("Refreshing...");
    componentKey.value += 1;
}

async function handleNewItem() {
    const bookmarkStore = useBookmarksStore();
    console.log("Title: ", new_item_title.value);
    console.log("URL: ", new_item_url.value);
    console.log("Category Id:", new_item_category_id.value.id);
    try {
        new_item_url.value = prepend_https(new_item_url.value);
        bookmarkStore.add_item(new_item_title.value, new_item_url.value, new_item_category_id.value.id)
            .catch((e) => {
                console.log(e);
            })
    } catch (e) {
        console.log(e);
    } finally {
        new_item_modal_visible.value = false;
        reloadData();
    }
}
</script>


<template>
    <div class="container">
        <DataFromStore :key="componentKey"/>
        <Dialog v-model:visible="new_item_modal_visible" modal header="Add new">
        <span>Add new bookmark</span>
        <div class="form-container">
            <form action="" @submit.prevent="handleNewItem">
                <label class="form-label" for="title">Title:</label>
                <input class="form-input" v-model="new_item_title" type="text" name="title">
                <label class="form-label" for="url"></label>
                <textarea class="form-input" v-model="new_item_url" name="url" rows="5" cols="50"></textarea>
                <label class="form-input" for="category-select">Category:</label>
                <Select name="category-select" v-model="new_item_category_id" :options="all_categories" optionLabel="title" placeholder="Select a Category" class="w-full md:w-56" />
                <input class="form-button" type="submit" value="Add">
            </form>
        </div>
        <div class="flex justify-end gap-2">
            <Button type="button" label="Cancel" severity="secondary" @click="new_item_modal_visible = false"></Button>
        </div>
    </Dialog>
    <Button class="action-button" label="Add" @click="new_item_modal_visible=true" />
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

</style>