<template>
  <section class="position-relative py-4 py-xl-5">
    <div class="container">
      <div class="row mb-5">
        <div class="col-md-8 col-xl-6 text-center mx-auto">
          <h2 v-if="register">Sign up</h2>
          <h2 v-else>Log in</h2>
          <p class="w-lg-50">Please provide the following info</p>
        </div>
      </div>
      <div class="row d-flex justify-content-center">
        <div class="col-md-6 col-xl-4">
          <div class="card mb-5">
            <div class="card-body d-flex flex-column align-items-center">
              <div class="my-4">
                <img
                  alt="User Image"
                  class="rounded-circle flex-shrink-0 me-3"
                  style="object-fit: cover"
                  width="100"
                  height="100"
                  src="http://192.168.1.8:2345/static/img/Users/0.webp"
                />
              </div>
              <div class="text-center">
                <div class="mb-3">
                  <input
                    class="form-control"
                    type="username"
                    name="username"
                    placeholder="Username"
                    v-model="username"
                    required
                  />
                </div>
                <div class="mb-3" v-if="register">
                  <input
                    class="form-control"
                    type="email"
                    name="email"
                    placeholder="Email"
                    v-model="email"
                    required
                    minlength="5"
                  />
                </div>
                <div class="mb-3">
                  <input
                    class="form-control"
                    type="password"
                    name="password"
                    placeholder="Password"
                    v-model="password"
                    required
                    minlength="4"
                  />
                </div>
                <div class="mb-3" v-if="register">
                  <input
                    class="form-control"
                    type="password"
                    name="password2"
                    placeholder="Re-enter Password"
                    v-model="password2"
                    required
                    minlength="4"
                  />
                </div>
                <div class="mb-3">
                  <button
                    class="btn btn-primary d-block w-100"
                    @click="registerOn"
                    v-if="register"
                    :aria-disabled="!isEmail(this.email)"
                  >
                    Register
                  </button>
                  <button
                    class="btn btn-primary d-block w-100"
                    type="submit"
                    @click="login"
                    v-else
                  >
                    Login
                  </button>
                </div>
                <p class="text-muted" v-if="register">
                  Have an account? <a @click="state" href="#">Log in</a>
                </p>
                <p class="text-muted" v-else>
                  Not a member? <a @click="state" href="#">Register</a>
                </p>
              </div>
              <div class="card-text alert alert-danger" v-if="this.error">
                {{ this.msg }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import axios from "axios";

export default {
  name: "LoginView",
  data() {
    return {
      userSession: JSON.parse(localStorage.getItem("userSession")) || null,
      register: false,
      username: "",
      password: "",
      password2: "",
      email: "",
      token: "",
      exp: "",
      msg: "",
      error: false,
    };
  },
  methods: {
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
    click() {
      location.href = "/";
    },
    state() {
      this.error = false;
      this.register = !this.register;
    },
    async registerOn() {
      if (
        this.isEmail(this.email) &&
        this.isUsername(this.username) &&
        this.isPassword(this.password) &&
        this.isMatching(this.password, this.password2)
      ) {
        await axios
          .post("http://192.168.1.8:2345/vueapp/user", {
            Username: this.username,
            Password: this.password,
            Email: this.email,
          })
          .then((response) => response["data"])
          .then((response) => {
            if ("error" in response) {
              throw new Error(response.error_msg);
            } else {
              this.error = false;
              return response;
            }
          })
          .then(
            (response) => (
              (this.token = response.token), (this.exp = response.exp)
            )
          )
          .catch((error) => {
            // console.error("Error:", error);
            this.error = true;
            this.msg = error;
          });
        if (!this.error) {
          this.userSession = {
            token: this.token,
            exp: this.exp,
          };
          localStorage.setItem("userSession", JSON.stringify(this.userSession));
          this.click();
        }
      } else {
        this.msg = "Fields not filled properly";
        this.error = true;
      }
    },
    async login() {
      if (this.isUsername(this.username) && this.isPassword(this.password)) {
        await axios
          .post("http://192.168.1.8:2345/vueapp/login", {
            username: this.username,
            password: this.password,
          })
          .then((response) => response["data"])
          .then((response) => {
            if ("error" in response) {
              throw new Error(response.error_msg);
            } else {
              this.error = false;
              return response;
            }
          })
          .then(
            (response) => (
              (this.token = response.token), (this.exp = response.exp)
            )
          )
          .catch((error) => {
            // console.error("Error:", error);
            this.error = true;
            this.msg = error;
          });
        if (!this.error) {
          this.userSession = {
            token: this.token,
            exp: this.exp,
          };
          localStorage.setItem("userSession", JSON.stringify(this.userSession));
          this.click();
        }
      } else {
        this.msg = "Fields not filled properly";
        this.error = true;
      }
    },
  },
  mounted() {
    document.title = this.register ? "Register" : "Login";
  },
};
</script>
