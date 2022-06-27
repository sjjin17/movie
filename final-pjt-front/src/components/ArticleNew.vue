<template>
  <div>
    <h1>새 리뷰 작성</h1>
    <form @submit="onSubmit">

      <!-- 리뷰 검색 기능, 리뷰 선택시 movie_pk를 submit -->
      <div>
        <label for="movie_pk">영화를 검색하세요</label>
        <v-select
          v-model="article.movie_pk"
          :reduce="(option) => option.pk"
          :options="searchMovies"
          label="title"
          id="movie_pk"
        >
        </v-select>
      </div>

      <!-- 별점 -->
      <div class="my-3">
        <div class="d-flex">별점</div>
        <div class="star-rating">   <!-- 별 모양으로 CSS -->
          <input type="radio" id="5-stars" name="rating" value="5" v-model="article.star_rate"/>
          <label for="5-stars" class="star pr-4">★</label>
          <input type="radio" id="4-stars" name="rating" value="4" v-model="article.star_rate"/>
          <label for="4-stars" class="star">★</label>
          <input type="radio" id="3-stars" name="rating" value="3" v-model="article.star_rate"/>
          <label for="3-stars" class="star">★</label>
          <input type="radio" id="2-stars" name="rating" value="2" v-model="article.star_rate"/>
          <label for="2-stars" class="star">★</label>
          <input type="radio" id="1-star" name="rating" value="1" v-model="article.star_rate" />
          <label for="1-star" class="star">★</label>
        </div>
      </div>
      <div class="d-flex flex-column my-3">
        <label for="title">리뷰 제목</label>
        <input v-model="article.title" type="text" id="title" />
      </div>
      <div class="d-flex flex-column my-3">
        <label for="content">리뷰 내용</label>
        <textarea v-model="article.content" type="text" id="content" class="textarea-height"></textarea>
      </div>
      <div class="my-1 d-flex justify-content-end">
        <button>제출</button>
      </div>
    </form>
  </div>
</template>

<script>
  // ArticleAll의 자식components
  import { mapGetters, mapActions } from 'vuex'
  import "vue-select/dist/vue-select.css"
  
  export default {
    name: 'AritcleNew',
    data() {
      return {
        article: {
          movie_pk: null,
          star_rate: null,
          title: '',
          content: '',
        },
      }
    },
    computed: {
      ...mapGetters(['searchMovies'])
    },
    
    methods: {
      ...mapActions(['createArticle', 'searchMovie']),
      onSubmit() {
        this.createArticle(this.article)
      },
    },
    created() {
      this.searchMovie(this.article.title)
    },
  }
</script>

<style>
  .star-rating {
    display: flex;
    flex-direction: row-reverse;
    font-size: 2.25rem;
    line-height: 2.5rem;
    justify-content: space-around;
    padding: 0 0.2em;
    text-align: center;
    width: 5em;
  }
  
  /* radio 클릭부분 없애기 */
  .star-rating input {
    display: none;
  }
  
  /* 테두리만 있는 빈 별 */
  .star-rating label {
    -webkit-text-fill-color: transparent;
    -webkit-text-stroke-width: 2.3px;
    -webkit-text-stroke-color: #2b2a29;
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

  .textarea-height {
    height: 200px;
  }
</style>