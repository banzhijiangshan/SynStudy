<template>
  <div class="todo-header">
    <input
      type="text"
      placeholder="输入你的计划项，按回车键加入列表"
      v-model="title"
      @keyup.enter="add"
      maxlength="34"
    />
  </div>
</template>

<script>
import { nanoid } from "nanoid";
export default {
  name: "MyHeader",
  data() {
    return {
      title: "",
    };
  },
  props: ["addTodo"],
  //接收从App传递过来的addTodo
  methods: {
    add() {
      //校验数据
      if (!this.title.trim()) return alert("输入不能为空");
      //将用户输入生成一个对象
      const todoObj = { id: nanoid(), title: this.title, done: false };
      //将新生成的对象传给App
      this.addTodo(todoObj);
      this.title = "";
    },
  },
};
</script>

<style scoped>
/*header*/
.todo-header input {
  width: 578px;
  height: 32px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 4px 7px;
}

.todo-header input:focus {
  outline: none;
  border-color: rgba(82, 168, 236, 0.8);
  box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.075),
    0 0 8px rgba(82, 168, 236, 0.6);
}
</style>
