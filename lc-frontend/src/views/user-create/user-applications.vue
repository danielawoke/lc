<script setup>
import { useRoute, useRouter } from 'vue-router'
import { nextTick, onMounted, watch } from 'vue';
import { AccountLocal } from '@/lib/appwrite';
import { ref } from 'vue';
import popUp from '@/views/user-create/popup/candidate-popup.vue';
import Header from '@/components/header.vue';
import dayjs from 'dayjs';
import axios from 'axios';
const apiURL = import.meta.env.VITE_APP_API_URL;
useRouter(); 
useRoute();

// convert this into a list of elements instead of this


let feedback = ref([]);
let applications = ref([
    // {jobTitle: "Software Engineer", projectTitle: "Project Alpha", status: "Under Review", timeposted: "2026-06-25 10:30:00.000000+00"},
]);

let filteredJobs = ref(applications.value);


let candidatePopup = ref([false]);
let popupData = ref({});
let selectedId = ref(0);
let scrollable = ref(['auto']);

onMounted(async () => {
    let user = await AccountLocal.get();
    await axios.get(`${apiURL}users/applications/load/${user.$id}`).then((response) => {
        console.log(response.data);
        applications.value = response.data.applications;
        filteredJobs.value = response.data.applications;
    });
    await nextTick();
    fontAdjust();
})

function filterJobs(search){
    filteredJobs.value = applications.value.filter(application => {
        if(!application.application_object?.job || !application.project_name){
            return false;
        }
        return application.application_object.job.toLowerCase().includes(search.toLowerCase()) || application.project_name.toLowerCase().includes(search.toLowerCase());
    });
    fontAdjust();
}

function fontAdjust(){
    for (let element of document.getElementsByClassName("profile-name")) {
        console.log(element.offsetHeight);
        let fontsizeChange = 10;
        while (element.offsetHeight > 60) {
            element.style.fontSize = fontsizeChange + "px";
            fontsizeChange -= 2;
        }
    }
    for (let element of document.getElementsByClassName("role-description")) {
        let fontsizeChange = 13;
        element.style.fontSize = fontsizeChange + "px";
        while (element.offsetHeight > 50) {
            element.style.fontSize = fontsizeChange + "px";
            fontsizeChange -= 2;
        }
    }
    for( let element of document.getElementsByClassName("prev-name")){
        let fontsizeChange = 14;
        element.style.fontSize = fontsizeChange + "px";
        while (element.offsetHeight > 25) {
            element.style.fontSize = fontsizeChange + "px";
            fontsizeChange -= 2;
        }
    }
    for( let element of document.getElementsByClassName("larger-prev-name")){
        let fontsizeChange = 13;
        element.style.fontSize = fontsizeChange + "px";
        while (element.offsetHeight > 60) {
            element.style.fontSize = fontsizeChange + "px";
            fontsizeChange -= 2;
        }
    }
    for( let element of document.getElementsByClassName("role-info")){
        let fontsizeChange = 13;
        element.style.fontSize = fontsizeChange + "px";
        while (element.offsetHeight > 25) {
            element.style.fontSize = fontsizeChange + "px";
            fontsizeChange -= 2;
        }
    }
}

let currId = ref([]);
let currJobs = ref([]);

let currIndex = ref(0);

async function openCandidatePopup(application, index){
    popupData.value = application;
    currIndex.value = index;
    candidatePopup.value[0] = true;
    await nextTick();
    document.getElementById('popup-backdrop').style.top = document.getElementById("application-container").scrollTop + 'px';
    document.getElementById('popup').style.top = document.getElementById("application-container").scrollTop + 'px';
}

let rejectAllPopup = ref([false]);
let selectedJob = ref([]);

</script>

<template>

    
    <Header />
    <popUp v-if="candidatePopup[0]" :renderVar="candidatePopup" :scrollable="scrollable" :candidate="popupData" :applications="{'true': applications, 'filtered': filteredJobs}" :id="currId" :index="currIndex"/>
    <div class="background">
        <div class="applications-container">
            <input id="search-input" class="job-search" placeholder="Search by project or job title..." v-model="search" @input="filterJobs(search)" />
            <div style="overflow-y:auto; height: calc(100% - 30px);">
                <div v-for="(application, index) in filteredJobs" class="decision-row" @click="openCandidatePopup(application, index)">
                    <div class="job-header">
                        {{application.application_object.job}}<span style="font-style: italic; font-weight: normal; color: #555;"> - {{application.project_name}}</span>
                    </div>
                    <div class="text-container">
                        <div class="status-text">{{application.status}}</div>
                        <div class="date-text">{{ dayjs(application.date_created).format('YYYY/M/D') }}</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
</template>
<style scoped>
.text-container{
    position: relative;
    bottom:-2px;
    height:25px;
}
.date-text{
    font-family: sans-serif;
    font-size: 14px;
    color:#555555;
    text-align: left;
    padding-bottom: 10px;
    position: absolute;
    right:0;
}
.status-text{
    font-family: sans-serif;
    font-size: 14px;
    color:#555555;
    text-align: left;
    padding-bottom: 10px;
    position: absolute;
    left:0;
}
.proj-title{
    font-family: sans-serif;
    font-size: 16px;
    color:#555555;
    text-align: left;
    padding-bottom: 10px;
    top:5px;
}
.background{
    height:calc(100vh - 60px);
    position: absolute;
    top:60px;
    left: 0;
    width: calc(100vw);
    z-index: -2;
    background: radial-gradient(circle, rgb(145, 137, 255), rgb(78, 214, 255), rgb(54, 31, 255));
}
.applications-container{
    position: relative;
    margin:auto;
    top:-0px;
    max-width: 1000px;
    padding-left:30px;
    padding-right:30px;
    background:rgba(255, 255, 255, 0.486);
    box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.425);
    padding-top:20px;
    padding-bottom:20px;
    height: calc(100% - 40px);
}
.nothing-for-now-image{
    width: auto;
    height: 140px;
    display:block;
    margin:auto;
    width:100%;
    max-width: 1200px;
    filter: invert(0);
    opacity: .1;
}
.no-results-text{
    font-family: sans-serif;
    font-size: 18px;
    color:#0000001a;

    text-align: center;
    vertical-align: middle;
    
    margin:auto;
    margin-top:40px;
    margin-bottom:-60px;
    position:relative;
    font-variant: small-caps;
}
.select{
    width: 20px;
    height: 20px;
    border-radius: 5px;
    background-color: #00000000;
    border: rgba(0, 0, 0, 0.562) solid 2px;
    position: absolute;
    top: 10px;
    right: 10px;
    margin-right: -40px;
    cursor: pointer;

}

.reject-text-button{
    color:#d4d4d4;
    cursor: pointer;
    font-weight: bolder;
    opacity: 1;
}
.gentle{
    color: #555555;
}
.harsh{
    color: rgb(92, 92, 92);
    text-decoration: solid underline rgb(214, 214, 214) 1px;
}
.role-with-select{
    width:200px;
    height:100px;
    margin-left:10px;
    margin-right:10px;
    padding:10px;
    display: inline-block;
    position: relative;
    float: left;
    border-left: #068fff62 solid 5px;
    border-right: #bbecff44 solid 35px;
    border-radius: 10px;
    box-shadow: 10px 0px 5px rgba(0, 0, 0, 0.164);
    background-color: #ffffff;
}
.sub-text-reject{
    font-family: sans-serif;
    font-size: 16px;
    color:#7ab1be;
    padding-right: 10px;
    padding-top: 10px;
    margin-right: 10px;
    margin-top: 5px;
    margin-bottom:-10px;
    text-shadow: none;
    font-weight: normal;
    max-width:500px;
}
.button{
    display: inline-block;
    padding: 10px 20px;
    margin: 10px;
    font-size: 14px;
    color: #333;
    background-color: #fff;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.1);
    font-family: fantasy;
}
.left-adjust{
    width:80%;
    margin-left:10%;
}
.element{
    display: block;
    font-family: sans-serif;
    font-size: 16px;
    color:#000000;
    text-align: center;
    padding-right: 10px;
    margin-right: 10px;
    vertical-align: middle;
    float: left;
    height: 10px;
    box-shadow: #00000000 0px 0px 10px;
}
.sigil-border{
    width: fit-content;
    height: fit-content;
    overflow: hidden;
    border-radius: 50%;
}
.center-sigil{
    width: 120px;
    height: 120px;
    padding: 180px;
    background-color: #ffffff;
    background-image: url('@/assets/founder-space/decisions/stars.png');
    background-repeat: cover;
    box-shadow: #00000080 0px 0px 30px;
    filter: invert(1);
}
.top-header-container{
    display: flex;
    width: calc(100%);
    height: 50px;
    background-color: #00000000;
    margin:auto;
    height:300px;
    justify-content: center;
    align-items: center;
    border-bottom: rgba(0, 0, 0, 0) solid 5px;
    margin-bottom: 100px;
    box-shadow: #00000080 0px 0px 30px;
    background-image: url('@/assets/founder-space/decisions/stars.png');
    background-repeat: repeat-x;
    overflow:hidden;
}
.top-bottom-text-container{
    display: block;
    background-color: #ffffff;
    width: calc(100%);
    position: absolute;
    top: 280px;
    margin: auto;
    height: 33px;
    padding-top: 10px;
    box-shadow: inset #00000000 0px 0px 30px;
}
.mid-dot{
    width: 10px;
    height: 10px;
    border-radius: 5px;
    background-color: #00ccff5d;
    position: absolute;
    margin:auto;
    top: 140px;
}
.prev-name{
    font-family: sans-serif;
    font-size: 12px;
    text-align: left;
    margin-top: 5px;
    margin-bottom: 5px;
    margin-top: 2px;
    overflow: hidden;
    color: #1d1d1dd0; 
    font-weight: lighter;
    white-space: wrap;
}
.profile-image{
    width: 40px;
    height: 40px;
    border-radius: 25px;
    border: rgba(0, 0, 0, 0.562) solid 2px;
    background-color: #00000000;
    float: left;
    margin:10px;
    margin-top: -10px;
    margin-left: 0;
    background-image: url('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT92rRF-vK8i3JSSCvn_oAcCqzD_lOmJa_--Q&s');
    background-size: contain;
    filter: invert(1);
}
.role-title{
    white-space: wrap;
    display: inline-block;
    font-family: sans-serif;
    font-size: 16px;
    font-weight: bold;
}
.role-description{
    white-space: wrap;
    font-family: sans-serif;
    font-size: 12px;
    text-align: left;
    margin-top: 5px;
    overflow: hidden;
    text-break: break-word;
}
.role-info{
    white-space: wrap;
    font-family: sans-serif;
    font-size: 12px;
    text-align: left;
    margin-top: 3px;
    overflow: hidden;
    text-break: break-word;
}
.role-title{
    white-space: wrap;
    display: inline-block;
    font-family: sans-serif;
    font-size: 16px;
    font-weight: bold;
}
.role-description{
    white-space: wrap;
    font-family: sans-serif;
    font-size: 12px;
    text-align: left;
    margin-top: 5px;
    overflow: hidden;
    text-break: break-word;
}
.element {
  position: fixed;
  bottom: 0;
  right: 0;
}
.job-search{
    background-color: #ffffffce;
    margin: auto;
    margin-top:5px;
    margin-bottom:5px;
    padding:10px;
    width:calc(100% - 20px);
    border: none;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.164);
}
.jobs-search-container{
    width: 100%;
    margin:auto;
    outline: none;
    background-color: #0066ff88;
    box-shadow: #00000080 0px 0px 30px;
    border-radius: 0  0 10px 10px;
    margin-bottom: 20px;
    position: sticky;
    top:0;
}
.job-header{
    font-family: Arial, sans-serif;
    font-size: 18px;
    font-weight: bold;
    text-shadow: 2px 2px 5px #00000000;
    color:#000000;
}
.meta-button-bottom-left{
    font-family:fantasy;
    font-size: 16px;
    text-align: left;
    margin-left: 10px;
    float: left;
    cursor: pointer;
    background-color: #06acee00;
}
.meta-text-bottom-right{
    font-family: sans-serif;
    font-size: 16px;
    color:#555555;
    text-align: right;
    padding-right: 10px;
    padding-bottom: 10px;
    margin-right: 10px;
    
    text-decoration: solid underline #b9b9b986 1px;
    
}
.text-container{
    text-align: right;
    margin:auto;
    
}
.line{
    background-color: #0099ff;
    border: none;
    height: 5px;
    margin:auto;
}
.decision-row{
    background-color: #ffffffa2;
    margin: auto;
    margin-top:5px;
    margin-bottom:5px;
    padding:10px;
    border-radius: 10px;
}
.decision-row:hover{
    background-color: #ffffffc9;
    cursor: pointer;
}
.header-text{
    font-family: Arial, sans-serif;
    font-size: 30px;
    font-weight: bold;
    margin-top: 20px;
    margin-bottom: 20px;
    text-shadow: 2px 2px 5px #97aaff36;
    color: rgb(83, 186, 255);
}
.roles-container-inline-correction{
    display: inline-block;
    height: 140px;
    padding-top: 15px;
    padding-bottom: 5px;
    margin-top: -20px;
    border-top: #9ad2ff solid 5px;
    border-bottom: #c8d5ff solid 5px;
    position: relative;
    white-space: nowrap;
    overflow-y: hidden;

}
.roles-container{
    display: flex;
    float: left;
    padding-top: 20px;
    margin-top:-20px;
    padding-right: 20px;
    padding-left: 10px;
    padding-bottom: 20px;
    width: max( fit-content, 100%);
}
.roles{
    margin-top: 100px;
    width: calc(100% - 35px);
    height: 130px;
    white-space: nowrap;
    padding: 20px;
    padding-bottom:20px;
    overflow: hidden;
    margin-top: 40px;
    margin-bottom: 30px;
    position: relative;
    border-radius: 5px;
    
}

.role{
    width:200px;
    height:100px;
    margin-left:10px;
    margin-right:10px;
    padding:10px;
    display: inline-block;
    position: relative;
    float: left;
    border-left: #068fff62 solid 5px;
    border-radius: 10px;
    box-shadow: 10px 0px 5px rgba(0, 0, 0, 0.164);
    background-color: #ffffff;
    white-space: wrap;
}

.left{
    font-size: 20px;
    color:#ffffffaf;
    width:20px;
    height:260px;
    line-height: 240px;
    margin-top: -130px;
    margin-left: -20px;
    padding-left: 10px;
    cursor: pointer;
    display: inline-block;
    font-weight: bolder;
    background-image: linear-gradient(to left, rgba(84, 218, 255, 0.473), rgba(75, 108, 255, 0.473)); 
    border-radius: 200px;
    vertical-align: middle;
    z-index: 100;
}
.right{
    font-size: 20px;
    font-weight: bold;
    color:#ffffffaf;
    width:30px;
    height:260px;
    line-height: 240px;
    margin-top: -130px;
    padding-left: 8px;
    cursor: pointer;
    display: inline-block;
    background-image: linear-gradient(to right, rgba(84, 218, 255, 0.452), rgba(75, 108, 255, 0.466)); 
    position: relative;
    z-index: 100;
    vertical-align: middle;
    margin-left: -10px;
}

.meta-text{
    font-family: sans-serif;
    font-size: 16px;
    color:#555555;
    text-align: left;
    padding-left: 10px;
    padding-bottom: 10px;
}
.job {
    text-align: left;
    box-shadow: 5px 5px 5px rgba(0, 0, 0, 0.164);
    padding: 5px;
}
.jobs{
    height: 100%;
    overflow: auto;
}
.jobs-container{
    display:block;
    font-family: fantasy;
    margin-top: 60px;
    height: 300px;
    padding: 20px;
    padding-left:0;
    padding-right:0%;
    background-color: #ffffff00;
    overflow-wrap: break-word;
    white-space: pre-wrap;
    font-size: 18px;
    color: #333;
    width: 500px;
    padding-bottom: 100px;
    box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.164);
    overflow: hidden;
    
}


.container{
    height:calc(100vh - 120px);
    overflow: auto;
    position: absolute;
    margin-top: 20px;
    left: 0;
    width: calc(100vw - 180px);
    z-index: -2;
    margin-left: 180px;
    text-align: center;
    
    
}
</style>