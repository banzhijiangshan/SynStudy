<template>
  <div>
    <el-main class="el-main">
      <el-image
        :src="require('@/assets/register.png')"
        style="margin: 0; position: absolute; height: 100%; width: 100%"
      ></el-image>
      <el-row class="el-row">
        <el-col align="center">
          <div class="radius">
            <el-form :model="form" label-width="auto" size="large">
              <br />
              <br />
              <el-form-item class="el-form-item">
                <el-input
                  class="el-input"
                  maxlength="30"
                  show-word-limits
                  placeholder="学号"
                  v-model="form.id"
                />
              </el-form-item>

              <el-form-item class="el-form-item">
                <el-input
                  class="el-input"
                  maxlength="30"
                  show-word-limit
                  placeholder="用户名"
                  v-model="form.name"
                />
              </el-form-item>

              <el-form-item class="el-form-item">
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

              <el-form-item class="el-form-item">
                <el-input
                  class="el-input"
                  maxlength="30"
                  show-word-limit
                  placeholder="重复密码"
                  show-password
                  v-model="form.repeatpassword"
                  type="password"
                />
              </el-form-item>

              <el-form-item class="el-form-item">
                <el-input
                  class="el-input"
                  maxlength="30"
                  show-word-limit
                  placeholder="邮箱"
                  show-password
                  v-model="form.email"
                  type="password"
                />
              </el-form-item>

              <el-row>
                <el-col :span="8" :offset="4">
                  <el-button
                    type="primary"
                    class="button-class"
                    round
                    @click="commit"
                    >注册</el-button
                  >
                </el-col>
                <el-col :span="8">
                  <el-button
                    type="success"
                    class="button-class"
                    round
                    @click="back"
                    >返回</el-button
                  >
                </el-col>
              </el-row>
            </el-form>
          </div>
        </el-col>
      </el-row>
    </el-main>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";
import { reactive } from "vue";
import instance from "@/axios";
import { ElMessage } from "element-plus";

const form = reactive({
  name: "",
  password: "",
  label: "",
  sex: "",
  area: "",
  stage: "",
  school: "",
  goal: "",
});

const router = useRouter();

const commit = async () => {
  instance
    .post("/register", {
      name: form.name,
      password: form.password,
      email: form.email,
    })
    .then((res) => {
      if (res.data.code === 200) {
        ElMessage({
          message: res.data.message,
          type: "success",
        });
        router.push("/");
      } else {
        ElMessage.error(res.data.message);
      }
    });
};
const back = () => {
  router.push("/");
};
</script>

<style scoped>
.h1 {
  text-align: center;
  font-size: 100px;
  transform: translateY(-50%);
  color: #ffbc37;
  font-family: STLiti, serif;
}

.radius {
  height: 65%;
  width: 400px;
  border: 1px solid var(--el-border-color);
  border-radius: 20px;
  margin-top: 240px;
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
  margin-bottom: 30px;
}

.el-form-item {
  display: inline-block;
  width: 80%;
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
</style>
