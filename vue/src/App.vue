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
  <div>
    <FullScreenImage />
    <router-link to="/signup"></router-link>
    <router-view></router-view>
  </div>
</template>

<script>
import FullScreenImage from "@/components/DengLu1.vue";

export default {
  name: "App",
  components: {
    FullScreenImage,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
