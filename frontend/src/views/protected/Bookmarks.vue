<script>
    import BookmarksList from '@/components/bookmarker/BookmarksList.vue';

    export default {
        data() {
            return {
                componentKey: 0,
            }
        },
        components: {
            BookmarksList
        },
        methods: {
            forceRerender() {
                this.componentKey += 1;
            }
        },
    }
</script>

<template>
    <div class="container">
        <div class="main-container">
            <main>
                <p>Bookmark manager</p>
                <div class="list-container">
                    <BookmarksList
                    @reloadThisList="() => forceRerender()"
                    :key="componentKey"
                    />
                    <button @click="forceRerender">Refresh</button>
                </div>
            </main>
        </div>
        <div class="link-container">
            <RouterLink id="back" to="/">Back to home</RouterLink>
        </div>
    </div>
</template>

<style scoped>
    .link-container {
        margin-top: 50px;
    }

    button {
        height: 35px;
        width: 70px;
        padding: 10px;
        margin: 20px 0;
        margin-left: 5px;
        background-color: #42B883;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.2s ease-in-out;
        font-size: 15px;
        font-weight: bold
    }
</style>