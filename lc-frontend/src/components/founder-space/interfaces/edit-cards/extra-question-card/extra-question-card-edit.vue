<script setup>
import { useRoute, useRouter } from 'vue-router'
import { onMounted } from 'vue';
import { ref, nextTick, watch } from 'vue';
import locationDatabase from '@/components/supporting-components/location-database.vue';
import ImageEditorPopUp from '@/components/founder-space/interfaces/edit-cards/image-replace/pop-up.vue';
import colorChangePopup from '@/components/founder-space/interfaces/edit-cards/color-change/popup-added-card.vue';
import { supabase } from "@/lib/supabase";
const route = useRoute();
const imageEditMode = ref(false);
const backDropClick = ref([false]);
const backDropClickColor = ref([false]);
const colorEditMode = ref(false);
const saveResults = ref([false, null]);
const color = ref(["rgb(0, 26, 255)"]);
const removeCardPopup = ref(false);
let originCard = null;
let props = defineProps({
  cardInfo: Object,
  SetToEdit: Array,
  extraCards: Array,
  key: Number
});

let dummyCardInfo = ref({
    conditions:{
        header:[true],
        paragraph:[true],
        image:[true],
        leftRightRelation:[false]
    },
    header: ["How do you plan to use the funds?"],
    paragraph: ["We plan to use the funds to expand our team and accelerate product development."],
    image: ["https://styles.redditmedia.com/t5_2qh1u/styles/communityIcon_21ykcg22rm6c1.png?width=128&frame=1&auto=webp&s=ed570cc1fa570576ed77f45ce8490b9f41c89cdc"],
    leftRightRelation: [null],
    backgroundColor: ["white"],
    textColor: ["#000000"],
    headerColor: ["#000000"],
    markedForDeletion: [false],
    id: 1,
    recentlySpawned: [false]
});

onMounted(async () => {

    dummyCardInfo.value = JSON.parse(JSON.stringify(props.cardInfo));

    await nextTick();
    
    contentWithLineBreaks.value = dummyCardInfo.value.paragraph[0].replace("<pre id='desc-text'>", '').replace("</pre>", '');
    
    titleTextAreaAdjust(document.getElementById(`main-title-${dummyCardInfo.value.id}`));
    descriptionTextAreaAdjust(document.getElementById(`main-description-${dummyCardInfo.value.id}`));

    if(dummyCardInfo.value.conditions.header[0]){
        document.getElementById(`main-title-${dummyCardInfo.value.id}`).addEventListener("input", updateTitle);
    }
    if(dummyCardInfo.value.conditions.paragraph[0]){
        document.getElementById(`main-description-${dummyCardInfo.value.id}`).addEventListener("input", updateDescription);
    }
    if(dummyCardInfo.value.conditions.image[0]){
        document.getElementById(`main-card-image-${dummyCardInfo.value.id}`).addEventListener("input", updateImage);
    }

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

function obtainObjectImage(url){
    if(url.indexOf("blob:") === 0){
        return url;
    } else {
        return getImageBlob(url);
    }
}

function genearteNewURLEnding(oldURLEnding) {
    console.log(props.key);
    let newString = String(props.cardInfo.id)+":::"+Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
    while(newString === oldURLEnding){
        newString = "main" + Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
    }
    return newString;
}

async function uploadProfileImage(blob, projectId, new_ending){

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

async function saveCard(){
    if(imageChangeInfo.url[0] != null){
        let image_url_ending = props.cardInfo.image[0]== "" ? "" : props.cardInfo.image[0].split("/").slice(-1)[0].split(".")[0];
        let new_ending = genearteNewURLEnding(image_url_ending);
        let old_url = props.cardInfo.image[0].split("/").slice(-2)[0]+"/"+props.cardInfo.image[0].split("/").slice(-1)[0];
        console.log(old_url);
        if(props.cardInfo.image[0] != ""){
            try{
                await supabase.storage.from("project_page_images").remove([old_url]); // note: array of file paths
            }
            catch(err){
                console.log("No existing profile image to delete, proceeding with upload.");
            }
        }
        let image_blob = null;
        try{
            image_blob = await fetch(imageChangeInfo.url[0]).then(r => r.blob());
        }catch(e){
            let response = await fetch(`${import.meta.env.VITE_CORS_PROXY_URL}${encodeURIComponent(imageChangeInfo.url[0])}`);
            console.log(response);
            if (!response.ok) {
                image_blob = null;
            }else{
                image_blob = response.blob();
            }
        }
        if(image_blob != null){
            let image_url = await uploadProfileImage(image_blob, route.params.projectId, new_ending);
            props.cardInfo.image[0] = image_url;
        }else{
            props.cardInfo.image[0] = imageChangeInfo.url[0];
            
        }
    }

    props.cardInfo.conditions = dummyCardInfo.value.conditions;
    props.cardInfo.header = dummyCardInfo.value.header;
    props.cardInfo.paragraph = dummyCardInfo.value.paragraph;
    props.cardInfo.backgroundColor = dummyCardInfo.value.backgroundColor;
    props.cardInfo.textColor = dummyCardInfo.value.textColor;
    props.cardInfo.headerColor = dummyCardInfo.value.headerColor;
    props.cardInfo.markedForDeletion = dummyCardInfo.value.markedForDeletion;
    props.cardInfo.id = dummyCardInfo.value.id;
    props.cardInfo.recentlySpawned = dummyCardInfo.value.recentlySpawned;

    props.SetToEdit[0] = false;
}

function cancel(){
    props.SetToEdit[0] = false;
    dummyCardInfo.value.recentlySpawned[0] = false;
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
    colorEditMode.value = true;
}

async function descriptionTextAreaAdjust(element) {
  element.style.height = "1px";
  await nextTick();
  let height = 0;
  if(!mobileMode.value){
    height = Math.max(element.scrollHeight, 300);
  }else{
    height = (element.scrollHeight);
  }
  document.getElementById(`main-description-${dummyCardInfo.value.id}`).style.height = (25+height)+"px";
  element.style.height = (25+height)+"px";
}

function titleTextAreaAdjust(element) {
  element.value = element.value.replace(/\n/g, '');
  element.style.height = "1px";
  let height = (25+element.scrollHeight-25);
  document.getElementById(`main-title-container-${dummyCardInfo.value.id}`).style.height = (height-60)+"px";
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
            document.getElementById(`main-card-image-${dummyCardInfo.value.id}`).src = newVal[1];
            dummyCardInfo.value.image[0] = newVal[1];
            saveResults.value = [false, null];
        }, time);
    }
},{deep: true});

async function addTitle(){
    dummyCardInfo.value.conditions.header[0] = !dummyCardInfo.value.conditions.header[0];
    await nextTick();
    titleTextAreaAdjust(document.getElementById(`main-title-${dummyCardInfo.value.id}`));
    if(dummyCardInfo.value.conditions.header[0]){
        document.getElementById(`main-title-${dummyCardInfo.value.id}`).addEventListener("input", updateTitle);
    }else{
        document.getElementById(`main-title-${dummyCardInfo.value.id}`).removeEventListener("input", updateTitle);
    }
}

async function addParagraph(){
    dummyCardInfo.value.conditions.paragraph[0] = !dummyCardInfo.value.conditions.paragraph[0];
    await nextTick();
    descriptionTextAreaAdjust(document.getElementById(`main-description-${dummyCardInfo.value.id}`));
    if(dummyCardInfo.value.conditions.paragraph[0]){
        document.getElementById(`main-description-${dummyCardInfo.value.id}`).addEventListener("input", updateDescription);
    }else{
        document.getElementById(`main-description-${dummyCardInfo.value.id}`).removeEventListener("input", updateDescription);
    }
    
}

function updateDescription(){
    contentWithLineBreaks.value = document.getElementById(`main-description-${dummyCardInfo.value.id}`).value;
    dummyCardInfo.value.paragraph[0] = document.getElementById(`main-description-${dummyCardInfo.value.id}`).value;
    console.log("Description updated:", document.getElementById(`main-description-${dummyCardInfo.value.id}`).value);
}
function updateTitle(){
    dummyCardInfo.value.header[0] = document.getElementById(`main-title-${dummyCardInfo.value.id}`).value;
    console.log("Title updated:", document.getElementById(`main-title-${dummyCardInfo.value.id}`).value);
}
function updateImage(){
    dummyCardInfo.value.image[0] = document.getElementById(`main-card-image-${dummyCardInfo.value.id}`).value;
    console.log("Image updated:", document.getElementById(`main-card-image-${dummyCardInfo.value.id}`).value);
}

async function addImage(){
    dummyCardInfo.value.conditions.image[0] = !dummyCardInfo.value.conditions.image[0];
    await nextTick();
    if(dummyCardInfo.value.conditions.image[0]){
        document.getElementById(`main-card-image-${dummyCardInfo.value.id}`).addEventListener("input", updateImage);
    }else{
        document.getElementById(`main-card-image-${dummyCardInfo.value.id}`).removeEventListener("input", updateImage);
    }
}
function addLeftRightRelation(){
    if(dummyCardInfo.value.conditions.image[0] && dummyCardInfo.value.conditions.paragraph[0] && !dummyCardInfo.value.conditions.leftRightRelation[0]){
        dummyCardInfo.value.conditions.leftRightRelation[0] = true;
    }
}

function addRightLeftRelation(){
    if(dummyCardInfo.value.conditions.image[0] && dummyCardInfo.value.conditions.paragraph[0] && dummyCardInfo.value.conditions.leftRightRelation[0]){
        dummyCardInfo.value.conditions.leftRightRelation[0] = false;
    }
}

function deleteCard(event){
    removeCardPopup.value = true;
}

function verifiedRemoval(){
    let index = props.extraCards.findIndex(card => card.id === props.cardInfo.id);
    props.extraCards.splice(index, 1);
    props.SetToEdit[0] = false;
    removeCardPopup.value = false;
}

function Cancelation(){
    removeCardPopup.value = false;
}

function mobileModeListener(){
    mobileMode.value = window.innerWidth <= 1200;
    console.log("Mobile mode:", mobileMode.value);
}

let mobileMode = ref(true)
mobileMode.value = window.innerWidth <= 1200;
window.addEventListener('resize', mobileModeListener);

</script>

<template>
    <colorChangePopup v-if="colorEditMode" :backDropClickColor="backDropClickColor" :cardInfo="dummyCardInfo" />
    <ImageEditorPopUp v-if="imageEditMode" :backDropClick="backDropClick" :saveResults="saveResults" :imageInfo="imageChangeInfo"/>
    <div v-if="removeCardPopup" class="pop-up-backdrop">
        <div class="custom-alert-popup">
            <div class="alert-content">
                <h2 class="popup-text">Are you sure you'd like to delete this card?</h2>
                <button class="popup-button" @click="verifiedRemoval">Yes</button>
                <button class="popup-button" @click="Cancelation">No</button>
            </div>
        </div>
    </div>
    <div v-if="mobileMode" class="card-color-surround" :style="{background: dummyCardInfo.backgroundColor[0]}">
        <div class="card" style="width:90%">
            <div class="float-correction" style="width:100%; margin-left:0;">
                <div class="toolbar">
                    <img @click="addTitle" :style="dummyCardInfo.conditions.header[0] ? 'opacity: 1' : 'opacity: .5'"  src="@/assets/founder-space/edit/added-card-edit/title.png" class="button" />
                    <img @click="addParagraph" :style="dummyCardInfo.conditions.paragraph[0] ? 'opacity: 1' : 'opacity: .5'"  src="@/assets/founder-space/edit/added-card-edit/paragraph.png" class="button" />
                    <img @click="addImage" :style="dummyCardInfo.conditions.image[0] ? 'opacity: 1' : 'opacity: .5'"  src="@/assets/founder-space/edit/added-card-edit/image.svg" class="button" />
                    <div class="image-text-relation-tray">
                        <img @click="addRightLeftRelation" :style="!dummyCardInfo.conditions.leftRightRelation[0] && dummyCardInfo.conditions.image[0] && dummyCardInfo.conditions.paragraph[0] ? 'opacity: 1' : 'opacity: .5'" src="@/assets/founder-space/edit/added-card-edit/left-right.png" class="button"/>
                        <img @click="addLeftRightRelation" :style="dummyCardInfo.conditions.leftRightRelation[0] && dummyCardInfo.conditions.image[0] && dummyCardInfo.conditions.paragraph[0] ? 'opacity: 1' : 'opacity: .5'" src="@/assets/founder-space/edit/added-card-edit/right-left.png" class="button"/>
                    </div>
                </div>
            </div>
            <div v-if="dummyCardInfo.conditions.header[0]" class="title-outline" :id="`main-title-container-${dummyCardInfo.id}`" style="margin-left:0; width:100%">
                <textarea :id="`main-title-${dummyCardInfo.id}`" class="title" @keypress='titleTextAreaAdjust($event.target)' @keyup='titleTextAreaAdjust($event.target)' @keydown='titleTextAreaAdjust($event.target)' style="overflow:hidden" :style="{color: dummyCardInfo.headerColor[0]}">{{ dummyCardInfo.header[0] }}</textarea>
            </div>
            <div class="gap"></div>
            <div class="details">
                <div v-if="dummyCardInfo.conditions.paragraph[0] && !dummyCardInfo.conditions.image[0]">
                                        <!-- <div id="description-container" style="margin:auto;display:block; width:95%"> -->

                    <div :id="`main-description-container-${dummyCardInfo.id}`" style="margin:auto;display:block;width:95%" class="description-container">
                        <textarea :id="`main-description-${dummyCardInfo.id}`" @keypress='descriptionTextAreaAdjust($event.target)' @keyup='descriptionTextAreaAdjust($event.target)' @keydown='descriptionTextAreaAdjust($event.target)' class="description" :style="{color: dummyCardInfo.textColor[0]}">{{contentWithLineBreaks}}</textarea>
                    </div>
                </div>
                <div v-else-if="!dummyCardInfo.conditions.paragraph[0] && dummyCardInfo.conditions.image[0]" style="margin:auto;display:block;width:fit-content;">
                    <div class="image-space" style="margin:auto; width:100%; height:auto;">
                        <img :id="'main-card-image-'+dummyCardInfo.id" class="image" :src="dummyCardInfo.image[0]" style="width:100%;"/>
                        <img @click="changeImage" class="image-edit-faint" src="@/assets/founder-space/edit/image-edit-faint.png" />
                    </div>
                </div>
                <div v-else-if="dummyCardInfo.conditions.paragraph[0] && dummyCardInfo.conditions.image[0] && dummyCardInfo.conditions.leftRightRelation[0] === true">
                    
                    <div id="description-container" style="margin:auto;display:block; width:100%; margin-top:-20px; outline:auto;">
                        <textarea style="width:100%" :id="`main-description-${dummyCardInfo.id}`" @keypress='descriptionTextAreaAdjust($event.target)' @keyup='descriptionTextAreaAdjust($event.target)' @keydown='descriptionTextAreaAdjust($event.target)' class="description" >{{contentWithLineBreaks}}</textarea>
                    </div>
                    <div style="margin:auto; margin-top:20px;">
                        <div class="image-space" style="margin:auto; width:100%; height:auto;">
                            <img :id="'main-card-image-'+dummyCardInfo.id" class="image" :src="dummyCardInfo.image[0]" style="width:100%"/>
                            <img @click="changeImage" class="image-edit-faint" src="@/assets/founder-space/edit/image-edit-faint.png" />
                        </div>
                    </div>
                </div>
                <div v-else-if="dummyCardInfo.conditions.paragraph[0] && dummyCardInfo.conditions.image[0] && !dummyCardInfo.conditions.leftRightRelation[0]">
                    <div style="margin:auto;">
                        <div class="image-space" style="margin:auto; width:100%; height:auto;">
                            <img :id="'main-card-image-'+dummyCardInfo.id" class="image" :src="dummyCardInfo.image[0]" style="width:100%"/>
                            <img @click="changeImage" class="image-edit-faint" src="@/assets/founder-space/edit/image-edit-faint.png" />
                        </div>
                    </div>
                    <div id="description-container" style="margin:auto;display:block; width:100%; margin-top:20px; outline:auto;">
                        <textarea style="width:100%" :id="`main-description-${dummyCardInfo.id}`" @keypress='descriptionTextAreaAdjust($event.target)' @keyup='descriptionTextAreaAdjust($event.target)' @keydown='descriptionTextAreaAdjust($event.target)' class="description" >{{contentWithLineBreaks}}</textarea>
                    </div>
                </div>
            </div>
            <div id="hyper-buttons-left" style="width:60px; margin-left:-10px;">
                <img @click="chageColor" id="paint" src="@/assets/founder-space/edit/paint-icon.png" />
            </div>
            <div id="hyper-buttons-right" style="margin-right:-10px; width:280px">
                <img @click="saveCard" class="save" src="@/assets/founder-space/edit/save-icon.png" />
                <img @click="cancel" class="cancel" src="@/assets/founder-space/edit/x-icon.png" />
                <img @click="deleteCard" class="delete" src="@/assets/founder-space/edit/added-card-edit/trash-bin.png"/>
            </div>
        </div>
    </div>
    <div v-else class="card-color-surround" :style="{background: dummyCardInfo.backgroundColor[0]}">
        <div class="card">
            <div class="float-correction">
                <div class="toolbar">
                    <img @click="addTitle" :style="dummyCardInfo.conditions.header[0] ? 'opacity: 1' : 'opacity: .5'"  src="@/assets/founder-space/edit/added-card-edit/title.png" class="button" />
                    <img @click="addParagraph" :style="dummyCardInfo.conditions.paragraph[0] ? 'opacity: 1' : 'opacity: .5'"  src="@/assets/founder-space/edit/added-card-edit/paragraph.png" class="button" />
                    <img @click="addImage" :style="dummyCardInfo.conditions.image[0] ? 'opacity: 1' : 'opacity: .5'"  src="@/assets/founder-space/edit/added-card-edit/image.svg" class="button" />
                    <div class="image-text-relation-tray">
                        <img @click="addRightLeftRelation" :style="!dummyCardInfo.conditions.leftRightRelation[0] && dummyCardInfo.conditions.image[0] && dummyCardInfo.conditions.paragraph[0] ? 'opacity: 1' : 'opacity: .5'" src="@/assets/founder-space/edit/added-card-edit/left-right.png" class="button"/>
                        <img @click="addLeftRightRelation" :style="dummyCardInfo.conditions.leftRightRelation[0] && dummyCardInfo.conditions.image[0] && dummyCardInfo.conditions.paragraph[0] ? 'opacity: 1' : 'opacity: .5'" src="@/assets/founder-space/edit/added-card-edit/right-left.png" class="button"/>
                    </div>
                </div>
            </div>
            <div v-if="dummyCardInfo.conditions.header[0]" class="title-outline" :id="`main-title-container-${dummyCardInfo.id}`">
                <textarea :id="`main-title-${dummyCardInfo.id}`" class="title" @keypress='titleTextAreaAdjust($event.target)' @keyup='titleTextAreaAdjust($event.target)' @keydown='titleTextAreaAdjust($event.target)' style="overflow:hidden" :style="{color: dummyCardInfo.headerColor[0]}">{{ dummyCardInfo.header[0] }}</textarea>
            </div>
            <div class="gap"></div>
            <div class="details">
                <div v-if="dummyCardInfo.conditions.paragraph[0] && !dummyCardInfo.conditions.image[0]">
                    <div :id="`main-description-container-${dummyCardInfo.id}`" style="margin:auto;display:block;" class="description-container">
                        <textarea :id="`main-description-${dummyCardInfo.id}`" @keypress='descriptionTextAreaAdjust($event.target)' @keyup='descriptionTextAreaAdjust($event.target)' @keydown='descriptionTextAreaAdjust($event.target)' class="description" :style="{color: dummyCardInfo.textColor[0]}">{{contentWithLineBreaks}}</textarea>
                    </div>
                </div>
                <div v-else-if="!dummyCardInfo.conditions.paragraph[0] && dummyCardInfo.conditions.image[0]" style="margin:auto;display:block;width:fit-content;">
                    <div class="image-space">
                        <img :id="'main-card-image-'+dummyCardInfo.id" class="image" :src="dummyCardInfo.image[0]"/>
                        <img @click="changeImage" class="image-edit-faint" src="@/assets/founder-space/edit/image-edit-faint.png" />
                    </div>
                </div>
                <div v-else-if="dummyCardInfo.conditions.paragraph[0] && dummyCardInfo.conditions.image[0] && dummyCardInfo.conditions.leftRightRelation[0] === true">
                    <div :id="`main-description-container-${dummyCardInfo.id}`" class="description-container">
                        <textarea :id="`main-description-${dummyCardInfo.id}`" @keypress='descriptionTextAreaAdjust($event.target)' @keyup='descriptionTextAreaAdjust($event.target)' @keydown='descriptionTextAreaAdjust($event.target)' class="description" >{{contentWithLineBreaks}}</textarea>
                    </div>
                    <div style="margin-left: 38px;" class="inline-correction">
                        <div class="image-space">
                            <img :id="'main-card-image-'+dummyCardInfo.id" class="image" :src="dummyCardInfo.image[0]" />
                            <img @click="changeImage" class="image-edit-faint" src="@/assets/founder-space/edit/image-edit-faint.png" />
                        </div>
                    </div>
                </div>
                <div v-else-if="dummyCardInfo.conditions.paragraph[0] && dummyCardInfo.conditions.image[0] && !dummyCardInfo.conditions.leftRightRelation[0]">
                    <div style="margin-left: 58px;" class="inline-correction">
                        <div class="image-space">
                            <img :id="'main-card-image-'+dummyCardInfo.id" class="image" :src="dummyCardInfo.image[0]" />
                            <img @click="changeImage" class="image-edit-faint" src="@/assets/founder-space/edit/image-edit-faint.png" />
                        </div>
                    </div>
                    <div style="width: calc(100% - min(25vw, 500px) - 238px);" class="description-container">
                        <textarea :id="`main-description-${dummyCardInfo.id}`" @keypress='descriptionTextAreaAdjust($event.target)' @keyup='descriptionTextAreaAdjust($event.target)' @keydown='descriptionTextAreaAdjust($event.target)' class="description" >{{contentWithLineBreaks}}</textarea>
                    </div>
                </div>
            </div>
            <div id="hyper-buttons-left">
                <img @click="chageColor" id="paint" src="@/assets/founder-space/edit/paint-icon.png" />
            </div>
            <div id="hyper-buttons-right">
                <img @click="saveCard" class="save" src="@/assets/founder-space/edit/save-icon.png" />
                <img @click="cancel" class="cancel" src="@/assets/founder-space/edit/x-icon.png" />
                <img @click="deleteCard" class="delete" src="@/assets/founder-space/edit/added-card-edit/trash-bin.png"/>
            </div>
        </div>
    </div>
</template>

<style scoped>
.popup-text{
    font-family: Fantasy;
    font-size: 16px;
    margin-bottom: 20px;
    text-align: center;
    color: white;
}
.popup-button{
    font-family: Fantasy;
    width: 80px;
    height: 40px;
    margin: 10px;
    border-radius: 10px;
    border: black solid 2px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.671);
    background-image: linear-gradient(45deg, black, rgb(59, 59, 59));
    color: rgb(255, 255, 255);
    cursor: pointer;
}
.pop-up-backdrop{
    position: fixed;
    top: 0;
    left: 0;
    width: 200%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 999;
    
}
.custom-alert-popup{
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: rgb(44, 44, 44);
    padding: 20px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
    z-index: 1000;
    padding: 20px;
    display: block; /* Initially hidden */
}
.image-text-relation-tray{
    display: inline-block;
    margin-left: 5px;
    border-left:#000000 solid 5px;
    padding-left: 10px;
    border-radius: 10px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.705);
    padding: 4px;
}
.button:active{
    transform: scale(90%);
    background-color: #000000;
    box-shadow: 0 0 0 0 rgba(102, 102, 102, 0.24);
}
.button:hover{
    background-color: #ffffff;
}
.button{
    width: 30px;
    height: 30px;
    padding:10px;
    border-radius: 5px;
    border: solid #000000 1px;
    margin-right:5px;
    background-color: #ffffff8c;
    padding: 5px;
    border: rgb(0, 0, 0) solid 3px;
    background-color:white; filter: invert(1);
}
.float-correction{
    margin-top: 20px;
    margin-left: 60px;
    position: absolute;
    width: fit-content;
    background-color: rgba(0, 0, 0, 0);
    height: 65px;
    z-index: 10;
    height: fit-content;
    z-index: 0;
}
.toolbar{
    background-color: #00000000;
    border-radius: 10px;
    overflow: hidden;
    width:fit-content;
    height:60px;
    padding:-10px;
    padding-top: 10px;
    padding-right: 10px;
    margin-left: 0px;
    float: left;
    left:0;
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
    width: 280px;
    height:100px;
    padding-bottom: 100px;
    z-index:100;
    margin-right: 70px;
}
.save{
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
.cancel{
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
.delete{
    float:right;
    width:60px;
    height:60px;
    border: rgb(255, 255, 255) solid 2px;
    box-shadow: 0px 0px 10px rgba(255, 255, 255, 0.671);
    background-image: linear-gradient(45deg, rgb(255, 255, 255), rgb(184, 184, 184));
    filter: invert(1);
    border-radius: 50%;
    cursor:pointer;
}
.details {
    text-align: left;
    margin-left: 60px;
    padding-bottom:180px;
    padding-top: 80px;
    height: auto;
    resize: none;
    margin:auto;
}
.description-container {
    display: inline-block;
    width: calc(100% - min(25vw, 500px) - 220px);
    margin-top: 0px;
    vertical-align:middle;
    outline:auto;
    height:fit-content;
    margin:auto;
    
    margin-left: 58px;
}
.description {
    width:100%;
    font-family: Arial, sans-serif;
    color: v-bind(cardInfo.textColor[0]);
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
    height:40px;
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
    margin-top:120px;
    margin-left: 58px;
    outline: auto;
    width: calc(100% - 180px);
    margin-bottom: -50px;
    z-index: 0;
    background-color: rgba(0, 0, 0, 0);

}
.title {
    z-index: 1;
    font-family: fantasy;
    color: v-bind(cardInfo.headerColor[0]);
    font-size: 30px;
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
    padding-top:50px;
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
    color: #666;
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