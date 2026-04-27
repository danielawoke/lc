<script setup>
import { useRoute, useRouter } from 'vue-router'
import { onMounted, nextTick } from 'vue';
import { ref } from 'vue';
const rawHtmlContent = ref('<p>This is a sample card content with <em>italic text</em> and <strong>bold text</strong>.</p>');
let props = defineProps({
  mainCardData: Object,
  SetToEdit: Array,
    viewMode: Boolean
});

useRouter(); 
useRoute();

onMounted(async () => {
    await nextTick();
    // console.log("Main card edit mounted with data:", props.mainCardData.image);
    console.log(props.mainCardData.content);

});


function mobileModeListener(){
    mobileMode.value = window.innerWidth <= 1200;
    console.log("Mobile mode:", mobileMode.value);
}

let mobileMode = ref(true)
mobileMode.value = window.innerWidth <= 1200;
window.addEventListener('resize', mobileModeListener);




</script>

<template>
    
    <div v-if="mobileMode" class="card-color-surround" :style="{backgroundColor: mainCardData.color.backgroundColor}">
        <div class="card" style="padding:0; width:100%">
            <div class="title"  :style="{color: mainCardData.color.titleColor[0]}">
                {{ mainCardData.title }}
            </div>
            <div v-if="!mainCardData.physicalLocation" class="location">
                <img class="location-icon" src="@/assets/location.png" />
                <div class="location-text" :style="{color: mainCardData.color.locationColor[0]}">
                    {{ mainCardData.location }}
                </div>
            </div>
            <div v-if="mainCardData.remote" class="remote-option"><img class="remote-image" src="https://cdn-icons-png.flaticon.com/512/3759/3759392.png">Remote</div>
            <div class="image-space" style="margin:auto; margin-top:10px; width: 100%;">
                <img class="image" :src="mainCardData.image" />
            </div>
            <div class="description" :style="{color: mainCardData.color.contentColor[0]}" style="padding:0; width:95%; text-align: left;">
                <div v-html="mainCardData.content"></div>
            </div>
            <div style="height:50px;"></div>
            <img v-if="!props.viewMode" id="edit-button" @click="props.SetToEdit[0] = true" class="edit-button" src="@/assets/founder-space/edit/edit-icon.png"/>
        </div>
    </div>
    <div v-else class="card-color-surround" :style="{backgroundColor: mainCardData.color.backgroundColor}">
        <div class="card">
            <div class="title"  :style="{color: mainCardData.color.titleColor[0]}">
                {{ mainCardData.title }}
            </div>
            <div v-if="!mainCardData.physicalLocation" class="location">
                <img class="location-icon" src="@/assets/location.png" />
                <div class="location-text" :style="{color: mainCardData.color.locationColor[0]}">
                    {{ mainCardData.location }}
                </div>
            </div>
            <div v-if="mainCardData.remote" class="remote-option"><img class="remote-image" src="https://cdn-icons-png.flaticon.com/512/3759/3759392.png">Remote</div>
            <div class="details">
                <div class="inline-correction">
                    <div class="image-space">
                        <img class="image" :src="mainCardData.image" />
                    </div>
                </div>
                <div class="description" :style="{color: mainCardData.color.contentColor[0]}">
                    <div v-html="mainCardData.content"></div>
                </div>
            </div>
            <img v-if="!props.viewMode" id="edit-button" @click="props.SetToEdit[0] = true" class="edit-button" src="@/assets/founder-space/edit/edit-icon.png"/>
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
    margin-left: 58px;
    margin-top: 10px;
    background-color: rgb(255, 255, 255);
    border-radius: 10px;
    width:fit-content;

    padding: 5px 5px 5px 5px;

}
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
    z-index: 10;
    margin-right: 70px;
}
.location-text {
    display: inline-block;
    width: calc(100% - 40px);
    font-family: Arial, sans-serif;
    color: #666;
    font-size: 20px;
    vertical-align: text-top;
    margin-left:5.5px;
}
.inline-correction {
    display: inline-block;
    
    vertical-align: top;
    
}
.card-color-surround{
    background-color: v-bind(color);
}
.card{
    width: calc( (100% - 180px) );
    height: auto;
    max-width: 1600px;
    border-radius: 10px;
    padding: 20px;
    margin: auto;
}
img{
    max-height:100%;
    max-width: fit-content;
    max-width:100%;
    vertical-align: middle;
}
.image-space {
    display: flex;
    justify-content: center; 
    align-items: center; 
    width: 25vw;
    max-width: 500px;
    height: 400px;
    background-color: rgba(153, 43, 24, 0);
}
.description {
    display: inline-block;
    color: #444;
    font-size: 18px;
    line-height: 1.6;
    width: calc(100% - min(25vw, 500px) - 180px);
}

.details {
    margin-top: 85px;
    height:auto;
    text-align: left;
    margin-left: 60px;
    overflow: hidden;
    padding-bottom:70px;
}
.title {
    font-weight: bold;
    font-family: 'arial', sans-serif;
    color: #333;
    font-size: 50px;
    margin-left: 60px;
    padding-top:60px;
    width: calc(100% -60px);
    height:auto;
    overflow-wrap: break-word;
    text-align: left;
    
}
.location {
    font-family: Arial, sans-serif;
    color: #666;
    font-size: 20px;
    text-align: left;
    margin-left: 60px;
    margin-top: 10px;
}
.location-icon {
    width: 21px;
    height: 20px;
    vertical-align: middle;
    margin-right: 10px;
    margin-top: -5px;
}
</style>

<style>
.desc-text{
    font-family: Arial, Helvetica, sans-serif;
    color: #444;
    font-size: 18px;
    line-height: 1.6;
    font-weight: normal;
}
</style>