<script setup>
import { ref, nextTick, render} from 'vue';
import { onMounted } from 'vue';
import MainCardMiniView from '@/components/founder-space/interfaces/edit-cards/color-change/mini-views/main-card-mini-view.vue';
import description from '@/components/job-page/description.vue';
import jobDescriptionTab from '@/components/founder-space/interfaces/edit-cards/roles-card/job-create-edit/creation-tabs/job-description-creation-tab.vue';
import JobQuestionCreationTab from '@/components/founder-space/interfaces/edit-cards/roles-card/job-create-edit/creation-tabs/job-question-creation-tab.vue';
import JobColorTab from '@/components/founder-space/interfaces/edit-cards/roles-card/job-create-edit/creation-tabs/job-color-tab.vue';
import JobPreview from '@/components/founder-space/interfaces/edit-cards/roles-card/job-create-edit/creation-tabs/job-preview.vue';
import CandidateApplication from '@/components/founder-space/interfaces/decisions/decisions-popups/components/candidate-application.vue';
import ContextRequest from '@/components/founder-space/interfaces/decisions/decisions-popups/components/context-request.vue';
import RejectionContextRequest from '@/components/founder-space/interfaces/decisions/decisions-popups/components/rejection-context-request.vue';
import axios from 'axios';
const apiURL = import.meta.env.VITE_APP_API_URL;
let props = defineProps({
    renderVar: Array,
    scrollable: Array,
    candidate: Object,
    jobsList: Array,
    id: Array,
    index: Number,
    applications : Object,
});

let candidateTemp = ref({});

onMounted(async () => {
    
});

let peopleFor = ref([
    {
        name: "Alex smith",
        image: "https://yt3.googleusercontent.com/VwzinGllvtUNSfEygjRp5EtR1JBWlTrTC8AOT_visy7aV2ZwrgtjvucUA_oTpTaaeR7i69Cg=s900-c-k-c0x00ffffff-no-rj"
    },
    {
        name: "John doe",
        image: "https://yt3.googleusercontent.com/VwzinGllvtUNSfEygjRp5EtR1JBWlTrTC8AOT_visy7aV2ZwrgtjvucUA_oTpTaaeR7i69Cg=s900-c-k-c0x00ffffff-no-rj"
    },
    {
        name: "Jane doe",
        image: "https://yt3.googleusercontent.com/VwzinGllvtUNSfEygjRp5EtR1JBWlTrTC8AOT_visy7aV2ZwrgtjvucUA_oTpTaaeR7i69Cg=s900-c-k-c0x00ffffff-no-rj"
    },
]);

let peopleAgainst = ref([
    {
        name: "Bob smith",
        image: "https://yt3.googleusercontent.com/VwzinGllvtUNSfEygjRp5EtR1JBWlTrTC8AOT_visy7aV2ZwrgtjvucUA_oTpTaaeR7i69Cg=s900-c-k-c0x00ffffff-no-rj"
    },
    {
        name: "Alice doe",
        image: "https://yt3.googleusercontent.com/VwzinGllvtUNSfEygjRp5EtR1JBWlTrTC8AOT_visy7aV2ZwrgtjvucUA_oTpTaaeR7i69Cg=s900-c-k-c0x00ffffff-no-rj"
    },
    {
        name: "Charlie doe",
        image: "https://yt3.googleusercontent.com/VwzinGllvtUNSfEygjRp5EtR1JBWlTrTC8AOT_visy7aV2ZwrgtjvucUA_oTpTaaeR7i69Cg=s900-c-k-c0x00ffffff-no-rj"
    },
]);

let tab = ref([1]);

const closePopup = async () => {
    props.scrollable[0] = 'auto';
    props.renderVar[0] = false;
    await nextTick();
    fontAdjust();
}



// When changing between tabs, the soluton where  we use the DOM ad check if it was clicked out of to save the inner HTML doesnt work, I think its because of the
// the tabs being non functional. 

// copilot said this after I wrote the above comment: So instead we use a watcher in the job-question-creation-tab.vue file to save the inner HTML when clicking outside of the editor divs.

function changeTab(event) {
    if(document.getElementById('editor')){
        props.jobInformation.jobDescription.description[0] = document.getElementById('editor').innerHTML;
    }
    if(document.getElementById('editor-1')){
        for(let i = 0; i < props.jobInformation.jobQuestions.extraQuestion.length; i++){
            props.jobInformation.jobQuestions.extraQuestion[i].questionHTML[0] = document.getElementById('editor-'+i).innerHTML;
        }
    }
    
    let target = event.target;
    let headerNumber = target.getAttribute('headerNumber');
    if (headerNumber) {
        tab.value[0] = parseInt(headerNumber);
    }
}

let noteMode = ref(true);
let inFavorView = ref(false);
let againstView = ref(false);

function activateNote(){

    noteMode.value = true;
    inFavorView.value = false;
    againstView.value = false;
    window.addEventListener('resize', fontAdjust);
    // document.getElementById('note-block').style.opacity = 1;
}

async function activateInfavor(){
    inFavorView.value = true;
    againstView.value = false;
    noteMode.value = false;
    await nextTick();
    fontAdjust();
    window.addEventListener('resize', fontAdjust);
    // document.getElementById('note-block').style.opacity = 1;
}

async function activateAgainst(){
    againstView.value = true;
    inFavorView.value = false;
    noteMode.value = false;
    await nextTick();
    fontAdjust();
    window.addEventListener('resize', fontAdjust);
}

function closeNote(){
    noteMode.value = false;
    window.removeEventListener('resize', fontAdjust);
}

function closeFavor(){
    inFavorView.value = false;
    window.removeEventListener('resize', fontAdjust);

}

function closeAgainst(){
    againstView.value = false;
    window.removeEventListener('resize', fontAdjust);
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

function startToggle(target){
    if(props.allCandidates.find(candidate => candidate.id === props.id).pinned[0]){
        props.allCandidates.find(candidate => candidate.id === props.id).pinned[0] = false;
        target.classList.remove('pinned');
    } else {
        props.allCandidates.find(candidate => candidate.id === props.id).pinned[0]= true;
        target.classList.add('pinned');
    }
    fontAdjust();
}

async function goToDiscussion(){
    internalTab.value = 2;
    await nextTick();
    fontAdjust();
}

function filterJobs(applications){
    let search = document.getElementById("search-input").value;
    applications["filtered"] = applications["true"].filter(application => {
        if(!application.application_object?.job || !application.project_name){
            return false;
        }
        return application.application_object.job.toLowerCase().includes(search.toLowerCase()) || application.project_name.toLowerCase().includes(search.toLowerCase());
    });
    fontAdjust();
}

async function DeleteApplication(){
    if(randInt.value != parseInt(document.querySelector("#confirm-delete-input").value)){
        document.querySelector("#confirm-delete-input").value = "";
        document.querySelector("#confirm-delete-input").placeholder = "Incorrect number, try again";
        return;
    }
    await axios.post(`${apiURL}/users/applications/delete/${props.candidate.user_id}/${props.candidate.application_id}`).then((response) => {
        console.log(response);
    }).catch((error) => {
        console.log(error);
    });
    let trueIndex = props.applications['true'].findIndex(application => application.application_id === props.candidate.application_id);
    props.applications['true'].splice(trueIndex, 1);
    filterJobs(props.applications);
    await nextTick();
    fontAdjust();
    closePopup();
}

async function goToRejectionFeedback(){
    internalTab.value = 1;
    await nextTick();
    fontAdjust();
}

async function goToApplication(){
    internalTab.value = 0;
    await nextTick();
    fontAdjust();
}

let internalTab = ref(0);

let feedback = ref([
    "I think the candidate has potential, but I am concerned about their lack of experience in the field. I would like to see more evidence of their skills and qualifications before making a final decision.",
    "While the candidate has some relevant experience, I am not convinced that they are the right fit for our team. I would like to see more examples of their work and how they have contributed to previous projects before making a final decision.",
    "The candidate's qualifications do not fully align with the requirements of the position. I would like to see more relevant experience or additional training before making a final decision."
])
let randInt = ref(0);
function deleteToggle(){
    internalTab.value = 1;
    randInt.value = Math.floor(Math.random() * 1000)+1000;
}



</script>

<template>
    <div @click.self="closePopup" id="popup-backdrop" class="popup-backdrop">
        <div id="popup" class="popup">
            <div class="header">
                <div class="buttons">
                    <img  @click="closePopup" class="close-button" value="Close" src="@/assets/user-tools/job-view/x-icon.png" />
                </div>
            </div>
            <div v-if="internalTab === 0" class="container-popup">
                <div class="main-body-container">
                    <div style="position:absolute; margin-left:50px; width:98%; z-index: 40; height:calc( 100% - 100px); max-width: 1100px;">
                        <CandidateApplication :decision="candidate"/>
                    </div>
                </div>
            </div>
            <div v-if="internalTab === 1" class="container-popup">
                <div class="main-body-container">
                    <div style="position:absolute; width:100%; height:calc( 100% - 200px); ">
                        <div style="position:relative; margin:auto; max-width:700px; text-align: center; color: black; font-family: sans-serif;">
                            Retype the following number to confirm deletion of this application
                            <div style="margin-top:10px">{{ randInt }}</div>
                            <input id="confirm-delete-input" style="margin-top:10px; padding:10px; font-size: 16px; text-align: center; width:50%; border: solid rgb(200, 200, 200) 1px; border-radius: 5px;" placeholder="Type the number here"/>
                        </div>
                    </div>
                </div>
            </div>
            <div v-if="internalTab === 2" class="container-popup">
                <div style="max-width:1000px; margin:auto; width: 80%; height:calc( 100% ); color:black;  ">
                    <div v-if="candidate.rejection_information.length == 0" style="position:relative; max-width:700px; text-align: left; color: black; font-family: Arial; font-size: 14px;">
                        ...You stand without objection!
                    </div>
                    <div v-else class="container-rejections">
                        <div v-for="(item, index) in candidate.rejection_information" :key="index" class="feedback-item">
                            <div style="margin-left:-25px; margin-bottom:-22px"><b>o</b></div>
                            {{ item.reason }}
                        </div>
                    </div>
                </div>
            </div>
            <div v-if="internalTab == 1" class="popup-footer">
                <div @click="DeleteApplication" class="confirm-deletion-button">
                    Comfirm Deletion
                </div>
            </div>
            <div v-else class="popup-footer">
                <div @click="deleteToggle" class="delete-application-button">
                    Delete Application
                </div>
                <div @click="goToDiscussion" :class="internalTab === 2 ? 'selected' : 'decision-button'">
                    View Rejection Feedback
                </div>
                <div @click="goToApplication" :class="internalTab === 0 ? 'selected' : 'decision-button'">
                    View Application
                </div>
            </div>
        </div>
    </div> 
</template>

    <!-- background-image: linear-gradient(to bottom, rgb(221, 221, 221), rgb(235, 235, 235)); -->
<style scoped>
.confirm-deletion-button:hover{
    cursor: pointer;
    background-image: linear-gradient(to bottom, rgb(17, 247, 255),rgb(186, 255, 240));
    border: solid rgb(238, 238, 238) 2px;
    color: rgb(41, 41, 41);
    font-family: Arial, Helvetica, sans-serif;
    letter-spacing: 1.5px;
    margin-top: -30px;
    padding-top: 40px;
    text-align: center;
    box-shadow: inset 0 10px 10px rgba(255, 255, 255, 0.863);
}
.confirm-deletion-button{
    width:calc(100% - 4px);
    height:calc( 100% + 20px);
    background-image: linear-gradient(to bottom, rgb(70, 255, 240),rgb(210, 235, 255));
    border: solid rgb(238, 238, 238) 2px;
    color: rgb(41, 41, 41);
    font-family: Arial, Helvetica, sans-serif;
    letter-spacing: 1.5px;
    margin-top: -30px;
    padding-top: 40px;
    text-align: center;
    box-shadow: inset 0 10px 10px rgba(255, 255, 255, 0.753);
    overflow: hidden;
}
.selected:hover{
    cursor: pointer;
    background: linear-gradient(to top, rgb(0, 0, 0), rgb(37, 37, 37));
    border: solid rgb(238, 238, 238) 2px;
    color: rgb(231, 231, 231);
    box-shadow: inset 0 10px 10px rgba(255, 255, 255, 0.863);
}
.decision-button:hover{
    cursor: pointer;
    background: linear-gradient(to top, rgb(206, 206, 206), rgb(223, 223, 223));
    border: solid rgb(238, 238, 238) 2px;
    color: rgb(41, 41, 41);
    box-shadow: inset 0 10px 10px rgba(255, 255, 255, 0.863);
}
.container-rejections{
    display: block;
    justify-content: center;
    align-items: center;
    height: calc(100% - 80px);
    width:calc(100% - 80px);
    padding:40px;
    position: relative;
    box-shadow: inset 0 0 20px rgba(255, 255, 255, 0.918);
    overflow:hidden
}
.feedback-item{
    background-color: rgba(255, 255, 255, 0);
    font-family: sans-serif;
    color: rgb(0, 0, 0);
    padding:10px;
    font-size: 16px;
    width:95%;
    margin: auto;
    margin-bottom: 0px;
    border-bottom: rgba(0, 0, 0, 0.678) solid 1px;
}
.selected{
    width:calc(33% - 4px);
    height:calc( 100% + 20px);
    background: linear-gradient(to top,rgb(59, 59, 59) 0%, rgb(7, 7, 7), rgb(34, 34, 34) 100%);
    border: solid rgb(238, 238, 238) 2px;
    color: rgb(231, 231, 231);
    font-family: fantasy;
    letter-spacing: 1.5px;
    margin-top: -30px;
    padding-top: 40px;
    text-align: center;
    box-shadow: inset 0 10px 10px rgba(255, 255, 255, 0.753);
    float:right;
    overflow: hidden;
}
.sumbit-rejection-button{
    width:calc(100% - 4px);
    height:calc( 100% + 20px);
    background-image: linear-gradient(to bottom, rgb(46, 46, 46), rgb(0, 0, 0));
    border: solid rgb(238, 238, 238) 2px;
    color: rgb(202, 202, 202);
    font-family: fantasy;
    letter-spacing: 1.5px;
    margin-top: -30px;
    padding-top: 40px;
    text-align: center;
    box-shadow: inset 0 10px 10px rgba(255, 255, 255, 0.753);
    overflow: hidden;
}
.sumbit-rejection-button:hover{
    cursor:pointer;
    background-image: linear-gradient(to bottom, rgb(0, 0, 0), rgb(15, 15, 15));
    
}
.sumbit-proposal-button:hover{
    cursor:pointer;
    background-image: linear-gradient(to bottom, rgb(0, 255, 157), rgb(99, 255, 133));
    
}
.sumbit-proposal-button{
    width:calc(100% - 4px);
    height:calc( 100% + 20px);
    background-image: linear-gradient(to bottom, rgb(27, 255, 206), rgb(117, 255, 147));
    border: solid rgb(238, 238, 238) 2px;
    color: rgb(41, 41, 41);
    font-family: fantasy;
    letter-spacing: 1.5px;
    margin-top: -30px;
    padding-top: 40px;
    text-align: center;
    box-shadow: inset 0 10px 10px rgba(255, 255, 255, 0.753);
    overflow: hidden;
}
.pin-icon{
    width:100%;
    height:100%;
    transition: all 0.2s ease;
}
.delegate-button{
    background-image: linear-gradient(to bottom, rgb(175, 175, 175), rgb(255, 255, 255));
}
.withdraw-button{
    background-image: linear-gradient(to bottom, rgb(51, 51, 51), rgb(179, 179, 179));
}
.reject-button{
    
    float:left;
    background-image: linear-gradient(to bottom, rgb(9, 218, 255), rgb(192, 240, 255));
}
.offer-button{
    
    float:right;
    background-image: linear-gradient(to bottom, rgb(255, 70, 70), rgb(255, 210, 210));
}
.application-button{
    float: right;
    background-image: linear-gradient(to bottom, rgb(20, 20, 20), rgb(56, 56, 56));
}
.reject-button:hover{
    
    border: solid rgb(255, 255, 255) 2px;
    filter: contrast(100%) saturate(120%);
    cursor: pointer;
}
.offer-button:hover{
    
    border: solid rgb(255, 255, 255) 2px;
    filter: saturate(140%);
    cursor: pointer;
}
.delegate-button:hover{
    
    border: solid rgb(255, 255, 255) 2px;
    filter: contrast(80%) brightness(110%);
    cursor: pointer;
}
.withdraw-button:hover{
    border: solid rgb(255, 255, 255) 2px;
    filter: contrast(80%) saturate(140%);
    cursor: pointer;
}
.delete-application-button{
    width:calc(33% - 4px);
    height:calc( 100% + 20px);
    background: linear-gradient(to top,rgb(27, 255, 225) 0%, rgb(172, 236, 255)  50%, rgb(28, 252, 222) 100%);
    border: solid rgb(238, 238, 238) 2px;
    color: rgb(41, 41, 41);
    font-family: fantasy;
    letter-spacing: 1.5px;
    margin-top: -30px;
    padding-top: 40px;
    text-align: center;
    box-shadow: inset 0 10px 10px rgba(255, 255, 255, 0.753);
    float:right;
    overflow: hidden;
    
}
.delete-application-button:hover{
    background: linear-gradient(to top,rgb(0, 255, 221) 0%, rgb(111, 222, 255)  50%, rgb(0, 255, 221) 100%);
    border: solid rgb(238, 238, 238) 2px;
    color: rgb(41, 41, 41);
    font-family: fantasy;
    letter-spacing: 1.5px;
    margin-top: -30px;
    padding-top: 40px;
    text-align: center;
    box-shadow: inset 0 10px 10px rgba(255, 255, 255, 0.753);
    float:right;
    overflow: hidden;
    cursor:pointer;
}

.decision-button{
    width:calc(33% - 4px);
    height:calc( 100% + 20px);
    background: linear-gradient(to top,rgb(206, 206, 206) 0%, rgb(223, 223, 223) 50%, rgb(206, 206, 206) 100%);
    border: solid rgb(238, 238, 238) 2px;
    color: rgb(41, 41, 41);
    font-family: fantasy;
    letter-spacing: 1.5px;
    margin-top: -30px;
    padding-top: 40px;
    text-align: center;
    box-shadow: inset 0 10px 10px rgba(255, 255, 255, 0.753);
    float:right;
    overflow: hidden;
}
.people-listing-name{
    position: relative;
    display: inline-block;
    font-size: 14px;
    color: rgb(0, 0, 0);
    font-family: sans-serif;
    width: calc(100% - 60px);
    font-weight: bold;
}
.info-features{
    --space: 50px;
}
.note-header-label{
    font-size: 15px;
    letter-spacing: 1px;
    font-weight: bold;
    font-family:'Courier New', Courier, monospace;
    color: rgb(150, 150, 150);
}
.minimize:hover{
    background-image: linear-gradient(to bottom, rgba(189, 189, 189, 0.952), rgba(211, 211, 211, 0.952));
    border-radius: 0%;
    box-shadow: inset 0 0 10px rgba(255, 255, 255, 0.767);;
    color:rgb(0, 0, 0);
}
.minimize{
    position: absolute;
    top:10px;
    margin-right:30px;
    height: 100%;
    width:40px;
    color:rgb(95, 95, 95);
    font-weight: bold;
    font-size: 25px;
    vertical-align: center;
    text-align: center;
    background-image: linear-gradient(to bottom, rgba(224, 224, 224, 0.952), rgba(230, 230, 230, 0.952)) !important;
    box-shadow: inset 0 0 10px rgba(255, 255, 255, 0.767);;
    z-index: 45;
}
.main-body-container{
    display: block;
    justify-content: center;
    align-items: center;
    height: 100%;
    width:calc(100%);
    position: relative;
    margin: 40px;
    margin-top:0;
    width:calc(100% - 40px);
    z-index: 30;
}
.star{
    position: absolute;
    height: 40px;
    width:40px;
    padding: 10px;
    right:5px;
    top:0px;
    z-index: 42;
    display:inline-block;
    background-color: rgb(255, 255, 255);
    border: black 3px solid;
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.767);
    background-size: 50% auto;
    background-repeat: no-repeat;
    background-position: center;
    overflow: hidden;
    cursor:pointer;
    border-radius:50%;
    transition: all 0.2s ease;
}
.star:hover{
    border: rgb(117, 57, 0) 3px solid;
}
.against{
    right: calc(0px + (2 * var(--space)));
    background-image: url("@/assets/founder-space/decisions/disengage.png");
    background-size: 60% auto;
    background-repeat: no-repeat;
    background-position: center;
}
.infavor{
    right: calc(0px + (1 * var(--space)));
    background-image: url("@/assets/founder-space/decisions/handraise.png");
    background-size: 60% auto;
    background-repeat: no-repeat;
    background-position: center;
}
.noteButton{
    right: calc(0px + (0 * var(--space)));
    background-image: url("@/assets/founder-space/decisions/note.png");
    background-size: 60% auto;
    background-repeat: no-repeat;
    background-position: center;
}
.note-content{
    position: relative;
    overflow:auto;
    width:85%;
    background-color: rgb(212, 212, 212);
    margin:auto;
    margin-left: -10px;
    height: 150px;
    padding: 20px;
    padding-top:40px;
    padding-right:80px;
    margin: -30px;
    font-size: 12px;
    text-align: left;
    z-index: 20;
    overflow:hidden;
    overflow-y:auto;
    box-shadow: inset 0 0 10px rgba(255, 255, 255, 0.918);
    font-family: sans-serif;
}
.people-listing{
    position: relative;
    overflow:auto;
    width:calc(100% - 0px);

    background-color: rgb(216, 216, 216);
    margin:auto;
    height: 140px;
    padding: 20px;
    padding-top:20px;
    padding-right:30px;
    padding-left:30px;
    margin-left: -30px;
    font-size: 12px;
    text-align: left;
    z-index: 20;
    overflow:hidden;
    overflow-y:auto;
    box-shadow: inset 0 0 20px rgba(255, 255, 255, 0.918);
    font-family: sans-serif;
    z-index: 20;

}
.note-footer{
    position: absolute;
    bottom: 0;
    width:100%;
    margin-left: -30px;
    font-size: 10px;
    color: rgb(99, 99, 99);
    background-color: rgb(223, 223, 223);
    padding: 5px;
    padding-left: 10px;
    padding-right: 30px;
    text-align: right;
    right:0;
    box-shadow: inset 0 0 10px rgba(255, 255, 255, 0.918);
    z-index: 40;
}
.note-header{
    position: relative;
    overflow:auto;
    width:100%;
    text-align: left;
    margin:auto;
    font-size:12px;
    padding:5px;
    padding-left: 45px;  
    padding-right: 40px; 
    padding-top:20px;
    margin-left:-40px;
    margin-left:-40px;
    box-shadow: inset 0 0 10px rgba(226, 226, 226, 0.918);
    background-color: rgb(228, 228, 228);
    color: rgb(2, 2, 2);
    height: 20px;
    margin-top:-40px; 
    z-index: 21;
    font-family: sans-serif;
    overflow: hidden;

}
.note{
    opacity: 1;
    display: block;
    height: 180px;
    width:calc(80% - 40px);
    max-width: 250px;
    margin: auto;
    margin-top: 20px;
    position: absolute;
    top:-20px;
    right:0;
    z-index: 20;
    padding:25px;
    margin-right:-10px;
    top:-20px;
    background-color:rgb(110, 110, 110);
    font-family: sans-serif;
    color: rgb(0, 0, 0);
    white-space: wrap;
    overflow:hidden;
    box-shadow: 0 0 30px rgba(255, 255, 255, 0.692);
    z-index: 41;
}
#note-block{
    animation: fadeInNote 0.3s;
}
@keyframes fadeInNote {
  from {
    opacity: 0;
    transform: translateY(0px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.popup-footer{
    text-align: left;
    background-color: rgb(236, 236, 236);
    box-shadow: rgba(255, 255, 255, 0.329) 0px 4px 6px -1px;
    width:calc(100% );
    max-width: calc(1050px - 40px);
    padding:20px;
    padding-bottom:20px;
    padding-top:30px;
    position: absolute;
    height:50px;
    left: 50%;
    transform: translateX(-50%);
    bottom:0;
    z-index: 40;
    filter: contrast(100%);
    
    overflow: hidden;
}
.decision-title{
    font-size: 20px;
    font-family: fantasy;
    color: rgb(114, 114, 114);
    margin-bottom: 20px;
    text-align: left;
    font-weight: bold;
    padding: 10px;
    margin:-10px;
    margin-top:-30px;
    margin-bottom:10px;
    margin-left: 20px;
    font-style: italic;
}
.button{
    float: right;
    width:100px;
    margin-right: 80px;
    background-color: rgba(255, 0, 0, 0.712);
    color: white;
    font-family: fantasy;
    letter-spacing: 1.5px;
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.575);
    margin-top: -10px;
    float: right;
    transition: box-shadow 0.3s ease;
    padding:10px;
    border-radius: 30px;
}
.header-number-text{
    margin-left: 20px;
    font-size: 13px;
    width:100%;
    vertical-align: top;
    margin:auto;
    margin-top: 6px;
    font-family: sans-serif;
    color: black;
}
.heaeder-number-container{
    display: inline-block;
    width: 120px;
    height: 80px;
    margin-right: 0px;
    text-align: center;
    vertical-align: top;
}
.heaeder-number-container-end{
    display: inline-block;
    width: 120px;
    height: 80px;
    text-align: center;
    vertical-align: top;
}

.circle-selected:hover{
    position: relative;
    font-weight: lighter;
    user-select: none;
    cursor: default;
    font-size: 20px;
    line-height: 40px;
    font-style: fantasy;
    height: 40px;
    width: 40px;
    margin:auto;
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.767);
    border: solid rgb(100, 142, 255) 2px;
    border-radius: 50%;
    margin-top: 10px;
    color: rgb(100, 142, 255);
    background-color: rgb(113, 191, 255);
}

.circle-selected{
    position: relative;
    font-weight: lighter;
    user-select: none;
    cursor: default;
    font-size: 20px;
    line-height: 40px;
    font-style: fantasy;
    height: 40px;
    width: 40px;
    margin:auto;
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.767);
    border: solid rgb(207, 221, 255) 2px;
    border-radius: 50%;
    margin-top: 10px;
    color: rgb(216, 230, 255);
    background-color: rgb(147, 207, 255);
    transition: all 0.2s ease;
}

.circle{
    position: relative;
    color: rgb(0, 0, 0);
    font-weight: lighter;
    user-select: none;
    cursor: default;
    font-size: 20px;
    line-height: 40px;
    font-style: fantasy;
    height: 40px;
    width: 40px;
    margin:auto;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.767);
    background-color: rgb(255, 255, 255);
    border: solid rgb(0, 0, 0) 2px;
    border-radius: 50%;
    margin-top: 10px;
    transition: all 0.2s ease;
}
.circle:hover{
    position: relative;
    color: rgb(142, 172, 255);
    font-weight: lighter;
    user-select: none;
    cursor: default;
    font-size: 20px;
    line-height: 40px;
    font-style: fantasy;
    height: 40px;
    width: 40px;
    margin:auto;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.767);
    border: solid rgb(183, 202, 255) 2px;
    background-color: rgb(206, 233, 255);
    border-radius: 50%;
    margin-top: 10px;
}

.left-block{
    background-color: rgba(255, 255, 255, 0);
    width:50%;
    height:90px;
    margin: auto;
    white-space: nowrap;
    overflow-x: auto;
    overflow-y: hidden;
    overflow-wrap: nowrap;
    margin-top: -10px;
}
.right{
    position: absolute;
    top: 50%;
    right: 0;
    font-size: 50px;
    color: rgb(0, 0, 0);
    font-weight: bold;
    user-select: none;
    cursor: default;
    transform: translateY(calc(-50% + 110px - 50px));
    font-size: 30px;
    line-height: 50px;
    height: 50px;
    width: 50px;
    margin-right:10px;
    background-image: linear-gradient(45deg, rgb(255, 255, 255), rgba(255, 255, 255, 0.479));
    border: solid black 5px;
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.767);
    border-radius: 50%;
}
.header {
    text-align: left;
    background-image: linear-gradient(to top, rgb(236, 236, 236), rgb(209, 209, 209));
    box-shadow: rgba(255, 255, 255, 0.329) 0px 4px 6px -1px;
    width:100%;
    max-width: 1050px;
    padding-bottom:20px;
    padding-top:30px;
    position: absolute;
    height:60px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 40;
}
.container-popup{
    font-family: sans-serif;
    padding:0px;
    padding-top:150px;
    font-size: 18px;
    line-height: 1.6;
    width:100%;
    max-width: calc(1050px );
    margin: auto;
    background-image: linear-gradient(45deg, white, rgb(207, 207, 207));
    height: calc(100vh - 300px);
    padding-bottom: 300px;
    transition: all 0.5s ease;
    overflow:hidden;
    box-shadow: rgba(255, 255, 255, 0.377) 0px 5px 15px 15px;
}
.popup{
    color: rgb(255, 255, 255);
    width:  calc( (100%));
    max-width: 1300px;
    height: calc( (100% - 0px));
    position: absolute;
    box-shadow: rgba(255, 255, 255, 0.171) 0px 5px 15px 15px;
    overflow:hidden;
    filter:invert(1);
}
.buttons{
    float: right;
    width:100px;
    margin-right: 80px;
    background-color: rgba(255, 255, 255, 0);
}
.close-button {
    font-size: 16px;
    padding:30px;
    display: block;
    padding: 10px;
    background-color:rgba(48, 48, 48, 0);
    color: white;
    font-family: fantasy;
    letter-spacing: 1.5px;
    box-shadow: 0 0 15px rgb(214, 214, 214);
    margin-top: -10px;
    transition: box-shadow 0.3s ease;
    height: 20px;
    margin-top: -30px;
    width: 20px;
    padding: 45px;
    float: right;
    margin-right: -20px;
}

.close-button:hover{
    box-shadow: 0 0 15px rgb(99, 99, 99);
}

.save-button {
    font-size: 16px;
    padding:30px;
    border-radius: 30px;
    display: inline-block;
    padding: 10px;
    background-color:rgba(0, 195, 255, 0.712);
    color: white;
    font-family: fantasy;
    letter-spacing: 1.5px;
    margin-left: 20px;
    box-shadow: 0 0 10px rgba(0, 195, 255, 0.575);
    margin-top: -10px;
    float: right;
    transition: box-shadow 0.3s ease;
}

.save-button:hover{
    box-shadow: 0 0 15px rgba(2, 255, 255, 0.795);
}


.popup-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}



.footer{
    background-color: rgb(255, 255, 255);
    box-shadow: rgb(138, 137, 137) 0px 4px 6px -1px;
    width:100%;
    height:40px;
    padding: 20px;
    margin: -20px;
    position: absolute;
    bottom: 0;
    margin-top: -20px;
}


</style>