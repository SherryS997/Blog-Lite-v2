import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/Home.vue";
import LoginView from "../views/Login.vue";
import PostView from "../views/Post.vue";
import AccountView from "../views/Account.vue";
import UploadView from "../views/Upload.vue";
import BlogEdit from "../views/BlogEdit.vue";
import SearchView from "../views/Search.vue";
import FollowView from "../views/Follows.vue";
import AnalyticsView from "../views/Analytics.vue";
import NotFoundView from "../views/NotFound.vue";

function isAuthenticated() {
  const user = localStorage.getItem("userSession");
  return user !== null;
}

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/account/:user/follows",
    name: "follows",
    component: FollowView,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/account/:user/analytics",
    name: "analytics",
    component: AnalyticsView,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/account/:user/followers",
    name: "followers",
    component: FollowView,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/search=:term",
    name: "search",
    component: SearchView,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/login",
    name: "login",
    component: LoginView,
  },
  {
    path: "/post/:id",
    name: "post",
    component: PostView,
  },
  {
    path: "/edit/post/:id",
    name: "blogEdit",
    component: BlogEdit,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/account/:name",
    name: "account",
    component: AccountView,
  },
  {
    path: "/upload",
    name: "upload",
    component: UploadView,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/:pathMatch(.*)*",
    name: "notfound",
    component: NotFoundView,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !isAuthenticated()) {
    next({ name: "login" });
  } else {
    next();
  }
});

export default router;
