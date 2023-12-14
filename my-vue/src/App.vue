<!--
  <template>
  <img alt="Vue logo" src="./assets/logo.png" />
  <HelloWorld msg="Welcome to Your Vue.js App" />
</template>

<script>
import HelloWorld from "./components/HelloWorld.vue";

export default {
  name: "App",
  components: {
    HelloWorld,
  },
};
</script>


<template>
  <div>
    <h1>Hello, World!</h1>
  </div>
</template>

<template>
  <div>
    <router-link to="/">首页</router-link>
    <router-link to="/about">关于我们</router-link>
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: "App",
};
</script>
-->

<template>
  <transition name="fade" mode="out-in">
    <router-view style="height: 100%; width: 100%"></router-view>
  </transition>
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
