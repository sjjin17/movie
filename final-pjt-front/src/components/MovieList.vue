<template>
  <div class="container font" id="my-list">
    <div class="row">
      <div class="col-2 ">
        <div class="d-grid gap-2 col-6 mx-auto mt-5">

          <button
            v-for="(genre, idx) in genre_results"
            :key="idx"
            @click="[buttonClick(genre[0])]"
            type="button"
            class="btn btn-secondary btn-sm"
          >{{ genre[1] }}</button>
        </div>
      
        
      </div>
      <br>
      <br>
      <br>
      <br>
      <div class="col-10">
        <div class="d-flex flex-column">
          <div class="d-flex flex-row-reverse mx-5">
            <div class="btn-group" role="group" aria-label="Basic radio toggle button group">
              <input @change="getRecentMovies" type="radio" class="btn-check" name="btnradio" id="btnradio1" autocomplete="off">
              <label class="btn btn-outline-primary" for="btnradio1">최신순</label>
  
              <input @change="getVoteMovies" type="radio" class="btn-check" name="btnradio" id="btnradio2" autocomplete="off">
              <label class="btn btn-outline-primary" for="btnradio2">평점순</label>
            </div>
          </div>
          <div class="row hidden-md-up">
            <div class="row row-cols-1 row-cols-md-3 row-cols-lg-6">
              <movie-card
                v-for="movie in getPage"
                :key="movie.id"
                :myMovie="movie"
                :movieId="movie.id"
                @get-modal-show="getModalIsShow"
                class="my-2"
              >
              <!-- <b-modal  size="xl" v-if="isModalShow" ref="modal2" id="modal2" title="Loading" hide-footer no-close-on-backdrop> -->
        
                <!-- <movie-modal
                  :movieId ="movie.id"
                  :modalShow="modalShow"
                >
                </movie-modal> -->
              <!-- </b-modal> -->
              </movie-card>
            </div>
          </div>
        </div>
      
      </div>

    </div>
    <b-pagination
      v-model="currentPage"
      :total-rows="getTotal"
      :per-page="perPage"
      aria-controls="my-list"
      first-text="First"
      prev-text="Prev"
      next-text="Next"
      last-text="Last"
      :limit=10
      @click="setPage"
      class="d-flex justify-content-center"
    ></b-pagination>


  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import MovieCard from '@/components/MovieCard'
// import MovieModal from '@/components/MovieModal'


export default {
  name: 'MovieList',
  components: {
    MovieCard,
    // MovieModal
  

  },
  data: function () {
    return {
      genreMovies: [],
      isShow: false,
      items: [],
      isModalShow: false,
      movieId: null,
      perPage: 18,
      currentPage: 1,
      userId: null,
      hateGenreId: [],
      genre_results: []
    }
  },
  computed: {
    ...mapGetters(['genres', 'genre', 'currentUser', 'profile']),
    getTotal: function () {
      return this.items.length
    },
    getPage: function () {

      return this.items.slice(
        (this.currentPage -1) * this.perPage, this.currentPage * this.perPage,
      )
    },

  
  },
  methods: {
    ...mapActions([
      'fetchGenres', 'fetchGenre', 'fetchProfile',
    ]),
    buttonClick: function (genreId) {
      this.fetchGenre(genreId)
      this.items = [...this.genre.movies_genres]
    },
    getRecentMovies () {
      // console.log(this.items.slice(0, 1))
      this.items.sort(function (a, b) {
        return new Date(b.release_date) - new Date(a.release_date)
      })
    },
    getVoteMovies () {
      // console.log(this.items.slice(0, 1))
      this.items.sort(function (a, b) {
        return b.vote_average - a.vote_average
      })
    },
    getModalIsShow: function (movie_id) {
      this.isModalShow = true
      this.movieId = movie_id
      console.log(this.movieId)
    },
    filterHateGenre: function () {
      this.userId = this.currentUser.pk
      // console.log(this.userId)
      console.log(this.profile)
      console.log(this.profile.hate_genre[0])
      this.hateGenreId = this.profile.hate_genre
      // for (genre in this.genres) {
      //   if (genre in hateGenreId) {
      //     this.genres.pop
      //   }
      let tmp = [[12, "모험"], [14, "판타지"], [16, "애니메이션"], [18, "드라마"], [27, "공포"], [28, "액션"], [35, "코미디"], [36, "역사"], [37, "서부"], [53, "스릴러"], [80, "범죄"], [99, "다큐멘터리"], [878, "SF"], [9648, "미스터리"], [10402, "음악"], [10749, "로맨스"], [10751, "가족"], [10752, "전쟁"], [10770, "TV 영화"]]
      console.log(1)
      let difference = tmp.filter(x => !this.hateGenreId.includes(x[0]))
      console.log(difference)
      this.genre_results = difference
    }
  },

  created() {
    this.fetchGenres(),
    this.filterHateGenre()
    // this.fetchProfile(this.userId)
    
  },
  // mounted() {   
  //   this.$ref.modal1.show()
  // }
}
</script>

<style>
.font {
  font-family: sans-serif, Arial;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>