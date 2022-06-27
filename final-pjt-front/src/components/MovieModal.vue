<template>
  <div>
    <div class="d-flex">
      <img v-if="movie.video_path === 'fail'" :src="moviePosterPath" :alt="movie.title" class="imagesize ms-5">
      <iframe
        v-else
        class="col-5"
        width="300"
        height="300"        
        :src="movieVideoPath"        
        title="YouTube video player"
        frameborder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen
      ></iframe>
      <movie-detail
        :movieId="movieId"
        class="col-7"
        :isLike="isLike"
        @my-liked="myLiked"  
      ></movie-detail>
    </div>
    <br>
    <!-- <h4 class="d-flex justify-content-center">similar movies</h4> -->
    <div class="container d-flex">

    
      <div class="row">
        <!-- 한줄평 -->
        <div class="col-5">
          <form @submit.prevent="onSubmit">
            
            <div class="d-flex my-3">
              <div class="mx-2 star-rating d-flex align-content-center">   <!-- 별 모양으로 변경 -->
                <input type="radio" id="5-stars" name="rating" value="5" v-model="star_rate"/>
                <label for="5-stars" class="star" style="-webkit-text-stroke-color: white;">★</label>
                <input type="radio" id="4-stars" name="rating" value="4" v-model="star_rate"/>
                <label for="4-stars" class="star" style="-webkit-text-stroke-color: white;">★</label>
                <input type="radio" id="3-stars" name="rating" value="3" v-model="star_rate"/>
                <label for="3-stars" class="star" style="-webkit-text-stroke-color: white;">★</label>
                <input type="radio" id="2-stars" name="rating" value="2" v-model="star_rate"/>
                <label for="2-stars" class="star" style="-webkit-text-stroke-color: white;">★</label>
                <input type="radio" id="1-star" name="rating" value="1" v-model="star_rate" />
                <label for="1-star" class="star" style="-webkit-text-stroke-color: white;">★</label>
              </div>
              <div class="mx-2 d-flex align-content-center justify-content-center">

                <label for="one_line_comment"></label>
                <input type="text" id="one_line_comment" v-model="content">
              </div>

            
              <input type="submit">

            </div>

            

          </form>
          <!-- {{ linecomments }} -->
          <div class="container">
            <div class="row">
              <div class="col">닉네임 </div>
              <div class="col">별점 </div>
              <div class="col">한줄평</div>
            </div>
          </div>
          <div 
            v-for="linecomment in linecomments"
            :key="linecomment.pk"
            class="my-2"
          >
            <div class="container">
              <div class="row">
                <div class="col">{{ linecomment.user.nickname}} </div>
                <div class="col">
                  <div class="star-ratings">
                    <div 
                      class="star-ratings-fill space-x-2 text-lg"
                      :style="{ width: linecomment.star_rate * 20 + 1.5 + '%' }"
                    >
                      <span style="-webkit-text-stroke-color: #8c8f94;">★</span><span style="-webkit-text-stroke-color: #8c8f94;">★</span><span style="-webkit-text-stroke-color: #8c8f94;">★</span><span style="-webkit-text-stroke-color: #8c8f94;">★</span><span style="-webkit-text-stroke-color: #8c8f94;">★</span>
                    </div>
                    <div class="star-ratings-base space-x-2 text-lg">
                      <span style="-webkit-text-stroke-color: #8c8f94;">★</span><span style="-webkit-text-stroke-color: #8c8f94;">★</span><span style="-webkit-text-stroke-color: #8c8f94;">★</span><span style="-webkit-text-stroke-color: #8c8f94;">★</span><span style="-webkit-text-stroke-color: #8c8f94;">★</span>
                    </div>
                  </div>
                  <!-- {{ linecomment.star_rate }} -->
                </div>
                <div class="col">{{ linecomment.content }}</div>
              </div>
            </div>
            
          </div>
        </div>

        <!-- 유사한 영화목록 -->
        <div class="col-7">
          <div class="row row-cols-1 row-cols-md-3">
            
            <modal-card
              v-for="similarMovie in similarMovies"
              :key="similarMovie.id"
              :myMovie="similarMovie"
              class="my-2"
              
            >
            </modal-card>

          </div>

        </div>
      </div>
    </div>

  </div>
    

</template>

<script>
// MovieCarousel의 하위component
import axios from 'axios'
import { mapGetters, mapActions } from 'vuex'
import MovieDetail from '@/components/MovieDetail'
import ModalCard from '@/components/ModalCard'

const API_KEY = process.env.VUE_APP_TMDB_API_KEY
const API_URL = 'https://api.themoviedb.org/3/movie/'

export default {
  name: 'MovieModal',
  components: {
    MovieDetail,
    ModalCard,
  },
  props: { 
    movieId: Number,
    modalShow: Boolean,
    
    
  
    

  },
  data: function () {
    return {
      similarMovies: [],
      isLike : false,
      content: '',
      star_rate: null,
      
    
    }
  },
  computed: {
    ...mapGetters(['movie', 'linecomments']),
    movieVideoPath: function () {
      const youtubeUrl = 'https://www.youtube.com/embed/'
      return youtubeUrl + this.movie.video_path
    },
    moviePosterPath: function () {
      // return 'https://www.themoviedb.org/t/p/w300_and_h450_bestv2' + this.movie.poster_path
      return 'https://www.themoviedb.org/t/p/w300_and_h450_bestv2' + this.movie.poster_path
    },
    // ratingToPercent() {
    //   const score = +this.linecomment.star_rate * 20;
    //   return score + 1.5;
    // }
    
  },
  methods: {
    ...mapActions(['fetchMovie', 'fetchLineComments', 'createLineComment']),
    getSimilar: function () {
      axios({
        method: 'get',
        url: API_URL + this.movieId +'/similar',
        params: {
          api_key: API_KEY,   
          language: 'ko'
        }
      })
      .then(response => {
        //console.log(response.data)
        //this.similarMovies = response.data.results.slice(0, 4)
        this.similarMovies = response.data.results.sort(function (a, b) {
          return b["vote_count"] - a["vote_count"]  // vote_count혹은 popularity로 정렬한 후 slice
        }).slice(0, 6) // 6개 -> 4개 (자리 없음) -> 사이즈 변경 후 6개로 다시 변경
        console.log(this.similarMovies)
        console.log(this.movieId)
      })
    },
    onSubmit() {
      this.createLineComment({movie_pk: this.movieId, content: this.content, star_rate: this.star_rate})
      this.content = ''
      console.log('hello')
    },

  }, 
  created() {
    this.fetchMovie(this.movieId)
    //console.log(this.movie.title)
    this.getSimilar()
    this.fetchLineComments(this.movieId)
    
    
  },
  
}
</script>

<style>
  .imagesize{ 
    max-height: 450px;
    max-width: 350px;
  }

  .star-rating {
    display: flex;
    flex-direction: row-reverse;
    font-size: 1.5rem;
    line-height: 1.75rem;
    justify-content: space-around;
    padding: 0 0.2em;
    text-align: center;
    width: 3em;
  }
  
  /* radio 클릭부분 없애기 */
  .star-rating input {
    display: none;
  }
  
  /* 테두리만 있는 빈 별 */
  .star-rating label {
    /* -webkit-text-fill-color: transparent; */
    -webkit-text-stroke-width: 2.3px;
    -webkit-text-stroke-color: rgb(255, 255, 255);
    cursor: pointer;
  }
  
  /* 클릭했을 때 별 색깔(클릭하면 별 색 더 진해지도록) */
  .star-rating :checked ~ label {
    -webkit-text-fill-color: gold;
  }
  
  /* 별 위에 눌렀을 때 별 색깔 */
  .star-rating label:hover,
  .star-rating label:hover ~ label {
    -webkit-text-fill-color: #fff58c;
  }

  .star-ratings {
    color: #aaa9a9; 
    position: relative;
    unicode-bidi: bidi-override;
    width: max-content;
    -webkit-text-fill-color: transparent;
    -webkit-text-stroke-width: 0.2px;
    -webkit-text-stroke-color: #2b2a29;
  }
  
  .star-ratings-fill {
    color: #fff58c;
    padding: 0;
    position: absolute;
    z-index: 1;
    display: flex;
    top: 0;
    left: 0;
    overflow: hidden;
    -webkit-text-fill-color: gold;
  }
  
  .star-ratings-base {
    z-index: 0;
    padding: 0;
  }
</style>