<template>
  <div>
  
    
    <div class="col">
      <div class="card" sytle="width:100%;">       
        <img :src="movieImagePath" class="card-img-top rounded float-left img-thumbnail"  :alt="myMovie.title" sytle="width:100;">        
      </div>
    </div>  
  </div>
</template>

<script>
// MovieModal의 하위component

export default {
  name: 'ModalCard',



  computed: {
    movieImagePath: function () {
      return 'https://www.themoviedb.org/t/p/w300_and_h450_bestv2' + this.myMovie.poster_path
    },
  },
  props: {
    similarMovie: Object,
    myMovie: Object,
    movieId: Number,
  }

  
    

  
  
}
</script>

<style>
  
  .black-bg {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgb(0,0, 0, 0.6);

    z-index: 1050;
  }
  .white-bg {
    width: 90%;
    margin: 80px auto;
    background: white;
    border-radius: 5px;
    padding: 20px 0;
  }
  .overflow {
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 4; 
    -webkit-box-orient: vertical;
  }
  .imgsize {
    height: 100px;
    width: 100px;
  }
  #font {
  font-family: sans-serif, Arial;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  }

</style>