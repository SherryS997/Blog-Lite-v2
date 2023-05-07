<template>
  <div class="home">
    <HomePage
      :posts="readyDiscoverPosts"
      :discover="true"
      :user="this.compUser"
      @updateData="updateData"
      v-show="this.readyDiscover"
    />
    <HomePage
      :posts="readyHomePosts"
      :discover="false"
      :user="this.compUser"
      @updateData="updateData"
      v-show="!this.readyDiscover"
    />
  </div>
</template>

<script>
import HomePage from "@/components/Home.vue";
import axios from "axios";

export default {
  name: "HomeView",
  components: {
    HomePage,
  },
  props: {
    discover: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      userSession: JSON.parse(localStorage.getItem("userSession")) || null,
      discoverPosts: null,
      homePosts: null,
      user: null,
    };
  },
  methods: {
    updateData() {
      this.fetchDiscoverData();
      this.fetchHomeData();
    },
    async fetchDiscoverData() {
      await axios
        .get(`http://192.168.1.8:2345/vueapp/post/all`)
        .then((result) => result.data)
        .then((result) => {
          this.discoverPosts = result.slice(0, 6);
        })
        .catch(() => {
          // console.error("Error fetching data:", error);
        });
      this.$forceUpdate();
    },
    async fetchHomeData() {
      if (this.userSession) {
        axios.defaults.headers.common[
          "Authorization"
        ] = `Bearer ${this.userSession.token}`;
        await axios
          .get("http://192.168.1.8:2345/vueapp/token")
          .then((response) => response)
          .then((result) => {
            this.user = result.data;
          })
          .catch(() => {
            // console.error("Error fetching data:", error);
          });
      }
      await axios
        .get(`http://192.168.1.8:2345/vueapp/post/${this.cur}`)
        .then((result) => result.data)
        .then((result) => {
          this.homePosts = result.slice(0, 6);
        })
        .catch(() => {
          // console.error("Error fetching data:", error);
        });
      this.$forceUpdate();
    },
  },
  async beforeMount() {
    this.fetchHomeData();
    this.fetchDiscoverData();
  },
  computed: {
    compUser() {
      return this.user;
    },
    readyDiscover() {
      return this.discover;
    },
    readyDiscoverPosts() {
      return this.discoverPosts;
    },
    readyHomePosts() {
      return this.homePosts;
    },
    cur() {
      if (this.userSession) {
        return this.userSession.token;
      } else {
        return "all";
      }
    },
  },
  mounted() {
    document.title = "Home";
  },
};
</script>
