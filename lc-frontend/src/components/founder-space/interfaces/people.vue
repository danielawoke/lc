<script setup>

import { useRoute, useRouter } from 'vue-router'
import { nextTick, onMounted, watch } from 'vue';
import { ref } from 'vue';
import {AccountLocal} from '@/lib/appwrite.js';
import dayjs from 'dayjs';
import axios from 'axios';
const router = useRouter()
const route = useRoute()
const apiUrl = import.meta.env.VITE_APP_API_URL;

onMounted(async () => {
    await loadPeople();
});

let people = ref([]);

async function loadPeople(){
    try{
        let user = await AccountLocal.get();
        await axios.post(`${import.meta.env.VITE_APP_API_URL}projects/admin-load/${route.params.projectId}/${user.$id}/`, { private_key: import.meta.env.VITE_API_PRIVATE_KEY })
            .then(response => {
                people.value = response.data.members_info;
                console.log("Loaded people:", people.value);
            });
    }catch(error){
        console.error("Error loading people:", error);
    }
}

function mobileModeListener(){
    mobileMode.value = window.innerWidth <= 768;
    console.log("Mobile mode:", mobileMode.value);
}

let mobileMode = ref(true)
mobileMode.value = window.innerWidth <= 768;
window.addEventListener('resize', mobileModeListener);



</script>

<template>
    <div class="container" :style="{width: mobileMode ? '100vw' : 'calc(100vw - 50px)', marginLeft: mobileMode? '0': '50px'}">
        <div class="people-listing">
            <div v-for="(person, i) in people" :key="i" @click="router.push('/profile/'+person.usertag)">
                <div class="person-block">
                    <img class="person-image" :src="person.image" />
                    <div class="text-block">
                        <div class="people-listing-name">{{person.name}}</div>
                        <div class="people-listing-position">{{person.position}}</div>
                        <div class="people-listing-date">Joined: <i>{{dayjs(person.dateJoined).format('MMMM D, YYYY')}}</i></div>
                    </div>
                </div>
            </div>
        </div>  
    </div>
</template>

<style scoped>
.people-listing-name{
    font-size: 22px;
    font-weight: bold;
    color: rgb(0, 0, 0);
}
.people-listing-position{
    font-size: 14px;
    color: rgb(0, 0, 0);
    font-weight:normal;
}
.people-listing-date{
    font-size: 14px;
    color: rgb(0, 0, 0);
    font-weight:normal;
}
.person-block{
    padding-top: 20px;
    padding-bottom: 20px;
    padding-left:40px;
    padding-right:40px;
    background-color: rgba(255, 255, 255, 0.527);
    margin: auto;
    margin-top: 15px;
    margin-bottom:15px;
    border-radius: 40px;
    width:calc(100% - 150px);
    box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
}
.person-block:hover{
    box-shadow: 0px 6px 20px rgba(0, 0, 0, 0.2);
    cursor: pointer;
    transform: translateY(-2px);
    transition: all 0.3s ease;
}
.person-image{
    vertical-align: top;
    margin-right:10px; 
    width:10%; 
    max-width:100px;
    min-width: 80px;
    aspect-ratio: 1 / 1;
    border-radius:50%; 
    display:inline-block;
    background-color: black;
}
.text-block{
    position: relative;
    display: inline-block;
    font-size: 14px;
    color: rgb(0, 0, 0);
    font-family: sans-serif;
    width: calc(80%);
    font-weight: bold;
    background:rgba(0, 0, 0, 0);
    height:80px;
    margin-top:10px;
}
.people-listing{
    position: relative;
    overflow:auto;
    background-color: rgba(216, 216, 216, 0);
    height: auto;
    font-size: 12px;
    text-align: left;
    z-index: 20;
    overflow:hidden;
    overflow-y:auto;
    font-family: sans-serif;
    z-index: 20;
    width: calc(100% - 0px);

}
.container{
    display: block;
    position: absolute;
    top: 60px;
    left: 0px;
    margin: auto;
    height: calc(100vh - 60px);
    background:rgba(45, 118, 255, 0.103);
    overflow-y:auto;
}
</style>