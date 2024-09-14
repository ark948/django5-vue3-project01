<script setup>
import { ref, onMounted } from 'vue';
import api from '@/api/api';

const props = defineProps({
    id: Number,
    title: String,
    url: String,
    
});

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
    
</template>


<style scoped>

</style>