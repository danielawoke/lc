<script setup>
import { useRoute, useRouter } from 'vue-router'
import { nextTick, onMounted,onUnmounted, watch } from 'vue';
import { ref } from 'vue';
import DecisionPopup from '@/components/founder-space/interfaces/decisions/archive-popups/decision-popup.vue';
import CandidatePopup from '@/components/founder-space/interfaces/decisions/archive-popups/candidate-popup.vue';
import MassDelegate from '@/components/founder-space/interfaces/decisions/archive-popups/mass-delegate.vue';
import axios from 'axios';
import { createClient } from '@supabase/supabase-js';
const supabase = createClient(import.meta.env.VITE_SUPABASE_URL, import.meta.env.VITE_SUPABASE_ANON_KEY);
import {AccountLocal} from '@/lib/appwrite'
const apiURL = import.meta.env.VITE_APP_API_URL;
const route = useRoute();

let props = defineProps({
    scrollable: Array
});

let jobs = ref([
    {
        title: "Software Engineer", 
        candidates:[
            {name: "Mother of two kidssa", desc: "Mother of two kids"},
            {name: "Ramuja sa as sa sa sa", desc: "Mother of two kidsMother of two kidsMother of two kidsMother of two kidsMother of two kidsMother of two kidsMother of two kids"},
            {name: "Ramuja sa as sa sa sa", desc: "Mother of two kids"}
        ]
    },
    {
        title: "Product Designer", 
        candidates:[
            {name: "Mother of two kidssa", desc: "Mother of two kids"},
            {name: "Ramuja sa as sa sa sa", desc: "Mother of two kidsMother of two kidsMother of two kidsMother of two kidsMother of two kidsMother of two kidsMother of two kids"},
            {name: "Ramuja sa as sa sa sa", desc: "Mother of two kids"}
        ]
    },
    {
        title: "Marketing Lead", 
        candidates:[
            {name: "Mother of two kidssa", desc: "Mother of two kids"},
            {name: "Ramuja sa as sa sa sa", desc: "Mother of two kidsMother of two kidsMother of two kidsMother of two kidsMother of two kidsMother of two kidsMother of two kids"},
            {name: "Ramuja sa as sa sa sa", desc: "Mother of two kids"}
        ]
    },
    
]);

let filteredJobs = ref(jobs.value);

let coMemberProposals = ref([
    // {id:1, type:"Offer Position", name:"Jaliyah WhitneyJaliyah WhitneyJaliyah WhitneyJaliyah Whitney", role:"Maze DesignerMaze ", select:false, decision:"In Favor", delegateTo:[-1]},
    // {id:242324, type:"Start Discussion", name:"Jaliyah Whitney", role:"Maze Designer",select:false, "decision":"Against", delegateTo:[-1]},
    // {id:3, type:"Offer Membership", name:"Jaliyah Whitney",select:false, decision:"Withdraw", delegateTo:[-1]},
    // // Use the member ID to refer to the delegated member
    // {id:4, type:"Remove Member", name:"Jaliyah Whitney",select:false, decision:"Delegate", delegateTo:[1]},
    // {id:5, type:"Change Vote Threshold", select:false, decision:"In Favor", delegateTo:[-1]},
]);

let selectedProposalCount = ref([0]);


let rejectedCandidates = ref([
    // {id:1,name: "Sergant p", role: "Mother of two kids", pinned:[false]},
    // {id:2,name: "Ramuja sa as sa sa sa", role: "Mother of two kidsMother of two kidsMother of two kidsMother of two kidsMother of two kidsMother of two kidsMother of two kids", pinned:[false]},
    // {id:3,name: "zebera za", role:"web3 specialist", pinned:[false]},
    // {id:4,name: "sad za", role:"product designer", pinned:[false]},

]);

let filteredRejectedCandidates = ref(rejectedCandidates.value);

let candidateSelected = ref(true);
let candidateInfo = ref({});
let userID = ref(-1);
let channel = null;
onMounted(async () => {

    let user = await AccountLocal.get();
    userID.value = user.$id;
    await axios.get(`${apiURL}projects/votes/load_signed_proposals/${route.params.projectId}/${user.$id}`).then((response) => {
        coMemberProposals.value = response.data;
    });

    channel = supabase
                .channel('candidates')
                .on(
                    'postgres_changes',
                    {
                    event: 'INSERT',
                    schema: 'public',
                    table: 'proposals',
                    filter: `user_id=eq.${userID.value}`
                    },
                    async (payload) => {
                        if(payload.new.project_id == route.params.projectId && payload.new.voted == true){

                            let dom = document.getElementById('jobs-container');
                            let prevWidth = dom.scrollWidth;
                            coMemberProposals.value.unshift(payload.new);
                            await nextTick();
                            let diff = dom.scrollWidth - prevWidth;
                            if(dom.scrollLeft < 200){
                                dom.scrollLeft = 0;
                            }else{
                                dom.scrollLeft = dom.scrollLeft + diff;
                            }
                        }
                    }
                )
                .subscribe();

    await nextTick();
    fontAdjust();

});

onUnmounted(() => {
    if (channel) {
        supabase.removeChannel(channel);
    }
});

function filterJobs(search){
    filteredJobs.value = jobs.value.filter(job => job.title.toLowerCase().includes(search.toLowerCase()));
}

function fontAdjust(){
    let names = document.getElementsByClassName('people-listing-name');
    for(let i = 0; i < names.length; i++){
        let name = names[i];
        console.log(name.offsetHeight);
        if(name.offsetHeight > 40){
            name.style.top = "12px";
        }
        let fontSize = 16;
        while(name.offsetHeight > 50){
            fontSize--;
            name.style.fontSize = fontSize + "px";
        }
    }
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

function toggleProposalSelect(proposal){
    if(proposal.select){
        selectedProposalCount.value[0] -= 1;
    }
    else{
        selectedProposalCount.value[0] += 1;
    }
    proposal.select = !proposal.select;
}
function selectAllProposals(){
    for(let proposal of coMemberProposals.value){
        proposal.select = true;
    }
    selectedProposalCount.value[0] = coMemberProposals.value.length;
}
function deselectAllProposals(){
    for(let proposal of coMemberProposals.value){
        proposal.select = false;
    }
    selectedProposalCount.value[0] = 0;
}

function filterRejectedCandidates(search){
    filteredRejectedCandidates.value = rejectedCandidates.value.filter(candidate => candidate.preview_data.name.toLowerCase().includes(search.toLowerCase()));
    fontAdjust();
}

let decisionPopup = ref([false]);
let candidatePopup = ref([false]);
let massDelegatePopup = ref([false]);
let selectedId = ref(-1);
let popupData = ref({});
let candidateObject = ref({});

async function openDecisionPopup(proposal){

    // You need to use the proposal here to change what is getting passed into the decision popup

    selectedId.value = proposal.proposal_id;
    candidateObject.value = proposal;

    await axios.get(`${apiURL}projects/votes/load_proposal_data/${proposal.proposal_id}`).then(response => {
        popupData.value = response.data[0];
        popupData.value.type = proposal.proposal_meta_cache.type;
        popupData.value.vote = proposal.vote;
        popupData.value.delegate_id = [proposal.delegate_id];
    }).catch(error => {
        console.error("Error fetching candidate info:", error);
    });
    
    proposal.err = false;
    props.scrollable[0] = 'hidden';
    decisionPopup.value[0] = true;

    await nextTick();
    document.getElementById('popup-backdrop').style.top = document.getElementById("total-container").scrollTop + 'px';
    document.getElementById('popup').style.top = document.getElementById("total-container").scrollTop + 'px';

}

async function withdrawSelected(){
    // This function will need to interact with the backend to withdraw the user's vote from the selected proposals, but for now we will just deselect them and reset the count.
    let i = 0;
    while(i<coMemberProposals.value.length){
        let proposal = coMemberProposals.value[i];
        if(proposal.select){
            try{
                await axios.post(`${apiURL}projects/votes/cast_vote/${userID.value}/${proposal.proposal_id}`, {
                    vote: "withdraw"
                });
                coMemberProposals.value.splice(i, 1);
            }catch(error){
                console.error("Error withdrawing vote:", error);
                i++;
            }
        }
        else{
            i++;
        }
    }
    selectedProposalCount.value[0] = 0;
    await nextTick();
    fontAdjust();
}

function openMassDelegatePopup(){
    props.scrollable[0] = 'hidden';
    massDelegatePopup.value[0] = true;
    nextTick().then(() => {
        document.getElementById('popup-backdrop').style.top = document.getElementById("total-container").scrollTop + 'px';
        document.getElementById('popup').style.top = document.getElementById("total-container").scrollTop + 'px';
    });
}

async function candidatePopupOpen(candidate){

    let applicant_id = candidate.application_id;
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


let errorLog = ref([""]);

</script>

<template>
    
    <DecisionPopup v-if="decisionPopup[0]" :userID="userID" :renderVar="decisionPopup" :scrollable="scrollable" :decision="popupData" :id="selectedId" :allDecisions="coMemberProposals" :selectedProposalCount="selectedProposalCount"/>
    <MassDelegate v-if="massDelegatePopup[0]" :renderVar="massDelegatePopup" :userID="userID" :errorLog="errorLog" :scrollable="scrollable" :candidate="popupData" :allDecisions="coMemberProposals" />
    <CandidatePopup v-if="candidatePopup[0]" :renderVar="candidatePopup" :scrollable="scrollable" :candidate="popupData" :candidateObject="candidateObject" :id="selectedId" />
    
    <div class="decision-row">
        <div class="header-text">
            Signed Undetermined Co-Member Proposals 
        </div>
        <hr class="line"/> 
        <div class="roles">
            <div class="left"><</div>
            <div class="roles-container-inline-correction" id="jobs-container">
                <div v-if="coMemberProposals.length==0">
                    <div class="no-results-text">Nothing for now...</div>
                    <img class="nothing-for-now-image" src="@/assets/founder-space/decisions/nothing-for-now.png"/>
                </div>
                <div class="roles-container">
                    
                    <!-- Extend Offer for Role (For a specific role, add member )
                         Add Member (In genearl, can be anyone)
                         Start Discussion with Cadidate (From pool) -->
                    <div v-for="proposal in coMemberProposals" class="role-with-select" :style="proposal.err ? 'box-shadow: 0 0 15px cyan; background: rgb(200, 255, 255)' : ''">
                        <div @click="toggleProposalSelect(proposal)" class="select" :style="proposal.select ? 'background-color: #007bff;' : 'background-color: transparent;'"></div>
                        <div @click.self="openDecisionPopup(proposal)" style="background-color:transparent; padding:6px; margin:-6px; height:100%;width:100%;">
                            <div @click.self="openDecisionPopup(proposal)" class="role-title">{{proposal.proposal_meta_cache.type}}</div>
                            <div v-if="proposal.proposal_meta_cache.type=='Start Discussion' || proposal.proposal_meta_cache.type=='Offer Position'">
                                <div @click.self="openDecisionPopup(proposal)" class="prev-name" >{{proposal.proposal_meta_cache.name}}</div>
                                <div @click.self="openDecisionPopup(proposal)" class="role-info"><i @click.self="openDecisionPopup(proposal)" style="font-style:lighter;">{{proposal.proposal_meta_cache.role}}</i></div>
                                <div @click.self="openDecisionPopup(proposal)" style="position:absolute; top: 85px;">
                                    <!-- <div class="sub-profile-image"></div>
                                    <div class="sub-profile-image"></div> -->
                                    <!-- <div class="sub-profile-image"></div>
                                    <div class="sub-profile-image"></div>
                                    <div class="remaining">+99</div> -->
                                </div>
                            </div>
                            <div v-else-if="proposal.proposal_meta_cache.type=='Remove Member' || proposal.proposal_meta_cache.type=='Direct Invite'">
                                <div @click.self="openDecisionPopup(proposal)" class="larger-prev-name" >{{proposal.proposal_meta_cache.name}}</div>
                                <div style="position:absolute; top: 85px;">
                                    <!-- <div class="sub-profile-image"></div>
                                    <div class="sub-profile-image"></div> -->
                                </div>
                            </div>
                            <div v-else>
                                <div style="position:absolute; top: 85px;">
                                    <!-- <div class="sub-profile-image"></div>
                                    <div class="sub-profile-image"></div> -->
                                    <!-- <div class="sub-profile-image"></div>
                                    <div class="sub-profile-image"></div>
                                    <div class="remaining">+99</div> -->
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="right">></div>
        </div>
        <div class="text-container">
            <div class="text-container">
            <div @click="withdrawSelected" class="meta-button-bottom-left gentle">Withdraw</div>
            <div @click="openMassDelegatePopup" class="meta-button-bottom-left gentle">Delegate</div>
            <div class="meta-button-bottom-left gentle">|</div>
            <div v-if="selectedProposalCount<coMemberProposals.length" @click="selectAllProposals()" class="meta-button-bottom-left harsh">Select All</div>
            <div v-else @click="deselectAllProposals()" class="meta-button-bottom-left harsh">Deselect All</div>
            <div class="meta-text-bottom-right">{{ coMemberProposals.length }} results</div>
        </div>
        <div style="color:cyan; text-align: left; font-family: Arial, Helvetica, sans-serif; font-size: 16px; margin-left: 20px;">{{errorLog[0]}}</div>
        </div>
    </div>
    <!-- <div class="decision-row">
        <div style="color:black" class="job-header">
            Reject Pile
            <div class="sub-text-reject">
                Candidates you have personally rejected will appear here. If no action is taken, candidates listed here will be removed automatically after 30 days.
            </div>
        </div>
        <div style="background:transparent; box-shadow:none;" class="jobs-search-container">
            <input v-on:input="filterRejectedCandidates($event.target.value)" style="background:white; margin-bottom:-10px;margin-top:30px; box-shadow: inset 0px 0px 20px rgba(0, 0, 0, .1);" class="job-search" placeholder="Search for the candidate you're looking for..."/>
        </div>
        <div class="roles">
            <div class="left"><</div>
            <div class="roles-container-inline-correction">
                <div v-if="filteredRejectedCandidates.length==0">
                    <div class="no-results-text">Nothing for now...</div>
                    <img class="nothing-for-now-image" src="@/assets/founder-space/decisions/nothing-for-now.png"/>
                </div>
                <div v-else class="roles-container">
                    <div class="role" v-for="candidate in filteredRejectedCandidates" style="margin-top:0px;padding-top:20px;" @click="candidatePopupOpen(candidate)">
                        <div style="" class="role-title"><div style='' class="profile-image"></div><span class="profile-name" :style="candidate.preview_data.name.length>15? 'display:block; vertical-align: top; margin-top:-5px;' : ''" @click="candidatePopupOpen(candidate)">{{ candidate.preview_data.name }}</span></div>
                        <div class="role-description"><i @click="candidatePopupOpen(candidate)">{{ candidate.preview_data.job }}</i></div>
                    </div>
                </div>
            </div>
            <div class="right">></div>
        </div>
        <div class="text-container">
            <div class="meta-button-bottom-left harsh">Reject Remaining</div>
            <div class="meta-text-bottom-right">{{ filteredRejectedCandidates.length }} results</div>
        </div>
    </div> -->
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
    color:#000000;
    cursor: pointer;
    font-weight: bolder;
    opacity: 1;
}
.gentle{
    color: #555555;
    text-decoration: solid underline #b9b9b986 1px;
}
.gentle:hover{
    color: #414141;
    text-decoration: solid underline #49494986 1px;
}
.harsh:hover{
    font-weight: bolder;
    color: #417cd3;
    text-decoration: solid underline #417cd3 1px;
}
.harsh{
    font-weight: bolder;
    color: #417cd3;
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
.larger-prev-name{
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
.prev-name{
    font-family: sans-serif;
    font-size: 12px;
    text-align: left;
    margin-top: 3px;
    margin-bottom: 5px;
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