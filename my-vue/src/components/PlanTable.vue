<template>
  <div>
    <div class="custom-dialog">
      <el-dialog
        title="计划表"
        v-model="dialogVisible"
        width="50%"
        :before-close="handleClose"
        :center="true"
      >
        <div id="root">
          <div class="todo-container">
            <div class="todo-wrap">
              <MyHeader :addTodo="addTodo"></MyHeader>
              <div class="spacer"></div>
              <MyList
                :todos="todos"
                :checkTodo="checkTodo"
                :deleteTodo="deleteTodo"
              ></MyList>
              <MyFooter
                :todos="todos"
                :checkAllTodo="checkAllTodo"
                :clearAllTodo="clearAllTodo"
              ></MyFooter>
            </div>
          </div>
        </div>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import MyHeader from "./MyHeader.vue";
import MyList from "./MyList.vue";
import MyFooter from "./MyFooter.vue";

export default {
  name: "PlanTable",
  components: { MyHeader, MyList, MyFooter },
  data() {
    return {
      todos: [
        { id: "001", title: "这是一个完成的例子", done: true },
        { id: "002", title: "这是一个未完成的例子", done: false },
      ],
      dialogVisible: false,
    };
  },
  mounted() {
    this.dialogVisible = true;
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
    handleClose() {
      this.dialogVisible = false;
      this.$emit("flesh");
    },

    open() {
      this.dialogVisible = true;
    },
  },
};
</script>

<style>
.body {
  background: #fff;
}
.btn {
  display: inline-block;
  padding: 4px 12px;
  margin-bottom: 0;
  font-size: 14px;
  line-height: 20px;
  text-align: center;
  vertical-align: middle;
  cursor: pointer;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.2),
    0 1px 2px rgba(0, 0, 0, 0.05);
  border-radius: 4px;
}

.btn-danger {
  color: #fff;
  background-color: #da4f49;
  border: 1px solid #bd362f;
}

.btn-danger:hover {
  color: #fff;
  background-color: #bd362f;
}

.btn:focus {
  outline: none;
}

.todo-container {
  width: 600px;
  margin: 0 auto;
}
.todo-container .todo-wrap {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
}
.custom-dialog .el-dialog {
  font-family: "Helvetica";
}
.spacer {
  margin-bottom: 12px; /* 或者使用 padding-bottom，根据需要调整间距 */
}
</style>
