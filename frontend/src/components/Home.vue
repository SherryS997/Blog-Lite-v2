<template>
  <div class="container py-4 py-xl-5">
    <div class="row mb-5">
      <div class="col-md-8 col-xl-6 text-center mx-auto">
        <h2 v-show="this.discover">Latest Articles</h2>
        <h2 v-show="!this.discover && this.loadedPosts.length > 0">
          Latest Articles from your follows
        </h2>
        <h2 v-show="this.loadedPosts.length == 0 && !this.discover">
          Checkout the Discover Page for the Latest Articles
        </h2>
      </div>
    </div>
    <div
      class="row gy-4 row-cols-1 row-cols-md-2 row-cols-xl-3"
      v-if="this.loadedPosts"
    >
      <div class="col" v-for="post in loadedPosts" :key="post">
        <post-short
          :post="post.post"
          :user="post.user"
          :cur="this.loadedUser"
          @updateData="updateData"
        />
      </div>
    </div>
    <div v-else>Loading</div>
  </div>
</template>

<script>
import PostShort from "@/components/PostShort.vue";

export default {
  components: { PostShort },
  name: "HomePage",
  props: {
    posts: {
      type: Array,
      required: true,
    },
    discover: {
      type: Boolean,
      required: true,
    },
    user: {
      type: Object,
      required: true,
    },
  },
  computed: {
    loadedPosts() {
      if (this.posts) {
        return this.posts;
      }
      return {};
    },
    loadedUser() {
      if (this.user) {
        return this.user;
      }
      return {};
    },
  },
  methods: {
    updateData() {
      this.$emit("updateData");
    },
  },
};
</script>
