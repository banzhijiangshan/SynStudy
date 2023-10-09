import { createRouter, createWebHistory } from 'vue-router';
import DengLu1 from './components/DengLu1.vue';
import SignUp from './components/SignUp.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: DengLu1 },
    { path: '/signup', component: SignUp },
  ],
});

export default router;
