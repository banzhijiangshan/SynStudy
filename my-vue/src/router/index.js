import { createRouter, createWebHistory } from 'vue-router';
import IndexPage from '../components/IndexPage.vue';
import RegisterPage from '../components/RegisterPage.vue';
import LunBo from '../components/LunBo.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: IndexPage },
    { path: '/register', component: RegisterPage },
    { path:'/lunbo',component:LunBo },
  ],
});

export default router;
