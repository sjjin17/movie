<template>
  <div id="font">
    <!-- <div>{{ profile }}</div> -->

    <!-- 작성 글, 좋아요 영화, 찜 영화 버튼 만들기 -->
    <!-- 두개씩 뽑고 세부페이지 모달 -->
    <h1 class="my-3">{{ profile.nickname }}님의 프로필</h1>
    <div v-if="currentUser.pk === $route.params.userPk" class="mx-3">
      <router-link :to="{ name: 'ProfileEdit', params: { userPk: currentUser.pk } } ">회원정보 수정</router-link>
    </div>
    <hr>
    <div class="d-flex justify-content-evenly">
      <img :src="profile_url" alt="안 떠?" id="profile_img" class="imgsize">
      <div class="d-flex flex-column justify-content-center">
        <h3 class="mx-1 my-2 me-5">
          아이디: {{ profile.username }}
        </h3>
        <h3 class="mx-1 my-2 me-5" v-if="profile.nickname">
          닉네임: {{ profile.nickname }}
        </h3>
      </div>
    </div>
    <hr>
    <div v-if="profile.review_set">
      <h2>작성한 글</h2>
      <div>작성한 글 갯수: {{ profile.review_count }}</div>
      <!-- <ul>
        <div v-for="article in profile.review_set" :key="article.pk">
          <div class="d-flex just">
            <router-link :to="{ name: 'article', params: { articlePk: article.pk } }">
              {{ article.title }}
            </router-link>
            <div>
              {{ article.content }}
            </div>
          </div>
        </div>
      </ul> -->
      <div class="mx-5">
        <table class="table mx-5">
          <thead>
            <tr>
              <th scope="col">#</th>
              <th scope="col">리뷰 제목</th>
              <th scope="col">리뷰 내용</th>
            </tr>
          </thead>
          <tbody v-for="(article, idx) in profile.review_set" :key="idx">
            <tr>
              <th scope="row">{{ idx + 1 }}</th>
              <td><a :href="`/articles/${article.pk}`">{{ article.title }}</a></td>
              <td>{{ article.content }}</td>
            </tr>
          </tbody>
        </table>

      </div>
    </div>
    <br>
    <div v-if="profile.comment_count">
      <h2>작성한 댓글</h2>
      <div class="my-2">작성한 댓글 갯수: {{ profile.comment_count }}</div>
      <ul>
        <span v-for="comment in profile.comment_set" :key="comment.pk" class="mx-3">
          {{ comment.content }}
        </span>
      </ul>
    </div>

    <div v-if="profile.onelinecomment_count">
      <h2>작성한 한줄평</h2>
      <div class="my-2">작성한 한줄평 갯수: {{ profile.onelinecomment_count }}</div>
      <ul>
        <div v-for="onelinecomment in profile.onelinecomment_set" :key="onelinecomment.pk" class="mx-3">
          {{ onelinecomment.content }}
        </div>
      </ul>
    </div>

    <hr>
    <div v-if="profile.save_movies_count">
      <br>
      <h2>저장한 영화</h2>
      <div>저장한 영화 갯수: {{ profile.save_movies_count }}</div>
      <br>
      <ul>
        <div class="row row-cols-1 row-cols-md-4 g-4">
          <div v-for="save_movie in profile.save_movies" :key="save_movie.id">
            <div class="col">
              <div class="card" sytle="width:100%;">
                <img :src="'https://www.themoviedb.org/t/p/w300_and_h450_bestv2' + save_movie.poster_path" class="card-img-top rounded float-left img-thumbnail"  :alt="save_movie.title" sytle="width:100;">
                <div class="card-body">
                  <h5 class="card-title fx-6 overflow">{{ save_movie.title }}</h5>
                </div>
              </div>
            </div>
          </div>
        </div>
      </ul>
    </div>

    <div v-if="profile.like_movies_count">
      <h2>좋아요한 영화</h2>
      <div>좋아요한 영화 갯수: {{ profile.like_movies_count }}</div>
      <ul>
        <div class="row row-cols-1 row-cols-md-4 g-4">
          <div v-for="like_movie in profile.like_movies" :key="like_movie.id" class="d-flex flex-column">
            <div class="col">
              <div class="card" sytle="width:100%;">
                <img :src="'https://www.themoviedb.org/t/p/w300_and_h450_bestv2' + like_movie.poster_path" class="card-img-top rounded float-left img-thumbnail"  :alt="like_movie.title" sytle="width:100;">
                <div class="card-body">
                  <h5 class="card-title fx-6 overflow">{{ like_movie.title }}</h5>
                </div>
              </div>
            </div>
          </div>
        </div>
      </ul>
    </div>


  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'


export default {
  name: 'ProfileView',
  data() {
    return {
      profile_url: null,
    }
  },
  computed: {
    ...mapGetters(['profile', 'currentUser']),
  },
  methods: {
    ...mapActions(['fetchProfile', 'fetchCurrentUser']),
  },
  created() {
    this.fetchCurrentUser()
    const payload = { userPk: this.$route.params.userPk }
    this.fetchProfile(payload)
    this.profile_url = "http://127.0.0.1:8000" + this.profile.profile_img
  },
}
</script>

<style>
#font {
  font-family: sans-serif, Arial;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>