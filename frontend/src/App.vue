<template>
  <nav class="navbar navbar-dark navbar-expand-md sticky-top bg-dark py-3">
    <div class="container">
      <a class="navbar-brand d-flex align-items-center" href="#"
        ><router-link to="/" class="home">
          <span>Blog Lite</span>
        </router-link></a
      >
      <button
        class="navbar-toggler"
        data-bs-toggle="collapse"
        data-bs-target="#navcol-5"
        v-if="
          isOnline &&
          $route.name != 'notfound' &&
          $route.name != 'analytics' &&
          $route.name != 'follows' &&
          $route.name != 'followers' &&
          $route.name != 'search' &&
          $route.name != 'blogEdit' &&
          $route.name != 'upload' &&
          $route.name != 'login' &&
          $route.name != 'post' &&
          $route.name != 'account'
        "
      >
        <span class="visually-hidden">Toggle navigation</span
        ><span class="navbar-toggler-icon"></span>
      </button>
      <div
        id="navcol-5"
        class="collapse navbar-collapse"
        v-if="
          isOnline &&
          $route.name != 'search' &&
          $route.name != 'notfound' &&
          $route.name != 'analytics' &&
          $route.name != 'follows' &&
          $route.name != 'followers' &&
          $route.name != 'blogEdit' &&
          $route.name != 'upload' &&
          $route.name != 'login' &&
          $route.name != 'post' &&
          $route.name != 'account'
        "
      >
        <span class="navbar-text" v-if="userSes"
          >Welcome {{ this.compUsername }}</span
        >
        <ul class="navbar-nav ms-auto" v-if="userSession">
          <li class="nav-item">
            <a
              class="nav-link active"
              v-if="!this.compDiscover"
              href="#"
              @click="undiscover()"
            >
              Discover
            </a>
            <a class="nav-link active" v-else href="#" @click="undiscover()">
              Home
            </a>
          </li>
          <li class="nav-item">
            <router-link class="nav-link active" to="/upload"
              >Upload</router-link
            >
          </li>
          <li class="nav-item">
            <router-link class="nav-link active" @click="logout" to="/"
              >Log out</router-link
            >
          </li>
          <li class="nav-item">
            <input
              class="border rounded border border-dark"
              style="
                margin-top: 7px;
                margin-left: 0px;
                margin-right: 15px;
                margin-bottom: 7px;
              "
              type="search"
              name="search"
              placeholder="Search"
              @keyup.enter="handleKeyPress"
              v-model="this.search"
              required
            />
          </li>
        </ul>
        <ul class="navbar-nav ms-auto" v-else></ul>
        <span
          class="navbar-text"
          style="
            margin-right: -18px;
            padding-right: 0px;
            margin-bottom: -8px;
            margin-top: -8px;
          "
        >
          <img
            alt="User Image"
            class="rounded-circle flex-shrink-0 me-3"
            style="object-fit: cover"
            width="36"
            height="36"
            :src="userImg"
            v-if="userSession"
          />
        </span>
        <div class="ms-md-2">
          <router-link
            class="btn btn-primary ms-md-2"
            to="/login"
            v-if="userSes == null"
            >Login
          </router-link>
          <router-link
            class="btn btn-primary ms-md-2"
            :to="this.account"
            v-else-if="userSes"
            >My Account
          </router-link>
        </div>
      </div>
      <div v-else>
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <button class="btn btn-secondary" v-if="isOnline" @click="goBack">
              &lt; Back
            </button>
          </li>
        </ul>
      </div>
    </div>
  </nav>
  <router-view :discover="this.compDiscover" v-if="isOnline" />
  <NoInternet v-else></NoInternet>
</template>

<script>
import axios from "axios";
import NoInternet from "./views/NoInternet.vue";

export default {
  components: {
    NoInternet,
  },
  data() {
    return {
      serverStatus: false,
      search: "",
      userSession: JSON.parse(localStorage.getItem("userSession")) || null,
      discover: false,
      user: null,
    };
  },
  methods: {
    logout() {
      this.userSession = null;
      localStorage.removeItem("userSession");
      location.reload();
    },
    handleKeyPress() {
      this.$router.push({ name: "search", params: { term: this.search } });
      this.search = "";
    },
    async fetchData() {
      if (this.userSes) {
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
      fetch("http://192.168.1.8:2345/")
        .then((response) => {
          if (response.ok) {
            this.serverStatus = true;
          } else {
            this.serverStatus = false;
          }
        })
        .catch(() => {
          this.serverStatus = false;
        });
      this.$forceUpdate();
    },
    undiscover() {
      this.discover = !this.discover;
    },
    goBack() {
      this.$router.go(-1);
    },
  },
  computed: {
    isOnline() {
      return this.serverStatus;
    },
    compDiscover() {
      return this.discover;
    },
    userSes() {
      return this.userSession;
    },
    account() {
      if (this.user) {
        return "/account/" + this.compUsername;
      } else {
        return "";
      }
    },
    userImg() {
      if (this.user) {
        return (
          "http://192.168.1.8:2345/static/img/Users/" + this.user.img + ".webp"
        );
      } else {
        return require("@/assets/0.webp");
      }
    },
    compUsername() {
      if (this.user) {
        return this.user.username;
      }
      return "";
    },
  },
  async beforeMount() {
    this.fetchData();

    if (this.userSession) {
      const expiry = Date.parse(this.userSession.exp);
      if (expiry < Date.now()) {
        this.logout();
      }
    }
  },
  mounted() {
    setInterval(() => {
      fetch("http://192.168.1.8:2345/")
        .then((response) => {
          if (response.ok) {
            this.serverStatus = true;
          } else {
            this.serverStatus = false;
          }
        })
        .catch(() => {
          this.serverStatus = false;
        });
    }, 5000);
  },
};
</script>

<style>
.home {
  color: inherit;
  text-decoration: none;
  font-weight: normal;
}
</style>
