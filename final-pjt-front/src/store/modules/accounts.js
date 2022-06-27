import router from '@/router'
import axios from 'axios'
import drf from '@/api/drf'


export default {
  // namespaced: true,

  // state는 직접 접근하지 않겠다!
  state: {
    token: localStorage.getItem('token') || '' ,
    currentUser: {},
    profile: {},
    authError: null,
  },
  // 모든 state는 getters 를 통해서 접근하겠다.
  getters: {
    isLoggedIn: state => !!state.token,
    currentUser: state => state.currentUser,
    profile: state => state.profile,
    authError: state => state.authError,
    authHeader: state => ({ Authorization: `Token ${state.token}`})
  },

  mutations: {
    SET_TOKEN: (state, token) => state.token = token,
    SET_CURRENT_USER: (state, user) => state.currentUser = user,
    SET_PROFILE: (state, profile) => state.profile = profile,
    SET_AUTH_ERROR: (state, error) => state.authError = error,
  },

  actions: {
    saveToken({ commit }, token) {
      commit('SET_TOKEN', token)
      localStorage.setItem('token', token)
    },
    removeToken({ commit }) {
      commit('SET_TOKEN', '')
      localStorage.setItem('token', '')
    },
    login({ commit, dispatch }, credentials) {
      axios({
        url: drf.accounts.login(),
        method: 'post',
        data: credentials
      })
        .then(res => {
          const token = res.data.key
          dispatch('saveToken', token)
          dispatch('fetchCurrentUser')
          router.push({ name: 'articles' })
        })
        .catch(err => {
          console.error(err.response.data)
          commit('SET_AUTH_ERROR', err.response.data)
        })
    },
    signup({ commit, dispatch }, credentials) {
      axios({
        url: drf.accounts.signup(),
        method: 'post',
        data: credentials
      })
        .then(res => {
          console.log('api보낸 직후')
          const token = res.data.key
          dispatch('saveToken', token)
          dispatch('fetchCurrentUser')
          router.push({ name: 'articles' })
        })
        .catch(err => {
          console.error(err.response.data)
          commit('SET_AUTH_ERROR', err.response.data)
        })
    },
    logout({ getters, dispatch }) {
      axios({
        url: drf.accounts.logout(),
        method: 'post',
        // data: {},
        headers: getters.authHeader,
      })
        .then(() => {
          dispatch('removeToken')
          alert('성공적으로 logout!')
          router.push({ name: 'login' })
        })
        .error(err => {
          console.error(err.response)
        })
    },
    fetchCurrentUser({ commit, getters, dispatch }) {
      if (getters.isLoggedIn) {
        axios({
          url: drf.accounts.currentUserInfo(),
          method: 'get',
          headers: getters.authHeader,
        })
          .then(res => commit('SET_CURRENT_USER', res.data))
          .catch(err => {
            if (err.response.status === 401) {
              dispatch('removeToken')
              router.push({ name: 'login' })
            }
          })
      }
    },
    fetchProfile({ commit, getters }, { userPk }) {
      axios({
        url: drf.accounts.profile(userPk),
        method: 'get',
        headers: getters.authHeader,
      })
        .then(res => {
          console.log(res)
          commit('SET_PROFILE', res.data)
        })
    },
    updateProfile({ commit, getters }, { pk, nickname, hate_genre }) {
      axios({
        url: drf.accounts.editprofile(pk),
        method: 'put',
        data: { pk, nickname, hate_genre },
        headers: getters.authHeader,
      })
        .then(res => {
          console.log('이미지 이외 변경 완료')
          console.log(res)
          commit('SET_PROFILE', res.data)
          router.push({
            name: 'profile',
            params: { userPk: pk }
          })
        })
    },
    // updateProfileTwo({ getters }, formdata ) {
    //   console.log('axios 보내기 전')
    //   console.log(formdata)
    //   console.log({Authorization: getters.authHeader['Authorization'], 'Content-Type': 'multipart/form-data'})
    //   console.log(drf.accounts.editprofiletwo)
    //   // console.log(getters.authHeader) = {Authorization: 'Token bdabdf94c20481371854eec8dda9e274b77bc33e'}
    //   axios({
    //     url: drf.accounts.editprofiletwo,
    //     method: 'post',
    //     data: formdata,
    //     headers: {Authorization: getters.authHeader['Authorization'], 'Content-Type': 'multipart/form-data'},
    //   })
    //     .then(res => {
    //       console.log('이미지 변경 선공')
    //       console.log(res)
    //       // commit('SET_PROFILE', res.data)
    //       // router.push({
    //       //   name: 'profile',
    //       //   params: { userPk: pk }
    //       // })
    //     })
    //     .catch(err => {
    //       console.log('이미지 변경 안됨')
    //       console.log(err.response)
    //       console.log('이미지 변경 안됨')
    //     })
    // }
  },
}
