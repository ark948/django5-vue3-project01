<script>
    import BookmarksList from '@/components/bookmarker/BookmarksList.vue';

    export default {
        data() {
            return {

            }
        },
        components: {
            BookmarksList
        },
        methods: {

        },
        mounted() {
            console.log('Bookmark Parent mounted.');
        }
    }
</script>

<template>
    <div class="container">
        <div class="main-container">
            <main>
                <p>Bookmark manager</p>
                <div class="list-container">
                    <BookmarksList />
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
</style>