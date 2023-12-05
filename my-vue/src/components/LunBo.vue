<template>
  <div
    class="SwiperBox"
    ref="SwiperBox"
    @mouseenter="MouseFun('移入')"
    @mouseleave="MouseFun('移出')"
  >
    <!-- 图片 -->
    <div
      class="imgBox"
      :style="{ left: `-${leftVal}px`, transition: `${ition}s` }"
    >
      <img :src="item.imgUrl" v-for="(item, index) in imgList" :key="index" />
      <!-- 复制第一张放到最后,以实现无缝无线循环滚动效果 -->
      <img :src="imgList[0].imgUrl" alt="" />
    </div>
    <!-- 下方指示点容器 -->
    <div class="instBox">
      <div
        @click="instFun(index)"
        v-for="(item, index) in imgList.length"
        :key="index"
        :class="['inst', index == imgShow ? 'instActv' : '']"
      ></div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      imgList: [
        { imgUrl: require("../assets/1.png") },
        { imgUrl: require("../assets/2.png") },
        { imgUrl: require("../assets//3.png") },

        // 添加其他图片信息
      ],
      leftVal: 0, // 轮播图盒子的偏移值
      flag: true, // 用来节流防止重复点击
      start: null, // 自动执行下一张定的时器
      imgWidth: 720, // 在这里填写你需要的图片宽度
      ition: 0.6, // 设置轮播图过渡时间
      imgShow: 0, // 表示当前显示的图片索引
    };
  },
  mounted() {
    // this.imgWidth = this.$refs.SwiperBox.offsetWidth // 自动获取轮播图盒子宽度
    this.timer();
  },
  methods: {
    // 这里定义一个鼠标移入移出事件，鼠标悬停时停止自动轮播，鼠标移出则重新执行自动轮播
    MouseFun(type) {
      type == "移入" ? clearTimeout(this.start) : this.timer();
    },
    // 此为自动轮播定时器
    timer() {
      this.start = setInterval(() => {
        this.NextFun();
      }, 2400);
    },
    // 这里通过额外封装的节流函数触发 PrevFun() 和 NextFun(),以达到防止重复点击的效果
    throttle(fun) {
      if (this.flag) {
        this.flag = false;
        fun();
        setTimeout(() => {
          this.flag = true;
        }, 650);
      }
    },
    // 上一张
    PrevFun() {
      if (this.leftVal == 0) {
        this.ition = 0;
        this.imgShow = this.imgList.length - 1;
        this.leftVal = this.imgList.length * this.imgWidth;
        this.$nextTick(() => {
          setTimeout(() => {
            this.ition = 0.6;
            this.leftVal -= this.imgWidth;
          }, this.ition * 1000);
        });
      } else {
        this.ition = 0.6;
        this.leftVal -= this.imgWidth;
        this.imgShow--;
      }
    },
    // 下一张
    NextFun() {
      if (this.leftVal == (this.imgList.length - 1) * this.imgWidth) {
        this.ition = 0.6;
        this.leftVal += this.imgWidth;
        this.imgShow = 0;
        this.$nextTick(() => {
          setTimeout(() => {
            this.ition = 0;
            this.leftVal = 0;
          }, this.ition * 1000);
        });
      } else {
        this.ition = 0.6;
        this.leftVal += this.imgWidth;
        this.imgShow++;
      }
    },
    // 点击小圆点
    instFun(index) {
      this.ition = 0.6;
      this.leftVal = index * this.imgWidth;
      this.imgShow = index;
    },
  },
};
</script>

<style>
* {
  padding: 0px;
  margin: 0px;
  box-sizing: border-box;
}
/* 图片容器样式 */
.SwiperBox {
  position: relative;
  width: 720px;
  height: 640px;
  top: 0px; /* 自定义垂直位置 */
  left: 130px;
  align-items: center;
  box-sizing: border-box;
  cursor: pointer;
  overflow: hidden;
}
.imgBox {
  position: absolute;
  top: 0px;
  left: 0px;
  min-width: 500px;
  height: 480px;
  display: flex;
  justify-content: flex-start;
}
/* 图片默认样式 */
.imgBox img {
  flex-shrink: 0;
  width: 720px;
  height: 640px;
}
/* 下方指示器盒子 */
.instBox {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  bottom: 10px;
  display: flex;
}
/* 小圆点 */
.inst {
  width: 10px;
  height: 10px;
  border: 1px solid #ccc;
  margin-right: 8px;
  background: #fff;
  border-radius: 50%;
  cursor: pointer;
}
.inst:last-child {
  margin-right: 0px;
}
.instActv {
  border: 1px solid #1677ff;
  background: #1677ff;
}
</style>
