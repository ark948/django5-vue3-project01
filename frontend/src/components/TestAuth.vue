<script>
    import api from '@/api/api';
    export default {
        data() {
            return {
                message: ""
            }
        },
        created() {
            console.log("This component created.");
        },
        mounted() {
            console.log("This component mounted.")
            this.getData()
        },

        methods: {
            getData() {
                api.get('test/')
                    .then(response => {
                        this.message += response.data.info
                    })
                    .catch(error => {
                        this.message = error
                    })
                
            }
        }
    }
</script>

<template>
    <div class="container">
        <p>{{ message }}</p>
        <div class="link-container">
            <RouterLink id="back" to="/">Back to home</RouterLink>
        </div>
    </div>
</template>