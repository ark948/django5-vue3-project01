<script setup>
    import { ref } from 'vue';
    import ModalComponent from './ModalComponent.vue';

    const isModalOpened = ref(false);
    const openModal = () => {
        isModalOpened.value = true;
    };
    const closeModal = () => {
        isModalOpened.value = false;
    };

    const submitHandler = () => {
        // handle modal submit
    }
</script>


<template>
    <div class="container">
        <div>
        <button @click="openModal">Open modal</button>
        </div>
    <!-- listen to modal-close event emitted by child -->
    <ModalComponent :isOpen="isModalOpened" @modal-close="closeModal" @submit="submitHandler" name="first-modal">
        <template #header></template>
        <template #content>Custom content</template>
        <template #footer>Custom content</template>
    </ModalComponent>
    </div>
</template>


<style scoped>

</style>