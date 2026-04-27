<script setup>
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
const router = useRouter();
onMounted(() => {
  // You can add any logic here that needs to run when the component is mounted
});

function login(){
  router.push("/createUser");
}

</script>

<template>
  <div class="Base">
    <div>
      <div class="container">
      <div class="titleContainer">
        <img class="logo" src="@/assets/logo.png" alt="Logo" />
        <div class="title">Launch Pad</div>
      </div>
      <div class="nav-item exB">Main Page</div>
      <div class="nav-item exB">Explore</div>
      <div class="nav-item exW">Create Project</div>
      <div class="nav-item exW end-element">Info</div>
      <div class="right-portion">
          <img class="right-portion-element messages" src="@/assets/header/bell.png" alt="Messages" />
          <img class=" right-portion-element notification" src="@/assets/header/message.png" alt="Notification" />
          <img class=" right-portion-element profile" @click="login" src="@/assets/header/profile.png" alt="Profile" />
      </div>
    </div>
    </div>
    
  </div>
</template>

<style scoped>
.titleContainer {
  display: inline-block;
  
  /*
    background-color: rgba(255, 137, 78, 0.504);
    padding-top: 100px;
    padding-bottom: 20px;
    padding-right: 25px;
    margin-left: -10px;
    margin-top:-100px;
    border-bottom-right-radius: 20px;
  */
}
.Base {
  display: block;
  position: absolute;
  top: 0;
  left: 0;
  width: calc(100vw);
  margin: auto;
  height: 70px;
  /*background-color: rgb(255, 189, 147);*/
  background: rgba(0, 0, 0, 0.651);
  box-shadow: 5px 5px 15px 5px #000000;
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
  margin-top: 5px;
  font-family: fantasy;
  color: rgb(255, 255, 255);

}

.end-element {
  /*border-right: 2px solid rgb(0, 0, 0);*/
}
.start-element {
  margin-left: 130px;
}
.logo {
  display: inline-block;
  width: 80px; 
  /*80px is the original size, so 50px is a good size for the logo in the header*/
  height: 80px;
  border-radius: 50px;
  position: absolute;
  margin-top: -20px;
  margin-left: 25px;
  /* whatever the dominant color of what is on the inside, should match the color of this */
  box-shadow: 0px 8px 8px 0px #3c4600;
  border: 4px solid rgb(227, 155, 78);
  background-image: linear-gradient(45deg, rgb(255, 109, 31), rgb(255, 221, 165)); 
  filter: contrast(100%);
}
.background-title{
  position: absolute;
  font-family:fantasy;
  font-size: 21px;
  transform: scaleY(200%) translateY(-10px);
  font-variant: small-caps;
  color: rgb(255, 255, 255);
  font-weight: bold;
  margin-left: 125px;
  margin-right: 0px;
  width:150px;
  text-align: center;
  margin-top: 0px;
}
.title{
  display: inline-block;
  font-family:fantasy;
  font-size: 20px;
  transform: scaleY(200%) translateY(0px);
  font-variant: small-caps;
  color: rgb(255, 255, 255);
  font-weight: bold;
  margin-left: 130px;
  margin-right: 10px;
  width:140px;
  text-align: center;
  margin-top: 0px;

}

.right-portion{
  display: inline-block;
  margin-left: auto;
}

.right-portion-element {
  width: 35px;
  height: 35px;
  border-radius: 50px;
  margin-top: -15px;
  cursor: pointer;
  margin-right: 25px;
  filter:invert(1);
  border: 2px solid rgb(0, 0, 0);
  box-shadow: 0px 0px 1px 1px #0000006c;
  padding:5px;
}

.profile {

  background-image: url("@/assets/header/profile.png");
}

.notification {

  background-image: url("@/assets/header/bell.png");
}
.messages {
}
</style>
