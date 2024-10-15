<script setup>

// vue imports
import { onMounted, ref, watch } from 'vue';

// 3rd party imports
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import { RouterLink } from 'vue-router';
import Button from 'primevue/button';
import { FilterMatchMode } from '@primevue/core/api';
import IconField from 'primevue/iconfield';
import InputIcon from 'primevue/inputicon';
import InputText from 'primevue/inputtext';


const props = defineProps(['data']);
const data = props.data;
const selectedItem = ref([]);
const infos = ref("");
const loading = ref(true);
const filters = ref({
    global: { value: null, matchMode: FilterMatchMode.CONTAINS },
    id: { value: null, matchMode: FilterMatchMode.EQUALS },
    title: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
    url: { value: null, matchMode: FilterMatchMode.CONTAINS },
    category: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
});

const emit = defineEmits(['selected', 'selectedIsEmpty']);


onMounted(() => {
    console.log("[Table.vue] --> Mounted.");
    loading.value = false;
    selectedItem.value = [];
})


// watchers
watch(
    () => selectedItem.value,
    async () => {
        console.log("Current --> ", selectedItem.value.length);
    }
)

watch(
    () => selectedItem.value,
    async () => {
        infos.value = "";
        emit('selected', selectedItem.value);
    }
)

watch(() => selectedItem.value, async () => {
    if (selectedItem.value.length === 0) {
        emit('selectedIsEmpty');
    }
})


</script>



<template>
    <div class="container">
        <div class="data-table-container">
            <DataTable 
            :value="data" 
            v-model:selection="selectedItem"
            paginator
            :rows="15"
            dataKey="id" 
            size="small"
            v-model:filters="filters"
            filterDisplay="row"
            :loading="loading"
            :globalFilterFields="['title', 'url', 'category']"
            removableSort
            showGridlines
            tableStyle="width: 50rem"
            >   
                <template #header>
                    <div class="flex justify-end">
                        <Button type="button" icon="pi pi-filter-slash" label="Clear" outlined @click="clearFilter()" />
                        <IconField>
                            <InputIcon>
                                <i class="pi pi-search" />
                            </InputIcon>
                            <InputText name="global-search" v-model="filters['global'].value" placeholder="Keyword Search" />
                        </IconField>
                    </div>
                </template>
                <template #empty> No customers found. </template>
                <template #loading> Loading customers data. Please wait. </template>
                <Column selectionMode="multiple"></Column>
                <Column field="id" header="Id" sortable>
                </Column>
                <Column field="title" header="Title" sortable>
                    <template #filter="{ filterModel, filterCallback }">
                        <InputText v-model="filterModel.value" type="text" @input="filterCallback()" placeholder="Search by title" />
                    </template>
                </Column>
                <Column field="url" header="URL">
                    <template #filter="{ filterModel, filterCallback }">
                        <InputText v-model="filterModel.value" type="text" @input="filterCallback()" placeholder="Search in URL:" />
                    </template>
                </Column>
                <Column field="category" header="Category" sortable>
                    <template #filter="{ filterModel, filterCallback }">
                        <InputText v-model="filterModel.value" type="text" @input="filterCallback()" placeholder="Search by Category" />
                    </template>
                </Column>
                <Column header="Actions" :exportable="false" style="min-width: 12rem">
                    <template #body="slotProps">
                        <Button label="Edit" outlined rounded class="mr-2" @click="$emit('edit-item', slotProps.data)" />
                        <Button label="Delete" outlined rounded severity="danger" @click="$emit('confirm-delete-item', slotProps.data)" />
                    </template>
                </Column>
            </DataTable>
        </div>
        <div class="infos-container">
            <p>{{ infos }}</p>
        </div>
    </div>
</template>



<style scoped>
    .p-datatable-table {
      width: 100%;
      border-spacing: 0;
      font-size: 10px;
    }
</style>