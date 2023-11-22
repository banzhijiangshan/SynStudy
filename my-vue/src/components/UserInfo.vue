<template>
  <div>
    <el-dialog
      title="个人信息"
      v-model="dialogVisible"
      width="57%"
      :before-close="handleClose"
    >
      <el-form :model="form" :rules="rules" ref="form" label-width="150px">
        <div class="updateinfo">
          <div class="left">
            <el-form-item label="头像" prop="avatar">
              <!--<input
                type="file"
                @change="handleAvatarChange"
                accept="image/*"
              />
              <img
                v-if="form.avatar"
                style="width: 110px; height: 110px; border-radius: 50%"
                :src="form.avatar"
              />-->
              <el-upload
                class="avatar-uploader"
                action="/uploadAvatar"
                :show-file-list="false"
                :on-success="handleAvatarSuccess"
                :before-upload="beforeAvatarUpload"
              >
                <img v-if="imageUrl" :src="imageUrl" class="avatar" />
                <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
              </el-upload>
            </el-form-item>
            <!--<el-form-item label="密码" prop="password">
              <el-input v-model="form.password"></el-input>

            </el-form-item>
            <el-form-item label="用户名" prop="username">
              <el-input v-model="form.username"></el-input>

            </el-form-item>
            <el-form-item label="年龄" prop="age">
              <el-input v-model="form.age"></el-input>
            </el-form-item>
            <el-form-item label="性别" prop="sex">
              <el-switch
                v-model="form.sex"
                active-color="#13ce66"
                inactive-color="#ff4949"
                active-text="男"
                inactive-text="女"
                :active-value="1"
                :inactive-value="0"
              >
              </el-switch>
            </el-form-item>
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="form.email"></el-input>
            </el-form-item>
          </div>
          <div class="right">
            <el-form-item label="学号" prop="id">
              <el-input
                v-model="form.id"
                style="width: 280px"
                disabled
              ></el-input>
            </el-form-item>

            <el-form-item label="地区" prop="area">
              <el-input v-model="form.area" style="width: 280px"></el-input>
            </el-form-item>
            <el-form-item label="兴趣爱好" prop="hobby">
              <el-input v-model="form.hobby" style="width: 280px"></el-input>
            </el-form-item>
            <el-form-item label="职业" prop="work">
              <el-input v-model="form.work" style="width: 280px"></el-input>
            </el-form-item>
            <el-form-item label="个性签名" prop="design">
              <el-input v-model="form.design" style="width: 280px"></el-input>
            </el-form-item>
            <el-form-item label="手机号码" prop="phone">
              <el-input v-model="form.phone" style="width: 280px"></el-input>
            </el-form-item>
          </div>
        </div>
      </el-form>
      <template v-slot:footer>
        <el-button @click="handleClose">取 消</el-button>
        <el-button type="primary" @click="submit">提 交</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import instance from "@/axios";
import { ElMessage } from "element-plus";
//import { Plus } from "@element-plus/icons-vue";

export default {
  name: "PersonalDia",
  data() {
    return {
      dialogVisible: false,
      imageUrl: "",
      form: {
        password: "",
        username: "",

        age: Number,
        sex: Number,
        email: "",
        id: Number,
        area: "",
        hobby: "",
        work: "",
        design: "",
        phone: "",
      },
      rules: {
        username: [
          { required: true, message: "用户名不能为空", trigger: "blur" },
        ],
        password: [
          { required: true, message: "密码不能为空", trigger: "blur" },
        ],
      },
    };
  },
  mounted() {
    this.load();
    this.dialogVisible = false;
  },
  methods: {
    open() {
      this.dialogVisible = true;
    },
    load() {
      instance.get("/getUserInfo").then((res) => {
        this.imageUrl = res.data.userInfo.image;
        this.form.password = res.data.userInfo.password;
        this.form.username = res.data.userInfo.username;
        this.form.age = res.data.userInfo.age;
        if (res.data.userInfo.sex === 0) {

          this.form.sex = false;
        } else if (res.data.userInfo.sex === 1) {
          this.form.sex = true;
        }
        this.form.email = res.data.userInfo.email;
        this.form.id = res.data.userInfo.id;
        this.form.area = res.data.userInfo.area;
        this.form.hobby = res.data.userInfo.hobby;
        this.form.work = res.data.userInfo.work;
        this.form.design = res.data.userInfo.design;
        this.form.phone = res.data.userInfo.phone;
      });
    },
    submit() {
      instance.post("/updateUserInfo", this.form).then((res) => {
        if (res.data.code === 200) {
          ElMessage({
            message: "保存成功",
            type: "success",
          });
        } else {
          ElMessage({
            message: "保存失败",
            type: "error",
          });
        }
      });
    },
    handleClose() {
      this.dialogVisible = false;
      this.$emit("flesh");
    },
    handleAvatarSuccess(response, uploadFile) {
      this.imageUrl = URL.createObjectURL(uploadFile.raw);
    },
    beforeAvatarUpload(rawFile) {
      if (rawFile.type !== "image/jpeg") {
        ElMessage.error("Avatar picture must be JPG format!");
        return false;
      } else if (rawFile.size / 1024 / 1024 > 2) {
        ElMessage.error("Avatar picture size can not exceed 2MB!");
        return false;
      }
      return true;
    },
  },
};
</script>

<style scoped>
.updateinfo {
  height: 390px;
  overflow: auto;
}
.left {
  /* width: 330px; */
  float: left;
}
.right {
  overflow: hidden;
}
.avatar-uploader .avatar {
  width: 110px;
  height: 110px;
  display: block;
}
</style>

<style>
.avatar-uploader .el-upload {
  border: 1px dashed var(--el-border-color);
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--el-transition-duration-fast);
}

.avatar-uploader .el-upload:hover {
  border-color: var(--el-color-primary);
}

.el-icon.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 110px;
  height: 110px;
  text-align: center;
}
</style>
