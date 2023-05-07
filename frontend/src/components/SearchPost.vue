<template>
  <div class="row g-0">
    <div class="col-md-6 order-first order-md-last" style="min-height: 250px">
      <div class="text-white p-4 p-md-5">
        <h2 class="fw-bold text-white mb-3">{{ this.post.title }}</h2>
        <p class="mb-2">{{ this.post.text.slice(0, 120) + "..." }}</p>
        <span
          ><router-link :to="{ name: 'post', params: { id: post.roll } }"
            >Read More</router-link
          ></span
        >
      </div>
    </div>
    <div class="col-md-6">
      <img
        alt="Post Image"
        class="w-100 d-block"
        style="object-fit: cover; height: 320px"
        :src="this.postImg"
      />
    </div>
  </div>
</template>

<script>
export default {
  name: "SearchPost",
  props: {
    post: {
      type: Object,
      required: true,
    },
  },
  computed: {
    postImg() {
      if (this.post) {
        return (
          "http://192.168.1.8:2345/static/img/Posts/" + this.post.img + ".webp"
        );
      }
      return require("@/assets/default_post.webp");
    },
  },
};
</script>
