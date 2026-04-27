<script setup>
import { ref, nextTick} from 'vue';
import { onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import MainCardMiniView from '@/components/founder-space/interfaces/edit-cards/color-change/mini-views/main-card-mini-view.vue';
import description from '@/components/job-page/description.vue';
import jobDescriptionTab from '@/components/founder-space/interfaces/edit-cards/roles-card/job-create-edit/creation-tabs/job-description-creation-tab.vue';
import JobQuestionCreationTab from '@/components/founder-space/interfaces/edit-cards/roles-card/job-create-edit/creation-tabs/job-question-creation-tab.vue';
import JobColorTab from '@/components/founder-space/interfaces/edit-cards/roles-card/job-create-edit/creation-tabs/job-color-tab.vue';
import JobPreview from '@/components/founder-space/interfaces/edit-cards/roles-card/job-create-edit/creation-tabs/job-preview.vue';
import CandidateApplication from '@/components/founder-space/interfaces/decisions/decisions-popups/components/candidate-application.vue';
import MemberListing from '@/components/founder-space/interfaces/decisions/decisions-popups/components/member-listing.vue';
const apiURL = import.meta.env.VITE_APP_API_URL;
const route = useRoute();
let props = defineProps({
    renderVar: Array,
    scrollable: Array,
    decision: Object,
    id: Number,
    allDecisions: Array,
    selectedProposalCount: Array,
    errorLog: Array,
});

// let decision = ref({
//     type: "Remove Member",
//     name: "John Doe",
//     note: "John has been consistently underperforming and has not been meeting the expectations of his role. Despite multiple discussions and attempts to provide support and resources for improvement, there has been no significant progress. His lack of contribution is affecting the overall productivity and morale of the team. It is in the best interest of the company and the team to remove John from his position and find a more suitable candidate who can meet the demands of the role and contribute positively to the team's success."
// });


onMounted(async () => {
    //fetch members and set them to the members variable, for now we will just use some dummy data
    axios.get(`${apiURL}projects/votes/load_members/${route.params.projectId}`).then(response => {
        let data = response.data.members;
        console.log("Members data:", data);
        members.value = data.map(voter => {
            return {
                id: voter.user_id,
                name: voter.display_name,
                image: voter.image
            }
        });
        filteredMembers.value = members.value;
    }).catch(error => {
        console.log(error);
    });

});

let tab = ref([1]);

const closePopup = async () => {
    props.scrollable[0] = 'auto';
    props.renderVar[0] = false;
    await nextTick();
    fontAdjust();
}

let members = ref([

]);

let filteredMembers = ref(members.value);

function filterMembers(event){
    let value = event.target.value.toLowerCase();
    filteredMembers.value = members.value.filter(member => member.name.toLowerCase().includes(value));
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
}

async function confirmDelegate(){
    //run some process here in the backend, will be static/stable in the archive when redone, but for now we just close the delegate select and return to the main decision view.
    let i = 0;
    while(i < props.allDecisions.length){
        if(props.allDecisions[i].select){
            try{
                await axios.post(`${apiURL}projects/votes/cast_vote/${props.userID}/${props.allDecisions[i].proposal_id}`, {
                    vote: "delegate",
                    delegate_id: selectedId.value[0]
                });
                props.allDecisions.splice(i, 1);
            }catch(e){
                props.allDecisions[i].err = "failed to delegate.";
                i++;
                props.errorLog[0] = "! Some delegations failed to be declared, please select different a diffrent delegate for the failed delegations.";
            }
        }else{
            i++;
        }
    }

    closePopup();   

}


let delegateSelect = ref(false);
let selectedId = ref([-1]);
let errorMessage = ref("");


</script>

<template>
    <div @click.self="closePopup" id="popup-backdrop" class="popup-backdrop">
        <div id="popup" class="popup">
            <div class="header">
                <div class="buttons">
                    <img  @click="closePopup" class="close-button" value="Close" src="@/assets/user-tools/job-view/x-icon.png" />
                </div>
            </div>
            <div class="container-popup">
                <div class="member-search-container">
                    <input v-on:input="filterMembers($event)" class="memberSearch" placeholder="Search for memebr you'd like to delegate to">
                </div>
                <div class="main-body-container">
                    <div style="position:absolute; left: 50px; width:98%; z-index: 40; height:calc( 100% - 80px); ">
                        <MemberListing :members="filteredMembers" :selectedId="selectedId"/>
                    </div>
                </div>
            </div>
            <div class="popup-footer">
                <div @click="confirmDelegate" class="delegate-confirm-button">
                    Confirm Delegation
                </div>
            </div>
        </div>
    </div> 
</template>

<style scoped>
.delegate-confirm-button:hover{
    border: solid rgb(255, 255, 255) 2px;
    background-image: linear-gradient(to bottom, rgb(110, 255, 27), rgb(228, 255, 164));
    cursor: pointer;
}
.delegate-confirm-button{
    float: right;
    width:calc(100% - 4px);
    height:calc( 100% + 20px);
    border: solid rgb(238, 238, 238) 2px;
    color: rgb(41, 41, 41);
    font-family: fantasy;
    letter-spacing: 1.5px;
    margin-top: -30px;
    padding-top: 40px;
    float: right;
    overflow: hidden;
    text-align: center;
    box-shadow: inset 0 10px 10px rgba(255, 255, 255, 0.753);
    background-image: linear-gradient(to bottom, rgb(122, 255, 45), rgb(243, 255, 214));
}
.member-search-container{
    font-size: 20px;
    font-family: fantasy;
    color: rgb(114, 114, 114);
    margin-bottom: 20px;
    text-align: left;
    font-weight: bold;
    padding: 20px;
    margin-bottom:10px;
    margin-top:-40px;
    width: calc(100% - 20px);
    padding-right:10px;
    font-style: italic;
    box-shadow: rgb(255, 255, 255) 0px 10px 10px;
}
.memberSearch{
    width: calc(100% - 40px);
    height:28px;
    padding: 10px;
    border: solid rgb(200, 200, 200) 1px;
    border-radius: 5px;
    font-size: 14px;
    border-radius: 10px;
}
.delegate-button{
    background-image: linear-gradient(to bottom, rgb(175, 175, 175), rgb(255, 255, 255));
}
.withdraw-button{
    background-image: linear-gradient(to bottom, rgb(51, 51, 51), rgb(179, 179, 179));
}
.reject-button{
    background-image: linear-gradient(to bottom, rgb(9, 218, 255), rgb(192, 240, 255));
}
.offer-button{
    background-image: linear-gradient(to bottom, rgb(255, 70, 70), rgb(255, 210, 210));
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
.decision-button{
    float: right;
    width:calc(25% - 4px);
    height:calc( 100% + 20px);
    background-color: rgb(221, 221, 221);
    border: solid rgb(238, 238, 238) 2px;
    color: rgb(41, 41, 41);
    font-family: fantasy;
    letter-spacing: 1.5px;
    margin-top: -30px;
    padding-top: 40px;
    float: right;
    
    overflow: hidden;
    text-align: center;
    box-shadow: inset 0 10px 10px rgba(255, 255, 255, 0.753);
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
.toggle{
    position: absolute;
    height: 30px;
    width:40px;
    right:0px;
    top:0px;
    z-index: 42;
    display:inline-block;
    background-color: rgb(219, 219, 219);
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.767);
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
    
    overflow: hidden;
    filter: contrast(100%);
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
    height: calc(100vh - 500px);
    padding-bottom: 300px;
    transition: all 0.5s ease;
    overflow:hidden;
    box-shadow: rgba(255, 255, 255, 0.377) 0px 5px 15px 15px;
}
.popup{
    background-image: linear-gradient(45deg, rgba(255, 255, 255, 0.678), rgba(255, 255, 255, 0.623));
    color: rgb(255, 255, 255);
    width:  calc( (100%));
    max-width: 1300px;
    height: calc( (100%));
    position: fixed;
    top: 50%;   
    left: 50%;
    transform: translate(-50%, 0%); 
    box-shadow: rgba(209, 209, 209, 0.171) 0px 5px 15px 15px;
    overflow:hidden;
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

.popup-backdrop.removing{
    opacity: 0;

}

.popup-backdrop {
    width: 100%;
    height: 100%;
    background-color: rgba(255, 255, 255, 0.555);
    position: fixed;
    z-index: 10;
    opacity: 1;
    animation: fadeIn 0.3s;
    transition: opacity 0.3s ease-out;
    padding-bottom: 100px;
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