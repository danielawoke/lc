<script setup>
import { useRoute, useRouter } from 'vue-router'
import { onMounted, nextTick, watch } from 'vue';
import { ref } from 'vue';
import JobDescription from '@/components/founder-space/interfaces/edit-cards/roles-card/job-description/view.vue';
import jobPage from '@/components/job-page/description.vue';
import colorChangePopup from '@/components/founder-space/interfaces/edit-cards/color-change/popup-jobs.vue';
import JobCreator from '@/components/founder-space/interfaces/edit-cards/roles-card/job-create-edit/popup.vue';

let props = defineProps({
    jobsCardData: Object,
    SetToEdit: Array
});

const route = useRoute();

let backDropClickColor = ref([false])
let colorEditMode = ref(false);
let jobIDForRemoval = ref("");
let removeJobPopup = ref(false);
let jobView = ref([false]);
let jobInformation = ref({});


let dummyColor = ref({backgroundColor: ["white"], jobCardColor: ["black"], textColor: ["white"]});

onMounted(async () => {
    dummyColor.value = JSON.parse(JSON.stringify(props.jobsCardData.color));
});

watch(backDropClickColor, async (newVal) => {
    if (newVal[0] == true) {
        console.log("backdrop clicked");
        const element = document.getElementById('popup-backdrop');
        await nextTick();
        const keyframes = [
        { opacity: 1 },
        { opacity: 0 }
        ];
        const time = 300;
        const timing = {
        duration: time, // milliseconds
        iterations: Infinity, // or a number, e.g., 3
        direction: 'alternate', // plays forward and then backward
        easing: 'ease-in-out'
        };
        // Play the animation
        const animation = element.animate(keyframes, timing);
        setTimeout(() => {
            animation.cancel();
            colorEditMode.value = false;
            backDropClickColor.value[0] = false;
        }, time);
    }
},{deep: true});

function chageColor(){
    colorEditMode.value = true;
}


let newJobRef = ref(false);

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
    jobInformation.value = emptyJob;
    jobView.value[0] = true;
}

async function editRole(job){
    jobInformation.value = job.job_object;
    jobView.value[0] = true;
}

function verifiedRemoval(){
    jobsCardData.value.jobs = jobsCardData.value.jobs.filter(job => job.jobID !== jobIDForRemoval.value);
    removeJobPopup.value = false;
}

function Cancelation(){
    removeCardPopup.value = false;
}

function saveCard(){
    props.jobsCardData.color = dummyColor.value;
    props.SetToEdit[0] = false;
}

function cancel(){
    props.SetToEdit[0] = false;
}

function mobileModeListener(){
    mobileMode.value = window.innerWidth <= 1200;
    console.log("Mobile mode:", mobileMode.value);
}

let mobileMode = ref(true)
mobileMode.value = window.innerWidth <= 1200;
window.addEventListener('resize', mobileModeListener);




</script>

<template>

    <!-- disable brackets in the freeform text editors -->

    <colorChangePopup v-if="colorEditMode" :backDropClickColor="backDropClickColor" :color="dummyColor" :originCard="originCard"/>
    <JobCreator v-if="jobView[0]" :renderVar="jobView" :jobInformation="jobInformation" :jobs="props.jobsCardData.jobs" :job_id="job_id"/>
        <div v-if="removeJobPopup" class="pop-up-backdrop">
            <div class="custom-alert-popup">
                <div class="alert-content">
                    <h2 class="popup-text">Are you sure you'd like to delete this job?</h2>
                    <button class="popup-button" @click="verifiedRemoval">Yes</button>
                    <button class="popup-button" @click="Cancelation">No</button>
                </div>
            </div>
        </div>

    <div v-if="mobileMode" class="card-color-surround" :style="{background: dummyColor.backgroundColor[0]}">
        <div class="card" style="width:100%">
            <div class="roles">
                <div class="left"> < </div>
                <!-- <input placeholder="Search for the work you'd like to do" class="search" /> -->
                <div class="roles-container-inline-correction">
                    <div class="roles-container">
                        <div class="dashed-border">
                            <div @click="addNewRole" class="add-role-card"> 
                                <img class="job-add-icon" src="@/assets/founder-space/edit/job-edit/add-plus.png" />
                                <div class="add-role-desc">ADD ROLE</div>
                            </div>
                        </div>
                        <div @click="editRole(job)" v-for="job in props.jobsCardData.jobs" class="role" :style="{background: dummyColor.jobCardColor[0], color: dummyColor.textColor[0]}">
                            <div class="role-title">{{ job.job_object.jobDescription.title[0] }}</div>
                            <div class="role-description">{{ job.job_object.jobDescription.summary[0] }}</div>
                            <div class="delete-job-button"></div>
                        </div>
                    </div>
                </div>
                <div class="right"> > </div>
            </div>
            <div id="hyper-buttons-left" style="width:100px">
                <img @click="chageColor" id="paint" src="@/assets/founder-space/edit/paint-icon.png" />
            </div>
            <div id="hyper-buttons-right">
                <img @click="saveCard" id="save" src="@/assets/founder-space/edit/save-icon.png" />
                <img @click="cancel" id="cancel" src="@/assets/founder-space/edit/x-icon.png" />
            </div>
        </div>        
    </div>
    <div v-else class="card-color-surround" :style="{background: dummyColor.backgroundColor[0]}">
        <div class="card">
            <div class="roles">
                <div class="left"> < </div>
                <!-- <input placeholder="Search for the work you'd like to do" class="search" /> -->
                <div class="roles-container-inline-correction">
                    <div class="roles-container">
                        <div class="dashed-border">
                            <div @click="addNewRole" class="add-role-card"> 
                                <img class="job-add-icon" src="@/assets/founder-space/edit/job-edit/add-plus.png" />
                                <div class="add-role-desc">ADD ROLE</div>
                            </div>
                        </div>
                        <div @click="editRole(job)" v-for="job in props.jobsCardData.jobs" class="role" :style="{background: dummyColor.jobCardColor[0], color: dummyColor.textColor[0]}">
                            <div class="role-title">{{ job.job_object.jobDescription.title[0] }}</div>
                            <div class="role-description">{{ job.job_object.jobDescription.summary[0] }}</div>
                            <div class="delete-job-button"></div>
                        </div>
                    </div>
                </div>
                <div class="right"> > </div>
            </div>
            <div id="hyper-buttons-left">
                <img @click="chageColor" id="paint" src="@/assets/founder-space/edit/paint-icon.png" />
            </div>
            <div id="hyper-buttons-right">
                <img @click="saveCard" id="save" src="@/assets/founder-space/edit/save-icon.png" />
                <img @click="cancel" id="cancel" src="@/assets/founder-space/edit/x-icon.png" />
            </div>
        </div>        
    </div>
</template>

<style scoped>
.popup-text{
    font-family: Fantasy;
    font-size: 16px;
    margin-bottom: 20px;
    text-align: center;
    color: white;
}
.popup-button{
    font-family: Fantasy;
    width: 80px;
    height: 40px;
    margin: 10px;
    border-radius: 10px;
    border: black solid 2px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.671);
    background-image: linear-gradient(45deg, black, rgb(59, 59, 59));
    color: rgb(255, 255, 255);
    cursor: pointer;
}
.pop-up-backdrop{
    position: fixed;
    top: 0;
    left: 0;
    width: 200%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 999;
    
}
.custom-alert-popup{
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: rgb(44, 44, 44);
    padding: 20px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
    z-index: 1000;
    padding: 20px;
    display: block; /* Initially hidden */
}
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
.job-add-icon{
    width:55%;
    height:55%;
    margin:auto;
    object-fit: contain;
    position: relative;
    margin-top: 5px;
    opacity: .5;
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
.add-role-desc{
    font-family:'Franklin Gothic Medium';
    font-family: sans-serif;
    color:#00000073;
    text-align: center;
    font-size:16px; 
    margin-top: 10px; 
    letter-spacing: 8px;
    
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
.add{
    width: 40px;
    height: 40px;
    background-color: rgb(0, 0, 0);
    color: white;
    font-size: 40px;
    border-radius: 50%;
    margin-top: -200px;
    margin-left: 230px;
    float:left;
    padding: 20px;
}
#paint{
    float:left;
    width:60px;
    height:60px;
    border: black solid 2px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.671);
    background-image: linear-gradient(45deg, black, rgb(95, 94, 94));
    border-radius: 50%;
    cursor:pointer;
}

#hyper-buttons-left{
    float:left;
    margin-top:-110px;
    width: 200px;
    height:100px;
    padding-bottom: 100px;
    z-index:100;
    margin-right: 70px;
}
#hyper-buttons-right{
    float:right;
    margin-top:-110px;
    width: 200px;
    height:100px;
    padding-bottom: 100px;
    z-index:100;
    
    margin-right: 70px;
}
#save{
    float:right;
    width:60px;
    height:60px;
    border: black solid 2px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.671);
    background-image: linear-gradient(45deg, black, rgb(95, 94, 94));
    border-radius: 50%;
    margin-left:40px;
    cursor:pointer;
}
#cancel{
    float:right;
    width:60px;
    height:60px;
    border: black solid 2px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.671);
    background-image: linear-gradient(45deg, black, rgb(95, 94, 94));
    border-radius: 50%;
    cursor:pointer;
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
    height: 130px;
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
    margin-bottom: 150px;
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
    margin-top: -130px;
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
    margin-top: -130px;
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
    z-index: 10;
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