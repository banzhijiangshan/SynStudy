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

export default {
  components: { PersonalDia, InfoDia },
  data() {
    return {
      hour: 0,
      min: 0,
      studytogether: 0,
    };
  },
  mounted() {
    instance.get("/getStudyInfo").then((res) => {
      this.hour = res.data.hour;
      this.minute = res.data.minute;
      this.studytogether = res.data.studytogether;
    });
  },
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

.enter-button1 {
  position: absolute;
  top: 40.5%;
  left: 68.2%;
  width: 155px;
  height: 64px;
  transform: translate(-50%, -50%);
  background-color: transparent;
  border: 3px solid transparent;
  transition: border 0.3s;
}
.enter-button1:hover {
  background-color: transparent;
  border-color: white;
}

.enter-button2 {
  position: absolute;
  top: 58.86%;
  left: 40.6%;
  width: 155px;
  height: 64px;
  transform: translate(-50%, -50%);
  background-color: transparent;
  border: 3px solid transparent;
  transition: border 0.3s;
}
.enter-button2:hover {
  background-color: transparent;
  border-color: white;
}

.enter-button3 {
  position: absolute;
  top: 77.2%;
  left: 29.55%;
  width: 155px;
  height: 64px;
  transform: translate(-50%, -50%);
  background-color: transparent;
  border: 3px solid transparent;
  transition: border 0.3s;
}
.enter-button3:hover {
  background-color: transparent;
  border-color: white;
}

.enter-button4 {
  position: absolute;
  top: 77.2%;
  left: 68.2%;
  width: 155px;
  height: 64px;
  transform: translate(-50%, -50%);
  background-color: transparent;
  border: 3px solid transparent;
  transition: border 0.3s;
}
.enter-button4:hover {
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

.titletime {
  position: absolute;
  top: 8.3%;
  left: 58.2%;
  transform: translate(-50%, -50%);
  font-size: 50px;
  color: white;
  font-family: STLiti, serif;
}

.titlenum {
  position: absolute;
  top: 93.3%;
  left: 41%;
  transform: translate(-50%, -50%);
  font-size: 50px;
  color: #000000;
  font-family: STLiti, serif;
}
</style>
