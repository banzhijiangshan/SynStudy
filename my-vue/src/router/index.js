import { createRouter, createWebHistory } from 'vue-router';
import IndexPage from '../components/IndexPage.vue';
import RegisterPage from '../components/RegisterPage.vue';
import LunBo from '../components/LunBo.vue';
import BuildingFloor from '../components/BuildingFloor.vue';
import TeachingBuilding from '../components/TeachingBuilding.vue';
import ClassRoom from '../components/ClassRoom.vue';
import StudyScene from '../components/StudyScene.vue';
import SecondFloor from '../components/SecondFloor.vue';


const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: IndexPage },
    { path: '/register', component: RegisterPage },
    { path:'/lunbo',component:LunBo },
    { path:'/floor',component:BuildingFloor},
    { path:'/building',component:TeachingBuilding},
    { path:'/classroom',component:ClassRoom },
    { path:'/study',component:StudyScene },
    { path:'/second',component:SecondFloor },
  ],
});

export default router;
