<script setup>
import { nextTick } from 'vue';
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import { AccountLocal } from '@/lib/appwrite';
import axios from 'axios';
import router from '@/router';
const route = useRoute();
const apiURL = import.meta.env.VITE_APP_API_URL;

let settings_config = ref({
    private_project: false,
    remote: false,
    remove_physical_locations: false,
    description:""
});

let mode = ref('chat');
let configureMode = ref('Room Settings');
let currentImage = ref('@/assets/founder-space/chat/closed-door.svg');
let usertag = ref('');
let userData = null;
onMounted(async () => {
    await axios.get(`${apiURL}projects/settings/load/${route.params.projectId}`).then((response) => {
        settings_config.value = response.data.settings;
        nextTick(() => {
            let wordCountDisplay = document.querySelector('.word-count');
            wordCountDisplay.textContent = `${settings_config.value.description.length}/300`;
        });
    }).catch((error) => {
        console.error("Error loading project settings:", error);
    });
    
    userData = await AccountLocal.get();
    
    await axios.get(`${apiURL}users/search/full_profile/${userData.$id}`).then((response) => {
        usertag.value = response.data.profile[0].user_tag;
    }).catch((error) => {
        console.error("Error checking project membership:", error);
    });
});

function updateWordCount(event){
    let wordCount = event.target.value.length;
    let wordCountDisplay = event.target.nextElementSibling;
    event.target.value = event.target.value.replace(/\n/g, ""); // Remove newlines from the input
    if(wordCount > 300){
        event.target.value = event.target.value.slice(0, 300);
        wordCount = 300;
    }
    wordCountDisplay.textContent = `${wordCount}/300`;
}

async function saveChanges(){
    try {
        settings_config.value.description = document.querySelector('.rename-input').value;
        console.log("Saving changes with:", settings_config.value);
        await axios.post(`${apiURL}projects/settings/edit/${route.params.projectId}`, {
            settings: settings_config.value
        }).then((response) => {
            let changesHover = document.querySelector('.changes-hover');
            changesHover.style.display = 'block';
            setTimeout(() => {
                changesHover.style.display = 'none';
            }, 5000);
        }).catch((error) => {
            console.error("Error updating project settings:", error);
        });
    } catch (error) {
        console.error("Error showing changes hover:", error);
    }
    
}

async function confirmLeave(){
    let deleteText = document.getElementById('deleteText').value;
    if(deleteText === usertag.value){
        await axios.post(`${apiURL}projects/leave/${route.params.projectId}/${userData.$id}`).then((response) => {
            router.push('/');
        }).catch((error) => {
            console.error("Error leaving project:", error);
        });
        // router.push('/');
        // window.location.reload();
       
    } else {
        alert("Usertag does not match. Please retype your usertag to confirm.");
    }
}

let popupActive = ref(false);

function toggleLeaveProject(){
    popupActive.value = true;
}

function mobileModeListener(){
    mobileMode.value = window.innerWidth <= 768;
    console.log("Mobile mode:", mobileMode.value);
}

let mobileMode = ref(true)
mobileMode.value = window.innerWidth <= 768;
window.addEventListener('resize', mobileModeListener);




</script>

<template>

        
        <div v-if="popupActive" @click.self="popupActive=false" class="popup-backdrop">
            <div class="changeRoomNamePopup">
                <div class="popupContent">
                    <div class="room-edit-header">Room Settings</div>
                    <div style="margin-bottom:20px; font-family:Arial, Helvetica, sans-serif; color:rgb(0, 0, 0);">Retype your usertag to confirm deletion</div>
                    <input class="room-edit-input" id="deleteText" :placeholder="usertag" />
                    <button class="room-edit-delete" style="float:right;" @click="confirmLeave">Confirm Leave</button>
                </div>
            </div>
        </div>

        <div class="container" :style="{width: mobileMode ? '100vw' : 'calc(100vw - 50px)', marginLeft: mobileMode? '0px': '50px'}">
            <div class="full-setting-container">
                <div class="setting-display-container">
                    <div>
                        <div class="prefacing-header">
                            General
                            <div class="sub-text">Make changes to the entire project's operations</div>
                        </div>
                        <div class="question-box">
                            <div class="option-label">
                                Publicity
                            </div>
                            <div class="option-action-space-block">
                                <div class="toggle">
                                    <label class="switch">
                                        <input type="checkbox" :checked="settings_config.private_project" @click="settings_config.private_project = !settings_config.private_project">
                                        <span class="slider round"></span>
                                    </label>
                                </div>
                                <div class="option-description">
                                    <div><b>Privatize Project</b></div>
                                    <div>This will take the project away from public view. Memebers can still chat through the chat feature</div>
                                </div>
                            </div>
                        </div>
                        <div class="question-box">
                            <div class="option-label">
                                Location
                            </div>
                            <div class="option-action-space-block">
                                <div class="toggle">
                                    <label class="switch">
                                        <input type="checkbox" :checked="settings_config.remote_friendly" @click="settings_config.remote_friendly = !settings_config.remote_friendly">
                                        <span class="slider round"></span>
                                    </label>
                                </div>
                                <div class="option-description">
                                    <div><b>Remote Friendly</b></div>
                                    <div>This will show on the project homepage and search results that you are a remote project</div>
                                </div>
                                <div class="toggle">
                                    <label class="switch" >
                                        <input type="checkbox" :checked="settings_config.remove_physical_locations" @click="settings_config.remove_physical_locations = !settings_config.remove_physical_locations">
                                        <span class="slider round"></span>
                                    </label>
                                </div>
                                <div class="option-description">
                                    <div><b>Remove Physical Locations</b></div>
                                    <div>This will remove physical locations from the main page of the project, and the project will not be categorized as being local to any physical areas in search results</div>
                                </div>
                            </div>
                        </div>
                        
                                
                        <div>
                            <div class="input-label">
                                Project Description
                                <div class="sub-text">On the main page and search results, this will be the brief summary of your project to others</div>
                            </div>
                            <div style="width: calc(100% - 100px); max-width: 400px;">
                                <textarea @input="updateWordCount" class="rename-input" placeholder="Enter project description" :value="settings_config.description"></textarea>
                                <div class="word-count">0/300</div>
                            </div>
                        </div>
                    </div>
                    <div class="option-padding">
                        <div class="delete-room-button" @click="toggleLeaveProject">Leave Project</div>
                    </div>
                    <div style="margin-left:20px; margin-top:10px;">
                        <div class="sub-text">If you are the only person in the project, this will delete the project permanently</div>
                    </div>
                    <div style="position:relative;">
                        <div class="changes-hover">Changes Saved</div>
                        <div @click="saveChanges" class="save-button" >
                            Save
                        </div>
                    </div>
                    <div style="height:300px"></div>
                </div>
            </div>
        </div>



    <!-- HTML ARCHIVE -->

    
    <!-- <div class="header-of-chat">
        <div class="room-display">
            <div class="change-room-button" @click="currentImage = currentImage === '@/assets/founder-space/chat/closed-door.svg' ? '@/assets/founder-space/chat/open-door.svg' : '@/assets/founder-space/chat/closed-door.svg'"></div>
            <div class="room-name-box">
                <p style="font-family: fantasy; font-size: 14px; color: rgb(0, 0, 0); margin-top: 20px;">Room 1: Main Room</p>
                <p style="font-family: fantasy; font-size: 14px; color: rgb(0, 0, 0);">Room 2: Breakout Room</p>
                <p style="font-family: fantasy; font-size: 14px; color: rgb(0, 0, 0);">Room 3: Breakout Room</p>
            </div>
        </div>
        <div class="room-title">Main Room</div>
    </div> -->

    <!-- Sengs -->
</template>

<style scoped>
.room-edit-delete:hover{
    background: red;
    color:rgb(255, 255, 255);
    filter: brightness(1);
    transition: all ease 0.3s;
    
}
.room-edit-delete{
    background-color: transparent;
    color: rgb(0, 0, 0);
    font-family: Arial, Helvetica, sans-serif;
    font-size: 14px;
    border: 1px solid rgb(0, 0, 0);
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    float:left;
}
.room-edit-sumbit:hover{
    filter: brightness(.8);
}
.room-edit-sumbit:active{
    filter: brightness(.6);
}
.room-edit-sumbit{
    background-color: rgb(255, 255, 255);
    color: rgb(0, 0, 0);
    font-family: Arial, Helvetica, sans-serif;
    font-size: 14px;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    float:right;
}
.room-edit-input{
    width: calc(100% - 20px);
    padding: 10px;
    background-color: transparent;
    color:rgb(0, 0, 0);
    margin-bottom: 20px;
    border-radius: 5px;
    font-size: 16px;
}
.room-edit-header{
    font-family: Arial, Helvetica, sans-serif;
    font-size: 20px;
    color: rgb(0, 0, 0);
    text-align: center;
    margin-bottom: 20px;
}
.changeRoomNamePopup{
    background: linear-gradient(to top, white, rgb(255, 255, 255));
    padding: 20px;
    border-radius: 10px;
}
.popup-backdrop{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}
@keyframes fadeInOut {
    0% { opacity: 0; }
    10% { opacity: 1; }
    90% { opacity: 1; }
    100% { opacity: 0; }
}
.changes-hover{
    display: none;
    position: absolute;
    right: 50px;
    bottom: -70px;
    padding: 10px 20px;
    background-color: rgb(0, 0, 0);
    color: white;
    font-family: Arial, Helvetica, sans-serif;
    border-radius: 5px;
    animation: fadeInOut 5s ease-in-out;
}
.save-button:hover{
    transition: all 0.3s ease;
    background: linear-gradient(to top, rgb(0, 0, 0), rgb(95, 95, 95));
    color: rgb(255, 255, 255);
    cursor: pointer;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
}
.save-button{
    display: block;
    position: absolute;
    right: 50px;
    bottom: -120px;
    padding: 10px 20px;
    background-color: rgb(0, 0, 0);
    color: white;
    font-family: Arial, Helvetica, sans-serif;
    border-radius: 5px;
    border: 2px solid
}
.word-count{
    font-family: Arial, Helvetica, sans-serif;
    color: rgb(73, 73, 73);
    font-size: 12px;
    text-align: right;
    margin-right:-20px;
    margin-top:-20px;
}
.rename-input{
    display: block;
    padding: 10px;
    margin-left: 18px;
    width: calc(100%);
    background-color: rgba(80, 80, 80, 0.123);
    outline: none;
    border: none;
    resize: none;
    border-radius: 5px;
    padding-bottom:30px;
    color: rgb(5, 5, 5);
    font-size: 14px;
    font-family: Arial, Helvetica, sans-serif;
    height: 100px;
}
.input-label{
    font-family: Arial;
    color: rgb(19, 19, 19);
    font-size: 22px;
    font-weight: bold;
    margin-left: 20px;
    text-align: left;
    float:left;
    width:100%;
    margin-top: 60px;
    margin-bottom:20px;
    background-color: rgba(0, 0, 255, 0);

}
.sub-text{
    font-family: fantasy;
    color: rgb(73, 73, 73);
    font-size: 14px;
    margin-top: 10px;
    background-color: rgba(0, 0, 255, 0);
    text-align: left;
    display:block;
    overflow:hidden;
    font-weight: normal;
}
.setting-mark{
    position:relative;
    font-family: fantasy;
    color:rgb(34, 34, 34);
    padding-bottom:0px;
    width:300px;
    padding:20px;
    padding-top:10px;
    padding-bottom:10px;
    background: rgba(1, 1, 107, 0);
    text-align: left;
    display:inline-block;
    overflow:hidden;
    font-weight: bold;
}
.settings-footer-container:hover{
    background-color: rgba(0, 0, 0, 0);
    opacity: 1;
}
.settings-footer-container{
    display: block;
    position: absolute;
    left: 0px;
    top: 20px;
    padding: 15px;
    width: 230px;
    background-color: rgba(185, 180, 180, 0);
    opacity: 0.6;
    transition: all 0.3s ease;
    cursor: pointer;
}
.setting-text{
    font-family: fantasy;
    padding-bottom:0px;
    width:200px;
    margin-top: -10px;
    background: rgba(0, 0, 255, 0);
    text-align: left;
    display:inline-block;
    overflow:hidden;
    font-weight: bold;
    transform: translate(40px, 0);
}
.selected-setting{
    font-family: fantasy;
    width:275px;
    padding:10px;
    margin-left: 15px;
    text-align: left;
    background-color: #ffffff2a;
    border-radius: 5px;
    border-left: 3px solid rgba(46, 46, 46, 0.87);
}
.selected-setting:hover{
    cursor: pointer;
    background-color: #ffffff40;
}
.unselected-setting{
    font-family: fantasy;
    width:276px;
    padding:8px;
    padding-left:10px;
    padding-right:10px;
    margin-left: 10px;
    text-align: left;
    background-color: #58585800;
    border: 2px solid rgba(255, 255, 255, 0.164);
    border-radius: 5px;
}
.unselected-setting:hover{
    cursor: pointer;
    background-color: #3d3d3dc7;
}
.chat-icon{
    width: 30px;
    height: 30px;
    background-color: rgba(221, 221, 221, 0.623);
    margin-left: -110px;
    margin-top: 0px;
    padding-left: 0px;
    cursor: pointer;
    position:absolute;
    top:5px;
    display:inline-block;
    filter:invert(1);
    background-image: url('@/assets/founder-space/chat/left-arrow.png');
    background-size: contain;
    background-position: center;
    background-repeat: no-repeat;
    transform: translate(100px, 0);
    transition: all 0.3s ease;
}
.settings-footer{
    display: block;
    position: absolute;
    left: 0;
    bottom: 0px;
    height: 80px;
    width: calc(320px);
    background-color: rgba(27, 27, 27, 0.623);
    transition: all 0.3s ease;
}
.configure-side-bar{
    display: block;
    position: absolute;
    left: 0;
    top: 0;
    padding-top: 0px;
    padding-left: 0px;
    height: calc(100% - 0px);
    font-size: 14px;
    width: 320px;
    box-shadow: 5px 5px 15px 5px #1a1a1a;
    background: #d1d1d100;
    overflow-y: auto;
    overflow-x: hidden;
}
.full-setting-container{
    display: block;
    position:absolute;
    left:0px;
    height: 100%;
    width: calc(100% - 0px);
    background-color: rgba(255, 0, 0, 0);
}
.delete-room-button{
    display: inline-block;
    width:fit-content;
    padding:10px;
    border-radius: 5px;
    margin-top: 20px;
    border: 2px solid rgb(255, 0, 0);
    font-family: fantasy;
    float:left;
    margin-left:-80px;
    transition: all 0.3s ease;
}
.delete-room-button:hover{
    background-color: rgb(255, 0, 0);
    color:white;
    cursor: pointer;
}

.configure-container:hover .chat-icon{
    color: rgb(255, 255, 255);
    transform: translate(0px, 0);
}
.configure-container:hover .configure-text{
    color: rgb(255, 255, 255);
    visibility: visible;
}
.prefacing-header{
    font-family: fantasy;
    color: rgb(0, 0, 0);
    font-size: 28px;
    font-weight: bold;
    text-align: left;
    float:left;
    width:calc(100% - 0px);
    margin-bottom:-0px;
    margin-top: 20px;
    padding: 80px;
    padding-bottom:0;
    margin-left:-80px;
    margin-top:-60px;
    position: relative;
    z-index: 1;
    background-color: rgba(143, 143, 143, 0);
}
.option-action-space-block{
    display: inline-block;
    width:calc(100% - 200px);
    min-width:400px;
    height:auto;
    background-color: rgba(255, 255, 255, 0);
    margin-top: 20px;
    padding-top: 20px;
}
.option-padding{
    display: inline-block;
    width:calc(100% - 200px);
    height:auto;
    background-color: rgba(255, 255, 255, 0);
    margin-top: 20px;
    padding-top: 20px;
}
.option-label{
    display: inline-block;
    font-family: fantasy;
    color: rgb(43, 43, 43);
    font-size: 16px;
    font-weight: bold;
    margin-left: 20px;
    text-align: left;
    float:left;
    width:100px;
    margin-top: 60px;
    background-color: rgba(0, 0, 255, 0);
}
.option-description{
    display: inline-block;
    font-family: fantasy;
    color: rgb(73, 73, 73);
    width: calc(100% - 100px);
    background-color: rgba(0, 0, 255, 0);
    text-align: left;
    font-size: 14px;
    margin-left: 20px;
    margin-top: 20px;
    float:left;
}
.toggle{
    display: inline-block;
    margin-top: 20px;
    margin-left: 20px;
    float:left;
}
.switch {
  position: relative;
  display: inline-block;
  width: 45px;
  height: 15px;
}
.switch input { 
  opacity: 0;
  width: 0;
  height: 0;
}
.slider {
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
  bottom: -2.5px;
  background-color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.473);
  transition: .4s;
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

.setting-display-container{
    display: block;
    right: 0px;
    top: 20px;
    padding: 15px;
    padding-left:40px;
    padding-right:40px;
    padding-bottom:120px;
    height: calc(100% - 0px);
    max-width: 600px;
    background-color: rgba(255, 255, 255, 0);
}
.notification-settings{
    display: block;
    width:400px;
    height:20px;
    background-color: rgb(255, 255, 255);
    margin:auto;
    margin-top: 20px;
}
.configure-container:hover{
    background-color: rgba(255, 255, 255, 0);
    opacity: 1;
}
.configure-container:hover .confiure-icon{
    color: rgb(255, 255, 255);
    transform: translate(0px, 0);
}
.configure-container:hover .configure-text{
    color: rgb(255, 255, 255);
    visibility: visible;
}
.configure-container{
    display: block;
    position: absolute;
    left: 0px;
    top: 20px;
    padding: 15px;
    width: 230px;
    background-color: rgba(255, 0, 0, 0);
    opacity: 0.6;
    transition: all 0.3s ease;
    cursor: pointer;
}
.new-room{
    display: block;
    position: absolute;
    left: 0;
    bottom: 0px;
    height: 80px;
    width: calc(250px);
    background: rgb(0, 0, 0);
    
    box-shadow: 0px 0px 40px rgba(0, 0, 0, 0.89);
    transition: all 0.3s ease;

}
.confiure-icon{
    width: 30px;
    height: 30px;
    background: rgb(255, 255, 255);
    margin-left: -110px;
    margin-top: 0px;
    padding-left: 80px;
    cursor: pointer;
    position:absolute;
    top:5px;
    display:inline-block;
    filter:invert(1);
    background-image: url('@/assets/founder-space/chat/setting.png');
    background-size: contain;
    background-position: center;
    background-repeat: no-repeat;
    transform: translate(-120px, 0);
    transition: all 0.3s ease;
}
.configure-text{
    visibility: hidden;
    font-family: fantasy;
    color: rgb(255, 255, 255);
    padding-bottom:0px;
    width:200px;
    margin-top: -10px;
    background: rgba(0, 0, 255, 0);
    text-align: left;
    display:inline-block;
    overflow:hidden;
    font-weight: bold;
    transition: all 0.3s ease;
}
.Add-Room:hover{
    cursor: pointer;
    color: rgba(194, 194, 194, 0.8);
    
    border: 2px solid rgba(223, 223, 223, 0.8);
}
.Add-Room{
    font-family: fantasy;
    color: rgba(223, 223, 223, 0.404);
    padding-bottom:10px;
    width:196px;
    margin-top:5px;
    padding-left: 10px;
    text-align: left;
    border-radius: 5px;
    padding-top:10px;
    border: 2px solid rgba(44, 44, 44, 0.404);
}

.expanded{
    transform: rotate(90deg);
    transition: all 0.3s ease;
    width: 20px;
    height: 20px;
    background-color: rgba(221, 221, 221, 0);
    box-shadow:  0px 0px 10px rgba(255, 255, 255, 0);
    margin-left: 5px;
    margin-bottom:-5px;
    cursor: pointer;
    display:inline-block;
    transition: transform 0.1s ease;
    transform: translate(-5px, 5px) rotate(90deg);
}
.room-type-label:hover{
    cursor: pointer;
    color: rgba(255, 94, 0, 0.753);
}

.collapse{
    width: 20px;
    height: 20px;
    background-color: rgba(221, 221, 221, 0);
    box-shadow:  0px 0px 10px rgba(255, 255, 255, 0);
    margin-left: 5px;
    margin-bottom:-5px;
    cursor: pointer;
    display:inline-block;
    transition: transform 0.1s ease;
}
.room-type-label{
    font-family: fantasy;
    color: rgba(207, 141, 42, 0.953);
    padding-bottom:0px;
    width:200px;
    background: rgba(0, 0, 255, 0);
    text-align: left;
    display:inline-block;
    margin-left: -30px;
    overflow:hidden;
    font-weight: bold;
}
.unselected-room{
    font-family: fantasy;
    color: rgba(255, 255, 255, 0.774);
    padding-bottom:10px;
    width:200px;
    margin-top:5px;
    padding-left: 10px;
    text-align: left;
    border-radius: 5px;
    padding-top:10px;
    background: linear-gradient(to top, rgba(255, 255, 255, 0.048), rgba(255, 255, 255, 0.041));
}
.unselected-room:hover{
    cursor: pointer;
    background-color: rgba(255, 255, 255, 0.089);
}
.selected-room{
    font-family: fantasy;
    color: rgba(255, 255, 255, 0.774);
    padding-bottom:10px;
    width:200px;
    margin-top:5px;
    padding-left: 10px;
    text-align: left;
    border-radius: 5px;
    padding-top:10px;
    background-color: rgba(167, 100, 0, 0.953);
}
.selected-room:hover{
    cursor: pointer;
    background-color: rgba(187, 112, 0, 0.953);
}
.room-side-bar{
    display: block;
    position: absolute;
    left: 0;
    top: 0;
    padding-top: 20px;
    padding-left: 20px;
    height: calc(100% - 100px);
    font-size: 14px;
    width: 230px;
    background: linear-gradient(to top, rgb(26, 26, 26), rgb(14, 14, 14), rgb(0, 0, 0));
    overflow-y: auto;
    overflow-x: hidden;
}
.full-chat-container{
    display: block;
    position:absolute;
    right:0;
    height: 100%;
    width: calc(100% - 250px);
}
.room-display:hover .change-room-button{
    background-image:url('@/assets/founder-space/chat/open-door.svg');
}
.room-display:hover .room-name-box{
    display: block;
}
.room-name-box{
    display:none;
    position: absolute;
    top:-20px;
    
    right: -15px;
    width: calc(100vw - 250px);
    max-width: 400px;
    min-height: 90px;
    height:auto;
    background-color: rgba(255, 255, 255, 0);
    border-radius: 20px;
    padding-left: 10px;
    padding-right: 10px;
    padding-bottom: 20px;
    margin-top: 15px;
    margin-left: 20px;
}
.room-display{
    width:75px;
    height: 75px;
    display: block;
    background-color: rgb(122, 119, 119);
    position: absolute;
    top:20px;
    right: 50px;
    border-radius: 20px;
    z-index: 100;
}
.change-room-button{
    width: 45px;
    height: 45px;
    padding:15px;
    background-color: rgb(221, 221, 221);
    box-shadow:  0px 0px 10px rgba(255, 255, 255, 0.89);
    border-radius: 20px;
    filter: invert(1);
    background-image:url('@/assets/founder-space/chat/closed-door.svg');
    background-size: 60%;
    background-repeat: no-repeat;
    background-position: center;
    cursor: pointer;
}
.message-content-container{
    padding-left:60px; border-left: 2px solid rgba(255, 255, 255, 0); border-radius: 5px; 
    background: linear-gradient(to right, rgba(255, 255, 255, 0), rgba(255, 255, 255, 0));

}
.division-line{
    display:block;
    width: 100%;
    border: none;
    height:2px;
    margin-bottom: -0px;
    background: rgba(255, 255, 255, 0.329);
}
.division-text{
    display:block;
    font-size: 13px;
    color: rgba(255, 255, 255, 0.582);
    background-color: rgb(12, 12, 12);
    font-weight: bold;
    font-family: fantasy;
    padding-top:10px;
    padding-left:10px;
    padding-right:10px;
    width:100%;
    width: fit-content;
    margin: auto;
    margin-top: -20px;
    text-align: center;

}
.day-divison{
    display: block;
    opacity: .5;
    margin-bottom: 50px;
    margin-top: 10px;


}
.time{
    display: inline-block;
    font-size: 11px;
    color: rgba(235, 235, 235, 0.719);
    margin-top: 10px;
    margin-left: 10px;
    font-family: fantasy;
}
.room-title{
    width:calc(100% - 100px);
    display: block;
    font-size: 16px;
    color: rgb(0, 0, 0);
    font-family: fantasy;
    padding-top: 17px;
    margin-left: 20px;
    text-align: left;
}
.header-of-chat{
    display: block;
    height: 60px;
    width: calc(100%);
    background-color: rgb(10, 10, 10);
    box-shadow: 0px 10px 10px rgba(32, 32, 32, 0.5);
}
.spacing{
    margin-bottom: 100px;
    width: 100%;
}
.message-text{
    display: block;
    margin-top: 5px;
    font-size: 14px;
    color: rgb(206, 206, 206);
    font-family: fantasy;
}
.content-block{
    display: block;
    margin-left: 20px;
    margin-top: -50px;
    background-color: rgba(0, 0, 0, 0);
}
.message{
    display:block;
    align-items: center;
    height: auto;
    padding-bottom: 0px;
    background:#0057b300;
    width: calc(100%);
    padding-top:20px;
    padding-right:100px;
    margin-top:-20px;
    min-height: 0px;
}
.profile-pic{
    width: 45px;
    height: 45px;
    background-color: rgba(255, 255, 255, 0);
    border-radius: 50%;
    margin-left: -45px;
    display: inline-block;
    border: 2px solid rgba(0, 0, 0, 0.712);
}
.content{
    display: block;
    font-size: 14px;
    color: rgb(255, 255, 255);
    margin-top: 20px;
    margin-left:20px;
    font-family: fantasy;

}
.name{
    display: inline-block;
    font-size: 14px;
    font-family: fantasy;
}
.chat-messages{
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    gap: 20px;
    padding: 20px;
    background-color: rgba(0, 0, 0, 0);
}
.message-container{
    overflow-y: auto;
    overflow-x: hidden;
    padding: 10px;
    padding-top:40px;
    height: calc(100% - 130px);
    width:calc(100% - 40px);
    background-color: rgba(49, 49, 49, 0);
    text-align: left;
}
.chat-box{
    display: flex;
    width: calc(100% - 80px);
    margin-left:30px;
}
.send-button-container{
    margin-left: 20px;
    display: inline-block;
    width:fit-content;
    height: 45px;
    padding:10px;
    border-radius: 5px;
    
    margin:-5px;
    
    margin-top: 10px;
    background-color: rgba(255, 80, 27, 0);

}
.send-button-container:hover{
    background: rgba(255, 255, 255, 0.089);
    cursor: pointer;
}
.send-button {
    display: inline-block  !important;  
    width: 47px;
    height: 47px;
    background-color: rgba(0, 174, 255, 0);
    background-image:url('@/assets/founder-space/chat/send.png');
    background-size: contain;
    background-position: center;
    background-repeat: no-repeat;
    filter: invert(1);
    border: 12px solid rgba(0, 174, 255, 0);
    border-radius: 5px;
}
.chat-input {
    display:inline-block;
    background: rgba(61, 61, 61, 0) !important;
    padding: 10px;
    width: 100%;
    height: 30px;
    font-size: 16px;
    font-family: fantasy;
    margin-top: 20px;
    border:none;
    color:white;
    outline: none;
    resize: none;
    border-radius: 4px;
}
.text-bar{
    position: absolute;
    bottom:0px;
    height: 80px;
    width: 100%;
    
    background: rgb(10, 10, 10);
    box-shadow: 0px 0px 40px rgba(0, 0, 0, 0.89);
    margin-top: 20px;
}
.container {
    
    box-shadow: inset 0px 0px 40px rgba(0, 0, 0, 0.89);
    height:calc(100vh - 60px);
    overflow-y: auto;
    
    overflow-x: hidden;
    position: absolute;
    margin-top: 20px;
    left: 0;
    background-color: rgba(255, 255, 255, 0);
    width: calc(100vw - 50px);

    z-index: -2;
    margin-left: 50px;
    text-align: center;
}   
.chat-header {
    background-color: #96343494;
    padding: 10px;
    text-align: center;
}
.chat-messages {
    flex: 1;
    padding: 10px;
    overflow-y: auto;
    background-color: #ffffff;
}
.chat-input {
    display: flex;
    padding: 10px;
    background-color: #f5f5f5;
}
.chat-input input {
    flex: 1;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
}
.chat-input button {
    margin-left: 10px;
    padding: 10px 20px;
    background-color: #ff0000;
    color: #fff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}
.chat-input button:hover {
    background-color: #0056b3;
}
</style>