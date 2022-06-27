<template>
  <nav class="nabarbackground">
    <div class="container">

      <ul class="row justify-content-end">
        <div class="col-6 d-flex">
          <div class="mx-3">
            <router-link :to="{ name: 'HomeView' }">Home</router-link>
          </div>
          <div v-if="isLoggedIn" class="mx-3">
            <router-link :to="{ name: 'ArticleAll' }">Review</router-link>
          </div>
          <div class="mx-3">
            <router-link :to="{ name: 'MovieSearch' }">Search</router-link>
          </div>
        </div>

        <div class="col-1 d-flex">
          <div v-if="!isLoggedIn" class="mx-3">
            <router-link :to="{ name: 'login' }">Login</router-link>
          </div>
          <div v-if="isLoggedIn" class="mx-3">
            <router-link :to="{ name: 'logout' }">Logout</router-link>
          </div>
          <div v-if="!isLoggedIn" class="mx-3">
            <router-link :to="{ name: 'signup' }">Signup</router-link>
          </div>
          <div v-if="isLoggedIn" class="mx-3">
            <router-link :to="{ name: 'profile', params: { userPk: currentUser.pk } }">
              Mypage 
            </router-link>
          </div>
        </div>
      </ul>
    </div>
  </nav>
</template>

<script>
  import { mapGetters } from 'vuex'

  export default {
    name: 'NavBar',

    computed: {
      ...mapGetters(['isLoggedIn', 'currentUser']),
    },
    
  }
</script>

<style>
.nabarbackground {
 background-image: url("../assets/update_navbar.png");
 height: 100px
 /* background-color: #cccccc; */
}
</style>
