import api from "@/api/api";

async function get_bookmarks() {
  console.log("Getting the list...");
  // const res = await api.get(`bookmarker/api/?page=${page_number.value}`)
  const res = await api
    .get("bookmarker/api/no-paginate/")
    .then((response) => {
      if (response.status === 200) {
        console.log("Response 200");
        for (let i = 0; i < response.data.length; i++) {
          // console.log(response.data[i]);
          all_bookmarks.value.push(response.data[i]);
        }
      } else {
        console.log("[BookmarksList.vue] Response NOT 200", response.status);
      }
    })
    .catch((error) => {
      console.log("ERROR");
      console.log(`[BookmarksList.vue] => ${error.message}`);
    })
    .finally(() => {
      console.log(`Total of ${all_bookmarks.value.length} items.`);
    });
}


export { get_bookmarks };