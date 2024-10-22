<script setup>

import { useBookmarksStore } from '@/stores';
import { onMounted, ref } from 'vue';

onMounted(() => {
    console.log("MOUNTED.");
    bookmarksStore.get_list();
    items.value = bookmarksStore.bookmarks_list;
});

const bookmarksStore = useBookmarksStore();
const items = ref();

</script>


<template>
    <div class="container">
        list:
        <div v-for="item in items" :key="item.id">
            <p>item: {{ item.id }} - {{ item.title }} - {{ item.url }} - {{ item.category_id }}</p>
        </div>
        <div class="nav-container">
            <p><RouterLink to="/">Home</RouterLink></p>
        </div>
    </div>
</template>


<style scoped>

</style>