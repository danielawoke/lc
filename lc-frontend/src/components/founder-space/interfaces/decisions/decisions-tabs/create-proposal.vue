<script setup>
import { useRoute, useRouter } from 'vue-router'
import { defineComponent, nextTick, onMounted, watch } from 'vue';
import { AccountLocal } from '@/lib/appwrite';
import { ref } from 'vue';
import axios from 'axios';
const apiURL = import.meta.env.VITE_APP_API_URL;
const route = useRoute();
import ProposalArchive from '@/components/founder-space/interfaces/decisions/decisions-popups/proposal-archive-popup.vue';
useRouter(); 

let props = defineProps({    
    scrollable: Array,
})

let jobs = ref([
    {id: 1, title: "Software Engineer", description: "Description for Job 1"},
    {id: 2, title: "Product Manager", description: "Description for Job 2"},
    {id: 3, title: "Designer", description: "Description for Job 3"},
    {id: 4, title: "Data Analyst", description: "Description for Job 4"},
    {id: 5, title: "DevOps Engineer", description: "Description for Job 5"},
    {id: 6, title: "QA Engineer", description: "Description for Job 6"},
    {id: 7, title: "Marketing Specialist", description: "Description for Job 7"},
    {id: 8, title: "Sales Representative", description: "Description for Job 8"},
    {id: 9, title: "HR Manager", description: "Description for Job 9"},
    {id: 10, title: "Finance Analyst", description: "Description for Job 10"},
]);

let OfferTabCandidateInfo = ref(["Null", "Null"]);
let offerJobTab = ref(1);
let offerCandidateTab = ref(1);
let selection = ref(0);
let currentThreshold = ref("67%");
let proposalSumbited = ref(false);
let filteredOfferJobs = ref(jobs.value);
let TabedFilteredOfferJobs = ref(filteredOfferJobs.value.slice(0,8));
// this will be from an api call and will be left as null otherwise
let OfferSelectedJobCandidates = ref([
    // {id: 1, name: "john", application: "link", discussion: "link", jobTitle: "Software Engineer"},
    // {id: 2, name: "sarah", application: "link", discussion: "link", jobTitle: "Product Manager"},
    // {id: 3, name: "michael", application: "link", discussion: "link", jobTitle: "Software Engineer"},
    // {id: 4, name: "emily", application: "link", discussion: "link", jobTitle: "Designer"},
    // {id: 5, name: "david", application: "link", discussion: "link", jobTitle: "Data Analyst"},
    // {id: 6, name: "laura", application: "link", discussion: "link", jobTitle: "Product Manager"},
    // {id: 7, name: "robert", application: "link", discussion: "link", jobTitle: "Software Engineer"},
]);
let filteredOfferCandidates = ref(OfferSelectedJobCandidates.value);
let TabedFilteredOfferCandidates = ref(filteredOfferCandidates.value.slice(0,5));
let removeMemeberTab = ref(1);
let memebers = ref([
    // {id: 1, name: "john", profile: "link"},
    // {id: 2, name: "ito", profile: "link"},
    // {id: 3, name: "michael", profile: "link"},
    // {id: 4, name: "emily", profile: "link"},
    // {id: 5, name: "david", profile: "link"},
    // {id: 6, name: "laura", profile: "link"},
    // {id: 7, name: "robert", profile: "link"},
]);
let filteredMembers = ref(memebers.value);
let TabedFilteredMembers = ref(filteredMembers.value.slice(0,5));
let selectedMember = ref("Null");
let user = null

onMounted(async () => {

    user = await AccountLocal.get();

    await axios.get(`${apiURL}projects/votes/load_discussions/${route.params.projectId}`).then((response) => {
        console.log(response.data.chat_layout.Discussions);
        for (let job of response.data.chat_layout.Discussions){
            for (let candidate of job.Candidates){
                OfferSelectedJobCandidates.value.push({id: candidate.user_id, name: candidate.name, application: "link", discussion: "link", jobTitle: job.Job, proposal: candidate.proposal_saved, job_id: job.job_id});
            }
        }
        filteredOfferCandidates.value = OfferSelectedJobCandidates.value;
        TabedFilteredOfferCandidates.value = filteredOfferCandidates.value.slice(0,5);
    }).catch((error) => {
        console.log(error);
    })

    axios.get(`${apiURL}projects/votes/load_members/${route.params.projectId}`).then((response) => {
        memebers.value = response.data.members;
        filteredMembers.value = memebers.value;
        TabedFilteredMembers.value = filteredMembers.value.slice(0,5);
    }).catch((error) => {
        console.log(error);
    })

    await nextTick();
    document.getElementById("select").addEventListener("change", async (e) => {
        selection.value = e.target.value;
        await nextTick();
        backgroundResize();
    });
    backgroundResize();
    window.addEventListener("resize", backgroundResize);
});

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


async function submitProposal(type){
    // api call to submit proposal here
    
    if(type == "Offer Position"){
        console.log(OfferTabCandidateInfo.value);
        if(OfferTabCandidateInfo.value[1] == "Null"){
            alert("Please select a candidate for the offer position proposal");
            return;
        }

        try{
            
            await axios.post(`${apiURL}projects/votes/create_proposal/${route.params.projectId}/${user.$id}/${OfferTabCandidateInfo.value[1].job_id}/`, {
                type: type,
                offer_position_data:OfferTabCandidateInfo.value[1],
                context: document.getElementById("proposal-context").value,
            }).then((response) => {
                console.log(response);
            }).catch((error) => {
                console.log(error);
            })
        }catch(e){
            console.log(e);
            return;
        }
    }else if(type == "Remove Member") {
        
        if(selectedMember.value == "Null"){
            alert("Please select a candidate for the offer position proposal");
            return;
        }
        
        try{
            await axios.post(`${apiURL}projects/votes/create_proposal/${route.params.projectId}/${user.$id}/${0}/`, {
                type: type,
                remove_member_data: selectedMember.value,
                context: document.getElementById("proposal-context").value,
            }).then((response) => {
                console.log(response);
            }).catch((error) => {
                console.log(error);
            })
        }catch(e){
            console.log(e);
            return;
        }
    }else if(type == "Direct Invite"){

        if(!verfiedUserAt.value){
            alert("Please enter a valid @ for the direct invite proposal");
            return;
        }
        try{
            await axios.post(`${apiURL}projects/votes/create_proposal/${route.params.projectId}/${user.$id}/${0}/`, {
                type: type,
                inviteTag: document.getElementById("invite_tag").value,
                context: document.getElementById("proposal-context").value,
            }).then((response) => {
                console.log(response);
            }).catch((error) => {
                console.log(error);
            })
        }catch(e){
            console.log(e);
            return;
        }
    }


    proposalSumbited.value = true;
    await nextTick();
    backgroundResize();
}

function selectJob(event, el){
    OfferTabCandidateInfo.value[0] = el;
    OfferTabCandidateInfo.value[1] = "Null";
}
function selectCandidate(event, el){
    console.log(el);
    OfferTabCandidateInfo.value[1] = el;
}
function backSelectCandidate(){
    OfferTabCandidateInfo.value[0] = "Null";
    OfferTabCandidateInfo.value[1] = "Null";
}

function filter(search){
    offerJobTab.value = 1;
    filteredOfferJobs.value = jobs.value.filter(el => {
        if(el.title.toString().toLowerCase().includes(search.toLowerCase())){
            return el;
        }
    })
    TabedFilteredOfferJobs.value = filteredOfferJobs.value.slice(0,8);
}
function offerTabSelect(tabNum){
    offerJobTab.value = tabNum;
    TabedFilteredOfferJobs.value = filteredOfferJobs.value.slice((tabNum-1)*8, (tabNum-1)*8 + 8);
}
function prevOfferJobTab(){
    if(offerJobTab.value > 1){
        offerJobTab.value = offerJobTab.value - 1;
        TabedFilteredOfferJobs.value = filteredOfferJobs.value.slice((offerJobTab.value-1)*8, (offerJobTab.value-1)*8 + 8);
    }
}
function nextOfferJobTab(){
    if(offerJobTab.value < Math.ceil(filteredOfferJobs.value.length/8)){
        offerJobTab.value = offerJobTab.value + 1;
        TabedFilteredOfferJobs.value = filteredOfferJobs.value.slice((offerJobTab.value-1)*8, (offerJobTab.value-1)*8 + 8);
    }
}
function filterOfferCandidates(search){
    offerCandidateTab.value = 1;
    filteredOfferCandidates.value = OfferSelectedJobCandidates.value.filter(el => {
        if(el.name.toString().toLowerCase().includes(search.toLowerCase())){
            return el;
        }
    })
    TabedFilteredOfferCandidates.value = filteredOfferCandidates.value.slice(0,5);
}
function offerCandidateTabSelect(tabNum){
    offerCandidateTab.value = tabNum;
    TabedFilteredOfferCandidates.value = filteredOfferCandidates.value.slice((tabNum-1)*5, (tabNum-1)*5 + 5);
}

function removeMemeberFilter(search){
    console.log(search);
    removeMemeberTab.value = 1;
    filteredMembers.value = memebers.value.filter(el => {
        if(el.name.toString().toLowerCase().includes(search.toLowerCase())){
            return el;
        }
    })
    TabedFilteredMembers.value = filteredMembers.value.slice(0,5);
}
function removeMemeberTabChange(tabNum){
    removeMemeberTab.value = tabNum;
    TabedFilteredMembers.value = filteredMembers.value.slice((tabNum-1)*5, (tabNum-1)*5 + 5);
}
function removeSelectedMember(el){
    if(selectedMember.value == el){
        selectedMember.value = "Null";
    }
    else{
        selectedMember.value = el;
    }
}

let verfiedUserAt = ref(false);

async function verifyAt(at){
    verfiedUserAt.value = false;

    let valid = document.getElementById("valid-at");
    let invalid = document.getElementById("invalid-at");
    let loading = document.getElementById("loading-at");
    valid.style.display = "none";
    invalid.style.display = "none";
    loading.style.display = "block";

    await axios.get(`${apiURL}users/search/verify_at/${at}`).then((response) => {
        if(response.data.valid){
            verfiedUserAt.value = true;
            valid.style.display = "block";
            invalid.style.display = "none";
            loading.style.display = "none";
        }else{
            verfiedUserAt.value = false;
            valid.style.display = "none";
            invalid.style.display = "block";
            loading.style.display = "none";
        }
    }).catch((error) => {
        console.log(error);
        verfiedUserAt.value = false;
        valid.style.display = "none";
        invalid.style.display = "block";
        loading.style.display = "none";
    });

}
function thresholdErrorCheck(number){
    let input = number;
    let NANError = document.getElementById("NAN-error");
    let outBoundPercentageError = document.getElementById("out-bound-percetage-error");
    let outBoundFractionError = document.getElementById("out-bound-fraction-error");
    let nothing = document.getElementById("nothing");
    NANError.style.display = "none";
    outBoundPercentageError.style.display = "none";
    outBoundFractionError.style.display = "none";
    nothing.style.display = "block";
    if(number == ""){
        return;
    }
    if(isNaN(input)){
        if(input.includes("/")){
            let splitInput = input.split("/");
            if(splitInput.length == 2 && (!isNaN(splitInput[0]) && !isNaN(splitInput[1]))){
                if(splitInput[0]/splitInput[1] > 1 || splitInput[0]/splitInput[1] <= 0){
                    nothing.style.display = "none";
                    outBoundFractionError.style.display = "block";
                }
            }
            else{
                nothing.style.display = "none";
                NANError.style.display = "block";
            }
        }
        else{
            nothing.style.display = "none";
            NANError.style.display = "block";
        }
    }
    else{
        if(input > 100 || input <= 0){
            nothing.style.display = "none";
            outBoundPercentageError.style.display = "block";
        }
    }
}

async function save(){
    saveChanges.value = true;
    await nextTick();

    //logic to save the changes and submit the proposal to the member base for review
}


let decisionPopup = ref([false, "Null"]);
let popupData = ref(null);

async function viewProposal(el){
    decisionPopup.value[0] = true;
    props.scrollable[0] = 'hidden';
    popupData.value = el;
    console.log(popupData.value);
    await nextTick();
    document.getElementById('popup-backdrop').style.top = document.getElementById("total-container").scrollTop + 'px';
    document.getElementById('popup').style.top = document.getElementById("total-container").scrollTop + 'px';
}

</script>
<template>

    <ProposalArchive v-if="decisionPopup[0]" :userID="userID" :renderVar="decisionPopup" :scrollable="scrollable" :decision="popupData" :id="selectedId" :allDecisions="coMemberProposals" :selectedProposalCount="selectedProposalCount"/>
    
    <div class="background">
        <div class="configuration-container">
            <div v-if="!proposalSumbited">
                <div class="question">
                    <div class="question-text">
                        Select type of proposal you'd like to make:
                    </div>
                    <div class="yes-no-container">
                        <select id="select" class="job-tab-selection">
                            <option :value="0">~Click to Select~</option>
                            <!-- <option :value="1">1. Start Discussion</option> -->
                            <option :value="2">Offer Position</option>
                            <option :value="3">Direct Invite</option>
                            <!-- <option :value="4">Change Voting Threshold</option> -->
                            <option :value="5" style="color:red" >Remove Member</option>
                        </select>
                    </div>
                </div>
                <br>
                <br>
                <br>
                <div v-if="selection==0"></div>
                <div v-else-if="selection==1">
                    <div class="question">
                        <div class="question-text">
                            Enter the @ of the person you'd like to start a discussion with
                        </div>
                        <div class="search-container">
                            <input v-on:input="verifyAt($event.target.value)" class="job-search" placeholder="Enter @ of candidate from pool"/>
                            
                            <!-- <div class="search-drop-down">
                                <div class="drop-down-entry">sdadasd</div>
                            </div>     -->
                        </div>
                        
                        <div style="height:80px;">
                            <img  style="display:none;" id="loading-at" class="meta-search-text-image" src="@/assets/founder-space/decisions/loading.gif" />
                            <div style="display:none;" id="valid-at" class="meta-search-text">@ is valid <b style="color:green">✔</b></div>
                            <div id="invalid-at" style="color:cyan; display:none" class="meta-search-text">@ is invalid</div>
                        </div>
                    
                    </div>
                    <div class="question">
                        <div class="question-text">
                            Provide context for this propsal
                        </div>
                        <textarea id="proposal-context" class="proposal-context" placeholder="Enter context for this proposal...">No context given</textarea>
                    </div>

                    <div class="question">
                    <div class="Save" @click="submitProposal">
                        Sumbit Proposal
                    </div>
                </div>

                </div>
                <div v-else-if="selection==2">
                    <div class="question">
                        <div>
                            <div class="question-text">
                                Select the candidate you'd like to give an offer to 
                            </div>
                            <div class="question-text" style="font-size:12px; color:#888888; margin-top:-10px; margin-bottom:10px;">
                                these are only candidates who are in discussion for this role
                            </div>
                            <div class="meta-jobs-container">
                                <input v-on:input="filterOfferCandidates($event.target.value)" style="padding-right:10px; width:calc(100% - 20px); border-radius:0;" type="text" class="job-search" placeholder="Search candidate..."/>
                                <!-- <div class="job-nav">
                                    <div class="buttons-tray">
                                        <span>
                                            <label @click="backSelectCandidate" class="meta-button-bottom-left"><b>⇐</b> Back to Job Selection</label>
                                        </span>
                                    </div>
                                </div>   -->
                                <div style="min-height:300px;">
                                    <div v-for="el in TabedFilteredOfferCandidates" class="job" @click.self="selectCandidate($event.target, el)" :style="OfferTabCandidateInfo[1]==el? 'filter: hue-rotate(-35deg); background-image: linear-gradient(to bottom, #33c2ff, #2672ff); color: black; border-bottom: #afdbff solid 3px;':''">
                                        <div @click.self="selectCandidate($event.target, el)" style="margin-bottom:-10px;" class="job-title">
                                            {{ el.name }}
                                        </div>
                                        <div style="font-style:italic; font-size:12px; color:#888888; margin-top:10px; margin-left:-0px">
                                            {{el.jobTitle}}
                                        </div>
                                        <div @click.self="selectCandidate($event.target, el)" class="buttons-tray">
                                            <!-- application will bring up popup, discussion will be a new tab -->
                                            <div @click="viewProposal(el)" class="meta-button-bottom-left" style="opacity: 1;">View Proposal</div>
                                            <div class="meta-button-bottom-left" style="opacity: 1;">View Discussion</div>
                                        </div>
                                    </div>  
                                </div>  
                                <div class="tab">
                                    <div class="tabs"> 
                                        <div @click="offerCandidateTabSelect(offerCandidateTab - 1)" class="taber">Prev</div>
                                        <div class="tab-container">
                                            <input v-on:input="offerCandidateTabSelect($event.target.value)" style="width:25px; border-radius:5px;" class="tab-input" :value="offerCandidateTab"/>
                                            <div class="total" >/<div class="remainingTabs">{{ Math.ceil(filteredOfferCandidates.length/5) }}</div></div>
                                        </div>
                                        <div @click="offerCandidateTabSelect(offerCandidateTab + 1)" class="taber">Next</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <!-- <div>
                            <div class="question-text">
                                Select the job you'd like to offer
                            </div>
                            <div class="meta-jobs-container">
                                <input style="padding-right:10px; width:calc(100% - 20px); border-radius:0;" type="text" class="job-search" placeholder="Search jobs..."  v-on:input="filter($event.target.value)"/>
                                <div class="job-nav">
                                    <div class="buttons-tray">
                                        <span></span>
                                    </div>
                                </div>  
                                <div style="min-height:300px;">
                                    <div v-for="el in TabedFilteredOfferJobs" class="job" @click="selectJob($event.target, el)" :style="OfferTabCandidateInfo[0]==el? 'background-image: linear-gradient(to bottom, rgba(163, 172, 255, 0.267), rgba(105, 245, 255, 0.89)); border-bottom: #afdbff solid 3px;':''">
                                        <div class="job-title">
                                            {{ el.title }}
                                        </div>
                                    </div>    
                                </div>
                                <div class="tab">
                                    <div class="tabs"> 
                                        <div @click="prevOfferJobTab()" class="taber">Prev</div>
                                        <div class="tab-container">
                                            <input v-on:input="offerTabSelect($event.target.value)" style="width:25px; border-radius:5px;" class="tab-input" :value="offerJobTab"/>
                                            <div class="total" >/<div class="remainingTabs">{{ Math.ceil(filteredOfferJobs.length/8) }}</div></div>
                                        </div>
                                        <div @click="nextOfferJobTab()" class="taber">Next</div>
                                    </div>
                                </div>  
                            </div>
                        </div> -->
                    </div>
                    <div class="question">
                        <div class="question-text">
                            Provide context for this propsal
                        </div>
                        <textarea id="proposal-context" class="proposal-context" placeholder="Enter context for this proposal...">No context given</textarea>
                    </div>
                    <div class="question">
                        <div class="Save" @click="submitProposal('Offer Position')">
                            Sumbit Proposal
                        </div>
                    </div>
                </div>
                <div v-else-if="selection==3">
                    <div class="question">
                            <div class="question-text">
                                Enter the @ of the person you'd like to invite
                            </div>
                            <div class="search-container">
                                <input v-on:input="verifyAt($event.target.value)" class="job-search" id="invite_tag" placeholder="Enter @ of the user you'd like to propose an invite to"/>
                            </div>
                            
                            <div style="height:80px;">
                                <img  style="display:none;" id="loading-at" class="meta-search-text-image" src="@/assets/founder-space/decisions/loading.gif" />
                                <div style="display:none;color:green;filter:hue-rotate(180deg)" id="valid-at" class="meta-search-text">@ is valid <b style="color:green;">✔</b></div>
                                <div id="invalid-at" style="color:cyan; display:none;" class="meta-search-text">@ is invalid</div>
                            </div>
                        </div>
                        <div class="question">
                            <div class="question-text">
                                Provide context for this propsal
                            </div>
                            <textarea id="proposal-context" class="proposal-context" placeholder="Enter context for this proposal...">No context given</textarea>
                        </div>

                        <div class="question">
                        <div class="Save" @click="submitProposal('Direct Invite')">
                            Sumbit Proposal
                        </div>
                    </div>
                </div>
                <div v-else-if="selection==4">
                    <div class="question">
                        <div class="question-text">
                            Enter the new voting threshold you'd like to set (current is {{ currentThreshold }})
                        </div>
                        <div style="font-size:14px; margin-top:-10px;color:gray" class="question-text">
                            Enter as fraction or percent number (ex. 2/3 or 67.4)
                        </div>
                        <input v-on:input="thresholdErrorCheck($event.target.value)" style="width:150px; padding:10px; font-size:15px; margin-top:0px;" class="job-search" placeholder="Enter new threshold..." />
                        <div id="nothing" style="color:white; margin-top:10px; display:block;">~</div>
                        <div id="NAN-error" style="color:cyan; margin-top:10px;display:none" >Not a number</div>
                        <div id="out-bound-percetage-error" style="color:cyan; margin-top:10px;display:none" >Value must be between 0 and 100 if numeric percentage</div>
                        <div id="out-bound-fraction-error" style="color:cyan; margin-top:10px;display:none" >Value must be between 0 and 1 if fractional</div>
                    </div>
                    <div class="question">
                        <div class="question-text">
                            Provide context for this propsal
                        </div>
                        <textarea id="proposal-context" class="proposal-context" placeholder="Enter context for this proposal...">No context given</textarea>
                    </div>

                    <div class="question">
                        <div class="Save" @click="submitProposal">
                            Sumbit Proposal
                        </div>
                    </div>
                </div>
                <div v-else-if="selection==5">
                    <!-- <div class="question">
                        <div class="question-text">
                            <b>Important:</b> If 25% of members choose to withdraw from the vote, the proposal will be thrown out completely. In addition to this, <b style="color:cyan;">members will NOT be able to vote anonymously on this proposal.</b> Removing a member is a serious action. Please use this judiciously.
                        </div>
                    </div> -->
                    <div class="question">
                        <div class="question-text">
                            Select the member you'd like to propose to remove:
                        </div>
                        <div class="meta-jobs-container">
                            <input v-on:input="removeMemeberFilter($event.target.value)" style="padding-right:10px; width:calc(100% - 20px); border-radius:0;" type="text" class="job-search" placeholder="Search Member..." />
                            <div style="min-height:300px;">
                                <div v-for="el in TabedFilteredMembers" class="job" :style="selectedMember==el?  'filter: hue-rotate(-35deg); background-image: linear-gradient(to bottom, #33c2ff, #2672ff); color: black; border-bottom: #afdbff solid 3px;':''" @click.self="removeSelectedMember(el)">
                                    <div style="margin-bottom:-10px" class="job-title" @click.self="removeSelectedMember(el)">{{ el.name }}</div>
                                    <div class="buttons-tray" @click.self="removeSelectedMember(el)">
                                        <!-- profile will be a seperate tab -->
                                        <RouterLink class="meta-button-bottom-left" style="opacity: 1;" :to="`/profile/${el.usertag}`">View Profile</RouterLink>
                                    </div>
                                </div>    
                            </div>
                            <div class="tab">
                                <div class="tabs"> 
                                    <div @click="removeMemeberTabChange(removeMemeberTab-1)" class="taber">Prev</div>
                                    <div class="tab-container">
                                        <input v-on:input="removeMemeberTabChange($event.target.value)" style="width:25px; border-radius:5px;" class="tab-input" :value="removeMemeberTab"/>
                                        <div class="total" >/<div class="remainingTabs">{{Math.ceil(filteredMembers.length/5)}}</div></div>
                                    </div>
                                    <div @click="removeMemeberTabChange(removeMemeberTab+1)" class="taber">Next</div>
                                </div>
                            </div>  
                        </div>
                    </div>
                    <div class="question">
                        <div class="question-text">
                            Provide context for this propsal
                        </div>
                        <textarea id="proposal-context" class="proposal-context" placeholder="Enter context for this proposal...">No context given</textarea>
                    </div>
                    <div class="question">
                        <div class="Save" @click="submitProposal('Remove Member')">
                            Sumbit Proposal
                        </div>
                    </div>
                </div>
            </div>
            <div v-else>
                <div class="header-text">
                    Proposal Sumbited!
                </div>
                <div class="meta-text">
                    Your proposal has been sumbited to the member base for review. You can monitor its progress in the Decisions tab of the Founder Space.
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.proposal-context{
    width: calc(100%);
    height: 150px;
    border-radius: 10px;
    padding: 10px;
    font-family: sans-serif;
    font-size: 16px;
    color:#555555;
    outline: none;
    border: #cccccc solid 2px;
    resize: none;
}
.meta-search-text-image{
    width: 90px;
    height: auto;
    margin-right: 0px;
    vertical-align: middle;
    float: right;
}
.drop-down-entry{
    font-family: sans-serif;
    font-size: 16px;
    color:#555555;
    text-align: left;
    padding: 10px;
    cursor: pointer;
}
.search-drop-down{
    position: absolute;
    background-color: #d6d6d6;
    width: calc(90%);
    top: 40px;
    left: 5px;
    z-index: 1000;
    height: 100px;
}
.meta-search-text{
    font-family: sans-serif;
    font-size: 16px;
    color:#555555;
    text-align: left;
    padding-right: 10px;
    padding-top: 10px;
    float: right;
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
    padding:10px;
    padding-top:0px;
    padding-bottom:10px;
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
    width:100%;
    border:none;
    height: 40px;
    border-radius: 5px;
    color: rgb(189, 189, 189);
    background-color: #ffffff00;
    font-weight: bolder;
    outline: none;
    background: black;
    padding: 10px;
}
.tab-input{
    font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
    font-weight: bold;
    text-align: center;
    width: 50px;
    height: 30px;
    background-image: linear-gradient(45deg, #ffffff, #d1d1d1);
    border: solid 3px #b3b3b3;
    color: rgb(54, 54, 54);
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
    width: calc(95%);
    padding: 10px;
    font-size: 16px;
    margin:auto;
    outline: none;
    border: none;
    color:rgb(0, 0, 0);
    background-color: #dddddd;
    position: relative;
    z-index: 10;
    border-radius: 10px;
}
.search-button-container{
    display: inline-block;
    background-color: #ffffff;
    position: absolute;
    box-shadow: #0000003a 0px 0px 5px;
    width:35px;
    height:35px;
    padding: 0px;
    margin-left: -40px;
    margin-top: 2px;
    z-index: 100;
    border-radius: 50%;
}
.search-icon{
    width: 60%;
    height: 60%;
    margin: 20%;
    display: block;
    justify-content: center;
    align-items: center;
    cursor: pointer;
}
.meta-jobs-container{
    width: 100%;
    overflow: auto;
    background-color: #c4c4c459;
}
.question-text{
    font-family: sans-serif;
    font-size: 16px;
    color:#555555;
    text-align: left;
    padding-bottom: 20px;
    display:block;
}
.buttons-tray{
    display: block;
    margin-top: 10px;
    left:0;
    height:20px;
}
.job-title{
    display:block;
    height:fit-content;
    width:fit-content;
    font-weight: bold;
    padding-bottom: 10px;
}
.job{
    position: relative;
    display:block;
    text-align: left;
    background-image: linear-gradient(to bottom, white, rgb(235, 231, 231));
    border-bottom: #d3d3d3 solid 3px;
    z-index: 1000;
    height: auto;

}
.job:hover{
    background-image: linear-gradient(to bottom, rgb(255, 255, 255), rgb(255, 255, 255));
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
    float:left;
    display: block;
    margin-top: 0px;
    left:0;
    width:100%;
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
    cursor: pointer;
    transition: all 0.3s ease;
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
.search-container{
    width: 100%;
    height:40px;
    outline: none;
    background-color: #fafafa59;
    border-radius: 10px;
    position: relative;
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
    width:fit-content;
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
    padding: 5px;
    padding-right: 5px;
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