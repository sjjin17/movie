<template>
  <div class="container">
    <div>
      <!-- {{ movie }}
      {{ movieId }} -->
      <!-- {{ movie.id }} -->
      <div class="d-flex justify-content-between">
        <h4 class="fw-bolder my-1">{{ movie.title }}</h4>
        <div>
          <!-- <button @click="likeMovie(movieId)">
            <i class="fa-solid fa-heart"></i>
          </button> -->
          <i v-if="isLike === true" @click="likeMovie(movieId)" class="fa-solid fa-heart"></i>
          <i v-else @click="likeMovie(movieId)" class="fa-regular fa-heart"></i>
          <span class="mx-1 me-2">{{ movie.like_users_count }}</span>

          <i class="fa-regular fa-bookmark" @click="saveMovie(movieId)"></i>
          <!-- <button @click="saveMovie(movieId)">저장</button> -->
          <span class="mx-1">{{ movie.save_users_count }}</span>
          
        </div>  
        
      </div>
      
      <p class="fw-semibold movie-content" style="text-align:justify">{{ movie.overview }}</p>
      <!-- <button @click="lessConent" v-if="isMore">접기</button>
      <button @click="moreContent" v-else>더보기</button> -->
      

      <div>개봉일:&nbsp; {{ movie.release_date }}</div>
      <span>장르: &nbsp;</span>
      <span
        v-for="genre in movie.genres"
        :key="genre.id"
        class="badge rounded-pill text-bg-secondary mx-1"
      >{{ genre.name }}&nbsp; &nbsp;</span>
          
      <div>상영시간: {{ movie.runtime }}</div>
      <div>평점: {{ movie.vote_average }}</div>
      <span
        v-for="director in oneDirector"
        :key="director.id"
      >{{ director.also_known_as }}&nbsp;</span>
      <span
        v-for="actor in movie.actors"
        :key="actor.id"
      >{{ actor.also_known_as }}&nbsp;</span>
    </div>

   
    <span 
      v-for="keyword in aFewKeywords" 
      :key="keyword.id"
    >
      <span># {{ keyword.name }}</span>
      &nbsp;    
    </span>

    <!-- cgv에서 영화 검색 -->
    <br>
    <br>
    <span v-if="cgvUrl != False">
      <b-button variant="light">
        <a :href="cgvUrl" class="text-decoration-none">
          <img src="https://img.cgv.co.kr/R2014/images/common/logo/logoRed.png" alt="cgv 이미지" class="cgv">
          
        </a>
      </b-button>
    </span>
  </div>
</template>

<script>
// MovieModal의 하위component
import { mapGetters, mapActions } from 'vuex'
import axios from 'axios'

const API_KEY = process.env.VUE_APP_TMDB_API_KEY
const API_URL = 'https://api.themoviedb.org/3/movie/'


export default {
  name: 'MovieDetail',
  data: function () {
    return {
      keywords: [],
      isMore: false,
      cgvUrl: ''
            
    }
  },
  props: {
    movieId: Number,
    isLike: Boolean,
  },

  computed: {
    ...mapGetters(['movie']),  
    oneDirector: function () {
      return this.movie.directors.slice(0, 1)
    },
    aFewKeywords: function () {
      return this.keywords.slice(0,5)
    },
  },
  methods: {
    ...mapActions(['fetchMovie', 'likeMovie', 'saveMovie']),
    getKeywords: function () {
      axios({
        method: 'get',
        url: API_URL + this.movieId +'/keywords',
        params: {
          api_key: API_KEY,   
        }
      })
      .then(response => {
        this.keywords = response.data.keywords
        })
    },
    getUrl: function() {
      console.log(this.movie.title)
      setTimeout(() => {
        axios({
          method: 'get',
          url: 'http://localhost:8000/api/v1/movies/reservation/' + `${this.movie.title}/`,
          contentType: "application/json; charset=utf-8;"
        })
          .then(res => {
            this.cgvUrl = res.data.movie_url
            console.log(this.cgvUrl)
          })
          .catch(err => {
            console.err(err)
          })
      }, 800)
    },
  }, 
  created() {
    this.fetchMovie(this.movieId)
    this.getKeywords()
    this.getUrl()
  },

  
}
</script>

<style>
  .cgv {
    width: 50px;

  }
</style>