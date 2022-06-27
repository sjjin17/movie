<template>
  <div>
    <h1 class="border-bottom">리뷰 상세 페이지</h1>
    <br>


    <div class=" d-flex justify-content-center">
      <b-card no-body class="overflow-hidden bg-light" style="width: 90%;">
        <b-row no-gutters>
          <!-- 영화 제목, 이미지 -->
          <b-col md="4">
            <h4 class="mt-2">영화제목: <span style="font-weight:bold;">{{ article.movie.title }}</span></h4>
            <b-card-img :src="movieImagePath" :alt="article.movie.title" class="rounded-0"></b-card-img>
          </b-col>
          <!-- 리뷰 상세 -->
          <b-col md="8">
            <div class="container">
              <div class="row d-flex flex-column">
                <div class="col my-2">
                  <div class="d-flex justify-content-end my-3 mx-5">
                    <i @click="likeArticle(articlePk)" class="fa-regular fa-heart">  {{ likeCount }}</i>
                  </div>              
                  <div class="d-flex  justify-content-center">
                    <h1>{{ article.title }}</h1>
                  </div>
                </div>
                <!-- 리뷰 내용의 경우, html자체를 넣어줌 -->
                <div class="col my-2">
                  <p v-html="content"></p>
                </div>
                <!-- 별점 -->
                <div class="col d-flex justify-content-center my-2">
                  <div>
                    별점:
                  </div>
                  <div class="star-ratings d-flex justify-content-end">
                    <div 
                      class="star-ratings-fill space-x-2 text-lg"
                      :style="{ width: ratingToPercent + '%' }"
                    >
                      <span>★</span><span>★</span><span>★</span><span>★</span><span>★</span>
                    </div>
                    <div class="star-ratings-base space-x-2 text-lg">
                      <span>★</span><span>★</span><span>★</span><span>★</span><span>★</span>
                    </div>
                  </div>
                </div>

                <div class="col my-2">
                  작성자: {{ article.user.nickname }}
                </div>

                <!-- 작성시간, 수정시간 -->
                <div class="col my-2">
                  <div>{{ article.created_at }} 작성</div>
                  <div>{{ article.updated_at }} 수정</div>
                </div>

                <!-- 본인이 작성한 리뷰의 경우, 수정 및 삭제 가능 -->
                <div class="col my-2">                  
                  <div v-if="isAuthor">
                    <!-- 수정의 경우 모달로 나오도록 -->
                    <b-button v-b-modal.modal-footer-sm @click="modalShow = !modalShow" class="mx-1">수정</b-button>
                    <!-- <b-modal v-model="modalShow" id="modal-footer-sm" title="리뷰 수정" button-size="sm" hide-footer> -->
                    <b-modal v-model="modalShow" id="modal-footer-sm" title="리뷰 수정" button-size="sm" ok-only>
                      <article-edit :articlePk="articlePk"></article-edit>
                    </b-modal>
                    <button @click="deleteArticle(articlePk)" type="button" class="btn btn-secondary mx-1">삭제</button> 
                  </div>
                  
                </div>
              </div>
            </div>
          </b-col>
        </b-row>
      </b-card>
    </div>
    <hr>

    <div class="mx-5 border border-secondary my-2">
      <h3 class="mt-3">댓글</h3>
      <hr>
      <comment-list :comments="article.comment_set"></comment-list>
    </div>


  </div>
</template>

<script>
  import ArticleEdit from '@/components/ArticleEdit'
  import CommentList from '@/components/CommentList'
  import { mapGetters, mapActions } from 'vuex'

  export default {
    name: 'ArticleDetail',
    components: {
      ArticleEdit,
      CommentList,
    },
    data() {
      return {
        articlePk: this.$route.params.articlePk,
        modalShow: false,
        content: ""
      }
    },
    computed: {
      ...mapGetters(['article', 'isAuthor']),
      likeCount() {
        return this.article.like_users?.length
      },
      movieImagePath: function () {
        return 'https://www.themoviedb.org/t/p/w300_and_h450_bestv2' + this.article.movie.poster_path
      },
      ratingToPercent() {
        const score = +this.article.star_rate * 20;
        return score + 1.5;
      }
    },
    methods: {
      ...mapActions([
        'fetchArticle',
        'likeArticle',
        'deleteArticle',
      ])
    },
    created() {
      this.fetchArticle(this.articlePk)
      // content 줄 바꿈을 위해서 줄바꿈이 있는 부분을 <br>로 바꿔줌
      this.content = this.article.content.replaceAll(/(\n|\r\n)/g, "<br>")
    },
  }
</script>

<style>
  .star-ratings {
    color: #aaa9a9; 
    position: relative;
    unicode-bidi: bidi-override;
    width: max-content;
    -webkit-text-fill-color: transparent;
    -webkit-text-stroke-width: 1.3px;
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