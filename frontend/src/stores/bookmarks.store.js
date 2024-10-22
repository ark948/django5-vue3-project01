import { defineStore } from "pinia";
import router from "@/router";
import api from "@/api/api";
import { useAuthStore } from "./auth.store";

export const useBookmarksStore = defineStore({
    id: 'bookmarks',
    state: () => ({
        bookmarks_list: [],
        access_token: JSON.parse(localStorage.getItem('access_token')),
    }),
    actions: {
        get_list() {
            api.get('bookmarker/api/no-paginate/', { headers: { Authorization: this.access_token }})
                .then((response) => {
                    if (response.status === 200) {
                        for (let i =0; i < response.data.length; i++) {
                            this.bookmarks_list[i] = response.data[i];
                        }
                    } else {
                        console.log('list - not 200', response.status);
                    };
                })
                .catch(e => {
                    console.log("[Bookmarks Store ERROR]", e.message);
                })
                .finally(() => {
                    console.log("Total: -> ", this.bookmarks_list.length);
                });
        },

        async add_item() {
            
        },
        
        async get_item() {
            
        },

        async remove_item() {

        },

        async edit_item() {

        }
    }
})