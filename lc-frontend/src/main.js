import './assets/main.css'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router/'
import VueGoogleMaps from '@fawmi/vue-google-maps';
// import { nodePolyfills } from 'vite-plugin-node-polyfills'; 

createApp(App).use(router).use(VueGoogleMaps, {
  load: {
    key: import.meta.env.VITE_GOOGLE_MAPS_API_KEY,
    libraries: ['places'],
  }
}).mount('#app')