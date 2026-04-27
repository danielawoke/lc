<script setup>
import { useRoute, useRouter } from 'vue-router'
import { onMounted, nextTick } from 'vue';
import { ref } from 'vue';
const rawHtmlContent = ref('<p>This is a sample card content with <em>italic text</em> and <strong>bold text</strong>.</p>');
let props = defineProps({
  title: String,
  content: String,
  image: String,
  location: String,
  color: Object
});

useRouter(); 
useRoute();

onMounted(async () => {
    await nextTick();
    adjustFontSizes();
});

function adjustFontSizes() {
    let containerWidth = document.getElementById('main-card-mini-view').offsetWidth;
    document.getElementById('main-card-mini-view-title').style.fontSize = (containerWidth * 0.05) + "px";
    document.getElementById('main-card-mini-view-location').style.fontSize = (containerWidth * 0.02) + "px";
    document.getElementById('main-card-mini-view-details').style.fontSize = (containerWidth * 0.02) + "px";
}
</script>

<template>
    <div id="main-card-mini-view" class="card">
        <div id="main-card-mini-view-title" class="title">
            {{ title }}
        </div>
        <div class="location">
            <img class="location-icon" src="@/assets/location.png" />
            <div id="main-card-mini-view-location" class="location-text">
                {{ location }}
            </div>
        </div>
        <div id="main-card-mini-view-details" class="details">
            <div class="inline-correction">
                <div class="image-space">
                    <img class="image" :src="image" />
                </div>
            </div>
            <div class="description" v-html="content"></div>
        </div>
    </div>
</template>

<style scoped>
.card-color-surround{
    background-color: v-bind(props.color.backgroundColor[0]);
}
.card{
    width:70%;
    height: auto;
    aspect-ratio: 1 / 1;
    background-color: v-bind(props.color.backgroundColor[0]);
    margin: auto;
    margin-top: 5%;
    border-radius: 50%;
    padding-left: 10%;
    padding-right: 10%;
    padding-top: 20%;
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
    color: v-bind(props.color.contentColor[0]);
    
    line-height: 1.6;
    margin-left: 5%;
    width: 55%;
}
#desc-text{
    font-family: fantasy;
    color: v-bind(props.color.contentColor[0]);
    line-height: 1.6;
    background-color: transparent;
    
}
.details {
    height:auto;
    text-align: left;
    overflow: hidden;
    width: 100%;
    margin-top: -15%;
    color: v-bind(props.color.titleColor[0]);
}
.title {
    display: block;
    font-weight: bold;
    font-family: fantasy;
    color: v-bind(props.color.titleColor[0]);
    width: calc(80%);
    height:auto;
    text-align: left;
}
.location {
    position: relative;
    font-family: Arial, sans-serif;
    color: v-bind(props.color.locationColor[0]);
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
