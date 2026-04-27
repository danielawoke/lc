<script setup>

import { useRoute, useRouter } from 'vue-router'
import { nextTick, onMounted, watch } from 'vue';
import { ref } from 'vue';
import dayjs from 'dayjs';
import Header from '@/components/header.vue';
import { AccountLocal } from '@/lib/appwrite';
import axios from 'axios';
import Location from '@/components/supporting-components/location-project-create.vue';
const apiUrl = import.meta.env.VITE_APP_API_URL
const route = useRoute();
const router = useRouter();

let friendList = ref([]);
let userId = null;


onMounted(async () => {
    try{
        let user = await AccountLocal.get();
        console.log("USER:", user);
        userId = user.$id;
        // console.log("FRIENDS LIST:", friendsList);
    }catch(e){
        router.push('/login');
    }
    
});

let projectData = ref({
    title: "",
    location: "",
    remoteFriendly: false,
    physicalLocation: false
});

async function convertAddressToCoordinates(address){
    try{
        const response = await axios.get(`https://maps.googleapis.com/maps/api/geocode/json`, {
            params: {
                address: address,
                key: import.meta.env.VITE_GOOGLE_MAPS_API_KEY
            }
        });
        if(response.data.results.length > 0){
            const location = response.data.results[0].geometry.location;
            return location; // { lat: ..., lng: ... }
        }else{
            console.error("No results found for the given address.");
            return null;
        }
    }catch(err){
        console.error("Error converting address to coordinates:", err);
        return null;
    }
}


let partnerInvites = ref([]);


function removeTag(partner){
    let index = partnerInvites.value.indexOf(partner);
    if(index > -1){
        partnerInvites.value.splice(index, 1);
    }
}

function addPartner(){
    // This is just a placeholder, you would replace this with your actual logic to add a partner
    let newPartner = document.querySelector('.usertag-input').value;
    if(newPartner && !partnerInvites.value.includes(newPartner)){
        partnerInvites.value.push(newPartner);
        document.querySelector('.usertag-input').value = "";
    }
}

let sumbitting = false;

async function createProject(){

    if(sumbitting){
        return;
    }

    projectData.value.location = document.getElementById("location-input").value;

    document.querySelector('.button').innerText = "Loading...";
    sumbitting = true;
    let coordinates = await convertAddressToCoordinates(projectData.value.location);
    if (!coordinates) {
        coordinates = { lat: 0, lng: 0 };
    }
    let project_page_data = ref({
        "mainCard": {
            "title": projectData.value.title || "Project Title",
            "location": projectData.value.location || "Project Location",
            "image": 'https://jogfzuscvmxhjqnopyfd.supabase.co/storage/v1/object/public/project_page_images/default.png',
            "color": {
                "backgroundColor": ["white"],
                "titleColor": ["#000000"],
                "contentColor": ["#000000"],
                "locationColor": ["#000000"]
            },
            "physicalLocation": projectData.value.physicalLocation || false,
            "remote": projectData.value.remoteFriendly || false,
            "content": `<pre id='desc-text'>Welcome to your project draft! \n\nThis is the fouders's space of your project, it is where you will manage candidates that apply to your project, talk to and interview new candidates, design your project page, and the create role postings to recruit more memebers.\n\nTo set up your project page, click the pencil edit icon to the bottom right to make changes. Text editors will pop up in corresponding locations, and the rest should be easy to follow!\n\nTo add role/job postings for your project, and in the list of jobs you select the \"ADD ROLE\" button and a job creation menu will come up with more details.\n\nWhen new candidates apply, your entire team will be able to review thier application through the \"votes\" tab to the right, and collectively vote to reject or proceed to with a discussion/interview in the \"chat\"  tab in the right menu. For more details, go to the \"help\" tab.\n\nIf you feel like your project needs more space to really be presented propperly, at the bottom you can add extra cards by clicking the \"ADD CARD\" button.\n\nWhen youre ready to publish your project, go to settings, add a project descritpion, thne detoggle the \"Privatize\" setting under publicity.\n\nHave fun making something awsome, and I deeply thank you for contributing to lauch pad's community </pre>`,
            "coordinates": coordinates
        },
        "jobsCard": {
            "jobs": [],
            "color": {
                "backgroundColor": ["white"],
                "jobCardColor": ["black"],
                "textColor": ["white"],
            }
        },
        "extraCards": []
    });

    await axios.post(`${apiUrl}projects/create`, {
        project_page: project_page_data,
        project_meta: projectData.value,
        invites: partnerInvites.value,
        creator_id: userId
    }).then((response) => {
        console.log("Project created successfully:", response.data);
        router.push('/project-edit/'+response.data.project_id+'/edit');
    }).catch((error) => {
        console.error("Error creating project:", error);
        document.querySelector('.button').innerText = "Create Draft";
        if(error.response.status == 400){
            errorText.value = 'Only premimum members can be a part of more than one project at a time. To create this project. Please sign up for a premimum account, or leave the project you are currently in';
        }
        sumbitting = false;
    });

}

let errorText = ref('');

</script>

<template>
    <Header style="z-index:10" />
    <div class="container">
        <!-- <div class="outline-block"> -->
            <div class="queryBox">
                <div class="header">Project Create</div>
                <input class="title" placeholder="Project Title" v-model="projectData.title" />
                <div class="physical-toggle">
                    <input type="checkbox" class="check" v-model="projectData.physicalLocation" />
                    <label class="remote-text">Disable physical locations for project</label>
                </div>
                <Location :location="projectData.location" style="position: absolute; top: 140px; left:20px;"/>
                <div class="remote-toggle">
                    <input type="checkbox" class="check" v-model="projectData.remoteFriendly" />
                    <label class="remote-text">Make Project Remote Friendly</label>
                </div>
                <div class="pre-add-text">
                    Pre-Invite Partners (optional)
                </div>
                <div>
                    <input class="usertag-input" placeholder="@vcai11" />
                    <div @click="addPartner" class="add-button">+</div>
                </div>
                <div class="partner-listing">
                    <span class="partner-block" v-for="partner in partnerInvites" :key="partner">@{{ partner }}<span class="remove-partner" style="margin-left:5px;" @click="removeTag(partner)">X</span></span>
                </div>
                <div style="font-family:Arial, Helvetica, sans-serif; color:red; position:absolute; bottom:50px; margin:20px;">{{errorText}}</div>
                <div>
                    <div @click="createProject" class="button">Create Draft</div>
                </div>
            </div>
        <!-- </div> -->
    </div>
</template>

<style scoped>
.outline-block{
    max-width: 700px;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    padding:50px;
    width: 100%;
    border-radius: 200px;
}
.remove-partner{
    color:red;
}
.remove-partner:hover{
    cursor:pointer;
    color:white;
    transition: all 0.1s ease-in;
    background: black;
}
.partner-block:hover{
    background: rgba(0, 0, 0, 0.8);
    color: rgb(255, 255, 255);
    border: 1px white solid;
    transition: all 0.1s ease-in;
}
.partner-listing{
    position: absolute;
    top: 370px;
    left:20px;
    width:calc(90% + 18px);
    border: white solid 1px;
    border-radius: 10px;
    height: 50px;
    padding:5px;
    padding-left:0px;
    padding-right:0px;
    overflow-x: hidden;
    overflow-y: auto;
    background:black;
    
}
.partner-block{
    background: white;
    font-family: Arial, Helvetica, sans-serif;
    color: black;
    padding: 5px;
    width:fit-content;
    border-radius: 5px;
    margin: 5px;
    border: 1px white solid;
    display: inline-block;
}
.add-button{
    position: absolute;
    top: 330px;
    left: 240px;
    width:fit-content;
    width:25px;
    padding-bottom: 3px;
    padding-top:3px;
    background: black;
    font-family: Arial, Helvetica, sans-serif;
    color:white;
    font-weight: bold;
    border-radius: 5px;
    text-align: center;
    color:white;
    cursor:pointer;
    border: black solid 1px;
}
.usertag-input{
    position:absolute;
    top:330px;
    left:20px;
    background:black;
    color:white;
    padding:5px;
    border-radius:5px;
    border:none;
    outline:none;
    min-width: 200px;
}
.pre-add-text{
    position: absolute;
    top: 300px;
    left:20px;
    font-size: 16px;
    color: rgb(255, 255, 255);
    font-family: sans-serif;
}
.button{
    position: absolute;
    top:480px;
    right: 20px;
    width:fit-content;
    padding:10px 20px;
    background: black;
    font-family: Arial, Helvetica, sans-serif;
    color:white;
    font-weight: bold;
    border-radius: 10px;
    margin-top: 20px;
    cursor:pointer;
    border: black solid 1px;
    width:100px;
    text-align: center;
}
.button:hover{
    background: rgb(14, 14, 14); 
    color: white;
    transition: all .2s ease-in-out;
    border: white solid 1px;
    transform: scale(.97);
}
.button:active{
    filter: invert(1);
    color: white;
    transition: all 0.1s ease-in-out;
}
.physical-toggle{
    position: absolute;
    top: 200px;
    left:20px;
    display: flex;
    align-items: center;
}
.check{
    width: 20px;
    height: 20px;
    background-color: rgba(255, 255, 255, 0.8);
    border-radius: 5px;
}
.remote-text{
    font-size: 16px;
    color: rgb(255, 255, 255);
    font-family: sans-serif;
    margin-left:10px;
}
.remote-toggle{
    position: absolute;
    top: 250px;
    left:20px;
    display: flex;
    align-items: center;
}
.header{
    position: absolute;
    top:20px;
    left:20px;
    width: 90%;
    padding: 10px;
    font-size: 25px;
    margin: auto;
    color: rgb(255, 255, 255);
    background-color: rgba(255, 255, 255, 0);
    border:none;
    border-radius: 10px;
    color: rgb(255, 255, 255);
    font-weight: bold;
    font-family: Arial, Helvetica, sans-serif;
}
.title{
    position: absolute;
    top:90px;
    left:20px;
    width: 90%;
    padding: 10px;
    font-size: 15px;
    margin: auto;
    color: rgb(0, 0, 0);
    background-color: rgba(0, 0, 0, 0.658);
    border:none;
    border-radius: 10px;
    color: white;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
    
}
.queryBox{
    width: 100%;
    max-width: 600px;
    width:calc(100vw - 60px);
    margin-top: 20px;
    border-radius: 20px;
    position: relative;
    height:570px;
    left:50%;
    top: 50%;
    transform: translate(-50%, -50%);
    box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.5);
    background: linear-gradient(45deg, rgba(0, 0, 0, 0.815), rgb(54, 54, 54, 0.815));
    animation: fadeIn 0.1s ease-in-out;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}
.people-listing-name{
    font-size: 22px;
    font-weight: bold;
    color: rgb(0, 0, 0);
}
.people-listing-position{
    font-size: 14px;
    color: rgb(0, 0, 0);
    font-weight:normal;
}
.people-listing-date{
    font-size: 14px;
    color: rgb(0, 0, 0);
    font-weight:normal;
}
.person-block{
    border-radius: 20px;
    padding-top: 20px;
    padding-bottom: 20px;
    padding-left:40px;
    padding-right:40px;
    width:calc(100% - 140px);
    background-color: rgba(255, 255, 255, 0.164);
    margin:auto;
    margin-top: 10px;
    margin-bottom: 10px;
}
.person-block:hover{
    cursor:pointer;
    background-color: rgba(255, 255, 255, 0.541);
    transition: all 0.01s ease-in;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
}
.person-image{
    vertical-align: top;
    margin-right:10px; 
    width:10%; 
    max-width:100px;
    min-width: 80px;
    aspect-ratio: 1 / 1;
    border-radius:50%; 
    display:inline-block;
    background-color: black;
    background-size: cover;
    border: solid rgba(0, 0, 0, 0.466) 2px;
}
.text-block{
    position: relative;
    display: inline-block;
    font-size: 14px;
    color: rgb(0, 0, 0);
    font-family: sans-serif;
    width: calc(80%);
    font-weight: bold;
    background:rgba(0, 0, 0, 0);
    height:80px;
    margin-top:10px;
}
.people-listing{
    position: relative;
    overflow:auto;
    background-color: rgba(216, 216, 216, 0);
    height: auto;
    font-size: 12px;
    text-align: left;
    z-index: 20;
    overflow:hidden;
    overflow-y:auto;
    font-family: sans-serif;
    z-index: 20;
    width: calc(100% - 0px);
}
.container{
    display: block;
    position: absolute;
    top: 60px;
    left: 0px;
    width: calc(100vw - 0px);
    margin: auto;
    height: calc(100vh - 60px);
    overflow-y: auto;
    z-index:-1;
    background: radial-gradient(circle, rgb(11, 137, 255), rgb(123, 0, 134));
    
}
</style>