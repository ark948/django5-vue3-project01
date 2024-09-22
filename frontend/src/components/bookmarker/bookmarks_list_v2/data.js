import api from "@/api/api";


async function get_all_bookmark_items() {
    console.log("Aquiring list...");
    const item_list = [];
    const res = await api
      .get("bookmarker/api/no-paginate/")
      .then((response) => {
        if (response.status === 200) {
            console.log('SUCCESS-200')
          for (let i = 0; i < response.data.length; i++) {
            // console.log(response.data[i]);
            item_list.push(response.data[i]);
          }
          console.log('data.js', item_list);
          return item_list;
        } else {
            console.log('ERROR-', response.status);
        }
      })
      .catch((error) => {
        console.log('Error occurred. > ', error.message);
      })
      .finally(() => {
        console.log('Request finished.');
      });
  }

export { get_all_bookmark_items };