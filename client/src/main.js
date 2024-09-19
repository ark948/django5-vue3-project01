import './assets/main.css';

import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';
import Notifications from '@kyvg/vue3-notification';
import PrimeVue from 'primevue/config';
import Aura from '@primevue/themes/aura';

// Vuetify
import 'vuetify/styles';
import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';

const app = createApp(App)

const vuetify = createVuetify({
    components,
    directives,
});

app.use(Notifications);
app.use(createPinia());
app.use(router);
app.use(vuetify);
app.use(PrimeVue, {
    theme: {
        preset: Aura
    }
});
app.mount('#app');
