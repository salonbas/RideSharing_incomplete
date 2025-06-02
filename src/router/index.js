import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '@/views/HomePage.vue';
import EventListPage from '@/views/EventListPage.vue';
import CreateEventPage from '@/views/CreateEventPage.vue';
import LoginPage from '@/views/LoginPage.vue';
import ForgotPasswordPage from '@/views/ForgotPasswordPage.vue';
import NewPasswordPage from '@/views/NewPasswordPage.vue';
import CreateAccountPage from '@/views/CreateAccountPage.vue';
import PersonalInfoPage from '@/views/PersonalInfoPage.vue';
import MyEventsPage from '@/views/MyEventsPage.vue';
import NotFoundView from '@/views/NotFoundView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomePage },
    { path: '/events', name: 'events', component: EventListPage },
    { path: '/create-event', name: 'createEvent', component: CreateEventPage },
    { path: '/login', name: 'login', component: LoginPage },
    { path: '/forgot-password', name: 'forgotPassword', component: ForgotPasswordPage },
    { path: '/new-password', name: 'newPassword', component: NewPasswordPage },
    { path: '/create-account', name: 'createAccount', component: CreateAccountPage },
    { path: '/profile', name: 'personalInfo', component: PersonalInfoPage },
    { path: '/my-events', name: 'myEvents', component: MyEventsPage },
    { path: '/:catchAll(.*)', name: 'NotFound', component: NotFoundView },
  ],
});

export default router;
