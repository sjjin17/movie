import axios from 'axios'
import drf from '@/api/drf'
//import router from '@/router'





export default {
  state: {
    movies: [],
    movie: [],
    genres: [],
    genre: [],
    linecomments: [],
    
  },
  getters: {
    movies: state => {return state.movies},
    movie: state => {return state.movie},
    genres: state => {return state.genres},
    genre: state => {return state.genre},
    linecomments: state => {return state.linecomments},

  },
  mutations: {
    SET_MOVIES: (state, movies) => state.movies = movies,
    SET_MOVIE: (state, movie) => state.movie = movie,
    SET_GENRES: (state, genres) => state.genres = genres,
    SET_GENRE: (state, genre) => state.genre = genre,
    SET_LINECOMMENTS: (state, linecomments) => state.linecomments = linecomments,
  },
  actions: {
    fetchMovies({ commit, getters }) {
      axios({
        url: drf.movies.movies(),
        method: 'get',
        headers: getters.authHeader,
      })
      .then(response => commit('SET_MOVIES', response.data))
      .catch(err => console.error(err.response))
    },

    fetchMovie({ commit, getters }, moviePk) {
      axios({
        url: drf.movies.movie(moviePk),
        method: 'get',
        headers: getters.authHeader,
      })
        .then(response => commit('SET_MOVIE', response.data))
        .catch(err => console.error(err.response))
    },


    fetchGenres({ commit, getters }) {
      axios({
        url: drf.movies.genres(),
        method: 'get',
        headers: getters.authHeader,
      })
        .then(response => commit('SET_GENRES', response.data))
        .catch(err => console.error(err.response))
    },
    
    fetchGenre({ commit, getters }, genrePk) {
      axios({
        url: drf.movies.genre(genrePk),
        method: 'get',
        headers: getters.authHeader,
      })
        .then(response => commit('SET_GENRE', response.data))
        // .then(() => {
        //   router.go(router.currentRoute)
          
        // })
        .catch(err => console.error(err.response))
    },
    fetchLineComments({ commit, getters }, moviePk) {
      axios({
        url: drf.movies.lineComments(moviePk),
        method: 'get',
        headers: getters.authHeader,
      })
        .then(response => {
          commit('SET_LINECOMMENTS', response.data)
        })

        .catch(err => console.error(err.response))
    },
    likeMovie({ commit, getters }, moviePk) {
      axios({
        url: drf.movies.likeMovie(moviePk),
        method: 'post',
        headers: getters.authHeader,
      })
        .then(response => commit('SET_MOVIE', response.data))
        .catch(err => console.error(err.response))
    },
    saveMovie({ commit, getters }, moviePk) {
      axios({
        url: drf.movies.saveMovie(moviePk),
        method: 'post',
        headers: getters.authHeader,
      })
        .then(response => commit('SET_MOVIE', response.data))
        .catch(err => console.error(err.response))

    },
    createLineComment({ commit, getters }, { movie_pk, content, star_rate }) {
      axios({
        url: drf.movies.lineComments(movie_pk),
        method: 'post',
        data: { star_rate, content },
        headers: getters.authHeader,
      })

        .then(response => {
          commit('SET_LINECOMMENTS', response.data) 
        })

        .catch(err => console.error(err.response))
    },
  },
  modules: {
  }
}
