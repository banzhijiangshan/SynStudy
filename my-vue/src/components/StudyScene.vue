<template>
  <div>
    <el-main class="el-main">
      <PlanTable ref="infoRef"></PlanTable>
      <el-image
        :src="require('@/assets/study.png')"
        style="margin: 0; position: absolute; height: 100%; width: 100%"
      ></el-image>
    </el-main>
    <el-button type="primary" class="plan-button" @click="plan">
      我的计划
    </el-button>
    <el-button type="primary" class="shift-button"> 切换场景 </el-button>
    <el-button type="info" class="board-button"> 黑板 </el-button>
    <el-button type="primary" class="back-button" @click="outclass">
    </el-button>
  </div>
</template>

<script>
import PlanTable from "./PlanTable.vue";

export default {
  components: { PlanTable },
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
      this.$router.push("/classroom");
    },
  },
};
</script>

<style scoped>
.todo-container {
  position: absolute;
  top: 50%;
  left: 50%;
}

.plan-button {
  position: absolute;
  top: 37.5%;
  left: 2.7%;
}

.back-button {
  position: absolute;
  top: 10%;
  left: 94%;
  width: 50px;
  height: 48px;
  transform: translate(-50%, -50%);
  background-color: transparent;
  border: none;
}
.back-button:hover {
  background-color: transparent;
}

.shift-button {
  position: absolute;
  top: 58%;
  left: 2%;
}

.board-button {
  position: absolute;
  top: 79%;
  left: 2.85%;
}
</style>
