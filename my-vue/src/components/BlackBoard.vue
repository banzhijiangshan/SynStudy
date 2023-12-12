<template>
  <div>
    <el-dialog
      title=""
      v-model="dialogVisible"
      width="70%"
      :height="400"
      :before-close="handleClose"
      :show-close="false"
    >
      <el-button type="primary" class="back-button" @click="backToStudy">
      </el-button>

      <el-button type="primary" ref="buttonRef" class="new-button"> </el-button>
      <el-popover
        ref="popoverRef"
        :virtual-ref="buttonRef"
        trigger="click"
        title="写一个新问题"
        :width="450"
        center="true"
        virtual-triggering
        placement="top"
        align="center"
      >
        <el-form :model="questionForm" label-width="80px">
          <el-form-item label="简述:">
            <el-input
              v-model="questionForm.title"
              class="titleInput"
              maxlength="20"
              show-word-limit
            ></el-input>
          </el-form-item>
          <el-form-item label="内容:">
            <el-input
              v-model="questionForm.content"
              class="contentInput"
              type="textarea"
              :rows="8"
              maxlength="200"
              show-word-limit
            ></el-input>
          </el-form-item>
          <el-form-item>
            <el-button
              type="primary"
              @click="submitQuestion"
              class="submit-button"
              >提交</el-button
            >
          </el-form-item>
        </el-form>
      </el-popover>

      <ul
        class="list"
        v-infinite-scroll="load"
        style="overflow: hidden auto !important"
        infinite-scroll-immediate="false"
        v-loading="loading"
      >
        <li
          v-for="(item, index) in allQuestions"
          class="list-item"
          :key="index"
          :style="{ backgroundColor: getColor(index) }"
        >
          <div class="list-top">
            <img :src="item.imageUrl" />
            <div style="margin-left: 6px; color: #2073e3; float: left">
              <span style="float: left; font-size: 16px">{{
                item.userName
              }}</span>
              <div style="width: 200px"></div>
              <span
                style="
                  position: absolute;
                  float: left;
                  font-size: 14px;
                  align-items: center;
                  display: flex;
                  color: #000000;
                  left: 40%;
                "
              >
                {{ item.askTime }}
              </span>
            </div>
          </div>

          <div class="list-main">
            <div class="list-main-text">
              <p>简述：{{ item.titleContent }}</p>
            </div>
            <el-button
              type="info"
              class="info-button"
              @click="toComment(item.id)"
            >
              查看详情
            </el-button>
            <div style="width: 100%"></div>
          </div>

          <!--<div class="list-bottom">
            <el-button
              type="info"
              class="info-button"
              @click="toComment(item.id)"
            >
              查看详情
            </el-button>
          </div>-->
        </li>
      </ul>
    </el-dialog>

    <!--详情区-->

    <el-drawer v-model="drawer" :direction="direction">
      <template #header>
        <h2>问题详情</h2>
      </template>
      <template #default>
        <div class="list-top">
          <img :src="avatarUrl" />
          <div style="margin-left: 6px; color: #2073e3; float: left">
            <span style="float: left">{{ currentAsker }}</span>
            <div style="width: 200px"></div>
            <span
              style="
                position: relative;
                float: left;
                font-size: 16px;
                align-items: center;
                display: flex;
                color: #a426ce;
                left: 40%;
              "
            >
              {{ currentAskTime }}
            </span>
          </div>
        </div>

        <div class="detail-content">
          <textarea
            v-model="currentContent"
            style="width: 100%; height: 200px; resize: none"
            readonly
            class="styled-textarea"
          >
          </textarea>
        </div>

        <div class="inputComment">
          <textarea
            v-model="textareaContent"
            placeholder="说点什么..."
            maxlength="200"
            @input="calcInput"
          >
          </textarea>
          <span
            style="
              position: absolute;
              font-size: 14px;
              float: left;
              left: 3%;
              bottom: 5%;
            "
            >还可以输入{{ canInputText }}个字符</span
          >
          <span class="sent" @click="sentComment">发送</span>
        </div>

        <!--评论列表-->
        <div class="comment-list">
          <ul class="comment-ul">
            <li
              class="comment-li"
              v-for="(com, index) in currentComments"
              :key="index"
            >
              <div class="comment-li-top">
                <img :src="com.commenterUrl" />
                <span class="comment-nickName">{{ com.userName }}</span>
                <span style="font-size: 15px; margin-left: auto">{{
                  com.commentTime
                }}</span>
                <span
                  v-if="!com.openReply"
                  style="cursor: pointer; margin-left: auto; font-size: 16px"
                  @click="openReply(com, index)"
                >
                  回复</span
                >
                <span
                  v-if="com.openReply"
                  style="cursor: pointer; margin-left: auto; font-size: 16px"
                  @click="closeReply(index)"
                >
                  收起</span
                >
              </div>

              <div class="comment-li-content" @click="openReply(com, index)">
                <span style="text-align: left; float: left; cursor: pointer">{{
                  com.content
                }}</span>
              </div>
              <div class="inputReply" v-if="com.openReply">
                <textarea
                  v-model="com.replyContent"
                  :placeholder="'回复@' + com.userName + ': '"
                  maxlength="200"
                  @input="calcInputReply(index)"
                >
                </textarea>
                <span
                  style="
                    position: absolute;
                    font-size: 14px;
                    float: left;
                    left: 3%;
                    bottom: 5%;
                  "
                  >还可以输入{{ com.canInputReply }}个字符</span
                >
                <span class="sent" @click="sentReply(com, index)">回复</span>
              </div>
              <!--回复列表-->
              <ul class="reply-ul">
                <li
                  class="reply-li"
                  v-for="(reply, index1) in com.replies"
                  :key="index1"
                >
                  <div class="reply-li-top">
                    <img :src="reply.fromUserAvatarUrl" />
                    <span class="reply-nickName"
                      >{{ reply.fromUserNickName }}
                      <span style="font-size: 15px; margin: 3px; color: #000000"
                        >回复</span
                      >
                      {{ reply.toUserNickName }}</span
                    >
                    <span style="margin-left: auto; font-size: 13px">{{
                      reply.replyTime
                    }}</span>
                    <span
                      v-if="!reply.openReply"
                      style="
                        cursor: pointer;
                        margin-left: auto;
                        font-size: 14px;
                      "
                      @click="openReplySon(reply)"
                    >
                      回复</span
                    >
                    <span
                      v-if="reply.openReply"
                      style="
                        cursor: pointer;
                        margin-left: auto;
                        font-size: 14px;
                      "
                      @click="closeReplySon(reply)"
                    >
                      收起</span
                    >
                  </div>
                  <div class="reply-li-content">
                    <span style="float: left">{{ reply.content }}</span>
                  </div>

                  <div class="inputReplySon" v-show="reply.openReply">
                    <textarea
                      v-model="reply.replyContent"
                      :placeholder="'回复@' + reply.fromUserNickName + ': '"
                      maxlength="200"
                      @input="calcReplySon(index, index1)"
                    >
                    </textarea>
                    <span
                      style="
                        position: absolute;
                        font-size: 12px;
                        float: left;
                        left: 3%;
                        bottom: 5%;
                      "
                      >还可以输入{{ reply.canInputReply }}个字符</span
                    >
                    <span class="sent" @click="sentReplySon(com, index, reply)"
                      >回复</span
                    >
                  </div>
                </li>
              </ul>
            </li>
          </ul>
        </div>
      </template>

      <template #footer> </template>
    </el-drawer>
  </div>
</template>

<script>
import instance from "@/axios";
import { ElMessage } from "element-plus";
import { ref } from "vue";

export default {
  name: "BlackBoard",
  data() {
    return {
      currentQuestionId: "",
      dialogVisible: false,
      allQuestions: [],
      page: 0,
      loadFinished: false,
      questionForm: {
        title: "",
        content: "",
      },
      loading: false,
      currentAsker: "Alice",
      currentAskTime: "2021-06-01 11:00",
      currentContent: "",
      //"有ABC三个神,只知他们名为“真实、虚谎、任性”,但不知哪个代号属于哪个名字。真实之神只说真话，虚谎之神只说假话,而任性之神会随机地说真话或假话。我们的任务是找出ABC的身份。我们一共可以问他们三个问题，且问题必须是用“是”或“否回答的问题，每次只能向其中一个神发问但可以问同一个神多个问题。神只会用他们的语言回答“da”或“ja”,其中一个代表“是”，一个代表“否”,但我们不知道哪个回答是哪个意思。如何提问才能区分出三个神的身份?",
      currentComments: [],
      /*{
          id: 1,
          commenterUrl: "",
          userName: "Bob",
          commentTime: "2021-06-01 12:00",
          content: "这个问题很有意思",
          openReply: false,
          replies: [
            {
              commentId: 1,
              content: "我也觉得",
              replyTime: "2021-06-01 12:05",
              toUserNickName: "Bob",
              fromUserNickName: "Carol",
              fromUserAvatarUrl: "",
              openReply: false,
              canInputReply: 200,
            },
          ],
          replyContent: "",
          canInputReply: 200,
        },*/
      avatarUrl: "", //当前问题的提问者的头像
      canInputText: 200,
      textareaContent: "",
      backUrl: "", //后端传回
      backUserName: "", //后端传回
      backId: "",
    };
  },
  setup() {
    const buttonRef = ref(null);
    const popoverRef = ref(null);
    const drawer = ref(false);

    return {
      buttonRef,
      popoverRef,
      drawer,
    };
  },
  mounted() {
    this.dialogVisible = false;
    this.load();
  },

  methods: {
    open() {
      this.dialogVisible = true;
    },
    handleClose() {
      this.dialogVisible = false;
      this.$emit("flesh");
    },
    backToStudy() {
      this.dialogVisible = false;
    },
    getColor(index) {
      const colors = ["#FFC0CB", "#ADD8E6", "#CFFECF", "#FDF9D4", "#D4D4D4"]; // 定义不同的颜色值数组
      const colorIndex = index % colors.length; // 每三个表项为一个循环
      return colors[colorIndex]; // 返回对应索引的颜色值
    },

    //后端回传格式：code, data:{questions:[{id, titleContent, imageUrl, userName, askTime}]}
    load() {
      if (this.loadFinished === false) {
        this.loading = true;
        instance
          .post("/getAllQuestions", {
            page: this.page,
          })
          .then((res) => {
            if (res.data.code === 200) {
              for (let i = 0; i < res.data.questions.length; i++) {
                this.allQuestions.push(res.data.questions[i]);
              }
              this.page += res.data.questions.length;
              if (res.data.questions.length < 5) {
                this.loadFinished = true;
              }
            }
            this.loading = false;
          });
      } else {
        ElMessage({
          message: "我是有底线哒~",
          type: "warning",
        });
      }
    },
    getNewestQuestion() {
      instance.get("/getNewestQuestion").then((res) => {
        if (res.data.code === 200) {
          this.allQuestions.unshift(res.data.question);
          this.page += 1;
          //this.loadFinished = true;
        }
      });
    },
    submitQuestion() {
      if (this.questionForm.title === "" || this.questionForm.content === "") {
        ElMessage({
          message: "标题或内容不能为空",
          type: "error",
        });
        return;
      }
      let now = new Date();
      let year = now.getFullYear();
      let month = String(now.getMonth() + 1).padStart(2, "0");
      let day = String(now.getDate()).padStart(2, "0");
      let hours = String(now.getHours()).padStart(2, "0");
      let minutes = String(now.getMinutes()).padStart(2, "0");
      let seconds = String(now.getSeconds()).padStart(2, "0"); // 获取当前秒数
      let formattedDateTime = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
      instance
        .post("/addQuestion", {
          title: this.questionForm.title,
          content: this.questionForm.content,
          askTime: formattedDateTime,
        })
        .then((res) => {
          if (res.data.code === 200) {
            ElMessage({
              message: "提交成功",
              type: "success",
            });
            this.questionForm.title = "";
            this.questionForm.content = "";
            //this.loadFinished = false;
            this.getNewestQuestion();
          }
        });
    },
    //后端回传格式：code, data:{avatarUrl, userName, asktime, content, comments:[{commenterUrl, userName, commentTime, content, replies:[{fromUserAvatarUrl, fromUserNickName, toUserNickName, replyTime, replyContent}]} ]}
    toComment(id) {
      instance.post("/getQuestionById", { id: id }).then((res) => {
        if (res.data.code === 200) {
          this.currentAsker = res.data.question.userName;
          this.currentAskTime = res.data.question.askTime;
          this.currentContent = res.data.question.content;
          this.currentComments = res.data.question.comments;
          this.avatarUrl = res.data.question.avatarUrl;
          this.currentQuestionId = id;
        }
        console.log("详情", res);
        this.drawer = true;
      });
    },
    calcInput() {
      let len = this.textareaContent.length;
      this.canInputText = 200 - len;
    },
    calcInputReply(index) {
      let len = this.currentComments[index].replyContent.length;
      this.currentComments[index].canInputReply = 200 - len;
    },
    calcReplySon(index, index1) {
      let len = this.currentComments[index].replies[index1].content.length;
      this.currentComments[index].replies[index1].canInputReply = 200 - len;
    },
    sentComment() {
      let tempComment = this.textareaContent;
      if (tempComment === "") {
        ElMessage({
          message: "评论内容不能为空",
          type: "error",
        });
        return;
      }
      let now = new Date();
      let year = now.getFullYear();
      let month = String(now.getMonth() + 1).padStart(2, "0");
      let day = String(now.getDate()).padStart(2, "0");
      let hours = String(now.getHours()).padStart(2, "0");
      let minutes = String(now.getMinutes()).padStart(2, "0");
      let seconds = String(now.getSeconds()).padStart(2, "0"); // 获取当前秒数
      let formattedDateTime = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
      //请求
      instance
        .post("/addComment", {
          time: formattedDateTime,
          questionId: this.currentQuestionId,
          content: tempComment,
        })
        .then((res) => {
          if (res.data.code === 200) {
            this.$message({
              message: "发送成功",
              type: "success",
            });
            this.textareaContent = "";
            this.backUrl = res.data.info.imageUrl;
            this.backUserName = res.data.info.userName;
            this.backId = res.data.info.commentId;
          } else {
            this.$message({
              message: "发送失败",
              type: "error",
            });
          }
          //用现有数据更新当前评论区
          let addComment = {
            id: this.backId,
            commenterUrl: this.backUrl,
            userName: this.backUserName,
            commentTime: formattedDateTime,
            content: tempComment,
            openReply: false,
            replies: [],
            replyContent: "",
            canInputReply: 200,
          };
          this.currentComments.push(addComment);
        });
    },
    openReply(com) {
      com.openReply = true;
      //com.replyContent = "回复@" + com.userName + ": ";
      //this.$set(com, "openReply", true);
      //this.$set(com, "回复@" + com.nickName);
    },
    closeReply(index) {
      this.currentComments[index].openReply = false;
    },
    sentReply(com, index) {
      if (com.replyContent === "") {
        ElMessage({
          message: "回复内容不能为空",
          type: "error",
        });
        return;
      }
      let now = new Date();
      let year = now.getFullYear();
      let month = String(now.getMonth() + 1).padStart(2, "0");
      let day = String(now.getDate()).padStart(2, "0");
      let hours = String(now.getHours()).padStart(2, "0");
      let minutes = String(now.getMinutes()).padStart(2, "0");
      let seconds = String(now.getSeconds()).padStart(2, "0"); // 获取当前秒数
      let formattedDateTime = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
      let fromUserNickName = "";
      let fromUserAvatarUrl = "";
      instance.get("/getUserInfo").then((res) => {
        fromUserNickName = res.data.userInfo.username;
        fromUserAvatarUrl = res.data.userInfo.image;
      });
      let reply = {
        commentId: com.id,
        content: com.replyContent,
        replyTime: formattedDateTime,
        toUserNickName: com.userName,
        fromUserNickName: fromUserNickName,
        fromUserAvatarUrl: fromUserAvatarUrl,
      };
      console.log(reply);
      this.currentComments[index].replies.push(reply);
      instance.post("/sentReply", reply).then((res) => {
        if (res.data.code === 200) {
          com.replyContent = "";
          com.openReply = false;
        }
      });
    },
    sentReplySon(com, index, reply) {
      if (reply.replyContent === "") {
        ElMessage({
          message: "回复内容不能为空",
          type: "error",
        });
        return;
      }
      let now = new Date();
      let year = now.getFullYear();
      let month = String(now.getMonth() + 1).padStart(2, "0");
      let day = String(now.getDate()).padStart(2, "0");
      let hours = String(now.getHours()).padStart(2, "0");
      let minutes = String(now.getMinutes()).padStart(2, "0");
      let seconds = String(now.getSeconds()).padStart(2, "0"); // 获取当前秒数
      let formattedDateTime = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
      let fromUserNickName = "";
      let fromUserAvatarUrl = "";
      instance.get("/getUserInfo").then((res) => {
        fromUserNickName = res.data.userInfo.username;
        fromUserAvatarUrl = res.data.userInfo.image;
      });
      let replySon = {
        commentId: reply.commentId,
        content: reply.replyContent,
        replyTime: formattedDateTime,
        toUserNickName: reply.fromUserNickName,
        fromUserNickName: fromUserNickName,
        fromUserAvatarUrl: fromUserAvatarUrl,
      };
      this.currentComments[index].replies.push(replySon);
      instance.post("/sentReply", replySon).then((res) => {
        if (res.data.code === 200) {
          reply.replyContent = "";
          reply.openReply = false;
        }
      });
    },
    openReplySon(reply) {
      reply.openReply = true;
    },
    closeReplySon(reply) {
      reply.openReply = false;
    },
  },
};
</script>

<style scoped>
.back-button {
  position: absolute;
  top: 10%;
  left: 8%;
  width: 95px;
  height: 58px;
  transform: translate(-50%, -50%);
  border: none;
  background-color: transparent;
}
.back-button:hover {
  background-color: transparent;
}

.new-button {
  position: absolute;
  top: 90%;
  left: 83%;
  width: 65px;
  height: 50px;
  transform: translate(-50%, -50%);
  border: none;
  background-color: transparent;
}
.new-button:hover {
  background-color: transparent;
}

.titleInput {
  width: 300px;
}
.contentInput {
  width: 300px;
  height: 200px;
  line-height: 200px !important;
}

.submit-button {
  position: absolute;
  margin-top: 1px;
  left: 67%;
  width: 70px;
  height: 35px;
  border-radius: 3px;
  border: none;
}

.read-button {
  position: absolute;
  top: 90%;
  left: 20%;
  width: 65px;
  height: 50px;
  transform: translate(-50%, -50%);
  border: none;
}

.styled-textarea {
  width: 100%;
  height: 200px;
  resize: none;
  border: 2px solid #ccc; /* 添加边框 */
  border-radius: 10px; /* 圆角 */
  font-family: Helvetica; /* 字体 */
  font-size: 14px; /* 字号 */
  padding: 10px; /* 内边距 */
  box-sizing: border-box; /* 盒模型 */
}

.detail-content {
  margin-top: 10px;
}

.centered-title .el-popover__title {
  text-align: center;
}

:deep() .el-dialog {
  height: 70% !important;
}

:deep() .el-dialog,
.el-pager li {
  background-color: rgba(255, 0, 0, 0);
  color: #ffffff;
  background-image: url(../assets/board.png) !important;
  background-size: 100% 100%;
}
.el-dialog__header {
  padding-top: 10px !important;
  background-color: rgb(255, 255, 255, 0);
  border-radius: 14px 14px 0 0;
}
.el-dialog__body {
  border-top: 0 !important;
  background-color: rgba(19, 31, 59, 0);
  color: #ffffff;
}
.el-dialog__footer {
  text-align: center;
  background-color: rgba(255, 255, 255, 0);
}

.list {
  position: absolute;
  margin-top: 4%;
  margin-left: 13%;
  list-style-type: none;
  width: 76%;
  height: 63%;
}

.list-item {
  color: #000000;
  border-radius: 10px;
  padding: 5px;
  float: left;
  width: 90%;
  margin-top: 1.5%;
}

.list-top img {
  width: 45px;
  height: 45px;
  border-radius: 50%;
  object-fit: fill;
}

.list-top {
  position: relative;
  display: flex;
  align-items: center;
  width: 100%;
  flex-wrap: wrap;
  margin-left: 0.8%;
  margin-top: 0.8%;
}

.list-main {
  position: relative;
  float: left;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  width: 100%;
  margin-top: 0.8%;
  margin-left: 1.5%;
}

.list-main-text {
  text-align: left;
  float: left;
  overflow: hidden;
  text-overflow: ellipsis;
  width: 400px;
  display: -webkit-box;
  -webkit-line-clamp: 6;
  -webkit-box-orient: vertical;
  font-family: Helvetica;
  font-size: 16px;
  margin-right: 180px;
}

.inputComment {
  margin-top: 3%;
  width: 100%;
  margin-left: 0%;
  position: relative;
  height: 185px;
  border-radius: 13px;
  padding: 3%;
  background-color: #f7f2f2;
  color: #000000;
}

.inputComment textarea {
  width: 100%;
  position: relative;
  height: 150px;
  border: 0 solid;
  outline: none;
  resize: none;
  background-color: var(--main-bg-color);
  color: #000000;
}

.inputComment .sent {
  position: absolute;
  bottom: 4%;
  right: 3%;
  border-radius: 15px;
  background-color: #ee464b;
  color: white;
  padding: 2px 15px;
  font-size: 16px;
  float: right;
  cursor: pointer;
  height: 25px;
}

.comment-list {
  width: 100%;
  border-radius: 14px;
  margin-top: 4%;
  height: 72%;
  position: relative;
}

.comment-ul {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 99%;
  position: relative;
  list-style-type: none;
  overflow: auto;
}

.comment-li {
  margin: 2%;
  float: left;
  width: 96%;
  position: relative;
  overflow: auto;
}

.comment-li-top {
  display: flex;
  float: left;
  align-items: center;
  width: 90%;
}

.comment-li-top span {
  margin-left: 8px;
}

.comment-li img {
  width: 35px;
  height: 35px;
  border-radius: 50%;
}

.comment-li-content {
  margin-left: 7%;
  width: 86%;
  font-size: 14px;
  clear: left;
  float: left;
  padding: 5px;
  cursor: pointer;
  overflow: auto;
}

.comment-nickName {
  font-size: 18px;
  color: #2073e3;
}

.inputReply {
  float: left;
  margin-top: 1%;
  width: 92%;
  margin-left: 8%;
  position: relative;
  height: 140px;
  border-radius: 13px;
  padding: 2%;
  background-color: #eafffb;
  color: #000000;
}

.inputReply textarea {
  width: 98%;
  position: relative;
  height: 120px;
  border: 0 solid;
  outline: none;
  resize: none;
  background-color: #eafffb;
  color: #000000;
}

.inputReply .sent {
  position: absolute;
  bottom: 4%;
  right: 2%;
  border-radius: 30px;
  background-color: #ee464b;
  color: white;
  padding: 2px 15px;
  font-size: 16px;
  float: right;
  cursor: pointer;
  height: 25px;
}
.reply-ul {
  margin: 0;
  padding: 0;
  width: 100%;
  position: relative;
  list-style-type: none;
  overflow: auto;
}

.reply-li {
  margin-left: 7%;
  margin-top: 1%;
  float: left;
  width: 92%;
  position: relative;
  overflow: auto;
}

.reply-li-top {
  display: flex;
  float: left;
  align-items: center;
  width: 90%;
}
.reply-li img {
  width: 35px;
  height: 35px;
  border-radius: 50%;
}

.reply-li-content {
  margin-left: 8%;
  width: 82%;
  font-size: 16px;
  clear: left;
  float: left;
  padding: 5px;
  cursor: pointer;
}

.reply-nickName {
  font-size: 16px;
  color: #2073e3;
}

.inputReplySon {
  float: left;
  margin-top: 1%;
  width: 92%;
  margin-left: 8%;
  position: relative;
  height: 140px;
  border-radius: 13px;
  padding: 2%;
  background-color: #eafffb;
  color: #000000;
}

.inputReplySon textarea {
  width: 98%;
  position: relative;
  height: 120px;
  border: 0 solid;
  outline: none;
  resize: none;
  background-color: #eafffb;
  color: #000000;
}

.inputReplySon .sent {
  position: absolute;
  bottom: 4%;
  right: 2%;
  border-radius: 30px;
  background-color: #ee464b;
  color: white;
  padding: 2px 15px;
  font-size: 16px;
  float: right;
  cursor: pointer;
  height: 24px;
}

.info-button {
  border-radius: 10px;
  border: none;
  color: white;
}
</style>
