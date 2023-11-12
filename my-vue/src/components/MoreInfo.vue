<template>
  <div>
    <el-dialog
      title="帮助"
      v-model="dialogVisible"
      width="30%"
      :before-close="handleClose"
    >
      暂时不能给你明确的答复，软件的用法需要你自己衡量！
    </el-dialog>
  </div>
</template>

<script>
//import { userInfo, updateUser } from "@/api/user.js";

export default {
  name: "InfoDia",
  data() {
    return {
      dialogVisible: false,
    };
  },
  mounted() {
    //this.load();
    this.dialogVisible = false;
  },
  methods: {
    open() {
      this.dialogVisible = true;
    },
    /*load() {
        userInfo(this.$store.state.id)
          .then((res) => {
            console.log(res);
            Object.assign(this.form, res.data);
          })
          .catch((err) => {
            console.log(err);
          });
      },
      submit() {
        updateUser(this.form)
          .then((res) => {
            console.log(res);
            this.dialogVisible = false;
            this.$emit("flesh");
          })
          .catch((err) => {
            console.log(err);
          });
      },*/
    handleClose() {
      this.dialogVisible = false;
      this.$emit("flesh");
    },
  },
};
</script>

<style scoped>
.el-dialog {
  position: absolute;
  top: 300px;
}
</style>
