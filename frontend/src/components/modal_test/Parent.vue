<script setup>
import { ref } from 'vue';
import Modal from './Modal.vue';

const isModalOpened = ref(false);
const openModal = () => {
    isModalOpened.value = true;
};
const closeModal = () => {
    isModalOpened.value = false;
}


</script>


<template>
    <div class="container">
        <button @click="openModal">open</button>
        <Modal :isOpen="isModalOpened" @close-modal="closeModal">
            <template #content></template>
        </Modal>
    </div>
</template>


<style scoped>

</style>