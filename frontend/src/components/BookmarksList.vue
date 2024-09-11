<script setup>
import { ref, onMounted } from 'vue';
import api from '@/api';
import BookmarkEntry from './BookmarkEntry.vue';

const responseHolder = ref("");
const errorHolder = ref("");
const all_bookmarks = ref([])

onMounted(() => {
    console.log('[BookmarksList.vue] - mounted.')
    get_bookmarks();
})

async function get_bookmarks() {
    console.log("[BookmarksList.vue]")
    console.log("[BookmarksList.vue] Getting the list...")
    const res = await api.get('bookmarker/')
    .then((response) => {
        if (response.status === 200) {
            console.log("Response 200")
            for (let i=0; i < response.data.length; i++) {
                console.log("Item => ", response.data[i])
                all_bookmarks.value.push(response.data[i])
                
            }
        }
    })
    .catch((error) => {
        console.log("ERROR")
        console.log(`[BookmarksList.vue] => ${error.message}`);

    })
}
</script>

<template>
    <div class="container">
        <div class="welcome-container">
            <h3>Your Bookmarks:</h3>
        </div>
        <div class="main-container">
            <div class="data-container">
                <!-- <BookmarkEntry v-for="bm in all_bookmarks" :key="bm.id" :id="bm.id" /> -->
                <p v-for="(item, index) in all_bookmarks" :key="item.id">
                    # {{ index+1 }}
                    Title: {{ item.title }}
                    URL: {{ item.url }}
                </p>
            </div>
            <div class="error-container">
                <p>{{ errorHolder }}</p>
            </div>
        </div>
    </div>
</template>