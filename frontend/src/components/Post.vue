<template>
  <div class="container py-4 py-xl-5">
    <div class="col-md-12 col-xl-12 card">
      <img
        alt="Post Image"
        class="card-img-top w-100 d-block"
        style="object-fit: cover; height: 400px"
        :src="this.postImg"
      />
      <div class="card-body p-4">
        <p class="text-primary card-text mb-0">Article</p>
        <h1 class="display-3 card-title">{{ this.post.title }}</h1>
        <div style="padding-bottom: 0px; margin-bottom: 15px"></div>
        <div class="d-flex">
          <img
            alt="User Image"
            class="rounded-circle flex-shrink-0 me-3"
            width="50"
            height="50"
            style="object-fit: cover"
            :src="this.userImg"
          />
          <div>
            <p class="fw-bold mb-0">{{ post.author }}</p>
            <p class="text-muted mb-0">{{ post.date }}</p>
          </div>
        </div>
        <div>
          <div style="padding-bottom: 0px; margin-bottom: 15px"></div>
          <p
            class="fs-5 card-text"
            v-for="line in post.text.split('\n')"
            :key="line"
          >
            {{ line }}
          </p>
        </div>
      </div>
    </div>
    <div>
      <section class="position-relative py-4 py-xl-5">
        <div class="container position-relative">
          <div class="card mb-5">
            <div class="card-body p-sm-5" style="padding-right: 11px">
              <div>
                <div>
                  <h2><u>Comment Section:</u></h2>
                </div>
                <div v-for="comment in this.comments" :key="comment">
                  <p class="fs-5 card-text">
                    <strong>{{ comment.author }}:</strong> {{ comment.comment }}
                  </p>
                </div>
              </div>
              <br />
              <div v-if="this.userSession">
                <div class="mb-3">
                  <textarea
                    class="form-control"
                    placeholder="Comment here"
                    v-model="this.com"
                  ></textarea>
                </div>
                <div>
                  <button
                    class="btn btn-primary d-block w-100"
                    type="submit"
                    :disabled="this.isDisabled"
                    @click="comment"
                  >
                    Upload Comment
                  </button>
                </div>
              </div>
              <p class="fs-5 card-text" v-else>
                <router-link to="/login" v-if="userSes == null"
                  >Login
                </router-link>
                to comment!
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "postComp",
  props: {
    post: {
      type: Object,
      required: true,
    },
    user: {
      type: Object,
      required: true,
    },
    comments: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      userSession: JSON.parse(localStorage.getItem("userSession")) || null,
      com: null,
    };
  },
  methods: {
    comment() {
      if (this.userSession) {
        axios.defaults.headers.common[
          "Authorization"
        ] = `Bearer ${this.userSession.token}`;

        axios
          .post(
            "http://192.168.1.8:2345/vueapp/post/" +
              this.$route.params.id +
              "/comment",
            {
              Comment: this.com,
            }
          )
          .catch(() => {
            // Handle the error
            // console.error(error);
          });

        this.com = null;
        this.$emit("updateComments");
      }
    },
  },
  computed: {
    isDisabled() {
      if (this.com) {
        return this.com.length == 0;
      }

      return true;
    },
    compCom() {
      return this.comments;
    },
    userImg() {
      if (this.user) {
        return (
          "http://192.168.1.8:2345/static/img/Users/" + this.user.img + ".webp"
        );
      }
      return require("@/assets/0.webp");
    },
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
