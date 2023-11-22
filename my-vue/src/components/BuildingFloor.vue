<template>
  <div>
    <el-main class="el-main">
      <PersonalDia ref="infoRef"></PersonalDia>
      <InfoDia ref="infoRef1"></InfoDia>
      <el-image
        :src="
          isDay
            ? require('@/assets/floorday.png')
            : require('@/assets/night1.png')
        "
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
    <el-button type="primary" class="enter-button" @click="goin1"> </el-button>
    <el-button type="primary" class="enter-button1" @click="goin2"> </el-button>
    <el-button type="primary" class="enter-button2" @click="goin3"> </el-button>
    <el-button type="primary" class="goon-button" @click="goon"> </el-button>
  </div>
</template>

<script>
import PersonalDia from "./UserInfo.vue";
import InfoDia from "./MoreInfo.vue";
import instance from "@/axios";

export default {
  components: {
    PersonalDia,
    InfoDia,
  },
  data() {
    return {
      isDay: true,
    };
  },
  mounted() {
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
    goback() {
      this.$router.push("/building");
    },
    showInfoDia() {
      this.$refs.infoRef1.open();
    },
    goin1() {
      //math
      instance.post("/classRoom", {
        subject: "math",
      });
      this.$router.push("/classroom");
    },
    goin2() {
      //phy
      instance.post("/classRoom", {
        subject: "phy",
      });
      this.$router.push("/classroom");
    },
    goin3() {
      //chem
      instance.post("/classRoom", {
        subject: "chem",
      });
      this.$router.push("/classRoom");
    },
    goon() {
      this.$router.push("/second");
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

.goon-button {
  position: absolute;
  top: 53.5%;
  right: 4.3%;
  width: 86px;
  height: 90px;
  background-color: transparent;
  border: none;
}
.goon-button:hover {
  background-color: transparent;
}
</style>
