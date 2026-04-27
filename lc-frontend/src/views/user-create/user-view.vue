<script setup>
    import Header from '@/components/header.vue';
    import {onMounted, ref, nextTick} from 'vue';
    import axios from 'axios';
    import { AccountLocal } from '@/lib/appwrite';
    import dayjs from 'dayjs';
    import { useRoute, useRouter } from 'vue-router';
    import { createClient } from '@supabase/supabase-js';

    const supabase = createClient(import.meta.env.VITE_SUPABASE_URL, import.meta.env.VITE_SUPABASE_ANON_KEY);

    const route = useRoute();
    const router = useRouter();
    //write a lookingFor with <100 characters
    let activeTime = ref("Now");
    let edit = ref(false);
    let tempColor = ref("#FFDDC1");
    let changeInduced = ref(false);
    let dummyProfile = ref(null);
    let friend = ref(false);
    let profileId = ref('');
    let profileData = ref(
        {
            looking_for: "",
            user_image: "",
            location: "",
            skills: [],
            links: [],
            user_tag: "",
            display_name: "",
            bio: "",
            bg_color: "rgb(64,0,183)",
            text_color: "white",
            skills: []
        }
    );
    let user = ref(null);
    let adminRights = ref(false);
    let active = ref(false);
    onMounted(async () => {
        let profileUserTag = route.params.usertag;
        profileData.value = await axios.get(`${import.meta.env.VITE_APP_API_URL}users/search/search_by_usertag/${profileUserTag}`);
        profileId.value = profileData.value.data.profile[0].user_id;
        activeTime.value = formatActiveTime(profileData.value.data.profile[0].time_last_active);
        active.value = profileData.value.data.profile[0].active;
        try{
            user.value = await AccountLocal.get();
            if(user.value.$id === profileData.value.data.profile[0].user_id){
                adminRights.value = true;
                active.value = true;
            }
            let friendResponse = await axios.get(`${import.meta.env.VITE_APP_API_URL}users/search/is_friends/${user.value.$id}/${profileId.value}`);
            friend.value = friendResponse.data.is_friend;
        }catch{
            user.value = null;
        }
        let channel = await supabase
            .channel('messages')
            .on(
                'postgres_changes',
                {
                event: 'UPDATE',
                schema: 'public',
                table: 'users',
                filter: `user_tag=eq.${profileUserTag}`
                },
                (payload) => {
                    if(payload.new.is_active !== active.value){
                        active.value = payload.new.is_active;
                        if(active.value){
                            activeTime.value = "Now";
                        } else {
                            activeTime.value = formatActiveTime(payload.new.time_last_active);
                        }
                    }
                    
                }
            )
            .subscribe();
        
        

        profileData.value = {
            looking_for: profileData.value.data.profile[0].looking_for,
            user_image: profileData.value.data.profile[0].profile_data.UserImage,
            location: profileData.value.data.profile[0].profile_data.location,
            skills: profileData.value.data.profile[0].skills? profileData.value.data.profile[0].skills : [],
            user_tag: profileData.value.data.profile[0].user_tag,
            display_name: profileData.value.data.profile[0].profile_data.display_name,
            links: profileData.value.data.profile[0].profile_data.links? profileData.value.data.profile[0].profile_data.links : [],
            bio: profileData.value.data.profile[0].profile_data.bio? profileData.value.data.profile[0].profile_data.bio : null,
            bg_color: profileData.value.data.profile[0].profile_data.bg_color ? profileData.value.data.profile[0].profile_data.bg_color : "rgb(64,0,183)",
            text_color: profileData.value.data.profile[0].profile_data.text_color ? profileData.value.data.profile[0].profile_data.text_color : "white"
        }
        
        const now = dayjs();
        backgroundAdjust();
        
        // get last active time
        // const lastActive = dayjs(activeTime);
        // // if last active time is within a month, show relative time
        // if (now.diff(lastActive, 'month') < 1) {
        //     activeTime = lastActive.fromNow();
        // }
        
        checkMobileView();
        window.addEventListener("resize", backgroundAdjust);
        window.addEventListener("resize", checkMobileView);

        console.log(friend.value);

    });
    // if date time exceeds a month, show exact date time
    
    function formatActiveTime(time){
        const now = dayjs();
        let returnTime = "";
        if(now.diff(dayjs(time), 'minutes') < 60){
            returnTime = now.diff(dayjs(time), 'minutes') + " minutes ago";
        } else if (now.diff(dayjs(time), 'hours') < 24) {
            returnTime = now.diff(dayjs(time), 'hours') + " hours ago";

        } else if (now.diff(dayjs(time), 'days') < 30) {
            returnTime = now.diff(dayjs(time), 'days') + " days ago";

        } else {
            returnTime = dayjs(time).format('MMMM D, YYYY h:mm A');
        }
        console.log(returnTime);
        return returnTime;
    }

    let mobileView = ref(false);
    function checkMobileView(){
        mobileView.value = window.innerWidth <= 968;
        // if(mobileView.value){
            
        // } else {
            
        // }
    }

    function backgroundAdjust(){
        // let physicalHeight = document.querySelector(".info-container").offsetHeight + 200;
        // document.getElementById("background").style.height = "calc(100vh - 60px)";
        // let viewportHeight = document.getElementById("background").offsetHeight;
        // if(physicalHeight > viewportHeight){
        //     document.getElementById("background").style.height = physicalHeight + "px";
        // }
        // console.log(physicalHeight, viewportHeight);
    }
    function addSkill(){
        const newSkill = event.target.previousElementSibling.value.trim();
        if(newSkill && !dummyProfile.value.skills.includes(newSkill)){
            dummyProfile.value.skills.push(newSkill);
            event.target.previousElementSibling.value = "";
        }
    }
    function syncContent(){
        const editor = document.getElementById('bio-editor');
        if(editor){
            const htmlContent = editor.innerHTML;
            console.log("Synced content:", htmlContent);
            // Here you can also update the corresponding question's questionHTML with the new content
        }
    }
    function bioEditToggled(){
        if(dummyProfile.value.bio){
            dummyProfile.value.bio = null;
        } else {
            dummyProfile.value.bio = "<div>write your bio here...</div>";
        }
    }
    function linkEditToggled(){
        if(dummyProfile.value.links && dummyProfile.value.links.length > 0){
            dummyProfile.value.links = null;
        } else {
            dummyProfile.value.links = [["",""]];
        }
    }
    async function saveUser(){
        profileData.value = JSON.parse(JSON.stringify(dummyProfile.value));
        if(dummyProfile.value.bio){
            profileData.value.bio = document.getElementById("bio-editor").innerHTML;
        }
        await axios.post(`${import.meta.env.VITE_APP_API_URL}users/update_page/${user.value.$id}`, profileData.value);
        changeInduced.value = true;
        await nextTick();
        let changeInducedText = document.querySelector(".changes-saved");
        if(changeInducedText){
            changeInducedText.style.opacity = 1;
            setTimeout(() => {
                if(changeInducedText){
                    changeInducedText.style.opacity = 0;
                }
            }, 3000);
        }
    }
    function closeEdit(){
        edit.value = false;
        changeInduced.value = false;
    }
    async function openEdit(){
        dummyProfile.value = JSON.parse(JSON.stringify(profileData.value));
        await nextTick();
        edit.value = true;
        await nextTick();
        backgroundAdjust();
    }
    function openWindow(url){
        window.open(url, '_blank');
    }

    function produceLinkImage(link){
        if(link[1].includes("canva") || link[0].toLowerCase().trim().includes("resume")){
            return new URL("@/assets/profile-page/link-icons/resume.jpg", import.meta.url);
        }else if(link[1].includes("linkedin")){
            return new URL("@/assets/profile-page/link-icons/linkedin.webp", import.meta.url);
        } else if(link[1].includes("github")){
            return new URL("@/assets/profile-page/link-icons/github.svg", import.meta.url);;
        } else {
            return new URL("@/assets/profile-page/link-icons/blocks.png", import.meta.url);;
        }
    }

    let toolBarSelects = ref([false, false,false]);
    function toggleToolBarOption(index){
        toolBarSelects.value[index] = !toolBarSelects.value[index];
        if(index === 0){
            document.execCommand('bold');
        } else if(index === 1){
            document.execCommand('italic');
        } else if(index === 2){
            document.execCommand('underline');
        }
    }
    let fontSize = ref(3);
    function adjustBioEditorFontSize(){
        if(fontSize.isNaN()){
            fontSize.value = 3;
        }
        fontSize.value = Math.max(1, Math.min(7, fontSize.value));

    }

    async function sendMessage(){
        router.push("/messages?" + new URLSearchParams({ usertag: profileData.value.user_tag, new: true, friends: friend.value }). toString());
    }

    async function changeFriendStatus(){
        friend.value = !friend.value;
        if(friend.value){
            await axios.post(`${import.meta.env.VITE_APP_API_URL}users/add_friend/${user.value.$id}/${profileId.value}`, { private_key: import.meta.env.VITE_API_PRIVATE_KEY, friend_usertag: profileData.value.user_tag, friend_image: profileData.value.user_image, friend_display_name: profileData.value.display_name });
        } else {
            await axios.post(`${import.meta.env.VITE_APP_API_URL}users/remove_friend/${user.value.$id}/${profileId.value}`, { private_key: import.meta.env.VITE_API_PRIVATE_KEY, friend_usertag: profileData.value.user_tag });
        }
    }

function goToProjects(){
    router.push("/user-projects/" + profileData.value.user_tag);
}

function goToFriends(){
    router.push("/friends/" + profileData.value.user_tag);
}

</script>

<template>
    <Header/>
        <!-- <div>
            <div style="display:inline-block; width:15px;" ></div>
            <span class="prof-icon selected">Main</span>
            <span class="prof-icon">Past Projects</span>
        </div> -->
    <div class="background" id="background" :style="!edit ? {background: profileData.bg_color, color: profileData.text_color} : {background: dummyProfile.bg_color, color: dummyProfile.text_color}">
    <div v-if="!mobileView" class="full-container" id="full-container">
            
            <div class="info-container" v-if="!edit">
                <div class="top-button">
                    <span @click="goToProjects" class="header-button">Projects</span>
                    <span @click="goToFriends" class="header-button">Friends</span>
                </div>
                <div class="bio-block">
                    <!-- <div class="looking-for-text">
                        <b>Im looking for: </b> {{ profilePageInfo.lookingFor }}
                        <div style="height:20px;"></div>
                    </div> -->
                    
                    <div style="margin-bottom:20px; font-size:16px">
                        <div v-html="profileData.bio"></div>
                    </div>
                    
                    <div  class="edit-button" @click="openEdit" v-if="adminRights"></div>
                    <div class="link-box" v-for="link in profileData.links" :key="link.url" @click="openWindow(link[1])">
                        <img :src="produceLinkImage(link)" style="width:100%; height:100%; object-fit:cover;"/>
                        <div class="link-label" style="color:black">{{ link[0] }}</div>
                    </div>
                    <div class="skill-block">
                        <div class="skill-title"><b>Skills:</b></div>
                        <div v-for="skill in profileData.skills" :key="skill" class="skill">
                            {{ skill }}
                        </div>
                    </div>

                </div>
                <!-- <div>
                    <h2>Pinned Projects:</h2>
                </div> -->
            </div>
            <div v-else class="info-container" style="margin-top:40px">
                <div class="edit-section">
                    <!-- <div class="block">
                        <div class="edit-text">Im looking for...</div>
                        <textarea id="looking-for-text-edit" class="edit-question">{{ dummyProfile.lookingFor }}</textarea>
                    </div> -->
                    <div class="block">
                        <div class="edit-text"> Add a bio </div>
                        <div class="toggle">
                            <div class="toggle">
                                <input @click="bioEditToggled" type="checkbox" id="toggle" class="toggle-slider-input" :checked="dummyProfile.bio"/>
                                <label for="toggle" class="toggle-slider"></label>
                            </div>
                        </div>
                        <div v-if="dummyProfile.bio" class="bio-editor">
                            <div class="freeform-input">
                                <div class="toolbar">
                                    <img src="@/assets/founder-space/edit/job-edit/freeform-text-editor/bold.png" :class="toolBarSelects[0] ? 'selected-button' : 'button'" @click="toggleToolBarOption(0)" />
                                    <img src="@/assets/founder-space/edit/job-edit/freeform-text-editor/italics.webp" :class="toolBarSelects[1] ? 'selected-button' : 'button'" @click="toggleToolBarOption(1)" />
                                    <img src="@/assets/founder-space/edit/job-edit/freeform-text-editor/underline.png" :class="toolBarSelects[2] ? 'selected-button' : 'button'" @click="toggleToolBarOption(2)" />
                                    <span class="seperator">|</span>
                                    <input type="color" class="color-picker" onchange="document.execCommand('foreColor', false, this.value)" />
                                    <input type="text" class="font-size-input" v-model="fontSize" onchange='document.execCommand("fontSize", false, this.value)' v-on:change="adjustBioEditorFontSize" /><span class="px-text">px</span>
                                </div>
                                <div class="editor" id="bio-editor" contenteditable="true" @click="syncContent(index, $event)" v-html="dummyProfile.bio"></div>
                                <div class="sub-text">Drag and drop to add an image</div>
                            </div>
                        </div>
                    </div>
                    <div class="block">
                        <div class="edit-text"> Add links </div>
                        <div class="toggle">
                            <div class="toggle">
                                <input @click="linkEditToggled" type="checkbox" class="toggle-slider-input" id="toggle-1" :checked="dummyProfile.links && dummyProfile.links.length > 0"/>
                                <label for="toggle-1" class="toggle-slider"></label>
                            </div>
                        </div>
                        <div v-if="dummyProfile.links && dummyProfile.links.length > 0" class="link-list">
                            <div v-for="(link, index) in dummyProfile.links" :key="index" class="link-input-box">
                                <input v-model="link[0]" class="link-label-input" style="color:white" placeholder="Link Label"/>
                                <input v-model="link[1]" class="link-url-input" style="color:white" placeholder="Link URL"/>
                                <div @click="dummyProfile.links.splice(index, 1)" class="remove-link">x</div>
                            </div>
                            <div @click="dummyProfile.links.push(['', ''])" class="add-link-button">Add Link</div>
                        </div>
                    </div>
                    <div class="block">
                        <div class="edit-text">Skills</div>
                        <input class="edit-input"/>
                        <div @click="addSkill" class="add-skill-button">+</div>
                        <div class="skill-block">
                            <div v-for="skill in dummyProfile.skills" :key="skill" class="skill">
                                {{ skill }} <span style="font-size:18px; color:red;" @click="dummyProfile.skills.splice(dummyProfile.skills.indexOf(skill), 1)">x</span>
                            </div>
                        </div>
                    </div>
                    <span class="block" style="width:130px;display:inline-block; vertical-align:top; border-left: solid rgb(0, 0, 0) 1px; padding-left:20px; margin-right:20px; border-right: solid rgb(0, 0, 0) 1px;">
                        <div style="margin:auto; text-align:left; position:relative;">
                            Background Color
                        </div>
                        <div style="height:10px;"></div>
                        <div style="width:70px; height:30px; border-radius:5px; margin:auto;">
                            <input  type="color" v-model="dummyProfile.bg_color" />
                        </div>
                    </span>
                    <span class="block" style="width:100px; display:inline-block; vertical-align:top; border-left: solid rgb(0, 0, 0) 1px; padding-left:20px; padding-right:0px; border-right: solid rgb(0, 0, 0) 1px;">
                        <div style="margin:auto; text-align:center; text-align:left; position:relative;">
                            Text Color
                        </div>
                        <div style="height:10px;"></div>
                        <input type="color" style="margin-left:2.5px" v-model="dummyProfile.text_color" />
                    </span>
                    <div class="sub-text">
                        Please avoid color combinations that are difficult to read
                    </div>
                    <div style="height:60px;">
                        <div v-if="changeInduced" class="changes-saved">Changes saved successfully</div>
                        <br>
                        <div @click="saveUser" class="save-button">Save</div>
                        <div @click="closeEdit" class="close-edit">Return</div>
                    </div>
                </div>
            </div> 
        <div class="right-aside">
            <div style="height:50px"></div>
            <div class="profile-image-block">
                <div class="profile-image" :style="{ backgroundImage: `url(${profileData.user_image})`}"></div>
            </div>
            
            
            <!-- <div class="setting-block">
                <div class="settings"></div>
            </div> -->
            <div class="name">{{ profileData.display_name }}</div>
            <div class="tag">@{{ profileData.user_tag }}</div>
            <div @click="sendMessage" class="message-button">
                Send Message
            </div>
            <div style="height: 10px;"></div>
            <div @click="changeFriendStatus" v-if="friend" class="friend-button" style="background: rgb(70, 70, 255);">
                Friends
            </div>
            <div @click="changeFriendStatus" v-else class="friend-button" >
                Add Friend
            </div>
            <div v-if="active" class="time" style="color: green; font-weight:bold;"><span>● </span><b> Active</b></div>
            <div v-else class="time"><span style="color: gray;">● </span><b style="color:white;">Last Active: </b><i style="color:white;">{{ formatActiveTime(profileData.active_time) }}</i></div>
            <div style="width:90%; margin:auto; margin-top:10px; margin-bottom:10px; font-family: fantasy; font-size:15px;"><b>Im looking for: </b>{{ profileData.looking_for }}</div>
            <div class='location' v-if="profileData.location != ''">
                <!-- <img src='@/assets/main-page/location.png' class="location-icon"/> -->
                📍{{ profileData.location }}
            </div>
            <div v-else class="location">
                <img src="https://cdn-icons-png.flaticon.com/512/3759/3759392.png" style="width:15px; height:15px; margin-bottom:-2.5px; display:inline-block;"> Remote
            </div>
        </div> 
    </div>
    <div v-else class="mobile-info-container" id="full-container">
            
        <div class="mobile-right-aside">
            <div class="profile-image-block">
                <div class="profile-image" :style="{ backgroundImage: `url(${profileData.user_image})`}"></div>
            </div>
            
            
            <!-- <div class="setting-block">
                <div class="settings"></div>
            </div> -->
            <div class="name">{{ profileData.display_name }}</div>
            <div class="tag">@{{ profileData.user_tag }}</div>
            <div class="message-button" @click="sendMessage">
                Send Message
            </div>
            <div style="height: 10px;"></div>
            <div @click="changeFriendStatus" v-if="friend" class="friend-button" style="background: rgb(70, 70, 255);">
                Friends
            </div>
            <div @click="changeFriendStatus" v-else class="friend-button" >
                Add Friend
            </div>
            <div v-if="activeTime === 'Now'" class="mobile-time" style="color: green; font-weight:bold;"><span>● </span><b> Active</b></div>
            <div v-else class="mobile-time"><span style="color: gray;">● </span><b style="color:white;">Last Active: </b><i style="color:white;">{{activeTime}}</i></div>
            <div style="width:90%; margin:auto; margin-top:10px; margin-bottom:10px; font-family: fantasy; font-size:15px;"><b>Im looking for: </b>{{ profileData.looking_for }}</div>
            <div class='location' v-if="profileData.location != ''">
                📍{{ profileData.location }}
            </div>
            <div v-else class="location">
                <img src="https://cdn-icons-png.flaticon.com/512/3759/3759392.png" style="width:15px; height:15px; margin-bottom:-2.5px; display:inline-block;"> Remote
            </div>
        </div> 
        <div class="mobule-info-container" v-if="!edit">
                <div style="margin-top:-50px; margin-bottom:50px;">
                    <span @click="goToProjects" class="header-button">Projects</span>
                    <span @click="goToFriends" class="header-button">Friends</span>
                </div>
                <div class="bio-block">
                    <!-- <div class="looking-for-text">
                        <b>Im looking for: </b> {{ profilePageInfo.lookingFor }}
                        <div style="height:20px;"></div>
                    </div> -->
                    
                    <div style="margin-bottom:20px; font-size:16px">
                        <div v-html="profileData.bio"></div>
                    </div>
                    
                    <div  class="mobile-edit-button" @click="openEdit" v-if="adminRights"></div>
                    <div class="link-box" v-for="link in profileData.links" :key="link.url" @click="openWindow(link[1])">
                        <img :src="produceLinkImage(link)" style="width:100%; height:100%; object-fit:cover;"/>
                        <div class="link-label" style="color:black">{{ link[0] }}</div>
                    </div>
                    <div class="skill-block">
                        <div class="skill-title"><b>Skills:</b></div>
                        <div v-for="skill in profileData.skills" :key="skill" class="skill">
                            {{ skill }}
                        </div>
                    </div>

                </div>
                <!-- <div>
                    <h2>Pinned Projects:</h2>
                </div> -->
            </div>
            <div v-else class="mobule-info-container" >
                <div class="edit-section">
                    <!-- <div class="block">
                        <div class="edit-text">Im looking for...</div>
                        <textarea id="looking-for-text-edit" class="edit-question">{{ dummyProfile.lookingFor }}</textarea>
                    </div> -->
                    <div class="block">
                        <div class="edit-text"> Add a bio </div>
                        <div class="toggle">
                            <div class="toggle">
                                <input @click="bioEditToggled" type="checkbox" id="toggle" class="toggle-slider-input" :checked="dummyProfile.bio"/>
                                <label for="toggle" class="toggle-slider"></label>
                            </div>
                        </div>
                        <div v-if="dummyProfile.bio" class="bio-editor">
                            <div class="freeform-input">
                                <div class="toolbar">
                                    <img src="@/assets/founder-space/edit/job-edit/freeform-text-editor/bold.png" :class="toolBarSelects[0] ? 'selected-button' : 'button'" @click="toggleToolBarOption(0)" />
                                    <img src="@/assets/founder-space/edit/job-edit/freeform-text-editor/italics.webp" :class="toolBarSelects[1] ? 'selected-button' : 'button'" @click="toggleToolBarOption(1)" />
                                    <img src="@/assets/founder-space/edit/job-edit/freeform-text-editor/underline.png" :class="toolBarSelects[2] ? 'selected-button' : 'button'" @click="toggleToolBarOption(2)" />
                                    <span class="seperator">|</span>
                                    <input type="color" class="color-picker" onchange="document.execCommand('foreColor', false, this.value)" />
                                    <input type="text" class="font-size-input" v-model="fontSize" onchange='document.execCommand("fontSize", false, this.value)' v-on:change="adjustBioEditorFontSize" /><span class="px-text">px</span>
                                </div>
                                <div class="editor" id="bio-editor" contenteditable="true" @click="syncContent(index, $event)" v-html="dummyProfile.bio"></div>
                                <div class="sub-text">Drag and drop to add an image</div>
                            </div>
                        </div>
                    </div>
                    <div class="block">
                        <div class="edit-text"> Add links </div>
                        <div class="toggle">
                            <div class="toggle">
                                <input @click="linkEditToggled" type="checkbox" class="toggle-slider-input" id="toggle-1" :checked="dummyProfile.links && dummyProfile.links.length > 0"/>
                                <label for="toggle-1" class="toggle-slider"></label>
                            </div>
                        </div>
                        <div v-if="dummyProfile.links && dummyProfile.links.length > 0" class="link-list">
                            <div v-for="(link, index) in dummyProfile.links" :key="index" class="link-input-box">
                                <input v-model="link[0]" class="link-label-input" style="color:white" placeholder="Link Label"/>
                                <input v-model="link[1]" class="link-url-input" style="color:white" placeholder="Link URL"/>
                                <div @click="dummyProfile.links.splice(index, 1)" class="remove-link">x</div>
                            </div>
                            <div @click="dummyProfile.links.push(['', ''])" class="add-link-button">Add Link</div>
                        </div>
                    </div>
                    <div class="block">
                        <div class="edit-text">Skills</div>
                        <input class="edit-input"/>
                        <div @click="addSkill" class="add-skill-button">+</div>
                        <div class="skill-block">
                            <div v-for="skill in dummyProfile.skills" :key="skill" class="skill">
                                {{ skill }} <span style="font-size:18px; color:red;" @click="dummyProfile.skills.splice(dummyProfile.skills.indexOf(skill), 1)">x</span>
                            </div>
                        </div>
                    </div>
                    <span class="block" style="width:130px;display:inline-block; vertical-align:top; border-left: solid rgb(0, 0, 0) 1px; padding-left:20px; margin-right:20px; border-right: solid rgb(0, 0, 0) 1px;">
                        <div style="margin:auto; text-align:left; position:relative;">
                            Background Color
                        </div>
                        <div style="height:10px;"></div>
                        <div style="width:70px; height:30px; border-radius:5px; margin:auto;">
                            <input  type="color" v-model="dummyProfile.bg_color" />
                        </div>
                    </span>
                    <span class="block" style="width:100px; display:inline-block; vertical-align:top; border-left: solid rgb(0, 0, 0) 1px; padding-left:20px; padding-right:0px; border-right: solid rgb(0, 0, 0) 1px;">
                        <div style="margin:auto; text-align:center; text-align:left; position:relative;">
                            Text Color
                        </div>
                        <div style="height:10px;"></div>
                        <input type="color" style="margin-left:2.5px" v-model="dummyProfile.text_color" />
                    </span>
                    <div class="sub-text">
                        Please avoid color combinations that are difficult to read
                    </div>
                    <div style="height:60px;">
                        <div v-if="changeInduced" class="changes-saved">Changes saved successfully</div>
                        <br>
                        <div @click="saveUser" class="save-button">Save</div>
                        <div @click="closeEdit" class="close-edit">Return</div>
                    </div>
                </div>
            </div> 
            <div style="height:100px;"></div>
    </div>
</div>

</template>




<style scoped>
.header-button{
    padding:10px 20px;
    margin:10px;
    background:rgba(0, 0, 0, 0.432);
    color:white;
    font-family: Arial, Helvetica, sans-serif;
    font-size:16px;
    border-radius:5px;
    cursor: pointer;
    display:inline-block;
}
.header-button:hover{
    background:rgba(0, 0, 0, 0.8);
    color:white;
    transition: all 0.3s ease;
    transform: scale(1.05);
}
.header-button:active{
    transform: scale(1);
    transition: all 0.1s ease;
}
.top-button{
    width:calc(100% - 600px);
    height:40px;
    background:rgba(0, 0, 0, 0);
    color:white;
    font-family: fantasy;
    font-size:16px;
    border-radius:5px;
    cursor: pointer;
    position: absolute;
    top:90px;
    left: 60px;

}
.mobile-edit-button{
    position:absolute;
    top:-20px;
    right:20px;
    width:60px;
    height:60px;
    box-shadow: 0 0 10px rgb(255, 255, 255);
    font-size: 14px;
    font-family: fantasy;
    color:white;
    text-shadow: 0 0 2px white;
    border-radius: 10px;
    background-image: url("@/assets/profile-page/edit.png");
    filter:invert(1);
    background-size:cover;
    background-color: rgb(255, 255, 255);
    cursor: pointer;
}
.mobile-info-container{
    padding:20px;
    overflow-x: hidden;
    position: absolute;
    width:95%;
    top:0px;
    left:0;
    height:calc(100vh - 100px);
}
.mobile-time{
    font-size: 12px;
    font-family: fantasy;
    width:calc(95% - 20px);
    margin-top:10px;
    margin-left:20px;
    margin-bottom:-10px;
    background-color: black;
    padding:10px;
    width:fit-content;
    border-radius:5px;
    position: absolute;
    top:370px;
    right:40px;
}
.mobile-right-aside{
    width:100%;
    background:rgba(0, 0, 0, 0.082);
    margin-bottom:50px;
    padding-top:40px;
    margin-top:20px;
    padding-bottom:40px;
}
.mobule-info-container{
    padding:20px;
}

.setting-block:hover{
    transform: rotate(90deg);
    cursor: pointer;
}
.setting-block{
    width:30px;
    height:30px;
    background:white;
    padding:10px;
    transition: all 0.3s ease;
    background-image: url("@/assets/profile-page/gear.png");
    background-size:80%, 80%;
    background-position: center;
    background-repeat: no-repeat;
    border-radius: 50%;
    top:340px;
    right:110px;
    position:absolute;
}
.settings{
    width:30px;
    height:30px;
    background-size:cover;
    margin:auto;
    margin-top:20px;
    cursor: pointer;
}
.color-block{
    display:inline-block;
    margin-right: 20px;
}
.selected-button{
    background:rgb(255, 176, 130);
    color:white;
    width:20px;
    height:20px;
    color:white;
    font-size:20px;
    border: solid black 1px;
    line-height:30px;
    padding:5px;
    text-align:center;
    border-radius:5px;
    margin-right:10px;
    box-shadow: 0px 5px 5px 0px #000000;
    cursor: pointer;
}
.looking-for-sub{
    width:80%;
    margin:auto;
    font-family: fantasy;
    font-size:14px;
}
.background{
    position: absolute;
    top:60px;
    left:0;
    width:100%;
    height:calc(100vh - 60px);
    z-index: -2;
}
.changes-saved{
    color: rgb(255, 255, 255);
    font-weight: lighter;
    background: black;
    padding:20px;
    margin-left: 20px;
    margin-top:-10px;
    position:absolute;
    right:0;
    bottom: 50px;
    border-radius: 20px;
    animation: fadeinout 4s;
}

@keyframes fadeinout {
    0% {opacity: 0;}
    10% {opacity: 1;}
    76% {opacity: 1;}
    90% {opacity: 0;}
    100% {opacity: 0;}
}

.close-edit{
    width:70px;
    background:rgb(0, 0, 0);
    color:white;
    font-size:16px;
    font-family: fantasy;
    text-align:center;
    padding:10px;
    border-radius:5px;
    margin-top:10px;
    float:right;
    margin-right:20px;
}
.save-button{
    width:50px;
    background:rgb(255, 176, 130);
    color:white;
    font-size:16px;
    font-family: fantasy;
    text-align:center;
    padding:10px;
    border-radius:5px;
    margin-top:10px;
    float:right;
    margin-right:20px;
}
.save-button:hover{
    background:rgb(255, 109, 31);
    color:white;
    transition: all 0.3s ease;
    cursor: pointer;
}
.remove-link{
    width:20px;
    height:20px;
    background:rgb(0, 0, 0);
    color:white;
    font-size:14px;
    line-height:20px;
    text-align:center;
    padding: 2px;
    border-radius:50%;
    position:absolute;
    top:5px;
    right:5px;
    cursor: pointer;
}
.add-link-button{
    width:100%;
    background:rgba(0, 0, 0, 0.399);
    border:white solid 1px;
    color:white;
    font-size:16px;
    font-family: fantasy;
    text-align:center;
    padding:10px;
    border-radius:5px;
    margin-top:10px;
}
.add-link-button:hover{
    background:rgb(255, 176, 130);
    color:white;
    transition: all 0.3s ease;
    cursor: pointer;
}
.link-input-box{
    position: relative;
    background: rgba(0, 0, 0, 0.082);
    margin-top:10px;
    padding:10px;
    border-radius: 10px;
    width:100%;
}
.link-label-input{
    width:calc(50% - 15px);
    max-width:200px;
    font-size: 16px;
    font-family: fantasy;
    border:none;
    border-bottom: 1px solid rgb(0, 0, 0);
    background: rgba(0, 0, 0, 0);
    margin-right:10px;
    outline:none;
    display:block;
}
.link-url-input{
    width:calc(100% - 15px);
    margin-top:10px;
    outline:auto;
    font-size: 16px;
    font-family: fantasy;
    border:none;
    background: rgba(0, 0, 0, 0);
    display:block;
    margin-top:10px;
}
.block{
    border-radius: 20px;
    padding: 20px;
    margin-bottom:20px;
}

.px-text{
    font-size: 16px;
    font-family: fantasy;
    position:relative;
    margin-left: 10px;
    top:-8px;
   /* color:rgb(0, 0, 0);*/


}
.sub-text{
    font-size: 12px;
    font-family: fantasy;
    color: rgb(0, 0, 0, 0.5);
    margin-top: 5px;
}
.font-size-input{
    width:20px;
    height:20px;
    padding:2px;
    border:solid rgb(0, 0, 0) 1px;
    display:inline-block;
    margin-left:10px;
    margin-bottom: -10px;
    transform: translateY(-8px);
}
.color-picker{
    width:30px;
    height:30px;
    padding:0px;
    display:inline-block;
}
.seperator{
    width:20px;
    height:20px;
    color:rgb(196, 196, 196);
    font-size:20px;
    line-height:0px;
    padding:5px;
    position:relative;
    top:-10px;
    border-radius:5px;
    margin-right:10px;
}
.freeform-input{
    width:100%;
    height: fit-content;
    border-radius: 100px;
    border-radius: 10px;
    overflow:hidden;
    margin-top: 10px;
    word-break: break-all;
    
}
.toolbar{
    position:relative;
    background:rgba(0, 0, 0, 0.37);
    white-space: wrap;
    padding:10px;
    padding-left: 20px;
    width:100%;
}
.editor{
    padding:10px;
    overflow-y:auto;
    overflow-x: hidden;
    height:300px;
    outline:none;
    width:calc(100% - 22px);
    background: rgba(0, 0, 0, 0);
    border: solid 1px rgb(0, 0, 0);
}
.button{
    width:20px;
    height:20px;
    color:white;
    font-size:20px;
    border: solid black 1px;
    line-height:30px;
    padding:5px;
    text-align:center;
    border-radius:5px;
    margin-right:10px;
    box-shadow: 0px 5px 5px 0px #000000;
    background: rgba(255, 255, 255, 0.315);
    cursor: pointer;
}

.toggle-slider-input {
  display: none;
}

.toggle {
  display: flex;
  width: 100%;
  max-width: 300px;
}
.toggle-slider {
  position: relative;
  width: 50px;
  height: 25px;
  background-color: #ccc;
  border-radius: 15px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
.toggle-slider::before {
  content: "";
  position: absolute;
  top: 2.5px;
  left: 2.5px;
  width: 20px;
  height: 20px;
  background-color: white;
  border-radius: 50%;
  transition: transform 0.3s ease;
}

#toggle:checked + .toggle-slider {
  background-color: rgb(255, 176, 130);
}
#toggle:checked + .toggle-slider::before {
  transform: translateX(25px);
}

.toggle-slider-input:checked + .toggle-slider {
  background-color: rgb(255, 176, 130);
}
.toggle-slider-input:checked + .toggle-slider::before {
  transform: translateX(25px);
}
.add-skill-button{
    display:inline-block;
    width:30px;
    height:30px;
    background:rgb(255, 176, 130);
    color:white;
    font-size:20px;
    line-height:30px;
    text-align:center;
    border-radius:5px;
    margin-left:10px;
    box-shadow: 0px 5px 5px 0px #000000;
    cursor: pointer;
}
.edit-input{
    width:calc(100% - 60px);
    max-width:300px;
    padding:10px;
    font-size: 16px;
    font-family: fantasy;
    border:none;
    border-radius: 10px;
    background: rgba(0, 0, 0, 0.05);
}
.skill:hover{
    background: rgb(255, 176, 130);
    color:white;
    transition: all 0.3s ease;
    cursor: pointer;
}
.skill:active{
    background: rgb(255, 176, 130);
    color:white;
    transition: all 0.3s ease;
    cursor: pointer;
    transform: scale(0.95);
}
.skill{
    display:inline-block;
    box-shadow: 0px 5px 5px 0px #000000;
    padding:7px;
    margin-bottom:5px;
    margin-right:15px;
    border-radius:10px;
    font-size: 16px;
    font-family: fantasy;
}
.skill-block{
    width:100%;
    margin-top:10px;
    
}
.edit-section{
    width:100%;
    height:auto;
    border-radius: 20px;
    margin-top:-50px;
    margin-left:-20px;
    position: relative;
}
.block{
    border-radius: 20px;
    padding: 20px;
    margin-bottom:20px;
}
.edit-text{
    font-size: 16px;
    font-family: fantasy;
    margin-bottom: 10px;
}
.edit-question{
    width:100%;
    height:100px;
    margin-top:10px;
    font-size: 16px;
    font-family: fantasy;
    padding:10px;
    resize:none;
    max-width:400px;
    border:none;
    border-radius: 10px;
    background: rgba(0, 0, 0, 0.05);
}
.line{
    height:2px; 
    width:100%; 
    background:rgba(0, 0, 0, 0.68); 
    margin-top:20px;
}
.bio-block{
    position:relative;
    margin-top:0px;
}
.edit-button:hover{
    transform: scale(1.1);
    transition: all 0.3s ease;
    cursor: pointer;

}
.edit-button{

    position:absolute;
    top:-20px;
    right:-50px;
    width:40px;
    height:40px;
    box-shadow: 0 0 10px rgb(255, 255, 255);
    font-size: 14px;
    font-family: fantasy;
    color:white;
    text-shadow: 0 0 2px white;
    border-radius: 10px;
    background-image: url("@/assets/profile-page/edit.png");
    filter:invert(1);
    background-size:cover;
    background-color: rgb(255, 255, 255);

}
.location-icon{
    width: 10px;
    height: 10px;
    margin-right: -1px;
    margin-left: -1.5px;
    margin-bottom: -1.5px;
}
.location{
    font-size: 12px;
    font-family: fantasy;
    width:calc(95% - 20px);
    margin:auto;
    margin-top:15px;
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
.prof-icon:hover{
    filter: brightness(80%);
    cursor: pointer;
}
.prof-icon{
    font-size:14px;
    font-family: fantasy;
    position: relative;
    display:inline-block;
    color:white;
    margin:0px;
    margin-top: -1px;
    margin-bottom:15px;
    margin-right:10px;
    border-right: rgba(255, 255, 255, 0) 1px solid;
}
.selected{
    color:rgb(255, 187, 0) !important; /* Darker color */
    text-decoration-thickness: 3px; /* Thicker line */
    text-underline-offset: 5px;
}
.link-label{
  position: absolute; /* Positions relative to the nearest positioned ancestor (the parent) */
  bottom: 0px;
  background-color: rgba(255, 255, 255, 0.8);
  font-weight: bold;
  width:calc(100% - 10px);
  padding: 10px;
  font-size: 14px;
  box-shadow: 0px -5px 10px 0px #00000042;
  height:20px;

}
.link-box{
    position: relative; 
    display:inline-block;
    margin-right: 20px;
    font-size: 14px;
    font-family: fantasy;
    margin-bottom:10px;
    width:200px;
    height:110px;
    border-radius: 10px;
    box-shadow: 0px 5px 10px 0px #00000042;
    overflow:hidden;
}
.link-box:hover{
    transform: scale(1.05);
    transition: all 0.3s ease;
    box-shadow: 0px 10px 15px 0px #00000042;
    cursor: pointer;
}
.friend-button:hover{
    background:rgba(0, 0, 0, 0.158);
    color:white;
    transition: all 0.3s ease;
    cursor: pointer;
    
}
.friend-button:active{
    background:rgba(0, 0, 0, 0);
    color:white;
    transition: all 0.3s ease;
    cursor: pointer;
    transform: scale(0.95);
}
.friend-button{
    width:calc(95% - 40px);
    height:20px;
    margin:auto;
    background:rgba(0, 0, 0, 0.37);
    padding:10px;
    text-align:center;
    border-radius:5px;
    box-shadow: 0px 5px 5px 0px #000000;
    font-family:fantasy;
}
.skill-title{
    font-size: 16px;
    font-family: fantasy;
    margin-bottom:10px;
}
.looking-for-text{
    font-size: 16px;
    font-family: fantasy;
    margin-top:20px;
    width:100%;
}
.skill{
    display:inline-block;
    box-shadow: 0px 5px 5px 0px #000000;
    padding:7px;
    margin-bottom:5px;
    margin-right:15px;
    border-radius:10px;
    font-size: 16px;
    font-family: fantasy;
}
.skill-block{
    width:100%;
    margin-top:10px;
    
}
.tag{
    font-size:12px;
    font-family:fantasy;
    text-align:center;
    margin-bottom:10px;
}
.time{
    font-size: 12px;
    font-family: fantasy;
    width:calc(95% - 20px);
    margin-top:10px;
    margin-left:20px;
    margin-bottom:-10px;
    background-color: black;
    padding:10px;
    width:fit-content;
    border-radius:5px;
    position: absolute;
    top:350px;
    right:0;
}
.text{
    font-size:16px;
    font-family:fantasy;
    margin-top:10px;
}
.name{
    font-size:20px;
    font-family:fantasy;
    text-align:center;
    margin-top:10px;
}
.info-container{
    display:inline-block;
    width:calc(100% - 540px);
    height:calc(100%);
    margin-top:100px;
    padding:80px;
    font-family: fantasy;
    background: rgba(160, 233, 255, 0);
}
.message-button{
    width:calc(95% - 40px);
    height:20px;
    margin:auto;
    margin-top: 5px;
    background:rgba(255, 255, 255, 1);
    color:black;
    padding:10px;
    text-align:center;
    border-radius:5px;
    box-shadow: 0px 5px 5px 0px #000000;
    font-family:fantasy;
}
.message-button:hover{
    background:rgba(255, 255, 255, 0.8);
    color:black;
    transition: all 0.3s ease;
    cursor: pointer;
}
.message-button:active{
    background:rgba(255, 255, 255, 0.5);
    color:black;
    transition: all 0.3s ease;
    cursor: pointer;
    transform: scale(0.95);
}
.profile-image{
    width:auto;
    height:100%;
    vertical-align: middle;
    background-size: cover;
    background-position: center;
}
.profile-image-block{
    width:300px;
    height:300px;
    border-radius:50%;
    margin:auto;
    background: rgba(0, 0, 0, 0);
    margin-top:20px;
    margin-bottom:20px;
    overflow:hidden;
    
    border: solid rgba(0, 0, 0, 0.486) 5px;
}
.full-container{
    height:auto;
    display:block;
    position:absolute;
    top:0px;
    width:95vw;
    left:50%;
    transform: translateX(-50%);
    margin:auto;
    max-width:1300px;
    height:calc(100vh - 95px);
    overflow-y: auto;
    scrollbar-width: none;
    -ms-overflow-style: none;
}

.full-container::-webkit-scrollbar {
  display: none;
}
.right-aside{
    position:relative;
    display:inline-block;
    width:350px;
    margin-right: 20px;
    height:fit-content;
    padding-bottom:20px;
    overflow:hidden;
    vertical-align: top;
}

</style>