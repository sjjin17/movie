<template>
  <div>
    <input type="text"  @keyup="searchTimeOut">
    <input type="submit">
  </div>
</template>

<script>
export default {
  name: 'MovieSearchBar',
  data: function() {
    return {
      timer: null,
    }
  },
  methods: {

    searchTimeOut(event) {  
      if (this.timer) {
        clearTimeout(this.timer);
        this.timer = null
      }
      this.timer = setTimeout(() => {
        // your code
        this.$emit('input-change', event.target.value)
      }, 300)
    }   
  }
}
</script>

<style>  

</style>