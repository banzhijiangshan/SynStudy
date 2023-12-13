<template>
  <div>
    <el-main class="el-main">
      <PlanTable ref="infoRef"></PlanTable>
      <PersonalDia ref="infoRef1"></PersonalDia>
      <InfoDia ref="infoRef2"></InfoDia>
      <BlackBoard ref="infoRef3"></BlackBoard>
      <el-image
        :src="currentScene"
        alt="Current Scene"
        style="margin: 0; position: absolute; height: 100%; width: 100%"
      ></el-image>

      <el-button type="primary" class="plan-button" @click="plan">
        我的计划
      </el-button>
      <el-button type="primary" class="shift-button" @click="showSceneDialog">
        切换场景
      </el-button>
      <el-button type="primary" class="board-button" @click="showBoard">
        黑板
      </el-button>
      <el-button type="primary" class="back-button" @click="outclass">
      </el-button>

      <el-dialog
        title="选择虚拟场景"
        v-model="dialogVis"
        width="55%"
        center="true"
      >
        <div class="scene-grid">
          <div v-for="(scene, index) in scenes" :key="index">
            <div class="scene-item">
              <img
                :src="scene"
                alt="Scene"
                class="scene-image"
                @click="switchScene(index + 1)"
              />
              <span class="image-description">{{ descriptions[index] }}</span>
            </div>
          </div>
        </div>
      </el-dialog>
      <ClockCounter class="myclk" ref="clockref"></ClockCounter>
    </el-main>
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
    <h2 class="titlenum">{{ studytogether }}</h2>
  </div>
</template>

<script>
import PlanTable from "./PlanTable.vue";
import PersonalDia from "./UserInfo.vue";
import InfoDia from "./MoreInfo.vue";
import ClockCounter from "./ClockCounter.vue";
import BlackBoard from "./BlackBoard.vue";
import instance from "@/axios";

export default {
  components: {
    PlanTable,
    PersonalDia,
    InfoDia,
    ClockCounter,
    BlackBoard,
  },
  data() {
    return {
      currentScene: require("@/assets/study.png"),
      studytogether: 0,
      dialogVis: false,
      timer: null,
      scenes: [
        require("@/assets/choice1.png"),
        require("@/assets/choice2.png"),
        require("@/assets/choice3.png"),
        require("@/assets/choice4.png"),
      ],
      choices: [
        require("@/assets/study.png"),
        require("@/assets/study2.png"),
        require("@/assets/study3.png"),
        require("@/assets/study4.png"),
      ],
      descriptions: ["清晨教室", "书房课桌", "小镇书屋", "傍晚教室"],
    };
  },
  mounted() {
    instance.post("/peopleIncrease").then((res) => {
      if (res.data.code === 200) {
        this.freshData();
        this.timer = setInterval(this.freshData, 5000);
      }
    });
  },
  methods: {
    //添加todo
    addTodo(todoObj) {
      this.todos.unshift(todoObj);
    },
    //勾选或取消勾选一个todo
    checkTodo(id) {
      //遍历todo
      this.todos.forEach((todo) => {
        if (todo.id === id) todo.done = !todo.done;
      });
    },
    deleteTodo(id) {
      this.todos = this.todos.filter((todo) => {
        return todo.id !== id;
      });
    },
    //全选或全不选
    checkAllTodo(done) {
      this.todos.forEach((todo) => {
        todo.done = done;
      });
    },
    //清除所有已完成todo
    clearAllTodo() {
      this.todos = this.todos.filter((todo) => {
        return !todo.done;
      });
    },
    plan() {
      this.$refs.infoRef.open();
    },
    outclass() {
      instance
        .post("/timeIncrease", {
          min: this.$refs.clockref.min,
          sec: this.$refs.clockref.sec,
        })
        .then((res) => {
          if (res.data.code === 200) {
            this.$router.push("/classroom");
          } else {
            this.$message.error(res.data.message);
          }
        });
    },
    showPersonalDialog() {
      this.$refs.infoRef1.open();
    },
    showInfoDia() {
      this.$refs.infoRef2.open();
    },
    freshData() {
      instance.get("/getStudyInfo").then((res) => {
        this.studytogether = res.data.studyInfo.studytogether;
      });
    },
    showSceneDialog() {
      this.dialogVis = true;
    },
    switchScene(index) {
      this.currentScene = this.choices[index - 1]; // Use index to get the corresponding choice
      this.dialogVis = false;
    },
    showBoard() {
      this.$refs.infoRef3.open();
    },
  },
  beforeUnmount() {
    instance.post("/peopleDecrease");
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
.todo-container {
  position: absolute;
  top: 50%;
  left: 50%;
}

.plan-button {
  position: absolute;
  top: 35.5%;
  left: 1.3%;
}

.back-button {
  position: absolute;
  top: 8%;
  left: 92.5%;
  width: 50px;
  height: 48px;
  background-color: transparent;
  transform: translate(-50%, -50%);

  border: none;
}
.back-button:hover {
  background-color: transparent;
}

.shift-button {
  position: absolute;
  top: 56%;
  left: 0.7%;
}

.board-button {
  position: absolute;
  top: 77%;
  left: 1.5%;
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

.myclk {
  position: absolute;
  top: 4.33%;
  left: 56%;
}

.titlenum {
  position: absolute;
  top: 17.8%;
  left: 41.55%;
  transform: translate(-50%, -50%);
  font-size: 47px;
  color: #ffffff;
  font-family: Helvetica;
}

.scene-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
}

.scene-image {
  max-width: 100%;
  height: auto;
  cursor: pointer;
  border-radius: 10px;
}
.scene-image:hover {
  border: 6px solid #1677ff;
}
.scene-item {
  position: relative;
}
.image-description {
  position: relative;
  left: 42%;
  font-family: "Arial";
}
</style>
