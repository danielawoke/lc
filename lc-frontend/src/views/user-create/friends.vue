<script setup>

import { useRoute, useRouter } from 'vue-router'
import { nextTick, onMounted, watch } from 'vue';
import { ref } from 'vue';
import dayjs from 'dayjs';
import Header from '@/components/header.vue';
import { AccountLocal } from '@/lib/appwrite';
import axios from 'axios';
const apiUrl = import.meta.env.VITE_APP_API_URL
const route = useRoute();
const router = useRouter();

let friendList = ref([]);

onMounted(async () => {
    containerHeightAdjust();
    window.addEventListener('resize', containerHeightAdjust);
    try{
        // let user = await AccountLocal.get();
        // let usertag = route.params.usertag;
        let usertag = route.params.usertag
        console.log(usertag)
        let friendsResponse = await axios.get(`${apiUrl}users/search/friends/${usertag}`);
        friendList.value = friendsResponse.data.friends;
        // console.log("FRIENDS LIST:", friendsList);
    }catch(e){
        router.push('/login');
    }
    
});

function containerHeightAdjust(){
    // document.querySelector('.container').style.height = "calc(100vh - " + 60 + "px)";
    // let height1 = document.querySelector('.container').offsetHeight;
    // document.querySelector('.container').style.height = "auto";
    // let height2 = document.querySelector('.container').offsetHeight;
    // if(height1 > height2){
    //     document.querySelector('.container').style.height = "calc(100vh - " + 60 + "px)";
    // }
    // else{
    //     document.querySelector('.container').style.height = "auto";
    // }
}

</script>

<template>
    <Header style="z-index:10" />
    <div class="container">
        <div class="people-listing">
            <div v-if="friendList.length == 0" style="font-size:18px; padding:20px;">
                No friends listed
            </div>
            <div v-for="(person, i) in friendList" :key="i">
                <div class="person-block" @click="router.push(`/profile/${person.friend_usertag}`)">
                    <img class="person-image" :style="{ backgroundImage: `url(${person.friend_image})` }" />
                    <div class="text-block">
                        <div class="people-listing-name">{{person.friend_display_name}}</div>
                        <div class="people-listing-position">@{{person.friend_usertag}}</div>
                        <!-- <div class="people-listing-date">Joined: <i>{{dayjs(person.dateJoined).format('MMMM D, YYYY')}}</i></div> -->
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
    border-radius: 20px;
    padding-top: 20px;
    padding-bottom: 20px;
    padding-left:40px;
    padding-right:40px;
    width:calc(100% - 140px);
    background-color: rgba(255, 255, 255, 0.164);
    margin:auto;
    margin-top: 10px;
    margin-bottom: 10px;
}
.person-block:hover{
    cursor:pointer;
    background-color: rgba(255, 255, 255, 0.541);
    transition: all 0.01s ease-in;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
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
    background-size: cover;
    border: solid rgba(0, 0, 0, 0.466) 2px;
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
    width: calc(100vw - 0px);
    margin: auto;
    height: calc(100vh - 60px);
    overflow-y: auto;
    z-index:-1;
    background: radial-gradient(circle, rgb(255, 83, 241), rgb(150, 150, 255))
    
}
</style>