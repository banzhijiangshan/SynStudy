//import { createApp } from 'vue'
//import App from './App.vue'

//createApp(App).mount('#app')

import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; // 引入Vue Router
import VueAxios from 'vue-axios'
import 'element-plus/dist/index.css'
import ElementPlus from 'element-plus'

const app = createApp(App)
app.use(ElementPlus)
app.use(VueAxios)
app.use(router)
app.mount('#app')
