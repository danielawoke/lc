<script setup>
import { useRoute, useRouter } from 'vue-router'
import { onMounted, ref } from 'vue'
import dayjs from 'dayjs';
import Header from '@/components/header.vue';
import locationDatabase from '@/components/supporting-components/location-explore.vue';
import { AccountLocal } from '@/lib/appwrite';
import axios from 'axios';
const apiUrl = import.meta.env.VITE_APP_API_URL


const router = useRouter()
const route = useRoute()
let user = ref(null);
let loaded = ref(false);
onMounted(async () => {
    let currentUserTag = ref(null);
    try{
        user.value = await AccountLocal.get();
        user.value = await AccountLocal.get();
        await axios.get(`${apiUrl}users/search/full_profile/${user.value.$id}`).then((response) => {
            currentUserTag.value = response.data.profile[0].user_tag;
        }).catch((error) => {
            console.error("Error fetching user data:", error);
        });
    }catch(e){
        console.log("Error fetching user:", e);
    }
    if(currentUserTag.value == route.params.usertag){
        await axios.get(`${apiUrl}projects/load/admin/${currentUserTag.value}`).then((response) => {
            projects.value = response.data.projects;
        }).catch((error) => {
            console.error("Error fetching user projects:", error);
        });
    }else{
        await axios.get(`${apiUrl}projects/load/public/${route.params.usertag}`).then((response) => {
            projects.value = response.data.projects;
        }).catch((error) => {
            console.error("Error fetching user projects:", error);
        });
    }
    loaded.value = true;
    fontAdjust();
    adjustListWidth();
    adjustHeaderContainerSize();
    window.addEventListener('resize', adjustListWidth);
    window.addEventListener('resize', adjustContainerHeight);
    window.addEventListener('resize', adjustHeaderContainerSize);

});

function adjustHeaderContainerSize(){
    
}

function adjustListWidth(){
    let projectList = document.getElementById("proj-list");
    console.log(window.innerWidth);
    let pixelWidth = 375 * Math.floor(window.innerWidth / 375);
    projectList.style.width = (pixelWidth) + "px";
}

function fontAdjust(){
    let profileNames = document.getElementsByClassName("profile-name");
    for (let profileName of profileNames) {
        let height = profileName.offsetHeight;
        let fontSize = 20;
        while(height > 40){
            profileName.style.fontSize = fontSize + "px";
            height = profileName.offsetHeight;
            fontSize-=2;
        }
    }
}
    


let projects = ref([]);


function adjustContainerHeight(){
    let block = document.querySelector(".result-screen");
    block.style.height = "fit-content";
    let height1 = block.offsetHeight;
    block.style.height = "calc(100vh - 0px)";
    let height2 = block.offsetHeight;
    if(height1 > height2){
        block.style.height = height1 + "px";
    }
}



</script>



<!-- start with sales from now on -->
<!-- I created an app for finding college studnets to create companies with -->

<template>
        <Header />

    
   
    <!-- <div class="background"> -->
        <div class="container">
             
            <div class="result-screen">
                <div style="width:fit-content;margin:auto;">
                    <!-- <div class="category-title"></div> -->
                    <div id="proj-list" style="margin:auto;">
                        
                            <div v-if="projects.length === 0 && loaded" style="margin: 30px; font-size:18px; font-family:Arial, Helvetica, sans-serif">No projects found.</div>
                            <span  v-for="project in projects">
                                <span class="project-card" @click="router.push('/project-edit/'+project.project_id+'/edit')">
                                    <div class="image-backdrop-project-card" :style="'background-image: url(' + project.project_page?._value.mainCard.image + ');'">
                                        <div class="project-top-container">
                                            <div style="width:100%; position:absolute; right:0; top:-100px;padding-top:100px; font-style:italic; ">
                                                <div style="font-size:12px;margin-top:5px" class="project-title">
                                                    {{ project.project_page?._value.mainCard.title }}
                                                </div>
                                                <div class="project-description">
                                                    {{ project.settings.description }}
                                                </div>
                                            </div>
                                        </div>
                                        <div class="project-bottom-container">
                                            <div class="project-meta-section">
                                                <div class="meta-text">
                                                    last edited {{ dayjs(project.last_edit_time).format('M/D/YYYY') }}
                                                </div>
                                                <div class="date-icon"></div>
                                            </div>
                                            <div class="project-meta-section">
                                                <div class="meta-text">
                                                    {{ project.members_info.length }} people
                                                </div>
                                                <div class="people-count-icon"></div>
                                            </div>
                                            <div class="project-meta-section">
                                                <div v-if="!project.settings.remove_physical_locations" class="meta-text">
                                                    {{ project.project_page?._value.mainCard.location }}
                                                </div>
                                                <div v-else class="meta-text">
                                                    Remote
                                                </div>
                                                <div  v-if="!project.settings.remove_physical_locations" class="location-icon"></div>
                                                <span v-if="project.settings.remote_friendly && !project.settings.remove_physical_locations" style="color:white; width:39px; margin-bottom: -12.5px;"> + <img src="https://cdn-icons-png.flaticon.com/512/3759/3759392.png" style="width:15px; height:15px; margin-bottom:-0.5px;"></span>
                                                <span v-else-if="project.settings.remote_friendly" style="color:white; width:19px; margin-bottom: -12.5px;"><img src="https://cdn-icons-png.flaticon.com/512/3759/3759392.png" style="width:15px; height:15px; margin-bottom:-0.5px;"></span>
                                            </div>
                                        </div>
                                    </div>
                                </span>
                            </span>
                        <!-- </span> -->
                    
                        
                    <!-- <span class="load-more-card">
                        <div class="load-more-text">+<br/>LOAD MORE</div>
                    </span> -->
                    </div>
                </div>
                </div>
            </div>
    <!-- </div> -->
               
</template>
<style scoped>
.image-backdrop-project-card{
    
    width:calc(100% - 20px);
    height:calc(100% - 20px);
    background-size: cover;
    background-repeat: no-repeat;
    background-color: rgba(0, 0, 0, 0.6);
    box-shadow: inset 0px 0px 15px 5px #00000099;
    padding:10px;
    background-position: center;
    background-blend-mode: overlay;
}
.project-card{
    display:inline-block;
    background-image: linear-gradient(45deg, rgb(255, 255, 255),rgb(255, 255, 255));
    box-shadow: inset 0px 0px 15px 5px rgba(0, 0, 0, 0.463);
    padding: 10px;
    margin: 10px;
    border-radius: 15px;
    width:330px;
    height:200px;
    overflow: hidden;
}
.project-card:hover{
    background-image: linear-gradient(45deg, rgb(255, 255, 255),rgb(255, 255, 255));
    box-shadow: inset 0px 0px 25px 15px rgba(12, 12, 12, 0.76);
    cursor: pointer;
    transition: all 0.3s ease;
}

.project-card:hover .project-top-container{
    background-color: rgba(0, 0, 0, 0.405);
    box-shadow: 0px 0px 15px 100px rgba(0, 0, 0, 0.405);
    cursor: pointer;
    transition: all 0.3s ease;
}

.project-card:hover .card-header{
    cursor: pointer;
}

.profile-drop-down-button{
    font-family: fantasy;
    font-size: 14px;
    color: rgb(0, 0, 0);
    display:block;
    width:100%;
    padding:10px;
}
.profile-drop-down-button:hover{
    color: rgb(133, 133, 133);
    cursor: pointer;
}
.profile-drop-down{
    width: 300px;
    height: 260px;
    position:absolute;
    right:20px;
    top:60px;
    border-radius: 10px;
    background:white;
    z-index: 100;
    overflow:hidden;
    box-shadow: 0px 0px 10px rgb(0, 0, 0);
    animation: fadeIn 0.1s ease;
}
.notification-title{
    font-family: fantasy;
    font-size: 14px;
    color: rgb(0, 0, 0);
}
.notification-drop-down{
    width: 500px;
    height: 400px;
    position:absolute;
    right:140px;
    top:60px;
    border-radius: 10px;
    background:white;
    z-index: 100;
    overflow:hidden;
    box-shadow: 0px 0px 10px rgb(0, 0, 0);
    animation: fadeIn 0.1s ease;
}
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}
.remove{
    width: 15px;
    height: 15px;
    background: rgb(0, 0, 0);
    color: white;
    font-family: fantasy;
    font-size: 10px;
    border-radius: 50%;
    text-align: center;
    line-height: 15px;
    right: 5px;
    top: 5px;
    float:right;
    cursor: pointer;
}
.settings:hover{
    filter: invert(1) brightness(130%) saturate(0%);
    transform: rotate(90deg);
}
.settings{
    width:30px;
    height:30px;
    background-image: url("@/assets/profile-page/gear.webp");
    background-size: 90% 90%;
    background-position: center;
    background-repeat: no-repeat;
    margin-top:10px;
    margin-right: 15px;
    float:right;
    cursor: pointer;
    filter: invert(1) brightness(200%) saturate(0%);
    background-color: rgb(255, 255, 255);
    transition: all 0.3s ease;
}
.clear-button{
    font-family: fantasy;
    font-size: 14px;
    color: rgb(255, 255, 255);
    display:inline-block;
    width: fit-content;
    margin-left: 15px;
    margin-bottom: -20px;
    position:relative;
    top:12px;
    padding:5px;
    border-radius: 10px;
    background: rgb(12, 89, 255);
}
.clear-button:hover{
    filter: invert(1) brightness(150%) hue-rotate(90deg);
    cursor: pointer;
}
.bottom-bar{
    width: 100%;
    height: 50px;
    background: rgb(0, 0, 0);
    border-top: 1px solid rgba(255, 255, 255, 0);
}
.message-sender-drop-down{
    font-family: fantasy;
    font-size: 14px;
    color: rgb(0, 0, 0);
    display:inline-block;
    width: calc(100% - 60px);
    background:rgba(0, 0, 0, 0);
    height:30px;
    margin-left: 10px;
    margin-bottom: -20px;
    position:relative;
    top:-20px;
    
}
.notifcation-drop-down-profile-picture{
    width: 30px;
    
    display:inline-block;
    height: 30px;
    border-radius: 50%;
    background-image: url("@/assets/default-profile-invert.png");
    background-size: cover;
    background-position: center;
    margin-bottom: 5px;
}
.message-item{
    border-bottom: 1px solid rgba(0, 0, 0, 0.1);
    padding: 10px;
}
.proj-title{
    font-family: fantasy;
    font-size: 15px;
    color: rgb(0, 0, 0);
}
.sub-title{
    font-family: fantasy;
    font-size: 14px;
    font-weight: bold;
    color: rgb(0, 0, 0);
}
.message-content{
    font-family: fantasy;
    font-size: 14px;
    color: rgb(0, 0, 0);
}
.message-drop-down{
    width: 500px;
    height: 400px;
    position:absolute;
    right:70px;
    top:60px;
    border-radius: 10px;
    background:white;
    z-index: 100;
    overflow:hidden;
    box-shadow: 0px 0px 10px rgb(0, 0, 0);
    animation: fadeIn 0.1s ease;
}
.message-notif-amount{
    width: 20px;
    height:20px;
    background:rgb(255, 0, 0);
    color: white;
    border-radius: 50%;
    position:absolute;
    bottom:7px;
    margin-left:50px;
    font-family: fantasy;
    font-weight:bold;
    font-size:12px;
    text-align: center;
    cursor: pointer;
}
.notif-amount{
    width: 20px;
    height: 20px;
    background:rgb(255, 0, 0);
    color: white;
    border-radius: 50%;
    position:absolute;
    bottom:7px;
    margin-left:-5px;
    font-family: fantasy;
    font-weight:bold;
    font-size:12px;
    text-align: center;
    
    cursor: pointer;

}
.drop-down-entry:hover{
    filter: invert(1) brightness(150%) hue-rotate(90deg);
    cursor: pointer;
}
.drop-down-entry{
    display: block;
    padding: 5px 5px;
    font-family: fantasy;
    background: rgb(71, 89, 255);
    border: 2px solid rgba(255, 255, 255, 0);
    box-shadow: rgb(0, 0, 0) 0px 0px 10px;
    color:rgb(255, 255, 255);
    font-size: 14px;
    margin-left: -5px;
    border-radius: 5px;
    cursor: pointer;
    margin-top:3px;
}
.drop-down-menu{
    position: relative;
    width: fit-content;
    height: fit-content;
    background: rgba(0, 0, 0, 0);
    border-radius: 5px;
    padding-left:12px;
    padding-right:12px;
    margin-left:-12px;
    margin-right:-12px;
    padding-bottom:6px;
    margin-bottom: -6px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
    border-top: none;
    display: block;
    z-index: 0;
}
.dropdown-icon{
    width:15px;
    height:15px;
    margin-left:5px;
    margin-bottom:-3.5px;
    background-image: url("https://cdn-icons-png.freepik.com/512/5800/5800629.png");
    transform: rotate(-90deg);
    float:right;
    transition: all 0.3s ease;
}

.selected{
    color:rgb(255, 187, 0) !important; /* Darker color */
    text-decoration-thickness: 3px; /* Thicker line */
    text-underline-offset: 5px;
}

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

}

.search-enter-button{
    width: 20px;
    height: 20px;
    filter:invert(1);
    background-image: url("@/assets/search.png");
    background-size: cover;
    background-position: center;
    display: inline-block;
    margin-left: 10px;
    cursor: pointer;
    position:absolute;
}
.search-input{
    width: calc(100% - 40px);
    border: none;
    color: white;
    font-family: fantasy;
    font-size: 14px;
    color:white;
    background: transparent;
    outline: none;
}
.search-box{
    display: inline-block;
    padding: 5px;
    width: calc(100% - 45px);
    font-size: 16px;
    border-radius: 5px;
    color:white;
    background:rgba(0, 0, 0, 0.104);
    border: solid white 1px;
    position:relative;
    top:-0px;
    left:10px;
}
.notification{
    width: 32px;
    height: 32px;
    margin-top: -15px;
    cursor: pointer;
    margin-right: 25px;
    filter:invert(1);
}
.profile-top-image{
    border-radius:50%;
    border: solid 2px rgba(255, 255, 255, 0.521);
    width: 35px;
    height: 35px;
    margin-top: -15px;
    cursor: pointer;
    margin-right: 25px;
}
.messages{
  width: 35px;
  height: 35px;
  margin-top: -15px;
  cursor: pointer;
  margin-right: 25px;
  filter:invert(1);
}
.top-header-container {
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
  margin-top: -15px;
  margin-left:10px;
  /* whatever the dominant color of what is on the inside, should match the color of this */
  border-radius: 50%;
  border: 2px solid rgb(109, 69, 27);
  background-color: rgb(247, 193, 118);
  background-image: linear-gradient(45deg, rgb(255, 109, 31), rgb(255, 221, 165));
}
.title-top-header{
  position:absolute;
  display: inline-block;
  font-family: fantasy;
  font-size: 20px;
  color: rgb(232, 232, 232);
  margin-left: 15px;
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

.prof-header{
    background: linear-gradient(to bottom, rgb(0, 0, 0), rgb(0, 0, 0));
    padding:10px;
    height: fit-content;
}
.prof-icon:hover{
    filter: brightness(80%);
    cursor: pointer;
}
.prof-icon{
    font-size:14px;
    font-family: fantasy;
    position: relative;
    display:inline-block;
    color:white;
    margin:0px;
    margin-top: -0px;
    margin-bottom:15px;
    margin-right:10px;
    border-right: rgba(255, 255, 255, 0) 1px solid;
}
.settings-button{
    width: 30px;
    height: 30px;
    background-image: url("@/assets/profile-page/gear.webp");
    background-size: cover;
    margin-top:-10px;
    
    margin-left: 0px;
    float:right;
    margin-right: 10px;
    cursor: pointer;
}
.time-text{
    font-family: fantasy;
    font-size: 12px;
    margin-left:15px;
    color: rgb(255, 255, 255);
}
.outline-container{
    display:inline-block;
    width: 370px;
    margin: 10px;
    height: 300px;
    border-radius: 20px;
    background: rgb(0, 0, 0);
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}
.remote-drop-down-menu{
    position: relative;
    float:left;
    width: fit-content;
    height: fit-content;
    background: rgb(255, 84, 84);
    padding-left:12px;
    padding-right:12px;
    margin-left:-12px;
    margin-right:-12px;
    padding-bottom:6px;
    margin-top:5px;
    margin-bottom: -6px;
    color: rgb(224, 224, 224);
    border-radius: 5px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
    z-index: 9999;
}
.remote-button:hover{
    background:rgb(0, 0, 0);
    filter: brightness(200%);
    cursor: pointer;
}
.remote-button{
    display: inline-block;
    padding: 2px 5px;
    width:25%;
    font-family: fantasy;
    text-align: center;
    background: rgb(255, 30, 30);
    
    border: 2px solid rgba(255, 255, 255, 0);
    box-shadow: rgb(0, 0, 0) 0px 0px 10px;
    color:rgb(255, 255, 255);
    font-size: 12px;
    border-radius: 5px;
}
.slider{
    width: 100%;

}
.dropdown-icon{
    width:15px;
    height:15px;
    margin-left:5px;
    margin-bottom:-3.5px;
    background-image: url("https://cdn-icons-png.freepik.com/512/5800/5800629.png");
    transform: rotate(-90deg);
    float:right;
    transition: all 0.3s ease;
}
.logo-icon-background{
   width:80px;
   height:80px;
    background: rgb(255, 255, 255);
    border-radius: 50px;
  position: absolute;
  margin-top: 10px;
  margin-left: 25px;
  /* whatever the dominant color of what is on the inside, should match the color of this */
  border: 4px solid rgb(227, 155, 78);
  background-image: linear-gradient(45deg, rgb(255, 109, 31), rgb(255, 221, 165)); 
  filter: contrast(100%);
  overflow: hidden;
}

.search-options{
    position: absolute;
    top:90px;
    width:100%;
    height:auto;

}
.drop-down-option:hover .dropdown-icon{
    filter: invert(1) brightness(150%);
    transform: rotate(0deg);
}
.drop-down-option{
    display: inline-block;
    padding: 5px 10px;
    font-family: fantasy;
    background: rgb(0, 0, 0);
    border: 1px solid rgba(255, 255, 255, 0.945);
    box-shadow: rgb(0, 0, 0) 0px 0px 10px;
    color:rgb(255, 255, 255);
    font-size: 14px;
    border-radius: 5px;
    margin-left: 20px;
    margin-top:3px;
    position: relative;
    cursor: pointer;
    z-index: 9999;
}
.select-option{
    display: inline-block;
    padding: 5px 10px;
    font-family: fantasy;
    background: rgb(71, 89, 255);
    border: 2px solid rgba(255, 255, 255, 0);
    box-shadow: rgb(0, 0, 0) 0px 0px 10px;
    color:rgb(255, 255, 255);
    font-size: 14px;
    border-radius: 5px;
    margin-left: 20px;
    cursor: pointer;
    margin-top:3px;
}
.load-more-text{
    color: rgba(255, 255, 255, 0.575);
    text-shadow: 2px 2px 0px rgba(0, 0, 0, 0.575);
    font-family: fantasy;
    font-size: 25px;
    font-weight: lighter;
    text-align: center;
    margin-top:65px;
}
.load-more-card:hover{
    background: rgba(221, 221, 221, 0.2);
    color: rgba(255, 255, 255, 0.9);
    text-shadow: 2px 2px 10px rgba(0, 0, 0, 0.8);
    cursor: pointer;
    box-shadow: inset 0px 0px 10px 10px rgba(0, 0, 0, 0.178);
}
.load-more-card{
    display:inline-block;
    border: dashed rgba(255, 255, 255, 0.671) 2px;
    padding: 10px;
    margin: 10px;
    border-radius: 15px;
    width:330px;
    height:200px;
    overflow: hidden;
}
.search-interface{
    position:absolute;
    width:100%;
    height:130px;
    top:0px;
    left:0;
    z-index: 0;
    background: rgb(0, 0, 0);
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.308);
}
.result-screen{
    position: absolute;
    top:0;
    width:100%;
    height:fit-content;
    padding-top:0px;
}
.galaxy{
    height:300px;
    width:300px;
    background-image: url("https://img1.picmix.com/output/stamp/normal/5/4/7/4/2384745_37f06.gif");
    background-size: contain;
    background-position: center;
    margin:auto;
    margin-top:-50px;
}
.bottom-margin{
    height: 10px;
    width:100%;
    background: #001f42;
    box-shadow: 0px -5px 5px 5px rgba(3, 3, 3, 0.616);
}
.top-margin{
    width:100%;
    height: 30px;
    background: linear-gradient(to top, rgba(0, 0, 0, 0.514), rgb(0, 0, 0));
    box-shadow: 0px -5px 5px 5px rgba(0, 0, 0, 0.11);
}
.search-block{
    height: 500px;
    background: radial-gradient( ellipse at center, rgba(94, 158, 255, 0.582) 5%, rgba(0, 0, 0, 0.767) 95%);
    font-variant: small-caps;
    color: white;
}
.search-block:hover .top-margin{
       
    background: linear-gradient(to top, rgba(0, 0, 0, 0.938), rgba(0, 0, 0, 0.856));
    box-shadow: 0px -5px 5px 5px rgba(0, 0, 0, 0.329);
}
.search-block:hover .wide-block{
    background: rgba(0, 0, 0, 0.405);
    font-variant: small-caps;
    color: white;
    cursor: pointer;
    box-shadow: inset 0px 0px 20px 10px rgba(0, 0, 0, 0.664);
    text-shadow: 2px 2px 10px rgb(255, 255, 255);
    font-size: 31px;
    border-top: solid rgba(0, 0, 0, 0.562) 8px;
    border-bottom: solid rgba(0, 0, 0, 0.8)  8px;
    filter: brightness(140%);
        
}
.wide-block{
    width: calc(100%);
    background: rgba(0, 21, 77, 0.267);
    box-shadow: inset 0px -15px 15px 0px rgba(0, 0, 0, 0.405);
    padding-top:90px;
    padding-bottom:100px;
    color:white;
    font-family: fantasy;
    font-size: 30px;
    text-align: center;
    margin:auto;
    margin-bottom: 30px;
    border-top: solid rgba(14, 14, 14, 0.479) 18px;
     transition: all 0.3s ease;
}
.profile-insearch-of-block{
    font-size: 12px;
    font-family: fantasy;
    color: white;
    font-weight: normal;
    background:rgba(0, 0, 0, 0);
    margin-top: 10px;
    height:35px;
}
.profile-skill-block{
    height:60px;
    background-color: rgba(0, 0, 0, 0);
}
.profile-skill{
    display: inline-block;
    background-color: rgba(255, 255, 255, 0.2);
    color: white;
    font-family: fantasy;
    font-size: 10px;
    padding: 5px 10px;
    border-radius: 20px;
    margin-right: 5px;
    margin-top: 10px;
}
.profile-name{
    background: rgba(0, 0, 0, 0);
}
.profile-self-statement{
    font-size: 10px;
    font-family: fantasy;
    color: white;
    font-weight: normal;
    background:rgba(0, 0, 0, 0);
}
.profile-header{
    position: absolute;
    display:inline-block;
    color: white;
    font-family: fantasy;
    font-size: 18px;
    width: 240px;
    height:80px;
    background-color: #001ee000;
    font-weight: bold;
    text-shadow: 2px 2px 5px rgba(0, 0, 0, 0);
}
.profile-picture{
    display:inline-block;
    position: relative;
    width: 80px;
    height: 80px;
    margin-right:5px;
    border-radius: 50%;
    box-shadow: 0px 0px 20px rgba(0, 0, 0, 0);
}
.profile-title-section{
    width: 100%;
    height: 80px;
    background-color: rgba(0, 0, 0, 0);;
}
.profile-bottom-container{
    width:calc(100%);
    height:15%;
    padding-left: 40px;
    padding-right: 40px;
    margin-left: -40px;
    background:rgba(0, 0, 0, 0);
    box-shadow: inset 0px 0px 15px 5px rgba(0, 0, 0, 0);
    position: relative;
}
.profile-top-container{
    position: relative;
    width: calc(100%);
    height: 90%;
    background: rgba(0, 0, 0, 0);
}
.people-count-icon{
    width: 15px;
    height: 15px;
    background-image: url('@/assets/main-page/people.png');
    background-size: cover;
    display: inline-block;
    margin-bottom: -10px;
    margin-right: 5px;
    filter: saturate(0%) invert(1); 
}
.date-icon{
    width: 15px;
    height: 15px;
    background-image: url('https://static.thenounproject.com/png/133028-200.png');
    background-size: cover;
    display: inline-block;
    margin-bottom: -10px;
    margin-right: 5px;
    filter: saturate(0%) invert(1); 
}
.clicks-icon{
    width: 15px;
    height: 15px;
    background-image: url('@/assets/main-page/views.png');
    background-size: cover;
    display: inline-block;
    margin-bottom: -10px;
    margin-right: 5px;
    filter: saturate(0%) invert(1); 
}
.project-meta-section{
    display: flex;
    align-items: center;
    height:18px;
}
.meta-text{
    width: calc(100% - 20px);
    text-align: right;
    display: inline-block;
    color: white;
    font-family: fantasy;
    font-size: 11px;
    margin-top: 10px;
    margin-right:5px;
}
.location-icon{
    width: 15px;
    height: 15px;
    background-image: url('@/assets/main-page/location.png');
    background-size: cover;
    display: inline-block;
    margin-bottom: -10px;
    margin-right: 5px;
    filter: saturate(0%) invert(1); 
}
.project-bottom-container{
    width:calc(100%);
    height:50%;
    padding-left: 40px;
    padding-right: 40px;
    margin-left: -40px;
    background:rgba(0, 0, 0, 0.487);
    box-shadow: inset 0px 0px 15px 5px rgba(0, 0, 0, 0.463);
    position: relative;
}   
.project-top-container{
    position: relative;
    width: calc(100%);
    height: 77%;
    background: rgba(0, 0, 0, 0);
}
.project-description{
    color: white;
    font-family: fantasy;
    font-size: 11px;
    margin-top: 10px;
}
.project-title{
    color: white;
    font-family: fantasy;
    font-size: 13px;
    font-weight: bold;
    text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.7);
}

.tunnel-outline{
    
}
.sub-tunnel-cut{
}
.tunnel:hover .sub-tunnel-cut{
}
.tunnel:hover .sub-tunnel{
    
    transform: translate(15%,30%) scale(1.1);
    background-image: linear-gradient(to bottom, #008caf 10%, #001ee0 90%);
    border: 2px solid rgba(255, 255, 255, 0.422);
    filter:brightness(50%);
    box-shadow: inset 0px 0px 25px 15px rgba(0, 25, 70, 0.729);
    transition: all 1s ease;
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

.sub-tunnel{
    position: absolute;
    margin: 0 auto;
    width: 77%;
    height: 75%;
    border-radius: 50%;
    z-index: 0;
    bottom:0px;
    box-shadow: inset 0px 0px 15px 3px rgba(0, 184, 216, 0.193);
    border: 2px solid rgba(0, 0, 0, 0);
    background:rgb(0, 0, 0);
    transform: translate(15%,40%);
    overflow: hidden;
}
.preface-elements-container{
    width: 100%;
    margin:auto;
}
.tunnel:hover .darkest-center{
    transition: all 1s ease;
    transform: translate(28%,0px);
    z-index: 20;
    background-image: linear-gradient(to bottom, #008caf 10%, #001ee0 90%);
    border: 2px solid rgba(255, 255, 255, 0.422);
    filter:brightness(20%);
    box-shadow: inset 0px 0px 25px 15px rgba(0, 25, 70, 0.729);
    transition: all 1s ease;
}
.darkest-center{
    position: absolute;
    margin: 0 auto;
    width: 62%;
    height: 50%;
    
    transform: translate(28%,0px);
    border-radius: 50%;
    bottom:2px;
    background: rgb(0, 0, 0);
    box-shadow: inset 0px 0px 15px 5px rgba(0, 0, 0, 0.729);
    z-index: -10;
}
.tunnel:hover{
    background-image: linear-gradient(to bottom, #008caf 10%, #001ee0 90%);
    cursor: pointer;
    box-shadow: inset 0px 0px 25px 15px rgba(0, 25, 70, 0.729);
    transition: all 1s ease;
    border:rgba(255, 255, 255, 1) solid 15px;
    transform: translate(-60%,0) scale(1.05);
    filter:contrast(100%) saturate(150%) brightness(150%) hue-rotate(-25deg);
}
.tunnel{
    position: absolute;
    display: block;
    margin: 0 auto;
    width: 25%;
    max-width:305px;
    aspect-ratio: 2.5 / 1;
    border-radius: 50%;
    z-index: 0;
    bottom:100px;
    background-image: linear-gradient(to bottom, #3acfd5 10%, #4f5fc1 90%);
    border: 15px solid rgb(0, 0, 0);
    box-shadow: inset 0px 0px 35px 5px rgba(0, 0, 0, 0.845);
    left:50%;
    transform: translate(-60%,0);
    overflow: hidden;
    
}
.create-proj-tunnel-caption{
    position: absolute;
    bottom: 50px;
    left:calc(50% - 220px);
    color: rgb(255, 255, 255);
    font-family: fantasy;
    font-size: 19px;
    font-weight: bold;
    z-index: 1;
}
.banner-image-outline{
    pointer-events: none; 
    display: block;
    width: 100%;
    max-width: 1200px;
    position: absolute;
    left:50%;
    top:50%;
    transform: translate(-50%, calc(-50% + 2px));
    z-index: 9;
    background: rgba(255, 255, 255, 0);
    filter:invert(1);
}

.banner-image{
    pointer-events: none; 
    display: block;
    margin: 0 auto;
    width: 100%;
    max-width: 1200px;
    position: relative;
    transform: translate(0,0);
    z-index: 10;
    background: rgba(255, 255, 255, 0);
}
.prefacing-block-text{
    
    width:calc(100% - 0px);
    height:fit-content;
    margin: auto;
    padding-top:100px;
    padding-bottom:100px;
    filter:brightness(150%);
    

}
.footer{
    width:calc(100% - 40px);
    position: absolute;
    bottom:0;
    text-align: left;
    padding: 20px;
    background-color: rgb(0, 0, 0);
    color:white;
    font-family: fantasy;
    font-size: 16px;
    padding-top:30px;
    margin-top:40px;
}
.preface-search-text{
    text-align: left;
    font-weight: lighter;
    text-decoration: underline;
    color:rgb(255, 255, 255);
    font-size: 20px;
    font-family: fantasy;
    margin-bottom: 10px;

}
.search-button{
    background: rgb(255, 254, 250);
    border: #00000000 solid 1px;
    border-radius: 10%;
    color:rgb(255, 255, 255);
    cursor: pointer;
    font-size: 20px;
    width:40px;
    height:40px;
    margin-left: 20px;
    margin-bottom: 5px;
    vertical-align: middle;
    z-index: 1;
    display:inline-block;
}
.search{
    position: absolute;
    top:20px;
    left:130px;
    padding:6px;
    padding-left:10px;
    width: calc(100% - 400px);
    font-size: 16px;
    border-radius: 5px;
    color:rgb(0, 0, 0);
    background:rgb(117, 107, 255);
    border: 2px solid rgba(255, 255, 255, 0);
    box-shadow: inset 0px 0px 10px rgba(0, 0, 0, 0.2);
    
}
.search-container{
    padding-top:80px;
    height:300px;
    margin:auto;
    background: rgba(0, 0, 0, 0);
}
.extra-proj-button-border:hover{
    position: relative;
    display: block;
    margin: 0 auto;
    background: rgb(255, 211, 99);
    padding: 40px;
    width: calc(100% - 100px);
    font-family: fantasy;
    font-weight: bold;
    text-shadow: 5px 5px 10px rgb(0, 0, 0);
    font-size: 33px;
    text-align: center;
    border: 10px solid rgb(255, 189, 102);
    color:rgb(255, 255, 255);
    box-shadow: inset 0 0 30px 30px rgb(255, 169, 40);
}
.create-proj-button:hover{
    background: rgb(255, 220, 133);
    text-shadow: 10px 10px 20px rgb(0, 0, 0);
    border: 10px solid rgb(255, 191, 71);
    color:rgb(255, 255, 255);
    cursor: pointer;
    font-size: 30px;
}
.extra-proj-button-border{
    position: relative;
    display: block;
    margin: 0 auto;
    background: goldenrod;
    padding: 40px;
    width: calc(100% - 100px);
    height:50px;
    font-family: fantasy;
    font-weight: bold;
    text-shadow: 5px 5px 10px rgb(0, 0, 0);
    font-size: 30px;
    text-align: center;
    border: 10px solid rgb(255, 145, 0);
    color:white;
    box-shadow: inset 0 0 20px 20px rgb(192, 109, 0);
    transition: all 0.3s ease;
}
.create-proj-button{
  background: rgb(255, 201, 63);
    text-shadow: 10px 10px 20px rgb(0, 0, 0);
    border: 10px solid rgb(255, 175, 25);
    color:rgb(255, 255, 255);
    cursor: pointer;
}
.prefacing-block-text{
    margin-bottom: 50px;
}
.category-title{
    text-align: center;
    font-weight: bold;
    margin: auto;
    font-size: 20px;
    margin-bottom: 30px;
    font-family: fantasy;
    color:white;
    text-shadow: 2px 2px 5px rgba(255, 255, 255, 0.627);
}
.project-list{
    margin:auto;
}

.container{
    position: absolute;
    padding-top:100px;
    right:0;
    top:60px;
    width: calc(100vw);
    height: calc(100vh - 160px);
    z-index: -10;
    overflow-y: auto;
    background: radial-gradient(circle, rgb(64, 0, 148), rgb(147, 16, 255));
    box-shadow: inset 0px 0px 20px 10px rgba(0, 0, 0, 0.5);
}

.left {
    display: inline-block;
    width: 50%;
    max-width: 1200px;

}
.right {
    display: inline-block;
    width: 50%;
    max-width: 1200px;
    background-color: rgba(240, 248, 255, 0);
}






.switch-toggle {
   float: left;
   background: black;
   border-radius: 2px;
   width: 90px;
}
.switch-toggle input {
  position: absolute;
  opacity: 0;
  width: 30%;
}
.switch-toggle input + label {
  padding: 10px;
  float:left;
  color: black;
  cursor: pointer;
}
.switch-toggle input:checked + label {
  background: red;
  border-radius: 50%;
}

.numberDiv {
  width: 90px;
  display: flex;
  padding-left: 10px;
  }
 
 .numberDiv p {
   width: 30%;
   }


.project-bottom-container{
    width:calc(100%);
    height:50%;
    padding-left: 40px;
    padding-right: 40px;
    margin-left: -40px;
    margin-top: -10px;
    background:rgba(0, 0, 0, 0.487);
    box-shadow: inset 0px 0px 15px 5px rgba(0, 0, 0, 0.463);
    position: relative;
    z-index: 1000;
}   
.project-top-container{
    position: relative;
    width: calc(100%);
    height: 77%;
    background: rgba(0, 0, 0, 0);
    z-index: 100;
}
.project-description{
    color: rgb(255, 255, 255);
    font-family: Arial, Helvetica, sans-serif;
    font-size: 11px;
    margin-top: 5px;
}
.project-title{
    color: white;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 13px;
    font-weight: bold;
    text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.7);
}
.image-backdrop-project-card{
    
    width:calc(100% - 20px);
    height:calc(100% - 20px);
    background-size: cover;
    background-repeat: no-repeat;
    background-color: rgba(0, 0, 0, 0.6);
    box-shadow: inset 0px 0px 15px 5px #00000099;
    padding:10px;
    background-position: center;
    background-blend-mode: overlay;
}
.tunnel-outline{
    
}
.sub-tunnel-cut{
}
.tunnel:hover .sub-tunnel-cut{
}
.tunnel:hover .sub-tunnel{
    
    transform: translate(15%,30%) scale(1.1);
    background-image: linear-gradient(to bottom, #008caf 10%, #001ee0 90%);
    border: 2px solid rgba(255, 255, 255, 0.422);
    filter:brightness(50%);
    box-shadow: inset 0px 0px 25px 15px rgba(0, 25, 70, 0.729);
    transition: all 1s ease;
}


.logo-icon-background:hover {
    box-shadow: 0px 0px 10px 2px #ffffffea;
    filter:contrast(120%) saturate(0);
    transition: all 0.3s ease;
    cursor: pointer;
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


</style>






<!--


<span  @click="PopulaceToggleDropDown" id="populace-categorical-tab" class="drop-down-option" style="z-index:4;">
                <span id="populace-categorical-tab-text">
                    For You
                </span>
                <span>
                    <img class="dropdown-icon" src="https://cdn-icons-png.freepik.com/512/5800/5800629.png"/>
                </span>
                <div id="populace-categorical-tab-drop-down" style="display:none;">
                    <div class="drop-down-menu">
                        <div style="height:5px"></div>
                        <div @click="populaceSelected" class="drop-down-entry">For You</div>
                        <div @click="populaceSelected" class="drop-down-entry">Recent</div>
                        <div @click="populaceSelected" class="drop-down-entry">Hot</div>
                        <div @click="populaceSelected" class="drop-down-entry">Most Popular</div>
                    </div>
                </div>
            </span>
            <span id="populace-categorical-tab-spacing"></span>
             <span @click="remoteToggle" id="remote-tab" class="drop-down-option" style="z-index:3;" >
                <span id="remote-text">
                    Remote <img src="https://cdn-icons-png.flaticon.com/512/3759/3759392.png" style="width:15px; height:15px; margin-bottom:-2.5px;">
                </span>
            </span>
            <span  @click.self="LocationToggleDropDown" id="location-tab" class="drop-down-option" style="z-index:2;">
                <span @click.self="LocationToggleDropDown" id="location-text">
                    New York, Ny
                </span>
                <span>
                    <img @click.self="LocationToggleDropDown" class="dropdown-icon" src="https://cdn-icons-png.freepik.com/512/5800/5800629.png"/>
                </span>
                <div id="location-tab-drop-down" style="display:none;">
                    <div class="drop-down-menu">
                        <div style="height:10px;"></div>
                            <locationDatabase />
                        <div id="location-width-adjust" style="height:10px; white-space: nowrap;opacity:0;">
                            
                        </div>
                        <input @click="locationConsiderationToggle" type="checkbox" :checked="!locationConsideration[0]" id="remote-only-checkbox" style="margin-right:5px;"/>
                        <label for="remote-only-checkbox" style="font-family: fantasy; font-size: 12px; color:white;">Dont consider physical locations</label>
                        <div style="height:5px;"> </div>
                    </div>
                </div>
            </span>

            <span id="location-tab-spacing"></span>
            <span  @click.self="DistanceToggleDropDown" id="distance-tab" class="drop-down-option" style="z-index:0;">
                <span id="distance-text" style="position:relative;">
                    {{ distance+" mi" }}
                </span>
                <span>
                    <img @click.self="DistanceToggleDropDown" class="dropdown-icon" src="https://cdn-icons-png.freepik.com/512/5800/5800629.png"/>
                </span>
                <div id="distance-tab-drop-down" style="display:none;">
                    <div class="drop-down-menu" style="width:140px; z-index: 9999;">
                        <div style="height:10px;"></div>
                        <input type="range" min="1" max="50" :value="distance" @input="updateDistance" class="slider" id="distance-range-input">
                        <div style="height:10px;"></div>
                    </div>
                </div>
            </span>
            <span id="distance-tab-spacing"></span>
            
            
            
-->


