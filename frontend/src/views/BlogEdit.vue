<template>
  <div class="container">
    <div>
      <section class="position-relative py-4 py-xl-5">
        <div class="container position-relative">
          <div class="row d-flex justify-content-center">
            <div class="col-md-12 col-lg-10 col-xl-10 col-xxl-10">
              <div class="card mb-5">
                <div class="card-body p-sm-5" style="padding-right: 11px">
                  <div class="mb-3">
                    <h2 class="text-centre mb-4">Edit Article</h2>
                  </div>
                  <p class="fs-6 card-text">
                    Upload an image below(not required):
                  </p>
                  <div
                    class="text-center"
                    style="padding-bottom: 0px; margin-bottom: 16px"
                  >
                    <input
                      class="form-control"
                      type="file"
                      ref="file"
                      placeholder="Upload Image"
                      @change="uploadFile"
                      required
                      accept="image/gif, image/jpeg, image/jpg, image/png"
                    />
                  </div>
                  <div class="mb-3">
                    <input
                      class="form-control"
                      type="text"
                      v-model="title"
                      placeholder="Title"
                      required
                    />
                  </div>
                  <div class="mb-3">
                    <textarea
                      class="form-control"
                      v-model="content"
                      rows="3"
                      placeholder="Content"
                      required
                    ></textarea>
                  </div>
                  <div>
                    <button
                      class="btn btn-primary d-block w-100"
                      type="submit"
                      @click="upload"
                      :disabled="!isValid"
                    >
                      Update Article
                    </button>
                  </div>
                  <br />
                  <div>
                    <p class="card-text alert alert-primary">
                      Certain changes maybe visible only after a reload of the
                      app!
                    </p>
                  </div>
                </div>
              </div>
            </div>
            <div
              v-show="this.isValid"
              class="col-md-12 col-lg-10 col-xl-10 col-xxl-10"
            >
              <div class="card mb-5">
                <div class="card-body p-sm-5" style="padding-right: 11px">
                  <div class="mb-3">
                    <h2 class="text-centre mb-4">Live Post Preview</h2>
                  </div>
                  <img
                    alt="Post Image"
                    class="card-img-top w-100 d-block"
                    style="object-fit: cover; height: 400px"
                    :src="this.imageUrl"
                    v-if="this.isValid"
                  />
                  <div class="card-body p-4">
                    <p class="text-primary card-text mb-0">Article</p>
                    <h1 class="display-3 card-title" v-if="this.compTitle">
                      {{ this.compTitle }}
                    </h1>
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
                        <p class="fw-bold mb-0">{{ this.userName }}</p>
                        <p class="text-muted mb-0">{{ this.compDate }}</p>
                      </div>
                    </div>
                    <div>
                      <div
                        style="padding-bottom: 0px; margin-bottom: 15px"
                      ></div>
                      <div v-if="this.compContent">
                        <p
                          class="fs-5 card-text"
                          v-for="line in this.compContent.split('\n')"
                          :key="line"
                        >
                          {{ line }}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
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
  name: "BlogEdit",
  data() {
    return {
      userSession: JSON.parse(localStorage.getItem("userSession")) || null,
      user: null,
      file: null,
      title: null,
      content: null,
      error: null,
      allowedTypes: ["image/jpeg", "image/png", "image/gif"],
      imageUrl: null,
      date: new Date(),
    };
  },
  methods: {
    async fetchData() {
      if (this.userSes) {
        await axios
          .get("http://192.168.1.8:2345/vueapp/post/" + this.$route.params.id)
          .then((response) => response)
          .then((result) => result.data)
          .then((result) => {
            this.title = result.post.title;
            this.content = result.post.text;
            this.imageUrl =
              "http://192.168.1.8:2345/static/img/Posts/" +
              result.post.img +
              ".webp";
          })
          .catch(() => {
            // console.error("Error fetching data:", error);
          });
        axios.defaults.headers.common[
          "Authorization"
        ] = `Bearer ${this.userSession.token}`;
        axios
          .get("http://192.168.1.8:2345/vueapp/token")
          .then((response) => response)
          .then((result) => {
            this.user = result.data;
          })
          .catch(() => {
            // console.error("Error fetching data:", error);
          });
      }
      this.$forceUpdate();
    },
    validateContent() {
      if (this.file && this.title && this.content) {
        return (
          this.allowedTypes.includes(this.file.type) &&
          this.title.length > 0 &&
          this.content.length > 0
        );
      } else if (this.imageUrl && this.title && this.content) {
        return (
          this.imageUrl && this.title.length > 0 && this.content.length > 0
        );
      } else {
        return false;
      }
    },
    uploadFile() {
      this.file = this.$refs.file.files[0];
      const reader = new FileReader();

      reader.onload = (event) => {
        this.imageUrl = event.target.result;
      };

      reader.readAsDataURL(this.file);
    },
    async upload() {
      if (this.userSession && this.isValid) {
        axios.defaults.headers.common[
          "Authorization"
        ] = `Bearer ${this.userSession.token}`;

        let formData = new FormData();
        formData.append("file", this.file);
        formData.append("title", this.compTitle);
        formData.append("content", this.compContent);

        await axios
          .put(
            "http://192.168.1.8:2345/vueapp/post/" + this.$route.params.id,
            formData,
            {
              headers: {
                "Content-Type": "multipart/form-data",
              },
            }
          )
          .catch(() => {
            // console.log(error);
          });

        location.href = "/account/" + this.userName;
      }
    },
  },
  computed: {
    userSes() {
      return this.userSession;
    },
    isValid() {
      return this.validateContent();
    },
    compFile() {
      if (this.file) {
        if (this.allowedTypes.includes(this.file.type)) {
          return this.file;
        }
        return null;
      }
      return null;
    },
    compDate() {
      return this.date.toISOString().slice(0, 10);
    },
    compTitle() {
      return this.title;
    },
    compContent() {
      return this.content;
    },
    userImg() {
      if (this.userSes) {
        return (
          "http://192.168.1.8:2345/static/img/Users/" + this.user.img + ".webp"
        );
      } else {
        return require("@/assets/0.webp");
      }
    },
    userName() {
      if (this.userSes) {
        return this.user.username;
      } else {
        return "";
      }
    },
  },
  async beforeMount() {
    this.fetchData();
  },
  mounted() {
    document.title = "Edit Blog";
  },
};
</script>
