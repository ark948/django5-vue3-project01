import './assets/main.css';

import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';
import Notifications from '@kyvg/vue3-notification';
import PrimeVue from 'primevue/config';
import Aura from '@primevue/themes/aura';

// Vuetify

// import { createVuetify } from 'vuetify';
// import * as components from 'vuetify/components';
// import * as directives from 'vuetify/directives';
// import 'vuetify/styles';

// Vuestic UI
import { createVuestic } from 'vuestic-ui';
import 'vuestic-ui/css';

const app = createApp(App)

app.use(Notifications);
app.use(createPinia());
app.use(router);
// const vuetify = createVuetify({
//     components,
//     directives,
// });
// app.use(vuetify);
app.use(PrimeVue, {
    theme: {
        preset: Aura
    }
});
app.use(createVuestic()).mount('#app');
