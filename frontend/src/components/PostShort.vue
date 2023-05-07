<template>
  <div class="card">
    <img
      alt="Post Image"
      class="card-img-top w-100 d-block"
      style="object-fit: cover; height: 200px"
      :src="this.postImg"
    />
    <div class="card-body p-4">
      <p class="text-primary card-text mb-0">Article</p>
      <h4 class="card-title">{{ post.title }}</h4>
      <p class="card-text" style="margin-bottom: 0px">
        {{ post.text.slice(0, 120) + "..." }}
      </p>
      <span>
        <router-link :to="{ name: 'post', params: { id: post.roll } }"
          >Read More</router-link
        >
      </span>
      <div class="d-flex" style="margin-top: 10px">
        <img
          alt="User Image"
          class="rounded-circle flex-shrink-0 me-3"
          style="object-fit: cover"
          width="50"
          height="50"
          :src="this.userImg"
        />
        <div>
          <router-link :to="accountUrl" :class="{ disabled: isLinkDisabled }"
            ><p class="fw-bold mb-0">{{ post.author }}</p></router-link
          >
          <p class="text-muted mb-0">{{ post.date }}</p>
        </div>
        <div class="row">
          <div
            class="btn-group"
            role="group"
            style="margin-bottom: 5px; margin-top: 5px; padding-left: 15px"
            v-if="!this.isLinkDisabled"
          >
            <button
              type="button"
              class="btn btn-danger"
              :disabled="!(this.userSession && this.username != post.author)"
              @click="like"
              v-if="this.compLike"
            >
              <i class="bi bi-heart-fill"></i>
              {{ post.likes }}
            </button>
            <button
              type="button"
              class="btn btn-primary"
              :disabled="!(this.userSession && this.username != post.author)"
              @click="like"
              v-else
            >
              <i class="bi bi-heart-fill"></i>
              {{ post.likes }}
            </button>
            <button
              class="btn btn-danger"
              style="margin-left: 5px"
              @click="follow"
              v-if="this.compFollowed"
            >
              Followed!
            </button>
            <button
              class="btn btn-primary"
              style="margin-left: 5px"
              @click="follow"
              v-else-if="this.compUnfollowed"
            >
              Follow
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "postShort",
  data() {
    return {
      userSession: JSON.parse(localStorage.getItem("userSession")) || null,
      followed: false,
      liked: false,
    };
  },
  props: {
    post: {
      type: Object,
      required: true,
    },
    user: {
      type: Object,
      required: true,
    },
    cur: {
      type: Object,
      required: true,
    },
  },
  methods: {
    async like() {
      if (this.userSession) {
        if (!this.compLike) {
          axios.defaults.headers.common[
            "Authorization"
          ] = `Bearer ${this.userSession.token}`;

          // Make the POST request with data
          await axios
            .post("http://192.168.1.8:2345/vueapp/like/" + this.post.roll)
            .catch(() => {
              // Handle the error
              // console.error(error);
            });

          this.liked = !this.liked;
        } else {
          axios.defaults.headers.common[
            "Authorization"
          ] = `Bearer ${this.userSession.token}`;

          // Make the POST request with data
          await axios
            .delete("http://192.168.1.8:2345/vueapp/like/" + this.post.roll)
            .catch(() => {
              // Handle the error
              // console.error(error);
            });

          this.liked = !this.liked;
        }

        this.$emit("updateData");
      }
    },
    async follow() {
      if (!this.compFollow) {
        axios.defaults.headers.common[
          "Authorization"
        ] = `Bearer ${this.userSession.token}`;

        // Make the POST request with data
        await axios
          .post(
            "http://192.168.1.8:2345/vueapp/user/" +
              this.post.author +
              "/follows"
          )
          .catch(() => {
            // Handle the error
            // console.error(error);
          });

        this.followed = !this.followed;
      } else {
        axios.defaults.headers.common[
          "Authorization"
        ] = `Bearer ${this.userSession.token}`;

        // Make the POST request with data
        await axios
          .delete(
            "http://192.168.1.8:2345/vueapp/user/" +
              this.post.author +
              "/follows"
          )
          .catch(() => {
            // Handle the error
            // console.error(error);
          });

        this.followed = !this.followed;
      }

      this.$emit("updateData");
    },
    async fetchData() {
      if (this.userSession) {
        await axios
          .get(
            `http://192.168.1.8:2345/vueapp/${this.username}/follows/${this.user.username}`
          )
          .then((response) => response)
          .then((result) => result.data)
          .then((result) => {
            this.followed = result.status == "true";
          })
          .catch(() => {
            // console.error("Error fetching data: Line 200");
          });

        await axios
          .get(
            "http://192.168.1.8:2345/vueapp/likes/" +
              this.username +
              "/" +
              this.post.roll
          )
          .then((response) => response)
          .then((result) => result.data)
          .then((response) => {
            this.liked = response.status == "true";
          })
          .catch(() => {
            // Handle the error
            // console.error(error);
          });
      }
      this.$forceUpdate();
    },
  },
  async beforeMount() {
    this.fetchData();
  },
  computed: {
    compFollow() {
      return this.followed;
    },
    compFollowed() {
      return (
        this.followed && this.userSession && this.username != this.post.author
      );
    },
    compUnfollowed() {
      return (
        !this.followed && this.userSession && this.username != this.post.author
      );
    },
    compLike() {
      return this.liked;
    },
    username() {
      if (this.userSession) {
        return this.cur.username;
      } else {
        return "";
      }
    },
    accountUrl() {
      return "/account/" + this.post.author;
    },
    isLinkDisabled() {
      return this.post.author === "[deleted]";
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

<style>
.disabled {
  pointer-events: none;
  opacity: 0.6;
  text-decoration: none;
  cursor: default;
}
</style>
