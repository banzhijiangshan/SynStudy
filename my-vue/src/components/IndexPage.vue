<template>
  <div>
    <el-main class="el-main">
      <el-image
        :src="require('@/assets/back.png')"
        style="margin: 0; position: absolute; height: 100%; width: 100%"
      ></el-image>
      <el-row class="el-row">
        <el-col>
          <div class="radius">
            <el-form :model="form" label-width="auto" size="large">
              <br />
              <br />
              <el-form-item style="display: inline-block; width: 80%">
                <el-input
                  class="el-input"
                  maxlength="30"
                  show-word-limit
                  placeholder="学号/邮箱"
                  v-model="form.name"
                />
              </el-form-item>
              <el-form-item style="display: inline-block; width: 80%">
                <el-input
                  class="el-input"
                  maxlength="30"
                  show-word-limit
                  placeholder="密码"
                  show-password
                  v-model="form.password"
                  type="password"
                />
              </el-form-item>

              <el-row>
                <el-col :span="8" :offset="4">
                  <el-button
                    type="primary"
                    class="button-class"
                    round
                    @click="login"
                    >登录</el-button
                  >
                </el-col>
                <el-col :span="8">
                  <el-button
                    type="success"
                    class="button-class"
                    round
                    @click="register"
                    >注册</el-button
                  >
                </el-col>
              </el-row>
            </el-form>
          </div>
        </el-col>
      </el-row>
    </el-main>
  </div>
  <div class="custom-container">
    <LunBo></LunBo>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";
import { reactive } from "vue";
import instance from "@/axios";
import { ElMessage } from "element-plus";
import LunBo from "./LunBo.vue";
import md5 from "js-md5";

const router = useRouter();

const form = reactive({
  name: "",
  password: "",
});

const login = async () => {
  if (!form.name || !form.password) {
    ElMessage.error("用户名或密码为空");
    return;
  }
  let password = md5(form.password);
  instance
    .post("/login", {
      name: form.name,
      password: password,
    })
    .then((res) => {
      if (res.data.code === 200) {
        router.push("/building");
        getStudentName();
      } else {
        ElMessage.error(res.data.message);
      }
    });
};

const register = async () => {
  await router.push("/register");
};

const getStudentName = async () => {
  instance.get("/getStudentName").then((res) => {
    if (res.data.code === 200) {
      ElMessage({
        message: "欢迎" + res.data.name + "同学!",
        type: "success",
      });
    }
  });
};
</script>

<style scoped>
.radius {
  height: 42%;
  width: 30%;
  border: 1px solid var(--el-border-color);
  border-radius: 20px;
  margin-top: 19%;
  margin-left: 63%;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.5);
  text-align: center;
  background-color: #daf3f1 !important;
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

.button-class {
  width: 70%;
  height: 80%;
  text-align: center;
  font-size: 20px;
  background-color: #1677ff;
  border-radius: 7px !important;
}

.custom-container {
  margin-top: -600px; /* 向下偏移 20px */
  margin-left: 5px; /* 向右偏移 50px */
}
</style>
