<script setup>
import { onMounted, render } from 'vue';
let props = defineProps({
    jobInformation: Object,
    tab: Array,
    renderVar: Array,
    job_id: String
});
const apiUrl = import.meta.env.VITE_APP_API_URL
import axios from 'axios';
import defaultJobDescriptionText from '@/components/founder-space/interfaces/edit-cards/roles-card/job-create-edit/creation-tabs/job-description-creation-tab-default-description-text/text.vue';
import { useRoute } from 'vue-router';



let route = useRoute();

onMounted(() => {
    
});

async function saveInformation(){
    console.log("Saving job information. Job ID:", props.job_id);
    if(props.job_id == "NEW"){
        await axios.post(apiUrl+"jobs/new_job/"+route.params.projectId, {
            job_object: props.jobInformation
        }).then((response) => {
            console.log("Job information saved successfully:", response.data);
            props.renderVar[0] = false;
        }).catch((error) => {
            console.error("Error saving job information:", error);
        });
    }else{
        await axios.post(apiUrl+"jobs/update_job/"+route.params.projectId+"/"+props.job_id, {
            job_object: props.jobInformation
        }).then((response) => {
            console.log("Job information updated successfully:", response.data);
            props.renderVar[0] = false;
        }).catch((error) => {
            console.error("Error updating job information:", error);
        });
    }
}

function deleteJob(){
    console.log("Deleting job. Job ID:", props.job_id);
    if(props.job_id == "NEW"){
        console.warn("Cannot delete a job that hasn't been created yet.");
        return;
    }
    axios.post(apiUrl+"jobs/delete_job/"+props.job_id).then((response) => {
        props.renderVar[0] = false;
    }).catch((error) => {
        console.error("Error deleting job:", error);
    });
}

function toggleClosed(){
    console.log("Toggling closed setting. Current value:", props.jobInformation.settings.closed[0]);
    props.jobInformation.settings.closed[0] = !props.jobInformation.settings.closed[0];
}

function toggleMaxApplications(){
    props.jobInformation.settings.maxApplications[0] = !props.jobInformation.settings.maxApplications[0];
}

function toggleApplicationDeadline(){
    props.jobInformation.settings.applicationDeadline[0] = !props.jobInformation.settings.applicationDeadline[0];
}

function updateMaxApplications(event){
    props.jobInformation.settings.maxApplications[1] = event.target.value;
}

function updateEndingDate(event){
    props.jobInformation.settings.applicationDeadline[1] = event.target.value;
}

</script>
<template>
    <div class="text-container">
        <div class="question-box">
            <div class="option-action-space-block">
                <div class="toggle">
                    <label class="switch" >
                        <input type="checkbox" :checked="props.jobInformation.settings.closed[0]" @click="toggleClosed">
                        <span class="slider round"></span>
                    </label>
                </div>
                <div class="option-description">
                    <div><b>Close job</b></div>
                    <div>You can still look at the applicants you've recieved for the job, but now the job will be closed for any new applications and be removed from the project page.</div>
                </div>
            </div>
            <!-- <div class="option-action-space-block">
                <div class="toggle">
                    <label class="switch" >
                        <input type="checkbox" :checked="props.jobInformation.settings.maxApplications[0]" @click="toggleMaxApplications">
                        <span class="slider round"></span>
                    </label>
                </div>
                <div class="option-description">
                    <div><b>Set maximum applications</b></div>
                    <div>Create a set number of applications you want to receive for this job. Counting starts from when this this job is saved with this toggle activated.</div>
                </div>
                <input placeholder="Enter maximum number of applicants" @input="updateMaxApplications" class="max-applications-input" v-if="props.jobInformation.settings.maxApplications[0]" :value="props.jobInformation.settings.maxApplications[1]"/>
            </div>
            <div class="option-action-space-block" style="margin-top:-20px;">
                <div class="toggle">
                    <label class="switch">
                        <input type="checkbox" :checked="props.jobInformation.settings.applicationDeadline[0]" @click="toggleApplicationDeadline">
                        <span class="slider round"></span>
                    </label>
                </div>
                <div class="option-description">
                    <div><b>Set application deadline</b></div>
                    <div>After the date you set here, the job will be closed for any new applications and be removed from the project page. You can still look at the applicants you've recieved after the deadline.<b>This wont be added to the job description.</b></div>
                </div>
                <input type="date" class="max-applications-input" @input="updateEndingDate" v-if="props.jobInformation.settings.applicationDeadline[0]" :value="props.jobInformation.settings.applicationDeadline[1]"/>
            </div> -->
        </div>

        <!-- <div class="error">You can delete a job haven't even made yet, silly!</div> -->
        <div class="bottom-tray">
            <div @click="deleteJob" class="delete-job-button" v-if="props.jobInformation.jobID != 'NEW'">
                Delete Job
            </div>
        </div>
        <div class="bottom-tray">
            <div class="next-button" @click="saveInformation">
                Save
            </div>
        </div>
    </div>
</template> 

<style scoped>
.bottom-tray{
    width:100%;
    height:fit-content;
    display:flex;
}
.error{
    color: rgb(255, 0, 0);
    font-size: 14px;
    margin-top: 20px;
    position: absolute;
    left:100px;
    bottom:-20px;
}
.delete-job-button:hover{
    background-color: rgb(255, 0, 0);
    color: white;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);
    transition: all 0.1s ease-in;
    transform: scale(105%);
}
.delete-job-button{
    
    box-shadow: 0px 0px 2px rgba(0, 0, 0, 0.5);
    width:fit-content;
    padding:5px 20px 5px 20px;
    background-color: #ffffff;
    border: red solid 2px;
    color: rgb(255, 0, 0);
    cursor: pointer;
    user-select: none;
    margin-left:80px;
    border-radius: 10px;
    font-size: 14px;
    position: absolute;
    bottom:0;
}
.max-applications-input{
    margin-top: 10px;
    width:300px;
    padding:5px;
    box-sizing: border-box;
    border-radius: 5px;
    font-family: Arial, Helvetica, sans-serif;
    margin-top:20px;
    margin-left: 80px;
    box-shadow: none;


}
.switch input { 
  opacity: 0;
  width: 0;
  height: 0;
}
.question-box{
    width:100%;
}
.option-action-space-block{
    display: block;
    width:calc(100% - 200px);
    min-width:400px;
    height:auto;
    background-color: rgba(255, 255, 255, 0);
    margin-top: 20px;
    padding-top: 20px;
}
.option-label{
    display: inline-block;
    font-family: fantasy;
    font-size: 16px;
    font-weight: bold;
    margin-left: 20px;
    text-align: left;
    float:left;
    width:100px;
    margin-top: 60px;
    background-color: rgba(0, 0, 255, 0);
}
.round{
    border-radius: 34px;
}

.toggle{    
    display: inline-block;
    margin-top: 24px;
    margin-left: 20px;
    
    float:left;
}
.option-description{
    display: inline-block;
    font-family: Arial, Helvetica, sans-serif;
    width: calc(100% - 100px);
    background-color: rgba(0, 0, 255, 0);
    text-align: left;
    font-size: 14px;
    margin-left: 20px;
    margin-top: 20px;
    float:left;
    
}
.switch{
  position: relative;
  display: inline-block;
  width: 45px;
  height: 15px;
}
.slider{
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: .4s;
}
.slider:before {
  position: absolute;
  content: "";
  height: 20px;
  width: 20px;
  left: -1px;
  bottom: -3px;
  background-color: rgb(255, 255, 255);
  transition: .4s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}
.switch input:checked + .slider {
  background-color: #2196F3;
}
.switch input:checked + .slider:before {
  transform: translateX(26px);
}
.slider.round {
  border-radius: 34px;
}
.slider.round:before {
  border-radius: 50%;
}

.word-count{
    font-size: 12px;
    color:v-bind(jobInformation.color.textColor[0]);
    filter: invert(.2);
    width:fit-content;  
    float:right;
    margin-top:-68px;
    margin-right:10px;
    z-index: 10;
}
.next-button{
    width:fit-content;
    background: linear-gradient(15deg, white, rgb(209, 209, 209));
    color: rgb(109, 109, 109);
    border: rgb(0, 0, 0) solid 2px;
    padding: 5px 20px 5px 20px;
    border-radius: 10px;
    cursor: pointer;
    user-select: none;
    position:absolute; 
    right:100px;
    bottom:-90px;
    font-size: 16px;
}
.button:active{
    transform: scale(90%);
    background-color: #aaaaaa;
    box-shadow: 0 0 0 0 rgba(102, 102, 102, 0.24); /* Example of shadow change */

}
.button:hover{
    background-color: #bbbbbb;
}
.button{
    width: 18px;
    height: 18px;
    padding:10px;
    border-radius: 5px;
    border: solid #b0b0b0 1px;
    margin:0;
    background-color: #ffffff8c;
    border: white solid 3px;
    filter: invert(1);
}
.toolbar{
    background-color: #00000036;
    border-radius: 10px;
    overflow: hidden;
    height:fit-content;
    height:45px;
}
.editor{
    border-radius: 10px;
    padding:10px;
    overflow-y:auto;
    white-space: pre-wrap;
    resize: vertical

}
.freeform-input{
    width:calc(100% - 60px);
    resize: none;
    font-size: 16px;
    margin-top:10px;
    border: solid #696969 1px;
    box-sizing: border-box;
    border-radius: 10px;
    margin-bottom: 40px;
    font-family: fantasy;
    word-break: break-all; 
    
}

.input{
    width:100%;
    resize: none;
    font-size: 16px;
    padding:10px;
    margin-top:10px;
    color:v-bind(jobInformation.color.textColor[0]);
    box-sizing: border-box;
    border-radius: 10px;
    margin-bottom: 40px;
    font-family: fantasy;
    background-color: rgba(0, 0, 0, 0);
}
input,textarea, select, .freeform-input{
    background-color: #00000000;
    box-shadow: inset 0 0 5px #00000070;
}
.text-container{
    text-align: left;
    padding: 30px;
    font-family: Arial, sans-serif;
    padding-bottom: 100px;
    font-family: fantasy;
    color:v-bind(jobInformation.color.textColor[0]);
    position:relative;
}

.text{
    width:calc(100% - 60px);
    font-size: 16px;
    margin-bottom: 10px;
    
}


@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
</style>