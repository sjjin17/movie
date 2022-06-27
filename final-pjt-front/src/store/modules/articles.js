import axios from 'axios'
import drf from '@/api/drf'
import router from '@/router'
import _ from 'lodash'

export default {
  state: {
    articles: [],
    article: {},
    searchMovies: []
  },

  getters: {
    articles: state => state.articles,
    article: state => state.article,
    isAuthor: (state, getters) => {
      return state.article.user?.username === getters.currentUser.username
    },
    isArticle: state => !_.isEmpty(state.article),
    searchMovies: state => state.searchMovies,
  },

  mutations: {
    SET_ARTICLES: (state, articles) => state.articles = articles,
    SET_ARTICLE: (state, article) => state.article = article,
    SET_ARTICLE_COMMENTS: (state, comments) => (state.article.comments = comments),
    SET_MOVIES: (state, searchMovies) => state.searchMovies = searchMovies,
  },

  actions: {
    fetchArticles({ commit, getters }) {
      axios({
        url: drf.articles.articles(),
        method: 'get',
        headers: getters.authHeader,
      })
        .then(res => commit('SET_ARTICLES', res.data))
        .catch(err => console.error(err.response))
    },
    searchMovie({ commit, getters }, title) {
      axios({        
        url: drf.movies.search(),
        method: 'get',
        headers: getters.authHeader,
        params: { "search": title }
      })
        .then(res => commit('SET_MOVIES', res.data))
        .catch(err => console.error(err.response))
    },
    fetchArticle({ commit, getters }, articlePk) {
      axios({
        url: drf.articles.article(articlePk),
        method: 'get',
        headers: getters.authHeader,
      })
        .then(res => commit('SET_ARTICLE', res.data))
        .catch(err => {
          console.error(err.response)
          // if (err.response.status === 404) {
          //   router.push({ name: 'NotFound404' })
          // }
        })
    },
    createArticle({ commit, getters }, { movie_pk, star_rate, title, content }) {     
      axios({
        url: drf.articles.getarticle(movie_pk),
        method: 'post',
        data: { star_rate, title, content },
        headers: getters.authHeader,
      })
        .then(res => {
          commit('SET_ARTICLE', res.data)
          router.push({ name: 'ArticleAll' })
        })
        .then(() => {
          router.go(router.currentRoute)
        })
    },

    likeArticle({ commit, getters }, articlePk) {
      axios({
        url: drf.articles.likeArticle(articlePk),
        method: 'post',
        headers: getters.authHeader,
      })
        .then(res => commit('SET_ARTICLE', res.data))
        .then(() => {
          router.go(router.currentRoute)
        })
        .catch(err => console.error(err.response))
    },

    updateArticle({ commit, getters }, { pk, star_rate, title, content }) {
      axios({
        url: drf.articles.article(pk),
        method: 'put',
        data: { title, content, star_rate },
        headers: getters.authHeader,
      })
        .then(res => {
          commit('SET_ARTICLE', res.data)
          router.push({
            name: 'article',
            params: { articlePk: getters.article.pk }
          })
        })
    },
    deleteArticle({ commit, getters }, articlePk) {      
      if (confirm('정말 삭제하시겠습니까?')) {
        axios({
          url: drf.articles.article(articlePk),
          method: 'delete',
          headers: getters.authHeader,
        })
          .then(() => {
            commit('SET_ARTICLE', {})
            router.push({ name: 'ArticleAll' })
            
          })
          .then(() => {
            router.go(router.currentRoute)
          })
          .catch(err => console.error(err.response))
      }
    },
    createComment({ commit, getters }, { articlePk, content }) {
      const comment = { content }

      axios({
        url: drf.articles.comments(articlePk),
        method: 'post',
        data: comment,
        headers: getters.authHeader,
      })
        .then(res => {
          commit('SET_ARTICLE_COMMENTS', res.data)
        })
        .then( () => {router.go(router.currentRoute) })
        .catch(err => console.error(err.response))
    },
    updateComment({ commit, getters }, { articlePk, commentPk, content }) {
      const comment = { content }

      axios({
        url: drf.articles.comment(articlePk, commentPk),
        method: 'put',
        data: comment,
        headers: getters.authHeader,
      })
        .then(res => {
          commit('SET_ARTICLE_COMMENTS', res.data)
        })
        .catch(err => console.error(err.response))
    },
    deleteComment({ commit, getters }, { articlePk, commentPk }) {
      if (confirm('정말 삭제하시겠습니까?')) {
        axios({
          url: drf.articles.comment(articlePk, commentPk),
          method: 'delete',
          data: {},
          headers: getters.authHeader,
        })
          .then(res => {
            commit('SET_ARTICLE_COMMENTS', res.data)
          })
          .then( () => {router.go(router.currentRoute) })
          .catch(err => console.error(err.response))
      }
    },

  }
}
