<script setup>
import { useRoute, useRouter } from 'vue-router'
import {ref} from 'vue'
import Header from '@/components/header.vue';
import Tool from '@/components/founder-space/tool-bar.vue'
import Chat from '@/components/founder-space/interfaces/chat.vue';

const router = useRouter()
const route = useRoute()

function mobileModeListener(){
    mobileMode.value = window.innerWidth <= 768;
    console.log("Mobile mode:", mobileMode.value);
}

let mobileMode = ref(true)
mobileMode.value = window.innerWidth <= 768;
window.addEventListener('resize', mobileModeListener);

let toolBarSelected = ref(true);

function goToEdit(){
    let projId = route.params.projectId
    router.push('/project-edit/'+projId+'/edit')
}

function goToVotes(){
    let projId = route.params.projectId
    router.push('/project-edit/'+projId+'/votes/personal')
}

function goToChat(){
    let projId = route.params.projectId
    router.push('/project-edit/'+projId+'/chat')
}

function goToPeople(){
    let projId = route.params.projectId
    router.push('/project-edit/'+projId+'/people')
}

function goToSettings(){
    let projId = route.params.projectId
    router.push('/project-edit/'+projId+'/settings')
}

</script>
<template>
    <Header />
    <div v-if="mobileMode">
        <div class="burgerContainer-top" v-if="mobileMode">
            <img class="settings-top" style="z-index:1000" src="https://static.thenounproject.com/png/1777842-200.png" @click="toolBarSelected=!toolBarSelected"/>
        </div>
        <div class="tool-side-bar" v-if="toolBarSelected">
            <div style="height:50px"></div>
            <div class="side-bar-text" @click="goToEdit">Edit</div>
            <div class="side-bar-text" @click="goToVotes">Votes</div>
            <div class="side-bar-text" @click="goToChat">Chat</div>
            <div class="side-bar-text" @click="goToPeople">People</div>
            <div class="side-bar-text" @click="goToSettings">Settings</div>
        </div>
    </div>
    <Chat />
    <Tool v-if="!mobileMode"/>
    <footer v-if="!mobileMode" />
</template>
<style scoped>  
.side-bar-text{
    color:white;
    text-align: center;
    font-size: 18px;
    margin-top:30px;
    font-family: Arial, Helvetica, sans-serif;
}
.side-bar-text:hover{
    color:rgb(190, 190, 190);
}
.tool-side-bar{
    position:absolute;
    width:calc(100vw - 10px);
    background: linear-gradient(to top, black, rgb(19, 19, 19));
    height: calc(100vh - 60px);
    top:60px;
    left:0;
    animation: slideIn ease-out 0.3s;
}
@keyframes slideIn {
    from {
        transform: translateX(-100%);
    }
    to {
        transform: translateX(0);
    }
}

.burgerContainer-top{
    position: fixed;
    top:15px;
    left:60px;
    filter: invert(0);
    z-index: 100;
}
.settings-top{
    width: 35px;
    height: 35px;
    background-size: 80% 80%;
    background-position: center;
    background-repeat: no-repeat;
    color: rgb(0, 0, 0);
    font-family: Arial, Helvetica, sans-serif;
    font-size: 12px;
    position: absolute;
    top:0px;
    filter:invert(1);
    left:10px;
    border-radius: 5px;
    overflow:hidden;
}

.copy-right{
    font-family: fantasy;
    font-size: 7px;
    position: absolute;
    top:37px;
    left: 20px;
    color: rgba(161, 161, 161, 0.664);
    padding: 10px;
}
footer{
    font-family: fantasy;
    font-size: 13px;
    position: absolute;
    bottom: 0;
    left: 0;
    width: calc(15px);
    height: 20px;
    color: rgb(232, 232, 232);
    padding: 20px;
    padding-bottom:20px;
    padding-top:20px;
    background-color: rgb(0, 0, 0);
    font-size: 10px;
}


</style>
    