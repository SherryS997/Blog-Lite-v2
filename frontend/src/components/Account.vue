<template>
  <div
    class="modal fade"
    id="importModal"
    tabindex="-1"
    aria-labelledby="importModal"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Import/Export Blogs</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <div class="card-body d-flex flex-column align-items-center">
            <div class="col-md-8 col-xl-6 text-center mx-auto">
              <p class="w-100"><strong>Instruction to Upload Blogs</strong></p>
              <p class="w-100">
                To upload a blog text and its picture, you can follow these
                steps:
              </p>
              <p class="w-100">
                1. Save the blog text and its picture with the title of the blog
                in your computer. For example, “title.txt” and “title.png”.
              </p>
              <p class="w-100">2. Compress all files into a single zip file.</p>
            </div>
            <div class="mb-3 w-75" v-if="this.impSuccess">
              <button class="btn btn-success d-block w-100 disabled">
                Successfully Imported! Please wait for the update.
              </button>
            </div>
            <div class="input-group mb-3 w-75" v-else>
              <input
                type="file"
                class="form-control"
                id="inputGroupFile04"
                aria-describedby="inputGroupFileAddon04"
                aria-label="Upload"
                accept=".zip"
                ref="zip"
                @change="uploadFile('importZip')"
              />
              <button
                :class="!this.zip ? 'disabled' : ''"
                class="btn btn-primary"
                type="button"
                id="inputGroupFileAddon04"
                @click="importBlogs"
              >
                Import Blogs
              </button>
            </div>
            <div class="mb-3 w-75">
              <button
                class="btn btn-success d-block w-100 disabled"
                v-if="this.success"
              >
                Successfully Exported! Check Email.
              </button>
              <button
                class="btn btn-primary d-block w-100"
                type="submit"
                v-else
                v-show="this.compPostLength > 0"
                @click="exportBlog"
              >
                Export Blogs through email
              </button>
            </div>
            <div class="card-text alert alert-danger" v-if="this.error">
              {{ this.msg }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div
    class="modal fade"
    id="apiModal"
    tabindex="-1"
    aria-labelledby="apiModal"
    aria-hidden="true"
  >
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5">API Token</h1>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">{{ this.apiToken }}</div>
      </div>
    </div>
  </div>
  <div
    class="modal fade"
    id="confirmDeleteAccountModal"
    tabindex="-1"
    aria-labelledby="confirmDeleteAccountModal"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5">Delete Account?</h1>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          Deleting the account will not delete your articles.
          <br />
          Their author will be tagged as [deleted].
          <br />
          Are you sure that you want to delete your account? This action cannot
          be undone.
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-danger" @click="deleteAccount">
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
  <div
    class="modal fade"
    id="changePassword"
    tabindex="-1"
    aria-labelledby="changePassword"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Change Password</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <div class="card-body d-flex flex-column align-items-center">
            <div class="col-md-8 col-xl-6 text-center mx-auto">
              <p class="w-lg-50">Please provide the following info</p>
            </div>
            <div class="mb-3">
              <input
                class="form-control"
                type="password"
                name="password"
                placeholder="New Password"
                v-model="password"
              />
            </div>
            <div class="mb-3">
              <input
                class="form-control"
                type="password"
                name="password2"
                placeholder="Re-enter New Password"
                v-model="password2"
              />
            </div>
            <div class="mb-3">
              <button
                class="btn btn-primary d-block w-100"
                type="submit"
                @click="changePass"
              >
                Change Password
              </button>
            </div>
            <div class="card-text alert alert-danger" v-if="this.error">
              {{ this.msg }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div
    class="modal fade"
    id="editAccount"
    tabindex="-1"
    aria-labelledby="editAccount"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Edit Account</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <div class="card mb-5">
            <div class="card-body d-flex flex-column align-items-center">
              <div class="col-md-8 col-xl-6 text-center mx-auto">
                <h2>Edit Account</h2>
                <p class="w-lg-50">Please provide the following info</p>
              </div>
              <div class="text-center">
                <p class="fs-6 card-text">
                  Upload a profile picture below(not required):
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
                    @change="uploadFile('profileImg')"
                    accept="image/gif, image/jpeg, image/jpg, image/png"
                  />
                </div>
                <div class="mb-3">
                  <input
                    class="form-control"
                    type="username"
                    name="username"
                    placeholder="New Username"
                    v-model="this.username"
                  />
                </div>
                <div class="mb-3">
                  <input
                    class="form-control"
                    type="email"
                    name="email"
                    placeholder="New Email"
                    v-model="this.email"
                  />
                </div>
                <div
                  class="text-center form-group"
                  style="padding-bottom: 0px; margin-bottom: 16px"
                  v-show="this.compPostLength > 0"
                >
                  <label
                    style="padding-right: 0.3cm"
                    v-show="this.compPostLength > 0"
                    >Select desired Report format:
                  </label>
                  <div
                    class="form-check form-check-inline"
                    v-show="this.compPostLength > 0"
                  >
                    <input
                      class="form-check-input"
                      type="radio"
                      name="inlineRadioOptions"
                      id="inlineRadio1"
                      value="PDF"
                      v-model="this.format"
                    />
                    <label class="form-check-label" for="inlineRadio1"
                      >PDF</label
                    >
                  </div>
                  <div
                    class="form-check form-check-inline"
                    v-show="this.compPostLength > 0"
                  >
                    <input
                      class="form-check-input"
                      type="radio"
                      name="inlineRadioOptions"
                      id="inlineRadio2"
                      value="HTML"
                      v-model="this.format"
                    />
                    <label class="form-check-label" for="inlineRadio2"
                      >HTML</label
                    >
                  </div>
                </div>
                <div class="mb-3">
                  <button
                    class="btn btn-primary d-block w-100"
                    type="submit"
                    @click="editAccount"
                  >
                    Edit Account
                  </button>
                </div>
                <p v-if="this.error">
                  <span style="color: rgb(255, 0, 0)">{{ this.msg }}</span>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <section class="py-4 py-xl-5">
    <div class="container">
      <div class="bg-dark border rounded border-0 border-dark overflow-hidden">
        <div class="row g-0">
          <div class="col-md-6">
            <div class="text-white p-4 p-md-5">
              <h2 class="fw-bold text-white mb-3">{{ this.compUsername }}</h2>
              <p class="mb-2">Articles written: {{ this.compPostLength }}</p>
              <p class="mb-2">
                <router-link
                  style="color: white"
                  :class="{ 'disabled-link': this.compFollowingLength == 0 }"
                  :to="{ name: 'follows', params: { user: this.compUsername } }"
                  >Following</router-link
                >:
                {{ this.compFollowingLength }}
              </p>
              <p class="mb-2">
                <router-link
                  style="color: white"
                  :to="{
                    name: 'followers',
                    params: { user: this.compUsername },
                  }"
                  :class="{ 'disabled-link': this.compFollowersLength == 0 }"
                  >Followers</router-link
                >:
                {{ this.compFollowersLength }}
              </p>
              <div class="my-3">
                <a
                  class="btn btn-light btn-lg me-2"
                  style="margin-top: 10px"
                  role="button"
                  v-if="this.state"
                  data-bs-toggle="modal"
                  data-bs-target="#editAccount"
                  >Edit Account</a
                >
                <a
                  class="btn btn-primary btn-lg me-2"
                  style="margin-top: 10px"
                  role="button"
                  v-if="this.state"
                  data-bs-toggle="modal"
                  data-bs-target="#confirmDeleteAccountModal"
                  >Delete Account</a
                >
                <button
                  class="btn btn-light btn-lg me-2"
                  style="margin-top: 10px"
                  role="button"
                  v-if="this.state"
                  data-bs-toggle="modal"
                  data-bs-target="#changePassword"
                >
                  Change Password
                </button>
                <button
                  class="btn btn-primary btn-lg me-2"
                  style="margin-top: 10px"
                  role="button"
                  v-if="this.state"
                  data-bs-toggle="modal"
                  data-bs-target="#apiModal"
                >
                  API Token
                </button>
                <router-link
                  class="btn btn-light btn-lg me-2"
                  style="margin-top: 10px"
                  v-if="this.state"
                  :to="{
                    name: 'analytics',
                    params: { user: this.compUsername },
                  }"
                  v-show="this.compPostLength > 0"
                  >Analytics</router-link
                >
                <button
                  class="btn btn-primary btn-lg me-2"
                  style="margin-top: 10px"
                  role="button"
                  v-if="this.state"
                  data-bs-toggle="modal"
                  data-bs-target="#importModal"
                >
                  Import/Export Blogs
                </button>
                <button
                  class="btn btn-danger btn-lg me-2"
                  v-if="!this.state && this.followed && this.userSession"
                  @click="followUpdate"
                >
                  Followed!
                </button>
                <button
                  class="btn btn-primary btn-lg me-2"
                  v-if="!this.state && !this.followed && this.userSession"
                  @click="followUpdate"
                >
                  Follow
                </button>
              </div>
            </div>
          </div>
          <div class="col-md-6 order-first order-md-last">
            <img
              alt="User Image"
              class="card-img-top w-100 d-block"
              style="object-fit: cover; height: 400px"
              :src="this.userImg"
            />
          </div>
        </div>
      </div>
    </div>
  </section>
  <section class="py-4 py-xl-5">
    <div class="container">
      <div
        class="bg-dark border rounded border-0 border-dark overflow-hidden"
        v-if="this.posts"
      >
        <PostSide
          v-for="post in this.posts"
          :key="post"
          :post="post"
          :state="this.state"
          @updateData="this.$emit('updateData')"
        ></PostSide>
      </div>
    </div>
  </section>
</template>

<script>
import PostSide from "@/components/PostSide.vue";
import axios from "axios";

export default {
  components: { PostSide },
  name: "AccountPage",
  data() {
    return {
      userSession: JSON.parse(localStorage.getItem("userSession")) || null,
      username: "",
      password: "",
      password2: "",
      email: "",
      msg: "",
      format: this.user.pdf == 1 ? "PDF" : "HTML",
      error: false,
      allowedTypes: ["image/jpeg", "image/png", "image/gif"],
      allowedImport: ["application/zip"],
      file: null,
      success: false,
      zip: null,
      impSuccess: false,
    };
  },
  props: {
    token: {
      type: Object,
      required: true,
    },
    posts: {
      type: Object,
      required: true,
    },
    user: {
      type: Object,
      required: true,
    },
    followers: {
      type: Object,
      required: true,
    },
    following: {
      type: Object,
      required: true,
    },
    state: {
      type: Boolean,
      required: true,
    },
    followed: {
      type: Boolean,
      required: true,
    },
  },
  computed: {
    apiToken() {
      if (this.userSession) {
        return this.token.token;
      }
      return "";
    },
    compUsername() {
      if (this.user) {
        return this.user.username;
      }
      return "";
    },
    compPostLength() {
      if (this.posts) {
        return this.posts.length;
      }
      return "";
    },
    compFollowersLength() {
      if (this.followers) {
        return this.followers.length;
      }
      return 0;
    },
    compFollowingLength() {
      if (this.following) {
        return this.following.length;
      }
      return 0;
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
  methods: {
    importBlogs() {
      axios.defaults.headers.common[
        "Authorization"
      ] = `Bearer ${this.userSession.token}`;

      let formData = new FormData();

      if (this.zip && this.allowedImport.includes(this.zip.type)) {
        formData.append("Import", this.zip);

        axios
          .post("http://192.168.1.8:2345/vueapp/user/import", formData)
          .catch(() => {
            // console.error("Error:", error);
          });

        this.impSuccess = !this.impSuccess;
      }
    },
    exportBlog() {
      axios.defaults.headers.common[
        "Authorization"
      ] = `Bearer ${this.userSession.token}`;

      // Make the POST request with data
      axios.get("http://192.168.1.8:2345/vueapp/user/export").catch(() => {
        // Handle the error
        // console.error(error);
      });

      this.success = true;
    },
    followUpdate() {
      this.$emit("followUpdate");
    },
    async deleteAccount() {
      axios.defaults.headers.common[
        "Authorization"
      ] = `Bearer ${this.userSession.token}`;

      // Make the POST request with data
      await axios.delete("http://192.168.1.8:2345/vueapp/user").catch(() => {
        // Handle the error
        // console.error(error);
      });

      this.userSession = null;
      localStorage.removeItem("userSession");
      location.href = "/";
    },
    validateContent() {
      if (this.file) {
        return this.allowedTypes.includes(this.file.type);
      } else {
        return false;
      }
    },
    uploadFile(name) {
      if (name == "profileImg") {
        this.file = this.$refs.file.files[0];
      } else if (name == "importZip") {
        this.zip = this.$refs.zip.files[0];
      }
    },
    isEmail(str) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

      return emailRegex.test(str);
    },
    isUsername(str) {
      return str.length > 0;
    },
    isPassword(str) {
      return str.length > 3;
    },
    isMatching(str1, str2) {
      return str1 === str2;
    },
    async editAccount() {
      if (
        this.validateContent() ||
        this.isEmail(this.email) ||
        this.isUsername(this.username) ||
        this.isUsername(this.format)
      ) {
        axios.defaults.headers.common[
          "Authorization"
        ] = `Bearer ${this.userSession.token}`;

        let formData = new FormData();

        if (this.validateContent()) {
          formData.append("New Image", this.file);
        }

        if (this.isEmail(this.email)) {
          formData.append("New Email", this.email);
        }

        if (this.isUsername(this.username)) {
          formData.append("New Username", this.username);
        }

        if (this.isUsername(this.format)) {
          if (this.format == "PDF") {
            formData.append("New Format", 1);
          } else {
            formData.append("New Format", 0);
          }
        }

        await axios
          .put("http://192.168.1.8:2345/vueapp/user", formData)
          .catch((error) => {
            // console.error("Error:", error);
            this.error = true;
            this.msg = error;
          });

        if (this.isUsername(this.username)) {
          location.href = "/account/" + this.username;
        } else {
          location.reload();
        }
      } else {
        this.msg = "Fields not filled properly";
        this.error = true;
      }
    },
    async changePass() {
      if (
        this.isPassword(this.password) &&
        this.isMatching(this.password, this.password2)
      ) {
        axios.defaults.headers.common[
          "Authorization"
        ] = `Bearer ${this.userSession.token}`;

        let formData = new FormData();
        formData.append("New Password", this.password);

        await axios
          .put("http://192.168.1.8:2345/vueapp/user", formData)
          .catch((error) => {
            console.error("Error:", error);
            this.error = true;
            this.msg = error;
          });

        location.reload();
      } else {
        this.msg = "Fields not filled properly";
        this.error = true;
      }
    },
  },
};
</script>

<style>
.disabled-link {
  pointer-events: none;
  color: grey;
  text-decoration: none;
  cursor: default;
}
</style>
