<script setup>
import { useRoute, useRouter } from 'vue-router'
import { onMounted, nextTick, watch } from 'vue';
import { ref } from 'vue';
import JobDescription from '@/components/founder-space/interfaces/edit-cards/roles-card/job-description/view.vue';
import jobPage from '@/components/job-page/description.vue';
import JobCreator from '@/components/founder-space/interfaces/edit-cards/roles-card/job-create-edit/popup.vue';
import JobView from '@/views/project_view/popup.vue';
import { AccountLocal } from '@/lib/appwrite.js';

let props = defineProps({
    jobsCardData: Object,
    SetToEdit: Array,
    viewMode: Boolean,
    projectTitle: String,
    preLoadPayload: Object,
});

const route = useRoute();
let jobView = ref([false]);
let jobInformation = ref({});
let userID = null;
let job_id = "";
onMounted(async () => {
    try {
        let user = await AccountLocal.get();
        userID = user.$id;
        console.log("User ID:", userID);
    } catch (error) {
        userID = null;
    }
});

async function addNewRole(){
    
    let emptyJob = {
        jobDescription: {
            title: [""],
            description: [""],
            summary: [""]
        },
        jobQuestions: {
            resume:["yes"],
            contacts: [["Email",1,"base"], ["Phone",0,"base"], ["IP-address",0,"base"]],
            anonymous: [false],
            extraQuestion: []
        },
        color: {
            backgroundColor: ["white"],
            textColor: ["black"]
        },
        settings: {
            closed: [false],
            maxApplications: [false, 100],
            applicationDeadline: [false, new Date().toISOString().split('T')[0]],
        }
    };
    job_id = "NEW";
    jobInformation.value = emptyJob;
    jobView.value[0] = true;
}

async function editRole(job){
    console.log(job.job_id);
    if(props.viewMode){
        candidateJobView.value[0] = true;
        jobInformation.value = job.job_object;
        job_id = job.job_id;
    }else{
        jobInformation.value = job.job_object;
        job_id = job.job_id;
        jobView.value[0] = true;
    }
}

function editMode(){
    props.SetToEdit[0] = true;
}

let candidateJobView = ref([false]);

function mobileModeListener(){
    mobileMode.value = window.innerWidth <= 1200;
    console.log("Mobile mode:", mobileMode.value);
}

let mobileMode = ref(true)
mobileMode.value = window.innerWidth <= 1200;
window.addEventListener('resize', mobileModeListener);



</script>

<template>
    <JobCreator v-if="jobView[0]" :renderVar="jobView" :jobInformation="jobInformation" :job_id="job_id"/>
    <JobView v-if="candidateJobView[0]" :renderVar="candidateJobView" :jobInformation="jobInformation" :job_id="job_id" :viewMode="viewMode" :userID="userID" :projectTitle="projectTitle"/>
    <JobView v-if="preLoadPayload?.render[0]" :renderVar="preLoadPayload?.render" :jobInformation="preLoadPayload?.jobInformation" :job_id="preLoadPayload?.job_id" :viewMode="viewMode" :userID="userID" :projectTitle="projectTitle"/>
    <div v-if="mobileMode" class="card-color-surround" :style="{background: props.jobsCardData.color.backgroundColor[0]}">
        <div class="card" style="width:100%">
            <div class="roles">
                <div class="left"> < </div>
                <!-- <input placeholder="Search for the work you'd like to do" class="search" /> -->
                <div class="roles-container-inline-correction">
                    <!-- <div class="roles-container">
                        <div @click="jobSelected" v-for="job in props.jobsCardData.jobs" class="role" :style="{background: props.jobsCardData.color.jobCardColor[0], color: props.jobsCardData.color.textColor[0]}">
                            <div class="role-title">{{ job.title }}</div>
                            <div class="role-description">{{ job.description }}</div>
                        </div>
                    </div> -->
                    <div class="roles-container">
                        <div v-if="!props.viewMode" class="dashed-border">
                            <div @click="addNewRole" class="add-role-card"> 
                                <img class="job-add-icon" src="@/assets/founder-space/edit/job-edit/add-plus.png" />
                                <div class="add-role-desc">ADD ROLE</div>
                            </div>
                        </div>
                        <div @click="editRole(job)" v-for="job in props.jobsCardData.jobs" class="role" :style="{background: props.jobsCardData.color.jobCardColor[0], color: props.jobsCardData.color.textColor[0]}">
                            <div class="role-title">{{ job.job_object.jobDescription.title[0] }}</div>
                            <div class="role-description">{{ job.job_object.jobDescription.summary[0] }}</div>
                            <div  v-if="!props.viewMode"  class="delete-job-button"></div>
                        </div>
                    </div>
                </div>
                <div class="right"> > </div>
            </div>
            <img v-if="!props.viewMode" id="edit-button" @click="editMode" class="edit-button" src="@/assets/founder-space/edit/edit-icon.png"/>
        </div>        
    </div>
    <div v-else class="card-color-surround" :style="{background: props.jobsCardData.color.backgroundColor[0]}">
        <div class="card">
            <div class="roles">
                <div class="left"> < </div>
                <!-- <input placeholder="Search for the work you'd like to do" class="search" /> -->
                <div class="roles-container-inline-correction">
                    <!-- <div class="roles-container">
                        <div @click="jobSelected" v-for="job in props.jobsCardData.jobs" class="role" :style="{background: props.jobsCardData.color.jobCardColor[0], color: props.jobsCardData.color.textColor[0]}">
                            <div class="role-title">{{ job.title }}</div>
                            <div class="role-description">{{ job.description }}</div>
                        </div>
                    </div> -->
                    <div class="roles-container">
                        <div v-if="!props.viewMode" class="dashed-border">
                            <div @click="addNewRole" class="add-role-card"> 
                                <img class="job-add-icon" src="@/assets/founder-space/edit/job-edit/add-plus.png" />
                                <div class="add-role-desc">ADD ROLE</div>
                            </div>
                        </div>
                        <div @click="editRole(job)" v-for="job in props.jobsCardData.jobs" class="role" :style="{background: props.jobsCardData.color.jobCardColor[0], color: props.jobsCardData.color.textColor[0]}">
                            <div class="role-title">{{ job.job_object.jobDescription.title[0] }}</div>
                            <div class="role-description">{{ job.job_object.jobDescription.summary[0] }}</div>
                            <div  v-if="!props.viewMode"  class="delete-job-button"></div>
                        </div>
                    </div>
                </div>
                <div class="right"> > </div>
            </div>
            <img v-if="!props.viewMode" id="edit-button" @click="editMode" class="edit-button" src="@/assets/founder-space/edit/edit-icon.png"/>
        </div>    
    </div>

    <!-- 
        HTML ARCHIVE
            <div class="jobs-container">
                <input class="job-search" placeholder="Search for certain roles here"  />
                <div class="meta-text">1321 results found</div>
                <div class="jobs">
                    <div v-for="job in jobs" class="job">
                        <div class="job-title">{{ job.title }}</div>
                        <div class="job-description">{{ job.description }}</div>
                    </div>
                </div>
            </div> 

        <div class="tab"> 
            <div class="tabs"> 
                <div class="taber">Prev</div>
                <div class="tab-container">
                    <input class="job-tab-selection" :value="tab"/>
                    <div class="total" >/<div class="remainingTabs">{{ 1 }}</div></div>
                </div>
                <div class="taber">Next</div>
            </div>
        </div>
    
    -->
</template>

<style scoped>
.delete-job-button{
    width: 22px;
    height: 22px;
    color: white;
    background-color: rgb(24, 24, 24);
    filter: invert(0);
    font-size: 16px;
    border-radius: 50%;
    position: absolute;
    border: rgb(255, 255, 255) solid 2px;
    top: 5px;
    right: 5px;
    opacity: 1;
    z-index: 1;
    background-image: url("@/assets/founder-space/edit/edit-icon.png");
    background-size: contain;
}
.dashed-border:hover{
    opacity: 1;
    cursor: pointer;
}
.dashed-border{
    width: fit-content;
    width:220px;
    opacity: .5;
    margin-left:10px;
    margin-right:10px;
    height: fit-content;
    background-image: url("data:image/svg+xml,%3csvg width='70%25' height='60%25' xmlns='http://www.w3.org/2000/svg'%3e%3crect width='100%25' height='100%25' fill='none' stroke='%23333' stroke-width='3' stroke-dasharray='20%2c 10' stroke-dashoffset='11' stroke-linecap='butt'/%3e%3c/svg%3e");
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
.add-role-desc{
    font-family:'Franklin Gothic Medium';
    font-family: sans-serif;
    color:#00000073;
    text-align: center;
    font-size:16px; 
    margin-top: 10px; 
    letter-spacing: 8px;
    
}
.job-add-icon{
    width:55%;
    height:55%;
    margin:auto;
    object-fit: contain;
    position: relative;
    margin-top: 5px;
    opacity: .5;
}
.add-role-card{
    width:200px;
    height:87px;
    margin-right:10px;
    background-color: #ffffff00;
    color:#b1b1b1;
    padding:10px;
    border-radius: 10px;
    display: inline-block;
    position: relative;
    float: left;
}
.search{
    font-family: Arial, sans-serif;
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    margin-top: -40px;
    font-size: 20px;
    font-weight: bold;
    width:80%;
    background: #00000000;
}
.roles-container-inline-correction{
    display: inline-block;
    height: 150px;
    width: calc(100% - 60px);
    overflow-x: auto;
    background-color: #00000000;
    position: relative;
    white-space: nowrap;
    
}
.roles-container{
    display: flex;
    float: left;
    padding-top: 10px;

}
.roles{
    margin-top: 100px;
    width:80%;
    height: 130px;
    white-space: nowrap;
    margin-bottom: 200px;
    box-shadow: #00000080 0px 0px 30px;
    background-color: #ffffff31;
    border-radius: 30px;
    padding: 20px;
    padding-top:50px;
    padding-bottom:20px;
    margin:auto;
    overflow: hidden;
    margin-top: 40px;
    margin-bottom: 120px;
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
    font-size: 40px;
    font-weight: bold;
    color:#000000;
    width:50px;
    height:260px;
    line-height: 250px;
    margin-top: -160px;
    margin-left: -20px;
    cursor: pointer;
    display: inline-block;
    background-color: #00000000;
    vertical-align: middle;
    
    box-shadow: #00000080 0px 0px 30px;
}
.right{
    font-size: 40px;
    font-weight: bold;
    color:#000000;
    width:50px;
    height:260px;
    line-height: 250px;
    margin-top: -160px;
    cursor: pointer;
    display: inline-block;
    background-color: #00000000;
    vertical-align: middle;
    box-shadow: #00000080 0px 0px 30px;
}
.role-title{
    white-space: wrap;
    font-family: sans-serif;
    font-size: 18px;
    font-weight: bold;
    text-align: left;
}
.role-description{
    white-space: wrap;
    font-family: sans-serif;
    font-size: 14px;
    text-align: left;
    padding-left: 5px;
    margin-top: 5px;
    overflow: hidden;
    text-break: break-word;
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

.job-search{
    width: 200px;
    border-radius: 5px;
    padding: 5px;
    font-size: 16px;
    margin:auto;
    margin-bottom: 20px;
    background-color: #00000000;
    width:80%;
}
.jobs-container{
    display:block;
    font-family: Arial, Helvetica, sans-serif;
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
    margin-bottom: 130px;
    padding-bottom: 100px;
    box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.164);
    overflow: hidden;
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
    margin-bottom: 8px;
    font-size: 14px;
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
.job-tab-selection{
    font-family: Arial, sans-serif;
    width: 25px;
    height: 25px;
    text-align: center;
    border-radius: 5px;
    color: rgb(255, 255, 255);
    background-color: #000000;
    
    font-weight: bolder;
    outline: none;
    border-bottom: solid 3px #ffffff;
}
.tab{
    
    font-weight: bolder;
    background-color: #ffffff00;
    height: 50px;
    padding: 25px;
    padding-left: 0;
    float: right;
}
.tabs{
    background-color: #00000000;
    color: white;
    margin-bottom: 30px;
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
    background-image: linear-gradient(45deg, #000000, #383838);
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.671);
    color: white;
    border-radius: 5px;
    text-align: center;
    line-height: 30px;
    cursor: pointer;
}

.main-divider{
    border: 0;
    height: 3px;
    background-color: #444444;
    margin: 10px 0 20px 0;
}
.line{

}

.job-title {
    font-weight: bold;
    font-size: 20px;
    margin-bottom: 5px;
    color: #1a1a1a;
}
.job-description {
    font-size: 16px;
}

.edit-button{
    position: relative;
    width: 60px;
    height: 60px;
    float: right;
    border-radius: 50%;
    border: black solid 2px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.671);
    background-image: linear-gradient(45deg, black, rgb(94, 94, 94));
    cursor: pointer;
    z-index: 0;
    margin-right: 70px;
    margin-top: -70px;
}

.card-color-surround{
}
.card{
    width: calc( (100% - 180px) );
    height: auto;
    max-width: 1600px;
    border-radius: 10px;
    padding: 20px;
    margin: auto;
}

.header-text {
    
    font-weight: normal;
    font-family: fantasy;
    color: #333;
    font-size: 40px;
    padding-top:60px;
    width: calc(100% -60px);
    height:auto;
    overflow-wrap: break-word;
    text-align: left;
    
}
</style>

<style>

</style>