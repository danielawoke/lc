<script setup>
import { useRoute, useRouter } from 'vue-router'
import { onMounted } from 'vue';
import { ref, nextTick, watch } from 'vue';
import axios from 'axios';
import locationDatabase from '@/components/supporting-components/location-database.vue';
import ImageEditorPopUp from '@/components/founder-space/interfaces/edit-cards/image-replace/pop-up.vue';
import colorChangePopup from '@/components/founder-space/interfaces/edit-cards/color-change/popup.vue';
import { supabase } from "@/lib/supabase";
const imageEditMode = ref(false);
const backDropClick = ref([false]);
const backDropClickColor = ref([false]);
const colorEditMode = ref(false);
const saveResults = ref([false, null]);
const color = ref({backgroundColor: ["rgb(0, 26, 255)"], titleColor: ["#FFFFFF"],  locationColor: ["#FFFFFF"], contentColor: ["#FFFFFF"]});
let route = useRoute();
let originCard = null;
let props = defineProps({
  mainCardData: Object,
  SetToEdit: Array,
});

let dummyCard = ref({
        title: "",
        location: "",
        image: "",
        color: {backgroundColor: ["white"], titleColor: ["#000000"], contentColor: ["#000000"], locationColor: ["#000000"]},
        physicalLocation:false,
        remote:false,
        content:""
    });

onMounted(async () => {
    await nextTick();
    dummyCard.value = JSON.parse(JSON.stringify(props.mainCardData));
    dummyCard.value.content = dummyCard.value.content.replace("<pre style=\"font-family: Arial, Helvetica, sans-serif; font-weight: normal; font-size: 18px; white-space: pre-wrap; break-word: break-word; \">", '').replace("</pre>", '');
    let mainTitleArea = document.getElementById("main-title");
    let descriptionArea = document.getElementById("main-description");
    await titleTextAreaAdjust(mainTitleArea);
    await descriptionTextAreaAdjust(descriptionArea);
    document.getElementsByClassName(".pac-container")[0].style.marginTop = "-25px !important";
});

let imageChangeInfo = {
    blob: [null],
    url: [null]
};

async function getImageBlob(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const blob = await response.blob();
        return blob;
    } catch (error) {
        console.error('Could not fetch image:', error);
    }
}

async function obtainObjectImage(url){
    if(url.indexOf("blob:") === 0){
        return url;
    } else {
        return await getImageBlob(url);
    }
}

async function convertURLToImageObject(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const blob = await response.blob();
        const imageObjectURL = URL.createObjectURL(blob);
        return imageObjectURL;
    } catch (error) {
        console.error('Could not convert URL to image object:', error);
    }   
}

async function uploadProfileImage(blob, projectId, new_ending){
    
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


function genearteNewURLEnding(oldURLEnding) {

    let newString = "main";
    while(newString === oldURLEnding){
        newString = "main" + Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
    }
    return newString;
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

async function saveCard(){
    if(imageChangeInfo.url[0] != null){
        let image_url_ending = props.mainCardData.image.split("/").slice(-1)[0].split(".")[0];
        let new_ending = genearteNewURLEnding(image_url_ending);
        let old_url = props.mainCardData.image.split("/").slice(-2)[0]+"/"+props.mainCardData.image.split("/").slice(-1)[0];
        try{
            await supabase.storage.from("project_page_images").remove([old_url]); // note: array of file paths
        }
        catch(err){
            console.log("No existing profile image to delete, proceeding with upload.");
        }
        let image_blob = null;
        try{
            image_blob = await fetch(imageChangeInfo.url[0]).then(r => r.blob());
        }catch(e){
            let response = await fetch(`${import.meta.env.VITE_CORS_PROXY_URL}${encodeURIComponent(imageChangeInfo.url[0])}`);
            if (!response.ok) {
                image_blob = null;
            }else{
                image_blob = response.blob();
            }
        }
        if(image_blob != null){
            let image_url = await uploadProfileImage(image_blob, route.params.projectId, new_ending);
            props.mainCardData.image = [image_url];
        }else{
            props.mainCardData.image = [imageChangeInfo.url[0]];
        }
        let image_url = await uploadProfileImage(image_blob, route.params.projectId, new_ending);
        props.mainCardData.image = image_url;
    }
    let content = document.getElementById("main-description").value;
    let title = document.getElementById("main-title").value;
    if(!dummyCard.value.physicalLocation){
        props.mainCardData.location = document.getElementsByClassName("location-text")[0].value;
        let coordinates = await convertAddressToCoordinates(document.getElementsByClassName("location-text")[0].value);
        if(coordinates != null){
            console.log("Coordinates obtained:", coordinates);
            props.mainCardData.coordinates = coordinates;
        }
    }
    props.mainCardData.content = `<pre style=\"font-family: Arial, Helvetica, sans-serif; font-weight: normal; font-size: 18px; white-space: pre-wrap; break-word: break-word; \">${content}</pre>`;
    props.mainCardData.title = title;
    props.mainCardData.color = dummyCard.value.color;
    props.SetToEdit[0] = false;
}

//     font-family: Arial, Helvetica, sans-serif;
    // color: #444;
    // font-size: 18px;
    // line-height: 1.6;
    // font-weight: normal;

function cancel(){
    props.mainCardData.content = `<pre style=\"font-family: Arial, Helvetica, sans-serif; font-weight: normal; font-size: 18px; white-space: pre-wrap; break-word: break-word; \">${props.mainCardData.content}</pre>`;
    props.SetToEdit[0] = false;
}

let contentWithLineBreaks = ref("");


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

function chageColor(){
    console.log("Change color clicked");
    originCard = ["MainCard", {
        title: document.getElementById("main-title").value,
        content: document.getElementById("main-description").value.substring(0, 1000)+"...",
        location: document.getElementsByClassName("location-text")[0].value.substring(0, 150)+"...",
        image: document.getElementById("main-card-image").src
    }];
    colorEditMode.value = true;
}

async function descriptionTextAreaAdjust(element) {
  element.style.height = "1px";
  await nextTick();
  let height = 0;
  if(mobileMode.value){
    height = Math.max(element.scrollHeight);
  }else{
    height = Math.max(element.scrollHeight, 300);
  }
  document.getElementById("description-container").style.height = (25+height)+"px";
  element.style.height = (25+height)+"px";
}

async function titleTextAreaAdjust(element) {
  element.value = element.value.replace(/\n/g, '');
  element.style.height = "1px";
  await nextTick();
  let height = (25+element.scrollHeight-25);
  document.getElementsByClassName("title-outline")[0].style.height = (height-60)+"px";
  element.style.height = height+"px";
}

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


watch(backDropClick, async (newVal) => {
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
            imageEditMode.value = false;
            backDropClick.value[0] = false;
        }, time);
    }
},{deep: true});

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
            document.getElementById("main-card-image").src = newVal[1];
            saveResults.value = [false, null];
        }, time);
    }
},{deep: true});



function mobileModeListener(){
    mobileMode.value = window.innerWidth <= 1200;
    console.log("Mobile mode:", mobileMode.value);
}

let mobileMode = ref(true)
mobileMode.value = window.innerWidth <= 1200;
window.addEventListener('resize', mobileModeListener);


</script>

<template>
    <colorChangePopup v-if="colorEditMode" :backDropClickColor="backDropClickColor" :colorInfo="dummyCard.color" :originCard="originCard"/>
    <ImageEditorPopUp v-if="imageEditMode" :backDropClick="backDropClick" :saveResults="saveResults" :imageInfo="imageChangeInfo"/>
    <div v-if="mobileMode" class="card-color-surround" :style="{ backgroundColor: dummyCard.color.backgroundColor }">
        <div class="card" style="width:95%; padding-top:20px;">
            <div class="title-outline">
                <textarea id="main-title" class="title" @keypress='titleTextAreaAdjust($event.target)' @keyup='titleTextAreaAdjust($event.target)' @keydown='titleTextAreaAdjust($event.target)' :style="{color: dummyCard.color.titleColor, overflow:'hidden'}" :value="dummyCard.title"></textarea>
            </div>
            <div v-if="!dummyCard.physicalLocation" class="location">
                <img class="location-icon" src="@/assets/location.png">
                <locationDatabase :location="dummyCard.location" :color="dummyCard.color.locationColor"/>
            </div>
            <div v-if="dummyCard.remote" class="remote-option"><img class="remote-image" src="https://cdn-icons-png.flaticon.com/512/3759/3759392.png">Remote</div>
            <div class="gap"></div>
            <div class="details">
                    <div class="image-space" style="margin:auto; margin-top:-50px; margin-bottom:20px; width: 100%;">
                        <img id="main-card-image" class="image" :src="dummyCard.image" />
                        <img @click="changeImage" class="image-edit-faint" src="@/assets/founder-space/edit/image-edit-faint.png" />
                    </div>
                <div  id="description-container" style="width:calc(100% + 50px); margin-left:-50px;">
                    <textarea id="main-description" @keypress='descriptionTextAreaAdjust($event.target)' @keyup='descriptionTextAreaAdjust($event.target)' @keydown='descriptionTextAreaAdjust($event.target)' class="description" :style="{color: dummyCard.color.contentColor}" :value="dummyCard.content"></textarea>
                </div>
            </div>
            <div id="hyper-buttons-left" style="width:100px;">
                <img @click="chageColor" id="paint" src="@/assets/founder-space/edit/paint-icon.png" />
            </div>
            <div id="hyper-buttons-right">
                <img @click="saveCard" id="save" src="@/assets/founder-space/edit/save-icon.png" />
                <img @click="cancel" id="cancel" src="@/assets/founder-space/edit/x-icon.png" />
            </div>
        </div>
    </div>
    <div v-else class="card-color-surround" :style="{ backgroundColor: dummyCard.color.backgroundColor }">
        <div class="card">
            <div class="title-outline">
                <textarea id="main-title" class="title" @keypress='titleTextAreaAdjust($event.target)' @keyup='titleTextAreaAdjust($event.target)' @keydown='titleTextAreaAdjust($event.target)' :style="{color: dummyCard.color.titleColor, overflow:'hidden'}" :value="dummyCard.title"></textarea>
            </div>
            <div v-if="!dummyCard.physicalLocation" class="location">
                <img class="location-icon" src="@/assets/location.png">
                <locationDatabase :location="dummyCard.location" :color="dummyCard.color.locationColor"/>
            </div>
            <div v-if="dummyCard.remote" class="remote-option"><img class="remote-image" src="https://cdn-icons-png.flaticon.com/512/3759/3759392.png">Remote</div>
            <div class="gap"></div>
            <div class="details">
                <div class="inline-correction">
                    <div class="image-space">
                        <img id="main-card-image" class="image" :src="dummyCard.image" />
                        <img @click="changeImage" class="image-edit-faint" src="@/assets/founder-space/edit/image-edit-faint.png" />
                    </div>
                </div>
                <div  id="description-container">
                    <textarea id="main-description" @keypress='descriptionTextAreaAdjust($event.target)' @keyup='descriptionTextAreaAdjust($event.target)' @keydown='descriptionTextAreaAdjust($event.target)' class="description" :style="{color: dummyCard.color.contentColor}" :value="dummyCard.content"></textarea>
                </div>
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
.remote-image{
    width: 20px;
    height: 20px;
    vertical-align: middle;
    margin-right: 10px;
    margin-left:-2.5px;
}
.remote-option{
    font-family: Arial, sans-serif;
    font-size: 20px;
    text-align: left;
    margin-left: 64px;
    margin-top: 10px;
    background-color: transparent;
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
.details {
    height:auto;
    text-align: left;
    margin-left: 60px;
    padding-bottom:180px;
    height: auto;
    resize: none;
}
#description-container {
    display: inline-block;
    width: calc(100% - min(25vw, 500px) - 220px);
    margin-left: 38px;
    margin-top: 0px;
    vertical-align:middle;
    outline:auto;
    height:fit-content;
}
.description {
    width:100%;
    font-family: Arial, sans-serif;
    color: v-bind(color.contentColor[0]);
    font-size: 18px;
    line-height: 1.6;
    background-color: transparent;
    border:none;
    outline: none;
    height:fit-content;
    overflow: hidden;
    resize: none;
    padding-bottom: 50px;
}
.image-space {
    outline: auto;
    display: flex;
    justify-content: center; 
    align-items: center;
    width: 25vw;
    max-width: 500px;
    height: 400px;
    background-color: transparent;
    overflow: hidden;
    position: relative;
    z-index: 6;
}
.image-edit-faint {
    outline: auto;
    width: 25vw;
    max-width: 500px;
    max-height: 400px;
    position: absolute;
    z-index: 5;
    opacity: 0.3;
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

.gap{
    height:85px;
    width:100%;
    background-color: rgba(255, 255, 255, 0);
    z-index: 1;
    overflow:hidden;
    position:relative;
}
.inline-correction {
    display: inline-block;
    vertical-align: top;
    
}
.title-outline {
    margin-top:59px;
    margin-left: 58px;
    outline: auto;
    width: calc(100% - 60px);
    z-index: 0;
    background-color: transparent;

}
.title {
     z-index: 1;
    font-family: "Arial", sans-serif;
    font-size: 50px;
    font-weight: bolder;
    background-color: transparent;
    z-index: 0;
    width: calc(100%);
    border:none;
    outline: none;
    field-sizing: content;
    resize: none;
    padding-top:30px;
    overflow-y: hidden;
    height:50px;
    padding-top: 0px !important;
    padding-bottom:60px;
}


.card-color-surround{
    z-index: -3;
}
.card{
    width: calc( (100% - 180px) );
    height: auto;
    max-width: 1600px;
    border-radius: 10px;
    padding: 20px;
    margin: auto;
    z-index: -3;
    background-color: transparent;
}
img{
    max-height:100%;
    max-width: fit-content;
    max-width:100%;
    vertical-align: middle;
}

.location {
    z-index: 100;
    font-family: Arial, sans-serif;
    color: v-bind(color.locationColor[0]);
    font-size: 20px;
    text-align: left;
    margin-left: 64px;
    margin-top: 10px;
    background-color: transparent;
    z-index: -1;
}
.location-icon {
    width: 21px;
    height: 20px;
    vertical-align: middle;
    margin-left: -4px;
    margin-top: -5px;
}
</style>