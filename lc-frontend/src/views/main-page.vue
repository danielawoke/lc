<script setup>
import { useRoute, useRouter } from 'vue-router'
import { onMounted, ref } from 'vue'
import Header from '@/components/header.vue'
import axios from 'axios'
const apiUrl = import.meta.env.VITE_APP_API_URL
const router = useRouter()
const route = useRoute()

let userCount = ref(0);

onMounted(async () => {
    fontAdjust();
    userCount.value = (await axios.get(apiUrl + "users/count")).data.user_count;

    document.querySelector(".background").addEventListener("scroll", (event) => {
        
        if(event.target.scrollTop + event.target.offsetHeight >= 1795){
            document.querySelector(".user-count").style.display = "none";   
            document.querySelector(".user-count-bottom").style.display = "block";
        }else{
            document.querySelector(".user-count").style.display = "block";
            document.querySelector(".user-count-bottom").style.display = "none";
        }
    });
})

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
    

function goToExplore(){
    router.push('/founderSpace/edit/a/a')
}


let projects = [
    { id: 1, name: 'Project Alpha', description: 'A revolutionary new app that changes everything.', location: "New York, NY", peopleCount: 5, clicks: 100 },
    { id: 2, name: 'Project Beta', description: 'An innovative platform for connecting people.', location: "San Francisco, CA", peopleCount: 3, clicks: 75 },
    { id: 3, name: 'Project Gamma', description: 'A cutting-edge solution for modern problems.', location: "Austin, TX", peopleCount: 7, clicks: 120 },
    { id: 4, name: 'Project Delta', description: 'A game-changing service that disrupts the market.', location: "Seattle, WA", peopleCount: 2, clicks: 50 },
]

let profiles = [
    { id: 1, name: 'Alice Johnson', location: "New York, NY", selfStatement: "CS + Math @ UMD", skills: ["Building Metalic Spheres", "Wood Burning", "Tree Removal", "Suprising"], inSearchOf: "Looking for a co-founder with expertise in marketing and business development." },
    { id: 2, name: 'Bob Smith', location: "San Francisco, CA", selfStatement: "Experienced software engineer with a passion for startups and innovation.", skills: ["Java", "Spring Boot", "SQL"], inSearchOf: "Looking for a co-founder with expertise in business development and marketing." },
    { id: 3, name: 'Charlie Brown', location: "Austin, TX", selfStatement: "Passionate about building impactful products and connecting with like-minded individuals.", skills: ["Python", "Django", "React"], inSearchOf: "Looking for a co-founder with expertise in design and user experience." },
    { id: 4, name: 'Diana Prince', location: "Seattle, WA", selfStatement: "Aspiring entrepreneur with a passion for technology and innovation.", skills: ["JavaScript", "Vue.js", "Node.js"], inSearchOf: "Looking for a co-founder with expertise in marketing and business development." },
]

function goToEdit() {
    router.push('/explore')
}

function goToProf(){
    router.push('/userview');
}

function login(){
    router.push('/login');
}

</script>


<!-- start with sales from now on -->
<!-- I created an app for finding college studnets to create companies with -->

<template>
    <Header />
    <div class="user-count">{{ userCount }} total users</div>
    <div class="background">
        
        <div class="container">
            <!-- <div class="prefacing-block-text">
                <div class="preface-elements-container">
                    <img class="banner-image" src="@/assets/main-page/ship-background-1.png" alt="Co-Founder Finder Logo" />
                    <img class="banner-image-outline" src="@/assets/main-page/ship-background-1.png" alt="Co-Founder Finder Logo" />
                    <div class="tunnel-outline" @click="goToEdit"> -->
                        <!-- Credit https://stackoverflow.com/questions/2717127/how-to-do-gradient-borders-in-css for gradient tunnel -->
                        <!-- <div class="tunnel">
                            <div class="sub-tunnel-cut">
                                <div class="sub-tunnel">
                                    <div class="darkest-center"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="create-proj-tunnel-caption">Click the tunnel to explore long shot projects and top talent!</div>
                </div>
            </div> -->
            <!-- <div class="split-screen">
                <div style="width:fit-content;margin:auto;">
                    <div class="left">
                        <div class="category-title">HOT PROJECTS 🔥</div>
                        <div class="project-list">
                            <span class="project-card" v-for="project in projects">
                                <div class="image-backdrop-project-card">
                                    <div class="project-top-container">
                                        <div class="project-title">
                                            {{ project.name }}
                                        </div>
                                        <div class="project-description">
                                            {{ project.description }}
                                        </div>
                                    </div>
                                    <div class="project-bottom-container">
                                        <div class="project-meta-section">
                                            <div class="meta-text">
                                                {{ project.clicks }} views
                                            </div>
                                            <div class="clicks-icon"></div>
                                        </div>
                                        <div class="project-meta-section">
                                            <div class="meta-text">
                                                {{ project.peopleCount }} people
                                            </div>
                                            <div class="people-count-icon"></div>
                                        </div>
                                        <div class="project-meta-section">
                                            <div class="meta-text">
                                                {{ project.location }}
                                            </div>
                                            <div class="location-icon"></div>
                                        </div>
                                    </div>
                                </div>
                            </span>
                        </div>
                    </div>
                    <div class="right">
                        <div style="width: fit-content; margin:auto;">
                            <div class="category-title">LOCAL TALENT</div>
                            <div class="project-list">
                                <span @click="goToProf" class="project-card" v-for="profile in profiles">
                                    <div class="profile-top-container">
                                        <div class="profile-title-section">
                                            <img class="profile-picture" src="@/assets/user-creation/default-profile.png" />
                                            <div class="profile-header">
                                                <div id="name-block" class="profile-name" style="margin-top:5px;">{{ profile.name }}  </div>
                                                <div class="profile-self-statement" style="margin-top:5px;">{{ profile.selfStatement }}</div>
                                            </div>
                                        </div>
                                        <div class="profile-skill-block">
                                            <div class="profile-skill" v-for="skill in profile.skills">
                                                {{ skill }}
                                            </div>
                                        </div>
                                        <div class="profile-insearch-of-block"><b>In search of:</b> {{ profile.inSearchOf }}</div>
                                    </div>
                                    <div class="profile-bottom-container">
                                        <div class="project-meta-section">
                                            <div class="meta-text">
                                                {{ profile.location }}
                                            </div>
                                            <div class="location-icon"></div>
                                        </div>
                                    </div>
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </div> -->
            <div>
                <div @click="goToEdit" class="search-block">
                    <div class="top-margin"></div>
                    <div class="wide-block">
                        <div class="galaxy">
                            Find someone to build your idea with, or join someone else's
                        </div>
                    </div>
                </div>
            </div>
            <div class="credit-box">
                <h2 style="margin-bottom:10px;">Credits:</h2>
                <div style="margin-left:10px;margin-bottom:10px;">Engineering and Design: Daniel Awoke</div>
                <div style="margin-left:10px;margin-bottom:10px;">Apollo Logo: Robert T. McCall </div>
                <div style="margin-left:10px; ">Star fall HTML/CSS backdrop: Saransh Sinha</div>
                <h2 style="margin-bottom:10px;">Contact:</h2>
                <div style="margin-left:10px; margin-bottom:10px;">contact@launchpad.land</div>
                <div style="margin-left:10px; margin-bottom:10px;">dawoke@terpmail.umd.edu</div>
                <div style="margin-left:10px">Please use this if you find any bugs that need to be reported</div>
                <h2 style="margin-bottom:10px;">Donations:</h2>
                <a style="margin-left:10px;" href="https://square.link/u/ltj1dIvZ">https://square.link/u/ltj1dIvZ</a>
            </div>
            <div class="user-count-bottom">{{ userCount }} total users</div>
            <div class="footer">
               Launch Pad &copy; 2026, All Rights Reserved
            </div>
        </div> 
        <div id="stars"></div>
        <div id="stars2"></div>
        <div id="stars3"></div>
    </div>
    
               
</template>
<style scoped>
.credit-box{
    padding:10px;
    height:450px;
    width:100vw;
    margin-top: -12px;
    background:rgba(0, 0, 0, 0.411);
    position: relative;
    color:white;
    font-family: Arial, Helvetica, sans-serif;
}
.sign-in-button:hover{
    filter: brightness(120%) hue-rotate(20deg);
    border: #ffffff solid 1px;
    transition: all 0.3s ease;
    box-shadow: 0 0 5px white;
}
.sign-in-button{
    background: rgba(0, 153, 255, 0);
    border: #ffffffb6 solid 1px;
    color:rgb(255, 255, 255);
    cursor: pointer;
    font-size: 12px;
    position:relative;
    padding: 6px 15px;
    font-family: Arial, Helvetica, sans-serif;
    border-radius: 15px;
    top:-12.5px;
    left:-25px;
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
    font-family: Arial, Helvetica, sans-serif;
    font-size: 14px;
    color:white;
    background: transparent;
    outline: none;
}
.search-box{

    display: inline-block;
    padding: 5px;
    width: calc(100% - 450px);
    font-size: 16px;
    border-radius: 5px;
    color:white;
    background:rgba(0, 0, 0, 0.104);
    border: solid white 1px;
    position:relative;
    top:-10px;
}
.top-header-container {
  display: flex;
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
  font-family: Arial, Helvetica, sans-serif;
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
  font-family: Arial, Helvetica, sans-serif;
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
  width: 35px;
  height: 35px;
  margin-top: -15px;
  cursor: pointer;
  margin-right: 25px;
  filter:invert(1);
}

.prof-header{
    background: linear-gradient(to bottom, rgb(0, 0, 0), rgb(0, 0, 0));
    padding:10px;
    height: fit-content;
}
.prof-icon{
    font-size:17px;
    font-family: Arial, Helvetica, sans-serif;
    padding:0px 0px;
    position: relative;
    border-radius:5px;
    color:white;
    margin:0px;
    margin-right:15px;
    margin-top:-2.5px;
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
  box-shadow: 5px 5px 15px 5px #1a1a1a;

}
.user-count-bottom{
    position: absolute;
    bottom: 100px;
    left: 20px;
    font-variant: normal;
    color: white;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 16px;
    z-index: 100;
    display: none;

}
.user-count{
    position: absolute;
    bottom: 20px;
    right: 20px;
    color: white;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 16px;
    z-index: 100;
}
.galaxy{
    height:300px;
    background-image: url("https://img1.picmix.com/output/stamp/normal/5/4/7/4/2384745_37f06.gif");
    background-size: contain;
    background-position: center;
    background-repeat: no-repeat;
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
    position: relative;
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
    font-family: Arial, Helvetica, sans-serif;
    font-size: 30px;
    text-align: center;
    margin:auto;
    margin-bottom: 30px;
    border-top: solid rgba(14, 14, 14, 0.479) 18px;
     transition: all 0.3s ease;
}
.profile-insearch-of-block{
    font-size: 12px;
    font-family: Arial, Helvetica, sans-serif;
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
    font-family: Arial, Helvetica, sans-serif;
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
    font-family: Arial, Helvetica, sans-serif;
    color: white;
    font-weight: normal;
    background:rgba(0, 0, 0, 0);
}
.profile-header{
    position: absolute;
    display:inline-block;
    color: white;
    font-family: Arial, Helvetica, sans-serif;
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
    font-family: Arial, Helvetica, sans-serif;
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
    font-family: Arial, Helvetica, sans-serif;
    font-size: 11px;
    margin-top: 10px;
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
    background-image: url('https://wallpapers.com/images/hd/kingdom-hearts-sora-1024-x-718-wallpaper-j3ztbn1r0o0b3ba3.jpg');
    background-size: cover;
    background-repeat: no-repeat;
    background-color: rgba(34, 56, 255, 0.6);
    box-shadow: inset 0px 0px 15px 5px #253bff99;
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
    width:calc(90vw - 40px);
    color: rgb(255, 255, 255);
    left:calc(50% - 0px);
    transform: translate(calc(-50% - 0px),0);
    font-family: Arial, Helvetica, sans-serif;
    font-size: 19px;
    font-weight: bold;
    z-index: 1;
    text-align: center;
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
    font-family: Arial, Helvetica, sans-serif;
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
    font-family: Arial, Helvetica, sans-serif;
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
    display: inline-block;
    margin: 20px auto;
    padding: 10px;
    width: calc(100% - 100px);
    font-size: 16px;
    border-radius: 5px;
    color:white;
    background:rgba(0, 0, 0, 0.104);
    border: solid white 1px;
    
}
.search-container{
    padding-top:80px;
    height:300px;
    margin:auto;
    width:60%;
    background: rgba(0, 0, 0, 0);
}
.extra-proj-button-border:hover{
    position: relative;
    display: block;
    margin: 0 auto;
    background: rgb(255, 211, 99);
    padding: 40px;
    width: calc(100% - 100px);
    font-family: Arial, Helvetica, sans-serif;
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
    font-family: Arial, Helvetica, sans-serif;
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
    font-family: Arial, Helvetica, sans-serif;
    color:white;
    text-shadow: 2px 2px 5px rgba(255, 255, 255, 0.627);
}
.project-list{
    margin:auto;
    width:750px;
    background-color: #ae000000;
}
.split-screen {
    width: calc(100% - 100px);
    background: rgba(0, 0, 0, 0.405);
    box-shadow: 0px -15px 15px 0px rgba(0, 0, 0, 0.405);
    padding:50px;
    margin-top: -50px;

}
.container{
    position: absolute;
    top:0;
    padding-top:50px;
    left:0;
    width: calc(100vw - 0px);
    margin:auto;
    height: auto;
    z-index: 1;
    background-color: rgba(255, 0, 0, 0);
    overflow-y: auto;
    overflow-x: hidden;
    -ms-overflow-style: none;  /* IE and Edge */
    scrollbar-width: none;
    
}
.container::-webkit-scrollbar {
    display: none; /* Chrome, Safari, Opera */
}


.background{
        position: absolute;
    top:0;
    padding-top:50px;
    left:0;
    width: 100vw;
    height: auto;
    z-index: -10;
    background-color: rgba(245, 0, 0, 0.526);
    overflow-y: auto;
    overflow-x:hidden;
}
.project-card{
    display:inline-block;
    background-image: linear-gradient(45deg, rgb(81, 98, 255),rgb(4, 125, 255));
    box-shadow: inset 0px 0px 15px 5px rgba(0, 0, 0, 0.463);
    padding: 10px;
    margin: 10px;
    border-radius: 15px;
    width:330px;
    height:200px;
    overflow: hidden;
}
.project-card:hover{
    background-image: linear-gradient(45deg, rgb(4, 125, 255), rgb(81, 98, 255));
    box-shadow: inset 0px 0px 25px 15px rgba(0, 0, 0, 0.663);
    cursor: pointer;
    transition: all 0.3s ease;
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

@media (1800px < width < 2300px) {
    .project-list{
        width:750px;
    }
}


@media (0px < width < 1000px) {
    .project-list{
        width:200px;
    }
}

@media only screen and (900px <= width < 1800px) {
    .left {
        position: relative;
        display: block;
        margin:auto;
        width: 100%;
    }
    .right {
        position: relative;
        display: block;
        margin:auto;
        width: 100%;
        margin-top: 20px;
        
    }
    .project-list{
        width:750px;
    }
}
@media only screen and (750px < width < 1300px) {
    .left {
        position: relative;
        display: block;
        margin:auto;
        width: 100%;
        background-color: rgba(240, 248, 255, 0);
    }
    .right {
        position: relative;
        display: block;
        margin:auto;
        width: 100%;
        background-color: rgba(240, 248, 255, 0);
        margin-top: 20px;
        
    }
    .project-list{
        width:750px;
    }
}
@media only screen and (0px < width <= 850px) {
    .left {
        position: relative;
        display: block;
        margin:auto;
        width: 100%;
        background-color: rgba(240, 248, 255, 0);
    }
    .right {
        position: relative;
        display: block;
        margin:auto;
        width: 100%;
        background-color: rgba(240, 248, 255, 0);
        margin-top: 20px;
        
    }
    .project-list{
        width:380px;
    }
}
</style>

<style lang="sass" scoped>

@function multiple-box-shadow ($n) 
  $value: '#{random(8000)}px #{random(8000)}px #FFF'
  @for $i from 2 through $n
    $value: '#{$value} , #{random(8000)}px #{random(8000)}px #FFF'

  @return unquote($value)

$shadows-small:  multiple-box-shadow(3100)
$shadows-medium: multiple-box-shadow(600)
$shadows-big:    multiple-box-shadow(300)

.background
  position: absolute;
  top:0;
  padding-top:50px;
  height: calc(100% - 50px);
  width: 100%
  background: radial-gradient(ellipse at bottom, #1B2735 0%, #090A0F 100%)
  overflow: auto;
  z-index: -10;
    
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
