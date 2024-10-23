import { defineStore } from "pinia";
import api from "@/api/api";

export const useBookmarksStore = defineStore({
    id: 'bookmarks',
    state: () => ({
        bookmarks_list: [],
        access_token: JSON.parse(localStorage.getItem('access_token')),
    }),
    actions: {
        get_list() {
            console.log("TOKEN --> ", this.access_token);
            api.get('bookmarker/api/no-paginate/', { headers: { Authorization: this.access_token }})
                .then((response) => {
                    if (response.status === 200) {
                        let count = 1;
                        for (let i =0; i < response.data.length; i++) {
                            response.data[i].count = count;
                            this.bookmarks_list[i] = response.data[i];
                            count++;
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

        async add_item(title, url, category_id, icon) {
            api.post('bookmarker/api/no-paginate/', {title: title, url: url, category_id: category_id, icon: icon}, {headers: {Authorization: this.access_token}})
                .then((response) => {
                    if (response.status === 201) {
                        console.log("new item.");
                    } else {
                        console.log("new item not 201");
                    }
                })
                .catch((e) => {
                    console.log("error in insertion: ", e.message);
                })
        },
        
        async get_item(id) {
            api.get(`bookmarker/api/${id}`, {headers: {Authorization: this.access_token}})
                .then((response) => {
                    if (response.status === 200) {
                        return response.data
                    } else {
                        console.log("get item not 200");
                    }
                })
                .catch((e) => {
                    console.log("error in getting item: ", e.message);
                })
        },

        async remove_item(id) {
            api.delete(`bookmarker/api/${id}`, {headers: {Authorization: this.access_token}})
                .then((response) => {
                    if (response.status === 204) {
                        console.log("item deleted.");
                    } else {
                        console.log("delte not 204");
                    }
                })
                .catch((e) => {
                    console.log("error in delete: ", e.message);
                })
        },

        async edit_item(id, new_title, new_url, new_category_id) {
            api.put(`bookmarker/api/${id}/`, {title: new_title, url: new_url, category_id: new_category_id}, { headers: {Authorization: this.access_token}})
                .then((response) => {
                    if (response.status === 200) {
                        console.log("Update successful.");
                    } else {
                        console.log("update not 200");
                    }
                })
                .catch((e) => {
                    console.log("Error in update: ", e.message);
                })
        }
    }
});