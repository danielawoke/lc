<script setup>
import { useRoute, useRouter } from 'vue-router'
import { nextTick, onMounted, watch, onUnmounted} from 'vue';
import { ref } from 'vue';
import axios from 'axios';
import MainCard from '@/components/founder-space/interfaces/edit-cards/main-card.vue';
import RolesCard from '@/components/founder-space/interfaces/edit-cards/roles-card.vue';
import AddCard from '@/components/founder-space/interfaces/edit-cards/add-card.vue'
import ExtraCard from '@/components/founder-space/interfaces/edit-cards/extra-question.vue';
import {AccountLocal} from '@/lib/appwrite.js';
import { createClient } from '@supabase/supabase-js';
const supabase = createClient(import.meta.env.VITE_SUPABASE_URL, import.meta.env.VITE_SUPABASE_ANON_KEY);

// extra card json for refrence

// let extraCards = ref([
//     {
//         conditions:{
//             header:[true],
//             paragraph:[true],
//             image:[true],
//             leftRightRelation:[false]
//         },
//         header: ["How do you plan to use the funds?"],
//         paragraph: ["We plan to use the funds to expand our team and accelerate product development."],
//         image: ["https://styles.redditmedia.com/t5_2qh1u/styles/communityIcon_21ykcg22rm6c1.png?width=128&frame=1&auto=webp&s=ed570cc1fa570576ed77f45ce8490b9f41c89cdc"],
//         leftRightRelation: [null],
//         backgroundColor: ["#FFDDC1"],
//         textColor: ["#000000"],
//         headerColor: ["#000000"],
//         markedForDeletion: [false],
//         id: 1,
//         recentlySpawned: [false]
//     },
//     {
//         conditions:{
//             header:[true],
//             paragraph:[true],
//             image:[true],
//             leftRightRelation:[false]
//         },
//         header: ["New Card Header"],
//         paragraph: ["New card content goes here."],
//         image: [""],
//         leftRightRelation: [false],
//         backgroundColor: ["#FFFFFF"],
//         textColor: ["#000000"],
//         headerColor: ["#000000"],
//         markedForDeletion: [false],
//         id: 2,
//         recentlySpawned: [false]
//     }
// ]);

let projectProfileData = ref({
    mainCard: {
        title: "",
        location: "",
        image: new URL("@/assets/founder-space/edit/default-comp-image.png", import.meta.url),
        color: {backgroundColor: ["white"], titleColor: ["#000000"], contentColor: ["#000000"], locationColor: ["#000000"]},
        physicalLocation:false,
        remote:true,
        content: ""
    },
    jobsCard: {
        jobs: [],
        color: {
            backgroundColor: ["white"],
            jobCardColor: ["black"],
            textColor: ["white"]
        }
    },
    extraCards: []
});

let jobs_channel = null;
let page_channel = null;
let socketUpdate = false;
let preLoadPayload = ref({
    render: [false],
    jobInformation: null,
    job_id: null
})

let route = useRoute();


function mobileModeListener(){
    mobileMode.value = window.innerWidth <= 768;
    console.log("Mobile mode:", mobileMode.value);
}

let mobileMode = ref(true)
mobileMode.value = window.innerWidth <= 768;

onMounted(async () => {
    // something about local storage?
    try{


        let user = await AccountLocal.get();

        await axios.post(`${import.meta.env.VITE_APP_API_URL}projects/admin-load/${route.params.projectId}/${user.$id}/`, { private_key: import.meta.env.VITE_API_PRIVATE_KEY })
            .then(response => {
                let data = response.data;
                projectProfileData.value = data.project_page._value;
            });

        await axios.get(`${import.meta.env.VITE_APP_API_URL}jobs/project-load/${route.params.projectId}/false`)
            .then(response => {
                let data = response.data;
                projectProfileData.value.jobsCard.jobs = data;
                console.log(route.query.job_id);
            });

            
        window.addEventListener('resize', mobileModeListener);

        page_channel = await supabase
            .channel('projects')
            .on(
                'postgres_changes',
                {
                    event: 'UPDATE',
                    schema: 'public',
                    table: 'projects',
                    filter: `project_id=eq.${route.params.projectId}`
                },
                (payload) => {
                    let jobs = projectProfileData.value.jobsCard.jobs;
                    projectProfileData.value.mainCard = payload.new.project_page._value.mainCard;
                    projectProfileData.value.jobsCard.color = payload.new.project_page._value.jobsCard.color;
                    projectProfileData.value.jobsCard.jobs = jobs;

                    let orderChange = false;
                    
                    for(let i = 0; i < payload.new.project_page._value.extraCards.length && i < projectProfileData.value.extraCards.length; i++){
                        if(payload.new.project_page._value.extraCards[i].id !== projectProfileData.value.extraCards[i].id ){
                            orderChange = true;
                            break;
                        }
                    }

                    if(!orderChange){
                        projectProfileData.value.extraCards = payload.new.project_page._value.extraCards;
                    }else{
                        let i = 0;
                        while(i < payload.new.project_page._value.extraCards.length){
                            console.log("Checking card with id:", payload.new.project_page._value.extraCards[i].id, " against ", projectProfileData.value.extraCards[i].id);
                            if(payload.new.project_page._value.extraCards[i].id != projectProfileData.value.extraCards[i].id){
                                projectProfileData.value.extraCards.splice(i,1);
                            }
                            i++;
                        }
                    }
                    

                    // let curr_proj_index = 0;
                    // let curr_payload_index = 0;
                    // while(curr_proj_index < projectProfileData.value.extraCards.length){
                    //     if(payload.new.project_page._value.extraCards[curr_payload_index].id !== projectProfileData.value.extraCards[curr_proj_index].id){
                    //         projectProfileData.value.extraCards.splice(curr_proj_index, 1);
                    //     }
                    //     else{
                    //         curr_proj_index++;
                    //         curr_payload_index++;
                    //     }
                    // }
                    // for(let i = curr_payload_index; i < payload.new.project_page._value.extraCards.length; i++){
                    //     projectProfileData.value.extraCards.push(payload.new.project_page._value.extraCards[i]);
                    // }

                    // projectProfileData.value.extraCards = payload.new.project_page._value.extraCards;
                    socketUpdate = true;
                }
            )
            .subscribe();
        jobs_channel = await supabase
            .channel('jobs')
            .on(
                'postgres_changes',
                {
                    event: '*',
                    schema: 'public',
                    table: 'jobs',
                    filter: `project_id=eq.${route.params.projectId}`
                },
                (payload) => {
                    if(payload.eventType === 'INSERT') {
                        // console.log("New job added:", payload.new);
                        projectProfileData.value.jobsCard.jobs.unshift(payload.new);
                    } else if (payload.eventType === 'UPDATE') {
                        // console.log("Job updated:", payload.new.job_id);
                        for (let i = 0; i < projectProfileData.value.jobsCard.jobs.length; i++){
                            if(projectProfileData.value.jobsCard.jobs[i].job_id === payload.new.job_id){
                                projectProfileData.value.jobsCard.jobs[i].job_object = payload.new.job_object;
                                break;
                            }
                        }
                    } else if (payload.eventType === 'DELETE') {
                        // console.log("Job deleted:", payload.old.job_id);
                        for (let i = 0; i < projectProfileData.value.jobsCard.jobs.length; i++){
                            if(projectProfileData.value.jobsCard.jobs[i].job_id === payload.old.job_id){
                                projectProfileData.value.jobsCard.jobs.splice(i, 1);
                                break;
                            }
                        }
                    }
                }
            )
            .subscribe();
    }
    catch(error) {
        console.error("Error loading project data:", error);
    }

    // for (let i = 0; i < 23; i++){
    //     projectProfileData.value.jobsCard.jobs.push({title: "", description: ""});
    // }
})

onUnmounted(() => {
  supabase.removeChannel(page_channel);
  supabase.removeChannel(jobs_channel);
});

// let mainCardData = ref({
//     title: "Project Title",
//     location: "The location they game",
//     image: new URL("@/assets/founder-space/edit/default-comp-image.png", import.meta.url),
//     color: {backgroundColor: ["#FFFF00"], titleColor: ["#000000"], contentColor: ["#000000"], locationColor: ["#000000"]},
//     physicalLocation:true,
//     remote:true,
//     content: `<pre id='desc-text'>Welcome to your project draft! \n\nThis is the fouders's space of your project, it is where you will manage candidates that apply to your project, talk to and interview new candidates, design your project page, and the create role postings to recruit more memebers.\n\nTo set up your project page, click the pencil edit icon to the bottom right to make changes. Text editors will pop up in corresponding locations, and the rest should be easy to follow!\n\nTo add roles/job postions for your project, edit the jobs card underneath this one to add roles. Simply click on edit, and in the list of jobs you select the \"ADD ROLE\" button and a job creation menu will come up with more details.\n\nWhen new candidates apply, your entire team will be able to review thier application through the \"votes\" tab to the right, and collectively vote to reject or proceed to with a discussion/interview in the \"chat\"  tab in the right menu. For more details, go to the \"help\" tab.\n\nIf you feel like your project needs more space to really be presented propperly, at the bottom you can add extra cards by clicking the \"ADD CARD\" button.\n\nWhen youre ready to publish your project, go to settings, add a project descritpion, thne detoggle the \"Privatize\" setting under publicity.\n\nHave fun making something awsome, and I deeply thank you for contributing to lauch pad's community </pre>`
// });


// let jobsCardData = ref({
//     jobs: [
//         { title: 'Any', description: 'Come to us, show us what you can do, and we\'ll try to make a place for you' }
//     ],
//     color: {
//         backgroundColor: ["white"],
//         jobCardColor: ["black"],
//         textColor: ["white"]
//     }
// });

// let changeInduced = ref(false);

watch(projectProfileData, async (newVal) => {

    if(socketUpdate){
        socketUpdate = false;
        return;
    }

    let new_proj_data = {
                "dep": {
                    "sc": 0,
                    "version": 0,
                    "__v_skip": true
                },
                "_value": newVal,
                "__v_isShallow": false,
            }

    axios.post(`${import.meta.env.VITE_APP_API_URL}projects/update-page/${route.params.projectId}`, { project_page: new_proj_data, private_key: import.meta.env.VITE_API_PRIVATE_KEY })
    .then(response => {
        console.log("Project page updated successfully");
    })
    .catch(error => {
        console.error("Error updating project page:", error);
    });
}, { deep: true });

let viewMode = ref(false);

</script>

<template>

<!-- Add websocket to view portion of components to have changes come and prevent overwritting issues, may or may not be implemented -->

<!-- Jobs can be overwritten when being added, this issue is impractical, it prevents two people from creating jobs at the same time, which can be a serious problem
        Redesign so that jobs are inserted and removed individually, not all in one clump of objects. Also I may bring job adding to the front
        and the editing will just be for card itself

        probabily isnt that bad just copy main edit over, copy the added cards over directly, and make jobs card more percise and independent
-->

<div class="container" :style="{width: mobileMode ? '100vw' : 'calc(100vw - 50px)', marginLeft: mobileMode? '0px': '50px', overflowX:'hidden'}">
    <MainCard :mainCardData="projectProfileData.mainCard" :viewMode="viewMode"/>
    <RolesCard :jobsCardData="projectProfileData.jobsCard" :viewMode="viewMode" :preLoadPayload="preLoadPayload"/>
    <ExtraCard v-for="(card, index) in projectProfileData.extraCards" :key="card.id" :cardInfo="card" :extraCards="projectProfileData.extraCards" :viewMode="viewMode"/>
    <AddCard :currentCards="projectProfileData.extraCards"/>
</div>
 <!-- <div class="publish">publish</div> -->

</template>

<style scoped>
.publish{
    width:100px;
    height:40px;
    background-color: rgb(255, 119, 119);
    color: white;
    font-family: Arial, Helvetica, sans-serif;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 20px;
    position: absolute;
    bottom: 30px;
    right: 30px;
}
.popup{
    width:500px;
    height:130px;
    position: absolute;
    top: 80px;
    right:30px;
    background: rgba(255, 255, 255, 1);
    border-radius: 20px;
    padding:20px;
    font-size: 16px;
    font-family: arial;
}
.container{
    height:calc(100vh - 60px);
    overflow: auto;
    position: absolute;
    margin-top: 20px;
    left: 0;
    background-color: rgb(255, 255, 255);
    z-index: -2;
    text-align: center;
}
</style>