<script setup>
import { onMounted, inject, ref, reactive, watch } from 'vue';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Button from 'primevue/button';
import Toast from 'primevue/toast';
import { useToast } from 'primevue/usetoast';
import { notify } from '@kyvg/vue3-notification';

const toast = useToast();
import api from '@/api/api';
import { useAuthStore } from '@/stores';
import router from '@/router';

const emit = defineEmits(['done'])


const dialogRef = inject('dialogRef');
const item = ref();
const selectedItem = ref([]);

const closeDialog = () => {
    dialogRef.value.close();
}

const records = ref([]);
const records2 = ref([]);
const snigle_item = {
    'title': '',
    'url': '',
    'category_id': 0,
    'icon': null
}
let bookmarks = {};


watch(() => selectedItem.value, async () => {
    console.log("items selected: --> ", selectedItem.value);
})


onMounted(() => {
    console.log(selectedItem.value);
    onFileSelect(csv_file.value);
})

const params = dialogRef.value.data;
const csv_file = ref(params.csv_file);

function onFileSelect(file) {
    const reader = new FileReader();

    reader.onload = (e) => {
        item.value = e.target.result;
        // console.log("1. --> ", item.value);
        item.value = item.value.split(/\r?\n/);
        // console.log('--> ', item.value);
        for (let i=0; i < item.value.length-1; i++) {
            // console.log(`item ${i} --> `, item.value[i]);
            if (i === 0) continue; // remove first line if csv file (headers)
            records.value.push(item.value[i]);
        }
        loop_done();
    };

    reader.readAsText(file);
}

function loop_done() {
    for (let i = 0; i<records.value.length; i++) {
        // console.log(`item ${i} --> `, typeof(records.value[i])); string -> array
        // console.log(`item ${i} --> `, records.value[i].split(','));
        records.value[i] = records.value[i].split(',');
        // console.log(`item ${i} --> `, records.value[i]); removing outer string
    }

    records.value.forEach((value, index, arr) => {
        // REMOVING OUTER STRING QUOTES
        // console.log("title: ",arr[index][1]);
        arr[index][1] = arr[index][1].slice(1, -1); // remove outer string for title
        arr[index][2] = arr[index][2].slice(1, -1); // and for url
        arr[index][3] = arr[index][3].slice(1, -1); // and for category
    });
    // console.log("item: ", bookmarks);

    records.value.forEach((value, index, arr) => {
        // FIXING Category (replacing text with category id)
        // console.log("Categories: --> ", arr[index][3]);
        switch (arr[index][3]) {
            case "Work":
                arr[index][3] = 1;
                break;
            case "Entertainment":
                arr[index][3] = 2;
                break;
            case "Useful":
                arr[index][3] = 3;
                break;
            default:
                arr[index][3] = "-";
        }
    })

}


function processImportRequest() {
    if (selectedItem.value.length == 0) {
        notify({
            title: "خطا.",
            text: "هیج آیتمی انتخاب نشد."
        });
        closeDialog();
    }
    const authStore = useAuthStore()
    const authStr = `Bearer ${authStore.access_token}`
    for (let i = 0; i < selectedItem.value.length; i++) {
        console.log("Inserting item...");
        api.post('bookmarker/api/no-paginate/', { title: selectedItem.value[i][1], url: selectedItem.value[i][2], category_id: selectedItem.value[i][3]}, { headers: {Authorization: authStr}})
            .then((response) => {
                if (response.status === 201) {
                    console.log("Successful.");
                } else {
                    console.log("Error");
                }
            })
            .catch(e => {
                console.log("Error: --> ", e.message);
            });
    }
    closeDialog();
    // router.push('/bookmarks-list'); not working
}

function importAll() {
    return 0;
}

</script>



<template>
    <div class="container">
        <h2>Select bookmarks to import</h2>
        <DataTable 
        :value="records"
        v-model:selection="selectedItem"
        >
            <Column selectionMode="multiple"></Column>
            <Column field="1" header="Title"></Column>
            <Column field="2" header="URL"></Column>
            <Column field="3" header="Category"></Column>
        </DataTable>
        <Button style="height: 30px; margin: 30px;" @click="closeDialog" label="Close" />
        <Button style="height: 30px; margin: 30px" type="button" label="Confirm" @click="processImportRequest" />
        <Button style="height: 30px; margin: 30px;" type="button" label="Import All" @click="importAll" />
    </div>
</template>