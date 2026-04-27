<script setup>
import { useRoute, useRouter } from 'vue-router'
import { onMounted, nextTick } from 'vue';
import { ref } from 'vue';
const rawHtmlContent = ref('<p>This is a sample card content with <em>italic text</em> and <strong>bold text</strong>.</p>');
let props = defineProps({
  color: Object,
});

useRouter(); 
useRoute();

onMounted(async () => {
    await nextTick();
    adjustFontSizes();
    window.addEventListener('resize', adjustFontSizes);
});

function adjustFontSizes() {
    let containerWidth = document.getElementById('main-card-mini-view').offsetWidth;
    document.getElementById('job-card-mini-view-title').style.fontSize = (containerWidth * 0.06) + "px";
    document.getElementById('job-card-mini-view-details').style.fontSize = (containerWidth * 0.04) + "px";
}
</script>

<template>
    <div id="main-card-mini-view" class="card">
        <div class="role">
            <div id="job-card-mini-view-title" class="role-title">Dirt Engineer</div>
            <div id="job-card-mini-view-details" class="role-description">Lorem ipsum, dolor sit amet laboriosam!</div>
        </div>
    </div>
</template>

<style scoped>
#main-card-mini-view{
    width:100%;
        height: 100%;
    background-color: v-bind(color.backgroundColor[0]);
}
.role-title{
    white-space: wrap;
    font-family: sans-serif;
    font-size: 10px;
    font-weight: bold;
    color:v-bind(color.textColor[0]);
    text-align: left;

}
.role-description{
    white-space: wrap;
    font-family: sans-serif;
    font-size: 7px;
    color:v-bind(color.textColor[0]);
    text-align: left;
    padding-left: 5px;
    margin-top: 5px;
    overflow: hidden;
    text-break: break-word;
}
.role{
    width: 60%;
    margin: auto;
    aspect-ratio: 1 / 2;
    height: 30%;
    margin-top: 30%;
    margin-left: 10%;
    background-color: v-bind(color.jobCardColor[0]);
    padding:10px;
    border-radius: 10px;
    display: inline-block;
    position: relative;
    float: left;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.671);
}
.card-color-surround{
    background-color: v-bind(color);
}
.card{
    width:70%;
    height: auto;
    aspect-ratio: 1 / 1;
    margin: auto;
    padding-bottom: 15%;
}
img{
    max-height:100%;
    max-width: fit-content;
    max-width:100%;
    vertical-align: middle;
}
.image-space {
    display: inline-block;
    justify-content: center; 
    align-items: center; 
    aspect-ratio: 4 / 5;
    background-color: rgba(153, 43, 24, 0);
    /*width: 80%;
    margin: auto;*/
}
.inline-correction {
    display: inline-block;
    vertical-align: top;
    width:35%;
    margin-top: 5%;
    
}
.description {
    display: inline-block;
    font-family: Arial, sans-serif;
    color: #444;
    
    line-height: 1.6;
    margin-left: 5%;
    width: 55%;
}
#desc-text{
    font-family: fantasy;
    color: #444;
    line-height: 1.6;
    background-color: transparent;
    
}
.details {
    height:auto;
    text-align: left;
    overflow: hidden;
    width: 100%;
    margin-top: -15%;
}
.title {
    display: block;
    font-weight: bold;
    font-family: fantasy;
    color: #333;
    width: calc(80%);
    height:auto;
    text-align: left;
}
.location {
    position: relative;
    font-family: Arial, sans-serif;
    color: #666;
    text-align: left;
    width:100%;
    word-break: break-word;
    display: block;
}
.location-icon {
    width: 2%;
    aspect-ratio: 1 / 1;
    height: auto;
    vertical-align: top;
}
.location-text {
    display: inline-block;
    width: 75%;
    font-family: Arial, sans-serif;
    color: #666;
    margin-left: 2%;
    vertical-align: top;
    height: auto
}
</style>
