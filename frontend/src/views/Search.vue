<template>
  <div class="container" style="padding-top: 44px">
    <div
      class="bg-dark border rounded border-0 border-dark overflow-hidden"
      style="padding-bottom: 0px; margin-bottom: 64px"
    >
      <div class="p-md-3" v-if="this.boolUsers">
        <p class="fw-bold text-white mb-2">
          Users found for the search term are as follows:
        </p>
      </div>
      <div v-if="this.boolUsers">
        <div v-for="user in this.compUsers" :key="user">
          <SearchUser :user="user"></SearchUser>
        </div>
      </div>
      <div class="p-md-3" v-if="!this.boolUsers">
        <p class="fw-bold text-white mb-3">
          No users found for the search term
        </p>
      </div>
    </div>
  </div>
  <div class="container" style="padding-bottom: 50px">
    <div class="bg-dark border rounded border-0 border-dark overflow-hidden">
      <div class="p-md-3" v-if="this.boolPosts">
        <p class="fw-bold text-white mb-3">
          Posts found for the search term are as follows:
        </p>
      </div>
      <div v-if="this.boolPosts">
        <div v-for="post in this.compPosts" :key="post">
          <SearchPost :post="post"></SearchPost>
        </div>
      </div>
      <div class="p-md-3" v-if="!this.boolPosts">
        <p class="fw-bold text-white mb-3">
          No Posts found for the search term
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import SearchPost from "@/components/SearchPost.vue";
import SearchUser from "@/components/SearchUser.vue";

export default {
  name: "SearchView",
  components: { SearchPost, SearchUser },
  data() {
    return {
      term: this.$route.params.term,
      users: null,
      posts: null,
    };
  },
  methods: {
    async fetchData() {
      await axios
        .get("http://192.168.1.8:2345/vueapp/search=" + this.term)
        .then((response) => response)
        .then((response) => response.data)
        .then((results) => {
          this.users = results.users;
          this.posts = results.posts;
        })
        .catch(() => {
          // console.error("Error fetching data:", error);
        });
      this.$forceUpdate();
    },
  },
  computed: {
    boolUsers() {
      if (this.users) {
        return this.users.length > 0;
      }
      return false;
    },
    boolPosts() {
      if (this.posts) {
        return this.posts.length > 0;
      }
      return false;
    },
    compUsers() {
      return this.users;
    },
    compPosts() {
      return this.posts;
    },
  },
  async beforeMount() {
    this.fetchData();
  },
  mounted() {
    document.title = "Search";
  },
};
</script>
