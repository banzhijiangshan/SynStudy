<template>
  <div>
    <el-main class="el-main">
      <PersonalDia></PersonalDia>
      <el-image
        :src="require('@/assets/floor.png')"
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

        <el-button type="primary" circle class="button-class">
          <el-icon style="vertical-align: middle">
            <MoreFilled />
          </el-icon>
        </el-button>
      </div>

      <div class="right-bottom">
        <el-button type="success" class="button-class1" @click="goback">
          <span style="vertical-align: middle"> 退出 </span>
          <el-icon style="vertical-align: middle">
            <Right />
          </el-icon>
        </el-button>
      </div>
    </el-row>
  </div>
</template>

<script setup>
//import { useRouter } from "vue-router";
import PersonalDia from "./UserInfo.vue";
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
  top: 780px;
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
