<script setup>
import { AccountLocal } from "@/lib/appwrite";
import { onMounted, ref } from "vue";
import { ID } from "appwrite";
import router from "@/router";
import { useRoute } from "vue-router";
import axios from "axios";
const apiUrl = import.meta.env.VITE_APP_API_URL;

let userId = "";
let secret = "";
let error = ref("");

onMounted(() => {
    userId = route.query.userId;
    secret = route.query.secret;
    axios.get(`${apiUrl}users/search/account_setup/${userId}`).then((res) => {}).catch((err) => {
        router.push("/login");
        alert("There was something wrong with looking up your account. Please try again, contact us if problems persist.");
    }); 
});

const route = useRoute();
let password = ref("");
let complete = ref(false);
async function resetPassword() {
  try {
    await AccountLocal.updateRecovery(
      userId,
      secret,
      password.value
    );
    complete.value = true;
  } catch (err) {
    error.value = err.message;
  }
};

</script>

<template>
  <div class="background">
    <section>
          <span></span>
          <span></span>
          <span></span>
          <span></span>
          <span></span>
          <span></span>
          <span></span>
          <span></span>
          <span></span>
          <span></span>
          <span></span>
          <span></span>
          <span></span>
          <span></span>
          <span></span>
          <span></span>
          <span></span>
          <span></span>
          <span></span>
          <span></span>
          <span></span>
          <span></span>
          <span></span>
          <span></span>
          <span></span>
          <!-- credit https://codepen.io/delroyprithvi/pen/LYyJROR -->
      </section>
    <div class="galaxy-backdrop">
    <div class="login-box">
        <div class="outline" v-if="!complete">
          <div class="login-header" style="margin-bottom:20px;">Password Reset</div>
          <div class="sub-text">
            Enter the new password you would like to use for your account.
          </div>
          <input v-model="password" class="input" placeholder="New Password" type="password" style="margin-top:20px;"/>
          <button @click="resetPassword(password)" class="register-button" style="margin-top:10px;">Reset Password</button>
          <div class="error-log">{{error}}</div>
        </div>
        <div class="outline" v-else>
          <div class="login-header" style="margin-bottom:20px;">Password Reset</div>
          <div class="sub-text">
            Password has been successfully reset! You can now log in with your new password.
          </div>
        </div>
      
      <div class="logoBox">
        <img src="@/assets/logo.png"  class="apollo"/>
      </div>
    </div>
  </div>
  </div>
</template>

<style scoped>
.sub-text{
  font-size: 12px;
  color: rgb(70, 70, 70);
  font-family: Arial, Helvetica, sans-serif;
  width:calc(100% - 40px);
  margin:auto;
}
.logoBox{
  width:100vw;
  max-width:2000px;
  position: absolute;
  transform: translate(-50%, -50%);
  left:calc(50% - 150px);
  background:rgba(255, 255, 255, 0);
  top: calc(50% + 100px);
  z-index: -1;
}
.apollo{
  width:fit-content;
  float:left;
  z-index: -1;
  filter: invert(0) contrast(00) hue-rotate(30deg);
  opacity: .1;
}
.galaxy-backdrop{
  width: 2000px;
  height: 1000px;
  position: absolute;
  top:50%;
  left:50%;
  transform: translate(-50%, -50%);
  border-radius: 0%;
   
}
.outline{
  padding: 30px;
  padding-bottom: 50px;
  border: 8px solid #8b8b8b81;
  box-shadow: inset 0 0 10px 10px #cacaca;
  border-radius: 10px;
  
  overflow:hidden;
  height:100%;
}

.register-link{
  font-size: 12px;
  color: rgb(0, 4, 255);
  font-family: Arial, Helvetica, sans-serif;
  width:fit-content;
  padding:2px;

  text-decoration: underline;
}
.register-link:hover{
  color: rgb(0, 4, 255);
  text-decoration: underline;
  cursor: pointer;
}
.register-link:active{
  color: rgb(0, 4, 255);
  text-decoration: underline;
}
.register-link:visited{
  color: rgb(0, 4, 255);
  text-decoration: underline;
}
.register-link:focus{
  color: rgb(0, 4, 255);
  text-decoration: underline;
}
.register-link:focus-visible{
  color: rgb(0, 4, 255);
  text-decoration: underline;
}
.register-link:focus-within{
  color: rgb(0, 4, 255);
  text-decoration: underline;
}
.sign-up-button{
  display: block;
  background-color: #ff6d41;
  color: rgb(255, 255, 255);
  padding: 10px;
  border-radius: 5px;
  width:calc(100% - 20px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  font-size: 12px;
  font-family: Arial, Helvetica, sans-serif;
  margin:auto;
  margin-top: 10px;
}
.background{
  width: 100vw;
  height: 100vh;
  position: absolute;
  top:0;
  left:0;
  filter:invert(0);
  overflow: hidden;
  background: radial-gradient(ellipse at center, rgb(1, 0, 88) 30%, rgb(2, 0, 36) 70%);
  background-image: url("https://static.vecteezy.com/system/resources/thumbnails/021/249/965/small/background-starry-night-sky-stars-sky-night-silhouette-of-the-mountains-vector.jpg");
  background-size: cover;
}
.register{
  font-size: 12px;
  color: rgb(0, 4, 255);
  font-family: Arial, Helvetica, sans-serif;
  width:fit-content;
  padding:10px;
  display: block;
  float:right;
}
.or-word{
  font-size: 14px;
  color: rgb(70, 70, 70);
  font-family: Arial, Helvetica, sans-serif;
  width:fit-content;
  margin: auto;
  margin-top: -15px;
  background-color: white;
  padding:5px;
  padding-left:20px;
  padding-right:20px;
  margin-bottom: 20px;
}
.register-text{
  position: absolute;
  bottom:25px;
  font-size: 12px;
  color: rgb(70, 70, 70);
  font-family: Arial, Helvetica, sans-serif;
  width: 100%;
  background-color: transparent;
  outline: none;
  border:none;
  text-align: right;
  margin-top:20px;
  margin-left:-60px;
}
.passwrod-forget-text{
  font-size: 12px;
  color: rgb(104, 104, 104);
  font-family: Arial, Helvetica, sans-serif;
  display:block;
  width:fit-content;
  margin:auto;
  margin-top: 20px;
  margin-bottom: 20px;
}
.passwrod-forget-text:hover{
  color: rgb(104, 104, 104);
  text-decoration: underline;
  cursor: pointer;
}
.line{
  margin-top:15px;
  margin-bottom: 15px;
  height: 1px;
  background:#b6b6b6;
  width: 90%;
  margin:auto;
  margin-top: 30px;
}
.login-header{
  font-family: Arial, Helvetica, sans-serif;
  font-size: 20px;
  margin-top:30px;
  margin-bottom: 40px;
  text-align: center;
}
.register-button{
  display: block;
  background-color: #ff0d86;
  color: rgb(255, 255, 255);
  padding: 10px;
  border-radius: 5px;
  width:calc(100% - 40px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  font-size: 12px;
  font-family: Arial, Helvetica, sans-serif;
  margin:auto;
  margin-top: 10px;
}
.login-button{
  display: block;
  background-color: #ffffff;
  color: rgb(128, 128, 128);
  padding: 10px;
  border-radius: 5px;
  width:calc(100% - 40px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  font-size: 12px;
  font-family: Arial, Helvetica, sans-serif;
  margin:auto;
  margin-top: 10px;
}
.input{
  display: block;
  background-color: #ffffff;
  color: rgb(70, 70, 70);
  padding: 10px;
  border-radius: 5px;
  width:calc(100% - 40px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  font-size: 12px;
  font-family: Arial, Helvetica, sans-serif;
  margin:auto;
  margin-top: 10px;
  margin-bottom: 10px;
}
.google-icon{
  width: 20px;
  height: 20px;
  margin-right: 10px;
  border:white 1px solid;
  background-image: url("@/assets/user-creation/google.png");
  background-size: cover;
  vertical-align: middle;
  background-position: center;
  
}
.login-gooogle-button{

  display: block;
  background-color: #ffffff;
  color: rgb(70, 70, 70);
  padding: 10px;
  border-radius: 5px;
  width:calc(100% - 40px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.356);
  cursor: pointer;
  font-size: 13px;
  font-family: Arial, Helvetica, sans-serif;
  margin:auto;
  margin-top: 10px;
  margin-bottom: 10px;
  
}
.login-gooogle-button:hover{
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.493);
  transition: all 0.3s ease;
}

.error-log{
  color: red;
  width:calc(100% - 40px);
  padding: 10px;
  text-align: left;
  font-size: 12px;
  margin-left: 5px;
  font-family: Arial, Helvetica, sans-serif;
}
.login-box {
  display:block;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  height: 490px;
  box-shadow: 0 40px 100px rgba(0, 0, 0, 0.692);
  border-radius: 10px;
  width: 450px;
  background: rgb(255, 255, 255);
  filter:invert(0);
  
}

*{
    margin: 0;
    padding:0;
    box-sizing: border-box;
}
body{
    overflow: hidden;
}
section{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100vh;
    /* https://lh3.googleusercontent.com/ka_5IYJDRkXZnbptxq64LPuggGL5FM8gnpJlsuSiOQh4b39kMkiRbVfX8iK8bjMg5SLkdfoix09P60wyFjN2=w681-h614 */
    background: radial-gradient(circle, rgb(47, 0, 78) 20%, rgb(2, 0, 34) 80%);

/*   background-color:black; */
    background-size: cover;
    animation: animateBg 50s linear infinite;
}

@keyframes animateBg{
    0%,100%{
        transform: scale(1);
    }
    50%{
        transform: scale(1);
    }
}

span{
    position: absolute;
    top:50%;
    left:50%;
    width: 4px;
    height: 4px;
    background: #fff;
    border-radius: 50%;
    box-shadow: 0 0 0 4px rgba(255,255,255,0.1),0 0 0 8px rgba(255,255,255,0.1),0 0 20px rgba(255,255,255,0.1);
    animation: animate 3s linear infinite;
}

@keyframes animate
{
    0%
    {
        transform: rotate(330deg) translateX(0);
        opacity: 1;
    }
    70%
    {
        opacity: 1;
    }
    100%
    {
        transform: rotate(330deg) translateX(-2000px);
        opacity: 0;
    }
}
span:nth-child(1){
    top: 0;
    right: 0;
    left: initial;
    animation-duration: 1s;
}
span:nth-child(2){
    top: 0;
    right: 80px;
    left: initial;
    animation-duration: 3s;
}
span:nth-child(3){
    top: 80px;
    right: 0px;
    left: initial;
    animation-duration: 30.75s;
}
span:nth-child(4){
    top: -100px;
    right: 180px;
    left: initial;
    animation-duration: 20.75s;
}
span:nth-child(5){
    top: 10px;
    right: 400px;
    left: initial;
    animation-duration: 5.75s;
}
span:nth-child(6){
    top: 0;
    right: 600px;
    left: initial;
    animation-duration: 2.75s;
}
span:nth-child(7){
    top: 300px;
    right: 0px;
    left: initial;
    animation-duration: 8.75s;
}
span:nth-child(8){
    top: 20px;
    right: 700px;
    left: initial;
    animation-duration: 1.75s;
}
span:nth-child(11){
    top: -30px;
    right: 1000px;
    left: initial;
    animation-duration: 13.75s;
}
span:nth-child(9){
    top: -20px;
    right: 450px;
    left: initial;
    animation-duration: 11.75s;
}

span:nth-child(10){
    top: -100px;
    right: 500px;
    left: initial;
    animation-duration: 20.75s;
}


</style>

<style lang="saas" scoped>

</style>
