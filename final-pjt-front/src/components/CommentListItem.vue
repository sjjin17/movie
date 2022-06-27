<template>
  <ul class="comment-list-item">
    <!-- <router-link :to="{ name: 'profile', params: { username: comment.user.username } }">
      {{ comment.user.username }}
    </router-link>:  -->

    <span v-if="!isEditing" class="mx-3">{{ payload.usernickname }}</span>
    <span v-if="!isEditing" style="font-weight: bold;">{{ payload.content }}</span>
    <span v-if="!isEditing" class="mx-3">{{ payload.created_at }}</span>

    <span v-if="isEditing">
      <input type="text" v-model="payload.content">
      <button @click="onUpdate">Update</button> |
      <button @click="switchIsEditing">Cancle</button>
    </span>

    <span v-if="currentUser.username === comment.user.username && !isEditing">
      <button @click="switchIsEditing">Edit</button> |
      <button @click="deleteComment(payload)">Delete</button>
    </span>
  </ul>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'CommentListItem',
  props: { comment: Object },
  data() {
    return {
      isEditing: false,
      payload: {
        articlePk: this.comment.review,
        commentPk: this.comment.pk,
        content: this.comment.content,
        created_at: this.comment.created_at,
        usernickname: this.comment.user.nickname,
      },
    }
  },
  computed: {
    ...mapGetters(['currentUser']),
  },
  methods: {
    ...mapActions(['updateComment', 'deleteComment']),
    switchIsEditing() {
      this.isEditing = !this.isEditing
    },
    onUpdate() {
      this.updateComment(this.payload)
      this.isEditing = false
    }
  },

}
</script>

<style>

</style>