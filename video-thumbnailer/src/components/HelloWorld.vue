<template>
  <div class="hello">
      <ul v-for="i in gifs">
        {{i['name']}}
      </ul>

  </div>
</template>

<script>
    import axios from 'axios'
    export default {
        name: 'HelloWorld',
        gifs: [],
        props: {
        msg: String
        },
        mounted () {
          axios.get("http://127.0.0.1:5000/gifs?list").then((response) => {
            this.gifs = response.data['objects']
          })
        }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
