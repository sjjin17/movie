<template>
  
  <div class="col font">
    <div class="card" sytle="width:100%;" @click="[getIsModalShow(myMovie.id), $refs['modal2'].show()]">
      <div v-show="!isSearch">
        <img :src="movieImagePath" class="card-img-top rounded float-left img-thumbnail"  :alt="myMovie.title" sytle="width:100;">
      </div>
      <!-- 영화 검색 결과는 이미지 대신 영화 제목만 나오도록 -->
      <div v-show="isSearch">
        <div class="card-body">
          <h5 class="card-title fx-6 overflow" style="font-size:small;">{{ myMovie.title }}</h5>
        </div>
      </div>
    </div>
    <b-modal title=" " body-text-variant="light" header-bg-variant="dark" body-bg-variant="dark" footer-bg-variant="dark" size="xl" ref="modal2" id="modal2" hide-footer close-on-backdrop>

      <movie-modal
        :movieId ="myMovie.id"
        
      >
      </movie-modal>
    </b-modal>
  </div>  
</template>

<script>
import MovieModal from '@/components/MovieModal'

export default {
  name: 'MovieCard',
  components: {
    MovieModal
  },
  // data () {
  //   return {
  //     isSearchState: 0
  //   }
  // },

  props: {
    similarMovie: Object,
    myMovie: Object,
    movieId: Number,
    isModalShow: Boolean,
    isSearch: Boolean,
  },
  computed: {
    movieImagePath: function () {
      return 'https://www.themoviedb.org/t/p/w300_and_h450_bestv2' + this.myMovie.poster_path
    },
  },
  methods: {
    getIsModalShow: function(movie_id) {
      this.$emit('get-modal-show', movie_id)
    },


  },


  
  
}
</script>

<style>
  .overflow {
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 4; 
    -webkit-box-orient: vertical;
  }
  .imgsize {
    height: 100px;
    width: 100px;
  }
  #font {
  font-family: sans-serif, Arial;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  }
</style>