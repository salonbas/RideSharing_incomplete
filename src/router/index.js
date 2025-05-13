import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '@/views/HomePage.vue';
import EventListPage from '@/views/EventListPage.vue';
import LoginPage from '@/views/LoginPage.vue';
import ForgotPasswordPage from '@/views/ForgotPasswordPage.vue';
import PersonalInfoPage from '@/views/PersonalInfoPage.vue';
import NotFoundView from '@/views/NotFoundView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomePage },
    { path: '/events', name: 'events', component: EventListPage },
    { path: '/login', name: 'login', component: LoginPage },
    { path: '/forgot-password', name: 'forgotPassword', component: ForgotPasswordPage },
    { path: '/profile', name: 'personalInfo', component: PersonalInfoPage },
    { path: '/:catchAll(.*)', name: 'NotFound', component: NotFoundView },
  ],
});

export default router;
