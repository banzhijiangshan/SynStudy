<template>
  <div>
    <el-main class="el-main">
      <PlanTable ref="infoRef"></PlanTable>
      <PersonalDia ref="infoRef1"></PersonalDia>
      <InfoDia ref="infoRef2"></InfoDia>
      <el-image
        :src="require('@/assets/study.png')"
        style="margin: 0; position: absolute; height: 100%; width: 100%"
      ></el-image>
      <el-button type="primary" class="plan-button" @click="plan">
        我的计划
      </el-button>
      <el-button type="primary" class="shift-button"> 切换场景 </el-button>
      <el-button type="info" class="board-button"> 黑板 </el-button>
      <el-button type="primary" class="back-button" @click="outclass">
      </el-button>
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
import instance from "@/axios";

export default {
  components: {
    PlanTable,
    PersonalDia,
    InfoDia,
    ClockCounter,
  },
  data() {
    return {
      studytogether: 0,
      timer: null,
    };
  },
  freshData() {
    instance.get("/getStudyInfo").then((res) => {
      this.studytogether = res.data.studytogether;
    });
  },
  mounted() {
    this.freshData();
    this.timer = setInterval(this.freshData, 5000);
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
      instance.post("/timeIncrease", {
        min: this.$refs.clockref.min,
        sec: this.$refs.clockref.sec,
      });
      this.$router.push("/classroom");
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
  top: 4.2%;
  left: 52.5%;
}

.titlenum {
  position: absolute;
  top: 17.56%;
  left: 41.6%;
  transform: translate(-50%, -50%);
  font-size: 50px;
  color: #ffffff;
  font-family: STLiti, serif;
}
</style>
