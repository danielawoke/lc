<script setup>
import { useRoute, useRouter } from 'vue-router'
import { onMounted, nextTick } from 'vue';
import { ref } from 'vue';
const rawHtmlContent = ref('<p>This is a sample card content with <em>italic text</em> and <strong>bold text</strong>.</p>');
let props = defineProps({
  cardInfo: Object
});

useRouter(); 
useRoute();

onMounted(async () => {
    await nextTick();
    adjustFontSizes();
});

function adjustFontSizes() {
    let containerWidth = document.getElementById('main-card-mini-view').offsetWidth;
    document.getElementById('main-card-mini-view-title').style.fontSize = (containerWidth * .2) + "px";
    document.getElementById('main-card-mini-view-location').style.fontSize = (containerWidth * .13) + "px";
    document.getElementById('main-card-mini-view-details').style.fontSize = (containerWidth * 0.1) + "px";
}
</script>

<template>
    <div id="main-card-mini-view" class="card">
        <div id="main-card-mini-view-title" class="title">
            Title 
        </div>
        <div id="main-card-mini-view-details" class="description">
            Content
        </div>
    </div>
</template>

<style scoped>
.card-color-surround{
    background-color: v-bind(props.cardInfo.backgroundColor[0]);
}
.card{
    width:100%;
    height: auto;
    aspect-ratio: 1 / 1;
    background-color: v-bind(props.cardInfo.backgroundColor[0]);
    border-radius: 50%;
    padding: 10%;
    margin: -10%;
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
    vertical-align: top;
    width:35%;
    margin-top: 5%;
    
}
.description {
    font-family: Arial, sans-serif;
    color: v-bind(props.cardInfo.textColor[0]);
    line-height: 1.6;
}
#desc-text{
    font-family: fantasy;
    color: v-bind(props.cardInfo.textColor[0]);
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
    color: v-bind(props.cardInfo.headerColor[0]);
    margin:auto;
    height:auto;
    text-align: center;
    margin-top: 15%;
}
.location {
    position: relative;
    font-family: Arial, sans-serif;
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
    font-family: Arial, sans-serif;
    vertical-align: top;
    height: auto
}
</style>
