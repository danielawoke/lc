<script setup>
import { useRoute, useRouter } from 'vue-router'
import ImageEditorPopUp from '@/components/founder-space/interfaces/edit-cards/image-replace/pop-up.vue';
import { ref} from 'vue';
import { nextTick, watch } from 'vue';
import { onMounted } from 'vue';
import { AccountLocal } from "@/lib/appwrite";
import axios from 'axios';
const apiUrl = import.meta.env.VITE_APP_API_URL;
useRoute();
const router = useRouter()
const route = useRoute();


let loadingAnimationInterval = null;


let verificationWorked = ref(0);

function nextLoading(button) {
  const registerButton = button;

  
  registerButton.style = "filter: brightness(0.80) contrast(1.2); cursor: loading; text-align: left; padding-left: 40px; width: 100px; ";
  registerButton.innerHTML = "Loading.";
  setTimeout(() => {
      registerButton.innerHTML = "Loading.";
    }, 100);
    setTimeout(() => {
      registerButton.innerHTML = "Loading..";
    }, 200);
    setTimeout(() => {
      registerButton.innerHTML = "Loading...";
    }, 300);
  
  loadingAnimationInterval = setInterval(() => {
    registerButton.style.transition = 'all 0.1s ease';
    setTimeout(() => {
      registerButton.innerHTML = "Loading.";
    }, 100);
    setTimeout(() => {
      registerButton.innerHTML = "Loading..";
    }, 200);
    setTimeout(() => {
      registerButton.innerHTML = "Loading...";
      
    }, 300);
    setTimeout(() => {
      registerButton.innerHTML = "Loading..";
    }, 800);
    setTimeout(() => {
      registerButton.innerHTML = "Loading...";
    }, 900);
    setTimeout(() => {
      registerButton.innerHTML = "Loading..";
    }, 1500);
    setTimeout(() => {
      registerButton.innerHTML = "Loading...";
    }, 1600);
  }, 2000);
}


onMounted(async () => {
    try{
        // let userObject = await AccountLocal.get();
        let data = route.query;
        await AccountLocal.updateVerification(data.userId, data.secret);
        verificationWorked.value = 0;
    }catch(err){
        verificationWorked.value = 1;
        router.push("/login");
    }
});


</script>
<template>
    <ImageEditorPopUp v-if="imageEditMode" :backDropClick="backDropClick" :saveResults="saveResults" :imageInfo="imageChangeInfo"/>
    <div class="background">
        <div class="zig-background">
            <div class="mid-container">
                <!-- make this more efficient and elegant -->
                <div class="forum-contaier">
                    
                        <!-- <div id="stars"></div> -->
                        <!-- <div id="stars2"></div>
                        <div id="stars3"></div>  -->
                    
                    <div class="center-title"><span class="logo-background"><span class="logo-image"></span></span></div>
                    <div class="scroll-box" v-if="verificationWorked==0">
                        <div style="height:30px;"></div>
                        <div class="content-container" >
                            <div style="overflow:auto; height:100%; width:100%">
                            <div class="usertag-block">
                                <div style="height:30px;"></div>
                                <div class="tag-block">
                                    <div class="tag-text">Verification confirmed! Go back to the account setup page and press next.</div>
                                </div>
                            </div>
                            </div>
                        </div>
                    </div>
                    <div class="scroll-box" v-if="verificationWorked==1">
                        <div style="height:30px;"></div>
                        <div class="content-container" >
                            <div style="overflow:auto; height:100%; width:100%">
                            <div class="usertag-block">
                                <div style="height:30px;"></div>
                                <div class="tag-block">
                                    <div class="tag-text">Verification failed, please resend the verification email and try again.</div>
                                </div>
                            </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>  
        </div> 
    </div>
    
</template>
<style scoped>
@keyframes shake {
    0% { transform: translate(1px, 1px) rotate(0deg); }
    10% { transform: translate(-1px, -2px) rotate(-1deg); }
    20% { transform: translate(-3px, 0px) rotate(1deg); }
    30% { transform: translate(3px, 2px) rotate(0deg); }
    40% { transform: translate(1px, -1px) rotate(1deg); }
    50% { transform: translate(-1px, 2px) rotate(-1deg); }
    60% { transform: translate(-3px, 1px) rotate(0deg); }
    70% { transform: translate(3px, 1px) rotate(-1deg); }
    80% { transform: translate(-1px, -1px) rotate(1deg); }
    90% { transform: translate(1px, 2px) rotate(0deg); }
    100% { transform: translate(1px, -2px) rotate(-1deg); }
}
@keyframes  gentleShake{
    0% { transform: translate(0px, 0px) }
    25% { transform: translate(-2px, -2px) }
    50% { transform: translate(2px, 0px)  }
    75% { transform: translate(-2px, 0px)  }
    100% { transform: translate(0px, 0px) }
}
.shake {
    animation: gentleShake 0.5s;
}

#error-message{
}
.tag-input{
    width:100%;
    max-width:360px;
    font-size:16px;
    margin-left:5px;
    border:none;
    outline:none;
    background:transparent;
    padding-bottom:5px;
    border-bottom: 1px black solid;
}
.tag-input-block{
    width:100%;
    max-width:400px;
    outline:none;
    margin-left:-5px;
    border-radius:10px;
    padding:5px;
}
.tag-text{
    font-family: fantasy;
    font-size: 16px;
    margin-bottom:10px;
}
.tag-block{
    display: block;
    margin:auto;
    margin-bottom: 20px;
    width: 85%;
    border-radius: 20px;
    padding:20px;
    background:rgba(255, 255, 255, 0.84);
}
.usertag-block{
}
.location-styling{
    border-radius:10px;
    width:100%;
    max-width:400px;
    
}
.logo-background{
    height:50px;
    width: 50px;
    position:relative;
    display:inline-block;
    top:0px;
    left:0px;
    padding:15px;
    margin:-29px;
    margin-right:-5px;
    margin-left:-50px;
    
    padding-bottom:21px;

    overflow:hidden;
    filter:saturate(0%);

    
    
}

.logo-image{
    width:60px;
    height:60px;
    position:absolute;
    top:12%;
    left:10%;
    background-image: url("@/assets/apollo8.png");
    background-size:cover;
    background-repeat: no-repeat;
    z-index:1000;
    
}
.mail-container{
    width:100%;
    height:100%;
    border-radius:50%;
    padding:40px;
    background: linear-gradient(45deg, rgba(173, 236, 255, 0.74), rgba(255, 255, 255, 0.74));
    box-shadow:  0 0 10px black;
    margin-left:20px;
}
.mail-prompt{
    display: inline-block;
    text-align: left;
    vertical-align: middle;
    height:fit-content;
    margin-right:20px;
    background:white;
    padding:20px;
    border-radius: 10px;
}
.mail-image{
    
    display: inline-block;
    width: 100%;
    height:100%;
}
.email-verify-block{
    display: flex;
    justify-content: center;
    gap:60px;
    width:100%;
}
.remove-popup{
    font-size: 14px;
    font-weight: bold;
    color: #00000093;
    cursor: pointer;
    font-family:fantasy;
    position: absolute;
    z-index: 7;
    background-color: rgb(80, 249, 255);
    padding: 15px;
    padding-left:10px;
    padding-top:10px;
    padding-bottom:5px;
    right:-5px;
    top:-5px;
    border-radius: 10px;
    float:right;
}
.pop-up{
    box-shadow: 0 0 10px #000000;
    position:absolute;
    top:0;
    right:0;
    max-width: 400px;
    width:100%;
    height: auto;
    padding:20px;
    margin:10px;
    border-radius: 20px;
    background:white;
    color:black;
    font-family: fantasy;
    overflow:hidden;
}
.zig-background{
    width:100%;
    height:100%;
    background-image: url("@/assets/user-creation/background-new-1.png");
    background-size: 1000px auto;
    background-repeat: repeat;
}
.selected-tab{
    display: inline-block;
    color: rgb(255, 139, 110);
    font-family: fantasy;
    font-size: 14px;
    margin-right: 20px;
    text-decoration-thickness: 2px;
    
    background:black;
    padding:10px;
    border-radius:15px;


}
.sub-title{
    font-family: fantasy;
    font-size: 25px;
    color: white;
    text-shadow: 2px 2px 4px #000000;
    position: relative;
    font-weight: bold;
    width:fit-content;
    width:85%;
    margin: auto;
    padding-left:0px;
    text-align: left;
    font-family: fantasy;
    margin-bottom:40px;
    margin-top:20px;
}
.center-title{
    font-family: fantasy;
    font-size: 40px;
    color: rgb(255, 255, 255);
    background: linear-gradient(45deg, rgba(255, 109, 31, 0.95), rgba(255, 109, 31, 0.74));
    position: relative;
    font-weight: bold;
    margin:auto;
    padding:20px;
    padding-left:50px;
    font-family: fantasy;
}
.tabs{
    width:90%;
    padding: 20px;
    margin:auto;
    background: linear-gradient(to top, transparent, rgba(132, 0, 255, 0));
}
.tab{
    display: inline-block;
    color: white;
    font-family: fantasy;
    font-size: 14px;
    margin-right: 20px;
    background:black;
    padding:10px;
    border-radius:15px;
}
.create-button{
    width:fit-content;
    width:130px;
    text-align: center;
    padding:10px;
    font-family: fantasy;
    border-radius: 5px;
    color:rgb(255, 255, 255);
    font-weight: bold;
    box-shadow: inset 0 0px 5px rgba(0, 0, 0, 0.596);
    background:rgb(88, 91, 255);
    position:absolute;
    top:5px;
    right:10px;
    
}
.terms-of-use-box{
    margin:auto;
    width:calc(95% - 60px);
    height: 450px;
    background-color: white;
    border: 1px solid white;
    border-radius: 5px;
    padding:30px;
    box-shadow: inset 0 0px 10px rgba(0, 0, 0, 0.8);
    color:black;
    font-family: fantasy;
    overflow-y: auto;
}
.invalid{
    width:30px;
    height:20px;
    color:red;
    padding:5px;
    border-radius:50%;
    font-size:25px;
    margin-left:10px;
    margin-bottom:-20px;
}
.valid{
    width:30px;
    height:20px;
    color:green;
    padding:5px;
    border-radius:50%;
    font-size:25px;
    margin-left:10px;
    margin-bottom:-20px;
}
.sub-link{
    font-family: fantasy;
    margin-right:20px;
    margin-top:10px;
    color:white;
    background:blue;
    border-radius:15px;
    box-shadow: 0 0 5px black;
    padding:10px;
}

.scroll-box{
    width:100%;
    height:100%;
}
.button-container{
    position: relative;
    display: block;
    justify-content: flex-end;
    width:95%;
    margin-bottom:200px;
    padding:10px;
    bottom:0;
    margin:auto;

}
.next-button{
    float:right;
    right:10px;
    bottom:0;
    text-align: center;
    width:fit-content;
    padding:10px;
    width:130px;
    font-family: fantasy;
    border-radius: 5px;
    background:rgb(255, 255, 255);
    border: rgb(121, 201, 255) 3px solid;
    box-shadow: inset 0 0px 5px rgba(0, 0, 0, 0.596);
    
    
}

.add-block{
    display: inline-block;
    width: 10px;
    margin-left: 12px;
    background-color: rgb(255, 255, 255);
    filter: hue-rotate(200deg);
    padding:10px;
    height:1px;
    padding-top:14px;
    padding-bottom:14px;
    color:rgb(0, 0, 0);
    border: 1px solid black;
    text-align: center;
    line-height: 0;
    font-size: 20px;
    border-radius: 5px;
    cursor: pointer;
    font-weight: bold;
    text-decoration: 10px 10px 5px rgb(0, 0, 0);
}
.image{
    width: auto;
    height: auto;
    
    max-height: 100%;
}
.image-space {
    outline: auto;
    display: flex;
    justify-content: left; 
    align-items: left;
    width: 25vw;
    max-width: 150px;
    aspect-ratio: 1 / 1;
    background-color: transparent;
    overflow: hidden;
    position: relative;
    z-index: 6;
    margin-top:20px;
    border-radius: 50%;
}
.image-edit-faint {
    outline: auto;
    width: 25vw;
    max-width: 150px;
    max-height: 150px;
    position: absolute;
    z-index: 5;
    opacity: 0;
    color:rgba(255, 255, 255, 0.205);
    background-color: rgb(26, 26, 26);
    padding: 100px;
    z-index: 0;
    transition: background-color 0.3s, opacity 0.3s;
}
.image-edit-faint:hover {
    opacity: 1.0;
    cursor: pointer;
    background-color: rgba(0, 0, 0, 0.842);
}

.forum-contaier{
    width:100%;
    height:calc(100% - 0px);
    min-height: 500px;
    display:block;
    margin: auto;
    box-shadow: inset 0 10px 20px rgb(0, 0, 0);
    overflow:hidden;
}
.content-container{
    width:85%;
    max-width: 900px;
    margin:auto;
    height:calc(100% - 20px);
    margin-top:-30px;
    position:relative;
    
    background:rgba(0, 0, 0, 0);
}
@media (max-width: 1000px) {
    .content-container{
        width:100%;
    }
}
.mid-container{
    width:100%;
    margin-top: -50px;
    padding-top:50px;
    height:calc(100%);
    box-shadow: inset 0 0 10px 10px #0000007a;
    background-image: radial-gradient(circle, rgba(73, 73, 73, 0) 30%, rgba(255, 255, 255, 0.25) 70%);
    overflow: auto;
    opacity: 1;
}
.remove-x{
    font-size: 17px;
    font-weight: bold;
    margin-left: 5px;
    color: #ffffff;
    cursor: pointer;
    font-family:fantasy;
}

.skill{
    display: inline-block;
    background-color: #0ed9c800;
    filter: hue-rotate(200deg);
    padding:10px;
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.664);
    color: rgb(0, 0, 0);
    border-radius: 10px;
    margin-right: 10px;
    margin-bottom: 10px;
    border: 1px solid #ffffff;
    font-family: fantasy;
}
.skills-block{
    display: block;
    background-color:#ffffff00;
    filter: hue-rotate(200deg);
    padding:15px;
    box-shadow: 0 10px 20px rgba(255, 255, 255, 0.295);
    border-radius: 10px;
    font-size: 14px;
    font-family: fantasy;
}
.skill-input{
    width: calc(100% - 30px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.452);
    max-width: 300px;
    border:none;
    outline:auto;
    border-radius: 5px;
    padding: 2px;
    padding-left: 10px;
    font-size: 16px;
    background-color: transparent;
    color: rgb(0, 0, 0);
}
.text-input{
    width: calc(100% - 30px);
    max-width: 400px;
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0);
    border:none;
    outline:auto;
    padding: 2px;
    padding-left: 10px;
    border-radius:5px;
    font-size: 16px;
    background-color: rgba(255, 255, 255, 0);

    color: rgb(0, 0, 0);
}
.text-area-input{
    width: calc(100% - 30px);
    max-width: 400px;
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.452);
    border:none;
    border-radius: 5px;
    padding: 2px;
    height:60px;
    resize: none;
    font-family: fantasy;
    padding-left: 10px;
    font-size: 16px;
    outline:auto;
    background-color: transparent;
    color: rgb(0, 0, 0);
}
.question-block{
    display: block;
    margin:auto;
    margin-bottom: 20px;
    width: 85%;
    border-radius: 20px;
    padding:20px;
    background:linear-gradient(45deg, rgba(255, 255, 255, 0.84), rgba(255, 255, 255, .84));
}
.text{
    font-size: 16px;
    font-family: fantasy;
    margin-bottom: 10px;
    color: rgb(0, 0, 0);
}
.scrollable-background{
    width:100%;
    height:100%;
    background-size: 700px auto;
    background-repeat: repeat;
    
}
.el-container{
    display: block;
    
    margin: auto;
    width:calc( 100% - 140px );
    max-width: 1200px;
    background: url("@/assets/user-creation/dots-light.png");
    background-color: rgba(0, 0, 0, 0.918);
    background-size: 2000px auto;
    background-repeat: repeat;
    padding: 70px;
    padding-top:180px;
    height: 10000px;
  box-shadow: 0 0 200px 400px #000000a2; 
}
.copy-right{
    font-family: fantasy;
    font-size: 10px;
    position: absolute;
    top:35px;
    left: 85px;
    color: #ffffff9f;
    padding: 10px;
}
.title{
    font-family: fantasy;
    font-size: 25px;
    color: rgb(255, 255, 255);
    text-shadow: 2px 2px 4px #000000;
    position: absolute;
    font-weight: bold;
    top: 0px;
    left: 90px;
    transform: translateY(12px) ;
}
.logo-icon-background{
  width:45px;
  height:45px;
  background: rgb(255, 255, 255);
  border-radius: 50px;
  position: absolute;
  margin-top: 8px;
  margin-left: 25px;
  /* whatever the dominant color of what is on the inside, should match the color of this */
  border: 2px solid rgb(227, 155, 78);
  background-image: linear-gradient(45deg, rgb(255, 109, 31), rgb(255, 221, 165)); 
  filter: contrast(100%);
  overflow: hidden;
}

.logo {
  display: inline-block;
  width: 45px; 
  /*80px is the original size, so 50px is a good size for the logo in the header*/
  height: 45px;
  filter:saturate(0);
  
}

.header{
    position: absolute;
    top:0;
    left:0;
    width:100vw;
    height:70px;
    background-image: linear-gradient(to bottom, rgb(0, 0, 0), rgb(17, 17, 17));
    box-shadow: 0 5px 50px rgba(0, 0, 0, 0.89);
    z-index: 1;
}
.background{
    position: fixed;
    top:0;
    left:0;
    width:100vw;
    height:100vh;
    background: linear-gradient(45deg, #050008 10%, hsl(234, 100%, 43%) 90%);
    background-color: rgb(0, 0, 0);
    display:flex;
    justify-content:center;
    align-items:center;
}
</style>


<style lang="sass" scoped>

@function multiple-box-shadow ($n) 
  $value: '#{random(6000)}px #{random(6000)}px #FFF'
  @for $i from 2 through $n
    $value: '#{$value} , #{random(6000)}px #{random(6000)}px #FFF'

  @return unquote($value)

$shadows-small:  multiple-box-shadow(2100)
$shadows-medium: multiple-box-shadow(600)
$shadows-big:    multiple-box-shadow(300)

.forum-contaier

    
#stars
  width: 1px
  height: 1px
  background: transparent
  box-shadow: $shadows-small
  z-index: -1;
  animation			: animStar 50s linear infinite
    
  &:after
    content: " "
    position: absolute
    top: 2000px
    width: 1px
    height: 1px
    z-index: -1;
    background: transparent
    box-shadow: $shadows-small
    
#stars2
  width: 2px
  height: 2px
  background: transparent
  box-shadow: $shadows-medium
  animation			: animStar 100s linear infinite
  z-index: -1;
    
  &:after
    content: " "
    position: absolute
    top: 2000px
    width: 2px
    height: 2px
    background: transparent
    box-shadow: $shadows-medium
    z-index: -1;
    
#stars3
  width: 3px
  height: 3px
  background: transparent
  box-shadow: $shadows-big
  z-index: -1;
  animation			: animStar 150s linear infinite
    
  &:after
    content: " "
    position: absolute
    top: 2000px
    width: 3px
    height: 3px
    background: transparent
    box-shadow: $shadows-big
    z-index: -1;

#title
  position: absolute
  top: 50%
  left: 0
  right: 0
  
  color: #FFF
  text-align: center
  font-family: 'lato',sans-serif
  font-weight: 300
  font-size: 50px
  letter-spacing: 10px
  
  margin-top: -60px
  padding-left: 10px
  
  span
    background: -webkit-linear-gradient(white, #38495a)
    -webkit-background-clip: text
    -webkit-text-fill-color: transparent
    
@keyframes animStar
  from	
    transform: translateY(0px)
  to		
    transform: translateY(-2000px)
    
</style>
