import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'
import vSelect from 'vue-select'



import articles from '@/store/modules/articles'
import movies from '@/store/modules/movies'
import accounts from '@/store/modules/accounts'


Vue.use(Vuex)
Vue.component('v-select', vSelect)

export default new Vuex.Store({
  modules: { articles, movies, accounts },
  plugins: [
    createPersistedState()
  ]

})
