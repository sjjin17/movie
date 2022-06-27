<template>
  <div>
    
    <carousel
      :navigationEnabled="true" 
      :paginationEnabled="false"
      :navigationNextLabel="nextLabel"
      :navigationPrevLabel="prevLabel"
      :perPage="5"
      :scrollPerPage="false"
      :spacePadding="0"  
      
       
    >
      <slide
        v-for="movie in movies"
        :key="movie.id"
        :movie="movie"
        @slideclick="[selectMovie(movie.id)]"

        
      >
        <div>
          <span class="card mx-2" style="width: 18rem;">
            <img :src="movieImagePath+movie.poster_path" class="card-img-top"  :alt="movie.title" width="200" @click="$refs['modal1'].show()">
          </span>
        </div>      
      </slide>
      
      <b-modal class="overlay background" body-text-variant="light" header-bg-variant="dark" body-bg-variant="dark" footer-bg-variant="dark"  size="xl" v-if="isModalShow" ref="modal1" id="modal1" title="" hide-footer close-on-backdrop>
        <!-- {{movieId}} -->
        <movie-modal
          :movieId = "movieId"
          :modalShow="modalShow"
          :no-stacking="true"      
        ></movie-modal>
      </b-modal>


    </carousel>
    


  </div>
</template>

<script>
// HomeView의 자식component
import { Carousel, Slide } from 'vue-carousel'
import MovieModal from '@/components/MovieModal'





export default {
  name: 'MovieCarousel',
  components: {
    Carousel,
    Slide,
    MovieModal,
    
  },
  data() {
    return {
      modalShow: false,
      nextLabel: "<i class='fa-solid fa-angles-right'></i>",
      prevLabel: "<i class='fa-solid fa-angles-left'></i>",
      movieTitle: null,
      
      
    }
  },


  props: {
    movies: Array,
    movieId: Number,
    isModalShow: Boolean,
    
  },
  computed: {
    movieImagePath: function () {
      return 'https://www.themoviedb.org/t/p/w600_and_h900_bestv2/' 
    },
 
  },
  methods: {
    selectMovie: function (selectMovieId) {
      this.$emit('select-one-movie', selectMovieId)  
    },

    // showModal: function () {
    //   this.$ref.modal1.show()
    // }
  
    // focusMyElement() {
    //   this.$refs.focusThis.focus()
    // }




  },
  mounted() {
    
    this.$ref.modal1.show();
  }


}
</script>

<style>
  .background {
    background-color: black;
  }
  .modal,
  .overlay{
    width: 100%;
    height: 100%;
    position: fixed;
    left: 0;
    top: 0;
  }
  .overlay {
    opacity: 0.5;
    background-color: black;
  }

  

  

</style>