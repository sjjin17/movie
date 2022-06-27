<template>
  <div>
    <h1>ArticleList</h1>
    <ul>
      <li v-for="article in articles" :key="article.pk">
        {{ article }}
      </li>
      <article-item>
      </article-item>
    </ul>
  </div>
</template>

<script>
  import ArticleItem from '@/components/ArticleItem'
  import { mapActions, mapGetters } from 'vuex'

  export default {
    name: 'ArticleList',
    components: { ArticleItem },
    computed: {
      ...mapGetters(['articles'])
    },
    methods: {
      ...mapActions(['fetchArticles'])
    },
    created() {
      this.fetchArticles()
    },
  }
</script>

<style>

</style>