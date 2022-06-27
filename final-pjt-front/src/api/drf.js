const HOST = 'http://localhost:8000/api/v1/'


const ACCOUNTS = 'accounts/'
const ARTICLES = 'communities/'
const CREATE = 'create/'
const COMMENTS = 'comments/'
const MOVIES = 'movies/'


export default {
  accounts: {
    login: () => HOST + ACCOUNTS + 'login/',
    logout: () => HOST + ACCOUNTS + 'logout/',
    signup: () => HOST + ACCOUNTS + 'signup/',
    // Token 으로 현재 user 판단
    currentUserInfo: () => HOST + ACCOUNTS + 'user/',
    // username으로 프로필 제공
    profile: userPk => HOST + ACCOUNTS + 'profile/' + `${userPk}/`,
    editprofile: userPk => HOST + ACCOUNTS + 'profile/' + `${userPk}/` + 'edit/',
    // editprofiletwo: () => HOST + ACCOUNTS + 'profile/edit/2/',
  },
  articles: {
    articles: () => HOST + ARTICLES,
    getarticle: moviePk => HOST + ARTICLES + `${moviePk}/` + CREATE,
    article: articlePk => HOST + ARTICLES + `${articlePk}/`,
    likeArticle: articlePk => HOST + ARTICLES + `${articlePk}/` + 'like/',
    comments: articlePk => HOST + ARTICLES + `${articlePk}/` + COMMENTS,
    comment: (articlePk, commentPk) =>
      HOST + ARTICLES + `${articlePk}/` + COMMENTS + `${commentPk}/`,
  },
  movies: {
    search: () => HOST + MOVIES,
    movies: () => HOST + MOVIES + 'all/',
    movie: moviePk => HOST + MOVIES + `${moviePk}/`,
    genres: () => HOST + MOVIES + 'genres/',
    genre: genrePk => HOST + MOVIES + 'genres/'+ `${genrePk}/`,
    likeMovie: moviePk => HOST + MOVIES + `${moviePk}/` + 'like/',
    saveMovie: moviePk => HOST + MOVIES + `${moviePk}/` + 'save/',
    searchMovie: () => HOST + MOVIES + 'search-result/',
    recommendation: () => HOST + MOVIES + 'recommendation/',
    lineComments: moviePk => HOST + MOVIES + `${moviePk}/` + 'linecomments/',
    deleteLinecomment: (moviePk, lineCommentPk) => HOST + MOVIES +`${moviePk}/` + `${lineCommentPk}/` +'delete/',
    
  }
}
