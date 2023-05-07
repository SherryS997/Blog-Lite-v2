<template>
  <div
    class="modal fade"
    :id="this.compModalName"
    tabindex="-1"
    :aria-labelledby="this.compModalName"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="exampleModalLabel">
            Delete Article?
          </h1>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          Delete the article "{{ this.post.title }}"?
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-danger" @click="deletePost">
            Yes
          </button>
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
          >
            No
          </button>
        </div>
      </div>
    </div>
  </div>
  <div class="row g-0">
    <div class="col-md-6 order-first order-md-last" style="min-height: 250px">
      <div class="text-white p-4 p-md-5">
        <h2 class="fw-bold text-white mb-3">{{ this.post.title }}</h2>
        <p class="mb-2">{{ this.post.text.slice(0, 150) + "..." }}</p>
        <router-link :to="{ name: 'post', params: { id: this.post.roll } }"
          >Read More</router-link
        >
        <div class="my-3" v-if="this.state">
          <router-link
            class="btn btn-primary btn-lg me-2"
            :to="{ name: 'blogEdit', params: { id: this.post.roll } }"
            >Edit Article</router-link
          >
          <button
            type="button"
            class="btn btn-light btn-lg"
            data-bs-toggle="modal"
            :data-bs-target="this.compModalHashName"
          >
            Delete Article
          </button>
        </div>
      </div>
    </div>
    <div class="col-md-6">
      <img
        alt="Post Image"
        class="w-100 d-block"
        style="object-fit: cover; height: 350px"
        :src="this.postImg"
      />
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "postSide",
  data() {
    return {
      userSession: JSON.parse(localStorage.getItem("userSession")) || null,
    };
  },
  props: {
    post: {
      type: Object,
      required: true,
    },
    state: {
      type: Boolean,
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
    compModalName() {
      return this.post.roll + "Modal";
    },
    compModalHashName() {
      return "#" + this.post.roll + "Modal";
    },
  },
  methods: {
    async deletePost() {
      axios.defaults.headers.common[
        "Authorization"
      ] = `Bearer ${this.userSession.token}`;

      // Make the POST request with data
      await axios
        .delete("http://192.168.1.8:2345/vueapp/post/" + this.post.roll)
        .catch(() => {
          // Handle the error
          // console.error(error);
        });

      this.$emit("updateData");
    },
  },
};
</script>
