<script setup>
import { ref, nextTick} from 'vue';
import { onMounted } from 'vue';
import FileDragDrop from '@/components/founder-space/interfaces/edit-cards/image-replace/pop-up-options/file-drag-drop.vue';
import LinkOption from '@/components/founder-space/interfaces/edit-cards/image-replace/pop-up-options/link-option.vue';
const activeTab = ref('file');

let props = defineProps({
    saveResults: Array,
    backDropClick: Boolean,
    imageInfo: Object,
});

let fileListner = null;
let linkListner = null;
let fileInput = null;
const fileSrc = ref(null);
const linkSrc = ref(null);
let file = "file";
let link = "link";

onMounted (() => {
    fileInput = document.getElementById("fileInput");
    fileListner = fileInput.addEventListener("change", function () {
        const files = this.files;
        const url = (URL.createObjectURL(files[0]));
        if(files[0].type.split("/")[0] !== "image"){
            error.value = "❗File must be an image";
            document.getElementById("error-message").classList.add("shake");
            setTimeout(() => {
                document.getElementById("error-message").classList.remove("shake");
            }, 500);
            return;
        }
        fileSrc.value = url;
        props.imageInfo.blob[0] = files[0];
        props.imageInfo.url[0] = url;
        file = "file-preview";
        activeTab.value = file;
        error.value = "";
    });
});

function save() {
    props.saveResults[0] = true;
    props.saveResults[1] = activeTab.value === "file-preview" ? fileSrc.value : linkSrc.value;
}


async function validateImage(url) {
  // Step 1: Check if it loads visually
  const canLoad = await new Promise((resolve) => {
    const img = new Image();
    img.onload = () => resolve(true);
    img.onerror = () => resolve(false);
    img.src = url;
  });

  if (!canLoad) return false;

  // Step 2 (optional): try fetch (may fail)
  try {
    const res = await fetch(url);
    const type = res.headers.get('content-type');
    return type?.startsWith('image/');
  } catch {
    // fallback: still valid visually
    return true;
  }
}

let error = ref("");

async function switchToLinkTab() {
    error.value = "";
    activeTab.value = link;
    await nextTick();
    document.getElementsByClassName("file-tab")[0].style.borderBottom = "2px solid rgba(255, 255, 255, 0)";
    document.getElementsByClassName("file-tab")[0].style.color = "rgba(255, 255, 255, 0.151)";
    document.getElementsByClassName("link-tab")[0].style.borderBottom = "2px solid rgba(255, 255, 255, 0.986)";
    document.getElementsByClassName("link-tab")[0].style.color = "rgba(255, 255, 255, 0.986)";
    fileInput.removeEventListener("change", fileListner);
    linkListner = document.getElementById("linkInput").addEventListener("input", async function (event) {
        const url = event.target.value;
        link = "link-preview";
        activeTab.value = link;
        props.urlInfo = url;
        props.imageInfo.blob[0] = null;
        props.imageInfo.url[0] = url;
        
        console.log(props.imageInfo)
        linkSrc.value = event.target.value;
        let validate = await validateImage(url);

        try{
            await fetch(props.imageInfo.url[0]).then(r => r.blob());
        }catch(e){
            console.log(`${import.meta.env.VITE_CORS_PROXY_URL}${encodeURIComponent(props.imageInfo.url[0])}`);
            let response = await fetch(`${import.meta.env.VITE_CORS_PROXY_URL}${encodeURIComponent(props.imageInfo.url[0])}`);
            if (!response.ok) {
                error.value = "This image could not be downloaded to our database. If the provider of the image changes, it will be removed. If you'd like to permanently keep this image, please download it and replace this image with the downloaded version from your local files.";
            }else{
                error.value = "";
            }
        }
    });
    console.log("switched to link tab");
}

async function switchToFileTab() {
    error.value = "";
    activeTab.value = file;
    await nextTick();
    document.getElementsByClassName("file-tab")[0].style.borderBottom = "2px solid rgba(255, 255, 255, 0.986)";
    document.getElementsByClassName("file-tab")[0].style.color = "rgba(255, 255, 255, 0.986)";
    document.getElementsByClassName("link-tab")[0].style.borderBottom = "2px solid rgba(255, 255, 255, 0)";
    document.getElementsByClassName("link-tab")[0].style.color = "rgba(255, 255, 255, 0.151)";
    fileInput = document.getElementById("fileInput");
    fileListner = fileInput.addEventListener("change", function () {
        const files = this.files;
        const url = (URL.createObjectURL(files[0]));
        if(files[0].type.split("/")[0] !== "image"){
            error.value = "❗File must be an image";
            document.getElementById("error-message").classList.add("shake");
            setTimeout(() => {
                document.getElementById("error-message").classList.remove("shake");
            }, 500);
            return;
        }
        props.imageInfo.blob[0] = files[0];
        props.imageInfo.url = url;
        fileSrc.value = url;
        file = "file-preview";
        activeTab.value = file;
        error.value = "";
    });
    console.log("switched to file tab");
}

function updateMainCardImage() {
    let mainCardImage = document.getElementById("main-card-image");
    mainCardImage.src = props.src;
}

function clearFileInput() {
    fileInput.value = "";
    fileSrc.value = null;
    file = "file";
    activeTab.value = file;
    nextTick().then(() => {
        fileInput = document.getElementById("fileInput");
        fileListner = fileInput.addEventListener("change", function () {
            const files = this.files;
            const url = (URL.createObjectURL(files[0]));
            if(files[0].type.split("/")[0] !== "image"){
                error.value = "❗File must be an image";
                document.getElementById("error-message").classList.add("shake");
                setTimeout(() => {
                    document.getElementById("error-message").classList.remove("shake");
                }, 500);
                return;
            }
            fileSrc.value = url;
            file = "file-preview";
            activeTab.value = file;
        });
    });
}

function closePopup() {
    props.backDropClick[0] = true;
}

</script>


<template>
    <div @click.self="closePopup" id="popup-backdrop" class="popup-backdrop">
        
        <div class="popup" :style="{left:'50%', width:'85%'}">
            <div class="header" style="overflow:auto;">
                <div class="tab-container" >
                    <div @click="switchToFileTab" class="file-tab">
                        File
                    </div>
                    <div @click="switchToLinkTab" class="link-tab">
                        Link
                    </div>
                </div>
            </div>
            <FileDragDrop v-if="activeTab === 'file' || activeTab === 'file-preview'" :src="fileSrc" />
            <LinkOption v-if="activeTab === 'link' || activeTab === 'link-preview'" :src="linkSrc" />
            <div id="error-message" style="color:red; position: absolute; bottom: 70px; font-size: 12px; font-family:Arial, Helvetica, sans-serif;">{{ error }}</div>
            <div class="footer">
            <div class="buttons"> 
                <div @click="save" v-if="activeTab === 'file-preview' || activeTab === 'link-preview'" class="save-button">
                    save
                </div>
                <div v-if="activeTab === 'file-preview'" @click="clearFileInput" class="cancel-button">
                    cancel
                </div>
                <div id="close-button" class="close-button">
                    close
                </div>
            </div>
        </div>   
    </div>    
</div> 
</template>

<style scoped>
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

.buttons{
    float: right;
    width:300px;
    margin-right: 80px;
}
.close-button {
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
    float: right;
    transition: box-shadow 0.3s ease;
}

.close-button:hover{
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.575);
}

.cancel-button {
    font-size: 16px;
    padding:30px;
    border-radius: 30px;
    margin-left: 20px;
    display: inline-block;
    padding: 10px;
    background-color:rgb(48, 48, 48);
    color: white;
    font-family: fantasy;
    letter-spacing: 1.5px;
    box-shadow: 0 0 10px rgba(68, 68, 68, 0.575);
    margin-top: -10px;
    float: right;
    transition: box-shadow 0.3s ease;
}

.cancel-button:hover{
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.575);
}

.save-button {
    font-size: 16px;
    padding:30px;
    border-radius: 30px;
    display: inline-block;
    padding: 10px;
    background-color:rgba(0, 195, 255, 0.712);
    color: white;
    font-family: fantasy;
    letter-spacing: 1.5px;
    margin-left: 20px;
    box-shadow: 0 0 10px rgba(0, 195, 255, 0.575);
    margin-top: -10px;
    float: right;
    transition: box-shadow 0.3s ease;
}

.save-button:hover{
    box-shadow: 0 0 15px rgba(2, 255, 255, 0.795);
}

.popup-backdrop.removing{
    opacity: 0;
}

.popup-backdrop {
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.911);
    position: fixed;
    top: 0;
    left: 0;
    z-index: 10;
    opacity: 1;
    animation: fadeIn 0.3s;
    transition: opacity 0.3s ease-out;
    
    filter:brightness(150%);
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
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
    width: calc(100% - 150px);
    height: calc(300px);
    cursor: pointer;
    border-radius: 10%;
    border:5px solid rgb(0, 0, 0);
    color: transparent;
    background-color: aqua;
    text-align: center;
    font-size: 18px;
    font-family: Arial, sans-serif;
    opacity: 0;
    margin: auto;
}

.container{
    opacity: 1;
    cursor: pointer;
    border-radius: 90px;
    padding-bottom: 50px;
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
    margin-top: calc( -1 * ( (100%) / 2) );
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
    cursor: pointer;
}
</style>
