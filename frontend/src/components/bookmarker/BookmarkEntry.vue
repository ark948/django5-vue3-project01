<script setup>
import { ref, onMounted } from 'vue';
import api from '@/api/api';
import { onClickOutside } from '@vueuse/core';

const props = defineProps({
    id: Number,
    title: String,
    url: String,
    isOpen: Boolean,
    
});
const emit = defineEmits(['modal-close']);
const target = ref(null); // refer to the container of modal
onClickOutside(target, () => emit('modal-close'));
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
                    Title: {{ bookmark_title }}
                    URL: {{ bookmark_url }}
                </div>
                <div v-if="isOpen" class="modal-mask">
                    <div class="modal-wrapper">
                        <div class="modal-container" ref="target">
                            <div class="modal-header">
                                <slot name="header">
                                    <h5>{{ bookmark_title }}</h5>
                                    <h5>{{ bookmark_url }}</h5>
                                </slot>
                            </div>
                            <div class="modal-body">
                                <slot name="content">body</slot>
                            </div>
                            <div class="modal-footer">
                                <slot name="footer">
                                    <div>
                                        <button @click.stop="emit('modal-close')">Close Modal</button>
                                    </div>
                                </slot>
                            </div>
                        </div>
                    </div>
                </div>
            </main>
            <div class="error-container">
                <p>{{ errorHolder }}</p>
            </div>
        </div>
    </div>
</template>


<style scoped>
.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
}
.modal-container {
  width: 300px;
  margin: 150px auto;
  padding: 20px 30px;
  background-color: #fff;
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
}
</style>