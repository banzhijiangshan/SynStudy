<template>
  <div>
    <el-main class="el-main">
      <PersonalDia ref="infoRef"></PersonalDia>
      <InfoDia ref="infoRef1"></InfoDia>
      <el-image
        :src="require('@/assets/floorday.png')"
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

      <div class="right-bottom">
        <el-button type="info" class="button-class1" @click="goback">
          <span style="vertical-align: middle"> 退出 </span>
          <el-icon style="vertical-align: middle">
            <Right />
          </el-icon>
        </el-button>
      </div>
    </el-row>
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

.right-bottom {
  position: absolute;
  top: 800px;
  right: 70px;
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
</style>
