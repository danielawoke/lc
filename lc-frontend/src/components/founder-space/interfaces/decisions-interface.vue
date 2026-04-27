<script setup>
import { useRoute, useRouter } from 'vue-router'
import { nextTick, onMounted, watch } from 'vue';
import {AccountLocal} from "@/lib/appwrite";
import { ref } from 'vue';
import Candidates from '@/components/founder-space/interfaces/decisions/decisions-tabs/candidates.vue';
import CoMemberProposals from '@/components/founder-space/interfaces/decisions/decisions-tabs/co-member-decisions.vue';
import Configuration from '@/components/founder-space/interfaces/decisions/decisions-tabs/configuration.vue';
import CreateProposal from '@/components/founder-space/interfaces/decisions/decisions-tabs/create-proposal.vue';
import Archive from '@/components/founder-space/interfaces/decisions/decisions-tabs/archive.vue';

let route = useRoute();
let router = useRouter();

let user = ref(null);

let jobs = ref([
    {id: 1, title: "Job 1", description: "Description for Job 1"},
    {id: 2, title: "Job 2", description: "Description for Job 2"},
    {id: 3, title: "Job 3", description: "Description for Job 3"},
    {id: 4, title: "Job 4", description: "Description for Job 4"},
    {id: 5, title: "Job 5", description: "Description for Job 5"},
    {id: 6, title: "Job 6", description: "Description for Job 6"},
    {id: 7, title: "Job 7", description: "Description for Job 7"},
    {id: 8, title: "Job 8", description: "Description for Job 8"},
    {id: 9, title: "Job 9", description: "Description for Job 9"},
    {id: 10, title: "Job 10", description: "Description for Job 10"},
]);

let candidateSelected = ref(true);
let candidateInfo = ref({});
let scrollable = ref(['auto']);
let tab = ref(""); // Candidates, Co-Member Proposals, Create Proposal

onMounted(async () => {
    //define full page from some kind of api of the like

    // fullPage = fetch(jobID) something like this
    tab.value = route.params.tab ? route.params.tab : "Personal";
    try {
        user.value = await AccountLocal.get();
    } catch (err) {
        console.log("Not logged in", err);
    }

    // load from decisions

    await nextTick();
})

function goToPersonal(){
    tab.value = "personal";
    router.push(`/project-edit/${route.params.projectId}/votes/personal`);
    leftBarToggle.value = false;
}

function goToCandidates(){
    tab.value = "candidates";
    router.push(`/project-edit/${route.params.projectId}/votes/candidates`);
    leftBarToggle.value = false;
}

function goToArchive(){
    tab.value = "archive";
    router.push(`/project-edit/${route.params.projectId}/votes/archive`);
    leftBarToggle.value = false;
}

function goToCreateProposal(){
    tab.value = "create-proposal";
    router.push(`/project-edit/${route.params.projectId}/votes/create-proposal`);
    leftBarToggle.value = false;
}

function goToConfiguration(){
    tab.value = "configuration";
    router.push(`/project-edit/${route.params.projectId}/votes/configuration`);
    leftBarToggle.value = false;
}


function mobileModeListener(){
    mobileMode.value = window.innerWidth <= 768;
    console.log("Mobile mode:", mobileMode.value);
}

let mobileMode = ref(true)
mobileMode.value = window.innerWidth <= 768;
window.addEventListener('resize', mobileModeListener);
let leftBarToggle = ref(false);

</script>

<template>

<!-- <CandidateView v-if="candidateSelected" /> -->

<!-- There will be a true list of jobs, decisions, etc, and a personalized one that is compared against and a modification of the true list. You will save personalized settings of the true list for the user -->

<!-- keep spee consistent by having a single table to index data through -->



<div v-if="mobileMode">
    <div class="burgerContainer" v-if="mobileMode">
        <img class="settings" style="z-index:1000" src="@/assets/founder-space/decisions/ham-orange.png" @click="leftBarToggle=!leftBarToggle"/>
    </div>
    <div class="votes-left-bar" v-if="leftBarToggle">
        <div class="left-bar-votes-text" @click="goToPersonal">Personal</div>
        <div class="left-bar-votes-text" @click="goToCandidates">Candidates</div>
        <div class="left-bar-votes-text" @click="goToArchive">Archive</div>
        <div class="left-bar-votes-text" @click="goToCreateProposal">Create Proposal</div>
        <div class="left-bar-votes-text" @click="goToConfiguration">Configuration</div>
    </div>
</div>

<div id='total-container' class="container" :style="{overflow: scrollable[0], width: mobileMode ? '100vw' : 'calc(100vw - 50px)', marginLeft: mobileMode? '0px': '50px'}">
    <div v-if="!mobileMode">
        <div class="top-header-container">
            <div class="sigil-border">
                <!-- <div class="background-circle-sigil"></div> -->
                <img class="center-sigil" src="@/assets/founder-space/decisions/angel-9.png" />
                <!-- <div style="color: #000; z-index:10000; position:relative; left:50%; top:50%;">{{ user }}</div> -->
            </div>
        </div>
        <div class="top-bottom-text-container">
            <div class="left-adjust">
                <div @click="goToPersonal" :class="tab == 'personal' ? 'element active' : 'element'">Personal</div>
                <div @click="goToCandidates" :class="tab == 'candidates' ? 'element active' : 'element'">Candidates</div>
                <div @click="goToArchive" :class="tab == 'archive' ? 'element active' : 'element'">Archive</div>
                <div @click="goToCreateProposal" :class="tab == 'create-proposal' ? 'element active' : 'element'">Create Proposal</div>
                <div @click="goToConfiguration" :class="tab == 'configuration' ? 'element active' : 'element'">Configuration</div>
            </div>
        </div>
    </div>
    <CoMemberProposals v-if="tab=='personal'" :scrollable="scrollable"/>
    <Candidates v-if="tab=='candidates'" :scrollable="scrollable"/>
    <Archive v-if="tab=='archive'" :scrollable="scrollable" />
    <CreateProposal v-if="tab=='create-proposal'" :scrollable="scrollable" />
    <Configuration v-if="tab=='configuration'"/>
    <br/>
    <br/>
    <br/>
    <br/>
    <br/>
    <br/>
</div>

</template>

<style scoped>
@keyframes slideIn {
    from {
        transform: translateX(-100%);
    }
    to {
        transform: translateX(0);
    }
}

.left-bar-votes-text{
    color:white;
    text-align: center;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 16px;
    margin-top:30px;
}
.left-bar-votes-text:hover{
    color:rgb(197, 197, 197);
}
.votes-left-bar{
    position:absolute;
    top:60px;
    left:0;
    width:100vw;
    height:calc(100vh - 60px);
    background:linear-gradient(to top, rgb(134, 9, 0), rgb(204, 75, 0));
    animation: slideIn ease 0.3s;
}

.settings{
    width: 30px;
    height: 30px;
    background-size: 80% 80%;
    background-position: center;
    background-repeat: no-repeat;
    color: rgb(0, 0, 0);
    font-family: Arial, Helvetica, sans-serif;
    font-size: 12px;
    position: absolute;
    top:0px;
    filter:invert(1);
    left:10px;
    border-radius: 5px;
    overflow:hidden;
}
.toolBarBurger{
    position: absolute;
    left:20px;
    top:0px;
    z-index: 100;
}
.burgerContainer{
    position: fixed;
    top:18px;
    left:110px;
    filter: invert(1);
    z-index: 100;
}
.burgerContainer:hover{
    transition:all ease-in 0.1s;
}
.active{
    filter: saturate(0) invert(1) contrast(2000%);
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
.Save:hover{
    filter: invert(1);
    box-shadow: #0000005c 0px 0px 15px;
}
.left-adjust{
    width:80%;
    text-align: left;
    margin:auto;
}
.element{
    display: block;
    font-family: sans-serif;
    font-size: 16px;
    color:#54b0cc;
    font-weight: lighter;
    text-align: center;
    vertical-align: middle;
    float: left;
    padding-top:10px;
    height: 30px;
    margin-top: -10px;
    margin-right: 30px;
    border-radius: 5px;
    cursor: pointer;
}
.background-circle-sigil{
    width: 120px;
    height: 120px;
    border-radius: 50%;
    position: absolute;
    padding:100px;
    background-image: url('@/assets/founder-space/decisions/stars.png');
    filter: invert(1);
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
    background-color: #ffd0b4;
    background-image: url('@/assets/founder-space/decisions/stars-1.png');
    background-repeat: cover;
    box-shadow: #1dd2ff 0px 0px 100px;
    filter: invert(1);

}
.top-header-container{
    display: flex;
    width: calc(100%);
    height: 50px;
    background-color: #ffffff;
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
    background-image: linear-gradient(to bottom, rgb(190, 240, 255), rgb(172, 238, 255));
    box-shadow: #9df8ff80 0px 0px 30px;
    width: calc(100%);
    position: absolute;
    top: 280px;
    margin: auto;
    height: 40px;
    padding-top: 10px;
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
.remaining{
    width: 25px;
    height: 25px;
    border-radius: 25px;
    background-color: #ff0707b4;
    color: white;
    font-size: 12px;
    font-weight: bold;
    vertical-align: middle;
    line-height: 25px;
    text-align: center;
    margin-top: 0;
    margin-left: 0;
    float: right;
    padding-left: 5px;
    padding-right: 5px;
}
.sub-profile-image{
    width: 22px;
    height: 22px;
    border-radius: 25px;
    border: rgba(0, 0, 0, 0.562) solid 2px;
    background-color: #00000000;
    float: left;
    margin:10px;
    margin-top: 0;
    margin-left: 0;
}
.profile-image{
    width: 30px;
    height: 30px;
    border-radius: 25px;
    border: rgba(0, 0, 0, 0.562) solid 2px;
    background-color: #00000000;
    float: left;
    margin:10px;
    margin-top: 0;
    margin-left: 0;
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
.job-search{
    width:  95%;
    border-radius: 5px;
    padding: 15px;
    font-size: 16px;
    margin:auto;
    margin: 20px;
    outline: none;
    border: none;
    background-color: #00000005;

}
.jobs-search-container{
    width: 100%;
    margin:auto;
    outline: none;
    background-color: #ffffff59;
    box-shadow: #00000080 0px 0px 30px;
    border-radius: 10px;
}
.job-header{
    font-family: Arial, sans-serif;
    font-size: 24px;
    font-weight: bold;
    margin-top: 20px;
    margin-bottom: 20px;
    text-shadow: 2px 2px 5px #00000036;
}
.meta-text-bottom-right{
    font-family: sans-serif;
    font-size: 16px;
    color:#555555;
    text-align: right;
    padding-right: 10px;
    padding-bottom: 10px;
    
    margin-right: 10px;
}
.text-container{
    text-align: right;
    margin:auto;
    
}
.line{
    background-color: #000000;
    box-shadow: #000000 0px 0px 30px;
    border: none;
    height: 5px;
    margin:auto;
}
.decision-row{
    width: calc(80%);
    position: relative;
    text-align: left;
    color:#000000d8;
    margin:auto;
    
    margin-top: 50px;
}
.header-text{
    font-family: Arial, sans-serif;
    font-size: 30px;
    font-weight: bold;
    margin-top: 20px;
    margin-bottom: 20px;
    text-shadow: 2px 2px 5px #00000036;
}


.roles-container-inline-correction{
    display: inline-block;
    height: 160px;
    width: calc(100% - 10px);
    overflow-x: auto;
    background-color: #00000000;
    position: relative;
    white-space: nowrap;
}
.roles-container{
    display: flex;
    float: left;
    padding-top: 5px;
}
.roles{
    margin-top: 100px;
    width: calc(100% - 35px);
    height: 130px;
    white-space: nowrap;
    box-shadow: #00000080 0px 0px 30px;
    background-color: #ffffff31;
    border-radius: 30px;
    padding: 20px;
    padding-bottom:20px;
    overflow: hidden;
    margin-top: 40px;
    margin-bottom: 30px;
    position: relative;
}
.role{
    width:200px;
    height:100px;
    margin-left:10px;
    margin-right:10px;
    padding:10px;
    border-radius: 10px;
    display: inline-block;
    position: relative;
    float: left;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.671);
}
.left{
    font-size: 20px;
    font-weight: bold;
    color:#000000af;
    width:20px;
    height:260px;
    line-height: 220px;
    margin-top: -130px;
    margin-left: -20px;
    padding-left: 5px;
    cursor: pointer;
    display: inline-block;
    background-color: #ffffff;
    vertical-align: middle;
    box-shadow: #00000080 0px 0px 30px;
    z-index: 100;
}
.right{
    font-size: 20px;
    font-weight: bold;
    color:#000000af;
    width:30px;
    height:260px;
    line-height: 220px;
    margin-top: -130px;
    padding-left: 8px;
    cursor: pointer;
    display: inline-block;
    background-color: #ffffff;
    z-index: 100;
    vertical-align: middle;
    box-shadow: #00000080 0px 0px 30px;
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
    height:calc(100vh - 60px);
    position: absolute;
    margin-top: 20px;
    left: 0;
    background-color: #d1eeff;
    z-index: -2;
    text-align: center;
    filter: grayscale(0);
    filter: saturate(100%);
    filter: invert(1);
}

</style>