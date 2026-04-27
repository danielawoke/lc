<script setup>
import { AccountLocal } from "@/lib/appwrite";
import { onMounted, ref } from "vue";
import { ID } from "appwrite";
import router from "@/router";
import axios from "axios";
import { useRoute } from "vue-router";
const route = useRoute();
const domain = import.meta.env.VITE_LAUNCHPAD_DOMAIN;
const apiUrl = import.meta.env.VITE_APP_API_URL;
// This page should have a gentle vibe, potentially simmialr to that of the decisions page, but more like box's login

let user = ref(null);
let error = ref(null);

let registerAnimationInterval = null;

function registerAnimation() {
  const registerButton = document.querySelector(".register-button");

  
  registerButton.style = "filter: saturate(1.5); brightness(0.95); cursor: not-allowed; text-align: left; padding-left: calc(50% - 50px);";
  registerButton.innerHTML = "Registering.";
  
  registerAnimationInterval = setInterval(() => {
    registerButton.style.transition = 'all 0.1s ease';
    setTimeout(() => {
      registerButton.style.height = "39px";
      registerButton.style.paddingTop = "0px";
      registerButton.innerHTML = "Registering.";
    }, 100);
    setTimeout(() => {
      registerButton.innerHTML = "Registering..";
    }, 200);
    setTimeout(() => {
      registerButton.innerHTML = "Registering...";
      registerButton.style.paddingTop = "8px";
      registerButton.style.height = "39px";
      
    }, 300);
    setTimeout(() => {
      registerButton.innerHTML = "Registering..";
    }, 800);
    setTimeout(() => {
      registerButton.innerHTML = "Registering...";
    }, 900);
    setTimeout(() => {
      registerButton.innerHTML = "Registering..";
    }, 1500);
    setTimeout(() => {
      registerButton.innerHTML = "Registering...";
    }, 1600);
  }, 2000);
}

async function register(email, password) {
  registerAnimation();
  error.value = "";
  try{
    await AccountLocal.create(
      ID.unique(),
      email,
      password,
    );
    console.log("User registered successfully");
    await AccountLocal.createEmailPasswordSession(email, password);
    console.log("Session created successfully");
    user.value = await AccountLocal.get();
    console.log("User data retrieved successfully:", user.value);
    console.log(`${apiUrl}users/create`);
    await axios.post(`${apiUrl}users/create`, {
      email: email,
      id: user.value.$id
    });
    console.log("User data sent to backend successfully");
    router.push("/account-setup");
  }catch(err){
    clearInterval(registerAnimationInterval);
    document.querySelector(".register-button").style = "text-align: center; padding-left: 0px;";
    document.querySelector(".register-button").innerHTML = "Register";
    if(err.message.includes("Email already exists")){
      error.value = "An account with this email already exists. Please log in or use a different email.";
    }else{
      error.value = err.message;
    }
    return;
  }finally{
    clearInterval(registerAnimationInterval);
    document.querySelector(".register-button").style = "text-align: center; padding-left: 0px;";
    document.querySelector(".register-button").innerHTML = "Register";
  }
}

onMounted(async () => {
  try{
    user.value = await AccountLocal.get();
    router.push("/");
  }catch(err){
    console.log("No active session found, staying on login page.");
  }
});

async function logout() {
  try{
    await AccountLocal.deleteSession("current");
    window.location.href = "/login";
  }catch(err){
    console.log("Error logging out", err);
  }
}

async function login(email, password) {
  try{
    await AccountLocal.createEmailPasswordSession(email, password);
    let userData = await AccountLocal.get();
    if(userData.isNew){
      router.push("/create");
    }else{
      router.push(`/auth/callback?redirect=${encodeURIComponent(route.query.redirect || "/")}`);
    }
  }catch(err){
    if(err.message.includes("Rate limit for")){
      error.value = "Too many login attempts. Please try again later.";
    }else{
      error.value = err.message;
    }
  }
}
async function forgetPassword(email) {
  try{
    await AccountLocal.createRecovery(email, `${domain}/password-reset`);
    error.value = "We've sent a password reset link to your email. If anything goes wrong, you can click the button again to resend a new reset link. If more problems persist, contact us.";
    document.querySelector("#error-text").style = "color:green";
  }catch(err){
    document.querySelector("#error-text").style = "color:red";
    if(err.message.includes("Email not found")){
      error.value = "No account found with this email. Please check the email or register for a new account.";
    }else{
      error.value = err.message;
    }
  }
}


// Doesnt allow signing out and sigingin back in, never tested if I can actually create a google account and get forwarded to the create page. 
// This still has to be fixed

async function loginWithGoogle() {
  AccountLocal.createOAuth2Session(
    "google",
    `${domain}auth/callback?redirect=${encodeURIComponent(route.query.redirect || "/")}`,
    `${domain}login`
  );
}
// Error logging out AppwriteException: User (role: guests) missing scopes (["account"])

let tab = ref("login");

async function goBackToLogin(){
  tab.value = "login";
  error.value = "";
  document.querySelector("#error-text").style = "color:red";
}

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
        <div class="outline" v-if="tab==='login'">
          <div class="login-header" @click="logout">Login to your account</div>
          <div class="login-gooogle-button" @click="loginWithGoogle"> <img class="google-icon"> </img>Sign in with Google</div>
          <div class="line"></div>
          <div class="or-word">or</div>
          <input v-model="email" class="input" placeholder="Email" />
          <input v-model="password" class="input" placeholder="Password" type="password" />
          <div style="width:100%;">
            <a @click="tab='forgot-password'; error=''" class="passwrod-forget-text">Forget Password</a>
          </div>
          
          <!--     
          <button @click="register(email, password, 'Optional Name')" class="input">Register</button> -->
          
          <button @click="login(email, password)" class="login-button">Login</button>
          
          <div class="error-log">{{error}}</div>
          <button class="register-text">Dont have an account? <a @click="tab='register'; error=''" class="register-link">Sign up</a></button>
          <!-- <button @click="register(email, password, 'Optional Name')" class="login-button">Register</button> -->


          <!-- this works, you cjust can't repeat the google emails you already have -->
        </div>
        <div class="outline" v-else-if="tab=='register'">
          <div class="login-header" style="margin-bottom:30px;">Register for an account</div>
          <!-- <div class="sub-text">
            By creating an account, you agree to our <a href="#" class="register-link">Terms of Service</a> and <a href="#" class="register-link">Privacy Policy</a>.
          </div> -->
          <input v-model="email" class="input" placeholder="Email" style="margin-top:10px;"/>
          <input v-model="password" class="input" placeholder="Password" type="password" />
          <div class="line" style="margin-bottom:30px; width:80%"></div>
          <button @click="register(email, password)" class="register-button">Register</button>
          <div class="error-log">{{error}}</div>
          <button class="register-text">Already have an account? <a @click="tab='login'; error=''" class="register-link">Sign in</a></button>
        </div>
        <div class="outline" v-else-if="tab=='forgot-password'">
          <div class="login-header" style="margin-bottom:20px;">Password Reset</div>
          <div class="sub-text">
            Enter your account's email address below, and we'll send you a link to reset your password.
          </div>
          <input v-model="email" class="input" placeholder="Email" style="margin-top:20px;"/>
          <button @click="forgetPassword(email)" class="register-button" style="margin-top:10px;">Send Reset Link</button>
          <div id="error-text" class="error-log">{{error}}</div>
          <button class="register-text"><a @click="goBackToLogin" class="register-link">Go back to login</a></button>
        </div>
      </div>
      
      <div class="logoBox">
        <img src="@/assets/logo.png"  class="apollo"/>
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
  max-width: 450px;
  width:calc(100vw - 60px);
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
