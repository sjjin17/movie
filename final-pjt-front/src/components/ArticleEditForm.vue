<template>
  <div>
    <form @submit.prevent="onSubmit">
      <!-- 별점 수정 -->
      <div class="my-3">
        <div class="d-flex">별점</div>
        <div class="star-rating">   <!-- 별 모양으로 변경 -->
          <input type="radio" id="5-stars" name="rating" value="5" v-model="newArticle.star_rate"/>
          <label for="5-stars" class="star pr-4">★</label>
          <input type="radio" id="4-stars" name="rating" value="4" v-model="newArticle.star_rate"/>
          <label for="4-stars" class="star">★</label>
          <input type="radio" id="3-stars" name="rating" value="3" v-model="newArticle.star_rate"/>
          <label for="3-stars" class="star">★</label>
          <input type="radio" id="2-stars" name="rating" value="2" v-model="newArticle.star_rate"/>
          <label for="2-stars" class="star">★</label>
          <input type="radio" id="1-star" name="rating" value="1" v-model="newArticle.star_rate" />
          <label for="1-star" class="star">★</label>
        </div>
      </div>

      <!-- 리뷰제목 수정 -->
      <div class="d-flex flex-column my-3">
        <label for="title">리뷰 제목</label>
        <input v-model="newArticle.title" type="text" id="title" />
      </div>

      <!-- 리뷰내용 수정 -->
      <div class="d-flex flex-column my-3">
        <label for="content">리뷰 내용</label>
        <textarea v-model="newArticle.content" type="text" id="content" class="textarea-height"></textarea>
      </div>

      <!-- 수정버튼 -->
      <div class="my-1">
        <button>수정</button>
      </div>
    </form>
  </div>
</template>

<script>
// ArticleEdit의 자식component
import { mapActions } from 'vuex'

  export default {
    name: 'ArticleEditForm',
    props: {
      article: Object,
    },
    data() {
      return {
        newArticle: {
          star_rate: this.article.star_rate,
          title: this.article.title,
          content: this.article.content,
        }
      }
    },

    methods: {
      ...mapActions(['updateArticle']),
      onSubmit() {
        const payload = {
          pk: this.article.pk,
          ...this.newArticle,
        }
        this.updateArticle(payload)
      },
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

  /* 리뷰 내용 크기 늘리기 */
  .textarea-height {
    height: 200px;
  }
</style>