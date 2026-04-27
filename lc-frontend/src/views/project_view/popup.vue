<script setup>
import { ref, nextTick} from 'vue';
import { onMounted } from 'vue';
import MainCardMiniView from '@/components/founder-space/interfaces/edit-cards/color-change/mini-views/main-card-mini-view.vue';
import description from '@/components/job-page/description.vue';
import jobDescriptionTab from '@/components/founder-space/interfaces/edit-cards/roles-card/job-create-edit/creation-tabs/job-description-creation-tab.vue';
import JobQuestionCreationTab from '@/components/founder-space/interfaces/edit-cards/roles-card/job-create-edit/creation-tabs/job-question-creation-tab.vue';
import JobColorTab from '@/components/founder-space/interfaces/edit-cards/roles-card/job-create-edit/creation-tabs/job-color-tab.vue';
import JobPreview from '@/components/founder-space/interfaces/edit-cards/roles-card/job-create-edit/creation-tabs/job-preview.vue';
import JobSettingsTab from '@/components/founder-space/interfaces/edit-cards/roles-card/job-create-edit/creation-tabs/job-settings-tab.vue';
import { supabase } from "@/lib/supabase";
let props = defineProps({
    color: Array,
    renderVar: Array,
    jobInformation: Object,
    jobs: Array,
    job_id: String,
    viewMode: Boolean,
    userID: String,
    projectTitle: String
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

onMounted(() => {
});

</script>

<template>
    <div @click.self="closePopup" id="popup-backdrop" class="popup-backdrop">
        <div class="popup">
            <div class="header">
                <div class="buttons">
                    <img  @click="closePopup" class="close-button" value="Close" src="@/assets/user-tools/job-view/x-icon.png" />
                </div>
                <!-- <div class="rel-correction">
                    <div class="left-block">
                        <div class="heaeder-number-container ">
                            <div headerNumber="1" @click="changeTab" :class="tab[0]==1 ? 'circle-selected' : 'circle'" >1</div>
                            <div class="header-number-text">
                                Role description
                            </div>
                        </div>
                        <div class="heaeder-number-container">
                            <div headerNumber="2" @click="changeTab" id="tab2-circle" :class="tab[0]==2 ? 'circle-selected' : 'circle'" >2</div>
                            <div class="header-number-text">
                                Role questions
                            </div>
                        </div>
                        <div class="heaeder-number-container">
                            <div headerNumber="3" @click="changeTab" id="tab3-circle" :class="tab[0]==3 ? 'circle-selected' : 'circle'" >3</div>
                            <div class="header-number-text">
                                Coloring
                            </div>
                        </div>
                        <div class="heaeder-number-container-end" style="margin-bottom: 20px">
                            <div headerNumber="4" @click="changeTab" id="tab4-circle" :class="tab[0]==4 ? 'circle-selected' : 'circle'" >4</div>
                            <div class="header-number-text">
                                Preview
                            </div>
                        </div>
                        <div class="heaeder-number-container-end" style="margin-bottom: 20px">
                            <div headerNumber="5" @click="changeTab" id="tab5-circle" :class="tab[0]==5 ? 'circle-selected' : 'circle'" >5</div>
                            <div class="header-number-text">
                                Settings
                            </div>
                        </div>
                    </div>
                </div> -->
            </div>
            <div class="popup-white-background" :style="{background: props.jobInformation.color.backgroundColor[0], color: props.jobInformation.color.textColor[0]}">
                <div  class='preview-container'>
                    <JobPreview :jobInformation="jobInformation" :tab="tab" :jobs="jobs" :renderVar="renderVar" :newJob="newJob" :viewMode="viewMode" :jobID="props.job_id" :userID="userID" :projectTitle="projectTitle"/>
                </div>
            </div>
        </div>
    </div> 
</template>

<style scoped>
.preview-container{
   font-family: sans-serif;
    margin-top: 200px;
    font-size: 18px;
    padding-top: 150px;
    padding-bottom: 150px;
    line-height: 1.6;
    margin: auto;
    background-color: v-bind(jobInformation.color.backgroundColor[0]);
    height: calc(100vh - 500px);
    padding-bottom: 300px;
    overflow-y:auto;
}
.rel-correction{

}
.header-number-text{
    margin-left: 20px;
    font-size: 13px;
    width:100%;
    vertical-align: top;
    margin:auto;
    margin-top: 6px;
    font-family: sans-serif;
    color: v-bind(jobInformation.color.textColor[0]);
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
    font-style: arial, Helvetica, sans-serif;
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
    font-style: arial, Helvetica, sans-serif;;
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
    font-style: arial, Helvetica, sans-serif;;
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
    font-style: arial, Helvetica, sans-serif;;
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
    height:90px;
    width: calc(100% - 200px);
    max-width:700px;
    white-space: nowrap;
    overflow-x: auto;
    overflow-y: hidden;
    overflow-wrap: nowrap;
    margin-top: -10px;
    position: absolute;
    right: 200px;
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
    background-color: v-bind(jobInformation.color.backgroundColor[0]);
    opacity: .9;
    box-shadow: rgba(0, 0, 0, 0.329) 0px 4px 6px -1px;
    width:100%;
    max-width: 1050px;
    padding-bottom:20px;
    padding-top:30px;
    height:60px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 40;
    position: relative;
}
.container{
    font-family: sans-serif;
    margin-top: 200px;
    font-size: 18px;
    padding-top: 150px;
    padding-bottom: 150px;
    line-height: 1.6;
    max-width: 750px;
    margin: auto;
    background-color: v-bind(jobInformation.color.backgroundColor[0]);
    height: calc(100vh - 500px);
    padding-bottom: 300px;
    transition: all 0.5s ease;
    overflow-y:auto;
    overflow-x:hidden;
}
.popup-white-background{
    box-shadow: rgba(0, 0, 0, 0.329) 0px 4px 6px -1px;
    width:100%;
    max-width: 1050px;
    height: calc(100% - 100px);
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    box-shadow: rgba(0, 0, 0, 0.171) 0px 5px 15px 15px;
    z-index: 1;
}
.popup{
    background-color: rgba(255, 255, 255, 0.404);
    color: rgb(0, 0, 0);
    width:  calc( (100% ));
    max-width: 1300px;
    height: calc(100% - 50px);
    position: absolute;
    top: 50%;
    left:50%;
    transform: translate(-50%, -50%);
    padding-top:50px;
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
    font-family: arial, Helvetica, sans-serif;;
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
    font-family: arial, Helvetica, sans-serif;;
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
    width: calc(100%);
    height: 100%;
    background-color: rgba(0, 0, 0, 0.555);
    position: fixed;
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