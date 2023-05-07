<template>
  <div class="container" style="padding-top: 44px">
    <div
      class="bg-dark border rounded border-0 border-dark overflow-hidden"
      style="padding-bottom: 0px; margin-bottom: 64px"
    >
      <div class="p-md-3">
        <h3 class="fw text-white mb-2">{{ this.user }}'s {{ this.state }}:</h3>
      </div>
      <div v-for="user in this.compFollows" :key="user">
        <SearchUser :user="user"></SearchUser>
      </div>
    </div>
  </div>
</template>

<script>
import SearchUser from "@/components/SearchUser.vue";
import axios from "axios";

export default {
  name: "FollowView",
  components: { SearchUser },
  data() {
    return {
      state: this.$route.matched[0].name,
      user: this.$route.params.user,
      follows: null,
    };
  },
  methods: {
    async fetchData() {
      await axios
        .get("http://192.168.1.8:2345/vueapp/" + this.user + "/" + this.state)
        .then((response) => response)
        .then((response) => response.data)
        .then((results) => {
          this.follows = results;
        })
        .catch(() => {
          // console.error("Error fetching data:", error);
        });
      this.$forceUpdate();
    },
  },
  computed: {
    compFollows() {
      return this.follows;
    },
  },
  async beforeMount() {
    this.fetchData();
  },
  mounted() {
    document.title = this.state == "follows" ? "Follows" : "Followers";
  },
};
</script>
