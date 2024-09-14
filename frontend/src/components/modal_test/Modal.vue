<script setup>
import { ref } from 'vue';
import { onClickOutside } from '@vueuse/core';

const props = defineProps({
    isOpen: Boolean,
    message: String
});

const emit = defineEmits(['close-modal']);
const target = ref(null);
onClickOutside(target, () => emit('close-modal'))

</script>


<template>
    <div v-if="isOpen" class="modal">
        <div class="modal-container" ref="target">
            <slot name="header"></slot>
            <br>
            <slot name="content">default body</slot>
            <br>
            <slot name="footer">
                footer
                <button @click.stop="emit('close-modal')">Close</button>
            </slot>
        </div>
    </div>
</template>


<style scoped>
.modal {
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