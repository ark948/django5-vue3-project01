<script setup>
import { ref, onMounted } from 'vue';
import api from '@/api/api';
import BookmarkEntry from './BookmarkItem.vue';
import { useRouter } from 'vue-router';

const responseHolder = ref("");
const errorHolder = ref("");
const all_bookmarks = ref([])
const insideRouter = useRouter();


onMounted(() => {
    console.log('[BookmarksList.vue] - mounted.')
    get_bookmarks();
})

async function get_bookmarks() {
    console.log("[BookmarksList.vue]");
    console.log("[BookmarksList.vue] Getting the list...");
    const res = await api.get('bookmarker/api/')
    .then((response) => {
        if (response.status === 200) {
            console.log("Response 200")
            for (let i=0; i < response.data.length; i++) {
                console.log(response.data[i]);
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

    const goToItem = (id) => {
        console.log("Going to item");
        console.log(id);
        router.push(`/bookmarker/${id}`);
    }
}
</script>

<template>
    <div class="container">
        
    </div>
</template>

<style scoped>

</style>