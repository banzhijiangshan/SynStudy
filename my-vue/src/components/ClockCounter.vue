<template>
  <div>
    <div>
      <h1 class="myh1">{{ formatTime(min) }} : {{ formatTime(sec) }}</h1>
    </div>
    <div v-if="isPaused">
      <div class="custom-dialog">
        <el-dialog
          title="别摸鱼了! Time flows away!"
          v-model="dialogVisible"
          width="30%"
          center="true"
          :before-close="handleClose"
        >
          <p style="text-align: center">你离开了自习室，计时已暂停</p>
          <div class="spacer"></div>
          <template v-slot:footer>
            <el-button type="primary" @click="resumeTimer" class="center-button"
              >我回来了</el-button
            >
          </template>
        </el-dialog>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ClockCounter",
  data() {
    return {
      min: 0,
      sec: 0,
      timer: null,
      isPaused: false,
      dialogVisible: false,
    };
  },
  mounted() {
    this.startTimer();
    this.dialogVisible = false;
    window.addEventListener("blur", this.pauseTimer);
  },
  methods: {
    startTimer() {
      this.timer = setInterval(() => {
        if (!this.isPaused) {
          this.sec++;
          if (this.sec === 60) {
            this.min++;
            this.sec = 0;
          }
        }
      }, 1000);
    },
    pauseTimer() {
      clearInterval(this.timer);
      this.isPaused = true;
      this.dialogVisible = true;
    },
    resumeTimer() {
      this.isPaused = false;
      this.dialogVisible = false;
      this.startTimer();
    },
    formatTime(value) {
      return value < 10 ? `0${value}` : value;
    },
    handleClose() {
      this.isPaused = false;
      this.dialogVisible = false;
      this.startTimer();
    },
  },
  beforeUnmount() {
    clearInterval(this.timer);
    window.removeEventListener("blur", this.pauseTimer);
  },
};
</script>

<style scoped>
/* Add your styles here */
.custom-dialog .el-dialog {
  font-family: "Helvetica";
}
.spacer {
  margin-bottom: 2px; /* 或者使用 padding-bottom，根据需要调整间距 */
}
.center-button {
  display: inline-block;
  padding: 4px 12px;
  margin-bottom: 0;
  font-size: 14px;
  line-height: 20px;
  text-align: center;
  vertical-align: middle;
}
.myh1 {
  font-size: 55px;
  font-family: "Arial";
  color: #bdedf8;
}
</style>
