<script setup>
import { useRoute, useRouter } from 'vue-router'
import { onMounted, nextTick } from 'vue';
import { ref } from 'vue';
const rawHtmlContent = ref('<p>This is a sample card content with <em>italic text</em> and <strong>bold text</strong>.</p>');
let props = defineProps({
  cardInfo: Object,
  SetToEdit: Array,
  viewMode: Boolean,
});

useRouter(); 
useRoute();

onMounted(async () => {
    await nextTick();
    let editButton = document.getElementById('edit-button'); 
    // editButton.addEventListener("click", function () {
    //     console.log("Edit button clicked");
    //     props.SetToEdit[0] = true;
    // });
});

function changeToEditMode(){
    props.SetToEdit[0] = true;
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
    <div v-if="mobileMode" class="card-color-surround">
        <div class="card" style="width:100%; padding-top:0;">
            <div v-if="props.cardInfo.conditions.header[0]"  class="title-outline" style="width:calc(100% - 10px); margin-left:10px;">
                <div class="title" style="overflow:hidden;">
                    {{ props.cardInfo.header[0] }}
                </div>
            </div>
            <!-- <div class="gap"></div> -->
            <div class="details">
                <div v-if="props.cardInfo.conditions.paragraph[0] && !props.cardInfo.conditions.image[0]">
                    <div id="description-container" style="margin:auto;display:block; width:95%">
                        <div class="description" style="width:90%; " >{{props.cardInfo.paragraph[0]}}</div>
                    </div>
                </div>
                <div v-else-if="!props.cardInfo.conditions.paragraph[0] && props.cardInfo.conditions.image[0]" style="margin:auto;display:block;width:fit-content;">
                
                        <div class="image-space" style="margin:auto; width:100%; height:auto;">
                            <img :id="'main-card-image-'+props.index" class="image" :src="props.cardInfo.image[0]" style="width:100%;"/>
                        <!-- <img @click="changeImage" class="image-edit-faint" src="@/assets/founder-space/edit/image-edit-faint.png" /> -->
                    </div>
                </div>
                <div v-else-if="props.cardInfo.conditions.paragraph[0] && props.cardInfo.conditions.image[0] && props.cardInfo.conditions.leftRightRelation[0] === true">
                    <div id="description-container" style="margin:auto;display:block; width:90%">
                        <div class="description" style="width:100%; " >{{props.cardInfo.paragraph[0]}}</div>
                    </div>
                    <div style="margin:auto;">
                        <div class="image-space" style="margin:auto; width:100%; height:auto;">
                            <img :id="'main-card-image-'+props.index" class="image" :src="props.cardInfo.image[0]" style="width:100%;"/>
                            <!-- <img @click="changeImage" class="image-edit-faint" src="@/assets/founder-space/edit/image-edit-faint.png" /> -->
                        </div>
                    </div>
                </div>
                <div v-else-if="props.cardInfo.conditions.paragraph[0] && props.cardInfo.conditions.image[0] && !props.cardInfo.conditions.leftRightRelation[0]">
                    <div style="margin:auto;">
                        <div class="image-space" style="margin:auto; width:100%; height:auto;">
                            <img :id="'main-card-image-'+props.index" class="image" :src="props.cardInfo.image[0]" style="width:100%;"/>
                            <!-- <img @click="changeImage" class="image-edit-faint" src="@/assets/founder-space/edit/image-edit-faint.png" /> -->
                        </div>
                    </div>
                    <div id="description-container" style="margin:auto;display:block; width:90%">
                        <div class="description" style="width:100%; " >{{props.cardInfo.paragraph[0]}}</div>
                    </div>
                </div>
                
            </div>
            <img v-if="!props.viewMode" @click="changeToEditMode" id="edit-button" class="edit-button" src="@/assets/founder-space/edit/edit-icon.png"/>
        </div>
    </div>
    <div v-else class="card-color-surround">
        <div class="card">
            <div v-if="props.cardInfo.conditions.header[0]"  class="title-outline">
                <div class="title" style="overflow:hidden;">
                    {{ props.cardInfo.header[0] }}
                </div>
            </div>
            <div class="gap"></div>
            <div class="details">
                <div v-if="props.cardInfo.conditions.paragraph[0] && !props.cardInfo.conditions.image[0]">
                    <div id="description-container" style="margin:auto;display:block;">
                        <div class="description" >{{props.cardInfo.paragraph[0]}}</div>
                    </div>
                </div>
                <div v-else-if="!props.cardInfo.conditions.paragraph[0] && props.cardInfo.conditions.image[0]" style="margin:auto;display:block;width:fit-content;">
                    <div class="image-space">
                        <img :id="'main-card-image-'+props.index" class="image" :src="props.cardInfo.image[0]"/>
                        <!-- <img @click="changeImage" class="image-edit-faint" src="@/assets/founder-space/edit/image-edit-faint.png" /> -->
                    </div>
                </div>
                <div v-else-if="props.cardInfo.conditions.paragraph[0] && props.cardInfo.conditions.image[0] && props.cardInfo.conditions.leftRightRelation[0] === true">
                    <div id="description-container">
                        <div class="description" >{{props.cardInfo.paragraph[0]}}</div>
                    </div>
                    <div style="margin-left: 38px;" class="inline-correction">
                        <div class="image-space">
                            <img :id="'main-card-image-'+props.index" class="image" :src="props.cardInfo.image[0]" />
                            <!-- <img @click="changeImage" class="image-edit-faint" src="@/assets/founder-space/edit/image-edit-faint.png" /> -->
                        </div>
                    </div>
                </div>
                <div v-else-if="props.cardInfo.conditions.paragraph[0] && props.cardInfo.conditions.image[0] && !props.cardInfo.conditions.leftRightRelation[0]">
                    <div style="margin-left: 58px;" class="inline-correction">
                        <div class="image-space">
                            <img :id="'main-card-image-'+props.index" class="image" :src="props.cardInfo.image[0]" />
                            <!-- <img @click="changeImage" class="image-edit-faint" src="@/assets/founder-space/edit/image-edit-faint.png" /> -->
                        </div>
                    </div>
                    <div style="width: calc(100% - min(25vw, 500px) - 238px);" id="description-container">
                        <div class="description" >{{props.cardInfo.paragraph[0]}}</div>
                    </div>
                </div>
                
            </div>
            <img v-if="!props.viewMode" @click="changeToEditMode" id="edit-button" class="edit-button" src="@/assets/founder-space/edit/edit-icon.png"/>
        </div>
    </div>
</template>

<style scoped>
.edit-button{
    position: relative;
    width: 60px;
    height: 60px;
    float: right;
    margin-top: -80px;
    border-radius: 50%;
    border: black solid 2px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.671);
    background-image: linear-gradient(45deg, black, rgb(94, 94, 94));
    cursor: pointer;
    z-index: 0;
    margin-right: 70px;
}popup-text{
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
#description-container {
    display: inline-block;
    width: calc(100% - min(25vw, 500px) - 220px);
    vertical-align:middle;
    outline:none;
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
    margin-top: -20px;
    padding-bottom: 50px;
}
.image-space {
    outline: none;
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
    outline: hidden;
    width: calc(100% - 180px);
    margin-bottom: -50px;
    z-index: 0;
    background-color: transparent;
    text-align: left;

}
.title {
    z-index: 1;
    font-family: Arial, Helvetica, sans-serif;
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
    height:auto;
    padding-top: 0px !important;
    padding-bottom:60px;
    text-align: left;   
}


.card-color-surround{
    background-color: v-bind(cardInfo.backgroundColor[0]);
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