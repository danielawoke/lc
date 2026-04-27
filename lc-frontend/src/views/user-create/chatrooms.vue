<script setup>
import { useRoute, useRouter } from 'vue-router'
import { ref, nextTick, watch, onMounted, onUnmounted } from 'vue';
import Header from '@/components/header.vue'
import axios from 'axios';
import { Account } from 'appwrite';
import { AccountLocal } from '@/lib/appwrite';
import dayjs from 'dayjs';

import { createClient } from '@supabase/supabase-js';
const supabase = createClient(import.meta.env.VITE_SUPABASE_URL, import.meta.env.VITE_SUPABASE_ANON_KEY);
const apiUrl = import.meta.env.VITE_APP_API_URL
const router = useRouter()
const route = useRoute()

let messages = ref(null);
let selectedNotification = ref(null);
let messageNotifications = ref([]);
let messageRate = 1000;
let selectAll = ref(false);

function toggleSelectAll() {
    selectAll.value = !selectAll.value;
    notifications.value.forEach(notification => {
        notification.read = selectAll.value;
    });
}

function shortened(content) {
    if(content.length > 50){
        return content.substring(0, 50) + "...";
    }
    return content;
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
let notifications = ref({
    "friends": [],
    "interviews": [],
    "unknown": [],
});
let mobileMode = ref(false);
onMounted(async () => {
    try {
        let user = await AccountLocal.get();
        userId = user.$id;

        let queriedUsertag = route.query.usertag;
        let areFriends = route.query.friends;
        let chat_room_id = route.query.chat_room_id;
        let type = route.query.type;

        mobileMode.value = window.innerWidth <= 768;
        window.addEventListener('resize', mobileModeListener);
        const userDataResponse = await axios.get(`${apiUrl}users/search/full_profile/${userId}`);
        userData = userDataResponse.data.profile[0];
        if(!userDataResponse.data["profile"]){
            router.push("/login");
        } else {
            console.log(notifications.value);
            await loadNotifs();
            supabase
                .channel('notifications')
                .on(
                    'postgres_changes',
                    {
                    event: '*',
                    schema: 'public',
                    table: 'unread_messages',
                    filter: `user_id=eq.${userId}`
                    },
                    (payload) => {
                        console.log("Received message notification change:", payload);
                        if(payload.eventType === "INSERT"){
                            notifications.value[payload.new.relation].push(payload.new);
                            let message = messageNotifications.value.find(msg => msg.chat_room_id === payload.new.chat_room_id);
                            if(message){
                                message.notifs.push(payload.new);
                            }
                        }
                    }
                )
                .subscribe();
        }

        if(queriedUsertag){
            tab.value = areFriends === "true" ? "friends" : "unknown";
            await loadRooms();
            let room_id = await axios.get(`${apiUrl}messages/auto_load/${userId}/${queriedUsertag}`);
            if(room_id.data.length>0){
                selectedNotification.value = room_id.data[0].chat_room_id;
                await loadChatroom(selectedNotification.value);
            }else{
                let res = await axios.post(`${apiUrl}users/new_chat_limit/${userId}`)
                console.log(res)
                if(!res.data.result){
                    alert("Only premium members can message more than 10 people in a given day. Please purchase a subscription in settings or wait till tommorow.")
                }else{
                    selectedNotification.value = -1;
                    profileResponse.value = await axios.get(`${apiUrl}users/search/search_by_usertag/${queriedUsertag}`);
                    newRoom.value = {
                        type: tab.value,
                        chat_room_id: -1,
                        room_name: `${profileResponse.value.data.profile[0].profile_data.display_name}`,
                        room_image: profileResponse.value.data.profile[0].profile_data.UserImage,
                        last_message: {
                            content: "Start the conversation!",
                            user_id: "~",
                            user_name: "",
                        },
                        last_update_time: "no-time",
                    };
                    messageNotifications.value.unshift(newRoom.value);
                    await nextTick();
                    let chatInputElement = document.getElementById("chat-input");
                    chatInputElement.addEventListener('keypress', sendEnter);
                }
            }
        }else if(chat_room_id && type){
            tab.value = type;
            await loadRooms();
            selectedNotification.value = chat_room_id;
            await loadChatroom(selectedNotification.value);
        }else{
            await loadRooms();
        }

    } catch (err) {
        console.log("Error fetching user data:", err);
        router.push("/login");
    }
});

function mobileModeListener(){
    mobileMode.value = window.innerWidth <= 768;
    console.log("Mobile mode:", mobileMode.value);
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
        console.log("Loaded rooms:", response.data.chatrooms);
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
    await axios.post(`${apiUrl}users/message_notifications/enable_notifications/${userId}`).catch((err) => {
        console.error("Error leaving chat room:", err);
    });
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

    if(mobileMode.value){
        leftBarToggle.value = false;
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

</script>

<template>
    <Header style="z-index:10"/>
    <div class="burgerContainer" v-if="mobileMode">
        <img class="settings" style="z-index:1000" src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Hamburger_icon.svg/1280px-Hamburger_icon.svg.png" @click="leftBarToggle=!leftBarToggle"/>
        <div class="notif-cirlce" style="top:-25px; left:5px; z-index:1000;" @click="leftBarToggle=!leftBarToggle" v-if="getNotifCountTotal() > 0">{{ getNotifCountTotal()>9 ? '9+' : getNotifCountTotal() }}</div>
    </div>
    <!-- <div class="toolBarBurger">
        <div class="burgerContainer" v-if="mobileMode">
            <img class="settings" style="z-index:1000; width:35px;" src="https://images.icon-icons.com/3871/PNG/512/menu_icon_244496.png" @click="toolBarSubsituteToggle=!toolBarSubsituteToggle"/>
        </div>
    </div> -->
    <div class="middle" v-if="!mobileMode">
        <div class="left-bar">
            <!-- Should update as a websocket if the element is not selected it should be subjec to moving around if new messages come into it, but we'll come back to this
                I may skips this all together -->
            <div class="tool-bar">
                <img class="settings" src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Hamburger_icon.svg/1280px-Hamburger_icon.svg.png" @click="roomSelectionMenu=!roomSelectionMenu"/>
                <div class="notif-cirlce" @click="roomSelectionMenu=!roomSelectionMenu" v-if="getNotifCountTotal() > 0">{{ getNotifCountTotal()>9 ? '9+' : getNotifCountTotal() }}</div>
                <div class="priv-title">{{ tab === 'friends' ? 'Friends' : tab === 'interviews' ? 'Interviews' : 'Unknown/Outbound' }}</div>
                <!-- <div class="friends-button" :class="{ 'active': tab === 'friends' }" @click="tabChange('friends')">Friends</div>
                <div class="interview-button" :class="{ 'active': tab === 'interviews' }" @click="tabChange('interviews')">Interviews</div>
                <div class="unknown-button" :class="{ 'active': tab === 'unknown' }" @click="tabChange('unknown')">Unknown</div> -->
            </div>
            <!-- the updates need to be thought out since the current user should see thier own messages as a notification -->
            <div style="position:relative; height:calc(100% - 50px); width:100%; overflow-y:auto; box-sizing:border-box; padding:10px;">
                <div v-if="status=='loaded' && (tab=== 'friends' || tab=== 'unknown')" v-for="message of messageNotifications" :key="message.chat_room_id" :class="selectedNotification === message.chat_room_id ? 'selected notification-card' : 'notification-card'" @click="selectedNotification = null; loadChatroom(message.chat_room_id); selectedNotification = message.chat_room_id;"
                                :style="message.last_update_time=='no-time'? 'height: 80px;':''">
                    <span class="group-chat-image" :style="{ backgroundImage: `url(${message.room_image})` }"></span>
                    <div class="note-name">{{ message.room_name }}</div>
                    <br />
                    <div class="note-content"><span v-html="shortened( `<b>${message.last_message?.user_id == userId ? 'You' : message.last_message?.user_name}</b> ${message.last_update_time=='no-time' ? 'No messages yet' : message.last_message?.content}` )"></span></div>
                    <div class="note-date">{{ message.last_update_time=="no-time" ? "" : dayjs(message.last_update_time).format('MM/DD/YYYY hh:mm A') }}</div>
                    <div class="room-notif-cirlce" v-if="message.notifs?.length>0">{{ message.notifs?.length > 9 ? '9+' : message.notifs?.length }}</div>
                </div>
                <div v-else-if="status=='loaded' && tab === 'interviews'"  v-for="message of messageNotifications" :key="message.chat_room_id" :class="selectedNotification === message.chat_room_id ? 'selected notification-card' : 'notification-card'" @click="selectedNotification = null; loadChatroom(message.chat_room_id); selectedNotification = message.chat_room_id;"
                                :style="message.last_update_time=='no-time'? 'height: 100px;':'height: 100px'">
                    <span class="group-chat-image" :style="{ backgroundImage: `url(${message.room_image})`, verticalAlign: 'top' }"></span>
                    <div class="note-name" style="margin-top: 5px;"><b>{{ message.room_name.split('@')[0] }}</b> - <i>{{ message.room_name.split('@')[1] }}</i></div>

                    <div class="note-content" style="margin-top:-5px"><span v-html="shortened( `<b>${message.last_message == null? '' : message.last_message?.user_id == userId ? 'You' : message.last_message?.user_name}</b> ${message.last_message == null ? 'No messages yet' : message.last_update_time=='no-time' ? 'No messages yet' : message.last_message?.content}` )"></span></div>
                    <div class="note-date">{{ message.last_update_time=="no-time" || message.last_message == null ? "" : dayjs(message.last_update_time).format('MM/DD/YYYY hh:mm A') }}</div>
                    <div class="room-notif-cirlce" v-if="message.notifs.length>0">{{ message.notifs?.length > 9 ? '9+' : message.notifs?.length }}</div>    
                </div>
                <div class="left-bar-text" v-else-if="status=='loading'">Loading...</div>
                <div class="left-bar-text" v-else-if="status=='error'">No messages found.</div>
                <div style="height:20px;"></div>
            </div>
            <div v-if="roomSelectionMenu" class="menu">
                <div style="height:40px"></div>
                <div @click="tab='friends'; loadRooms(); roomSelectionMenu=false;" class="body-time">Friends<div class="bar-notif-cirlce" v-if="notifications.friends.length > 0">{{ notifications.friends.length>9 ? '9+' : notifications.friends.length }}</div></div>
                <div @click="roomSelectionMenu=false; tab='interviews'; loadRooms();" class="body-time">Interviews<div class="bar-notif-cirlce" v-if="notifications.interviews.length > 0">{{ notifications.interviews.length>9 ? '9+' : notifications.interviews.length }}</div></div>
                <div @click="roomSelectionMenu=false; tab='unknown'; loadRooms();" class="body-time">Unknown/Outbound<div class="bar-notif-cirlce" v-if="notifications.unknown.length > 0">{{ notifications.unknown.length>9 ? '9+' : notifications.unknown.length }}</div></div>
            </div>
        </div>
        <div class="notification-display" :style="selectedNotification==null? 'filter:brightness(.8)' : ''">
            <img v-if="selectedNotification==null" src="@/assets/user-creation/private-message-wait-screen.png" class="wait-screen" />
             <div class="full-chat-container">
                <div class="message-container">
                    <div v-if="loadingMore" style="font-size: 20px; font-weight: bold; font-family:Arial, Helvetica, sans-serif; opacity:.6; padding:20px; margin:20px; margin-top:50px;">Loading messages...</div>
                    <div style="height:20px;"></div>
                    <!-- Im thinking make a global var for the day, and when it passes, in the messages you add a day division, or passes 24 hours -->
                    <div v-for="message in messages" class='message'>
                        <div style="padding-bottom:20px;" v-if="message.user_id!=-1">
                            <div class="message-content-container">
                                <div>
                                    <img class="profile-pic" :src="message.image_url"></img>
                                </div>
                                <div class="content-block">
                                    <b class="name" :style="{ color: message.color }">{{ message.name }} </b>
                                    <div class="time">{{ dayjs(message.time).format('MM/DD/YYYY hh:mm A') }}</div>
                                    <div class="message-text">{{ message.content }}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="spacing"></div>
                </div>
                <div v-if="selectedNotification!=null" class="text-bar">
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
    <div class="middle" v-else>
        <div class="left-bar-mobile" v-if="toolBarSubsituteToggle">
            <div class="menu-tool-bar-replace">
                <div style="height:40px"></div>
                <div @click="tab='friends'; loadRooms(); roomSelectionMenu=false;" class="body-time">Edit</div>
                <div @click="roomSelectionMenu=false; tab='interviews'; loadRooms();" class="body-time">Votes</div>
                <div @click="roomSelectionMenu=false; tab='unknown'; loadRooms();" class="body-time">Chat</div>
                <div @click="roomSelectionMenu=false; tab='unknown'; loadRooms();" class="body-time">People</div>
                <div  class="body-time" @click="goToSettings">Settings</div>
            </div>
        </div>
        <div class="left-bar-mobile" v-if="leftBarToggle">
            <div class="tool-bar">
                <img class="settings" src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Hamburger_icon.svg/1280px-Hamburger_icon.svg.png" @click="roomSelectionMenu=!roomSelectionMenu"/>
                <div class="notif-cirlce" @click="roomSelectionMenu=!roomSelectionMenu" v-if="getNotifCountTotal() > 0">{{ getNotifCountTotal()>9 ? '9+' : getNotifCountTotal() }}</div>
                <div class="priv-title">{{ tab === 'friends' ? 'Friends' : tab === 'interviews' ? 'Interviews' : 'Unknown/Outbound' }}</div>
            </div>
            <div style="position:relative; height:calc(100% - 50px); width:100%; overflow-y:auto; box-sizing:border-box; padding:10px;">
                <div v-if="status=='loaded' && (tab=== 'friends' || tab=== 'unknown')" v-for="message of messageNotifications" :key="message.chat_room_id" :class="selectedNotification === message.chat_room_id ? 'selected notification-card' : 'notification-card'" @click="selectedNotification = null; loadChatroom(message.chat_room_id); selectedNotification = message.chat_room_id;"
                                :style="message.last_update_time=='no-time'? 'height: 80px;':''">
                    <span class="group-chat-image" :style="{ backgroundImage: `url(${message.room_image})` }"></span>
                    <div class="note-name">{{ message.room_name }}</div>
                    <br />
                    <div class="note-content"><span v-html="shortened( `<b>${message.last_message?.user_id == userId ? 'You' : message.last_message?.user_name}</b> ${message.last_update_time=='no-time' ? 'No messages yet' : message.last_message?.content}` )"></span></div>
                    <div class="note-date">{{ message.last_update_time=="no-time" ? "" : dayjs(message.last_update_time).format('MM/DD/YYYY hh:mm A') }}</div>
                    <div class="room-notif-cirlce" v-if="message.notifs.length>0">{{ message.notifs?.length > 9 ? '9+' : message.notifs?.length }}</div>
                </div>
                <div v-else-if="status=='loaded' && tab === 'interviews'"  v-for="message of messageNotifications" :key="message.chat_room_id" :class="selectedNotification === message.chat_room_id ? 'selected notification-card' : 'notification-card'" @click="selectedNotification = null; loadChatroom(message.chat_room_id); selectedNotification = message.chat_room_id;"
                                :style="message.last_update_time=='no-time'? 'height: 80px;':''">
                    <span class="group-chat-image" :style="{ backgroundImage: `url(${message.room_image})`, verticalAlign: 'top' }"></span>
                    <div class="note-name" style="margin-top: 5px;"><b>{{ message.room_name.split('@')[0] }}</b> - <i>{{ message.room_name.split('@')[1] }}</i></div>

                    <div class="note-content" style="margin-top:0px"><span v-html="shortened( `<b>${message.last_message == null? '' : message.last_message?.user_id == userId ? 'You' : message.last_message?.user_name}</b> ${message.last_message == null ? 'No messages yet' : message.last_update_time=='no-time' ? 'No messages yet' : message.last_message?.content}` )"></span></div>
                    <div class="note-date">{{ message.last_update_time=="no-time" || message.last_message == null ? "" : dayjs(message.last_update_time).format('MM/DD/YYYY hh:mm A') }}</div>
                    <div class="room-notif-cirlce" v-if="message.notifs.length>0">{{ message.notifs?.length > 9 ? '9+' : message.notifs?.length }}</div>    
                </div>
                <div class="left-bar-text" v-else-if="status=='loading'">Loading...</div>
                <div class="left-bar-text" v-else-if="status=='error'">No messages found.</div>
                <div style="height:20px;"></div>
            </div>
            <div v-if="roomSelectionMenu" class="menu">
                <div style="height:40px"></div>
                <div @click="tab='friends'; loadRooms(); roomSelectionMenu=false;" class="body-time">Friends<div class="bar-notif-cirlce" v-if="notifications.friends.length > 0">{{ notifications.friends.length>9 ? '9+' : notifications.friends.length }}</div></div>
                <div @click="roomSelectionMenu=false; tab='interviews'; loadRooms();" class="body-time">Interviews<div class="bar-notif-cirlce" v-if="notifications.interviews.length > 0">{{ notifications.interviews.length>9 ? '9+' : notifications.interviews.length }}</div></div>
                <div @click="roomSelectionMenu=false; tab='unknown'; loadRooms();" class="body-time">Unknown/Outbound<div class="bar-notif-cirlce" v-if="notifications.unknown.length > 0">{{ notifications.unknown.length>9 ? '9+' : notifications.unknown.length }}</div></div>
            </div>
        </div>
        <div class="notification-display-mobile" :style="selectedNotification==null? 'filter:brightness(.8)' : ''">
            <img v-if="selectedNotification==null" src="@/assets/user-creation/private-message-wait-screen.png" class="wait-screen" />
             <div class="full-chat-container">
                <div class="message-container">
                    <div v-if="loadingMore" style="font-size: 20px; font-weight: bold; font-family:Arial, Helvetica, sans-serif; opacity:.6; padding:20px; margin:20px; margin-top:50px;">Loading messages...</div>
                    <div style="height:20px;"></div>
                    <!-- Im thinking make a global var for the day, and when it passes, in the messages you add a day division, or passes 24 hours -->
                    <div v-for="message in messages" class='message'>
                        <div style="padding-bottom:20px;" v-if="message.user_id!=-1">
                            <div class="message-content-container">
                                <div>
                                    <img class="profile-pic" :src="message.image_url"></img>
                                </div>
                                <div class="content-block">
                                    <b class="name" :style="{ color: message.color }">{{ message.name }} </b>
                                    <div class="time">{{ dayjs(message.time).format('MM/DD/YYYY hh:mm A') }}</div>
                                    <div class="message-text">{{ message.content }}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="spacing"></div>
                </div>
                <div v-if="selectedNotification!=null" class="text-bar">
                    <div class="chat-box-mobile">
                        <textarea id="chat-input" placeholder="write your message here..." class="chat-input" v-model="chatInput"></textarea>
                        <div @click="send(chatInput)" class="send-button-container">
                            <button class="send-button"></button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

</template>

<style scoped>
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
    top:60px;
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
    height: 100%;
    width: calc(100%);
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
.chat-box-mobile{
        display: flex;
        width: calc(100% - 150px);
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
    scrollbar-width: none; /* Firefox */
    scrollbar-color: transparent transparent; /* Firefox */
    scrollbar-width: none; /* Safari and Chrome */
    -ms-overflow-style: none;  /* IE and Edge */
}
.chat-input::-webkit-scrollbar {
    display: none; /* Safari and Chrome */
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
    white-space-collapse: collapse;
    overflow-wrap: break-word; /* Modern standard */
    word-wrap: break-word;     /* Legacy support */
    word-break: break-word
    
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
    max-width: calc(100% - 40px);
    margin-right: 80px;
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
.notification-display{
    position: absolute;
    top: 0px;
    left: 300px;
    width: calc(100vw - 380px);
    height: calc(100vh + 20px);
    background: radial-gradient(circle, rgba(108, 255, 223, 0.9), rgba(182, 56, 255, 0.7));
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
    background: radial-gradient(circle, rgba(108, 255, 223, 0.9), rgba(182, 56, 255, 0.7));
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
    background: linear-gradient(to top, rgb(255, 255, 255), rgb(252, 252, 252)); 
    position:relative;
    box-shadow: inset 0px 0px 20px rgba(0, 0, 0, 0.925);
    z-index: 10;
}
.left-bar-mobile{
    position: absolute;
    width: 100vw;
    left: 0px;
    height: 100%;
    z-index: 10;
    box-sizing: border-box;
    background: linear-gradient(to top, rgb(255, 255, 255), rgb(252, 252, 252)); 
    position:relative;
    box-shadow: inset 0px 0px 20px rgba(0, 0, 0, 0.925);
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