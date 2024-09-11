<script setup>
import { ref, onMounted } from 'vue';
import api from '@/api';

const props = defineProps(["id"]);
const bookmark_id = ref(props.id);
const bookmark_title = ref("");
const bookmark_url = ref("");
const errorHolder = ref("")

onMounted(() => {
    console.log("[BookmarkEntry.vue] - mounted with id of ", props.id);
    get_item();
});

async function get_item() {
    console.log("[BookmarkEntry.vue] - Getting item info...")
    const res = await api.get(`/bookmarker/${props.id}`)
    .then((response) => {
        if (response.status === 200) {
            console.log("SUCCESS")
            bookmark_title.value = response.data['title']
            bookmark_url.value = response.data['url']
        } else {
            console.log("RESPONSE NOT 200")
            errorHolder.value = error.message
        }
    })
    .catch((error) => {
        console.log("ERROR while getting item info.")
        
    })
}

</script>


<template>
    <div class="container">
        <div class="main-container">
            <main>
                <div class="item-container">
                    Title: <p>{{ bookmark_title }}</p>
                    URL: <p>{{ bookmark_url }}</p>
                </div>
            </main>
            <div class="error-container">
                <p>{{ errorHolder }}</p>
            </div>
        </div>
    </div>
</template>


<style scoped>
</style>