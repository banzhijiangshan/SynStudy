//import { createApp } from 'vue'
//import App from './App.vue'

//createApp(App).mount('#app')

import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; // 引入Vue Router配置文件

createApp(App)
  .use(router) // 使用Vue Router
  .mount('#app');
