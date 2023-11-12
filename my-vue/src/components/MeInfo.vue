<template>
  <div>
    <el-main class="el-main">
      <el-image
        :src="backImage"
        style="margin: 0; position: absolute; height: 100%; width: 100%"
      ></el-image>

      <!-- 返回按钮 -->
      <el-button
        class="back-button"
        type="primary"
        @click="goBack"
        circle
        :style="{ width: '40px', height: '40px', backgroundColor: '#ff69b4' }"
        ><i class="el-icon-arrow-left"></i
      ></el-button>

      <!-- 对话框按钮 -->
      <el-button
        class="dialog-button"
        type="primary"
        @click="openDialog"
        :style="{ width: '120px', height: '40px', backgroundColor: '#ff69b4' }"
        >打开对话框</el-button
      >

      <!-- 对话框 -->
      <el-dialog title="个人信息" :visible="dialogVisible" width="30%" center>
        <!-- 对话框内容，你可以根据需要修改 -->
        <div>
          <p>这里是个人信息的内容...</p>
        </div>
      </el-dialog>
    </el-main>
  </div>
</template>

<script>
export default {
  data() {
    return {
      backImage: require("../assets/class.png"),
      dialogVisible: false,
    };
  },
  methods: {
    goBack() {
      this.$router.go(-1);
    },
    openDialog() {
      this.dialogVisible = true;
    },
  },
};
</script>

<style scoped>
.back-button {
  position: absolute;
  top: 10px;
  left: 10px;
  border-radius: 50%;
  border: none;
  cursor: pointer;
}

.dialog-button {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  cursor: pointer;
}
</style>
