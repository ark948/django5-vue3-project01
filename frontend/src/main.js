import './assets/main.css';

import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';
import Notifications from '@kyvg/vue3-notification';

// PrimeVue
import PrimeVue from 'primevue/config';
import Aura from '@primevue/themes/aura';

// Vuetify
// Vuetify was deleted

// Vuestic UI
import { createVuestic } from 'vuestic-ui';
import 'vuestic-ui/css';

const app = createApp(App)

app.use(Notifications);
app.use(createPinia());
app.use(router);
app.use(PrimeVue, {
    theme: {
        preset: Aura
    }
});
app.use(createVuestic()).mount('#app');
