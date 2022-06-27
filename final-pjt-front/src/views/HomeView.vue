<template>
  <div> 
    <p class="text-start mx-5">recommend</p>
    <movie-carousel
      :movies="recommendation_movies"
      :movieId="movieId"
      :isModalShow="isModalShow"
      @select-one-movie="selectMovieId"
      class="mb-5"
    ></movie-carousel>
    
    <p class="text-start mx-5">popular</p>
    <movie-carousel
      :movies="popular_hate"
      :movieId="movieId"
      :isModalShow="isModalShow"
      @select-one-movie="selectMovieId" 
      class="mb-5"
    ></movie-carousel>

    <p class="text-start mx-5">Top Rated</p>
    <movie-carousel
      :movies="toprated_hate"
      :movieId="movieId"
      :isModalShow="isModalShow"
      @select-one-movie="selectMovieId"
      class="mb-5"
    ></movie-carousel>

    <p class="text-start mx-5">Now playing</p>
    <movie-carousel
      :movies="nowplaying_hate"
      :movieId="movieId"
      :isModalShow="isModalShow"
      @select-one-movie="selectMovieId"     
      class="mb-5"
    ></movie-carousel>


  </div>
</template>

<script>
import MovieCarousel from '@/components/MovieCarousel'
import axios from 'axios'
import drf from '@/api/drf'
import {mapGetters} from 'vuex'

const API_KEY = process.env.VUE_APP_TMDB_API_KEY
const API_URL = 'https://api.themoviedb.org/3'

export default {
  name: 'HomeView',
  components: {
    MovieCarousel,
  },
  data: function () {
    return {
      popular_movies: [],
      toprated_movies: [],
      nowplaying_movies: [],
      recommendation_movies: [],
      movieId: "",
      isModalShow: false,
      userId: null,
      hateGenreId: null,
      popular_hate: [],
      toprated_hate: [],
      nowplaying_hate: [],
      recommendation_hate: []
      

    }
  },
  computed: {
    ...mapGetters(['currentUser', 'profile']),
  },

  methods: {
    getMovie: function () {
      axios({
        method: 'get',
        url: drf.movies.recommendation(),
        headers: this.$store.getters.authHeader
      })
        .then(response => {
          console.log(response.data)
          this.recommendation_movies = response.data
          let tmp4 = []
          for (let recommend of this.recommendation_movies ) {
            //console.log(popular)
            // popular.genre_ids와 hate_genre가 겹치는 것이 하나도 없으면 popular_hate에 집어넣음
            // console.log(popular.genre_ids)
            let difference4 = recommend.genre_ids.filter(x => this.profile.hate_genre.includes(x))
            //console.log(difference)
            if (difference4.length === 0) {
              //console.log(1)
              tmp4.push(recommend)
              //console.log(tmp4)
            
            }
          }
        this.recommendation_hate = tmp4



        })


        .catch(err => {
          console.log(err.response)
        })

      axios ({
        method: 'get',
        url: API_URL + '/movie/popular',
        params: {
          api_key: API_KEY,
          language: 'ko',
          region: 'KR'
        }
      })
      .then(response => {
        this.popular_movies = response.data.results
        console.log(this.popular_movies)
        // console.log(this.profile.hate_genre)
        let tmp = []
        for (let popular of this.popular_movies ) {
          console.log(popular)
          // popular.genre_ids와 hate_genre가 겹치는 것이 하나도 없으면 popular_hate에 집어넣음
         // console.log(popular.genre_ids)
          let difference = popular.genre_ids.filter(x => this.profile.hate_genre.includes(x))
          console.log(difference)
          if (difference.length === 0) {
            console.log(1)
            tmp.push(popular)
            console.log(tmp)
          
          }
        this.popular_hate = tmp
        
          
        }

        
      })

      axios({
        method: 'get',
        url: API_URL + '/movie/top_rated',
        params: {
          api_key: API_KEY,
          language: 'ko',
          region: 'KR'
        }
      })
      .then(response => {
        this.toprated_movies = response.data.results
        //console.log(response.data)
        let tmp3 = []
        for (let toprated of this.toprated_movies ) {
          //console.log(popular)
          // popular.genre_ids와 hate_genre가 겹치는 것이 하나도 없으면 popular_hate에 집어넣음
         // console.log(popular.genre_ids)
          let difference3 = toprated.genre_ids.filter(x => this.profile.hate_genre.includes(x))
          //console.log(difference)
          if (difference3.length === 0) {
            //console.log(1)
            tmp3.push(toprated)
            //console.log(tmp)
          
          }
        }
        this.toprated_hate = tmp3
      })

      axios({
        method: 'get',
        url: API_URL + '/movie/now_playing',
        params: {
          api_key: API_KEY,
          language: 'ko',
          region: 'KR',
          
        }
      })
      .then(response => {
        this.nowplaying_movies = response.data.results
        let tmp2 = []
        for (let nowplaying of this.nowplaying_movies ) {
          
          // popular.genre_ids와 hate_genre가 겹치는 것이 하나도 없으면 popular_hate에 집어넣음
         // console.log(popular.genre_ids)
          let difference2 = nowplaying.genre_ids.filter(x => this.profile.hate_genre.includes(x))
          //console.log(difference2)
          if (difference2.length === 0) {
            //console.log(1)
            tmp2.push(nowplaying)
            //console.log(tmp)
          
          }
        }
        this.nowplaying_hate = tmp2

        //console.log(response.data)
      })

    },
    selectMovieId: function (selectMovieId) {
      this.movieId = selectMovieId
      this.isModalShow = true
    },

    getUserId: function () {
      this.userId = this.currentUser.pk
      
    }

  },
  created() {
    this.getMovie()
    this.getUserId()
  }
}
</script>

<style>
</style>