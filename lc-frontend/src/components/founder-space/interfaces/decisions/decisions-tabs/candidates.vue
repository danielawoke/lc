<script setup>
import { useRoute, useRouter } from 'vue-router'
import { nextTick, onMounted, onUnmounted, watch } from 'vue';
import { ref } from 'vue';
import CandidatePopup from '@/components/founder-space/interfaces/decisions/candidates-popups/candidate-popup.vue';
import RejectAllPopup from '@/components/founder-space/interfaces/decisions/candidates-popups/reject-all-popup.vue';
import axios, { all } from "axios";
import {AccountLocal} from '@/lib/appwrite.js';
import { createClient } from '@supabase/supabase-js';
const supabase = createClient(import.meta.env.VITE_SUPABASE_URL, import.meta.env.VITE_SUPABASE_ANON_KEY);
const apiURL = import.meta.env.VITE_APP_API_URL;
useRouter(); 
let route = useRoute();

let props = defineProps({
    scrollable: Array
});

let jobs = ref([
    
]);

let filteredJobs = ref(jobs.value);

let candidatePopup = ref([false]);
let candidateInfo = ref({});
let popupData = ref({});
let candidateObject = ref({});
let selectedId = ref(0);
let userId = "";
let rejectAllEnabled = ref(true);

let channel = null;
onMounted(async () => {
    try{
        let user = await AccountLocal.get();
        userId = user.$id;
        const response = await axios.get(`${apiURL}projects/votes/load_candidates/${route.params.projectId}/${userId}`);
        jobs.value = response.data.candidates;
        filteredJobs.value = jobs.value;
        channel = await supabase
                        .channel('candidates')
                        .on(
                            'postgres_changes',
                            {
                            event: 'INSERT',
                            schema: 'public',
                            table: 'new_candidates',
                            filter: `project_id=eq.${route.params.projectId}`
                            },
                            async (payload) => {
                                if(payload.new.user_id == userId){
                                    for (let job of jobs.value){
                                        if(job.job_id == payload.new.job_id){
                                            let dom = document.getElementById('job-'+job.job_id);
                                            let prevWidth = dom.scrollWidth;
                                            job.candidates.unshift(payload.new);
                                            await nextTick();
                                            let diff = dom.scrollWidth - prevWidth;   
                                            console.log(diff); 
                                            if(dom.scrollLeft < 200){
                                                dom.scrollLeft = 0;
                                            }else{
                                                dom.scrollLeft = dom.scrollLeft + diff;
                                            }
                                            
                                            break;
                                        }
                                    }
                                }
                            }
                        )
                        .subscribe();
                        
        // await axios.get(`${apiURL}/projects/votes/load_config_settings/${route.params.projectId}/${userId}`).then(response => {
        //     rejectAllEnabled.value = response.data.config_settings.configSettings.reject_remaining_enabled;
        // }).catch(error => {
        //     console.error("Error fetching reject all enabled status:", error);
        // });


    }catch(error){
        console.error("Error fetching jobs:", error);
    }
    await nextTick();
    fontAdjust();
})

onUnmounted(() => {
    if (channel) {
        supabase.removeChannel(channel);
    }
})

function filterJobs(search){
    filteredJobs.value = jobs.value.filter(job => job.title.toLowerCase().includes(search.toLowerCase()));
    fontAdjust();
}

function fontAdjust(){
    for (let element of document.getElementsByClassName("profile-name")) {
        console.log(element.offsetHeight);
        let fontsizeChange = 10;
        while (element.offsetHeight > 40) {
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


let selectedJobId = "";

let allCandidates = ref([]);

async function openCandidatePopup(candidate, job){
    let applicant_id = candidate.application_id;
    selectedJobId = job.job_id;
    allCandidates.value = job.candidates;
    await axios.get(`${apiURL}projects/votes/load_applicant_info/${applicant_id}`).then(response => {
        console.log(response.data);
        popupData.value = response.data.applicant_data;
        console.log(popupData.value);
    }).catch(error => {
        console.error("Error fetching candidate info:", error);
        popupData.value = {};
    });
    props.scrollable[0] = 'hidden';
    candidatePopup.value[0] = true;
    await nextTick();
    document.getElementById('popup-backdrop').style.top = document.getElementById("total-container").scrollTop + 'px';
    document.getElementById('popup').style.top = document.getElementById("total-container").scrollTop + 'px';

}

let rejectAllPopup = ref([false]);
let selectedJob = ref([]);

async function rejectAll(job){
    selectedJob.value = job;
    props.scrollable[0] = 'hidden';
    rejectAllPopup.value[0] = true;
    await nextTick();
    document.getElementById('popup-backdrop').style.top = document.getElementById("total-container").scrollTop + 'px';
    document.getElementById('popup').style.top = document.getElementById("total-container").scrollTop + 'px';
}



</script>

<template>
    <CandidatePopup v-if="candidatePopup[0]" :renderVar="candidatePopup" :scrollable="scrollable" :candidate="popupData" :candidateObject="candidateObject" :id="selectedId" :allCandidates="allCandidates" :userID="userId" :jobID="selectedJobId"/>
    <RejectAllPopup v-if="rejectAllPopup[0]" :renderVar="rejectAllPopup" :scrollable="scrollable" :job="selectedJob" :userID="userId"/>
    <div class="decision-row">
        <div class="header-text">
            All Candidates
        </div>
        <hr class="line"/>
        <div id="search" class="jobs-search-container">
            <input  @input="filterJobs($event.target.value)" class="job-search" placeholder="Filter for the job you're looking for..."/>
        </div>
    </div>
    <div v-for="(job) in filteredJobs" class="decision-row">
        <div class="job-header">
            {{ job.job_title }}
        </div>
        <div class="roles" >
            <div class="left"><</div>
            <div class="roles-container-inline-correction" :id="'job-' + job.job_id">
                <div v-if="job.candidates.length==0">
                    <div class="no-results-text">Nothing for now...</div>
                    <img class="nothing-for-now-image" src="@/assets/founder-space/decisions/nothing-for-now.png"/>
                </div>
                <div v-else class="roles-container">
                    <div v-for="candidate in job.candidates" class="role" style="margin-top:0px;padding-top:20px;" @click="openCandidatePopup(candidate.preview_data, job)">
                        <div style="" class="role-title"><div :style="{backgroundImage: 'url(' + candidate.preview_data.image + ')'}" class="profile-image"></div><span class="profile-name" :style="candidate.preview_data.name.length>15? 'display:block; vertical-align: top; margin-top:-5px;' : ''">{{ candidate.preview_data.name }}</span></div> 
                        <div style="color:black" class="role-description">{{ candidate.preview_data.description }}</div>
                    </div>
                </div>
            </div>
            <div class="right">></div>
        </div>
        <div class="text-container">
            <div @click="rejectAll(job)" class="meta-button-bottom-left harsh" v-if="rejectAllEnabled">Reject remaining</div>
            <div class="meta-text-bottom-right">{{ job.candidates.length }} results</div>
        </div>
    </div>
    
</template>
<style scoped>
.nothing-for-now-image{
    width: auto;
    height: 140px;
    display:block;
    margin:auto;
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
    font-style: italic;
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
.job-search{
    width:  95%;
    border-radius: 5px;
    padding: 15px;
    font-size: 16px;
    margin:auto;
    margin: 20px;
    outline: none;
    border: none;
    color:rgb(0, 0, 0);
    background-color: #ffffff;

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
    width:  95%;
    border-radius: 5px;
    padding: 15px;
    font-size: 16px;
    margin:auto;
    margin: 20px;
    outline: none;
    border: none;
    color:rgb(0, 0, 0);
    background-color: #ffffff;

}
.jobs-search-container{
    width: 100%;
    margin:auto;
    outline: none;
    background-color: #fafafa59;
    box-shadow: #00000080 0px 0px 30px;
    border-radius: 10px;
    margin-bottom: 20px;
    position: sticky;
    top:0;
}
.job-header{
    font-family: Arial, sans-serif;
    font-size: 24px;
    font-weight: bold;
    margin-top: 20px;
    margin-bottom: 20px;
    text-shadow: 2px 2px 5px #00000036;
    color:#005f9e;
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
    text-shadow: 2px 2px 5px #97aaff36;
    color: rgb(83, 186, 255);
}


.roles-container-inline-correction{
    display: inline-block;
    height: 140px;
    padding-top: 15px;
    padding-bottom: 5px;
    margin-top: -20px;
    width: calc(100% - 10px);
    border-top: #9ad1ff79 solid 5px;
    border-bottom: #c8d5ff59 solid 5px;
    position: relative;
    white-space: nowrap;
    overflow-x: auto;
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
    z-index: 0;
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