<script setup>
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
const router = useRouter();
onMounted(() => {
  // You can add any logic here that needs to run when the component is mounted
});
</script>

<template>
  <div class="Base">
    <div>
      <div class="container">
        <div class="left-block">
            <div class="title">Lauch Pad</div>
            <img class="logo" src="@/assets/logo.png" alt="Logo" />
        </div>
        <div class="right-portion">
          <img class="right-portion-element messages" src="@/assets/header/bell.png" alt="Messages" />
          <img class=" right-portion-element notification" src="@/assets/header/message.png" alt="Notification" />
          <img class=" right-portion-element profile" src="@/assets/header/profile.png" alt="Profile" />
        </div>
    </div>
    </div>
  </div>
</template>

<style scoped>
.Base {
  display: block;
  position: absolute;
  top: 0;
  left: 0;
  width: calc(100vw);
  margin: auto;
  height: 60px;
  background-color: rgb(0, 0, 0);
  /*background-image: linear-gradient(45deg, rgb(143, 219, 249), rgb(0, 183, 255)); */
  box-shadow: 5px 5px 15px 5px #1a1a1a;

}
.container {
  display: flex;
  min-width:940px;
  margin: auto;
  margin-top: 25px;
}

.nav-item {
  display: inline-block;
  height: 25px;
  font-size: 14px;
  /* border-left: 2px solid rgb(0, 0, 0); */
  padding-right: 25px;
  padding-left: 25px;
  font-family: fantasy;
  color: rgb(0, 0, 0);
}

.end-element {
  /*border-right: 2px solid rgb(0, 0, 0);*/
}
.start-element {
  margin-left: 150px;
}
.logo {
  display: inline-block;
  width: 40px;
  height: 40px;
  position: absolute;
  margin-top: -15px;
  /* whatever the dominant color of what is on the inside, should match the color of this */
  border-radius: 50%;
  border: 2px solid rgb(109, 69, 27);
  background-color: rgb(247, 193, 118);
  background-image: linear-gradient(45deg, rgb(255, 109, 31), rgb(255, 221, 165));
}
.title{
  display: inline-block;
  font-family: fantasy;
  font-size: 20px;
  color: rgb(232, 232, 232);
  margin-left: 30px;
  margin-right: 10px;
  margin-top: -5px;
}

.right-portion{
  display: inline-block;
  margin-left: auto;
}

.right-portion-element {
  width: 40px;
  height: 40px;
  border-radius: 50px;
  margin-top: -15px;
  cursor: pointer;
  margin-right: 25px;
  filter:invert(1);
  border: 2px solid rgb(0, 0, 0);
  
}

.profile {

}

.notification {

}
.messages {
  
}
</style>
