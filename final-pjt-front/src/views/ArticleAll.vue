<template>
  <div>
    <h1>리뷰 전체 보기</h1>

    <!-- 리뷰 작성 form -->
    <div>
      <b-button v-b-modal.modal-footer-sm>새 리뷰 작성</b-button>
      <!-- 새 리뷰 모달 사용(vue bootstrap 사용) -->
      <b-modal id="modal-footer-sm" title="리뷰 작성" button-size="sm" hide-footer>
        <article-new></article-new>
      </b-modal>
    </div>

    <!-- 정렬 방법 (종아요, 최신순) -->
    <div class="mx-5">
      <div class="mx-5 d-flex justify-content-between">
        <p>Current Page: {{ currentPage }}</p>
        <div class="d-flex justify-content-end">
          <div class="btn-group" role="group" aria-label="Basic radio toggle button group">
            <input @change="ArticleSortStar" type="radio" class="btn-check" name="btnradio" id="btnradio1" autocomplete="off">
            <label class="btn btn-outline-primary" for="btnradio1">좋아요 순</label>
            <input @change="ArticleSortDate" type="radio" class="btn-check" name="btnradio" id="btnradio2" autocomplete="off" checked>
            <label class="btn btn-outline-primary" for="btnradio2">최신순</label>
          </div>
        </div>
      </div>

      <!-- 리뷰 표 작성 (vue bootstrap 사용) -->
      <b-container fluid>
        <div class="overflow-auto">
          <b-table
            id="my-table"
            :items="items"
            :per-page="perPage"
            :current-page="currentPage"
            :fields="fields"
            :filter="filter"
            small hover
          >

            <!-- 리뷰 상세 이동 링크 -->
            <template #cell(리뷰제목)="data">
              <a :href="`/articles/${data.item.pk}`">{{ data.value }}</a>
            </template>

            <!-- 리뷰 작성자 프로필 이동 링크 -->
            <template #cell(작성자)="data">
              <a :href="`/profile/${data.item.userPk}`">{{ data.value }}</a>
            </template>
          </b-table>
    
          <b-col class="my-1">
            <!-- 표 검색 (영화제목, 리뷰제목, 작성자 등등 다 검색 가능), vue bootstrap 사용-->
            <b-form-group
              label-for="filter-input"
              label-cols-sm="3"
              label-align-sm="right"
              label-size="sm"
              class="mb-0 w-50 mx-auto"
            >
              <b-input-group size="sm">
                <b-form-input
                  id="filter-input"
                  v-model="filter"
                  type="search"
                  placeholder="리뷰를 검색하세요"
                ></b-form-input>

                <b-input-group-append>
                  <b-button :disabled="!filter" @click="filter = ''">검색</b-button>
                </b-input-group-append>
              </b-input-group>
            </b-form-group>
          </b-col>

          <!-- 리뷰 20개씩 pagination(vue bootstrap 사용) -->
          <b-pagination
            v-model="currentPage"
            :total-rows="rows"
            :per-page="perPage"
            aria-controls="my-table"
            class="d-flex justify-content-center my-3"
          ></b-pagination>
        </div>
      </b-container>

    </div>
  </div>
</template>

<script>
  import { mapActions, mapGetters } from 'vuex'
  import ArticleNew from '@/components/ArticleNew'

  export default {
    name: 'ArticleAll',
    components: {
      ArticleNew
    },
    data() {
      return {
        perPage: 20, // 한 페이지에 리뷰 20개씩
        currentPage: 1,
        fields: ['영화제목', '별점', '리뷰제목', '작성자', '작성시간', '좋아요수'],
        items: [],
        filter: null,
      }
    },
    computed: {
      ...mapGetters(['articles']),
      rows() {
        return this.articles.length
      }
    },
    methods: {
      ...mapActions(['fetchArticles']),
      // 표 사용을 위해서 format 바꿔줌
      getItems () {
        this.articles.forEach(article => {
          this.items.unshift({pk: article.pk, 영화제목: article.movie.title, 별점:article.star_rate, 리뷰제목: article.title, 작성자: article.user.nickname, 작성시간: article.created_at, 좋아요수: article.like_users_count, userPk: article.user.pk})
        })
      },
      // 좋아요 순으로 정렬
      ArticleSortStar () {
        this.items.sort(function (a, b) {
          return b["좋아요수"] - a["좋아요수"]
        })
      },
      // 최신 순으로 정렬
      ArticleSortDate () {
        this.items.sort(function (a, b) {
          return b.pk - a.pk
        })
      },
    },
    created() {
      // 모든 리뷰 불러온 후
      this.fetchArticles()
      // format 바꿔줌
      this.getItems()
    },
  }
</script>

<style>

</style>