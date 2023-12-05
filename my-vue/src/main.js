import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; // 引入Vue Router
import VueAxios from 'vue-axios'
import 'element-plus/dist/index.css'
import ElementPlus from 'element-plus'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'


const app = createApp(App)
app.use(ElementPlus)
app.use(VueAxios)
app.use(router)
app.mount('#app')
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
  }
