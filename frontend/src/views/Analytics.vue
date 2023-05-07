<template>
  <div class="container py-4 py-xl-5">
    <div class="row gy-4 row-cols-1 row-cols-md-2 row-cols-xl-3">
      <div class="col-md-12 col-xl-12">
        <div>
          <div class="py-4 d-flex">
            <div>
              <h4>{{ this.user }}'s Analytics</h4>
              <p>
                The chart below shows the views received by evey post
                {{ this.user }}.
              </p>
            </div>
            <div class="row">
              <div
                class="btn-group"
                role="group"
                style="
                  padding-top: 15px;
                  padding-left: 30px;
                  padding-bottom: 15px;
                "
              >
                <button
                  class="text-center btn btn-success btn-lg me-2 disabled"
                  type="submit"
                  v-if="this.success"
                >
                  Successfully Exported!
                </button>
                <button
                  class="text-center btn btn-primary btn-lg me-2"
                  type="submit"
                  v-else
                  @click="export_data"
                >
                  Email Data as CSV
                </button>
              </div>
            </div>
          </div>
          <img
            alt="Analytics Image"
            class="rounded img-fluid d-block w-100 border border-dark rounded"
            style="height: 100%; object-fit: cover"
            :src="compViewsImg"
          />
          <div class="py-4 d-flex">
            <div>
              <p>
                The charts shows the likes received by evey post from
                {{ this.user }}.
              </p>
            </div>
          </div>
          <img
            alt="Analytics Image"
            class="rounded img-fluid d-block w-100 border border-dark rounded"
            style="height: 100%; object-fit: cover"
            :src="compLikesImg"
          />
          <div class="py-4 d-flex">
            <div>
              <p>
                The charts shows the number of comments received by evey post
                from {{ this.user }}.
              </p>
            </div>
          </div>
          <img
            alt="Analytics Image"
            class="rounded img-fluid d-block w-100 border border-dark rounded"
            style="height: 100%; object-fit: cover"
            :src="compCommentsImg"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "AnalyticsView",
  data() {
    return {
      user: this.$route.params.user,
      userSession: JSON.parse(localStorage.getItem("userSession")) || null,
      success: false,
    };
  },
  methods: {
    async fetchData() {
      if (this.userSession) {
        axios.defaults.headers.common[
          "Authorization"
        ] = `Bearer ${this.userSession.token}`;

        await axios
          .get("http://192.168.1.8:2345/vueapp/analytics")
          .catch(() => {
            // console.log(error);
          });
      }
      this.success = false;
      this.$forceUpdate();
    },
    export_data() {
      if (this.userSession) {
        axios.defaults.headers.common[
          "Authorization"
        ] = `Bearer ${this.userSession.token}`;

        axios
          .get("http://192.168.1.8:2345/vueapp/analytics/export_data")
          .catch(() => {
            // console.log(error);
          });

        this.success = true;
      }
    },
  },
  computed: {
    apiToken() {
      if (this.userSession) {
        return this.userSession.token;
      }
      return "";
    },
    compViewsImg() {
      return (
        "http://192.168.1.8:2345/static/img/Analytics/" +
        this.user +
        "/Views.png"
      );
    },
    compLikesImg() {
      return (
        "http://192.168.1.8:2345/static/img/Analytics/" +
        this.user +
        "/Likes.png"
      );
    },
    compCommentsImg() {
      return (
        "http://192.168.1.8:2345/static/img/Analytics/" +
        this.user +
        "/Comments.png"
      );
    },
  },
  async beforeMount() {
    this.fetchData();
  },
  mounted() {
    document.title = "Analytics";
  },
};
</script>
