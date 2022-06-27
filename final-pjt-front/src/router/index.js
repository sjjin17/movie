import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '../store'

import HomeView from '@/views/HomeView'
import MovieSearch from '@/views/MovieSearch'
import ArticleAll from '@/views/ArticleAll'
import ArticleDetail from '@/views/ArticleDetail'

import LoginView from '@/views/LoginView'
import LogoutView from '@/views/LogoutView'
import SignupView from '@/views/SignupView'
import ProfileView from '@/views/ProfileView'
import ProfileEdit from '@/views/ProfileEdit'


Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'HomeView',
    component: HomeView
  },
  {
    path: '/search',
    name: 'MovieSearch',
    component: MovieSearch
  },
  {
    path: '/articles',
    name: 'ArticleAll',
    component: ArticleAll
  },
  {
    path: '/articles/:articlePk',
    name: 'article',
    component: ArticleDetail
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/logout',
    name: 'logout',
    component: LogoutView
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignupView
  },
  {
    path: '/profile/:userPk',
    name: 'profile',
    component: ProfileView,
  },
  {
    path: '/profile/:userPk/edit',
    name: 'ProfileEdit',
    component: ProfileEdit,
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
})

router.beforeEach((to, from, next) => {
  // 이전 페이지에서 발생한 에러메시지 삭제
  store.commit('SET_AUTH_ERROR', null)

  const { isLoggedIn } = store.getters

  const noAuthPages = ['login', 'signup']

  const isAuthRequired = !noAuthPages.includes(to.name)

  if (isAuthRequired && !isLoggedIn) {
    alert('Require Login. Redirecting..')
    next({ name: 'login' })
  } else {
    next()
  }

  if (!isAuthRequired && isLoggedIn) {
    next({ name: 'ArticleAll' })
  }
})


export default router
