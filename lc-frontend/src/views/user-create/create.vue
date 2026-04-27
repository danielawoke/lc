<script setup>
// Google accounts still havent been tested for any of this database alignment business that I've created, I need to find a way to actually test and know if its working or not
// for new google account users. Also, I need to convert thier addresses to lon and lat with the google api in the backend
import { useRoute, useRouter } from 'vue-router'
import ImageEditorPopUp from '@/components/founder-space/interfaces/edit-cards/image-replace/pop-up.vue';
import { ref} from 'vue';
import { nextTick, watch } from 'vue';
import Location from '@/components/supporting-components/location-profile.vue'
import { onMounted } from 'vue';
import { AccountLocal } from "@/lib/appwrite";
import { supabase } from "@/lib/supabase";
import axios from 'axios';

const route = useRoute();
const apiUrl = import.meta.env.VITE_APP_API_URL;
const domain = import.meta.env.VITE_LAUNCHPAD_DOMAIN;
const router = useRouter()
function goToMain() {
    router.push('/');
}
const imageEditMode = ref(false);
const backDropClick = ref([false]);
const saveResults = ref([false, null]);

let imageChangeInfo = {
    blob: [null],
    url: [null]
};

let page = ref(-1);
let skills = ref([]);
let userId = ref(null);
let verfied = ref(0);
let error = ref("");
let userObject = ref(null);
let userTag = "";

let allInfo = ref({
    username: "",
    lookingFor: "",
    skills: [],
    profilePicture: null
});

let userInfo = ref({
    displayName: "",
    location: "",
    skills: [],
    lookingFor: "",
    image: null,
    searchCoordinates: null,
});

let loadingAnimationInterval = null;

function nextLoading(button) {
    const registerButton = button;
    registerButton.style = "filter: brightness(0.80) contrast(1.2); cursor: loading; text-align: left; padding-left: 40px; width: 100px; ";
    registerButton.innerHTML = "Loading.";

    loadingAnimationInterval = setInterval(() => {
        setTimeout(() => {
        registerButton.innerHTML = "Loading.";
        }, 100);
        setTimeout(() => {
        registerButton.innerHTML = "Loading..";
        }, 200);
        setTimeout(() => {
        registerButton.innerHTML = "Loading...";
        
        }, 300);
        setTimeout(() => {
        registerButton.innerHTML = "Loading..";
        }, 800);
        setTimeout(() => {
        registerButton.innerHTML = "Loading...";
        }, 900);
        setTimeout(() => {
        registerButton.innerHTML = "Loading..";
        }, 1500);
        setTimeout(() => {
        registerButton.innerHTML = "Loading...";
        }, 1600);
    }, 2000);
}


onMounted(async () => {
    try{
        userObject.value = await AccountLocal.get();
        userId.value = userObject.value.$id;
        try{
            await axios.post(`${apiUrl}users/create`, {
                email: "",
                id: userId.value
            });   
        }catch(err){
            console.log("Error: ", err);
        }
    }catch(err){
        router.push("/login");
    }
});

function addSkill(){
    let val = document.getElementById("skill-input").value;
    if(val.length > 20){
        error.value = "❗Skill must be less than 20 characters long";
        document.getElementById("error-message").classList.add("shake");
        setTimeout(() => {
            document.getElementById("error-message").classList.remove("shake");
        }, 500);         
        return;  
    }
    if (val.trim() !== "") {
        skills.value.push(val.trim());
        document.getElementById("skill-input").value = "";
    }
    error.value = "";
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
            document.getElementById("main-card-image").style.backgroundImage = 'url('+newVal[1]+')';
            saveResults.value = [false, null];
            let type  = imageChangeInfo.blob[0].type;
            if(!type.startsWith("image/")){
                error.value = "File must of type image/*";
                document.getElementById("error-message").classList.add("shake");
                setTimeout(() => {
                    document.getElementById("error-message").classList.remove("shake");
                }, 500);
            }else{
                error.value = "";
            }
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

async function changeImage(){
    imageEditMode.value = true;
    await nextTick();
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


// async function uploadProfileImage(blob, projectId, new_ending){
    
//     // let randomString = Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);

//     const filePath = `${projectId}/${new_ending}.png`;
//     await supabase.auth.signInWithPassword({
//         email: import.meta.env.VITE_ADMIN_USERNAME,
//         password: import.meta.env.VITE_ADMIN_PASSWORD
//     });

//     try{
//         await supabase.storage.from("project_page_images").upload(filePath, blob);
//     }catch(err){
//         console.error("Error uploading project page image:", err);
//     }
    
//     const { data, error } = supabase.storage.from("project_page_images").getPublicUrl(filePath);
//     if (error) {
//         console.error(error);
//     } else {
//         console.log("URL:", data.publicUrl);
//     }
//     return data.publicUrl;
// }



async function uploadImage(blob, projectId){
    
    // let randomString = Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);

    const filePath = `${projectId}/${new_ending}.png`;
    await supabase.auth.signInWithPassword({
        email: import.meta.env.VITE_ADMIN_USERNAME,
        password: import.meta.env.VITE_ADMIN_PASSWORD
    });

    try{
        await supabase.storage.from("project_page_images").upload(filePath, blob);
    }catch(err){
        console.error("Error uploading project page image:", err);
    }
    
    const { data, error } = supabase.storage.from("project_page_images").getPublicUrl(filePath);
    if (error) {
        console.error(error);
    } else {
        console.log("URL:", data.publicUrl);
    }
    return data.publicUrl;
}

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
    // let image_url = await uploadProfileImage(image_blob, route.params.projectId, new_ending);
    // props.mainCardData.image = image_url;

    // try{
    //     await supabase.storage.from("profile_images").upload(filePath, blob);
    // }catch(err){
    //     console.error("Error uploading profile image:", err);
    // }
    
    // const { data, error } = supabase.storage.from("profile_images").getPublicUrl(filePath);
    // if (error) {
    //     console.error(error);
    // } else {
    //     console.log("URL:", data.publicUrl);
    // }
    // return data.publicUrl;
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

async function createAcount(){
    let button = document.querySelector(".create-button");
    nextLoading(button);
    if(document.getElementById("agree-checkbox").checked){
            let imageUrl = await uploadProfileImage(userInfo.value.image, userId.value);
            axios({
                method: 'post',
                url: `${apiUrl}users/create/complete-profile`,
                data: {
                    'user_id': userId.value,
                    'display_name': userInfo.value.displayName,
                    'location': userInfo.value.location,
                    'looking_for': userInfo.value.lookingFor,
                    'skills': userInfo.value.skills,
                    "image_url": imageUrl,
                    "search_coordinates": userInfo.value.searchCoordinates,
                    'terms-signed': true
                }
            }).then((response) => {
                router.push("/profile/"+userTag);
            }).catch((response_error) => {
                console.log(response_error);
                error.value = "❗An error occurred while creating your account, please try again. Contact us if problem can't be resolved.";
                document.getElementById("error-message").classList.add("shake");
                setTimeout(() => {
                    document.getElementById("error-message").classList.remove("shake");
                }, 500);
            });
    }else{
        error.value = "❗You must agree to the terms of use to create an account";
        document.getElementById("error-message").classList.add("shake");
        setTimeout(() => {
            document.getElementById("error-message").classList.remove("shake");
        }, 500);            
    }
}

async function verifyUserTag(){
    let tag = document.getElementsByClassName("tag-input")[0].value;
    let button = document.querySelector(".next-button");
    nextLoading(button);
    const regex = /^[a-zA-Z0-9]+$/;
    if(tag.length < 3 || tag.length > 35){
        error.value = "❗Tag must be between 3 and 35 characters long";
        document.getElementById("error-message").classList.add("shake");
        setTimeout(() => {
            document.getElementById("error-message").classList.remove("shake");
        }, 500);           
        clearInterval(loadingAnimationInterval);
        button.style = "text-align: center; padding-left: 0px;";
        button.innerHTML = "Next";
    }
    else if (!regex.test(tag)) {
        error.value = "❗Tag must contain only letters and numbers";
        document.getElementById("error-message").classList.add("shake");
        setTimeout(() => {
            document.getElementById("error-message").classList.remove("shake");
        }, 500);
        
        button.innerHTML = "Next";
        clearInterval(loadingAnimationInterval);
    } else{
        axios({
            method: 'post',
            url: `${apiUrl}users/create/set-tag`,
            data: {
                'user_tag': tag,
                'user_id': userId.value,
                "email": userObject.value.email
            }
        }).then((response) => {
            page.value = 0;
            clearInterval(loadingAnimationInterval);
            button.style = "text-align: center; padding-left: 0px;";
            button.innerHTML = "Next";
            userTag = tag;
        }).catch((response_error) => {
            if(response_error.response && response_error.response.data.error.includes("{'message': 'duplicate key value violates unique constraint ")){
                error.value = `❗usertag ${tag} is already taken, please choose a different one.`;
            }else{
                error.value = `❗An error occurred while setting your usertag, please try again. Contact us if problem can't be resolved.`;
            }
            document.getElementById("error-message").classList.add("shake");
            setTimeout(() => {
                document.getElementById("error-message").classList.remove("shake");
            }, 500);
            clearInterval(loadingAnimationInterval);
            setTimeout(() => {
                button.style = "text-align: center; padding-left: 0px;";
                button.innerHTML = "Next";
            }, 2000);
            
        });
    }
}

function getDisplayName(){
    let dispalyName = document.getElementById("display-name-text").value;
    userInfo.value.displayName = dispalyName;
    page.value=0.15;
}

async function getDisplayLocation(location){
    let locationValue = document.getElementById("location-input").value == "" ? "Remote" : document.getElementById("location-input").value;
    if(locationValue == "Remote"){
        userInfo.value.location = "Remote";
        let coordinates = await convertAddressToCoordinates("United States");
        let lat = coordinates.lat;
        let lng = coordinates.lng;
        userInfo.value.searchCoordinates = { lat, lng };
        page.value=0.2;
        return;
    }
    userInfo.value.location = locationValue;
    let coordinates = await convertAddressToCoordinates(locationValue);
    let lat = coordinates.lat;
    let lng = coordinates.lng;
    userInfo.value.searchCoordinates = { lat, lng };
    page.value=0.2;
}

async function getSearchLocation(location){
    let locationValue = document.getElementById("location-input").value;
    if(locationValue == ""){
        page.value=0.15;
        return;
    }
    let coordinates = await convertAddressToCoordinates(locationValue);
    console.log(coordinates);
    let lat = coordinates.lat;
    let lng = coordinates.lng;
    userInfo.value.searchCoordinates = { lat, lng };
    page.value=0.15;
    console.log(userInfo.value.searchCoordinates);
}

function getLookingFor(){
    let lookingFor = document.getElementById("looking-for-text").value;
    console.log(lookingFor);
    if(lookingFor.length > 100 || lookingFor.length < 5){
        error.value = "❗Looking for must be between 5 and 100 characters long";
        document.getElementById("error-message").classList.add("shake");
        setTimeout(() => {
            document.getElementById("error-message").classList.remove("shake");
        }, 500);           
        return;  
    }
    userInfo.value.lookingFor = lookingFor;
    page.value=0.3;
}

function getSkills(){
    if(skills.value.length < 2){
        error.value = "❗Please enter at least 2 skills";
        document.getElementById("error-message").classList.add("shake");
        setTimeout(() => {
            document.getElementById("error-message").classList.remove("shake");
        }, 500);           
        return;  
    }
    userInfo.value.skills = skills.value;
    page.value=0.4;
}

async function getImage(){
    let image = document.getElementById("main-card-image").style.backgroundImage;
    image = image.substring(5, image.length-2);
    console.log(image)
    if(image == ''){
        image = 'https://jogfzuscvmxhjqnopyfd.supabase.co/storage/v1/object/public/profile_images/default'
    }
    let button = document.querySelector(".next-button");
    nextLoading(button);
    // let image_blob = await fetch(image).then(r => r.blob());
    userInfo.value.image = image;
    if(!userObject.value.emailVerification){
        page.value=1;
        await AccountLocal.createVerification(`${domain}verify`);
    }else{
        page.value=2;
    }
}


async function verifyEmailCheck(){
    try{
        let button = document.querySelector(".next-button");
        nextLoading(button);
        let userObject = await AccountLocal.get();
        if(userObject.emailVerification){
            page.value=2;
        }else{
            error.value = "❗Email hasn't been verified yet, please try again";
            document.getElementById("error-message").classList.add("shake");
            setTimeout(() => {
                document.getElementById("error-message").classList.remove("shake");
            }, 500);          
        }
    }catch(err){
        
        error.value = "❗An error occurred while verifying your email, please try again. Contact us if problem can't be resolved.";
        document.getElementById("error-message").classList.add("shake");
        setTimeout(() => {
            document.getElementById("error-message").classList.remove("shake");
        }, 500);  
        clearInterval(loadingAnimationInterval);
        setTimeout(() => {
            button.style = "text-align: center; padding-left: 0px;";
            button.innerHTML = "Next";
        }, 2000);
    }
}


async function signout(){
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
        router.push("/explore");

        

    }).catch(err => {
        console.log("Error logging out", err);
    });
}

let mobileView = ref(false);
function checkMobileView(){
    mobileView.value = window.innerWidth <= 968;
}

window.addEventListener("resize", checkMobileView);


</script>
<template>
    <ImageEditorPopUp v-if="imageEditMode" :backDropClick="backDropClick" :saveResults="saveResults" :imageInfo="imageChangeInfo"/>
    <div class="background">
        <div class="zig-background">
            <div class="mid-container">
                <!-- make this more efficient and elegant -->
                <div class="forum-contaier">
                    
                        <!-- <div id="stars"></div> -->
                        <!-- <div id="stars2"></div>
                        <div id="stars3"></div>  -->
                    
                    
                    <div class="center-title"><span class="logo-background"><span class="logo-image"></span></span>New Account<div class="signout" @click="signout">Sign Out</div></div>
                    <div class="scroll-box" v-if="page==-1">
                        

                        <div style="height:30px;"></div>
                        <div class="content-container" >
                            
                            <!-- <div class="pop-up">
                                <div class="remove-popup">X</div>
                                <div>Welcome to Launch Pad! You can leave this page and fill it out at another time, but you wont be able to use any of the features of the application until you establish your profile.</div>
                            </div> -->
                            <div class="tabs">
                                
                                <span class="selected-tab">Personal</span>
                                <span class="tab">Email Verification</span>
                                <span class="tab">Terms of Use</span>
                            </div>

                            <div style="overflow:auto; height:100%; width:100%">
                            <div class="usertag-block">
                                <div style="height:30px;"></div>
                                <div class="tag-block">
                                    <div class="tag-text">Enter the usertag you'd like to have</div>
                                    <div class="tag-input-block">
                                        <div style="font-family:Arial, Helvetica, sans-serif; display:inline-block; width:fit-content">@</div><input class="tag-input" type="text" placeholder="e.g. cockroach45">
                                    </div>
                                    <div id="error-message" style="color:red; font-family:Arial, Helvetica, sans-serif; font-size:11px; margin-top:10px; margin-bottom:-10px;">{{error}}</div>
                                </div>
                               
                                <div class="button-container">   
                                    <div @click="verifyUserTag" class="next-button">Next</div>
                                </div>
                                <div style="height:250px;"></div>  
                            </div>
                            </div>
                        </div>
                    </div>
                    <div class="scroll-box" v-if="page==0">
                        

                        <div style="height:30px;"></div>
                        <div class="content-container" >
                            <div class="tabs">
                                
                                <span class="selected-tab">Personal</span>
                                <span class="tab">Email Verification</span>
                                <span class="tab">Terms of Use</span>
                            </div>

                            <div style="overflow:auto; height:100%; width:100%">
                            
                                <div style="height:30px;"></div>
                                <div class="question-block">
                                    <div class="text">Enter your display name</div>
                                    <input id="display-name-text" class="text-input" type="text" placeholder="e.g. Jack the Ripper">
                                </div>
                                <div class="button-container">   
                                    <div @click="getDisplayName" class="next-button">Next</div>
                                </div>
                                <div style="height:250px;"></div>
                            </div>
                        </div>
                    </div>
                    <div class="scroll-box" v-if="page==0.22222">
                        

                

                        <div style="height:30px;"></div>
                        <div class="content-container" >
                            <div class="tabs">
                                
                                <span class="selected-tab">Personal</span>
                                <span class="tab">Email Verification</span>
                                <span class="tab">Terms of Use</span>
                            </div>

                            <div style="overflow:auto; height:100%; width:100%">
                            
                                <div style="height:30px;"></div>
                                
                               
                                
                                <div class="question-block">
                                    <div class="text">Enter your location</div>
                                    <Location class="location-styling"/>
                                    <div style="height:20px"></div>
                                    <div class="sub-text">This will be used in the search engine to find oppurtunities closer to you</div>
                                    <div class="sub-text">Feel free to use as precise of a location as you'd like, this information will be kept private, and by our privacy policy it will be encrypted and we will not be allowed to decrypt the data to look at it</div>
                                    
                                </div>
                                <div class="button-container">   
                                    <div @click="getSearchLocation" class="next-button">Next</div>
                                </div>
                                <div style="height:250px;"></div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="scroll-box" v-if="page==0.15">
                        
                        <div style="height:30px;"></div>
                        <div class="content-container" >
                            <div class="tabs">
                                
                                <span class="selected-tab">Personal</span>
                                <span class="tab">Email Verification</span>
                                <span class="tab">Terms of Use</span>
                            </div>

                            <div style="overflow:auto; height:100%; width:100%">
                            
                                <div style="height:30px;"></div>
                                
                               
                                
                                <div class="question-block">
                                    <div class="text">Enter your display location</div>
                                    <Location class="location-styling"/>
                                    <div style="height:20px"></div>
                                    <div class="sub-text">Please don't write your exact address, but your general region. This will be visible to other users who may want to know if you live near by to work with you</div>
                                    <div class="sub-text">Leave blank if you want to be a remote based user</div>
                                    
                                </div>
                                <div class="button-container">   
                                    <div @click="getDisplayLocation" class="next-button">Next</div>
                                </div>
                                <div style="height:250px;"></div>
                            </div>
                        </div>

                        
                    </div>
                    <div class="scroll-box" v-if="page==0.2">
                        

                        <div style="height:30px;"></div>
                        <div class="content-container" >
                            <div class="tabs">
                                <span class="selected-tab">Personal</span>
                                <span class="tab">Email Verification</span>
                                <span class="tab">Terms of Use</span>
                            </div>

                            <div style="overflow:auto; height:100%; width:100%">
                            
                                <div style="height:30px;"></div>
                                <div class="question-block">
                                    <div class="text">What are you looking for on Launch Pad?</div>
                                    <textarea class="text-area-input" id="looking-for-text" type="text" placeholder="Im am looking for..."></textarea> 
                                    <div id="error-message" style="color:red; font-family:Arial, Helvetica, sans-serif; font-size:11px; margin-top:10px; margin-bottom:-10px;">{{error}}</div>
                                </div>
                                <div class="button-container">   
                                    <div @click="getLookingFor" class="next-button">Next</div>
                                </div>
                                <div style="height:250px;"></div>
                            </div>
                        </div>
                    </div>
                    <div class="scroll-box" v-if="page==0.3">
                        

                        <div style="height:30px;"></div>
                        <div class="content-container" >
                            <div class="tabs">
                                
                                <span class="selected-tab">Personal</span>
                                <span class="tab">Email Verification</span>
                                <span class="tab">Terms of Use</span>
                            </div>

                            <div style="overflow:auto; height:100%; width:100%">
                                <div style="height:30px;"></div>
                                <div class="question-block">
                                    <div class="text">What skills do you have? List at least 2</div>
                                    <input class="skill-input" id="skill-input" type="text">
                                    <span @click="addSkill" class="add-block">+</span>
                                    <br style="margin-bottom: 10px;">
                                    <div id="error-message" style="color:red; font-family:Arial, Helvetica, sans-serif; font-size:11px; margin-top:10px; margin-bottom:-10px;">{{error}}</div>
                                    <br style="margin-bottom:10px;">
                                    <div class="skills-container">
                                        <div v-for="(skill, index) in skills" :key="index" class="skill">
                                            {{ skill }}
                                            <span class="remove-x" @click="skills.splice(index, 1)">x</span>
                                        </div>
                                    </div>
                                </div>
                                <div class="button-container">   
                                    <div @click="getSkills" class="next-button">Next</div>
                                </div>
                                <div style="height:250px;"></div>
                            </div>
                        </div>
                    </div>
                    <div class="scroll-box" v-if="page==0.4">
                        <div style="height:30px;"></div>
                        <div class="content-container" >
                            <div class="tabs">
                                <span class="selected-tab">Personal</span>
                                <span class="tab">Email Verification</span>
                                <span class="tab">Terms of Use</span>
                            </div>

                            <div style="overflow:auto; height:100%; width:100%">
                            
                                <div style="height:30px;"></div>
                                
                               
                                
                                <div class="question-block">
                                    <div class="text">Click the image bellow to set a profile picture. Leave for default (current image)</div>
                                    <div class="image-space">
                                        <div id="main-card-image" class="image" :style="'width:150px; height:150px;'"></div>
                                        <img @click="changeImage" class="image-edit-faint" src="@/assets/founder-space/edit/image-edit-faint.png" />
                                    </div>
                                    <div id="error-message" style="color:red; font-family:Arial, Helvetica, sans-serif; font-size:11px; margin-top:10px; margin-bottom:-10px;">{{error}}</div>
                                </div>
                                <div class="button-container">   
                                    <div @click="getImage" class="next-button">Verify Account</div>
                                </div>
                                <div style="height:250px;"></div>
                            </div>
                        </div>
                    </div>
                    <div class="scroll-box" v-if="page==1">
                        
                        <div style="height:30px;"></div>
                        <div class="content-container">
                            <div class="tabs">
                                <span class="tab">Personal</span>
                                <span class="selected-tab">Email Verification</span>
                                <span class="tab">Terms of Use</span>
                            </div>

                            <div style="overflow:auto; height:100%; width:100%">
                                <div style="height:30px;"></div>
                                <div class="email-verify-block" style="min-height:400px">
                                    <div class="mail-container">
                                        <img src="@/assets/user-creation/mail-1.png" class="mail-image"/>
                                    </div>
                                    <div class="mail-prompt">
                                        <div class="text" style="font-weight:bold;">We've sent an email to you with a link. </div>
                                        <div class="text">Please click on that link to verify your account. If it doesn't end up working, you can send another link using the resend button below.</div>
                                        <div class="text">After verifying, press next</div>
                                        <br style="margin-bottom:10px;">
                                        <span class='sub-link' style="background:black">Resend Verification</span>
                                        <br style="margin-bottom:10px;">
                                        <div id="error-message" style="color:red; font-family:Arial, Helvetica, sans-serif; font-size:11px; margin-top:10px; margin-bottom:-10px;">{{error}}</div>
                                    </div>
                                    
                                </div>
                                <div class="button-container">   
                                    <div @click="verifyEmailCheck" class="next-button">Next</div>
                                </div>
                                <div style="height:200px;"></div>
                            </div>
                        </div>
                    </div>
                    <div class="scroll-box" v-if="page==2">

                        <div style="height:30px;"></div>
                        
                        <div class="content-container">
                            <div class="tabs">
                                <span class="tab">Personal</span>
                                <span class="tab">Email Verification</span>
                                <span class="selected-tab">Terms of Use</span>
                            </div>
                            <div style="overflow:auto; height:100%; width:100%">
                                <div style="height:30px;"></div>
                                <div class="terms-of-use-box">
                                    <h1>User Terms of Use</h1>
                                    <p>By creating an account on Launch Pad, you agree to</p>
                                    <p>1.) Not post any content in violation of United States law</p>
                                    <p>2.) Not post any content that demeans, harasses, or targets groups of people</p>
                                    <p>3.) Not post any romantic/sexually bidding content.</p>
                                    
                                    <h1>Privacy Policy</h1>
                                    <p>1.) We do not, and will not share any of your data with any third party / external sources. We secure your data through the best means avaible to us, but we do not ensure 100% security in the case of a technically compromising security breach, and we are not responsible for damages in such scenarios.</p>
                                    <p>2.) We reserve the right to review and audit any material sent between two paries, as well as review any unpublished content to prevent this platform from becoming used for illegal exchange</p>

                                </div>
                                <div class="button-container">   
                                    <div style="background:black; padding:10px; border-radius:10px; height:auto;width:fit-content; max-width:calc(100% - 200px); position:absolute; top:5px;">
                                        <input @click="error=''"  type="checkbox" id="agree-checkbox">
                                        <label for="agree-checkbox" style="color:white; font-family:arial; margin-left:10px;">I have read and agree to the Terms of Use and Privacy Policy</label>
                                        <br>
                                        <div id="error-message" style="color:red; font-family:arial; font-size:11px; margin-top:1px; margin-bottom:-0px;">{{error}}</div>
                                    </div>
                                    
                                    <span @click="createAcount" class="create-button">Create Account</span>
                                </div>
                                <div style="height:160px;"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>  
        </div> 
    </div>
    
</template>
<style scoped>
.signout{
    background: linear-gradient(45deg, rgb(0, 0, 0), rgb(2, 2, 2));
    border: rgb(255, 255, 255) solid 1.5px;
    color:white;
    position:absolute;
    bottom:20px;
    right:20px;
    padding:8px;
    font-size: 12px;
    font-weight: bold;
    display:block;
    border-radius: 20px;
    text-align: center;
    z-index: 100;
}
.signout:hover{
    transition: all ease .3s;
    transform: scale(1.05);
    background: linear-gradient(45deg, rgb(37, 37, 37), rgb(53, 53, 53));
    cursor: pointer;
}
.sub-text{
    font-family: Arial, Helvetica, sans-serif;
    font-size: 12px;
    color: #000000b3;
    max-width: 300px;
    margin-bottom: 10px;
}
@keyframes shake {
    0% { transform: translate(1px, 1px) rotate(0deg); }
    10% { transform: translate(-1px, -2px) rotate(-1deg); }
    20% { transform: translate(-3px, 0px) rotate(1deg); }
    30% { transform: translate(3px, 2px) rotate(0deg); }
    40% { transform: translate(1px, -1px) rotate(1deg); }
    50% { transform: translate(-1px, 2px) rotate(-1deg); }
    60% { transform: translate(-3px, 1px) rotate(0deg); }
    70% { transform: translate(3px, 1px) rotate(-1deg); }
    80% { transform: translate(-1px, -1px) rotate(1deg); }
    90% { transform: translate(1px, 2px) rotate(0deg); }
    100% { transform: translate(1px, -2px) rotate(-1deg); }
}
@keyframes  gentleShake{
    0% { transform: translate(0px, 0px) }
    25% { transform: translate(-2px, -2px) }
    50% { transform: translate(2px, 0px)  }
    75% { transform: translate(-2px, 0px)  }
    100% { transform: translate(0px, 0px) }
}
.shake {
    animation: gentleShake 0.5s;
}

#error-message{
}
.tag-input{
    width:100%;
    max-width:360px;
    font-size:16px;
    margin-left:5px;
    border:none;
    outline:none;
    background:transparent;
    padding-bottom:5px;
    border-bottom: 1px black solid;
}
.tag-input-block{
    width:100%;
    max-width:400px;
    outline:none;
    margin-left:-5px;
    border-radius:10px;
    padding:5px;
}
.tag-text{
    font-family: Arial, Helvetica, sans-serif;
    font-size: 16px;
    margin-bottom:10px;
}
.tag-block{
    display: block;
    margin:auto;
    margin-bottom: 20px;
    width: 85%;
    border-radius: 20px;
    padding:20px;
    background:rgba(255, 255, 255, 0.84);
}
.usertag-block{
}
.location-styling{
    border-radius:10px;
    width:100%;
    max-width:400px;
    
}
.logo-background{
    height:50px;
    width: 50px;
    position:relative;
    display:inline-block;
    top:0px;
    left:0px;
    padding:15px;
    margin:-29px;
    margin-right:-5px;
    margin-left:-50px;
    
    padding-bottom:21px;

    overflow:hidden;
    filter:saturate(0%);

    
    
}

.logo-image{
    width:60px;
    height:60px;
    position:absolute;
    top:12%;
    left:10%;
    background-image: url("@/assets/apollo8.png");
    background-size:cover;
    background-repeat: no-repeat;
    z-index:1000;
    
}
.mail-container{
    width:100%;
    height:100%;
    border-radius:50%;
    padding:40px;
    background: linear-gradient(45deg, rgba(173, 236, 255, 0.74), rgba(255, 255, 255, 0.74));
    box-shadow:  0 0 10px black;
    margin-left:20px;
}
.mail-prompt{
    display: inline-block;
    text-align: left;
    vertical-align: middle;
    height:fit-content;
    margin-right:20px;
    background:white;
    padding:20px;
    border-radius: 10px;
}
.mail-image{
    
    display: inline-block;
    width: 100%;
    height:100%;
}
.email-verify-block{
    display: flex;
    justify-content: center;
    gap:60px;
    width:100%;
}
.remove-popup{
    font-size: 14px;
    font-weight: bold;
    color: #00000093;
    cursor: pointer;
    font-family:Arial, Helvetica, sans-serif;
    position: absolute;
    z-index: 7;
    background-color: rgb(80, 249, 255);
    padding: 15px;
    padding-left:10px;
    padding-top:10px;
    padding-bottom:5px;
    right:-5px;
    top:-5px;
    border-radius: 10px;
    float:right;
}
.pop-up{
    box-shadow: 0 0 10px #000000;
    position:absolute;
    top:0;
    right:0;
    max-width: 400px;
    width:100%;
    height: auto;
    padding:20px;
    margin:10px;
    border-radius: 20px;
    background:white;
    color:black;
    font-family: Arial, Helvetica, sans-serif;
    overflow:hidden;
}
.zig-background{
    width:100%;
    height:100%;
    background-image: url("@/assets/user-creation/background-new-1.png");
    background-size: 1000px auto;
    background-repeat: repeat;
}
.selected-tab{
    display: inline-block;
    color: rgb(255, 139, 110);
    font-family: Arial, Helvetica, sans-serif;
    font-size: 14px;
    margin-right: 20px;
    text-decoration-thickness: 2px;
    
    background:black;
    padding:10px;
    border-radius:15px;


}
.sub-title{
    font-family: Arial, Helvetica, sans-serif;
    font-size: 25px;
    color: white;
    text-shadow: 2px 2px 4px #000000;
    position: relative;
    font-weight: bold;
    width:fit-content;
    width:85%;
    margin: auto;
    padding-left:0px;
    text-align: left;
    font-family: Arial, Helvetica, sans-serif;
    margin-bottom:40px;
    margin-top:20px;
}
.center-title{
    font-family: Arial, Helvetica, sans-serif;
    font-size: 30px;
    color: rgb(255, 255, 255);
    background: linear-gradient(45deg, rgba(255, 109, 31, 0.95), rgba(255, 109, 31, 0.74));
    position: relative;
    font-weight: bold;
    margin:auto;
    padding:20px;
    padding-left:50px;
    font-family: Arial, Helvetica, sans-serif;
}
.tabs{
    width:90%;
    padding: 20px;
    margin:auto;
    background: linear-gradient(to top, transparent, rgba(132, 0, 255, 0));
}
.tab{
    display: inline-block;
    color: white;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 14px;
    margin-right: 20px;
    background:black;
    padding:10px;
    border-radius:15px;
}
.create-button{
    width:fit-content;
    width:130px;
    text-align: center;
    padding:10px;
    font-family: Arial, Helvetica, sans-serif;
    border-radius: 5px;
    color:rgb(255, 255, 255);
    font-weight: bold;
    box-shadow: inset 0 0px 5px rgba(0, 0, 0, 0.596);
    background:rgb(88, 91, 255);
    position:absolute;
    top:5px;
    right:10px;
}
.terms-of-use-box{
    margin:auto;
    width:calc(95% - 60px);
    height: 450px;
    background-color: white;
    border: 1px solid white;
    border-radius: 5px;
    padding:30px;
    box-shadow: inset 0 0px 10px rgba(0, 0, 0, 0.8);
    color:black;
    font-family: Arial, Helvetica, sans-serif;
    overflow-y: auto;
}
.invalid{
    width:30px;
    height:20px;
    color:red;
    padding:5px;
    border-radius:50%;
    font-size:25px;
    margin-left:10px;
    margin-bottom:-20px;
}
.valid{
    width:30px;
    height:20px;
    color:green;
    padding:5px;
    border-radius:50%;
    font-size:25px;
    margin-left:10px;
    margin-bottom:-20px;
}
.sub-link{
    font-family: Arial, Helvetica, sans-serif;
    margin-right:20px;
    margin-top:10px;
    color:white;
    background:blue;
    border-radius:15px;
    box-shadow: 0 0 5px black;
    padding:10px;
}

.scroll-box{
    width:100%;
    height:100%;
}
.button-container{
    position: relative;
    display: block;
    justify-content: flex-end;
    width:95%;
    margin-bottom:200px;
    padding:10px;
    bottom:0;
    margin:auto;

}
.next-button{
    float:right;
    right:10px;
    bottom:0;
    text-align: center;
    width:fit-content;
    padding:10px;
    width:130px;
    font-family: Arial, Helvetica, sans-serif;
    border-radius: 5px;
    background:rgb(255, 255, 255);
    border: rgb(121, 201, 255) 3px solid;
    box-shadow: inset 0 0px 5px rgba(0, 0, 0, 0.596);
    
    
}

.add-block{
    display: inline-block;
    width: 10px;
    margin-left: 12px;
    background-color: rgb(255, 255, 255);
    filter: hue-rotate(200deg);
    padding:10px;
    height:1px;
    padding-top:14px;
    padding-bottom:14px;
    color:rgb(0, 0, 0);
    border: 1px solid black;
    text-align: center;
    line-height: 0;
    font-size: 20px;
    border-radius: 5px;
    cursor: pointer;
    font-weight: bold;
    text-decoration: 10px 10px 5px rgb(0, 0, 0);
}
.image{
    background-image: url('@/assets/user-creation/default-profile.png');
    background-repeat: no-repeat;
    background-size:cover;
    background-position: center;
    max-height: 100%;
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

.forum-contaier{
    width:100%;
    height:calc(100% - 0px);
    min-height: 500px;
    display:block;
    margin: auto;
    box-shadow: inset 0 10px 20px rgb(0, 0, 0);
    overflow:hidden;
}
.content-container{
    width:85%;
    max-width: 900px;
    margin:auto;
    height:calc(100% - 20px);
    margin-top:-30px;
    position:relative;
    
    background:rgba(0, 0, 0, 0);
}
@media (max-width: 1000px) {
    .content-container{
        width:100%;
    }
}
.mid-container{
    width:100%;
    margin-top: -50px;
    padding-top:50px;
    height:calc(100%);
    box-shadow: inset 0 0 10px 10px #0000007a;
    background-image: radial-gradient(circle, rgba(73, 73, 73, 0) 30%, rgba(255, 255, 255, 0.25) 70%);
    overflow: auto;
    opacity: 1;
}
.remove-x{
    font-size: 17px;
    font-weight: bold;
    margin-left: 5px;
    color: #ffffff;
    cursor: pointer;
    font-family:Arial, Helvetica, sans-serif;
}

.skill{
    display: inline-block;
    background-color: #0ed9c800;
    filter: hue-rotate(200deg);
    padding:10px;
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.664);
    color: rgb(0, 0, 0);
    border-radius: 10px;
    margin-right: 10px;
    margin-bottom: 10px;
    border: 1px solid #ffffff;
    font-family: Arial, Helvetica, sans-serif;
}
.skills-block{
    display: block;
    background-color:#ffffff00;
    filter: hue-rotate(200deg);
    padding:15px;
    box-shadow: 0 10px 20px rgba(255, 255, 255, 0.295);
    border-radius: 10px;
    font-size: 14px;
    font-family: Arial, Helvetica, sans-serif;
}
.skill-input{
    width: calc(100% - 30px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.452);
    max-width: 300px;
    border:none;
    outline:auto;
    border-radius: 5px;
    padding: 2px;
    padding-left: 10px;
    font-size: 16px;
    background-color: transparent;
    color: rgb(0, 0, 0);
}
.text-input{
    width: calc(100% - 30px);
    max-width: 400px;
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0);
    border:none;
    outline:auto;
    padding: 2px;
    padding-left: 10px;
    border-radius:5px;
    font-size: 16px;
    background-color: rgba(255, 255, 255, 0);

    color: rgb(0, 0, 0);
}
.text-area-input{
    width: calc(100% - 30px);
    max-width: 400px;
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.452);
    border:none;
    border-radius: 5px;
    padding: 2px;
    height:60px;
    resize: none;
    font-family: Arial, Helvetica, sans-serif;
    padding-left: 10px;
    font-size: 16px;
    outline:auto;
    background-color: transparent;
    color: rgb(0, 0, 0);
}
.question-block{
    display: block;
    margin:auto;
    margin-bottom: 20px;
    width: 85%;
    border-radius: 20px;
    padding:20px;
    background:linear-gradient(45deg, rgba(255, 255, 255, 0.84), rgba(255, 255, 255, .84));
}
.text{
    font-size: 16px;
    font-family: Arial, Helvetica, sans-serif;
    margin-bottom: 10px;
    color: rgb(0, 0, 0);
}
.scrollable-background{
    width:100%;
    height:100%;
    background-size: 700px auto;
    background-repeat: repeat;
    
}
.el-container{
    display: block;
    
    margin: auto;
    width:calc( 100% - 140px );
    max-width: 1200px;
    background: url("@/assets/user-creation/dots-light.png");
    background-color: rgba(0, 0, 0, 0.918);
    background-size: 2000px auto;
    background-repeat: repeat;
    padding: 70px;
    padding-top:180px;
    height: 10000px;
  box-shadow: 0 0 200px 400px #000000a2; 
}
.copy-right{
    font-family: Arial, Helvetica, sans-serif;
    font-size: 10px;
    position: absolute;
    top:35px;
    left: 85px;
    color: #ffffff9f;
    padding: 10px;
}
.title{
    font-family: Arial, Helvetica, sans-serif;
    font-size: 25px;
    color: rgb(255, 255, 255);
    text-shadow: 2px 2px 4px #000000;
    position: absolute;
    font-weight: bold;
    top: 0px;
    left: 90px;
    transform: translateY(12px) ;
}
.logo-icon-background{
  width:45px;
  height:45px;
  background: rgb(255, 255, 255);
  border-radius: 50px;
  position: absolute;
  margin-top: 8px;
  margin-left: 25px;
  /* whatever the dominant color of what is on the inside, should match the color of this */
  border: 2px solid rgb(227, 155, 78);
  background-image: linear-gradient(45deg, rgb(255, 109, 31), rgb(255, 221, 165)); 
  filter: contrast(100%);
  overflow: hidden;
}

.logo {
  display: inline-block;
  width: 45px; 
  /*80px is the original size, so 50px is a good size for the logo in the header*/
  height: 45px;
  filter:saturate(0);
  
}

.header{
    position: absolute;
    top:0;
    left:0;
    width:100vw;
    height:70px;
    background-image: linear-gradient(to bottom, rgb(0, 0, 0), rgb(17, 17, 17));
    box-shadow: 0 5px 50px rgba(0, 0, 0, 0.89);
    z-index: 1;
}
.background{
    position: fixed;
    top:0;
    left:0;
    width:100vw;
    height:100vh;
    background: linear-gradient(45deg, #050008 10%, hsl(234, 100%, 43%) 90%);
    background-color: rgb(0, 0, 0);
    display:flex;
    justify-content:center;
    align-items:center;
}
</style>


<style lang="sass" scoped>

@function multiple-box-shadow ($n) 
  $value: '#{random(6000)}px #{random(6000)}px #FFF'
  @for $i from 2 through $n
    $value: '#{$value} , #{random(6000)}px #{random(6000)}px #FFF'

  @return unquote($value)

$shadows-small:  multiple-box-shadow(2100)
$shadows-medium: multiple-box-shadow(600)
$shadows-big:    multiple-box-shadow(300)

.forum-contaier

    
#stars
  width: 1px
  height: 1px
  background: transparent
  box-shadow: $shadows-small
  z-index: -1;
  animation			: animStar 50s linear infinite
    
  &:after
    content: " "
    position: absolute
    top: 2000px
    width: 1px
    height: 1px
    z-index: -1;
    background: transparent
    box-shadow: $shadows-small
    
#stars2
  width: 2px
  height: 2px
  background: transparent
  box-shadow: $shadows-medium
  animation			: animStar 100s linear infinite
  z-index: -1;
    
  &:after
    content: " "
    position: absolute
    top: 2000px
    width: 2px
    height: 2px
    background: transparent
    box-shadow: $shadows-medium
    z-index: -1;
    
#stars3
  width: 3px
  height: 3px
  background: transparent
  box-shadow: $shadows-big
  z-index: -1;
  animation			: animStar 150s linear infinite
    
  &:after
    content: " "
    position: absolute
    top: 2000px
    width: 3px
    height: 3px
    background: transparent
    box-shadow: $shadows-big
    z-index: -1;

#title
  position: absolute
  top: 50%
  left: 0
  right: 0
  
  color: #FFF
  text-align: center
  font-family: 'lato',sans-serif
  font-weight: 300
  font-size: 50px
  letter-spacing: 10px
  
  margin-top: -60px
  padding-left: 10px
  
  span
    background: -webkit-linear-gradient(white, #38495a)
    -webkit-background-clip: text
    -webkit-text-fill-color: transparent
    
@keyframes animStar
  from	
    transform: translateY(0px)
  to		
    transform: translateY(-2000px)
    
</style>
