<template>
  <div class="font d-flex justify-content-center">

    <div  class=" border formsize">
      
      <h1 class="my-3">{{ profile.username }}님의 회원정보 수정</h1>
      <!-- {{ profile }} -->
      <hr>
      <form @submit.prevent="onSubmit" enctype="multipart/form-data">
        <div class="d-flex justify-content-evenly">
          <img :src="profile_img" alt="안 떠?" id="profile_img" class="imgsize">
          <div class="d-flex flex-column justify-content-center">
            <div class="mx-1 my-2">
              아이디: {{ profile.username }}
            </div>
            <div class="mx-1 my-2">
              <label for="nickname">닉네임: </label>
              <!-- <b-form-input v-model="newProfile.nickname" placeholder="닉네임을 입력하세요" id="nickname"></b-form-input> -->
              <input v-model="newProfile.nickname" type="text" id="nickname" placeholder="닉네임을 입력하세요"/>
            </div>
          </div>
        </div>
        <div>
          <h2>선호하지 않는 장르르 선택하세요!</h2>
          <div>선택 시 그 장르 영화는 추천되지 않습니다.</div>
          <div>단, 검색은 가능합니다</div>
          <b-form-group v-slot="{ ariaDescribedby }" >
            <b-form-checkbox-group
              id="checkbox-group-1"
              v-model="newProfile.hate_genre"
              :options="options"
              :aria-describedby="ariaDescribedby"
              name="flavour-1"
            ></b-form-checkbox-group>
          </b-form-group>
        </div>
        <!-- <div>
          <div>
            <label for="chooseFile">사진 변경</label>
          </div>
          <input ref="image" @change="uploadImg()" type="file" id="chooseFile" name="chooseFile" accept="image/*">
        </div>  -->
        <button class="btn btn-primary my-3">수정</button>
      </form>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: "ProfileEdit",
  data() {
    return {
      profile_img: null,
      newProfile: {
        nickname: null,
        // profile_img: null,
        hate_genre: [],  //옵션에서 selected 된거
      },
      options: [],
    }
  },
  computed: {
    ...mapGetters(['profile', 'genres'])
  },
  methods: {
    ...mapActions(['fetchProfile', 'updateProfile', 'fetchGenres', 'updateProfileTwo']),
    onSubmit() {

      // 이미지 이외 변경
      const payload = {
        pk: this.profile.id,
          ...this.newProfile,
        }
      console.log(payload)
      this.updateProfile(payload)

      // // 이미지 변경
      // console.log(this.profile_img)
      // const formdata = new FormData()
      // formdata.append('profile_img', this.profile_img)
      // // formdata.append('pk', this.profile.id)
      // console.log(formdata)
      // this.updateProfileTwo(formdata)

    },
    // uploadImg() {
    //   this.profile_img = this.$refs['image'].files[0]

    // },


  },
  created() {
    const payload = { userPk: this.$route.params.userPk }
    this.fetchProfile(payload)
    this.newProfile.nickname = this.profile.nickname
    this.newProfile.hate_genre = this.profile.hate_genre
    this.profile_img = "http://127.0.0.1:8000" + this.profile.profile_img
    this.fetchGenres()
    this.genres.forEach(genre => {
      this.options.push({ text: genre.name, value: genre.id })
    })
  },

}
</script>

<style>
.formsize {
  width:50%
}
.imgsize {
  width: 30%;
  height: 30%;
}
#font {
  font-family: sans-serif, Arial;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>