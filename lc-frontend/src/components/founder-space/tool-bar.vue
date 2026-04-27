<script setup>
import { useRoute, useRouter } from 'vue-router'
import { onMounted, ref } from 'vue';
const router = useRouter();
const route = useRoute();
onMounted(() => {
  
});

function goToEdit() {
  router.push(`/project-edit/${route.params.projectId}/edit`);
}

function goToDecisions() {
  router.push(`/project-edit/${route.params.projectId}/votes/personal`);
}

function goToChat() {
  router.push(`/project-edit/${route.params.projectId}/chat`);
  
}

function goToSettings() {
  router.push(`/project-edit/${route.params.projectId}/settings`);
  
}

function goToPeople() {
  router.push(`/project-edit/${route.params.projectId}/people`);
}

</script>

<template>


<div class="toolBar">
    <div id="edit-button" :class="router.currentRoute.value.path.split('/')[3].includes('edit') ? 'toolBar-item-selected' : 'toolBar-item'" @click="goToEdit" src="@/assets/founder-space/edit/edit-icon-1.png">
        <img class="toolBar-icon" src="@/assets/founder-space/edit/edit-icon-1.png"></img>
        <div style="margin-top:15px; font-size:12px; text-align: center; margin-left: -8px; width:40px">edit</div>
        <!-- edit -->
    </div>
    <div  id="decisions-button" :class="router.currentRoute.value.path.split('/').includes('votes') ? 'toolBar-item-selected' : 'toolBar-item'" @click="goToDecisions">
        <img class="toolBar-icon" src="@/assets/founder-space/decisions/handraise.png"></img>
        <div style="margin-top:15px; font-size:12px; text-align: center; margin-left: -8px; width:40px">votes</div>
    </div>
    <!-- <div class="toolBar-item">
        <img class="toolBar-icon" src="@/assets/founder-space/edit/edit-icon-1.png"></img>
         calendar
    </div> -->
    <div  id="chat-button"  :class="router.currentRoute.value.path.split('/')[3].includes('chat') ? 'toolBar-item-selected' : 'toolBar-item'" @click="goToChat">
        <img class="toolBar-icon" src="@/assets/founder-space/decisions/discussion.png"></img>
        <div style="margin-top:15px; font-size:12px; text-align: center; margin-left: -8px; width:40px">chat</div>
    </div>
    <div :class="router.currentRoute.value.path.split('/')[3].includes('people') ? 'toolBar-item-selected' : 'toolBar-item'" @click="goToPeople">
        <img class="toolBar-icon" src="@/assets/founder-space/people.png"></img>
        <div style="margin-top:15px; font-size:12px; text-align: center; margin-left: -8px; width:40px">people</div>
    </div>
    <!-- <div class="toolBar-item" :class="router.currentRoute.value.path.includes('settings') ? 'toolBar-item-selected' : 'toolBar-item'">
        <img class="toolBar-icon" src="@/assets/founder-space/chart.png"></img>
    </div> -->
    <div @click="goToSettings" :class="router.currentRoute.value.path.split('/')[3].includes('settings') ? 'toolBar-item-selected' : 'toolBar-item'">
        <img class="toolBar-icon" src="@/assets/founder-space/chat/setting.png"></img>
        <div style="margin-top:15px; font-size:12px; text-align: center; margin-left: -8px; width:40px">settings</div>
    </div>
    
    <!-- <div @click="goToSettings" :class="router.currentRoute.value.path.split('/')[3].includes('help') ? 'toolBar-item-selected' : 'toolBar-item'">
        <img class="toolBar-icon" src="https://cdn-icons-png.flaticon.com/512/171/171322.png"></img>
        <div style="margin-top:15px; font-size:12px; text-align: center; margin-left: -8px; width:40px">help</div>
    </div> -->
</div>

</template>

<style scoped>
.toolBar-icon{
    width: 20px;
    height: 20px;
    margin-top: -5px;
    margin-left:2.5px;
    filter:invert(1);
    position: absolute;
}
.toolBar-item{
    font-family: fantasy;
    color: rgb(206, 206, 206);
    font-size: 15px;
    width:25px;    
    height:25px;
    /*background-color: rgb(44, 44, 44);*/
    margin:auto;
    padding:10px;
    background-image: linear-gradient(to top, rgb(0, 0, 0), rgb(0, 0, 0));
    border: white solid 1px;
    border-radius: 10px;
    margin-top: 5px;
}
.toolBar-item-selected{
    font-family: fantasy;
    color: rgb(206, 206, 206);
    font-size: 15px;
    width:25px;    
    height:25px;
    padding:10px;
    margin:auto;
    border: rgb(0, 0, 0) solid 1px;
    background-image: linear-gradient(to top, rgb(255, 123, 62), rgb(255, 8, 0));
    filter:invert(1);
    border-radius: 10px;
    margin-top: 5px;
}
.toolBar{

    overflow-y: auto;
    overflow-x: hidden;
    position: absolute;
    left: 0;
    z-index: -1;
    width:55px;
    padding-top:20px;
    height: calc(100vh - 210px);
    padding-bottom: 100px;
    background:rgb(0, 0, 0);
}
.logo {
  display: inline-block;
  width: 80px;
  height: 80px;
  position: absolute;
  margin-top: -80px;
  margin-left: 40px;
    border-radius: 50%;
  background-color: rgb(0, 0, 0);}
.image{
    text-align: center;
    margin-top: 20px;
}
.container{
    height:100px;
    position: absolute;
    margin-top: 120px;
    left: 0;
    background-color: rgb(255, 255, 255);
    width: calc(100vw - 180px);
    z-index: -2;
    margin-left: 180px;
    text-align: center;
}
.toolBar-item-selected:hover{
    cursor: pointer;
    filter:invert(0) brightness(1.5);
    border: rgb(255, 255, 255) solid 1px;
    background-image: linear-gradient(to top, rgb(0, 96, 121), rgb(0, 183, 255));
}
.toolBar-item:hover{
    filter:invert(1);
    cursor: pointer;
}

footer{
    font-family: fantasy;
    font-size: 13px;
    position: absolute;
    bottom: 0;
    left: 0;
    width: calc(100vw - 40px);
    height: 20px;
    color: rgb(232, 232, 232);
    padding: 20px;
    padding-bottom:20px;
    padding-top:20px;
    background-color: rgb(0, 0, 0);
    font-size: 10px;
}

</style>