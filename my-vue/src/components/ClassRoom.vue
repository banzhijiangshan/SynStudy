<template>
  <div>
    <el-main class="el-main">
      <el-image
        :src="require('@/assets/class.png')"
        style="margin: 0; position: absolute; height: 100%; width: 100%"
      ></el-image>
    </el-main>
    <el-button type="primary" class="enter-button" @click="study"> </el-button>
    <el-button type="primary" class="back-button" @click="exit"> </el-button>
  </div>
</template>

<script>
export default {
  components: {},
  methods: {
    study() {
      this.$router.push("/study");
    },
    exit() {
      this.$router.push("/floor");
    },
  },
};
</script>

<style scoped>
.el-main {
  height: 100%;
  width: 100%;
  margin: 0;
  padding: 0;
}

.enter-button {
  position: absolute;
  top: 40.5%;
  left: 58%;
  width: 155px;
  height: 64px;
  transform: translate(-50%, -50%);
  background-color: transparent;
  border: 3px solid transparent;
  transition: border 0.3s;
}
.enter-button:hover {
  background-color: transparent;
  border-color: white;
}

.back-button {
  position: absolute;
  top: 6.5%;
  left: 82%;
  width: 3.5%;
  height: 6%;
  background-color: transparent;
  transform: translate(-50%, -50%);

  border: none;
}
.back-button:hover {
  background-color: transparent;
}
</style>
