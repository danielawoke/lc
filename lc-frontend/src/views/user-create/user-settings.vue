<!-- To wipe docker
docker compose down -v
docker system prune -af
-->

<script setup>
import { ref, nextTick, watch, onMounted } from 'vue';
import Location from '@/components/supporting-components/location-profile.vue';
import ImageEditorPopUp from '@/components/founder-space/interfaces/edit-cards/image-replace/pop-up.vue';
import Header from '@/components/header.vue';
import {AccountLocal} from '@/lib/appwrite.js';
import axios from 'axios';
import { useRouter } from 'vue-router';
const apiURL = import.meta.env.VITE_APP_API_URL;
import { supabase } from '@/lib/supabase.js';
import { loadStripe } from '@stripe/stripe-js';
import dayjs from 'dayjs';
let stripe = null;
let subscription = ref('Freemium');
const router = useRouter();

function selectRoom(categoryId, roomId) {
    // Do a call to the backend to the new messages for this channel
    messages.value = [
        { sender: 'Alice', time: '9/2/2026, 10:28 AM', color: '#ff5555', content: 'Hey, do you know where the snakes are? I need to feed them. Hey, do you know where the snakes are? I need to feed them. Hey, do you know where the snakes are? I need to feed them. Hey, do you know where the snakes are? I need to feed them. Hey, do you know where the snakes are? I need to feed them. Hey, do you know where the snakes are? I need to feed them. Hey, do you know where the snakes are? I need to feed them.  ', 
        imageURL: 'https://www.ckfamilydds.com/wp-content/uploads/2024/02/why-we-lick.jpg' },
        { sender: 'Bob', time: '9/2/2026, 10:30 AM', color: '#55ff55', content: 'Yes, they are in the backyard.', imageURL: 'https://www.ckfamilydds.com/wp-content/uploads/2024/02/why-we-lick.jpg' },
    ];
    selectedRoom.value = [categoryId, roomId];
}

let userID = null;
let completeSave = ref(false);
let personalSettings = ref({});

onMounted(async () => {
    let user = await AccountLocal.get()
    userID = user.$id;

    await axios.get(`${apiURL}users/settings/load_personal_settings/${userID}`).then(async (response) => {
        personalSettings.value = response.data[0];        
        
    }).catch((error) => {
        console.error(error);
    });

    stripe = await loadStripe(import.meta.env.VITE_STRIPE_PUBLIC_KEY);

    
});

async function subscribe(){
    const res = await fetch(`${apiURL}users/subscribe_session/${userID}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ priceId: 'price_1TNZLXK2Xpe5FcUQkKaLPuRQ' }),
    });

    const { url } = await res.json();
    window.location.href = url;
}

function createNewRoom() {
    const newRoomId = roomCategories.value[0].rooms.length;
    let backendRoomNumber = 2;
    let newID = roomCategories.value[0].rooms.length;
    roomCategories.value[0].rooms.push({ name: `Room ${backendRoomNumber}`, id: newID, category: 'Founder' });
    selectRoom(0, newID);
}

function collapse(category){
    category.collapsed = !category.collapsed;
}

let mode = ref('chat');
let configureMode = ref('Room Settings');

let currentImage = ref('@/assets/founder-space/chat/closed-door.svg');


async function changeImage(){
    imageEditMode.value = true;
    await nextTick();
    console.log(imageChangeInfo)
    document.getElementById("close-button").addEventListener("click", function () {
        const element = document.getElementById('popup-backdrop');
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
            imageEditMode.value = false;
        }, time);
    });
}

let imageEditMode = ref(false);
const backDropClick = ref([false]);
const saveResults = ref([false, null]);
let imageChangeInfo = {
    blob: [null],
    url: [null]
};

function logout(){
    
    AccountLocal.deleteSession("current").then(async () => {
        
        try {
            await AccountLocal.deleteSessions();
        } catch {}

        document.cookie.split(";").forEach(c => {
            document.cookie = c
            .replace(/^ +/, "")
            .replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/");
        });

        localStorage.clear();
        sessionStorage.clear();
        window.location.reload();

        

    }).catch(err => {
        console.log("Error logging out", err);
    });
}

watch(saveResults, async (newVal) => {
    if (newVal[0] === true) {
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
            imageEditMode.value = false;
            // document.getElementById("main-card-image").style.backgroundImage = 'url('+newVal[1]+')';
            personalSettings.value.profile_data.UserImage = newVal[1]
            saveResults.value = [false, null];
        }, time);
    }
},{deep: true});


watch(backDropClick, async (newVal) => {
    if (newVal[0] == true) {
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
            imageEditMode.value = false;
            backDropClick.value[0] = false;
        }, time);
    }
},{deep: true});

async function uploadProfileImage(url, userId){

    const filePath = `${userId}`;
    // I really dont like this auth setup, see if there's a way you can avoid using a login like this on the frontend
    await supabase.auth.signInWithPassword({
        email: import.meta.env.VITE_ADMIN_USERNAME,
        password: import.meta.env.VITE_ADMIN_PASSWORD
    });
    
    try{
        await supabase.storage.from("profile_images").remove([filePath]); // note: array of file paths
    }
    catch(err){
        console.log("No existing profile image to delete, proceeding with upload.");
    }

    let image_blob = null;
    try{
        image_blob = await fetch(url).then(r => r.blob());
    }catch(e){
        let response = await fetch(`${import.meta.env.VITE_CORS_PROXY_URL}${encodeURIComponent(url)}`);
        if (!response.ok) {
            image_blob = null;
        }else{
            image_blob = response.blob();
        }
    }
    if(image_blob != null){
        try{
            await supabase.storage.from("profile_images").upload(filePath, image_blob);
        }catch(err){
            console.error("Error uploading profile image:", err);
        }
        const { data, error } = supabase.storage.from("profile_images").getPublicUrl(filePath);
        if (error) {
            console.error(error);
        } else {
            console.log("URL:", data.publicUrl);
        }
        return data.publicUrl;
    }else{
        return url;
    }
}


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
            return location;
        }else{
            console.error("No results found for the given address.");
            return null;
        }
    }catch(err){
        console.error("Error converting address to coordinates:", err);
        return null;
    }
}

async function saveProfileChanges(){
    
    let imageURL = personalSettings.value.profile_data.UserImage;
    console.log(imageURL)

    if(imageChangeInfo.url[0]){
        imageURL = await uploadProfileImage(imageChangeInfo.url[0], userID);
    }

    let location = document.getElementById("location-input").value;
    let lat = personalSettings.value.lat;
    let lng = personalSettings.value.lng;

    if(location == ''){
        location = '';
        lat = 44.0682;
        lng = 114.742;
    }
    else if(location != personalSettings.value.profile_data.location){
        let coords = await convertAddressToCoordinates(location);
        lat = coords.lat;
        lng = coords.lng;
    }

    let display_name = document.getElementById("display-name-input").value;
    let looking_for = document.getElementById("looking-for-input").value;

    personalSettings.value.profile_data.UserImage = imageURL;
    personalSettings.value.profile_data.location = location;
    personalSettings.value.profile_data.display_name = display_name;

    console.log("Saving profile changes with the following data:", {
        profile_data: personalSettings.value.profile_data,
        lat: lat,
        lng: lng,
        looking_for: looking_for
    });

    await axios.post(`${apiURL}users/settings/update_personal_settings/${userID}`, {
        profile_data: personalSettings.value.profile_data,
        lat: lat,
        lng: lng,
        looking_for: looking_for
    }).then((response) => {
        completeSave.value = true;
        setTimeout(() => {
            completeSave.value = false;
        }, 5700);
    }).catch((error) => {
        console.error("Error saving profile changes:", error);
    });
}

async function updateNotificationSetting(setting, event){
    let newValue = event.target.checked;
    let currentSettingsClone = JSON.parse(JSON.stringify(personalSettings.value.notification_settings));
    currentSettingsClone[setting] = newValue;
    await axios.post(`${apiURL}users/settings/update_notification_settings/${userID}`, {
        setting: currentSettingsClone
    }).then((response) => {
        personalSettings.value.notification_settings[setting] = newValue;
    }).catch((error) => {
        console.error("Error updating notification setting:", error);
    });
}

let deleteAccountRender = ref(false)
async function deleteAccount(){
     if(document.getElementById("usertag-input").value === personalSettings.value.user_tag){
        await axios.post(`${apiURL}users/delete_user/${userID}`).then(async (response) => {
            supabase.auth.signOut();
            await logout();
            router.push("/");
        }).catch((error) => {
            console.error("Error deleting account:", error);
        });
    }
}

async function cancelSubscription(){
    await axios.post(`${apiURL}users/unsubscribe/${userID}`).then((response) => {
        personalSettings.value.Premium = "marked for deletion";
    }).catch((error) => {
        console.error("Error cancelling subscription:", error);
    });
}

async function resubscribe(){
    await axios.post(`${apiURL}users/resubscribe/${userID}`).then((response) => {
        personalSettings.value.Premium = "Premium";
    }).catch((error) => {
        console.error("Error resubscribing:", error);
    });
}

function mobileModeListener(){
    mobileMode.value = window.innerWidth <= 756;
    console.log("Mobile mode:", mobileMode.value);
}

let mobileMode = ref(false)
mobileMode.value = window.innerWidth <= 756;
window.addEventListener('resize', mobileModeListener);

let leftBarToggle = ref(false);

</script>

<template>
        <div v-if="deleteAccountRender" class="popup-background" @click.self="deleteAccountRender=false">
            <div class="menu">
                <div style="font-size:16px; font-style:normal; font-family:Arial, Helvetica, sans-serif; text-align: left; margin-bottom: 10px;"> Retype your usertag to delete your account permanently:</div>
                <input class="rename-input" id="usertag-input" style="width: calc(100% - 10px); position:absolute; left: 10px;" :placeholder="personalSettings?.user_tag"/>
                <div class="delete-button" style="margin-top:50px; margin-left:0; float:left;" @click="deleteAccountRender=false">Cancel</div>
                <div class="delete-button" style="margin-top:50px;" @click="deleteAccount">Delete Account</div>
            </div>
        </div>
        <ImageEditorPopUp v-if="imageEditMode" :backDropClick="backDropClick" :saveResults="saveResults" :imageInfo="imageChangeInfo"/>
        <Header />
        
        <div class="burgerContainer" v-if="mobileMode">
            <img class="settings" style="z-index:1000" src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Hamburger_icon.svg/1280px-Hamburger_icon.svg.png" @click="leftBarToggle=!leftBarToggle"/>
        </div>
        <div class="configure-mobile-side-bar" v-if="mobileMode && leftBarToggle" style="height:calc(100vh - 60px); top:60px; background:white; box-shadow:0 5px 30px 5px rgba(0,0,0,.5)">
            <div style="height:20px;"></div>
            <div @click="configureMode='Room Settings'; leftBarToggle = false;" :class="configureMode === 'Room Settings' ? 'selected-setting' : 'unselected-setting'" style="width:calc(100vw - 50px)">
                Personal
            </div>
            <div @click="configureMode='Notifications'; leftBarToggle = false;" :class="configureMode === 'Notifications' ? 'selected-setting' : 'unselected-setting'" style="width:calc(100vw - 50px)">
                Notifications
            </div>
            <div @click="configureMode='Account'; leftBarToggle = false;" :class="configureMode === 'Account' ? 'selected-setting' : 'unselected-setting'" style="width:calc(100vw - 50px)">
                Account
            </div>
        </div>
        <div class="container">
            <div class="configure-side-bar" v-if="!mobileMode">
                <div style="height:20px;"></div>
                <div @click="configureMode='Room Settings'" :class="configureMode === 'Room Settings' ? 'selected-setting' : 'unselected-setting'">
                    Personal
                </div>
                <div @click="configureMode='Notifications'" :class="configureMode === 'Notifications' ? 'selected-setting' : 'unselected-setting'">
                    Notifications
                </div>
                <div @click="configureMode='Account'" :class="configureMode === 'Account' ? 'selected-setting' : 'unselected-setting'">
                    Account
                </div>
            </div>
            <div class="full-setting-container" :style="mobileMode? 'width: calc(100vw)' : 'width: calc(100% - 320px)' ">
                <div class="setting-display-container">
                    <div v-if="configureMode === 'Notifications'" >
                         <div class="question-box">
                            <div class="option-label">
                                Notifications
                            </div>
                            <div class="option-action-space-block">
                                <div class="toggle">
                                    <label class="switch">
                                        <input type="checkbox" :checked="personalSettings?.notification_settings?.mute_friends_messages" @change="updateNotificationSetting('mute_friends_messages', $event)">
                                        <span class="slider round"></span>
                                    </label>
                                </div>
                                <div class="option-description">
                                    <div><b>Mute friends messages</b></div>
                                    <div>Turn off private messages from friends</div>
                                </div>
                                <div class="toggle">
                                    <label class="switch">
                                        <input type="checkbox" :checked="personalSettings?.notification_settings?.mute_interview_messages" @change="updateNotificationSetting('mute_interview_messages', $event)">
                                        <span class="slider round"></span>
                                    </label>
                                </div>
                                <div class="option-description">
                                    <div><b>Mute interview messages</b></div>
                                    <div>Turn off notifications from project groups interviewing you</div>
                                </div>
                                <div class="toggle">
                                    <label class="switch">
                                        <input type="checkbox" :checked="personalSettings?.notification_settings?.mute_unknown_private_messages" @change="updateNotificationSetting('mute_unknown_private_messages', $event)">
                                        <span class="slider round"></span>
                                    </label>
                                </div>
                                <div class="option-description">
                                    <div><b>Mute unknown private messages</b></div>
                                    <div>Turn off notifications from unknown users sending private messages</div>
                                </div>
                                <!-- <div class="toggle">
                                    <label class="switch">
                                        <input type="checkbox" :checked="personalSettings?.notification_settings?.mute_new_candidates_notifications" @change="updateNotificationSetting('mute_new_candidates_notifications', $event)">
                                        <span class="slider round"></span>
                                    </label>
                                </div>
                                <div class="option-description">
                                    <div><b>Mute new candidates notifications</b></div>
                                    <div>Wont be notified of new project applicants</div>
                                </div>
                                <div class="toggle">
                                    <label class="switch">
                                        <input type="checkbox" :checked="personalSettings?.notification_settings?.mute_new_proposals_notifications" @change="updateNotificationSetting('mute_new_proposals_notifications', $event)">
                                        <span class="slider round"></span>
                                    </label>
                                </div>
                                <div class="option-description">
                                    <div><b>Mute new proposal notifications</b></div>
                                    <div>Wont be notified of new proposals</div>
                                </div> -->
                                <div class="toggle">
                                    <label class="switch">
                                        <input type="checkbox" :checked="personalSettings?.notification_settings?.email_notifications" @change="updateNotificationSetting('email_notifications', $event)">
                                        <span class="slider round"></span>
                                    </label>
                                </div>
                                <div class="option-description">
                                    <div><b>Email Notifications</b></div>
                                    <div>Double down and send notifications through email (This email will be <b>{{personalSettings?.email}}</b>)</div>
                                </div>
                            </div>
                        </div>    
                    </div>
                    <div v-else-if="configureMode === 'Room Settings'">
                        <div style="margin-bottom: -50px;" class="question-box">
                            <div class="option-action-space-block">
                                <div class="input-label">
                                    Status
                                    <div class="sub-text">Enter a new status</div>
                                </div>
                                <textarea style="height: 100px; resize: none;" class="rename-input" id="looking-for-input" placeholder="Im looking for..." :value="personalSettings?.looking_for"/> 
                            </div>
                        </div>
                        <div style="margin-bottom: -50px;" class="question-box">
                            <div class="option-action-space-block">
                                <div class="input-label">
                                    Profile
                                    <div class="sub-text">Change your display name</div>
                                </div>
                                <input class="rename-input" id="display-name-input" placeholder="Enter new name" :value="personalSettings?.profile_data?.display_name"/>
                                <br/>
                                <div style="margin-left: 20px;" class="sub-text">Update your profile image</div>
                                <div class="image-space">
                                    <div id="main-card-image" class="image" :style="{backgroundImage: 'url('+personalSettings?.profile_data?.UserImage+')', backgroundPosition:'center', backgroundSize: 'cover', backgroundRepeat: 'no-repeat'}" ></div>
                                    <img @click="changeImage" class="image-edit-faint" src="@/assets/founder-space/edit/image-edit-faint.png" />
                                </div>
                            </div>
                        </div>
                        <div>
                            <div class="input-label">
                                Location
                                <div class="sub-text">Update your reigion</div>
                                <div class="sub-text">Leave blank to be a remote based user</div>
                            </div>
                            <div style="width:400px; margin-left:20px;">
                                <Location :location="personalSettings?.profile_data?.location"/>
                            </div>
                        </div>
                        
                        <div style="float:left; max-width:600px; position:relative" class="option-action-space-block">
                            
                            <div class="faint" v-if="completeSave">Changes Saved Successfully</div>
                            <div @click="saveProfileChanges" class="save-button">Save Changes</div>
                        </div>
                        <div style="height:200px"></div>
                    </div>
                    <div v-else-if="configureMode === 'Account'" >
                        
                        <div>
                            <div class="option-label" style="width:100%">
                                Manage Subscription
                            </div>
                            <div class="option-action-space-block">
                                <div class="subscritption-text">Currnet subscription: <b>{{ personalSettings.Premium }}</b></div>
                                    <div v-if="personalSettings.Premium === 'free'">
                                        <div @click="subscribe" class="subscribe-button">
                                            Purcahse Subscription
                                        </div>
                                    </div>
                                    <div v-else-if="personalSettings.Premium === 'marked for deletion'">
                                        <div class="subscritption-text">
                                            <span>Your subscription will end on: <b>{{ dayjs(personalSettings.subscription_end_date).format('ddd, MMM DD, YYYY') }}</b> </span>
                                        </div>
                                        <div @click="resubscribe" class="subscribe-button">
                                            Resubscribe
                                        </div>
                                    </div>
                                    <div v-else>
                                        <div class="subscritption-text">
                                            <span>Your subscription will renew on: <b>{{ dayjs(personalSettings.subscription_end_date).format('ddd, MMM DD, YYYY') }}</b> </span>
                                        </div>
                                        <div class="subscritption-text">Subscription cost: <b>$2.00/month</b></div>
                                        <div @click="cancelSubscription" class="subscribe-button">
                                            Cancel Subscription
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                        <div class="option-label" @click="deleteAccount">Danger Zone</div>
                        <div class="option-action-space-block">
                            <div @click="deleteAccountRender=!deleteAccountRender" class="delete-room-button">Delete Account</div>
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
@keyframes slideIn {
    from {
        transform: translateX(-100%);
    }
    to {
        transform: translateX(0);
    }
}

.configure-mobile-side-bar{
    display: block;
    position: absolute;
    left: 0;
    top: 0;
    padding-top: 0px;
    padding-left: 0px;
    height: calc(100% - 0px);
    font-size: 14px;
    width: 100vw;
    animation: slideIn ease 0.3s;
    box-shadow: 5px 5px 15px 5px #1a1a1a;
    background: #d1d1d100;
    overflow-y: auto;
    overflow-x: hidden;

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

.subscribe-button{
    font-family: Arial, Helvetica, sans-serif;
    font-size: 14px;
    color: rgb(255, 255, 255);
    background-color: rgb(0, 0, 0);
    padding: 10px;
    width: fit-content;
    display:block;
    position: relative;
    margin-left:20px;
    margin-top:15px;
}
.subscribe-button:hover{
    background-color: rgb(8, 164, 255);
    transition: all 0.3s ease;
    cursor: pointer;
}
.subscritption-text{
    font-family: Arial, Helvetica, sans-serif;
    font-size: 14px;
    color: rgb(0, 0, 0);
    margin-bottom: 10px;
    text-align: left;
    width:fit-content;
    padding-left:20px;
}
.menu{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: white;
    padding: 30px;
    border-radius: 10px;
    z-index: 1000;
}
.popup-background{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 999;
}
.faint{
    position: absolute;
    right: 0;
    margin-top: -30px;
    background:black;
    color: white;
    font-family: Arial, Helvetica, sans-serif;
    padding:10px;
    border-radius: 10px;
    box-shadow: 0px 5px 10px 5px #00000070;
    animation: fadeinout 6s ease-in-out;
    
}

@keyframes fadeinout {
    0% { opacity: 0; }
    10% { opacity: 1; }
    90% { opacity: 1; }
    100% { opacity: 0; }
}
.image{
    width:150px;
    height:150px;

}
.image-space {
    outline: auto;
    display: flex;
    justify-content: left; 
    align-items: left;
    width: 25vw;
    max-width: 150px;
    aspect-ratio: 1 / 1;
    background-color: transparent;
    overflow: hidden;
    position: relative;
    z-index: 6;
    margin-top:20px;
    margin-left:20px;
    border-radius: 50%;
}
.image-edit-faint {
    outline: auto;
    width: 25vw;
    max-width: 150px;
    max-height: 150px;
    position: absolute;
    z-index: 5;
    opacity: 0;
    color:rgba(255, 255, 255, 0.205);
    background-color: rgb(26, 26, 26);
    padding: 100px;
    z-index: 0;
    transition: background-color 0.3s, opacity 0.3s;
}
.image-edit-faint:hover {
    opacity: 1.0;
    cursor: pointer;
    background-color: rgba(0, 0, 0, 0.842);
}
.left-block{
    float:left;
    z-index:100;
}
.Base {
  display: block;
  position: absolute;
  top: 0;
  left: 0;
  width: calc(100vw);
  margin: auto;
  height: 60px;
  background-color: rgba(0, 0, 0, 0.856);
  /*background-image: linear-gradient(45deg, rgb(143, 219, 249), rgb(0, 183, 255)); */

}
.container {
    position:relative;
    margin: auto;
    background-color: rgba(85, 19, 19, 0.699);
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
    width: 40px;
    height: 40px;
    margin-top: 10px;
    margin-left:20px;
    background: rgba(0, 0, 255, 0);
    filter:saturate(0%) invert(1) contrast(500%);
    z-index: 100;
}
.title{
  position:absolute;
  display: inline-block;
  font-family: fantasy;
  font-size: 30px;
  color: rgb(232, 232, 232);
  margin-left: 15px;
  margin-top:15px;
}

.right-portion{
  display: inline-block;
  margin-left: auto;
  float:right;
  margin-top:20px;
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
    font-size:16px;
    font-family: fantasy;
    padding:5px 10px;
    border-radius:5px;
    color:white;
    margin:5px;
}
.rename-input{
    display: block;
    padding: 10px;
    
    margin-left: 18px;
    width: calc(100% - 100px);
    max-width: 400px;
    background-color: rgba(80, 80, 80, 0.123);
    outline: none;
    border: none;
    border-radius: 5px;
    color: rgb(5, 5, 5);
    font-size: 14px;
    font-family: fantasy;
}
.input-label{
    font-family: fantasy;
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
    background-color: #00000040;
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
    background-color:  #00000040;
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
    right:0px;
    height: 100%;
    background-color: rgba(255, 255, 255, 0.623);
    overflow-y: auto;
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
    margin-left:20px;
    transition: all 0.3s ease;
}
.delete-room-button:hover{
    background-color: rgb(255, 0, 0);
    color:white;
    cursor: pointer;
}
.save-button{
    display: inline-block;
    width:fit-content;
    padding:10px;
    border-radius: 5px;
    margin-top: 20px;
    border: 2px solid rgb(0, 0, 0);
    font-family: fantasy;
    float:right;
    margin-left:20px;
    transition: all 0.3s ease;
    background-color: rgba(0, 0, 0, 0);
}
.save-button:hover{
    background-color: rgb(0, 0, 0);
    color:white;
    cursor: pointer;
}
.delete-button{
    display: block;
    width:fit-content;
    padding:10px;
    border-radius: 5px;
    margin-top: 20px;
    border: 2px solid rgb(0, 0, 0);
    font-family: fantasy;
    float:right;
    margin-left:20px;
    transition: all 0.3s ease;
    background-color: rgba(0, 0, 0, 0);
}
.delete-button:hover{
    background-color: rgb(0, 0, 0);
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
    width:calc(100%);
    height:auto;
    background-color: rgba(129, 83, 83, 0);
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
  transition: .4s;
  
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.8);
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
    height: calc(100% - 40px);
    width: calc(100% - 80px);
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
    background-color: rgb(255, 255, 255);
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
    height:calc(100vh - 60px);
    overflow: auto;
    position: absolute;
    top: 60px;
    left: 0;
    background-color: rgb(255, 255, 255);
    width: calc(100vw);
    z-index: -2;
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