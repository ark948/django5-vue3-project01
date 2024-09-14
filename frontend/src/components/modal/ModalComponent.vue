<script setup>
    import { ref } from 'vue';
    import { onClickOutside } from '@vueuse/core';

    const props = defineProps({
        // receive isOpen prop from parent
        isOpen: Boolean,
    });

    const emit = defineEmits(["modal-close"]);
    // define a signal that parent can listen to
    const target = ref(null);
    onClickOutside(target, () => emit('modal-close'))
    // on clickoutside of target, emit the modal-close signal
    // modal-close signal is what tells the parent whether to close the modal or not
</script>


<template>
    <!-- display this if isOpen prop is true -->
    <div v-if="isOpen" class="modal-mask">
        <div class="modal-wrapper">
            <div class="modal-container" ref="target">
                <div class="modal-header">
                    <slot name="header">default header</slot>
                </div>
                <div class="modal-body">
                    <slot name="content">default content</slot>
                </div>
                <div class="modal-footer">
                    <slot name="footer">
                        <div>
                            <button @click.stop="emit('modal-close')">Submit</button>
                        </div>
                    </slot>
                </div>
            </div>
        </div>
    </div>
</template>


<style scoped>




</style>