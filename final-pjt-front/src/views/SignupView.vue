<template>
  <div>
    <h1>Signup</h1>
 
    <account-error-list v-if="authError"></account-error-list>

    <form @submit.prevent="signup(credentials)">
      <div>
        <label for="username">Username: </label>
        <input  v-model="credentials.username" type="text" id="username" required/>
      </div>
      <div>
        <label for="password1">Password: </label>
        <input v-model="credentials.password" type="password" id="password1" required />
      </div>
      <div>
        <label for="password2">Password Confirmation:</label>
        <input v-model="credentials.passwordConfirmation" type="password" id="password2" required />
      </div>
      <div>
        <label for="nickname">닉네임:</label>
        <input v-model="credentials.nickname" type="text" id="nickname" required />
      </div>


            <!-- profile_img(선택, image)
      nickname(필수, char)
      hate_genre(선택) -->

      <div>
        <button>Signup</button>
      </div>
    </form>
  </div>
</template>

<script>
  import { mapActions, mapGetters } from 'vuex'
  import AccountErrorList from '@/components/AccountErrorList.vue'

  export default {
    name: 'SignupView',
    components: {
      AccountErrorList,
    },
    data() {
      return {
        credentials: {
          username: '',
          password: '',
          passwordConfirmation:'',
          nickname: '',
        }
      }
    },
    computed: {
      ...mapGetters(['authError'])
    },
    methods: {
      ...mapActions(['signup'])
    },
  }
</script>

<style></style>
