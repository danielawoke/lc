<script setup>
import dayjs from 'dayjs';
import axios from 'axios';
import { ref, nextTick, watch, onMounted } from 'vue';
import { AccountLocal } from '@/lib/appwrite';
import { createClient } from '@supabase/supabase-js';
import { useRoute, useRouter } from 'vue-router'
import { onUnmounted } from 'vue';

const supabase = createClient(import.meta.env.VITE_SUPABASE_URL, import.meta.env.VITE_SUPABASE_ANON_KEY);
let messages = ref([]);
const router = useRouter()
const route = useRoute()
const apiUrl = import.meta.env.VITE_APP_API_URL;
let selectedRoom = ref([1, 1]);
let channel = null;
let chatInputElement = null;
let chatContainer = null;
let finisihedInitialLoading = false;
let loadingMore = ref(false);
let allLoaded = false;
let loads = ref(0);
let tab = ref("friends");
let userId = null;
let status = ref("loading");
let interval = null;
let chatInput = ref("");
let userData = null;
let newRoom = ref(null);
let profileResponse = ref(null);
let selectedNotification = ref(null);
let delRoomSelected = ref(false);

import bellImage from "@/assets/bell.png";
import bellOffImage from "@/assets/bell-off.png";

let roomCategories = ref([
    // { 
    //     category: "General",
    //     rooms: [
    //         { name: 'Main',  chatroomID: "2" },
    //     ],
    //     collapsed: false

    // },
    // { 
    //     category: "Software Engineer",
    //     rooms: [
    //         { name: 'Cindy', job: 'Software Engineer',  category: 'Candidate' },
    //         { name: 'Alveres', job: 'Product Manager',  category: 'Candidate' },
    //         { name: 'Derrick', job: 'Data Scientist',  category: 'Candidate' },
    //     ],
    //     collapsed: true

    // },
    // { 
    //     category: "Vue specialist",
    //     rooms: [
    //         { name: 'Cindy', job: 'Software Engineer', category: 'Candidate' },
    //         { name: 'Alveres', job: 'Product Manager', category: 'Candidate' },
    //         { name: 'Derrick', job: 'Data Scientist',  category: 'Candidate' },

    //     ],
    //     collapsed: true,

    // },
]);



function mobileModeListener(){
    mobileMode.value = window.innerWidth <= 768;
    console.log("Mobile mode:", mobileMode.value);
}

let mobileMode = ref(true)
mobileMode.value = window.innerWidth <= 768;

onMounted(async() => {
    try {
        let user = await AccountLocal.get();
        userId = user.$id;

        window.addEventListener('resize', mobileModeListener);
        let p_job_id = route.query.job_id;
        let p_chat_room_id = route.query.chat_room_id;
        console.log(p_job_id, p_chat_room_id);
        const userDataResponse = await axios.get(`${apiUrl}users/search/full_profile/${userId}`);
        userData = userDataResponse.data.profile[0];
        if(!userDataResponse.data["profile"]){
            router.push("/login");
        } else {
            await loadRooms();
            if(p_job_id && p_chat_room_id){
                let found = false;
                for(let i = 0; i < roomCategories.value.length; i++){
                    if(roomCategories.value[i].job_id == p_job_id){
                        for(let j = 0; j < roomCategories.value[i].rooms.length; j++){
                            console.log(roomCategories.value[i].rooms[j].chatroomID, p_chat_room_id);
                            if(roomCategories.value[i].rooms[j].chatroomID == p_chat_room_id){
                                await selectRoom(i, j);
                                found = true;
                                break;
                            }
                        }
                    }
                    if(found) break;
                }
            }else{
                await selectRoom(0, 0);
            }
        }
    } catch (err) {
        console.log("Error fetching user data:", err);
        // router.push("/login");
    }
});

onUnmounted(async () => {
    if(interval){
        clearInterval(interval);
    }
    if(channel){
        supabase.removeChannel(channel);
    }
    await axios.post(`${apiUrl}users/message_notifications/enable_notifications/${userId}`).catch((err) => {
        console.error("Error leaving chat room:", err);
    });
});

async function loadRooms(){

    try {
        let response = await axios.get(`${apiUrl}projects/discussions/load_rooms/${route.params.projectId}`);
        let roomsData = response.data;
        let rooms = [];

        let genRooms = {
            rooms:[],
            category: "Genearl",
            collapsed: false,
        }
        for (let room of roomsData.Genearl){
            genRooms.rooms.push({ name: room.name, chatroomID: room.chat_id });
        }
        rooms.push(genRooms);
        console.log(roomsData.Discussions);
        for (let JobDiscussion of roomsData.Discussions){
            let discussionCategory = {
                category: JobDiscussion.Job,
                rooms: [],
                collapsed: true,
                job_id: JobDiscussion.job_id,
            };
            for (let room of JobDiscussion.Candidates){
                console.log(room);
                discussionCategory.rooms.push({
                    name: room.name,
                    chatroomID: room.chat_id,
                    usertag: room.usertag,
                });
            }
            rooms.push(discussionCategory);
        }
        

        roomCategories.value = rooms;
    } catch (err) {
        console.error("Error loading rooms:", err);
    }

}

 
async function scrollMore(){
    if (chatContainer.scrollTop === 0) {
        await loadMore();
    }
} 

async function sendEnter(e){
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        send(chatInput.value);
    }
}

async function selectRoom(categoryId, roomId) {
    selectedRoom.value = [categoryId, roomId];
    selectedNotification.value = roomCategories.value[categoryId].rooms[roomId].chatroomID;
    await loadChatroom(selectedNotification.value);
    roomSelectionMenu.value = false;
}

async function loadChatroom(chat_room_id){

    loadingMore.value = false;
    allLoaded = false;

    if(chatInputElement){
        chatInputElement.removeEventListener('keypress', sendEnter);
    }
    if(chatContainer){
        chatContainer.removeEventListener('scroll', scrollMore);
        chatContainer.removeEventListener('resize', ensureScrollable);
    }
    await axios.post(`${apiUrl}users/message_notifications/in_chat_room/${userId}/${chat_room_id}`);
    try {
        if(channel){
            await supabase.removeChannel(channel);
        }
        messages.value = [];
        let response = await axios.get(`${apiUrl}messages/load/${chat_room_id}/none`);
        messages.value.push(...response.data);
        channel = await supabase
                        .channel('messages')
                        .on(
                            'postgres_changes',
                            {
                            event: 'INSERT',
                            schema: 'public',
                            table: 'messages',
                            filter: `chat_room_id=eq.${chat_room_id}`
                            },
                            (payload) => {
                                console.log("New message received:", payload);
                                messages.value.push({
                                    content: payload.new.content,
                                    time: payload.new.time,
                                    name: payload.new.name,
                                    image_url: payload.new.image_url,
                                });
                                if(finisihedInitialLoading && chatContainer.scrollTop + chatContainer.clientHeight >= chatContainer.scrollHeight - 100){
                                    chatContainer.scrollTop = chatContainer.scrollHeight;
                                }
                            }
                        ).subscribe();

            await axios.get(`${apiUrl}users/message_notifications/is_notifications_enabled/${userId}/${chat_room_id}`).then(response => {
                notificationsOn.value = response.data.status;
            }).catch(err => {
                console.error("Error fetching notification status:", err);
            });
    } catch (err) {
        console.error("Error loading chatroom:", err);
    }

    chatInputElement = document.getElementById("chat-input");
    chatContainer = document.querySelector(".message-container");
    chatInputElement.addEventListener('keypress', sendEnter);
    chatContainer.addEventListener('scroll', scrollMore);
    chatContainer.addEventListener('resize', ensureScrollable);

    await ensureScrollable();
    finisihedInitialLoading = true;

}


async function ensureScrollable() {
    const container = chatContainer;

    while (container.scrollHeight <= container.clientHeight) {
        const hasMore = await loadMore();
        if (!hasMore) break;

        await nextTick();
    }

    container.scrollTop = container.scrollHeight;
    
}

async function loadMore(){
    if(allLoaded){
        console.log("All messages loaded");
        loadingMore.value = false;
        return false;
    }
    loadingMore.value = true;
    chatContainer.scrollTop = 0;
    if(messages.value.length > 0 && finisihedInitialLoading){
        let lastMessageTime = messages.value[0].time;
        try {
            let response = await axios.get(`${apiUrl}messages/load/${selectedNotification.value}/${lastMessageTime}`);
            const container = chatContainer;
            const previousScrollHeight = container.scrollHeight;
            messages.value.unshift(...response.data);
            await nextTick();
            const newScrollHeight = container.scrollHeight;
            container.scrollTop += (newScrollHeight - previousScrollHeight);
            if(response.data.length === 0) {
                allLoaded = true;
            }
            
            loadingMore.value = false;
            return response.data.length > 0;
        } catch (err) {
            console.error("ADSADSADASDSA:", err);
            allLoaded = true;
            loadingMore = false;
            return false;
        }
    }
    loadingMore.value = false;
    return false;
}

async function createNewRoom() {
    axios.post(`${apiUrl}projects/discussions/create_general_room/${route.params.projectId}`)
    .then(async response => {
        console.log("New room created:", response.data);
        roomCategories.value[0].rooms.push(response.data.object);
        await selectRoom(0, roomCategories.value[0].rooms.length-1);
    }).catch(err => {
        console.error("Error creating new room:", err);
    });
}

function collapse(category){
    category.collapsed = !category.collapsed;
}

async function send(message_input){
    let message = message_input.trim();
    
    if (message !== "" && selectedNotification.value) {
        try {
            let fromNewRoom = false;
            if(selectedNotification.value === -1){
                fromNewRoom = true;
                let reciever_relation = await axios.get(`${apiUrl}users/search/is_friends/${profileResponse.value.data.profile[0].user_id}/${userId}`);
                let response = await axios.post(`${apiUrl}messages/create_room`, {
                    type: "personal",
                    users: [userData, profileResponse.value.data.profile[0]],
                    relation: [tab.value === "friends" ? "friends" : "unknown", reciever_relation.data.is_friends ? "friends" : "unknown"],
                });
                selectedNotification.value = response.data.chat_room_id;
                newRoom.value = false;
            }
            console.log("Sending message:", {
                chat_room_id: selectedNotification.value,
                sender_id: userId,
                content: message,
                sender_name: userData.profile_data.display_name,
                sender_image: userData.profile_data.UserImage,
            });
            console.log(userData);
            console.log(roomCategories.value[selectedRoom.value[0]].rooms[selectedRoom.value[1]])
            await axios.post(`${apiUrl}messages/send`, {
                chat_room_id: selectedNotification.value,
                sender_id: userId,
                content: message,
                sender_name: userData.profile_data.display_name,
                sender_image: userData.profile_data.UserImage,
                project_id: route.params.projectId,
                job_id: roomCategories.value[selectedRoom.value[0]].job_id ? roomCategories.value[selectedRoom.value[0]].job_id : "none",
                candidate_usertag: roomCategories.value[selectedRoom.value[0]].rooms[selectedRoom.value[1]].usertag,
                candidate_name: roomCategories.value[selectedRoom.value[0]].rooms[selectedRoom.value[1]].name,
            });
            chatInput.value = "";
            if(fromNewRoom){
                await loadChatroom(selectedNotification.value);
                await loadRooms();
            }
        } catch (err) {
            console.error("Error sending message:", err);
        }
    }
}

let mode = ref('chat');
let configureMode = ref('Room Settings');

let currentImage = ref('@/assets/founder-space/chat/closed-door.svg');

let roomSelectionMenu=ref(false);

let notificationsOn = ref(false);

async function toggleNotif(){
    await axios.post(`${apiUrl}users/message_notifications/enable_project_notifications/${userId}/${selectedNotification.value}`).then(response => {
        notificationsOn.value = !notificationsOn.value;
    }).catch(err => {
        console.error("Error toggling notifications:", err);
    });
    
}

let popupActive = ref(false);
let currRoomName = ref("");

function openSettings(){
    delRoomSelected.value = false;
    currRoomName.value = roomCategories.value[selectedRoom.value[0]].rooms[selectedRoom.value[1]].name;
    popupActive.value = true;
}

function deleteToggle(){
    delRoomSelected.value = !delRoomSelected.value;
}

async function confirmDeletion(){
    if(document.getElementById("deleteText").value != roomCategories.value[selectedRoom.value[0]].rooms[selectedRoom.value[1]].name){
        document.getElementById("deleteText").value = "";
        document.getElementById("deleteText").placeholder = "Name doesnt match, try again";
        return;
    }
    await axios.post(`${apiUrl}projects/discussions/delete_room/${route.params.projectId}`, {
        chatroomID: selectedNotification.value,
        jobID: "none",
    }).then(response => {
        console.log("Room deleted:", response.data);
        messages.value = [];
        roomCategories.value[selectedRoom.value[0]].rooms.splice(selectedRoom.value[1], 1);
        selectedNotification.value = null;
    }).catch(err => {
        console.error("Error deleting room:", err);
    });
    popupActive.value = false;
}

async function changeRoomName(){
    await axios.post(`${apiUrl}projects/discussions/edit_room_name/${route.params.projectId}`, {
        chatroomID: selectedNotification.value,
        newName: currRoomName.value,
    }).then(response => {
        console.log("Room name changed:", response.data);
        roomCategories.value[selectedRoom.value[0]].rooms[selectedRoom.value[1]].name = currRoomName.value;
    }).catch(err => {
        console.error("Error changing room name:", err);
    });
    popupActive.value = false;
}



</script>

<template>
    <div v-if="popupActive" @click.self="popupActive=false" class="popup-backdrop">
        <div class="changeRoomNamePopup">
            <div v-if="!delRoomSelected" class="popupContent">
                <div class="room-edit-header">Room Settings</div>
                <div style="margin-bottom:20px; font-family:Arial, Helvetica, sans-serif; color:rgb(255, 255, 255);">Room Name</div>
                <input class="room-edit-input" v-model="currRoomName" />
                <button class="room-edit-delete" @click="deleteToggle" >Delete Room</button>
                <button class="room-edit-sumbit" @click="changeRoomName">Save</button>
            </div>
            <div v-else class="popupContent">
                <div class="room-edit-header">Room Settings</div>
                <div style="margin-bottom:20px; font-family:Arial, Helvetica, sans-serif; color:rgb(255, 255, 255);">Retype the name of the room to confirm deletion</div>

                <input class="room-edit-input" id="deleteText" :placeholder="roomCategories[selectedRoom[0]].rooms[selectedRoom[1]].name"/>
                <button class="room-edit-delete" style="float:right;" @click="confirmDeletion">Confirm Deletion</button>
            </div>
        </div>
    </div>

    <div class="container" :style="{width: mobileMode ? 'calc(100vw)' : 'calc(100vw - 50px)', marginLeft: mobileMode? '0px': '50px'}">
        <div v-if="roomSelectionMenu" class="left-bar">
            <div v-for="(category, index) in roomCategories" class="room-category">
                <div class="left-bar-text" @click="collapse(category)">
                    <span>{{ category.category }}</span>
                    <span :class="category.collapsed ? 'toggle-room-collapse-unopened' : 'toggle-room-collapse-opened'">></span>
                </div>
                <div v-if="!category.collapsed">
                    <div v-for="(room, roomIndex) in category.rooms" class="room-display" :class="{ active: selectedRoom[0] === index && selectedRoom[1] === roomIndex }" @click="selectRoom(index, roomIndex)">
                        <div>{{ room.name }}</div>
                    </div>
                    <div v-if="index === 0" class="room-display" style="background:white; color:black;" @click="createNewRoom()">+ Create New Room</div>
                </div>
            </div>
        </div>
        <div class="notification-display" :style="selectedNotification==null? 'filter:brightness(.8)' : ''">
            <div class="chat-header">
                <div style="font-size:20px; text-align: left; font-family:Arial, Helvetica, sans-serif;">
                    <img class="settings" src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Hamburger_icon.svg/1280px-Hamburger_icon.svg.png" @click="roomSelectionMenu=!roomSelectionMenu"/>
                    <span style="position:relative; top:-17px">{{ selectedRoom ? roomCategories[selectedRoom[0]]?.rooms[selectedRoom[1]]?.name : '' }}</span>
                </div>
            </div>
            <div class="notif">
                <span @click="openSettings" class="delete" v-if="selectedRoom[0]===0 && selectedRoom[1]>0"></span>
                <span class="notification_image" @click="toggleNotif" :style="notificationsOn ? { backgroundImage: `url(${bellImage})` } : { backgroundImage: `url(${bellOffImage})` }"></span>
            </div>
            <img  src="@/assets/user-creation/private-message-wait-screen.png" class="wait-screen" :style="selectedNotification==null? 'display:block' : 'display:none'"/>
            <div class="full-chat-container">
                <div class="message-container">
                    <div v-if="loadingMore" style="font-size: 20px; font-weight: bold; font-family:Arial, Helvetica, sans-serif; opacity:.6; padding:20px; margin:20px; margin-top:50px;">Loading messages...</div>
                    <div style="height:20px;"></div>
                    <!-- Im thinking make a global var for the day, and when it passes, in the messages you add a day division, or passes 24 hours -->
                    <div v-for="message in messages" class='message' >
                        <div style="padding-bottom:20px;"  v-if="message.user_id != '-1'">
                            <div class="message-content-container">
                                <div>
                                    <img class="profile-pic" :src="message.image_url"></img>
                                </div>
                                <div class="content-block">
                                    <b class="name">{{ message.name }} </b>
                                    <div class="time">{{ dayjs(message.time).format('MM/DD/YYYY hh:mm A') }}</div>
                                    <div class="message-text">{{ message.content }}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="spacing"></div>
                </div>
                <div class="text-bar">
                    <div class="chat-box">
                        <textarea id="chat-input" placeholder="write your message here..." class="chat-input" v-model="chatInput"></textarea>
                        <div @click="send(chatInput)" class="send-button-container">
                            <button class="send-button"></button>
                        </div>
                    </div>
                </div>
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
    color:white;
    filter: brightness(1);
    transition: all ease 0.3s;
    
}
.room-edit-delete{
    background-color: transparent;
    color: rgb(255, 255, 255);
    font-family: Arial, Helvetica, sans-serif;
    font-size: 14px;
    border: 1px solid rgb(255, 255, 255);
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
    color:white;
    margin-bottom: 20px;
    border-radius: 5px;
    font-size: 16px;
}
.room-edit-header{
    font-family: Arial, Helvetica, sans-serif;
    font-size: 20px;
    color: rgb(255, 255, 255);
    text-align: center;
    margin-bottom: 20px;
}
.popup-backdrop{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.6);
    display: flex;
    justify-content: center;
    align-items: center;
}
.changeRoomNamePopup{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: linear-gradient(to bottom, rgb(36, 36, 36), rgb(12, 12, 12));
    padding: 20px;
    width: 100%;
    max-width: 400px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    z-index: 100;
}
.edit{
    width: 38px;
    height: 38px;
    background-image: url("@/assets/founder-space/edit/edit-icon.png");
    background-size: cover;
    color: rgb(0, 0, 0);
    font-family: Arial, Helvetica, sans-serif;
    font-size: 12px;
    top:10px;
    float: right;
    border-radius: 5px;
    margin-top: 0px;
    margin-right:10px;
    overflow:hidden;
}
.delete{
    width: 28px;
    height: 28px;
    background-image: url("@/assets/profile-page/gear.png");
    background-size: cover;
    color: rgb(0, 0, 0);
    font-family: Arial, Helvetica, sans-serif;
    font-size: 12px;
    top:10px;
    filter:invert(1);
    float: right;
    border-radius: 5px;
    margin-top: 5px;
    margin-left:15px;
    overflow:hidden;
}
.delete:hover{
    filter: brightness(.5) invert(.8);
    transition: ease 0.3s all;
    transform: scale(1.05) rotate(180deg);
    cursor: pointer;
}
.notification_image:hover{
    filter: brightness(.5) invert(.8);
    transition: ease 0.3s all;
    transform: scale(1.05);
    cursor: pointer;
}
.edit:hover{
    filter: brightness(.8) saturate(3);
    transition: ease 0.3s all;
    transform: scale(1.05);
    cursor: pointer;
}
.notification_image{
    width: 30px;
    height: 30px;
    filter:invert(1);
    background-size: cover;
    color: rgb(0, 0, 0);
    font-family: Arial, Helvetica, sans-serif;
    font-size: 12px;
    float:right;
    margin-top: 5px;
    margin-right:10px;
    border-radius: 5px;
}
.notif{
    background-color: rgb(29, 29, 29);
    width:100%;
    height:40px;
    padding-left:40px;
    padding-right:40px;
    margin-left:-40px;
}
.toggle-room-collapse-opened{
    float: right;
    margin-right: 20px;
    transition: transform 0.3s ease;
    padding-left:7px;
    padding-right:5px;
    padding-top:1.5px;
    padding-bottom:1.5px;
    color:rgb(255, 255, 255);
    transform: rotate(90deg)
    
}
.left-bar-text:hover .toggle-room-collapse-opened{
    color:rgb(255, 255, 255, .5);
    cursor: pointer;
    
}
.left-bar-text:hover{
    color:rgb(255, 255, 255, .5);
    cursor: pointer;
}
.left-bar-text:hover .toggle-room-collapse-unopened{
    color:rgb(255, 255, 255, .5);
    cursor: pointer;
    transform: rotate(90deg);
}
.toggle-room-collapse-unopened{
    float: right;
    margin-right: 20px;
    transition: transform 0.3s ease;
    padding-left:7px;
    padding-right:5px;
    padding-top:1.5px;
    padding-bottom:1.5px;
    color:rgb(255, 255, 255);
    
}
.room-display{
    font-family: Arial, Helvetica, sans-serif;
    font-size: 14px;
    color: rgb(255, 255, 255);
    padding: 10px;
    background-color: rgba(0, 0, 0, 0.8);
    border: 1px solid rgba(255, 255, 255, 0.692);
    margin: 10px;
    border-radius: 5px;
    cursor: pointer;
}
.room-display:hover{
    filter: brightness(.8);
}
.room-category{
    text-align: left;

}
.chat-header{
    height: 40px;
    width: calc(100%);
    padding-left: 40px;
    padding-right: 40px;
    padding-top:20px;
    margin-left: -40px;
    font-size:25px;
    color:white;
    background: linear-gradient(to bottom, black, rgb(46, 46, 46));
}
.container {
    box-shadow: inset 0px 0px 40px rgba(0, 0, 0, 0.89);
    height:calc(100vh - 60px);
    overflow: auto;
    position: absolute;
    margin-top: 20px;
    left:0;
    background-color: rgb(255, 255, 255);
    width: calc(100vw - 55px);
    z-index: -2;
    text-align: center;
    filter:invert(0);
}  
.wait-screen{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -60%);
    max-width: 700px;
    width:100%;
    aspect-ratio: 1 / 1;
    opacity: .5;
    
    
}
.menu{
    height:calc(100% - 50px);
    width:97%;
    background: linear-gradient(to left, rgb(29, 29, 29), rgb(26, 26, 26));
    position: absolute;
    top:50px;
    left:0;
    animation: slideIn 0.4s cubic-bezier(0.25, 1.0, 0.1, 1.0) ;
}


@keyframes slideIn {
    from {
        transform: translateX(-100%);
    }
    to {
        transform: translateX(0);
    }
}

.left-bar-text{
    font-family: Arial, Helvetica, sans-serif;
    font-size: 16px;
    color: rgb(255, 255, 255);
    text-align: left;
    padding-top:10px;
    padding:10px;
    font-weight: bold;


}
.active{
    background-color: rgba(0, 255, 255, 0.8);
    border: black 1px solid;
}
.active:hover{
    filter:brightness(.8);
    border: black 1px solid;
}
.interview-button{
    width: fit-content;
    padding: 5px;
    background-color: rgb(255, 255, 255);
    color: rgb(0, 0, 0);
    font-family: Arial, Helvetica, sans-serif;
    font-size: 12px;
    position: absolute;
    bottom:10px;
    left:70px;
    border-radius: 5px;
    overflow:hidden;
}
.unknown-button{
    width: fit-content;
    padding: 5px;
    background-color: rgb(255, 255, 255);
    color: rgb(0, 0, 0);
    font-family: Arial, Helvetica, sans-serif;
    font-size: 12px;
    position: absolute;
    bottom:10px;
    left:140px;
    border-radius: 5px;
    overflow:hidden;
}
.friends-button{
    width: fit-content;
    padding: 5px;
    background-color: rgb(255, 255, 255);
    color: rgb(0, 0, 0);
    font-family: Arial, Helvetica, sans-serif;
    font-size: 12px;
    position: absolute;
    bottom:10px;
    left:15px;
    border-radius: 5px;
    overflow:hidden;
}
.priv-title{
    font-family: Arial, Helvetica, sans-serif;
    font-size: 16px;
    color: rgb(255, 255, 255);
    padding: 15px;
    margin-left:40px;
}
.messages-dropdown{
    position: absolute;
    top: 60px;
    right: 0px;
    width: 300px;
    height: 400px;
    background-color: rgb(255, 255, 255);
    box-shadow: inset 0px 0px 20px rgba(0, 0, 0, 0.5);
    z-index: 10;
    border-radius: 0 0 0 10px;
    border: 2px solid rgb(0, 0, 0);
}
.message-content-container{
    padding-left:60px; border-left: 2px solid rgba(255, 255, 255, 0); border-radius: 5px; 
    background: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0));

}
.full-chat-container{
    display: block;
    position:absolute;
    right:0;
    height: calc(100% - 100px);
    width: calc(100%);
}
.notification-display{
    position: absolute;
    top: 0px;
    left: 0px;
    width: calc(100% - 80px);
    height: calc(100% - 40px);
    background: radial-gradient(circle, rgba(255, 208, 108, 0.9), rgba(255, 56, 56, 0.7));
    box-shadow: inset 0px 0px 100px rgba(0, 0, 0, 0.5);
    padding: 40px;
    padding-top: 0px;
    z-index: 0;
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
    width: 55px;
    height: 55px;
    background-color: rgba(255, 255, 255, 0);
    border-radius: 50%;
    margin-left: -45px;
    margin-bottom:-15px;
    display: inline-block;
    border: 2px solid rgba(0, 0, 0, 0.712);
}
.content{
    display: block;
    font-size: 14px;
    color: rgb(255, 255, 255);
    margin-top: 20px;
    margin-left:20px;
    font-family: Arial, Helvetica, sans-serif;

}
.name{
    display: inline-block;
    font-size: 14px;
    font-family: Arial, Helvetica, sans-serif;
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
    padding-top:0px;
    height: calc(100% - 10px);
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
.send-button-container:active{
    background: rgba(255, 255, 255, 0.189);
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
    width: calc(100% - 40px);
    height: 30px;
    font-size: 16px;
    font-family: Arial, Helvetica, sans-serif;
    margin-top: 20px;
    margin-right:20px;
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
.time{
    display: inline-block;
    font-size: 11px;
    color: rgba(46, 46, 46, 0.884);
    margin-top: 10px;
    margin-left: 10px;
    font-family: Arial, Helvetica, sans-serif;
}
.room-title{
    width:calc(100% - 100px);
    display: block;
    font-size: 16px;
    color: rgb(255, 255, 255);
    font-family: Arial, Helvetica, sans-serif;
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
    margin-bottom: 150px;
    width: 100%;
}
.message-text{
    display: block;
    margin-top: 5px;
    font-size: 14px;
    color: rgb(0, 0, 0);
    font-family: Arial, Helvetica, sans-serif;
}
.content-block{
    display: block;
    margin-left: 20px;
    margin-top: -50px;
    background-color: rgba(221, 0, 0, 0.253);
    border-radius: 10px;
    padding: 10px;
    white-space-collapse: break-spaces;
    width:fit-content;
}
.division-line{
    display:block;
    width: 100%;
    border: none;
    height:2px;
    margin-bottom: -0px;
    background: rgba(255, 255, 255, 0);
}
.division-text{
    display:block;
    font-size: 13px;
    color: rgb(0, 0, 0,.582);
    font-weight: bold;
    font-family: Arial, Helvetica, sans-serif;
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
.group-chat-image{
    width: 30px;
    height: 30px;
    background-color: rgba(0, 0, 0, 0);
    background-position: center;
    background-size: cover;
    border-radius: 50%;
    display:inline-block;
    margin-bottom:-10px;
    border: 2px solid rgba(0, 0, 0, 0.712);
}
.note-name{
    display:inline-block;
    font-size: 14px;
    height:30px;
    width: calc(100% - 50px);
    position: relative;
    background:rgba(255, 0, 0, 0);
    top:-5px;
    left: 5px;
    margin-bottom:-20px;
    font-family: Arial, Helvetica, sans-serif;
}
.settings{
    width: 30px;
    height: 30px;
    background-size: 80% 80%;
    background-position: center;
    background-repeat: no-repeat;
    color: rgb(0, 0, 0);
    font-family: Arial, Helvetica, sans-serif;
    font-size: 12px;
    position: relative;
    left:-10px;
    top: -10px;
    filter: saturate(0) invert(1) brightness(200%);
    border-radius: 5px;
    overflow:hidden;
}
.seperator{
    position: absolute;
    top:11px;
    filter:invert(1);
    left:41px;
    transform: scaleY(1.5);
    border-radius: 5px;
    overflow:hidden;
}
.body-title{
    font-family: Arial, Helvetica, sans-serif;
    font-size: 20px;
    margin-bottom: 10px;
}
.body-time{
    font-family: Arial, Helvetica, sans-serif;
    font-size: 16px;
    color: rgb(161, 161, 161);
    margin-bottom: 20px;
    text-align: center;
}
.body-time:hover{
    color: rgb(161, 161, 161, .5);
    cursor: pointer;
}
.body-time:active{
    color: rgb(161, 161, 161, .8);
}
.body-content{
    font-family: Arial, Helvetica, sans-serif;
    font-size: 14px;
}
.notification-card-read{
    width: 90%;
    height: 60px;
    margin:auto;
    background-color: rgb(155, 155, 155);
    box-shadow: inset 0px 0px 10px rgba(0, 0, 0, 0.5);
    padding: 10px;
    border-bottom: black solid 1px;
    box-sizing: border-box;
    cursor: pointer;
    opacity: 0.6;
}
.note-date{
    font-family: Arial, Helvetica, sans-serif;
    font-size: 10px;
    position: relative;
    top:15px;
}
.note-content{
    font-family: Arial, Helvetica, sans-serif;
    font-size: 12px;
    position: relative;
    top:10px;
    margin-left:0px;
}
.note-title{
    font-family: Arial, Helvetica, sans-serif;
    font-size: 13px;
    position: relative;
    top:5px;
}
.checkbox{
    display:inline-block;
    width:25px;
    border-radius: 5px;
    height:25px;
    margin-right: 10px;
    margin-bottom: -10px;
    background-color: rgb(255, 255, 255);
    box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.521);
}
.checked{
    width:100%;
    font-size: 20px;
    font-family: Arial, Helvetica, sans-serif;
    height:100%;
    background-color: rgb(1, 183, 255);
    position: absolute;
    top: 0px;
    color:white;
    padding-left:5px;
    padding-right:5px;
    margin-top: -1px;
    padding-bottom:2px;
    left: 0px;
}
.all{
    width: 25px;
    height: 25px;
    background-color: rgb(2, 2, 2);
    color: rgb(0, 0, 0);
    font-family: Arial, Helvetica, sans-serif;
    font-size: 12px;
    position: absolute;
    top:10px;
    left:10px;
    border-radius: 5px;
    overflow:hidden;
}
.tool-bar{
    position:relative;
    height: 50px;
    width: 100%;
    background: linear-gradient(to top, rgb(0, 0, 0), rgb(17, 17, 17));
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
}

.left-bar{
    position: absolute;
    width: calc(100%);
    max-width: 500px;
    left: 0px;
    top:60px;
    height: calc(100% - 60px);
    z-index: 10;
    box-sizing: border-box;
    background: linear-gradient(to top, rgb(17, 17, 17), rgb(12, 12, 12)); 
    position:relative;
    z-index: 10;
    text-align: left;
    animation:cubic-bezier(0, 0, 0, 1) slideIn 0.4s;
}
.notification-card{
    width: calc(100% - 10px);
    height: 90px;
    margin:auto;
    padding: 10px;
    box-sizing: border-box;
    cursor: pointer;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.253);
    border-radius: 20px;
    margin-top:10px;
}
.selected{
    width: calc(100% - 10px);
    height: 90px;
    margin:auto;
    background-color: rgb(0, 183, 255);
    padding: 10px;
    color:white;
    margin-top:10px;
    cursor: pointer;    border-radius: 20px;
}
.middle{
    position: absolute;
    top: 60px;
    left: 0;
    width:100vw;
    height:calc(100vh - 60px);
    background:rgba(0, 0, 255, 0.315);
    overflow:hidden;
}
.Base {
  display: block;
  position: absolute;
  top: 0;
  left: 0;
  width: calc(100vw);
  margin: auto;
  height: 60px;
  background-color: rgb(0, 0, 0);
  /*background-image: linear-gradient(45deg, rgb(143, 219, 249), rgb(0, 183, 255)); */
  box-shadow: 5px 5px 15px 5px #272727;

}

.nav-item {
  display: inline-block;
  height: 25px;
  font-size: 14px;
  /* border-left: 2px solid rgb(0, 0, 0); */
  padding-right: 25px;
  padding-left: 25px;
  font-family: Arial, Helvetica, sans-serif;
  color: rgb(0, 0, 0);
}

.end-element {
  /*border-right: 2px solid rgb(0, 0, 0);*/
}
.start-element {
  margin-left: 150px;
}
.logo {
  display: inline-block;
  width: 40px;
  height: 40px;
  margin-top: -15px;
  margin-left:10px;
  /* whatever the dominant color of what is on the inside, should match the color of this */
  border-radius: 50%;
  border: 2px solid rgb(109, 69, 27);
  background-color: rgb(247, 193, 118);
  background-image: linear-gradient(45deg, rgb(255, 109, 31), rgb(255, 221, 165));
}
.title{
  position:absolute;
  display: inline-block;
  font-family: Arial, Helvetica, sans-serif;
  font-size: 20px;
  color: rgb(232, 232, 232);
  margin-left: 15px;
  margin-top: -5px;
}

.right-portion{
  display: inline-block;
  margin-left: auto;
}

.right-portion-element {
  width: 40px;
  height: 40px;
  border-radius: 50px;
  margin-top: -15px;
  cursor: pointer;
  margin-right: 25px;
  filter:invert(1);
  border: 2px solid rgb(0, 0, 0);
  
}

.prof-header{
    background: linear-gradient(to bottom, rgb(0, 0, 0), rgb(0, 0, 0));
    padding:10px;
    height: fit-content;
}
.prof-icon{
    font-size:17px;
    font-family: Arial, Helvetica, sans-serif;
    padding:0px 0px;
    position: relative;
    border-radius:5px;
    color:white;
    margin:0px;
    margin-right:15px;
    margin-top:-2.5px;
}
</style>