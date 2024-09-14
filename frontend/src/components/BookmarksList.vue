<script setup>
import { ref, onMounted } from 'vue';
import api from '@/api';
import BookmarkEntry from './BookmarkEntry.vue';
import { useRouter } from 'vue-router';

const isModalOpened = ref(false);
const responseHolder = ref("");
const errorHolder = ref("");
const all_bookmarks = ref([])
const insideRouter = useRouter();

const openModal = () => {
    isModalOpened.value = true;
    };
const closeModal = () => {
    isModalOpened.value = false;
    };

const modalSubmitHandler = () => {
    // handle modal submit
    };

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
        <div class="welcome-container">
            <h3>Your Bookmarks:</h3>
        </div>
        <div class="main-container">
            <div v-for="item in all_bookmarks" class="data-container" :key="item.id">
                <BookmarkEntry
                :key="item.id" :id="item.id" :title="item.title" :url="item.url" />
                <button :isOpen="isModalOpened" @click="openModal" @modal-close="closeModal">open modal</button>
            </div>
            <div class="modal-button-container">
                <button @click="openModal">Opem modal</button>
            </div>
            <div class="error-container">
                <p>{{ errorHolder }}</p>
            </div>
        </div>
    </div>
</template>