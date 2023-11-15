<template>
  <div>
    <el-main class="el-main">
      <PersonalDia ref="infoRef"></PersonalDia>
      <InfoDia ref="infoRef1"></InfoDia>
      <el-image
        :src="require('@/assets/f2.png')"
        style="margin: 0; position: absolute; height: 100%; width: 100%"
      ></el-image>
    </el-main>
    <el-row class="button-container">
      <!-- 左上角的按钮组 -->
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
    </el-row>
    <el-button type="primary" class="enter-button" @click="goin"> </el-button>
    <el-button type="primary" class="enter-button1" @click="goin"> </el-button>
    <el-button type="primary" class="enter-button2" @click="goin"> </el-button>
    <el-button type="primary" class="down-button" @click="down"> </el-button>
  </div>
</template>

<script>
import PersonalDia from "./UserInfo.vue";
import InfoDia from "./MoreInfo.vue";
export default {
  components: {
    PersonalDia,
    InfoDia,
  },
  methods: {
    showPersonalDialog() {
      this.$refs.infoRef.open();
    },
    goback() {
      this.$router.push("/building");
    },
    showInfoDia() {
      this.$refs.infoRef1.open();
    },
    goin() {
      this.$router.push("/classroom");
    },
    down() {
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

.el-row {
  margin-top: 20px;
  margin-left: 30px;
}

.button-container {
  position: relative;
}

.left-top {
  position: absolute;
  top: 0;
  left: 0;
}

.button-class {
  display: inline-block;
  min-width: 50px;
  height: 50px;
  font-size: 24px;
}

.button-class1 {
  display: inline-block;
  min-width: 50px;
  height: 50px;
  font-size: 24px;
}

.el-dialog {
  z-index: 1000; /* Adjust the value as needed */
}

.enter-button {
  position: absolute;
  top: 27%;
  left: 54.5%;
  width: 155px;
  height: 56px;
  transform: translate(-50%, -50%);
  background-color: transparent;
  border: none;
}
.enter-button:hover {
  background-color: transparent;
}

.enter-button1 {
  position: absolute;
  top: 41%;
  left: 35.5%;
  width: 115px;
  height: 48px;
  transform: translate(-50%, -50%);
  background-color: transparent;
  border: none;
}
.enter-button1:hover {
  background-color: transparent;
}

.enter-button2 {
  position: absolute;
  top: 46%;
  left: 27%;
  width: 84px;
  height: 38px;
  transform: translate(-50%, -50%);
  background-color: transparent;
  border: none;
}
.enter-button2:hover {
  background-color: transparent;
}
.down-button {
  position: absolute;
  top: 82%;
  right: 4.3%;
  width: 86px;
  height: 90px;
  background-color: transparent;
  border: none;
}
.down-button:hover {
  background-color: transparent;
}
</style>
