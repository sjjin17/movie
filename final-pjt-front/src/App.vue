<template>
  <div id="app">
    <nav-bar></nav-bar>
    <br>
    <br>
    <router-view></router-view>
  </div>
</template>
<script>
import NavBar from '@/components/NavBar'
import { mapActions } from 'vuex'

export default {
  name: 'App',
  components: { NavBar },
  methods: {
    ...mapActions(['fetchCurrentUser'])
  },
  created() {
    this.fetchCurrentUser()
  }
}
</script>

<style>
#app {
  font-family: sans-serif, Arial;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
