<template>
  <div class="row g-0">
    <div class="col-md-6 order-first order-md-last" style="min-height: 250px">
      <div class="text-white p-4 p-md-5">
        <h2 class="fw-bold text-white mb-3">{{ this.user.username }}</h2>
        <p class="mb-2">Articles written: {{ this.user.articles }}</p>
        <p class="mb-2">Followers: {{ this.user.followers }}</p>
        <p class="mb-2">Following: {{ this.user.follows }}</p>
        <div class="my-3">
          <router-link
            class="btn btn-primary btn-lg me-2"
            role="button"
            :to="this.accountUrl"
            >Profile</router-link
          >
        </div>
      </div>
    </div>
    <div class="col-md-6">
      <img
        alt="User Image"
        class="w-100 d-block"
        style="height: 320px; object-fit: cover"
        :src="this.userImg"
      />
    </div>
  </div>
</template>

<script>
export default {
  name: "SearchUser",
  props: {
    user: {
      type: Object,
      required: true,
    },
  },
  computed: {
    accountUrl() {
      return "/account/" + this.user.username;
    },
    userImg() {
      if (this.user) {
        return (
          "http://192.168.1.8:2345/static/img/Users/" + this.user.img + ".webp"
        );
      }
      return require("@/assets/0.webp");
    },
  },
};
</script>
