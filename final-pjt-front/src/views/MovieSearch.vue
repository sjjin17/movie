<template>
  <div>
    <!-- 검색 -->
    <movie-search-bar
      @input-change="onInputChange"
    ></movie-search-bar>
    
    <!-- 검색했을 때 결과값 -->
    <movie-card
      v-for="result in results"
      :key="result.id"
      :myMovie="result"
      isSearch="ture"
    ></movie-card>

    <!-- 장르별 카드 -->
    <div v-show="results.length === 0">
      <movie-list></movie-list>
    </div>
  </div>
</template>

<script>
import MovieSearchBar from'@/components/MovieSearchBar'
import MovieList from '@/components/MovieList'
import MovieCard from '@/components/MovieCard'
import drf from '@/api/drf'
import axios from 'axios'



export default {
  name: 'MovieSearch',
  components: {
    MovieList,
    MovieSearchBar,
    MovieCard
  },
  data: function () {
    return {
      inputData: null,
      results: [],
      movieId: null,
    }
  },
  methods: {
    onInputChange: function (inputData) {
      this.inputData = inputData
      axios({
        method: 'get',
        url: drf.movies.searchMovie(),
        params: {
          search: this.inputData
        },
        headers: this.$store.getters.authHeader
      })
        .then(response => {
          this.results = response.data
        })
        .catch(err => {
          console.log(err.response)
        })
    }
  },
}
</script>

<style>

</style>