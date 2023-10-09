<template>
  <div class="sign-up">
    <img src="../assets/2.jpg" alt="Sign up" />
  </div>
</template>

<script>
export default {
  name: "SignUp",
};
</script>

<style scoped>
.sign-up {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: black; /* 可选，设置背景色 */
}

.sign-up img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain; /* 修改为contain以保持图片比例且充满容器 */
}
</style>
