<script setup>

import { useRoute, useRouter } from 'vue-router'
import { defineComponent, nextTick, onMounted, watch } from 'vue';
import { ref } from 'vue';
import axios from  'axios';
import {AccountLocal} from '@/lib/appwrite.js';


const apiURL = import.meta.env.VITE_APP_API_URL;
const route = useRoute();

useRouter(); 
useRoute();

let saveChanges = ref(false);

let withdrawFromAll = ref();
let rejectRemaining = ref();

let removeJobTab = ref(1);
let jobs = ref([
    // {id: 1, job: "Mechanical Engineer"},
    // {id: 2, job: "Software Engineer"},
    // {id: 3, job: "Data Scientist"},
    // {id: 4, job: "Product Manager"},
    // {id: 5, job: "UX Designer"},
    // {id: 6, job: "DevOps Engineer"},
    // {id: 7, job: "Systems Analyst"},
    // {id: 8, job: "Network Administrator"},
    // {id: 9, job: "Cybersecurity Specialist"},
    // {id: 10, job: "Database Administrator"},

]);
let filteredJobs = ref(jobs.value);
let TabedFilteredJobs = ref(filteredJobs.value.slice(0,8));
let SelectedJobs = ref([]);
let filteredSelectedJobs = ref(SelectedJobs.value);
let delegateSelect = ref(false);
let delegateSelectTab= ref(0);
let Members = ref([
    // {id: 1, name: "John Doe"},
    // {id: 2, name: "Jane Smith"},
    // {id: 3, name: "Michael Brown"},
    // {id: 4, name: "Emily Davis"},
    // {id: 5, name: "David Wilson"},
    // {id: 6, name: "Sarah Johnson"},
    // {id: 7, name: "Chris Lee"},
    // {id: 8, name: "Amanda Martinez"},
    // {id: 9, name: "James Anderson"},
    // {id: 10, name: "Patricia Taylor"},
    // {id: 11, name: "Robert Thomas"},
    // {id: 12, name: "Linda Moore"},
]);
let filterMembers = ref(Members.value);
let TabedFilteredMembers = ref(filterMembers.value.slice(0,8));
let reauthorizeTab = ref(1);
let reauthorizeJobs = ref([]);
let filteredReauthorizeJobs = ref(reauthorizeJobs.value);
let TabedFilteredReauthorizeJobs = ref(filteredReauthorizeJobs.value.slice(0,6));
let SelectedReauthorizeJobs = ref([]);
let filteredSelectedReauthorizeJobs = ref(SelectedReauthorizeJobs.value);
let user = null;

onMounted(async () => {

    user = await AccountLocal.get();
    
    await axios.get(`${apiURL}projects/votes/load_config_settings/${route.params.projectId}/${user.$id}`).then((response) => {
        let configSettings = response.data.config_settings.configSettings;
        let jobsData = response.data.jobs;
        withdrawFromAll.value = configSettings.withdraw_from_all;
        rejectRemaining.value = configSettings.reject_remaining_enabled;

        let takenJobs = [];

        for (let job of configSettings.delegated_jobs){
            reauthorizeJobs.value.push({job, type: "delegated"});   
            takenJobs.push(job.job_id);
        }
        
        for (let job of configSettings.withdrawn_jobs){
            reauthorizeJobs.value.push({job, type: "Withdrawn"});   
            takenJobs.push(job.job_id);
        }

        filteredReauthorizeJobs.value = reauthorizeJobs.value;
        TabedFilteredReauthorizeJobs.value = filteredReauthorizeJobs.value.slice(0,6);

        for (let job of jobsData){
            if(!takenJobs.includes(job.job_id)){
                let job_object = {
                    job_id: job.job_id,
                    job_name: job.job_object.jobDescription.title[0],
                }
                jobs.value.push(job_object);
            }
        }

        filteredJobs.value = jobs.value;
        TabedFilteredJobs.value = filteredJobs.value.slice(0,8);

        Members.value = response.data.members;
        filterMembers.value = Members.value;
        TabedFilteredMembers.value = filterMembers.value.slice(0,8);
        
        // console.log(TabedFilteredMembers.value);

    }).catch((error) => {
        console.log(error);
    });

    await nextTick();
    backgroundResize();
    window.addEventListener("resize", backgroundResize);

})

function backgroundResize(){
    let background = document.getElementsByClassName("background")[0];
    background.style.height = "100%";
    let h1 = background.offsetHeight;
    background.style.height = "auto";
    let h2 = background.offsetHeight;
    if(h1 > h2){
        background.style.height = "100%";
    }else{
        background.style.height = "auto"
    }
}

function removeSelectedJob(el){
    if(SelectedJobs.value.includes(el)){
        SelectedJobs.value = SelectedJobs.value.filter(job => job !== el);
    }
    else{
        SelectedJobs.value.push(el);
    }
    console.log(SelectedJobs.value);
}
function removeJobTabChange(num){
    removeJobTab.value = num;
    TabedFilteredJobs.value = filteredJobs.value.slice((removeJobTab.value-1)*8, (removeJobTab.value)*8);
}
function removeJobFilter(search){
    if(search === undefined || search === null){
        search = "";
    }
    console.log(jobs.value);
    filteredJobs.value = jobs.value.filter(job => job.job_name.toLowerCase().includes(search.toLowerCase()));
    removeJobTab.value = 1;
    TabedFilteredJobs.value = filteredJobs.value.slice(0,8);
    filteredSelectedJobs.value = SelectedJobs.value.filter(job => job.job_name.toLowerCase().includes(search.toLowerCase()));

}
function selectAllJobs(){
    SelectedJobs.value = [...filteredJobs.value];
    filteredSelectedJobs.value = [...filteredJobs.value];
}
function deselectAllJobs(){
    for(let job of filteredJobs.value){
        SelectedJobs.value = SelectedJobs.value.filter(selectedJob => selectedJob !== job);
    }
    filteredSelectedJobs.value = [];

}


function removeSelectedReauthorizeJob(el){
    if(SelectedReauthorizeJobs.value.includes(el)){
        SelectedReauthorizeJobs.value = SelectedReauthorizeJobs.value.filter(job => job !== el);
    }
    else{
        SelectedReauthorizeJobs.value.push(el);
    }
    console.log(SelectedReauthorizeJobs.value);
}
function reauthorizeTabChange(num){
    reauthorizeTab.value = num;
    TabedFilteredReauthorizeJobs.value = filteredReauthorizeJobs.value.slice((reauthorizeTab.value-1)*6, (reauthorizeTab.value)*6);
}

function reauthorizeFilter(search){
    if(search === undefined || search === null){
        search = "";
    }
    filteredReauthorizeJobs.value = reauthorizeJobs.value.filter(job => job.job.job_name.toLowerCase().includes(search.toLowerCase()));
    reauthorizeTab.value = 1;
    TabedFilteredReauthorizeJobs.value = filteredReauthorizeJobs.value.slice(0,6);
    filteredSelectedReauthorizeJobs.value = SelectedReauthorizeJobs.value.filter(job => job.job.job_name.toLowerCase().includes(search.toLowerCase()));
}

function selectAllReauthorizeJobs(){
    SelectedReauthorizeJobs.value = [...filteredReauthorizeJobs.value];
    filteredSelectedReauthorizeJobs.value = [...filteredReauthorizeJobs.value];
}
function deselectAllReauthorizeJobs(){
    for(let job of filteredReauthorizeJobs.value){
        SelectedReauthorizeJobs.value = SelectedReauthorizeJobs.value.filter(selectedJob => selectedJob !== job);
    }
    filteredSelectedReauthorizeJobs.value = [];
}


async function withdrawJobs(){
    for (let job of SelectedJobs.value){
        let job_object = {
            job: job,
            type: "Withdrawn"
        }
        reauthorizeJobs.value.unshift(
            job_object
        )
    }
    
    await nextTick();
    reauthorizeFilter(document.getElementById("reauthorizeSearch").value);
    jobs.value = jobs.value.filter(job => !SelectedJobs.value.includes(job));
    SelectedJobs.value = [];
    filteredSelectedJobs.value = [];
    removeJobFilter(document.getElementById("delWithSearch").value);
}


async function reauthorize(){
    console.log(SelectedReauthorizeJobs.value);
    
    for(let job of SelectedReauthorizeJobs.value){
        reauthorizeJobs.value = reauthorizeJobs.value.filter(reauthorizeJob => reauthorizeJob.job.job_id !== job.job.job_id);
        console.log(job);
        jobs.value.unshift(job.job);
    }

    reauthorizeFilter(document.getElementById("reauthorizeSearch").value);
    removeJobFilter(document.getElementById("delWithSearch").value);

    SelectedReauthorizeJobs.value = [];
}

function delegateSelected(){
    if(SelectedJobs.value.length > 0){
        delegateSelect.value = !delegateSelect.value;
    }
}
async function delegateMemeberSelected(delegate){
    

    for (let job of SelectedJobs.value){
        console.log(delegate);
        console.log(job);
        let delegate_object = {
                        "job": {
                            "job_id": job.job_id,
                            "job_name": job.job_name,
                            "delegate_id": delegate.user_id,
                            "delegate_name": delegate.profile_data.display_name,
                        },
                        "type": "delegated"
                    }

        reauthorizeJobs.value.unshift(
            delegate_object
        )
    }
    
    jobs.value = jobs.value.filter(job => !SelectedJobs.value.includes(job));
    SelectedJobs.value = [];
    filteredSelectedJobs.value = [];
    delegateSelect.value = false;
    await nextTick();
    reauthorizeFilter(document.getElementById("reauthorizeSearch").value);
    removeJobFilter(document.getElementById("delWithSearch").value);

}
function delegateTabChange(num){
    delegateSelectTab.value = num;
    TabedFilteredMembers.value = filterMembers.value.slice((delegateSelectTab.value-1)*8, (delegateSelectTab.value)*8);
}

function delegateMemeberFilter(search){
    delegateSelectTab.value = 1;
    TabedFilteredMembers.value = filterMembers.value.filter(member => member.name.toLowerCase().includes(search.toLowerCase())).slice((delegateSelectTab.value-1)*8, (delegateSelectTab.value)*8);
}

function withdrawFunction(value){
    if(value === "withdraw"){
        withdrawFromAll.value = true;
        //logic to withdraw from all current and future decisions
    }else{
        withdrawFromAll.value = false;
    }
}
function rejectFunction(value){
    if(value === "reject"){
        rejectRemaining.value = true;
        //logic to enable the reject remaining feature
    }else{
        rejectRemaining.value = false;
    }
    console.log(rejectRemaining.value);
    //logic to enable the reject remaining feature
}


let errorMessage = ref("");

async function save(){

    let configSettings = {
        "withdraw_from_all": withdrawFromAll.value,
        "reject_remaining_enabled": rejectRemaining.value,
        "delegated_jobs": reauthorizeJobs.value.filter(job => job.type === "delegated").map(job => job.job),
        "withdrawn_jobs": reauthorizeJobs.value.filter(job => job.type === "Withdrawn").map(job => job.job),
    }
    console.log(`${apiURL}projects/votes/update_config/${route.params.projectId}/${user.$id}`);
    
    try{
        let response =await axios.post(`${apiURL}projects/votes/update_config/${route.params.projectId}/${user.$id}`, {
            "config_settings": configSettings
        });
        saveChanges.value = true;
        await nextTick();
        backgroundResize();
    }catch(error){
        errorMessage.value = "Delegate Cycle Detected, please pick another combination of delegates for the chosen jobs.";
    }

    //logic to save the changes and submit the proposal to the member base for review
}

let delegateWithdrawDispute = ref(false);
function delegateWithdrawDisputeFunction(value){
    if(value === "reject"){
        delegateWithdrawDispute.value = true;
        //logic to have vote sent back to authority
    }else{
        delegateWithdrawDispute.value = false;
        //logic to withdraw with delegate
    }
}

</script>
<template>
    <div class="background">
        <div class="configuration-container">
            <div v-if="!saveChanges">
                <div class="question">
                    Would you like to withdraw from all current and future decisions?
                </div>
                <div class="yes-no-container">
                    <span style="display:inline-block; float:left; margin-top:10px;">
                        <input @click="withdrawFunction($event.target.value)" type="radio" id="withdraw-yes" value="withdraw" :checked="withdrawFromAll">
                        <label  class="button-text">Yes</label>
                    </span>
                    <span style="display:inline-block; float:left; margin-top:10px;">
                        <input @click="withdrawFunction($event.target.value)" type="radio" id="withdraw-no" name="withdraw" value="keep" :checked="!withdrawFromAll">
                        <label class="button-text">No</label>
                    </span>
                </div>
                <!-- <br>
                <br>
                <br> -->
                <!-- <div class="question">
                    Would you like to enable the <b>Reject Remaining</b> feature for the candidate pool view? This will allow you to instantly reject all remaining candidates listed for a given job with a single button, clearing out the job listing and allowing new cadidates to appear first.
                </div>
                <div class="yes-no-container">
                    <span style="display:inline-block; float:left; margin-top:10px;">
                        <input @click="rejectFunction($event.target.value)" type="radio" id="reject-yes" name="reject" value="reject" :checked="rejectRemaining">
                        <label  class="button-text">Yes</label>
                    </span>
                    <span style="display:inline-block; float:left; margin-top:10px;">
                        <input @click="rejectFunction($event.target.value)" type="radio" id="reject-no" name="reject" value="keep" :checked="!rejectRemaining">
                        <label class="button-text">No</label>
                    </span>
                </div> -->
                <!-- <br>
                <br>
                <br> -->
                <!-- <div class="question">
                    In the case a member you've delegated to happens to withdraw from a vote, would you like to withdraw as well or have the vote go back to being under your authority?
                </div>
                <div class="yes-no-container">
                    <span style="display:inline-block; float:left; margin-top:10px;">
                        <input @click="delegateWithdrawDisputeFunction($event.target.value)" type="radio" id="delegate-withdraw-dispute-yes" name="delegate-withdraw-dispute" value="reject" :checked="delegateWithdrawDispute">
                        <label  class="button-text">Have Vote sent back to my authority</label>
                    </span>
                    <span style="display:inline-block; float:left; margin-top:10px;">
                        <input @click="delegateWithdrawDisputeFunction($event.target.value)" type="radio" id="delegate-withdraw-dispute-no" name="delegate-withdraw-dispute" value="keep" :checked="!delegateWithdrawDispute">
                        <label class="button-text">Withdraw with my delegate</label>
                    </span>
                </div> -->
                <br>
                <br>
                <br>
                <div class="question">Select the following jobs you'd like to delegate to another memeber, or withdraw from entirely. 
                    <div style="font-size:11px;margin-top:10px; color:gray">This list is only of jobs that you currently have voting authority over, all delegated and wtihdrawn jobs are not listed</div>
                    <div class="question-text">
                    </div>
                    <!-- If you select withdraw, you will be removed from all current and future decisions related to the job, and will not receive any updates regarding it. If you select delegate, you will be able to choose a co-member to take your place in the decision, and will receive updates regarding the job, but will not have any decision power in it. -->
                    <div>
                        <div class="meta-jobs-container">
                            <div v-if="!delegateSelect">
                                <input id="delWithSearch" v-on:input="removeJobFilter($event.target.value)" style="padding-right:15px; width:calc(100% - 25px); border-radius:0;" type="text" class="job-search" placeholder="Search Job..." />
                                <div class="people-list-container">
                                    <div v-if="TabedFilteredJobs.length === 0" style="padding:15px; color:gray; font-size:14px; font-family:arial;">No Results</div>
                                    <div v-for="el in TabedFilteredJobs" class="job" :style="SelectedJobs.includes(el)?  'filter: hue-rotate(-35deg); background-image: linear-gradient(to bottom, #33c2ff, #2672ff); color: black; border-bottom:  #33cfff solid 3px;':''" @click.self="removeSelectedJob(el)">
                                        <div style="margin-bottom:-10px" class="job-title" @click.self="removeSelectedJob(el)">{{ el.job_name }}</div>
                                    </div>
                                </div>
                                <div class="buttons-tray-bottom" @click.self="removeSelectedJob(el)">
                                    <div @click="withdrawJobs" class="meta-button-bottom-left gentle" style="opacity: 1;margin-top:5px;">Withdraw</div>
                                    <div @click="delegateSelected" class="meta-button-bottom-left gentle" style="opacity: 1;margin-top:5px;">Delegate</div>
                                    <div class="meta-button-bottom-left" style="opacity: 1;margin-top:5px;">|</div>
                                    <div v-if="filteredSelectedJobs.length==filteredJobs.length" @click="deselectAllJobs" class="meta-button-bottom-left harsh" style="opacity: 1;margin-top:5px;">Deselect All</div>
                                    <div v-else @click="selectAllJobs" class="meta-button-bottom-left harsh" style="opacity: 1;margin-top:5px;">Select All</div>
                                </div>
                                <div class="tab">
                                    <div class="tabs"> 
                                        <div @click="removeJobTabChange(removeJobTab-1)" class="taber">Prev</div>
                                        <div class="tab-container">
                                            <input v-on:input="removeJobTabChange($event.target.value)" style="width:25px; border-radius:5px;" class="job-tab-selection" :value="removeJobTab"/>
                                            <div class="total" >/<div class="remainingTabs">{{Math.ceil(filteredJobs.length/8)}}</div></div>
                                        </div>
                                        <div @click="removeJobTabChange(removeJobTab+1)" class="taber">Next</div>
                                    </div>
                                </div>  
                            </div>
                            <div v-else>
                                <input v-on:input="delegateMemeberFilter($event.target.value)" style="padding-right:15px; width:calc(100% - 25px); border-radius:0;" type="text" class="job-search" placeholder="Search Member..." />
                                <div class="people-list-container">
                                    <div v-if="TabedFilteredMembers.length === 0" style="padding:15px; color:gray; font-size:14px; font-family:arial;">No Results</div>
                                    <div v-for="el in TabedFilteredMembers" class="job" @click.self="delegateMemeberSelected(el)">
                                        <div style="margin-bottom:-10px" class="job-title" @click.self="delegateMemeberSelected(el)">{{ el.profile_data.display_name }}</div>
                                    </div>
                                </div>
                                <div class="buttons-tray-bottom" @click.self="removeSelectedJob(el)">
                                    <!-- profile will be a seperate tab -->
                                    <div @click="delegateSelected" class="meta-button-bottom-left gentle" style="opacity: 1;margin-top:5px;">⇐ Back to Job Selection</div>
                                </div>
                                <div class="tab">
                                    <div class="tabs"> 
                                        <div @click="delegateTabChange(delegateSelectTab-1)" class="taber">Prev</div>
                                        <div class="tab-container">
                                            <input v-on:input="delegateTabChange($event.target.value)" style="width:25px; border-radius:5px;" class="job-tab-selection" :value="delegateSelectTab"/>
                                            <div class="total" >/<div class="remainingTabs">{{Math.ceil(filterMembers.length/8)}}</div></div>
                                        </div>
                                        <div @click="delegateTabChange(delegateSelectTab+1)" class="taber">Next</div>
                                    </div>
                                </div> 
                            </div>
                        </div>
                    </div>
                </div>
                <div class="question" >Select the following jobs you'd reauthorize.<div>
                        <div style="margin-top:15px" class="meta-jobs-container">
                            <input id="reauthorizeSearch" v-on:input="reauthorizeFilter($event.target.value)" style="padding-right:15px; width:calc(100% - 25px); border-radius:0;" type="text" class="job-search" placeholder="Search Job..." />
                            <div class="people-list-container">
                                <div v-if="TabedFilteredReauthorizeJobs.length === 0" style="padding:15px; color:gray; font-size:14px; font-family:arial;">No Results</div>
                                <div v-for="el in TabedFilteredReauthorizeJobs" class="job" :style="SelectedReauthorizeJobs.includes(el)?  'filter: hue-rotate(-35deg); background-image: linear-gradient(to bottom, #33c2ff, #2672ff); color: black; border-bottom:  #33cfff solid 3px;':''" @click.self="removeSelectedReauthorizeJob(el)">
                                    <div style="margin-bottom:-10px" class="job-title" @click.self="removeSelectedReauthorizeJob(el)">{{ el.job.job_name }}</div>
                                    <div v-if="el.type === 'Withdrawn'"  @click.self="removeSelectedReauthorizeJob(el)" style="padding-top:15px; font-size:12px; color:gray; margin-bottom: -5px;">Withdrawn</div>
                                    <div v-else-if="el.type === 'delegated'"  @click.self="removeSelectedReauthorizeJob(el)" style="padding-top:15px; font-size:12px; color:gray; margin-bottom: -5px;"><b>Delegated:</b> {{ el.job.delegate_name }}</div>
                                </div>
                            </div>
                            <div class="buttons-tray-bottom" @click.self="reauthorizeSelectedJobs">
                                <!-- profile will be a seperate tab -->
                                <div class="meta-button-bottom-left gentle" style="opacity: 1;margin-top:5px;" @click="reauthorize">Reauthorize</div>
                                <div class="meta-button-bottom-left" style="opacity: 1;margin-top:5px;">|</div>
                                <div v-if="filteredSelectedReauthorizeJobs.length==filteredReauthorizeJobs.length" @click="deselectAllReauthorizeJobs" class="meta-button-bottom-left harsh" style="opacity: 1;margin-top:5px;">Deselect All</div>
                                <div v-else @click="selectAllReauthorizeJobs" class="meta-button-bottom-left harsh" style="opacity: 1;margin-top:5px;">Select All</div>
                            </div>
                            <div class="tab">
                                <div class="tabs"> 
                                    <div @click="reauthorizeTabChange(reauthorizeTab-1)" class="taber">Prev</div>
                                    <div class="tab-container">
                                        <input v-on:input="reauthorizeTabChange($event.target.value)" style="width:25px; border-radius:5px;" class="job-tab-selection" :value="reauthorizeTab"/>
                                        <div class="total" >/<div class="remainingTabs">{{Math.ceil(filteredReauthorizeJobs.length/6)}}</div></div>
                                    </div>
                                    <div @click="reauthorizeTabChange(reauthorizeTab+1)" class="taber">Next</div>
                                </div>
                            </div>  
                        </div>
                    </div>
                </div>
                <div class="question">
                    <div style="color:cyan;position:absolute; bottom:60px; left:60px; width: calc(100% - 100px);">{{ errorMessage }}</div>
                    <div class="Save" @click="save">
                        Save changes
                    </div>
                </div>
            </div>
            
                    
            <div v-else>
                <div class="header-text">
                    Configuration Saved
                </div>
                <div class="meta-text">
                    You can exit this page. If changes aren't immediately present refresh and changes should appear.
                </div>

            </div>
        </div>
    
    </div>
</template>

<style scoped>
.header-text{
    font-family: Arial, sans-serif;
    font-size: 30px;
    font-weight: bold;
    margin-top: 20px;
    margin-bottom: 20px;
    text-shadow: 2px 2px 5px #97aaff36;
    color: rgb(83, 186, 255);
}

.people-list-container{
    min-height: 270px;
}
.multi-section-checkbox{
    float:left;
    margin-right: 10px;
}
.job-nav{
    display: block;
    width: calc(100% - 20px);
    padding: 10px;
    padding-left: 0;
    color:rgb(0, 0, 0);
    padding-bottom: 10px;
    background: rgba(0, 0, 0, 0.089);
    border-top: #d4d4d4 solid 5px;
    border-bottom: #d4d4d4 solid 5px;
    box-shadow: inset 0px 0px 15px #0000003a;
    background-image: linear-gradient(to bottom, rgb(255, 255, 255), rgb(250, 250, 250));
    padding:10px;
    padding-top:2px;
    padding-bottom:2px;
}
.select{   
    color:#0d6eff;
}
.tab{
    
    font-weight: bolder;
    height: 40px;
    padding: 10px;
    padding-left: 0;
    padding-bottom: 10px;
}
.tabs{
    background-color: #00000000;
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    float: left;
    font-size: 13px;
    padding: 5px;
    border-radius: 10px;
}
.taber{
    font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
    font-weight: bold;
    display: inline-block;
    width: 50px;
    height: 30px;
    background-image: linear-gradient(45deg, #ffffff, #d1d1d1);
    border: solid 3px #b3b3b3;
    color: rgb(54, 54, 54);
    border-radius: 5px;
    text-align: center;
    line-height: 30px;
    cursor: pointer;
    margin-bottom: -0px;
}
.job-tab-selection{
    font-family: Arial, sans-serif;
    width: 25px;
    height: 25px;
    text-align: center;
    border-radius: 5px;
    color: rgb(77, 77, 77);
    background-color: #ffffff00;
    
    font-weight: bolder;
    outline: none;
}

.remainingTabs{
    display: inline-block;
    color:#ffffff;
    font-size: 17px;
    margin-left: 3px;
    text-align: right;
    width:60%;
    color:#000000;
}
.tab-container{
    padding: 5px;
    border-radius: 5px;
    display: inline-block;
    align-items: center;
    height: 22px;
    margin-left:5px;
    margin-bottom: 10px;
    font-size: 14px;
    
    padding-bottom: 5px;
}
.total{
    font-family:  sans-serif;
    display: inline-block;
    text-align: left;
    margin-top: 5px;
    margin-left:5px;
    width: 45px;
    color:#222222;
    padding-right:0;

}
.job-search{
    display: inline-block;
    width: calc(90%);
    padding: 2%;
    padding-right: 8%;
    font-size: 16px;
    margin:auto;
    outline: none;
    border: none;
    color:rgb(0, 0, 0);
    background-color: #dddddd;
    position: relative;
    z-index: 10;
}
.search-button-container{
    display: inline-block;
    background-color: #ffffff;
    position: absolute;
    box-shadow: #0000003a -10px 0px 5px;
    width:55px;
    height:55px;
    margin-left:-5%;
    margin-top: 0px;
    z-index: 100;
}
.search-button{
    display: inline-block;
    width:1.5%;
    aspect-ratio: 1 / 1;
    width: 40%;
    padding: 30%;
    position: absolute;
    cursor: pointer;
    z-index: 100;
    background-color: #00000000;
}
.meta-jobs-container{
    width: 100%;
    height: fit-content;
    overflow: hidden;
    background-color: #fafafa59;
}
.question-text{
    font-family: sans-serif;
    font-size: 16px;
    color:#555555;
    text-align: left;
    padding-left: 10px;
    padding-bottom: 20px;
    display:block;
}
.buttons-tray-bottom{
    display: block;
    left:0;
    height:23px;
    padding:10px;
    width:calc(100% - 20px);
    background-image: linear-gradient(to bottom, rgb(216, 216, 216), rgb(238, 238, 238));
    box-shadow: inset 0px 0px 20px #00000033;
    border-top: hsl(0, 0%, 89%) solid 5px;
    border-bottom: hsl(0, 0%, 89%)  solid 5px;

}
.buttons-tray{
    display: block;
    margin-top: 10px;
    left:0;
    height:23px;
}
.job-title{
    display:block;
    height:fit-content;
    font-weight: bold;
}
.job{
    position: relative;
    display:block;
    text-align: left;
    height:fit-content;
    background-image: linear-gradient(to bottom, white, rgb(235, 231, 231));
    border-bottom: #d3d3d3 solid 3px;
    z-index: 1000;
    padding:5px;
}
.job:hover{
    filter: hue-rotate(-35deg);
    background-image: linear-gradient(to bottom, rgb(226, 226, 226), rgb(206, 206, 206));
    color: black;
    cursor: pointer;
}
.job-selected{
    position: relative;
    display:block;
    text-align: left;
    height:fit-content;
    background-color: #2b2b2b;
    color:rgb(219, 219, 219);
    border-bottom: #d3d3d3 solid 3px;
    z-index: 1000;
    padding:5px;
}
.background{
    width: 100%;
    height: auto;
    background-color:  #ffffff;
    position: absolute;
    z-index: -1;
    margin-top: -100px;
}
.button-text{
    font-family: sans-serif;
    font-size: 16px;
    color:#555555;
    text-align: left;
    padding-left: 10px;
    margin-right: 20px;
}
.yes-no-container{
    display: block;
    margin-top: -10px;
    width: 80%;
    float:left;
}
.question{
    font-family: sans-serif;
    font-size: 16px;
    color:#555555;
    text-align: left;
    padding-left: 10px;
    padding-bottom: 20px;
    display:block;
    margin-top: 20px;
    width:80%;
}
.Save{
    font-family: fantasy;
    margin-top: 20px;
    margin-bottom: 100px;
    width:auto;
    padding: 10px;
    background-image: linear-gradient(to bottom, #ffffff, #cccccc);
    border-radius: 15px;
    position: relative;
    float:right;
    box-shadow: #0000003a 0px 0px 10px;
    border: solid 1px #b3b3b3;
}
.Save:hover{
    filter: invert(1);
    box-shadow: #0000005c 0px 0px 15px;
}
.configuration-container{
    max-width: 800px;
    margin: auto;
    background-color: #ffffff;
    padding: 50px;
    padding-top:120px;
    z-index: -1;
    position: relative;
    height:auto;

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
    bottom:0;
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
.jobs-search-container{
    width: 100%;
    margin:auto;
    outline: none;
    background-color: #fafafa59;
    border-radius: 10px;
}
.job-header{
    font-family: fantasy;
    font-size: 20px;
    font-weight: bold;
    margin-top: 20px;
    margin-bottom: 20px;
    text-shadow: 2px 2px 5px #00000036;
    color:#005f9e;
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
.meta-button-bottom-left{
    font-family: sans-serif;
    font-size: 16px;
    text-align: left;
    margin-right:15px;
    padding-bottom: 10px;
    float: left;
    text-decoration: solid underline #b9b9b986 1px;
    cursor: pointer;
}
.gentle:hover{
    color: #383838;
    text-decoration: solid underline #383838 1px;
}
.harsh:hover{
    font-weight: bolder;
    color: #417cd3;
    text-decoration: solid underline #417cd3 1px;
}
.gentle{
    color: #555555;
}
.harsh{
    font-weight: bolder;
    color: #417cd3;
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
    background-color: #ffffff;
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
    padding: 15px;
    width: calc(100% - 30px);
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
    overflow: hidden;
}


.container{
    height:calc(100vh - 120px);
    overflow: auto;
    position: absolute;
    margin-top: 20px;
    left: 0;
    background-color: rgb(132, 130, 252);
    width: calc(100vw - 180px);
    z-index: -2;
    margin-left: 180px;
    text-align: center;
}
</style>