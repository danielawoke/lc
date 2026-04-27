<script setup>
import { ref } from 'vue';
let props = defineProps({
    src: {
        type: String,
        default: null
    }
});


</script>

<template>
<div class="drag-and-drop-file">
        <div v-if="src==null" class="upload-text">
            <div class="outline" style="max-height:350px;">
                <div class="container" style="max-height:350px;">
                    <input id="fileInput" type="file" class="file-input" accept="image/*" />
                    <div class="upload-instructions" style="margin-top:-300px;">
                        <img class="photo-icon" src="@/assets/founder-space/edit/image-drag-drop.png" />
                        <div class="upload-text-main">
                            Drag & Drop or Click to Replace Image
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div v-else>
            <img :src="src" class="preview-image"  style="margin-top:60px;"/>
        </div>        
</div>
</template>

<style scoped>
 
.buttons{
    float: right;
    width:300px;
}
.cancel-button {
    font-size: 16px;
    padding:30px;
    border-radius: 30px;

    display: inline-block;
    padding: 10px;
    background-color:rgb(48, 48, 48);
    color: white;
    font-family: fantasy;
    letter-spacing: 1.5px;
    box-shadow: 0 0 10px rgba(68, 68, 68, 0.575);
    margin-top: -10px;
}
.save-button {
    font-size: 16px;
    padding:30px;
    border-radius: 30px;
    margin-right: 50px;
    display: inline-block;
    padding: 10px;
    background-color:rgba(0, 195, 255, 0.712);
    color: white;
    font-family: fantasy;
    letter-spacing: 1.5px;
    margin-left: 20px;
    box-shadow: 0 0 10px rgba(0, 195, 255, 0.575);
    margin-top: -10px;
}

.preview-image {
    max-width: 500px;
    max-height: min(calc( 50vh - 150px), 400px);
    width:auto;
    display: block;
    margin: auto;
    margin-top: calc(100% / 2 - 350px);
    border-radius: 20px;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.856);
    
    filter: brightness(70%);
}

.popup-backdrop {
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.911);
    position: fixed;
    top: 0;
    left: 0;
    z-index: 10;
}
.popup{
    background-image: linear-gradient(45deg, rgb(12, 12, 12), rgb(39, 39, 39));
    color: rgb(0, 0, 0);
    width:  calc( (100% - 180px) * .9);
    height: calc( (100% - 180px) * .7);
    max-width: 800px;
    max-height: 600px;
    border-radius: 90px;
    padding: 20px;
    position: absolute;
    top: 50%;
    left: calc((100vw - 180px) / 2 + 180px);
    transform: translate(-50%, -50%);
    box-shadow: rgba(0, 0, 0, 0.87) 0px 5px 15px 10px;
    overflow:hidden;
}

.header {
    text-align: left;
    background-image: linear-gradient(to top, rgb(22, 22, 22), black);
    box-shadow: rgb(20, 20, 20) 0px 4px 6px -1px, rgb(0, 0, 0) 0px 2px 4px -1px;
    width:100%;
    height:40px;
    padding: 20px;
    margin:-20px;
}
.footer{
    background-color: rgba(0, 0, 0, 0.212);
    box-shadow: rgb(10, 10, 10) 4px 4px 8px 4px;
    width:100%;
    height:40px;
    padding: 20px;
    margin: -20px;
    position: absolute;
    bottom: 0;
    margin-top: -20px;
}
.file-input {
    width: calc(100%);
    height: calc(300px);
    border-radius: 90px;
    border:5px solid rgb(0, 0, 0);
    color: transparent;
    background-color: rgb(0, 0, 0);
    text-align: center;
    font-size: 18px;
    font-family: Arial, sans-serif;
    opacity: 0;
    margin: auto;
    padding-bottom: 50px;
    position: relative;
    z-index: 100;
    cursor: pointer;
}

.container{
    opacity: 1;
    border-radius: 90px;
    background-image: linear-gradient(45deg, rgba(14, 13, 13, 0.753), rgba(24, 24, 24, 0.342));
}
.outline{
    margin: auto;
    border-radius: 95px;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.856);
    max-width: 500px;
    width: calc(100% - 150px);
    height: auto;
    transition: all 0.7s ease;
}

.upload-instructions {
    color: rgba(0, 0, 0, 0.295);
    width: calc(100% - 50px);
    font-size: 16px;
    font-family: fantasy;
    text-align: center;
    background-color: rgba(250, 128, 114, 0);
    padding: 10px;
    margin:auto;
    margin-top: calc( -1 * ( (100%) / 2) - 50px);
    padding-bottom: 50px;
}

.photo-icon {
    width:150px;
    opacity: .3;
    display: block;
    margin:auto;
}
.upload-text-main {
    font-size:16px;
    font-family: fantasy;
    font-weight: lighter;
    text-spacing-trim: space-all;
    margin:auto;
    margin-top: 20px;
    color: rgba(255, 255, 255, 0.151);
    font-size: 20px;
    letter-spacing: 7px;
}
.formats {
    font-size: 5px;
    color: rgb(255, 255, 255);
}
.file-tab {
    display: inline-block;
    padding:5px;
    margin-left: -30px;
    padding-left: 15px;
    padding-right: 5px;
    font-size: 27px;
    letter-spacing: 7px;
    margin-top: -5px;
    margin-left: 30px;
    margin-right:5px;
    cursor: pointer;
    border-bottom: 2px solid rgba(255, 255, 255, 0.986);
    font-family: fantasy;
    color:rgb(255, 255, 255);
}
.link-tab {
    display: inline-block;
    padding:5px;
    padding-left: 20px;
    padding-right: 20px;
    margin-top:16px;
    font-family:fantasy;
    color: rgba(255, 255, 255, 0);
    padding-left: 15px;
    font-size: 27px;
    letter-spacing: 7px;
    padding-right: 15px;
    font-family: fantasy;
    color:rgba(53, 53, 53, 0.432);
    border-bottom: 2px solid rgba(255, 255, 255, 0);
}

</style>