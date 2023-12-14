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
    <el-button type="primary" class="enter-button1" @click="study"> </el-button>
    <el-button type="primary" class="enter-button2" @click="study"> </el-button>
    <el-button type="primary" class="enter-button3" @click="study"> </el-button>
    <el-button type="primary" class="enter-button4" @click="study"> </el-button>
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
    <h2 class="titletime">{{ hour }} 时 {{ min }} 分</h2>
    <h2 class="titlenum">{{ studytogether }}</h2>
  </div>
</template>

<script>
import PersonalDia from "./UserInfo.vue";
import InfoDia from "./MoreInfo.vue";
import instance from "@/axios";
import { ElMessage } from "element-plus";

export default {
  components: { PersonalDia, InfoDia },
  data() {
    return {
      hour: 0,
      min: 0,
      studytogether: 0,
      timer: null,
    };
  },
  mounted() {
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
        } else {
          instance.get("/getStudyInfo").then((res) => {
            this.hour = res.data.studyInfo.hour;
            this.min = res.data.studyInfo.minute;
            this.studytogether = res.data.studyInfo.studytogether;
          });
        }
      });
    this.timer = setInterval(this.heartBeat, 3000);
  },
  methods: {
    study() {
      this.$router.push("/study");
    },
    exit() {
      instance.post("/exitClassRoom").then((res) => {
        if (res.data.code === 200) {
          this.$router.push("/floor");
        }
      });
    },
    showPersonalDialog() {
      this.$refs.infoRef1.open();
    },
    showInfoDia() {
      this.$refs.infoRef2.open();
    },
    heartBeat() {
      instance
        .post("/heartbeat", {
          messsage: "I am alive!",
        })
        .then((res) => {
          if (res.data.valid === 0) {
            this.$router.push("/login");
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
.el-main {
  height: 100%;
  width: 100%;
  margin: 0;
  padding: 0;
}

.enter-button {
  position: absolute;
  top: 40.5%;
  left: 57.98%;
  width: 10.4%;
  height: 7.4%;
  transform: translate(-50%, -50%);
  background-color: transparent;
  border: 4px solid transparent;
  transition: border 0.3s;
}
.enter-button:hover {
  background-color: transparent;
  border-color: white;
  border-radius: 6px;
}

.enter-button1 {
  position: absolute;
  top: 40.5%;
  left: 68.26%;
  width: 10.4%;
  height: 7.4%;
  transform: translate(-50%, -50%);
  background-color: transparent;
  border: 4px solid transparent;
  transition: border 0.3s;
}
.enter-button1:hover {
  background-color: transparent;
  border-color: white;
  border-radius: 6px;
}

.enter-button2 {
  position: absolute;
  top: 58.86%;
  left: 40.72%;
  width: 10.4%;
  height: 7.4%;
  transform: translate(-50%, -50%);
  background-color: transparent;
  border: 4px solid transparent;
  transition: border 0.3s;
}
.enter-button2:hover {
  background-color: transparent;
  border-color: white;
  border-radius: 6px;
}

.enter-button3 {
  position: absolute;
  top: 77.2%;
  left: 29.68%;
  width: 10.4%;
  height: 7.4%;
  transform: translate(-50%, -50%);
  background-color: transparent;
  border: 4px solid transparent;
  transition: border 0.3s;
}
.enter-button3:hover {
  background-color: transparent;
  border-color: white;
  border-radius: 6px;
}

.enter-button4 {
  position: absolute;
  top: 77.2%;
  left: 68.33%;
  width: 10.4%;
  height: 7.4%;
  transform: translate(-50%, -50%);
  background-color: transparent;
  border: 4px solid transparent;
  transition: border 0.3s;
}
.enter-button4:hover {
  background-color: transparent;
  border-color: white;
  border-radius: 6px;
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

.titletime {
  position: absolute;
  top: 8.3%;
  left: 58.2%;
  transform: translate(-50%, -50%);
  font-size: 50px;
  color: white;
  font-family: Helvetica;
}

.titlenum {
  position: absolute;
  top: 93.3%;
  left: 41%;
  transform: translate(-50%, -50%);
  font-size: 50px;
  color: #000000;
  font-family: Helvetica;
}
</style>
