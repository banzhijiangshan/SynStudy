<template>
  <div>
    <el-dialog
      title=""
      v-model="dialogVisible"
      width="70%"
      :height="400"
      :before-close="handleClose"
      :show-close="false"
      class="board-dialog"
    >
      <el-button type="primary" class="back-button" @click="backToStudy">
      </el-button>

      <el-button type="primary" ref="buttonRef" class="new-button"> </el-button>
      <el-button type="primary" ref="myRef" class="my-button"> </el-button>

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

      <el-popover
        ref="popoverRef2"
        :virtual-ref="myRef"
        trigger="click"
        title="我的问题"
        :width="500"
        center="true"
        virtual-triggering
        placement="top"
        align="center"
        @show="getMyQuestions"
      >
        <ul class="my-list" style="overflow: auto">
          <li
            v-for="(item, index) in myQuestions"
            class="my-list-item"
            :key="index"
            :style="{ backgroundColor: getMyColor(index) }"
          >
            <div class="my-list-main">
              <div class="list-main-text">
                <el-input
                  type="textarea"
                  :value="'简述：' + item.titleContent"
                  readonly
                  autosize
                  class="styled-reply"
                >
                </el-input>
              </div>
              <div class="button-row">
                <el-button
                  type="info"
                  class="my-info-button"
                  @click="toComment(item.id)"
                >
                  详情
                </el-button>
                <el-button
                  type="primary"
                  class="edit-button"
                  @click="openEdit(item)"
                >
                  编辑
                </el-button>
                <el-button
                  type="danger"
                  class="delete-button"
                  @click="preDeleteQuestion(index)"
                >
                  删除
                </el-button>
              </div>

              <span v-if="item.isEdit" class="editArea">
                <el-form style="margin-left: 10px; margin-top: 8px">
                  <el-form-item label="简述:">
                    <el-input
                      v-model="currentEditTitle"
                      maxlength="20"
                      show-word-limit
                    ></el-input>
                  </el-form-item>
                  <el-form-item label="内容:">
                    <el-input
                      type="textarea"
                      v-model="currentEditContent"
                      autosize
                      maxlength="200"
                      show-word-limit
                      class="custom-textarea"
                    >
                    </el-input>
                  </el-form-item>
                  <el-form-item>
                    <el-button
                      type="success"
                      @click="submitEdit(item.id)"
                      class="my-submit-button"
                      >提交</el-button
                    >
                    <el-button
                      type="warning"
                      @click="closeEdit(item)"
                      class="my-exit-button"
                      >退出</el-button
                    >
                  </el-form-item>
                </el-form>
              </span>
              <div style="height: 10px"></div>
            </div>
          </li>
        </ul>
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
              <span
                style="float: left; font-size: 16px; font-family: Helvetica"
                >{{ item.userName }}</span
              >
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
          <div style="margin-left: 6px; color: #000000; float: left">
            <span
              style="float: left; font-size: 16px; font-family: Helvetica"
              >{{ currentAsker }}</span
            >
            <div style="width: 200px"></div>
            <span
              style="
                position: relative;
                float: left;
                font-size: 15px;
                font-family: Helvetica;
                align-items: center;
                display: flex;
                color: #052bd5;
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
            autosize
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
              font-family: Helvetica;
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
                  <el-button type="warning" class="reply-button"
                    >回复</el-button
                  ></span
                >
                <span
                  v-if="com.openReply"
                  style="cursor: pointer; margin-left: auto; font-size: 14px"
                  @click="closeReply(index)"
                >
                  <el-button type="success" class="reply-button"
                    >收起</el-button
                  ></span
                >
              </div>

              <div class="comment-li-content" @click="openReply(com, index)">
                <el-input
                  type="textarea"
                  v-model="com.content"
                  readonly
                  autosize
                  class="styled-reply"
                >
                </el-input>
              </div>
              <div class="inputReply" v-if="com.openReply">
                <textarea
                  v-model="com.replyContent"
                  :placeholder="'回复@ ' + com.userName + ': '"
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
                    font-family: Helvetica;
                  "
                  >还可以输入{{ com.canInputReply }}个字符</span
                >
                <span class="sent" @click="sentReply(com, index)">发表</span>
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
                      <span style="font-size: 13px; margin: 1px; color: #000000"
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
                      <el-button type="warning" class="reply-button"
                        >回复</el-button
                      ></span
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
                      <el-button type="success" class="reply-button"
                        >收起</el-button
                      ></span
                    >
                  </div>
                  <div class="reply-li-content">
                    <el-input
                      type="textarea"
                      v-model="reply.content"
                      readonly
                      autosize
                      class="styled-reply"
                    >
                    </el-input>
                    <!--<span style="float: left; white-space: pre-wrap">{{
                      reply.content
                    }}</span>-->
                  </div>

                  <div class="inputReplySon" v-show="reply.openReply">
                    <textarea
                      v-model="reply.replyContent"
                      :placeholder="'回复@ ' + reply.fromUserNickName + ': '"
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
                      >发表</span
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
import { ElMessage, ElMessageBox } from "element-plus";
import { ref } from "vue";

/*评论结构参考：
        {
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
      currentComments: [],
      avatarUrl: "", //当前问题的提问者的头像
      canInputText: 200,
      textareaContent: "",
      backUrl: "", //后端传回
      backUserName: "", //后端传回
      backId: "",

      myQuestions: [], //我的问题
      currentEditContent: "",
      currentEditTitle: "",
    };
  },
  setup() {
    const buttonRef = ref(null);
    const popoverRef = ref(null);
    const myRef = ref(null);
    const popoverRef2 = ref(null);
    const drawer = ref(false);

    return {
      buttonRef,
      popoverRef,
      myRef,
      popoverRef2,
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
      const colors = ["#FFC0CB", "#ADD8E6", "#CFFECF", "#FDF9D4", "#D4D4D4"];
      const colorIndex = index % colors.length;
      return colors[colorIndex];
    },
    getMyColor(index) {
      const colors = ["#FFE9E9", "#F6F0FF", "#F0F5FF"];
      const colorIndex = index % colors.length;
      return colors[colorIndex];
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
          this.currentComments = [];
          for (let i = 0; i < res.data.question.comments.length; i++) {
            let tempComment = {
              id: res.data.question.comments[i].commentId,
              commenterUrl: res.data.question.comments[i].commenterUrl,
              userName: res.data.question.comments[i].userName,
              commentTime: res.data.question.comments[i].commentTime,
              content: res.data.question.comments[i].content,
              openReply: false,
              replies: res.data.question.comments[i].replies,
              replyContent: "",
              canInputReply: 200,
            };
            this.currentComments.push(tempComment);
          }
          this.avatarUrl = res.data.question.avatarUrl;
          this.currentQuestionId = id;
        }
        this.drawer = true;
        console.log("pinglun", this.currentComments);
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
      let len = this.currentComments[index].replies[index1].replyContent.length;
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
          this.canInputText = 200;
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
        let reply = {
          commentId: com.id,
          content: com.replyContent,
          replyTime: formattedDateTime,
          toUserNickName: com.userName,
          fromUserNickName: fromUserNickName,
          fromUserAvatarUrl: fromUserAvatarUrl,
          replyContent: "",
          canInputReply: 200,
        };
        console.log("reply", reply);
        this.currentComments[index].replies.push(reply);
        instance.post("/sentReply", reply).then((res) => {
          if (res.data.code === 200) {
            com.replyContent = "";
            com.openReply = false;
            com.canInputReply = 200;
          }
        });
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
        let replySon = {
          commentId: com.id,
          content: reply.replyContent,
          replyTime: formattedDateTime,
          toUserNickName: reply.fromUserNickName,
          fromUserNickName: fromUserNickName,
          fromUserAvatarUrl: fromUserAvatarUrl,
          replyContent: "",
          canInputReply: 200,
        };
        this.currentComments[index].replies.push(replySon);
        instance.post("/sentReply", replySon).then((res) => {
          if (res.data.code === 200) {
            reply.replyContent = "";
            reply.openReply = false;
            reply.canInputReply = 200;
          }
        });
      });
    },
    openReplySon(reply) {
      reply.openReply = true;
    },
    closeReplySon(reply) {
      reply.openReply = false;
    },
    openEdit(item) {
      item.isEdit = true;
      this.currentEditTitle = item.titleContent;
      this.currentEditContent = item.content;
    },
    closeEdit(item) {
      this.currentEditTitle = "";
      this.currentEditContent = "";
      item.isEdit = false;
    },
    getMyQuestions() {
      instance.get("/getMyQuestions").then((res) => {
        if (res.data.code === 200) {
          this.myQuestions = [];
          for (let i = 0; i < res.data.questions.length; i++) {
            let tempQuestion = {
              id: res.data.questions[i].id,
              titleContent: res.data.questions[i].titleContent,
              content: res.data.questions[i].content,
              isEdit: false,
            };
            this.myQuestions.push(tempQuestion);
          }
        }
      });
    },
    preDeleteQuestion(index) {
      ElMessageBox.confirm("确定要删除这个问题吗？", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          this.deleteQuestion(index);
          ElMessage({
            type: "success",
            message: "删除成功",
          });
        })
        .catch(() => {
          ElMessage({
            type: "info",
            message: "操作取消",
          });
        });
    },
    deleteQuestion(index) {
      instance
        .post("/deleteQuestion", {
          questionId: this.myQuestions[index].id,
        })
        .then((res) => {
          if (res.data.code === 200) {
            //从allQuestions中删除
            for (let i = 0; i < this.allQuestions.length; i++) {
              if (this.allQuestions[i].id === this.myQuestions[index].id) {
                this.allQuestions.splice(i, 1);
                break;
              }
            }
            this.myQuestions.splice(index, 1);
          } else {
            ElMessage({
              message: "删除失败",
              type: "error",
            });
          }
        });
    },
    submitEdit(id) {
      if (this.currentEditContent === "" || this.currentEditTitle === "") {
        ElMessage({
          message: "标题或内容不能为空",
          type: "error",
        });
        return;
      }
      instance
        .post("/editQuestion", {
          questionId: id,
          title: this.currentEditTitle,
          content: this.currentEditContent,
        })
        .then((res) => {
          if (res.data.code === 200) {
            ElMessage({
              message: "修改成功",
              type: "success",
            });
            for (let i = 0; i < this.myQuestions.length; i++) {
              if (this.myQuestions[i].id === id) {
                this.myQuestions[i].content = this.currentEditContent;
                this.myQuestions[i].titleContent = this.currentEditTitle;
                this.myQuestions[i].isEdit = false;
                break;
              }
            }
            for (let i = 0; i < this.allQuestions.length; i++) {
              if (this.allQuestions[i].id === id) {
                this.allQuestions[i].titleContent = this.currentEditTitle;
                break;
              }
            }
            this.currentEditContent = "";
            this.currentEditTitle = "";
          } else {
            ElMessage({
              message: "修改失败",
              type: "error",
            });
          }
        });
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

.my-button {
  position: absolute;
  top: 89.8%;
  left: 91%;
  width: 65px;
  height: 50px;
  transform: translate(-50%, -50%);
  border: none;
  background-color: transparent;
}
.my-button:hover {
  background-color: transparent;
}

.titleInput {
  width: 300px;
}
.contentInput {
  width: 300px;
  height: 200px;
  line-height: 200px !important;
  font-family: Helvetica;
  font-size: 14px;
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

.my-list {
  position: relative;
  margin-top: 2%;
  margin-left: 6%;
  list-style-type: none;
  width: 100%;
  height: 400px;
}

.list-item {
  color: #000000;
  border-radius: 10px;
  padding: 5px;
  float: left;
  width: 90%;
  margin-top: 1.5%;
}

.my-list-item {
  color: #000000;
  border-radius: 8px;
  padding: 5px;
  float: left;
  width: 90%;
  margin-top: 2.5%;
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

.my-list-main {
  float: left;
  display: flex;
  flex-direction: column;
  width: 100%;
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
  margin-right: 170px;
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
  font-family: Helvetica;
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
  white-space: pre-wrap;
  font-family: Helvetica;
}

.comment-nickName {
  font-size: 15px;
  color: #2073e3;
  font-family: Helvetica;
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
  font-size: 14px;
  font-family: Helvetica;
  float: right;
  cursor: pointer;
  height: 22px;
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
  font-size: 14px;
  clear: left;
  float: left;
  padding: 5px;
  cursor: pointer;
  white-space: pre-wrap;
  font-family: Helvetica;
}

.reply-nickName {
  font-size: 13px;
  color: #2073e3;
  margin-left: 6px;
  font-family: Helvetica;
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
  font-size: 14px;
  font-family: Helvetica;
  float: right;
  cursor: pointer;
  height: 22px;
}

.info-button {
  border-radius: 10px;
  border: none;
  color: white;
}

.reply-button {
  border: none;
  font-size: 13px;
  height: 27px;
  width: 45px;
}

.styled-reply :deep(.el-textarea__inner) {
  border: none !important;
  box-shadow: none !important;
  resize: none !important;
  background-color: transparent !important;
}

.my-info-button {
  border-radius: 10px;
  border: none;
  color: white;
}

.edit-button {
  border-radius: 10px;
  border: none;
  color: white;
}

.delete-button {
  border-radius: 10px;
  border: none;
  color: white;
}

.editArea {
  margin-top: 6px;
}

.my-submit-button {
  position: absolute;
  margin-top: 15px;
  left: 29%;
  width: 57px;
  height: 34px;
  border-radius: 10px;
  border: none;
}
.my-exit-button {
  position: absolute;
  margin-top: 15px;
  left: 59%;
  width: 57px;
  height: 34px;
  border-radius: 10px;
  border: none;
}

.button-row {
  margin-left: 9px;
}

.custom-textarea {
  font-family: Helvetica;
  font-size: 14px;
}
</style>
