<template>
  <div>
    <el-main class="el-main">
      <PersonalDia ref="infoRef"></PersonalDia>
      <InfoDia ref="infoRef1"></InfoDia>
      <el-image
        :src="
          isDay
            ? require('@/assets/home.png')
            : require('@/assets/nightbuilding.png')
        "
        style="margin: 0; position: absolute; height: 100%; width: 100%"
      ></el-image>
      <el-button
        class="circular-button enter-button"
        type="primary"
        @click="enter"
        circle
        :style="{ width: '130px', height: '130px' }"
      ></el-button>
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
      <el-button
        class="rectangular-button"
        type="primary"
        icon="el-icon-search"
        @click="logout"
      ></el-button>
    </el-main>
  </div>
</template>

<script>
import { ElMessage } from "element-plus";
import PersonalDia from "./UserInfo.vue";
import instance from "@/axios";
import InfoDia from "./MoreInfo.vue";

export default {
  components: {
    PersonalDia,
    InfoDia,
  },
  data() {
    return {
      isDay: true,
      timer: null,
    };
  },
  mounted() {
    this.timer = setInterval(this.heartBeat, 3000);
    const currentTime = new Date().getHours();
    if (currentTime >= 6 && currentTime < 18) {
      this.isDay = true;
    } else {
      this.isDay = false;
    }
  },
  methods: {
    showPersonalDialog() {
      this.$refs.infoRef.open();
    },
    logout() {
      instance.post("/logout");
      this.$router.push("/");
      ElMessage({
        message: "Goodbye!Have a nice day in your real life!",
        type: "success",
      });
    },
    enter() {
      this.$router.push("/floor");
    },
    showInfoDia() {
      this.$refs.infoRef1.open();
    },
    heartBeat() {
      instance
        .post("/heartbeat", {
          messsage: "I am alive!",
        })
        .then((res) => {
          if (res.data.valid === 0) {
            this.$router.push("/");
            ElMessage({
              message: "登录已失效",
              type: "error",
            });
          }
        });
    },
  },
  beforeUnmount() {
    clearInterval(this.timer);
  },
};
</script>

<style scoped>
.circular-button {
  position: absolute;
  border-radius: 50%;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.enter-button {
  top: 75%;
  left: 59.96%;
  transform: translate(-50%, -50%);
  background-color: transparent;
}

.profile-button {
  top: 10%;
  left: 10%;
}

.rectangular-button {
  position: absolute;
  top: 2.1%;
  right: 2.35%;
  padding: 53px;
  border: none;
  background-color: transparent;
}

.rectangular-button:hover,
.circular-button:hover {
  background: transparent;
}

.el-main {
  height: 100%;
  width: 100%;
  margin: 0;
  padding: 0;
}

.el-row {
  margin-top: 10px;
  margin-bottom: 100px;
}

.el-input {
  text-align: center;
  vertical-align: middle;
}
.left-top {
  position: absolute;
  top: 20px;
  left: 30px;
}

.button-class {
  display: inline-block;
  min-width: 50px;
  height: 50px;
  font-size: 24px;
  top: 4%;
  left: 2%;
}

.custom-container {
  margin-top: -600px; /* 向下偏移 20px */
  margin-left: 5px; /* 向右偏移 50px */
}
</style>
