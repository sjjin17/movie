<template>
  <div>
    <div>
      <div>영화 제목</div>
      <div class="font d-flex">{{ article.movie.title }}</div>
    </div>
    <article-edit-form v-if="isArticle" :article="article" ></article-edit-form>
  </div>

</template>

<script>
// ArticleDetail의 자식component
import ArticleEditForm from '@/components/ArticleEditForm.vue'
import { mapGetters, mapActions } from 'vuex'
  export default {
    name: 'AritcleEditView',
    props: {
      articlePk: String,
    },
    components: { ArticleEditForm },
    
    computed: {
      ...mapGetters(['article', 'isArticle',])
    },
    methods: {
      ...mapActions(['fetchArticle'])
    },
    created() {
      this.fetchArticle(this.articlePk)
    },
  }
</script>

<style>
  .font {
    font-weight: bold;
    font-size: large;
  }
</style>