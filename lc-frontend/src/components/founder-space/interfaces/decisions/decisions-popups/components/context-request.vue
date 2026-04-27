<script setup>
import { ref, nextTick} from 'vue';
import { onMounted } from 'vue';
import MainCardMiniView from '@/components/founder-space/interfaces/edit-cards/color-change/mini-views/main-card-mini-view.vue';
import description from '@/components/job-page/description.vue';
import jobDescriptionTab from '@/components/founder-space/interfaces/edit-cards/roles-card/job-create-edit/creation-tabs/job-description-creation-tab.vue';
import JobQuestionCreationTab from '@/components/founder-space/interfaces/edit-cards/roles-card/job-create-edit/creation-tabs/job-question-creation-tab.vue';
import JobColorTab from '@/components/founder-space/interfaces/edit-cards/roles-card/job-create-edit/creation-tabs/job-color-tab.vue';
import JobPreview from '@/components/founder-space/interfaces/edit-cards/roles-card/job-create-edit/creation-tabs/job-preview.vue';

let props = defineProps({
    color: Array,
    renderVar: Array,
    jobs: Array,
    members: Object,
});
onMounted(() => {
    fontAdjust();
    window.addEventListener('resize', fontAdjust);
});

let jobInformation = ref({
    jobDescription: {
        title: ["SWE"],
        description: ["<div class='bold-text' data-v-inspector='src/components/founder-space/interfaces/edit-cards/roles-card/job-create-edit/creation-tabs/job-description-creation-tab-default-description-text/text.vue:4:5' data-v-b0813598=''>What you'll do: </div><div>Build a snow man!</div><div><u>Like this</u></div><div><u><b>Like that</b></u></div><div><u><b><i>And this to</i></b></u></div><br data-v-inspector='src/components/founder-space/interfaces/edit-cards/roles-card/job-create-edit/creation-tabs/job-description-creation-tab-default-description-text/text.vue:7:5' data-v-b0813598=''><div class='bold-text' data-v-inspector='src/components/founder-space/interfaces/edit-cards/roles-card/job-create-edit/creation-tabs/job-description-creation-tab-default-description-text/text.vue:8:5' data-v-b0813598=''>Abilities we're seeking: </div><div class='bold-text' data-v-inspector='src/components/founder-space/interfaces/edit-cards/roles-card/job-create-edit/creation-tabs/job-description-creation-tab-default-description-text/text.vue:8:5' data-v-b0813598=''><ol><li>Build a snow man</li></ol><div><ul><li>Then break it down</li></ul><div>DO IT</div><div><br></div></div></div><br data-v-inspector='src/components/founder-space/interfaces/edit-cards/roles-card/job-create-edit/creation-tabs/job-description-creation-tab-default-description-text/text.vue:10:5' data-v-b0813598=''><br data-v-inspector='src/components/founder-space/interfaces/edit-cards/roles-card/job-create-edit/creation-tabs/job-description-creation-tab-default-description-text/text.vue:11:5' data-v-b0813598=''>"],
        summary: ["This is a job summary"]
    },
    jobQuestions: {
        resume:["yes"],
        contacts: [["Email",2,"base"], ["Phone",0,"base"], ["IP-address",0,"base"]],
        anonymous: [true],
        extraQuestion: [
            {
                type:"free-form",
                questionHTML: ["What is your favorite color?"],
                questionType: ["freeform"],
                maxWord: [400, true],
                minWord: [100, false],
                isOptional: [false]
            },
            {
                type:"single-select",
                questionHTML: ["Select your skills"],
                options: ["JavaScript", "Python", "C++"],
                isOptional: [false]
            }
        ]
    },
    color: {
        backgroundColor: ["white"],
        textColor: ["white"]
    }
});


let tab = ref([1]);

const closePopup = async () => {
    props.renderVar[0] = false;
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

function fontAdjust(){
    let names = document.getElementsByClassName('people-listing-name');
    for(let i = 0; i < names.length; i++){
        let name = names[i];
        console.log(name.offsetHeight);
        name.style.top = "0px";
        if(name.offsetHeight > 40){
            name.style.top = "12px";
        }
        let fontSize = 18;
        name.style.fontSize = fontSize + "px";
        while(name.offsetHeight > 50){
            fontSize--;
            name.style.fontSize = fontSize + "px";
        }
    }
}

let selectedId = ref(-1);

function selectDelegate(person){
    if(selectedId.value == person.id){
        selectedId.value = -1;
    } else {
        selectedId.value = person.id;
    }
}

</script>

<template>
    <div class="application-box">
        <div style="color:black; margin-bottom:20px;">Please provide context for wanting to start discussion with this candidate</div>
        <textarea id="context-text" class="context-textarea" placeholder="Type here..." ></textarea>
    </div>
</template>

<style scoped>
.context-textarea{
    width: 100%;
    height: 150px;
    margin-top: 20px;
    padding: 10px;
    font-size: 16px;
    font-family: sans-serif;
    border: 1px solid rgb(200, 200, 200);
    border-radius: 5px;
    resize: none;
}
.people-listing-name{
    position: relative;
    display: inline-block;
    font-size: 18px;
    color: rgb(119, 119, 119);
    width: calc(100% - 100px);
    padding-left: 10px;
    font-family: sans-serif;
}
.person-block-selected:hover{
    background-image: linear-gradient(to bottom, rgb(0, 255, 191), rgb(125, 255, 201));
    cursor: pointer;
}
.person-block-selected{
    padding-left: 20px;
    padding-top:20px;
    margin-top:-20px;
    background-image: linear-gradient(to bottom, rgb(12, 255, 194), rgb(159, 255, 215));
    box-shadow: inset 0 0 30px rgba(255, 255, 255, 0.767);
}
.person-block:hover{
    padding-top:20px;
    margin-top:-20px;
    background-image: linear-gradient(to top, rgba(255, 255, 255, 0.767), rgba(221, 221, 221, 0.767));
    cursor: pointer;
}
.person-block{
    padding-left: 20px;
}
.application-box{
    text-align: left;
    font-family: sans-serif;
    font-size: 16px;
    line-height: 1.6;
    width:calc(100% - 160px);
    margin: auto;
    margin-left:-30px;
    margin-top: 0px;
    padding: 80px;
    padding-top:50px;
    height: 100%;
    transition: all 0.5s ease;
    overflow-x:hidden;
    color:rgb(160, 160, 160);
    position: inherit;
    z-index: 40;
}
.button{
    float: right;
    width:100px;
    margin-right: 80px;
    background-color: rgba(255, 0, 0, 0.712);
    color: white;
    font-family: fantasy;
    letter-spacing: 1.5px;
    box-shadow: 0 0 10px rgba(255, 0, 0, 0.575);
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
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.767);
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
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.767);
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
    background-color: rgba(95, 45, 128, 0);
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
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.767);
    border-radius: 50%;
}
.header {
    text-align: left;
    background-color: rgb(150, 150, 150);
    opacity: .9;
    box-shadow: rgba(112, 112, 112, 0.329) 0px 4px 6px -1px;
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
.container{
    font-family: sans-serif;
    margin-top: 200px;
    font-size: 18px;
    padding: 150px;
    line-height: 1.6;
    max-width: 750px;
    margin: auto;
    background-color: white;
    height: calc(100vh - 500px);
    padding-bottom: 300px;
    transition: all 0.5s ease;
    overflow-y:auto;
    overflow-x:hidden;
    box-shadow: rgba(255, 255, 255, 0.377) 0px 5px 15px 15px;
}
.popup{
    background-color: rgba(255, 255, 255, 0.404);
    color: rgb(0, 0, 0);
    width:  calc( (100% - 180px));
    max-width: 1300px;
    height: calc( (100%));
    position: fixed;
    top: 50%;   
    left: 50%;
    transform: translate(-50%, calc(-50%)); 
    box-shadow: rgba(209, 209, 209, 0.171) 0px 5px 15px 15px;
    overflow:hidden;
}
.buttons{
    float: right;
    width:100px;
    margin-right: 80px;
    background-color: rgba(0, 255, 255, 0);
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
    box-shadow: 0 0 15px rgba(255, 255, 255, 0.726);
    margin-top: -10px;
    transition: box-shadow 0.3s ease;
    height: 20px;
    margin-top: -30px;
    width: 20px;
    padding: 45px;
    float: right;
    margin-right: -20px;
    filter: invert(70%);
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
    position: absolute;
    margin:auto;
    top: 0;
    left: 0;
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