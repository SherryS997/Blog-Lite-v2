<template>
  <PostComp
    :post="this.compPost.post"
    :user="this.compPost.author"
    :comments="this.compComments"
    @updateComments="updateComments"
  />
</template>

<script>
import PostComp from "@/components/Post.vue";
import axios from "axios";

export default {
  components: { PostComp },
  name: "PostView",
  data() {
    return {
      post: null,
      comments: null,
    };
  },
  methods: {
    updateComments() {
      this.fetchData();
    },
    async fetchData() {
      await axios
        .get("http://192.168.1.8:2345/vueapp/post/" + this.$route.params.id)
        .then((response) => response)
        .then((result) => {
          this.post = result.data;
        })
        .catch(() => {
          // console.error("Error fetching data:", error);
        });
      await axios
        .get(
          "http://192.168.1.8:2345/vueapp/post/" +
            this.$route.params.id +
            "/comment"
        )
        .then((response) => response)
        .then((result) => {
          this.comments = result.data;
        })
        .catch(() => {
          // console.error("Error fetching data:", error);
        });
      this.$forceUpdate();
    },
  },
  computed: {
    compComments() {
      return this.comments;
    },
    compPost() {
      return this.post;
    },
  },
  async beforeMount() {
    this.fetchData();
  },
  mounted() {
    document.title = "Post";
  },
};
</script>
