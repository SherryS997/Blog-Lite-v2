<template>
  <AccountPage
    :token="this.compToken"
    :user="this.compUser"
    :posts="this.compPosts"
    :followers="this.compFollowers"
    :following="this.compFollowing"
    :state="this.curState"
    :followed="this.curFollowed"
    @updateData="updateData"
    @followUpdate="followUpdate"
  ></AccountPage>
</template>

<script>
import AccountPage from "@/components/Account.vue";
import axios from "axios";

export default {
  name: "AccountView",
  components: { AccountPage },
  data() {
    return {
      token: null,
      user: null,
      posts: null,
      followers: null,
      following: null,
      state: false,
      userSession: JSON.parse(localStorage.getItem("userSession")) || null,
      cur: null,
      followed: false,
    };
  },
  methods: {
    async fetchData() {
      await axios
        .get("http://192.168.1.8:2345/vueapp/user/" + this.$route.params.name)
        .then((response) => response)
        .then((result) => {
          this.user = result.data;
        })
        .catch(() => {
          // console.error("Error fetching data:", error);
        });
      axios
        .get("http://192.168.1.8:2345/vueapp/post/" + this.$route.params.name)
        .then((response) => response)
        .then((result) => {
          this.posts = result.data;
        })
        .catch(() => {
          // console.error("Error fetching data:", error);
        });
      axios
        .get(
          "http://192.168.1.8:2345/vueapp/user/" +
            this.$route.params.name +
            "/followers"
        )
        .then((response) => response)
        .then((result) => {
          this.followers = result.data;
        })
        .catch(() => {
          // console.error("Error fetching data:", error);
        });
      axios
        .get(
          "http://192.168.1.8:2345/vueapp/user/" +
            this.$route.params.name +
            "/follows"
        )
        .then((response) => response)
        .then((result) => {
          this.following = result.data;
        })
        .catch(() => {
          // console.error("Error fetching data: Line 71");
        });

      if (this.userSession) {
        axios.defaults.headers.common[
          "Authorization"
        ] = `Bearer ${this.userSession.token}`;
        await axios
          .get("http://192.168.1.8:2345/vueapp/token")
          .then((response) => response)
          .then((response) => response.data)
          .then((result) => {
            this.cur = result;
          })
          .catch(() => {
            // console.error("Error fetching data:", error);
          });

        axios
          .get("http://192.168.1.8:2345/vueapp/usertoken")
          .then((response) => response)
          .then((result) => {
            this.token = result.data;
          })
          .catch(() => {
            // console.error("Error fetching data:", error);
          });

        axios
          .get(
            `http://192.168.1.8:2345/vueapp/${this.cur.username}/follows/${this.compUser.username}`
          )
          .then((response) => response)
          .then((result) => result.data)
          .then((result) => {
            this.followed = result.status == "true";
          })
          .catch(() => {
            // console.error("Error fetching data: Line 108");
          });
      }
      this.$forceUpdate();
    },
    updateData() {
      this.fetchData();
      this.$forceUpdate();
      location.reload();
    },
    followUpdate() {
      if (!this.compFollow) {
        axios.defaults.headers.common[
          "Authorization"
        ] = `Bearer ${this.userSession.token}`;

        // Make the POST request with data
        axios
          .post(
            "http://192.168.1.8:2345/vueapp/user/" +
              this.compUser.username +
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
        axios
          .delete(
            "http://192.168.1.8:2345/vueapp/user/" +
              this.compUser.username +
              "/follows"
          )
          .catch(() => {
            // Handle the error
            // console.error(error);
          });

        this.followed = !this.followed;
      }

      this.fetchData();
    },
  },
  computed: {
    compToken() {
      return this.token;
    },
    compFollow() {
      return this.followed;
    },
    compUser() {
      if (this.user) {
        return this.user;
      }
      return {};
    },
    compPosts() {
      if (this.posts) {
        return this.posts;
      }
      return [];
    },
    compFollowers() {
      if (this.followers) {
        return this.followers;
      }
      return [];
    },
    compFollowing() {
      if (this.following) {
        return this.following;
      }
      return [];
    },
    curState() {
      if (this.userSession && this.user && this.cur) {
        return this.cur.username == this.user.username;
      } else {
        return false;
      }
    },
    curFollowed() {
      return this.followed;
    },
  },
  async beforeMount() {
    this.fetchData();
  },
  mounted() {
    document.title = "User Account";
  },
};
</script>
