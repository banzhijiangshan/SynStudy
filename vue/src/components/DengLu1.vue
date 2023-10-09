<template>
  <div class="full-screen-image">
    <img src="../assets/1.jpg" alt="Full-screen image" />
    <button class="custom-button" @click="redirectToPage">点击我跳转</button>
  </div>
</template>

<script>
export default {
  name: "FullScreenImage",
  methods: {
    redirectToPage() {
      this.$router.push("/signup");
    },
  },
};
</script>

<style scoped>
.full-screen-image {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: black;
}

.full-screen-image img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}
.custom-button {
  opacity: 0;
  position: absolute;
  top: 52.9%;
  left: 85.35%;
  transform: translate(-50%, -50%);
  background-color: #007bff; /* 背景颜色 */
  color: #fff; /* 文字颜色 */
  padding: 16px 28px;
  border: none;
  cursor: pointer;
}
</style>
