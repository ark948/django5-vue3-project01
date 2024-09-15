<script setup>
import { ref, onMounted } from 'vue';
import api from '@/api/api';
import BookmarkEntry from './BookmarkItem.vue';
import { useRouter } from 'vue-router';

const responseHolder = ref("");
const errorHolder = ref("");
const all_bookmarks = ref([])
const insideRouter = useRouter();

// primevue
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import ColumnGroup from 'primevue/columngroup'; // optional
import Row from 'primevue/row'; // optional
import Paginator from 'primevue/paginator';
const selectedItem = ref();

// frontend pagination
// get all data from backend, paginate in frontend
const page_number = ref(1);


onMounted(() => {
    console.log('[BookmarksList.vue] - mounted.')
    get_bookmarks();
})

async function get_bookmarks() {
    console.log("[BookmarksList.vue]");
    console.log("[BookmarksList.vue] Getting the list...");
    // const res = await api.get(`bookmarker/api/?page=${page_number.value}`)
    const res = await api.get('bookmarker/api/no-paginate/')
    .then((response) => {
        if (response.status === 200) {
            console.log("Response 200")
            for (let i=0; i < response.data.length; i++) {
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

}
</script>

<template>
    <div class="card">
        <DataTable 
        v-model:selection="selectedItem" 
        :value="all_bookmarks"
        paginator
        :rows="10"
        :rowsPerPageOptions="[5, 10, 20, 50]"
        showGridlines 
        stripedRows 
        tableStyle="min-width: 50rem">
            <Column selectionMode="multiple" headerStyle="width: 3rem"></Column>
            <Column field="title" header="Title"></Column>
            <Column field="url" header="URL"></Column>
        </DataTable>
    </div>
</template>

<style scoped>

</style>