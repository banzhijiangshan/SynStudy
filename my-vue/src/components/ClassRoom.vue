<template>
  <div>
    <el-main class="el-main">
      <el-image
        :src="require('@/assets/class.png')"
        style="margin: 0; position: absolute; height: 100%; width: 100%"
      ></el-image>
      <PersonalDia ref="infoRef1"></PersonalDia>
      <InfoDia ref="infoRef2"></InfoDia>
    </el-main>
    <el-button type="primary" class="enter-button" @click="study"> </el-button>
    <el-button type="primary" class="back-button" @click="exit"> </el-button>
    <div class="left-top">
      <el-button
        type="primary"
        circle
        class="button-class"
        @click="showPersonalDialog"
      >
        <el-icon style="vertical-align: middle">
          <User />
        </el-icon>
      </el-button>

      <el-button
        type="primary"
        circle
        class="button-class"
        @click="showInfoDia"
      >
        <el-icon style="vertical-align: middle">
          <MoreFilled />
        </el-icon>
      </el-button>
    </div>
  </div>
</template>

<script>
import PersonalDia from "./UserInfo.vue";
import InfoDia from "./MoreInfo.vue";

export default {
  components: { PersonalDia, InfoDia },
  methods: {
    study() {
      this.$router.push("/study");
    },
    exit() {
      this.$router.push("/floor");
    },
    showPersonalDialog() {
      this.$refs.infoRef1.open();
    },
    showInfoDia() {
      this.$refs.infoRef2.open();
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
.button-class {
  display: inline-block;
  min-width: 50px;
  height: 50px;
  font-size: 24px;
}

.left-top {
  position: absolute;
  top: 20px;
  left: 30px;
}
</style>
