<script setup>
import { useRoute, useRouter } from 'vue-router'
import { ref, nextTick, watch, onMounted, onUnmounted } from 'vue';
import Header from '@/components/header.vue';
import {AccountLocal} from '@/lib/appwrite';
import axios from 'axios';
import dayjs from 'dayjs';
import {supabase} from '@/lib/supabase';
const apiUrl = import.meta.env.VITE_APP_API_URL;
const router = useRouter()
const route = useRoute()


let selectedNotification = ref(1);
let selectAll = ref(false);

let messages = ref(null);
let messageNotifications = ref([]);
let messageRate = 1000;

function toggleSelectAll() {
    selectAll.value = !selectAll.value;
    notifications.value.forEach(notification => {
        notification.checked = selectAll.value;
    });
}

function shortened(content) {
    if(content.length > 40){
        return content.substring(0, 40) + "...";
    }
    return content;
}

async function acceptOffer(proposalId){
    await axios.post(`${apiUrl}users/claim_membership/${proposalId}`, {"type": "offer"}).then(async (response) => {
        console.log("Offer accepted:", response.data);
        await axios.get(`${apiUrl}users/search/full_profile/${userId}`).then((response) => {
            console.log(response.data.profile[0])
            let tag = response.data.profile[0].user_tag;
            router.push(`/user-projects/${tag}`);
        });
    }).catch((err) => {
        if(err.response.status == 400){
            errorText.value = 'Only premimum members can be a part of more than one project at a time. To create this project. Please sign up for a premimum account, or leave the project you are currently in';
        }
        console.error("Error accepting offer:", err);
    });
}

async function acceptInvite(projectId){
    await axios.post(`${apiUrl}users/claim_membership/${projectId}`,{ "user_id": userId, "type": "invite"}).then(async (response) => {
        console.log("Joined project:", response.data);
        await axios.get(`${apiUrl}users/search/full_profile/${userId}`).then((response) => {
            console.log(response.data.profile[0])
            let tag = response.data.profile[0].user_tag;
            router.push(`/user-projects/${tag}`);
        });
    }).catch((err) => {
        console.error("Error joining project:", err);
    });
}


let loads = ref(0);
let tab = ref("friends");
let userId = null;
let status = ref("loading");
let interval = null;
let chatInput = ref("");
let userData = null;
let newRoom = ref(null);
let profileResponse = ref(null);
let notificationChannel = null;
let leftBarToggle = ref(false);
let toolBarSubsituteToggle = ref(false);
let notifications = ref([]);

// Member ship offer notifcation
// {
//     id: -1,
//     title: "Project Name: Membership Offer",
//     text_summary: "Congrats! You've been offered the Any position at Project Name. Click the button to accept the offer.",
//     HTML: `
        // <div style='color:white; font-family: Arial, Helvetica, sans-serif; font-size: 14px; margin:auto; width:fit-content; padding:20px; background-color: rgb(63, 63, 63); border-radius: 10px;'>
        //     <div>Congrats! You've been offered the <b>Any</b> position at <b>Project Name</b>.</div>
        //     <button style="margin:auto; margin-top:20px; padding:10px; background-color: rgb(0, 183, 255); border:none; border-radius:5px; color:white; cursor:pointer; display:block;"
        //             id="accept-offer-button" proposal_id="123">
        //         Accept Offer
        //     </button>
        // </div>
//     `,
//     time: "no-time",
//     read: true,
//     relation: "friends"
// }

// Member ship invite notifcation
// {
//     id: -1,
//     title: "Project Name: Membership Invite",
//     text_summary: "Congrats! You've been invited to join Project Name. Click the button to accept the invite.",
//     HTML: `
        // <div style='color:white; font-family: Arial, Helvetica, sans-serif; font-size: 14px; margin:auto; width:fit-content; padding:20px; background-color: rgb(63, 63, 63); border-radius: 10px;'>
        //     <div>Congrats! You've been invited to join <b>Project Name</b>.</div>
        //     <button style="margin:auto; margin-top:20px; padding:10px; background-color: rgb(0, 183, 255); border:none; border-radius:5px; color:white; cursor:pointer; display:block;"
        //             id="accept-offer-button" proposal_id="123">
        //         Accept Invite
        //     </button>
        // </div>
//     `,
//     time: "no-time",
//     read: true,
//     relation: "friends"
// }

onMounted(async () => {
    try{

        let user = await AccountLocal.get();
        userId = user.$id;

        await axios.get(`${apiUrl}users/notifications/load_notifications/${userId}`).then((response) => {
            response.data.data.forEach(notification => {
                notifications.value.push(notification);
            });
        });

        for (let notification of notifications.value) {
            notification.checked = false;
        }

        let routeNotificationId = route.query.notification_id;

        channel = supabase.channel('notifications')
                        .on(
                            'postgres_changes',
                            {
                            event: 'INSERT',
                            schema: 'public',
                            table: 'notifications',
                            filter: `user_id=eq.${userId}`
                            },
                            (payload) => {
                                console.log("New notification received:", payload);
                                notifications.value.unshift(payload.new);
                                
                            }
                        )
                        .subscribe();

        status.value = "loaded";

        if(routeNotificationId){
            let notificationToSelect = notifications.value.find(notif => notif.id === routeNotificationId);
            if(notificationToSelect){
                await notificationSelected(notificationToSelect);
            }
        } else {
            selectedNotification.value = null;
        }

    } catch (err) {
        console.log("Error fetching user data:", err);
        router.push("/login");
    }
});

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
                console.log("Create room response:", response.data.chat_room_id);
                selectedNotification.value = response.data.chat_room_id;
                newRoom.value = false;
            }
            console.log("Sending message:", {
                chat_room_id: selectedNotification.value,
                sender_id: userId,
                content: message,
                sender_name: userData.profile_data.display_name,
                sender_image: userData.profile_data.UserImage,
                room_title: "Private Message"
            });
            console.log(userData);
            if(tab.value=="interviews"){
                let currentChatroom = messageNotifications.value.find(msg => msg.chat_room_id === selectedNotification.value);
                await axios.post(`${apiUrl}messages/send`, {
                    chat_room_id: selectedNotification.value,
                    sender_id: userId,
                    content: message,
                    sender_name: userData.profile_data.display_name,
                    sender_image: userData.profile_data.UserImage,
                    fromInterview:true,
                    project_title: currentChatroom.room_name.split('@')[1] + " - " + currentChatroom.room_name.split('@')[0],
                    interview_project_id: currentChatroom.project_id,
                    interview_job_id: currentChatroom.job_id,
                    candidate_name: userData.profile_data.display_name
                });
            }else{
                await axios.post(`${apiUrl}messages/send`, {
                    chat_room_id: selectedNotification.value,
                    sender_id: userId,
                    content: message,
                    sender_name: userData.profile_data.display_name,
                    sender_image: userData.profile_data.UserImage,
                    room_title: "Private Message"
                });
            }
            
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

async function loadRooms(){
    status.value = "loading";
    messageNotifications.value = [];
    try{
        let response = await axios.get(`${apiUrl}users/messages/${userId}/${tab.value}`);
        console.log("Chat rooms response:", response.data);
        for(let message of response.data.chatrooms){
            message.notifs = notifications.value[tab.value].filter(notif => notif.chat_room_id === message.chat_room_id);
        }
        messageNotifications.value.push(...response.data.chatrooms);
        if(newRoom.value && newRoom.value.type === tab.value){
            messageNotifications.value.unshift(newRoom.value);
        }
        status.value = "loaded";
    } catch (err) {
        status.value = "error";
    }
}

async function loadNotifs(){
    try {
        let response = await axios.get(`${apiUrl}users/message_notifications/load/${userId}`);
        response.data.data.forEach(notification => {
            notifications.value[notification.relation].push(notification);
        });
    } catch (err) {
        console.error("Error fetching notifications:", err);
    }
}

async function tabChange(newTab) {
    tab.value = newTab;
    messageNotifications.value = [];
    loads.value = 0;
    await loadRooms();
}

onUnmounted(async () => {
    if(interval){
        clearInterval(interval);
    }
    if(channel){
        supabase.removeChannel(channel);
    }
    // await axios.post(`${apiUrl}users/message_notifications/enable_notifications/${userId}`).catch((err) => {
    //     console.error("Error leaving chat room:", err);
    // });
});


async function createUpdater(){
    interval = setInterval(async () => {
        if(selectedNotification.value){
            await updateChatroom();
        }
    }, messageRate);
}

let channel = null;
let chatInputElement = null;
let chatContainer = null;
let finisihedInitialLoading = false;
let loadingMore = ref(false);
let allLoaded = false;
let errorText = ref('')

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

    try {
        if(channel){
            await supabase.removeChannel(channel);
        }
        messages.value = [];
        let response = await axios.get(`${apiUrl}messages/load/${chat_room_id}/none`);
        messages.value.push(...response.data);
        notifications.value[tab.value] = notifications.value[tab.value].filter(notif => notif.chat_room_id !== chat_room_id);
        let currentChatroom = messageNotifications.value.find(msg => msg.chat_room_id === chat_room_id);
        if(currentChatroom){
            currentChatroom.notifs = [];
        }        
        await axios.post(`${apiUrl}users/message_notifications/in_chat_room/${userId}/${chat_room_id}`);
        channel = supabase
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
                        )
                        .subscribe();
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
            console.error("Error loading more messages:", err);
            allLoaded = true;
            loadingMore = false;
            return false;
        }
    }
    loadingMore.value = false;
    return false;
}

let roomSelectionMenu = ref(false);

function getNotifCountTotal(){
    return notifications.value.friends.length + notifications.value.interviews.length + notifications.value.unknown.length;
}

async function deleteSelected(){
    let i = 0;
    let deletes = 0;
    while (i < notifications.value.length){
        if(notifications.value[i].checked){
            await axios.post(`${apiUrl}users/notifications/delete_notification/${userId}/${notifications.value[i].id}`);
            notifications.value.splice(i, 1);
            deletes++;
        }else{
            i++;
        }
    }

    if(deletes == 0 && selectedNotification.value){
        await axios.post(`${apiUrl}users/notifications/delete_notification/${userId}/${selectedNotification.value.id}`);
        let index = notifications.value.findIndex(notif => notif.id === selectedNotification.value.id);
        notifications.value.splice(index, 1);
    }
    if(selectAll.value){
        selectAll.value = false;
    }
}

async function notificationSelected(notification){
    selectedNotification.value = notification;
    if(!notification.read){
        await axios.post(`${apiUrl}users/notifications/mark_as_read/${userId}/${notification.id}`);
        notification.read = true;
    }
    await nextTick();
    console.log(notification.text_summary);
    if(notification.text_summary.includes("invited")){
        let acceptButton = document.getElementById("accept-offer-button");
        if(acceptButton){
            acceptButton.addEventListener('click', () => acceptInvite(acceptButton.getAttribute("project_id")));
        }
    }else{
        let acceptButton = document.getElementById("accept-offer-button");
        if(acceptButton){
            acceptButton.addEventListener('click', () => acceptInvite(acceptButton.getAttribute("proposal_id")));
        }
    }
    leftBarToggle.value = false;
}
function mobileModeListener(){
    mobileMode.value = window.innerWidth <= 756;
    console.log("Mobile mode:", mobileMode.value);
}

let mobileMode = ref(false)
mobileMode.value = window.innerWidth <= 756;
window.addEventListener('resize', mobileModeListener);


</script>

<template>


    <Header style="z-index:10"/>
    <div class="burgerContainer" v-if="mobileMode">
        <img class="settings" style="z-index:1000" src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Hamburger_icon.svg/1280px-Hamburger_icon.svg.png" @click="leftBarToggle=!leftBarToggle"/>
    </div>
    <div class="middle" v-if="!mobileMode">
        <div class="left-bar">
            <div class="tool-bar">
                <div @click="deleteSelected" class="deleteButton">Delete</div>
                <div @click="toggleSelectAll" :class="selectAll ? 'all-selected' : 'all'"></div>
            </div>
            <div style="position:relative; height:calc(100% - 50px); width:100%; overflow-y:auto; box-sizing:border-box; padding:10px;">
                <div v-if="status=='loaded'" v-for="notification of notifications" :class="selectedNotification && selectedNotification.id === notification.id ? 'selected notification-card' :   (notification.read ? 'notification-card-read' : 'notification-card')"
                                @click="notificationSelected(notification)" >
                    <div class="note-name"><b>{{ notification.title }}</b></div>
                    <div class="note-content"><span v-html="shortened( `${notification.text_summary}` )"></span></div>
                    <div class="note-date">{{ notification.last_update_time=="no-time" ? "" : dayjs(notification.last_update_time).format('MM/DD/YYYY hh:mm A') }}</div>
                    <div class="checkbox" type="checkbox" @click.stop="notification.checked = !notification.checked" :style="notification.checked? 'background-color: #007bff;' : ''"></div>
                </div>
            </div>
        </div>
        <div class="notification-display" :style="selectedNotification==null? 'filter:brightness(.8)' : ''">
            <img v-if="selectedNotification==null" src="@/assets/user-creation/private-message-wait-screen.png" class="wait-screen" />
            <div v-else>
                <div class="full-chat-container">
                    <div class="notif-body-title">{{ selectedNotification ? selectedNotification.title : '' }}</div>
                    <div class="notif-body-time">Recieved at {{ selectedNotification ? dayjs(selectedNotification.time).format('MM/DD/YYYY hh:mm A') : '' }}</div>
                    <div v-html="selectedNotification.HTML"></div>
                    <div style="color:red; margin-top:10px; font-family:Arial, Helvetica, sans-serif; font-size:16px;">{{errorText}}</div>
                </div>
            </div>
        </div>
    </div>
    <div class="middle" v-else>
        <div class="left-bar-mobile" v-if="leftBarToggle">
            
            <div class="left-bar" style="width:100vw">
            <div class="tool-bar">
                <div @click="deleteSelected" class="deleteButton">Delete</div>
                <div @click="toggleSelectAll" :class="selectAll ? 'all-selected' : 'all'"></div>
            </div>
            <div style="position:relative; height:calc(100% - 50px); width:100%; overflow-y:auto; box-sizing:border-box; padding:10px;">
                <div v-if="status=='loaded'" v-for="notification of notifications" :class="selectedNotification && selectedNotification.id === notification.id ? 'selected notification-card' :   (notification.read ? 'notification-card-read' : 'notification-card')"
                                @click="notificationSelected(notification)" >
                    <div class="note-name"><b>{{ notification.title }}</b></div>
                    <div class="note-content"><span v-html="shortened( `${notification.text_summary}` )"></span></div>
                    <div class="note-date">{{ notification.last_update_time=="no-time" ? "" : dayjs(notification.last_update_time).format('MM/DD/YYYY hh:mm A') }}</div>
                    <div class="checkbox" type="checkbox" @click.stop="notification.checked = !notification.checked" :style="notification.checked? 'background-color: #007bff;' : ''"></div>
                </div>
            </div>
        </div>
        

        </div>
        <div class="notification-display" :style="selectedNotification==null? 'filter:brightness(.8)' : ''" style="width:100vw; position:absolute; left:0;">
            <img v-if="selectedNotification==null" src="@/assets/user-creation/private-message-wait-screen.png" class="wait-screen" />
            <div v-else>
                <div class="full-chat-container">
                    <div class="notif-body-title">{{ selectedNotification ? selectedNotification.title : '' }}</div>
                    <div class="notif-body-time">Recieved at {{ selectedNotification ? dayjs(selectedNotification.time).format('MM/DD/YYYY hh:mm A') : '' }}</div>
                    <div v-html="selectedNotification.HTML"></div>
                    <div style="color:red; margin-top:10px; font-family:Arial, Helvetica, sans-serif; font-size:16px;">{{errorText}}</div>
                </div>
            </div>
        </div>
    </div>



    <!-- <Header />

    <div class="middle">
        <div class="left-bar">
            <div class="tool-bar">
                <div @click="toggleSelectAll" class="all">
                    <div v-if="selectAll" class="checked"></div>
                </div>
                <div class="seperator">|</div>
                <div class="delete"></div>
                <div class="settings"></div>
            </div>
            <div v-for="notification of notifications" :key="notification.id" :class="selectedNotification === notification.id ? 'selected notification-card' : (notification.read ? 'notification-card-read' : 'notification-card')" @click="selectedNotification = notification.id; notification.read = true;">
                <span class="checkbox"></span>
                <span class="note-title"><b>{{ notification.title }}</b></span>
                <div class="note-content">{{ shortened(notification.DeHTMLText) }}</div>
                <div class="note-date">{{ new Date(notification.timestamp).toLocaleString() }}</div>
            </div>
        </div>
        <div class="notification-display">
            <div v-if="selectedNotification">
                <div class="body-title">{{ notifications.find(n => n.id === selectedNotification).title }}</div>
                <div class="body-time">{{ new Date(notifications.find(n => n.id === selectedNotification).timestamp).toLocaleString() }}</div>
                <div class="body-content" v-html="notifications.find(n => n.id === selectedNotification).notificationHTML"></div>
            </div>
            <div v-else>
                <p>Select a notification to view its details.</p>
            </div>
        </div>
    </div> -->

</template>




<style scoped>
.all-selected{
    width: 20px;
    height: 20px;
    background-color: rgb(0, 183, 255);
    color: rgb(0, 0, 0);
    font-family: Arial, Helvetica, sans-serif;
    font-size: 12px;
    position: absolute;
    top:10px;
    right:25px;
    border-radius: 50%;
    overflow:hidden;
    
    box-shadow: inset 0px 0px 5px rgba(0, 0, 0, 0.521);
    border: 3px solid rgba(255, 255, 255, 0.459);
}
.all-selected:hover{
    cursor: pointer;
    background-color: rgb(0, 149, 207);
}
.all:hover{
    cursor: pointer;
    background-color: rgba(0, 183, 255, 0.192);
}
.deleteButton{
    font-family: Arial, Helvetica, sans-serif;
    font-size: 14px;
    position: absolute;
    top:8px;
    left:20px;
    border-radius: 5px;
    overflow:hidden;
    background: linear-gradient(to top, rgb(223, 223, 223), white);
    padding-left:8px;
    padding-right: 8px;
    padding-top:5px;
    padding-bottom:5px;
}
.deleteButton:hover{
    background: linear-gradient(to bottom, rgb(255, 255, 255), rgb(196, 196, 196));
    color:rgb(0, 0, 0);
    cursor: pointer;
}
.notif-body-title{
    font-family: Arial, Helvetica, sans-serif;
    font-size: 20px;
    margin-bottom: 10px;
    color:white;
}
.notif-body-time{
    font-family: Arial, Helvetica, sans-serif;
    font-size: 12px;
    color: rgb(199, 199, 199);
    margin-bottom: 20px;
}
.notif-body-content{
    color:white;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 14px;
}
.settings{
    width: 25px;
    height: 25px;
    background-size: 80% 80%;
    background-position: center;
    background-repeat: no-repeat;
    color: rgb(0, 0, 0);
    font-family: fantasy;
    font-size: 12px;
    position: absolute;
    top:10px;
    filter: saturate(0) invert(1) brightness(200%);
    right:10px;
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
.delete{
    width: 25px;
    height: 25px;
    background-color: rgb(255, 255, 255);
    background-image: url("@/assets/user-creation/trash-bin.png");
    border: solid 1px rgb(0, 0, 0);

    background-size: cover;
    color: rgb(0, 0, 0);
    font-family: fantasy;
    font-size: 12px;
    position: absolute;
    top:10px;
    filter:invert(1);
    left:50px;
    border-radius: 5px;
    overflow:hidden;
}
.body-title{
    font-family: fantasy;
    font-size: 20px;
    margin-bottom: 10px;
}
.body-time{
    font-family: fantasy;
    font-size: 12px;
    color: rgb(161, 161, 161);
    margin-bottom: 20px;
}
.body-content{
    font-family: fantasy;
    font-size: 14px;
}

.note-date{
    font-family: Arial, Helvetica, sans-serif;;
    font-size: 10px;
    position: relative;
    top:15px;
}
.note-content{
    font-family: Arial, Helvetica, sans-serif;
    font-size: 12px;
    position: relative;
}
.note-title{
    font-family: fantasy;
    font-size: 16px;
    position: relative;
    top:3px;
}

.checked{
    width:100%;
    font-size: 20px;
    font-family: fantasy;
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

.tool-bar{
    position:relative;
    height: 50px;
    width: 100%;
    background: linear-gradient(to top, rgb(0, 0, 0), rgb(17, 17, 17));
}
.notification-display{
    position: absolute;
    top: 0px;
    left: 300px;
    width: calc(100vw - 380px);
    height: calc(100vh - 60px);
    background-color: rgb(255, 255, 255);
    padding: 40px;
    overflow-y: auto;
}
.left-bar{
    width: 300px;
    height: 100%;
    z-index: 10;
    box-sizing: border-box;
    overflow-y: auto;
    float:left;
    background-color: rgb(63, 63, 63);
    position:relative;
    z-index: 10;
}
.notification-card{
    width: 100%;
    height: 80px;
    background-color: rgb(255, 255, 255);
    box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.1);
    padding: 10px;
    border-bottom: black solid 1px;
    box-sizing: border-box;
    cursor: pointer;
}
.selected{
    width:20px;
    height: 20px;
    background-color: rgb(255, 102, 31);
    box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.1);
    padding: 10px;
    color:white;
    border-bottom: black solid 1px;
    box-sizing: border-box;
    cursor: pointer;
}
.middle{
    position: absolute;
    top: 60px;
    left: 0;
    width:100vw;
    height:calc(100vh - 60px);
    background:rgba(119, 241, 37, 0.315);
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
.container {
  display: flex;
  min-width:940px;
  margin: auto;
  margin-top: 25px;
}

.nav-item {
  display: inline-block;
  height: 25px;
  font-size: 14px;
  /* border-left: 2px solid rgb(0, 0, 0); */
  padding-right: 25px;
  padding-left: 25px;
  font-family: fantasy;
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
  font-family: fantasy;
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
    font-family: fantasy;
    padding:0px 0px;
    position: relative;
    border-radius:5px;
    color:white;
    margin:0px;
    margin-right:15px;
    margin-top:-2.5px;
}

.menu-tool-bar-replace{
    position: absolute;
    top: 0px;
    left: 0;
    width:100%;
    background: linear-gradient(to left, rgb(29, 29, 29), rgb(26, 26, 26));
    height:calc(100%);
    z-index:10;
}
.toolBarBurger{
    position: absolute;
    left:-50px;
    top:0px;
}
.burgerContainer{
    position: absolute;
    left:60px;
    top:10px;
}
.room-notif-cirlce{
    position: absolute;
    right: 10px;
    top: 10px;
    width: 20px;
    height: 20px;
    background-color: rgb(255, 0, 0);
    border-radius: 50%;
    z-index: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: bold;
    color: white;
    font-family: Arial, Helvetica, sans-serif;
}
.bar-notif-cirlce{
    position: absolute;
    right: 20px;
    width: 20px;
    height: 20px;
    top:-0px;
    background-color: rgb(255, 0, 0);
    border-radius: 50%;
    z-index: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: bold;
    color: white;
    font-family: Arial, Helvetica, sans-serif;
}
.notif-cirlce{
    position: absolute;
    top: 22px;
    left: 22px;
    width: 20px;
    height: 20px;
    background-color: rgb(255, 0, 0);
    border-radius: 50%;
    z-index: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: bold;
    color: white;
    font-family: Arial, Helvetica, sans-serif;

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
    color: rgb(0, 0, 0);
    margin-top: 40px;
    text-align: center;

}
.active{
    filter:invert(1);
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
    height: calc(100% - 70px);
    width: calc(100% - 70px);
    padding:35px;
    background:rgba(0, 0, 0, 0.781);
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
    height: calc(100% - 130px);
    width:calc(100% - 40px);
    background-color: rgba(49, 49, 49, 0);
    text-align: left;
    -ms-overflow-style: none;  /* IE and Edge */
    scrollbar-width: none;
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
    bottom:120px;
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
    color: rgb(0, 0, 0);
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
    background-color: rgba(46, 78, 255, 0.253);
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
    display:block;
    font-size: 14px;
    width: calc(100% - 50px);
    position: relative;
    background:rgba(255, 0, 0, 0);
    margin-bottom:-5px;
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
    position: absolute;
    bottom:10px;
    filter: saturate(0) invert(1) brightness(200%);
    left:10px;
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
.delete{
    width: 25px;
    height: 25px;
    background-color: rgb(255, 255, 255);
    background-image: url("@/assets/user-creation/trash-bin.png");
    border: solid 1px rgb(0, 0, 0);

    background-size: cover;
    color: rgb(0, 0, 0);
    font-family: Arial, Helvetica, sans-serif;
    font-size: 12px;
    position: absolute;
    top:10px;
    filter:invert(1);
    left:50px;
    border-radius: 5px;
    overflow:hidden;
}
.body-title{
    font-family: Arial, Helvetica, sans-serif;
    font-size: 20px;
    margin-bottom: 10px;
}
.body-time{
    position: relative;
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
    width: calc(100% - 10px);
    height: 90px;
    margin:auto;
    padding: 10px;
    box-sizing: border-box;
    cursor: pointer;
    position:relative;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.623);
    border-radius: 20px;
    margin-top:10px;
    background: linear-gradient(to top, rgb(219, 219, 219), rgb(252, 252, 252));
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
    position:absolute;
    top:5px;
    right:2px;
    display:inline-block;
    width:20px;
    border-radius: 50%;
    height:20px;
    margin-right: 10px;
    margin-bottom: -10px;
    background-color: rgb(255, 255, 255);
    box-shadow: inset 0px 0px 5px rgba(0, 0, 0, 0.521);
    border: 3px solid rgba(255, 255, 255, 0.575);
}
.checkbox:hover{
    filter: brightness(90%);
    cursor: pointer;
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
.checkbox:hover{
    cursor: pointer;
    background-color: rgba(196, 196, 196, 0.712);
}
.all{
    width: 20px;
    height: 20px;
    background-color: rgb(49, 49, 49);
    color: rgb(0, 0, 0);
    font-family: Arial, Helvetica, sans-serif;
    font-size: 12px;
    position: absolute;
    top:10px;
    right:25px;
    border-radius: 50%;
    overflow:hidden;
    
    box-shadow: inset 0px 0px 5px rgba(0, 0, 0, 0.521);
    border: 3px solid rgba(255, 255, 255, 0.575);
}
.tool-bar{
    position:relative;
    height: 50px;
    width: 100%;
}
.notification-display{
    position: absolute;
    top: 0px;
    left: 300px;
    width: calc(100vw - 380px);
    height: calc(100vh + 20px);
    background: radial-gradient(circle, rgba(245, 255, 108, 0.9), rgba(255, 101, 12, 0.7));
    box-shadow: inset 0px 0px 100px rgba(0, 0, 0, 0.5);
    padding: 40px;
    padding-top: 0px;
    z-index: 0;
}
.notification-display-mobile{
    position: absolute;
    top: 0px;
    left: 0px;
    width: 100vw;
    height: calc(100vh + 20px);
    background: radial-gradient(circle, rgba(245, 255, 108, 0.9), rgba(255, 101, 12, 0.7));
    box-shadow: inset 0px 0px 100px rgba(0, 0, 0, 0.5);
    padding: 40px;
    padding-top: 0px;
    z-index: 0;
}
.left-bar{
    position: absolute;
    width: 300px;
    left: 0px;
    height: 100%;
    z-index: 10;
    box-sizing: border-box;
    background: rgb(255, 255, 255);
    box-shadow: inset 0px 0px 10px rgba(0, 0, 0, 0.623);
    position:relative;
    z-index: 10;
}
.left-bar-mobile{
    position: absolute;
    width: 100vw;
    left: 0px;
    height: 100%;
    z-index: 10;
    box-sizing: border-box;
    position:relative;
    z-index: 10;
    animation: slideIn 0.4s cubic-bezier(0.25, 1.0, 0.1, 1.0) ;
}
.notification-card{
    width: calc(100% - 10px);
    height: 90px;
    margin:auto;
    padding: 10px;
    box-sizing: border-box;
    cursor: pointer;
    position:relative;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.253);
    border-radius: 20px;
    margin-top:10px;
}
.selected{
    position:relative;
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
.container {
  display: flex;
  min-width:940px;
  margin: auto;
  margin-top: 25px;
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