<script setup>
import { useRoute, useRouter } from 'vue-router'
import { onMounted, ref } from 'vue'
import Header from '@/components/header.vue'
import locationDatabase from '@/components/supporting-components/location-explore.vue';
import { nextTick } from 'vue';
import dayjs from 'dayjs';
import axios from 'axios';
const apiUrl = import.meta.env.VITE_APP_API_URL;
const router = useRouter()
const route = useRoute()

let loadedStatus = ref("loading");
let searchResults = ref([]);
let loads = 0
let addRate = 50;
let userCount = ref(0)
let searchParameters = ref({
    distance: 2100,
    location: "USA",
    lng: -74.0060,
    lat: 40.7128,
    physicalLocation:true,
    remote:true,
    people:true,
    jobs: false,
    projects: true,
    searchType: "Recent",
})

onMounted(async () => {
    
    fontAdjust();
    adjustListWidth();
    adjustHeaderContainerSize();
    adjustContainerHeight();
    window.addEventListener('resize', adjustListWidth);
    window.addEventListener('resize', adjustContainerHeight);
    window.addEventListener('resize', adjustHeaderContainerSize);
    await processQuery(searchParameters);
    adjustListWidth();
    adjustHeaderContainerSize();
    adjustContainerHeight();
    userCount.value = (await axios.get(apiUrl + "users/count")).data.user_count;
});

function relativeTime(timePosted){
    const now = dayjs();
    const postedTime = dayjs(timePosted);
    const diffInSeconds = now.diff(postedTime, 'second');
    if(diffInSeconds < 60){
        return diffInSeconds + " seconds ago";
    }else if(diffInSeconds < 3600){
        const diffInMinutes = Math.floor(diffInSeconds / 60);
        return diffInMinutes + " minutes ago";
    }else if(diffInSeconds < 86400){
        const diffInHours = Math.floor(diffInSeconds / 3600);
        return diffInHours + " hours ago";
    }else if(diffInSeconds < 2592000){
        const diffInDays = Math.floor(diffInSeconds / 86400);
        return diffInDays + " days ago";
    }else if(diffInSeconds < 31104000){
        const diffInMonths = Math.floor(diffInSeconds / 2592000);
        return diffInMonths + " months ago";
    }else{
        const diffInYears = Math.floor(diffInSeconds / 31104000);
        return diffInYears + " years ago";
    }
}

let initialLoad = false;
let totalResults = 0;

async function processQuery(searchParameters){
    let query = route.query.q;
    if(query == undefined || query.trim() == ""){
        query = "undefined";
    }
    searchResults.value = [];
    loadedStatus.value = "loading";
    if(!initialLoad){
        query = query.trim();
        searchParameters.value = {
            distance: route.query.distance ? Number(route.query.distance) : searchParameters.value.distance,
            location: route.query.location ? route.query.location : searchParameters.value.location,
            lat: route.query.lat ? Number(route.query.lat) : searchParameters.value.lat,
            lng: route.query.lng ? Number(route.query.lng) : searchParameters.value.lng,
            physicalLocation: route.query.physicalLocation === "false" ? false : searchParameters.value.physicalLocation,
            remote: route.query.remote === "false" ? false : searchParameters.value.remote,
            people: route.query.people === "false" ? false : searchParameters.value.people,
            jobs: route.query.jobs === "false" ? false : searchParameters.value.jobs,
            projects: route.query.projects === "false" ? false : searchParameters.value.projects,
            searchType: route.query.searchType ? route.query.searchType : searchParameters.value.searchType,
            loads: loads,
            addRate: addRate
        }
        initialLoad = true;
    }

    if(query == undefined || query.trim() == ""){
        query = "undefined";
    }
    
    await axios({
        method: 'get',
        url: apiUrl + "search/"+query+"/"+JSON.stringify(searchParameters.value),
    }).then(async (response) => {
        searchResults.value.push(...response.data.data);
        totalResults = response.data.total_results;
        if(searchResults.value.length == 0){
            loadedStatus.value = "none";
            return;
        }else if((searchParameters.value.loads+1) * searchParameters.value.addRate < totalResults){
            loadedStatus.value = 'more';
        }else{
            loadedStatus.value = "loaded";
        }
        searchParameters.value.loads += 1;
    }).catch((error) => {
        console.log(error);
        loadedStatus.value = "none";
    });
}

async function loadMore(){
    let query = route.query.q;
    loadedStatus.value = "loading";
    await axios({
        method: 'get',
        url: apiUrl + "search/"+query+"/"+JSON.stringify(searchParameters.value),
    }).then(async (response) => {
        console.log(response.data.data);
        searchResults.value.push(...response.data.data);
        totalResults = response.data.total_results;
        console.log(totalResults);
        console.log(searchParameters.value.loads * searchParameters.value.addRate);
        if(searchResults.value.length == 0){
            loadedStatus.value = "none";
            return;
        }else if((searchParameters.value.loads + 1) * searchParameters.value.addRate  < totalResults){
            loadedStatus.value = 'more';
        }else{
            loadedStatus.value = "loaded";
        }
    }).catch((error) => {
        console.log(error);
        loadedStatus.value = "loaded";
    });
    
    searchParameters.value.loads += 1;
}


function adjustHeaderContainerSize(){
    let searchOpsBlock = document.getElementById("search-options");
    let searchBlock = document.getElementById("search-block");
    let height = searchOpsBlock.offsetHeight;
    searchBlock.style.height = height + 90 + "px";
    let ratio = .1;
    let dropDowns = document.getElementsByClassName("drop-down-entry");
    let selects = document.getElementsByClassName("select-option");
    for (let i = 0; i<1; i++){
        // el.style.marginBottom = -1*height*ratio;
        selects[i].style.marginBottom = height*ratio+"px";
    }
    for (let i = 0; i<1; i++){
        // el.style.marginBottom = -1*height*ratio;
        dropDowns[i].style.marginBottom = height*ratio+"px";
    }
}

function adjustListWidth(){
    let projectList = document.getElementsByClassName("project-list")[0];
    let pixelWidth = 370 * Math.floor(window.innerWidth / 370);
    projectList.style.width = (pixelWidth) + "px";
}

function fontAdjust(){
    let profileNames = document.getElementsByClassName("profile-name");
    for (let profileName of profileNames) {
        let height = profileName.offsetHeight;
        let fontSize = 20;
        while(height > 40){
            profileName.style.fontSize = fontSize + "px";
            height = profileName.offsetHeight;
            fontSize-=2;
        }
    }
}


let distance = ref(20);
function goToMain() {
    router.push('/');
}

function adjustContainerHeight(){
    console.log(searchParameters.value);
    let block = document.querySelector(".result-screen");
    block.style.height = "fit-content";
    let height1 = block.offsetHeight;
    block.style.height = "calc(100vh - 0px)";
    let height2 = block.offsetHeight;
    if(height1 > height2){
        block.style.height = height1 + "px";
    }
}

function PopulaceToggleDropDown(){
    let button = document.getElementById("populace-categorical-tab");
    let dropDown = document.getElementById("populace-categorical-tab-drop-down");
    let spacing = document.getElementById("populace-categorical-tab-spacing");
    if (dropDown.style.display == "none") {
        spacing.style.marginLeft = (button.offsetWidth+21) + "px";
        console.log(spacing.style.marginLeft);
        dropDown.style.display = "block";
        button.style.position = "absolute";
        document.getElementById("location-tab-drop-down").style.display = "none";
        document.getElementById("location-tab").style.position = "relative";
        document.getElementById("location-tab-spacing").style.marginLeft = (0) + "px";
        document.getElementById("distance-tab-drop-down").style.display = "none";
        document.getElementById("distance-tab").style.position = "relative";

    } else {
        spacing.style.marginLeft = 0+ "px";
        dropDown.style.display = "none";
        button.style.position = "relative";
    }
}

async function populaceSelected(e){
    // document.getElementById("populace-categorical-tab-text").innerHTML = e.target.innerHTML;
    searchParameters.value.searchType = e.target.innerHTML.replace(" ", "_");
    document.getElementById("location-tab-drop-down").style.display = "none";
    document.getElementById("location-tab").style.position = "relative";
    document.getElementById("location-tab-spacing").style.marginLeft = (0) + "px";
    document.getElementById("distance-tab-drop-down").style.display = "none";
    document.getElementById("distance-tab").style.position = "relative";
    searchResults.value = [];
    searchParameters.value.loads = 0;
    await processQuery(searchParameters);
}

let addressChange = false;
let tooglePhysicalSetting = false;
async function LocationToggleDropDown(){
    let button = document.getElementById("location-tab");
    let dropDown = document.getElementById("location-tab-drop-down");
    let spacing = document.getElementById("location-tab-spacing");
    if (dropDown.style.display == "none") {
        spacing.style.marginLeft = (button.offsetWidth+21) + "px";
        dropDown.style.display = "block";
        button.style.position = "absolute";
        document.getElementById("populace-categorical-tab-spacing").style.marginLeft = (0) + "px";
        document.getElementById("populace-categorical-tab-drop-down").style.display = "none";
        document.getElementById("populace-categorical-tab").style.position = "relative";
        document.getElementById("distance-tab-drop-down").style.display = "none";
        document.getElementById("distance-tab").style.position = "relative";
    } else {
        if(!document.getElementById("location-input-val").value == "" && searchParameters.value.location != document.getElementById("location-input-val").value){
            addressChange = true;
            searchParameters.value.location = document.getElementById("location-input-val").value;
            let coords = await convertAddressToCoordinates(searchParameters.value.location);
            searchParameters.value.lat = coords.lat;
            searchParameters.value.lng = coords.lng;
            document.getElementById("location-width-adjust").innerHTML = document.getElementById("location-input-val").value;
        }
        
        if(addressChange && !tooglePhysicalSetting){
            await processQuery(searchParameters);
        }

        addressChange = false;

        dropDown.style.display = "none";
        button.style.position = "relative";
        spacing.style.marginLeft = (0) + "px";
        // searchResults.value = [];
        // searchParameters.value.loads = 0;
    }
}


async function convertAddressToCoordinates(address){
    try{
        const response = await axios.get(`https://maps.googleapis.com/maps/api/geocode/json`, {
            params: {
                address: address,
                key: import.meta.env.VITE_GOOGLE_MAPS_API_KEY
            }
        });
        if(response.data.results.length > 0){
            const location = response.data.results[0].geometry.location;
            return location; // { lat: ..., lng: ... }
        }else{
            console.error("No results found for the given address.");
            return null;
        }
    }catch(err){
        console.error("Error converting address to coordinates:", err);
        return null;
    }
}


function exponetialConversion(number){
    return Math.round(Math.pow(number, 1.7));
}

function inverseExponetialConversion(number){
    return (Math.pow(number, 1/1.7));
}

function updateDistance(){
    let number = Number(document.getElementById("distance-range-input").value);
    number = exponetialConversion(number);
    searchParameters.value.distance = number;
}

async function DistanceToggleDropDown(){
    let button = document.getElementById("distance-tab");
    let dropDown = document.getElementById("distance-tab-drop-down");
    if (dropDown.style.display == "none") {
        document.getElementById("distance-tab-spacing").style.marginLeft = (button.offsetWidth+21) + "px";
        dropDown.style.display = "block";
        button.style.position = "absolute";
        document.getElementById("location-tab").style.position = "relative";
        document.getElementById("location-tab-drop-down").style.display = "none";
        document.getElementById("populace-categorical-tab-drop-down").style.display = "none";
        document.getElementById("populace-categorical-tab").style.position = "relative";
        document.getElementById("populace-categorical-tab-spacing").style.marginLeft = (0) + "px";
        document.getElementById("location-tab-spacing").style.marginLeft = (0) + "px";
    } else {
        dropDown.style.display = "none";
        button.style.position = "relative";
        document.getElementById("distance-tab-spacing").style.marginLeft = (0) + "px"; 
        searchResults.value = [];
        searchParameters.value.loads = 0;
        await processQuery(searchParameters);
    }
}

let remote = ref([false]);
let locationConsideration = ref([true]);

async function remoteToggle(){
    searchParameters.value.remote = !searchParameters.value.remote;
    searchResults.value = [];
    searchParameters.value.loads = 0;
    await processQuery(searchParameters);
}

function shortened(content){
    if(content.length > 50){
        return content.substring(0, 50) + "...";
    }
    return content;
}

function locationConsiderationToggle(){
    tooglePhysicalSetting = tooglePhysicalSetting ? false : true;
    searchParameters.value.physicalLocation = !searchParameters.value.physicalLocation;
}

async function toggleJobs(){
    searchParameters.value.jobs = !searchParameters.value.jobs;
    let query = "f"
    loadedStatus.value = "loading";
    searchResults.value = [];
    searchParameters.value.loads = 0;
    await processQuery(searchParameters);

}

async function toggleProjects(){
    searchParameters.value.projects = !searchParameters.value.projects;
    searchResults.value = [];
    searchParameters.value.loads = 0;
    await processQuery(searchParameters);
}   
async function togglePeople(){
    searchParameters.value.people = !searchParameters.value.people;
    searchResults.value = [];
    searchParameters.value.loads = 0;
    await processQuery(searchParameters);
}
async function goToJob(job){
    await incrementPublicCount(job);
    router.push('/project/'+job.project_id+'?job_id='+job.job_id);
}

async function goToProfile(profile){
    await incrementPublicCount(profile);
    router.push('/profile/'+profile.usertag);
}

async function goToProject(project){
    await incrementPublicCount(project);
    router.push('/project/'+project.project_id);
}

async function incrementPublicCount(entry){
    try{
        await axios.post(`${apiUrl}users/increment_view/${entry.id}`, {
            id: entry.id
        });
    }catch(err){
        console.error("Error incrementing public count:", err);
    }
}


</script>



<!-- start with sales from now on -->
<!-- I created an app for finding college studnets to create companies with -->

<template>

    <div class="user-count">{{ userCount }} total users</div>
    <div class="search-interface" id="search-block">
        <Header :searchParameters="searchParameters" />
        <div class="search-options" id="search-options">
            <span @click="toggleProjects" v-if="searchParameters.projects" class="select-option">Projects</span>
            <span @click="toggleProjects" v-else class="select-option" style="background:black; border: 2px solid rgb(140, 140, 140);">Projects</span>
            <span @click="togglePeople" v-if="searchParameters.people" class="select-option">People</span>
            <span @click="togglePeople" v-else class="select-option" style="background:black; border: 2px solid rgb(140, 140, 140);">People</span>
            <span @click="toggleJobs" v-if="searchParameters.jobs" class="select-option">Jobs</span>
            <span @click="toggleJobs" v-else class="select-option" style="background:black; border: 2px solid rgb(140, 140, 140);">Jobs</span>
            <span  @click="PopulaceToggleDropDown" id="populace-categorical-tab" class="drop-down-option" style="z-index:4;">
                <span id="populace-categorical-tab-text">
                    {{searchParameters.searchType.replace("_", " ")}}
                </span>
                <span>
                    <img class="dropdown-icon" src="https://cdn-icons-png.freepik.com/512/5800/5800629.png"/>
                </span>
                <div id="populace-categorical-tab-drop-down" style="display:none;">
                    <div class="drop-down-menu">
                        <div style="height:5px"></div>
                        <div @click="populaceSelected" class="drop-down-entry">Recent</div>
                        <div @click="populaceSelected" class="drop-down-entry">Most Popular</div>
                    </div>
                </div>
            </span>
            <span id="populace-categorical-tab-spacing"></span>
             <span @click="remoteToggle" id="remote-tab" class="drop-down-option" style="z-index:3; border: 2px solid rgb(0, 153, 255);" v-if="searchParameters.remote">
                <span id="remote-text">
                    Remote <img src="https://cdn-icons-png.flaticon.com/512/3759/3759392.png" style="width:15px; height:15px; margin-bottom:-2.5px;">
                </span>
            </span>
            <span @click="remoteToggle" id="remote-tab" class="drop-down-option" style="z-index:3; background:transparent; border: 2px solid rgb(255, 255, 255);" v-else>
                <span id="remote-text">
                    Remote <img src="https://cdn-icons-png.flaticon.com/512/3759/3759392.png" style="width:15px; height:15px; margin-bottom:-2.5px;">
                </span>
            </span>
            <span  @click.self="LocationToggleDropDown" id="location-tab" class="drop-down-option" style="z-index:2;">
                <span @click.self="LocationToggleDropDown" v-if="searchParameters.physicalLocation" id="location-text">
                    {{ searchParameters.location }}
                </span>
                <span @click.self="LocationToggleDropDown" v-else id="location-text" style="color:rgba(255, 255, 255, 0.575);">
                    {{ searchParameters.location }}
                </span>

                <span>
                    <img @click.self="LocationToggleDropDown" class="dropdown-icon" src="https://cdn-icons-png.freepik.com/512/5800/5800629.png"/>
                </span>
                <div id="location-tab-drop-down" style="display:none;">
                    <div class="drop-down-menu">
                        <div style="height:10px;"></div>
                            <locationDatabase />
                        <div id="location-width-adjust" style="height:10px; white-space: nowrap;opacity:0;">
                            
                        </div>
                        <input @click="locationConsiderationToggle" type="checkbox" :checked="!searchParameters.physicalLocation" id="remote-only-checkbox" style="margin-right:5px;"/>
                        <label for="remote-only-checkbox" style="font-family: fantasy; font-size: 12px; color:white;">Dont consider physical locations</label>
                        <div style="height:5px;"> </div>
                    </div>
                </div>
            </span>

            <span id="location-tab-spacing"></span>
            <span  @click.self="DistanceToggleDropDown" id="distance-tab" class="drop-down-option" style="z-index:0;">
                <span id="distance-text" :style="searchParameters.physicalLocation ? 'position:relative;' : 'position:relative; color:rgba(255, 255, 255, 0.575);'" >
                    <span v-if="searchParameters.distance>2000" style="font-size:25px; display:inline-block; margin:-10px; margin-top:-10px; margin-right:5px; margin-left:-5px; top:4px; position:relative;">∞ </span>{{ searchParameters.distance>2000? 'mi' : searchParameters.distance+" mi" }}
                </span>
                <span>
                    <img @click.self="DistanceToggleDropDown" class="dropdown-icon" src="https://cdn-icons-png.freepik.com/512/5800/5800629.png"/>
                </span>
                <div id="distance-tab-drop-down" style="display:none;">
                    <div class="drop-down-menu" style="width:140px; z-index: 9999;">
                        <div style="height:10px;"></div>
                        <input type="range" :value="inverseExponetialConversion(searchParameters.distance)" @input="updateDistance" class="slider" id="distance-range-input">
                        <div style="height:10px;"></div>
                    </div>
                </div>
            </span>
            <span id="distance-tab-spacing"></span>
        </div>
    </div>
    
   
    <!-- <div class="background"> -->
        <div class="container">
             
            <div class="result-screen">
                <div style="width:fit-content;margin:auto;">
                    <div class="category-title"></div>
                    <div class="project-list">
                        <span v-for="i in [1]">
                        <span v-for="result in searchResults">
                            <!-- <div v-if="result.type == 'project'" style="color:white"> Projects</div>
                            <div v-else-if="result.type == 'job'" style="color:white">Jobs</div> -->
                            <span v-if="result.type == 'project'" class="project-card" @click="goToProject(result)">
                                <div class="image-backdrop-project-card" :style="'background-image: url(' + result.image_url + ');'">
                                    <div class="project-top-container">
                                        <div style="width:100%; position:absolute; right:0; top:-100px;padding-top:100px; font-style:italic; ">
                                            <div style="font-size:12px;margin-top:5px" class="project-title">
                                                {{ result.title }}
                                            </div>
                                            <div class="project-description">
                                                {{ result.description }}
                                            </div>
                                        </div>
                                    </div>
                                    <div class="project-bottom-container">
                                        <div class="project-meta-section">
                                            <div class="meta-text">
                                                {{ result.public_count }} views
                                            </div>
                                            <div class="clicks-icon"></div>
                                        </div>
                                        <div class="project-meta-section">
                                            <div class="meta-text">
                                                {{ result.member_count }} people
                                            </div>
                                            <div class="people-count-icon"></div>
                                        </div>
                                        <div class="project-meta-section">
                                            <div v-if="result.physical" class="meta-text">
                                                {{ result.location }}
                                            </div>
                                            <div v-else class="meta-text">
                                                Remote
                                            </div>
                                            <div  v-if="result.physical" class="location-icon"></div>
                                            <span v-if="result.remote && result.physical" style="color:white; width:39px; margin-bottom: -12.5px;"> + <img src="https://cdn-icons-png.flaticon.com/512/3759/3759392.png" style="width:15px; height:15px; margin-bottom:-0.5px;"></span>
                                            <span v-else-if="result.remote" style="color:white; width:19px; margin-bottom: -12.5px;"><img src="https://cdn-icons-png.flaticon.com/512/3759/3759392.png" style="width:15px; height:15px; margin-bottom:-0.5px;"></span>
                                        </div>
                                    </div>
                                </div>
                            </span>
                            <span v-if="result.type == 'person'" class="person-card" @click="goToProfile(result)">
                                <div class="profile-top-container">
                                    <div class="profile-title-section">
                                        <div class="profile-picture" :style="{backgroundImage: 'url('+result.image_url+')', backgroundSize: 'cover', backgroundPosition:'center' }"></div>
                                        <!-- <img class="profile-picture" :src="result.image_url" /> -->
                                    </div>
                                    <div class="profile-header">
                                        <div id="name-block" class="profile-name" style="">{{ result.title }}  </div>
                                    </div>
                                    <div class="profile-insearch-of-block"><b>Im looking for:</b> {{ result.looking_for }}</div>
                                    <div class="profile-skill-block">
                                        <div class="profile-skill" v-for="skill in result.skills.slice(0,4)">
                                            {{ skill }}
                                        </div>
                                    </div>
                                </div>
                                <div class="profile-bottom-container">
                                    <div class="project-meta-section" style="background: rgba(0, 0, 0, 0.5); padding:0px; margin-left:30px; width:fit-content; position:absolute; bottom:10px; right:30px; border-radius:5px;">
                                        <div v-if="result.physical" class="meta-text">
                                            {{ result.location }}
                                        </div>
                                        <div v-else class="meta-text">
                                            Remote
                                        </div>
                                        <div  v-if="result.physical" class="location-icon"></div>
                                        <span v-if="result.remote && result.physical" style="color:white; width:39px; margin-bottom: -12.5px;"> + <img src="https://cdn-icons-png.flaticon.com/512/3759/3759392.png" style="width:15px; height:15px; margin-bottom:-0.5px;"></span>
                                        <span v-else-if="result.remote" style="color:white; width:19px; margin-bottom: -12.5px;"><img src="https://cdn-icons-png.flaticon.com/512/3759/3759392.png" style="width:15px; height:15px; margin-bottom:-0.5px;"></span>
                                    </div>
                                </div>
                            </span>
                            <span v-if="result.type == 'job'" class="explore-job-card" @click="goToJob(result)">
                                
                                <img class="pin" src="https://pngimg.com/d/pin_PNG64.png" />
                                <span class="help-wanted-text">HELP WANTED</span>
                                <div class="job-card-image-backdrop-project-card">
                                    <div class="project-top-container">
                                        <div style="width:100%; position:absolute; right:0; top:-110px;padding-top:100px; font-style:italic; ">
                                            <div style="font-size:12px;margin-top:5px" class="project-title">
                                                {{ result.title }}
                                            </div>
                                            <div class="project-description">
                                                {{ result.description }}
                                            </div>
                                        </div>
                                        <div style="" class="project-description"></div>
                                    </div>
                                    <div class="project-bottom-container" style="margin-top:-40px;">
                                        <div class="project-meta-section">
                                            <div class="meta-text">
                                                Posted {{ relativeTime(result.time_posted) }}
                                            </div>
                                            <div class="people-count-icon"></div>
                                        </div>
                                        <div class="project-meta-section" style="height:0px; position:relative; top:5px; margin:-15px; margin-top:10px;">
                                            
                                            <span v-if="result.physical" class="meta-text" style="margin-top:20px;">
                                                <div style="height: 50px; padding-top:10px; padding-left:10px;">
                                                    <div style="top:5px;right:5px; float: right; width:fit-content; vertical-align: top; margin-left:5px ">
                                                        <span v-if="result.physical" class="location-icon" style="margin:0;"></span>
                                                        <span v-if="result.remote && result.physical" style="color:white; width:39px;"> + <img src="https://cdn-icons-png.flaticon.com/512/3759/3759392.png" style="width:15px; height:15px; display:inline-block;"></span>
                                                        <span v-else-if="result.remote" style="color:white; width:19px;display:inline-block;"><img src="https://cdn-icons-png.flaticon.com/512/3759/3759392.png" style="width:15px; height:15px;display:inline-block; "></span>
                                                    </div>
                                                    <span style="margin-top:-10px;"> {{result.location}} </span>
                                                </div>
                                            </span>
                                            <span v-else class="meta-text" style="margin-top:-0px; margin-right:25px;">
                                                <div style="top:5px;right:5px; float: right; margin-left:5px; margin-right:-5px; width:fit-content;vertical-align: top;">
                                                    <span v-if="result.physical" class="location-icon" style="margin:0;"></span>
                                                    <span v-if="result.remote && result.physical" style="color:white; width:39px;"> + <img src="https://cdn-icons-png.flaticon.com/512/3759/3759392.png" style="width:15px; height:15px; display:inline-block;"></span>
                                                    <span v-else-if="result.remote" style="color:white; width:19px;display:inline-block;"><img src="https://cdn-icons-png.flaticon.com/512/3759/3759392.png" style="width:15px; height:15px;display:inline-block; "></span>
                                                </div>
                                                <span style="margin-top:-20px; margin-right:0px">Remote</span>
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            </span>
                        </span>
                        </span>
                    <span @click="loadMore"  v-if="loadedStatus=='more'" class="load-more-card">
                        <div class="load-more-text">+<br/>LOAD MORE</div>
                    </span>
                    <span style="color: white; font-family: arial; font-size: 16px;" v-if="loadedStatus=='none'">
                        No results
                    </span>
                    <span style="color: white; font-family: arial; font-size: 16px;" v-if="loadedStatus=='loading'">
                        Loading...
                    </span>
                    </div>
                </div>
            </div>
        </div> 
    <!-- </div> -->
               
</template>
<style scoped>
.user-count{
    position: fixed;
    bottom: 20px;
    left: 20px;
    color: white;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 16px;
    z-index: 100;
    height:20px;
}

.help-wanted-text{
    position: absolute;
    top: 6px;
    left: 15px;
    font-size: 22px;
}
.pin{
    width: 60px;
    height: 60px;
    position: relative;
    top: -25px;
    left: 130px;
    z-index: 9000;
}
.card-header{
    font-weight: bold;
    background: linear-gradient(45deg, rgba(0, 0, 0, 0.322), rgba(0, 0, 0, 0.418));
    width:calc(100% + 0px);
    position: absolute;
    top: -15px;
    left: -10px;
    border-radius: 8px 8px 0 0;
    padding: 10px;
    padding-bottom:5px;
    padding-top: -10px;
    padding-left:10px;
    color:rgb(0, 0, 0);
    z-index: 10;
}

.project-card:hover .card-header{
    cursor: pointer;
}

html{
    background-color: rgb(0, 0, 0);
}
.Base {
  display: block;
  position: absolute;
  top: 0;
  left: 0;
  width: calc(100vw);
  margin: auto;
  height: 60px;
  background-color: rgb(0, 0, 0);
  /*background-image: linear-gradient(45deg, rgb(143, 219, 249), rgb(0, 183, 255)); */

}
.notification{
    width: 32px;
    height: 32px;
    margin-top: -15px;
    cursor: pointer;
    margin-right: 25px;
    filter:invert(1);
}
.profile-top-image{
    border-radius:50%;
    border: solid 2px rgba(255, 255, 255, 0.521);
    width: 35px;
    height: 35px;
    margin-top: -15px;
    cursor: pointer;
    margin-right: 25px;
}
.messages{
  width: 35px;
  height: 35px;
  margin-top: -15px;
  cursor: pointer;
  margin-right: 25px;
  filter:invert(1);
}
.top-header-container {
  display: flex;
  margin: auto;
  margin-top: 25px;
}
.logo {
  display: inline-block;
  width: 40px;
  height: 40px;
  margin-top: -15px;
  margin-left:10px;
  /* whatever the dominant color of what is on the inside, should match the color of this */
  border-radius: 50%;
  border: 2px solid rgb(109, 69, 27);
  background-color: rgb(247, 193, 118);
  background-image: linear-gradient(45deg, rgb(255, 109, 31), rgb(255, 221, 165));
}
.title-top-header{
  position:absolute;
  display: inline-block;
  font-family: fantasy;
  font-size: 20px;
  color: rgb(232, 232, 232);
  margin-left: 15px;
  margin-top: -5px;
}
.search-enter-button{
    width: 20px;
    height: 20px;
    filter:invert(1);
    background-image: url("@/assets/search.png");
    background-size: cover;
    background-position: center;
    display: inline-block;
    margin-left: 10px;
    cursor: pointer;
    position:absolute;
}
.search-input{
    width: calc(100% - 40px);
    border: none;
    color: white;
    font-family: fantasy;
    font-size: 14px;
    color:white;
    background: transparent;
    outline: none;
}
.search-box{
    display: inline-block;
    padding: 5px;
    width: calc(100% - 410px);
    font-size: 16px;
    border-radius: 5px;
    color:white;
    background:rgba(0, 0, 0, 0.104);
    border: solid white 1px;
    position:relative;
    top:-10px;
}
.group-chat-image{
    width: 30px;
    height: 30px;
    background-color: rgba(0, 0, 0, 0);
    background-image: url("https://static.vecteezy.com/system/resources/thumbnails/020/767/286/small/cute-girl-holding-smartphone-with-speech-bubble-heart-cartoon-character-hand-draw-art-illustration-vector.jpg");
    background-position: center;
    background-size: cover;
    border-radius: 50%;
    display:inline-block;
    margin-bottom:-10px;
    border: 2px solid rgba(0, 0, 0, 0.712);
}
.messages-dropdown{
    position: absolute;
    top: 60px;
    right: 0px;
    width: 300px;
    height: 400px;
    background-color: rgb(255, 255, 255);
    box-shadow: inset 0px 0px 20px rgba(0, 0, 0, 0.5);
    z-index: 10;
    border-radius: 0 0 0 10px;
    border: 2px solid rgb(0, 0, 0);
}
      
.notification-card-read{
    width: 100%;
    height: 100px;
    background-color: rgb(201, 201, 201);
    box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.1);
    padding: 10px;
    border-bottom: black solid 1px;
    box-sizing: border-box;
    cursor: pointer;
    opacity: 0.6;
}
.note-date{
    font-family: Arial, Helvetica, sans-serif;
    font-size: 10px;
    position: relative;
    top:15px;
}
.note-content{
    font-family: Arial, Helvetica, sans-serif;
    font-size: 12px;
    position: relative;
    top:10px;
    margin-left:0px;
}
.note-title{
    font-family: Arial, Helvetica, sans-serif;
    font-size: 16px;
    position: relative;
    top:-2px;
}

.remote-drop-down-menu{
    position: relative;
    float:left;
    width: fit-content;
    height: fit-content;
    background: rgb(255, 84, 84);
    padding-left:12px;
    padding-right:12px;
    margin-left:-12px;
    margin-right:-12px;
    padding-bottom:6px;
    margin-top:5px;
    margin-bottom: -6px;
    color: rgb(224, 224, 224);
    border-radius: 5px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
    z-index: 9999;
}
.remote-button:hover{
    background:rgb(0, 0, 0);
    filter: brightness(200%);
    cursor: pointer;
}
.remote-button{
    display: inline-block;
    padding: 2px 5px;
    width:25%;
    font-family: fantasy;
    text-align: center;
    background: rgb(255, 30, 30);
    
    border: 2px solid rgba(255, 255, 255, 0);
    box-shadow: rgb(0, 0, 0) 0px 0px 10px;
    color:rgb(255, 255, 255);
    font-size: 12px;
    border-radius: 5px;
}
.slider{
    width: 100%;

}
.drop-down-entry:hover{
    filter: invert(1) brightness(150%) hue-rotate(90deg);
    cursor: pointer;
}
.drop-down-entry{
    display: block;
    padding: 5px 5px;
    font-family: fantasy;
    background: rgb(71, 89, 255);
    border: 2px solid rgba(255, 255, 255, 0);
    box-shadow: rgb(0, 0, 0) 0px 0px 10px;
    color:rgb(255, 255, 255);
    font-size: 14px;
    margin-left: -5px;
    border-radius: 5px;
    cursor: pointer;
    margin-top:3px;
}
.drop-down-menu{
    position: relative;
    width: fit-content;
    height: fit-content;
    background: rgba(0, 0, 0, 0);
    border-radius: 5px;
    padding-left:12px;
    padding-right:12px;
    margin-left:-12px;
    margin-right:-12px;
    padding-bottom:6px;
    margin-bottom: -6px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
    border-top: none;
    display: block;
    z-index: 0;
}
.dropdown-icon{
    width:15px;
    height:15px;
    margin-left:5px;
    margin-bottom:-3.5px;
    background-image: url("https://cdn-icons-png.freepik.com/512/5800/5800629.png");
    transform: rotate(-90deg);
    float:right;
    transition: all 0.3s ease;
}
.logo-icon-background{
    width:80px;
    height:80px;
    background: rgb(255, 255, 255);
    border-radius: 50px;
    position: absolute;
    margin-top: 10px;
    margin-left: 25px;
    /* whatever the dominant color of what is on the inside, should match the color of this */
    border: 4px solid rgb(227, 155, 78);
    background-image: linear-gradient(45deg, rgb(255, 109, 31), rgb(255, 221, 165)); 
    filter: contrast(100%);
    overflow: hidden;
}
.right-portion{
  display: inline-block;
  margin-left: auto;
}

.right-portion-element {
  width: 50px;
  height: 50px;
  border-radius: 50px;
  margin-top: -15px;
  cursor: pointer;
  margin-right: 25px;
}
.search-options{
    position: absolute;
    top:65px;
    width:100%;
    height:auto;

}
.drop-down-option:hover .dropdown-icon{
    filter: invert(1) brightness(150%);
    transform: rotate(0deg);
}
.drop-down-option{
    display: inline-block;
    padding: 5px 10px;
    font-family: fantasy;
    background: rgb(0, 0, 0);
    border: 1px solid rgba(255, 255, 255, 0.945);
    box-shadow: rgb(0, 0, 0) 0px 0px 10px;
    color:rgb(255, 255, 255);
    font-size: 14px;
    border-radius: 5px;
    margin-left: 20px;
    margin-top:3px;
    position: relative;
    cursor: pointer;
    z-index: 9999;
}
.select-option{
    display: inline-block;
    padding: 5px 10px;
    font-family: fantasy;
    background: rgb(0, 0, 0);
    border: 2px solid rgb(0, 153, 255);
    box-shadow: rgb(0, 0, 0) 0px 0px 10px;
    color:rgb(255, 255, 255);
    font-size: 14px;
    border-radius: 5px;
    margin-left: 20px;
    cursor: pointer;
    margin-top:3px;
}
.load-more-text{
    color: rgba(255, 255, 255, 0.575);
    text-shadow: 2px 2px 0px rgba(0, 0, 0, 0.575);
    font-family: fantasy;
    font-size: 25px;
    font-weight: lighter;
    text-align: center;
    margin-top:65px;
}
.load-more-card:hover{
    background: rgba(221, 221, 221, 0.2);
    color: rgba(255, 255, 255, 0.9);
    text-shadow: 2px 2px 10px rgba(0, 0, 0, 0.8);
    cursor: pointer;
    box-shadow: inset 0px 0px 10px 10px rgba(0, 0, 0, 0.178);
}
.load-more-card{
    display:inline-block;
    border: dashed rgba(255, 255, 255, 0.24) 2px;
    padding: 10px;
    margin: 10px;
    border-radius: 15px;
    width:300px;
    height:200px;
    overflow: hidden;
}
.search-interface{
    position:absolute;
    width:100%;
    height:fit-content;
    top:0px;
    left:0;
    z-index: 10;
    background: rgb(0, 0, 0);

    box-shadow: 0 0 20px rgba(0, 0, 0, 0.308);
}
.result-screen{
    width:100%;
    box-shadow: inset 0px -15px 15px 10px rgba(0, 0, 0, 0.405);
    padding-top:100px;
    padding-bottom:100px;
    background: linear-gradient(to bottom, rgb(14, 14, 14), rgb(22, 22, 22));
}
.galaxy{
    height:300px;
    width:300px;
    background-image: url("https://img1.picmix.com/output/stamp/normal/5/4/7/4/2384745_37f06.gif");
    background-size: contain;
    background-position: center;
    margin:auto;
    margin-top:-50px;
}
.bottom-margin{
    height: 10px;
    width:100%;
    background: #001f42;
    box-shadow: 0px -5px 5px 5px rgba(3, 3, 3, 0.616);
}
.top-margin{
    width:100%;
    height: 30px;
    background: linear-gradient(to top, rgba(0, 0, 0, 0.514), rgb(0, 0, 0));
    box-shadow: 0px -5px 5px 5px rgba(0, 0, 0, 0.11);
}
.search-block{
    height: 500px;
    background: radial-gradient( ellipse at center, rgba(94, 158, 255, 0.582) 5%, rgba(0, 0, 0, 0.767) 95%);
    font-variant: small-caps;
    color: white;
}
.search-block:hover .top-margin{
       
    background: linear-gradient(to top, rgba(0, 0, 0, 0.938), rgba(0, 0, 0, 0.856));
    box-shadow: 0px -5px 5px 5px rgba(0, 0, 0, 0.329);
}
.search-block:hover .wide-block{
    background: rgba(0, 0, 0, 0.405);
    font-variant: small-caps;
    color: white;
    cursor: pointer;
    box-shadow: inset 0px 0px 20px 10px rgba(0, 0, 0, 0.664);
    text-shadow: 2px 2px 10px rgb(255, 255, 255);
    font-size: 31px;
    border-top: solid rgba(0, 0, 0, 0.562) 8px;
    border-bottom: solid rgba(0, 0, 0, 0.8)  8px;
    filter: brightness(140%);
        
}
.wide-block{
    width: calc(100%);
    background: rgba(0, 21, 77, 0.267);
    box-shadow: inset 0px -15px 15px 0px rgba(0, 0, 0, 0.405);
    padding-top:90px;
    padding-bottom:100px;
    color:white;
    font-family: fantasy;
    font-size: 30px;
    text-align: center;
    margin:auto;
    margin-bottom: 30px;
    border-top: solid rgba(14, 14, 14, 0.479) 18px;
     transition: all 0.3s ease;
}
.profile-insearch-of-block{
    font-size: 12px;
    font-family: fantasy;
    color: white;
    font-weight: normal;
    background:rgba(0, 0, 0, 0.589);
    margin-top: 10px;
    position: relative; 
    width:fit-content;
    padding: 5px 10px;
    border-radius: 10px;
    z-index: 1000;
}
.profile-skill-block{
    height:60px;
    background-color: rgba(0, 0, 0, 0);
}
.profile-skill{
    display: inline-block;
    background-color: rgba(0, 0, 0, 0.562);
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);
    color: white;
    font-family: fantasy;
    font-size: 10px;
    padding: 5px 10px;
    border-radius: 20px;
    margin-right: 5px;
    margin-top: 10px;
    position: relative;
    z-index: 1000;
}
.profile-name{
    background: rgba(0, 0, 0, 0.562);
    color: white;
    font-family: fantasy;
    font-size: 16px;
    font-weight: bold;
    text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.7);
    top:0;
    position:absolute;
    padding:20px;
     border-radius: 0 0 10px 10px;
     margin-left:20px;
}
.profile-self-statement{
    font-size: 10px;
    font-family: fantasy;
    color: white;
    font-weight: normal;
    background:rgba(0, 0, 0, 0);
}
.profile-header{
    display:inline-block;
    color: white;
    font-family: fantasy;
    font-size: 18px;
    background-color: #92e00000;
    font-weight: bold;
    margin-bottom: 10px;
    text-shadow: 2px 2px 5px rgba(0, 0, 0, 0);
}
.profile-picture{
    display:inline-block;
    position: relative;
    width: 200px;
    height: 200px;
    margin-right:5px;
    border-radius: 50%;
    position: absolute;
    left: 60px;
    z-index: -0;
    box-shadow: 0px 0px 20px rgba(0, 0, 0, 0);
}
.profile-title-section{
    width: 100%;
    height: 80px;
    background-color: rgba(0, 0, 0, 0);;
}
.profile-bottom-container{
    width:calc(100%);
    height:15%;
    padding-left: 40px;
    padding-right: 40px;
    margin-left: -40px;
    background:rgba(0, 0, 0, 0);
    box-shadow: inset 0px 0px 15px 5px rgba(0, 0, 0, 0);
    position: relative;
}
.profile-top-container{
    position: relative;
    width: calc(100%);
    height: 90%;
    background: rgba(0, 0, 0, 0);
}
.people-count-icon{
    width: 15px;
    height: 15px;
    background-image: url('https://static.thenounproject.com/png/133028-200.png');
    background-size: cover;
    display: inline-block;
    margin-bottom: -10px;
    margin-right: 5px;
    filter: saturate(0%) invert(1); 
}
.clicks-icon{
    width: 15px;
    height: 15px;
    background-image: url('@/assets/main-page/views.png');
    background-size: cover;
    display: inline-block;
    margin-bottom: -10px;
    margin-right: 5px;
    filter: saturate(0%) invert(1); 
}
.project-meta-section{
    display: flex;
    align-items: center;
    height:18px;
}
.meta-text{
    width: calc(100% - 20px);
    text-align: right;
    display: inline-block;
    color: white;
    font-family: fantasy;
    font-size: 11px;
    margin-top: 10px;
    margin-right:5px;
}
.location-icon{
    width: 15px;
    height: 15px;
    background-image: url('@/assets/main-page/location.png');
    background-size: cover;
    display: inline-block;
    margin-bottom: -10px;
    margin-right: 5px;
    filter: saturate(0%) invert(1); 
}
.project-bottom-container{
    width:calc(100%);
    height:50%;
    padding-left: 40px;
    padding-right: 40px;
    margin-left: -40px;
    margin-top: -10px;
    background:rgba(0, 0, 0, 0.487);
    box-shadow: inset 0px 0px 15px 5px rgba(0, 0, 0, 0.463);
    position: relative;
    z-index: 1000;
}   
.project-top-container{
    position: relative;
    width: calc(100%);
    height: 77%;
    background: rgba(0, 0, 0, 0);
    z-index: 100;
}
.project-description{
    color: rgb(255, 255, 255);
    font-family: Arial, Helvetica, sans-serif;
    font-size: 11px;
    margin-top: 5px;
}
.project-title{
    color: white;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 13px;
    font-weight: bold;
    text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.7);
    z-index: 1000;
}
.image-backdrop-project-card{
    
    width:calc(100% - 20px);
    height:calc(100% - 20px);
    background-size: cover;
    background-repeat: no-repeat;
    background-color: rgba(0, 0, 0, 0.6);
    box-shadow: inset 0px 0px 15px 5px #00000099;
    padding:10px;
    background-position: center;
    background-blend-mode: overlay;
}
.tunnel-outline{
    
}
.sub-tunnel-cut{
}
.tunnel:hover .sub-tunnel-cut{
}
.tunnel:hover .sub-tunnel{
    
    transform: translate(15%,30%) scale(1.1);
    background-image: linear-gradient(to bottom, #008caf 10%, #001ee0 90%);
    border: 2px solid rgba(255, 255, 255, 0.422);
    filter:brightness(50%);
    box-shadow: inset 0px 0px 25px 15px rgba(0, 25, 70, 0.729);
    transition: all 1s ease;
}


.logo-icon-background:hover {
    box-shadow: 0px 0px 10px 2px #ffffffea;
    filter:contrast(120%) saturate(0);
    transition: all 0.3s ease;
    cursor: pointer;
}

.title{
  display: inline-block;
  font-family:fantasy;
  font-size: 20px;
  transform: scaleY(200%) translateY(0px);
  font-variant: small-caps;
  color: rgb(255, 255, 255);
  font-weight: bold;
  margin-left: 130px;
  margin-right: 10px;
  width:140px;
  text-align: center;
  margin-top: 0px;

}

.sub-tunnel{
    position: absolute;
    margin: 0 auto;
    width: 77%;
    height: 75%;
    border-radius: 50%;
    z-index: 0;
    bottom:0px;
    box-shadow: inset 0px 0px 15px 3px rgba(0, 184, 216, 0.193);
    border: 2px solid rgba(0, 0, 0, 0);
    background:rgb(0, 0, 0);
    transform: translate(15%,40%);
    overflow: hidden;
}
.preface-elements-container{
    width: 100%;
    margin:auto;
}
.tunnel:hover .darkest-center{
    transition: all 1s ease;
    transform: translate(28%,0px);
    z-index: 20;
    background-image: linear-gradient(to bottom, #008caf 10%, #001ee0 90%);
    border: 2px solid rgba(255, 255, 255, 0.422);
    filter:brightness(20%);
    box-shadow: inset 0px 0px 25px 15px rgba(0, 25, 70, 0.729);
    transition: all 1s ease;
}
.darkest-center{
    position: absolute;
    margin: 0 auto;
    width: 62%;
    height: 50%;
    
    transform: translate(28%,0px);
    border-radius: 50%;
    bottom:2px;
    background: rgb(0, 0, 0);
    box-shadow: inset 0px 0px 15px 5px rgba(0, 0, 0, 0.729);
    z-index: -10;
}
.tunnel:hover{
    background-image: linear-gradient(to bottom, #008caf 10%, #001ee0 90%);
    cursor: pointer;
    box-shadow: inset 0px 0px 25px 15px rgba(0, 25, 70, 0.729);
    transition: all 1s ease;
    border:rgba(255, 255, 255, 1) solid 15px;
    transform: translate(-60%,0) scale(1.05);
    filter:contrast(100%) saturate(150%) brightness(150%) hue-rotate(-25deg);
}
.tunnel{
    position: absolute;
    display: block;
    margin: 0 auto;
    width: 25%;
    max-width:305px;
    aspect-ratio: 2.5 / 1;
    border-radius: 50%;
    z-index: 0;
    bottom:100px;
    background-image: linear-gradient(to bottom, #3acfd5 10%, #4f5fc1 90%);
    border: 15px solid rgb(0, 0, 0);
    box-shadow: inset 0px 0px 35px 5px rgba(0, 0, 0, 0.845);
    left:50%;
    transform: translate(-60%,0);
    overflow: hidden;
    
}
.create-proj-tunnel-caption{
    position: absolute;
    bottom: 50px;
    left:calc(50% - 220px);
    color: rgb(255, 255, 255);
    font-family: fantasy;
    font-size: 19px;
    font-weight: bold;
    z-index: 1;
}
.banner-image-outline{
    pointer-events: none; 
    display: block;
    width: 100%;
    max-width: 1200px;
    position: absolute;
    left:50%;
    top:50%;
    transform: translate(-50%, calc(-50% + 2px));
    z-index: 9;
    background: rgba(255, 255, 255, 0);
    filter:invert(1);
}

.banner-image{
    pointer-events: none; 
    display: block;
    margin: 0 auto;
    width: 100%;
    max-width: 1200px;
    position: relative;
    transform: translate(0,0);
    z-index: 10;
    background: rgba(255, 255, 255, 0);
}
.prefacing-block-text{
    
    width:calc(100% - 0px);
    height:fit-content;
    margin: auto;
    padding-top:100px;
    padding-bottom:100px;
    filter:brightness(150%);
    

}
.footer{
    width:calc(100% - 40px);
    position: absolute;
    bottom:0;
    text-align: left;
    padding: 20px;
    background-color: rgb(0, 0, 0);
    color:white;
    font-family: fantasy;
    font-size: 16px;
    padding-top:30px;
    margin-top:40px;
}
.preface-search-text{
    text-align: left;
    font-weight: lighter;
    text-decoration: underline;
    color:rgb(255, 255, 255);
    font-size: 20px;
    font-family: fantasy;
    margin-bottom: 10px;

}
.search-button{
    background: rgb(255, 254, 250);
    border: #00000000 solid 1px;
    border-radius: 10%;
    color:rgb(255, 255, 255);
    cursor: pointer;
    font-size: 20px;
    width:40px;
    height:40px;
    margin-left: 20px;
    margin-bottom: 5px;
    vertical-align: middle;
    z-index: 1;
    display:inline-block;
}
.search{
    position: absolute;
    top:20px;
    left:130px;
    padding:6px;
    padding-left:10px;
    width: calc(100% - 400px);
    font-size: 16px;
    border-radius: 5px;
    color:rgb(0, 0, 0);
    background:rgb(255, 228, 107);
    border: 2px solid rgba(255, 255, 255, 0);
    box-shadow: inset 0px 0px 10px rgba(0, 0, 0, 0.2);
    
}
.search-container{
    padding-top:80px;
    height:300px;
    margin:auto;
    background: rgba(0, 0, 0, 0);
}
.extra-proj-button-border:hover{
    position: relative;
    display: block;
    margin: 0 auto;
    background: rgb(255, 211, 99);
    padding: 40px;
    width: calc(100% - 100px);
    font-family: fantasy;
    font-weight: bold;
    text-shadow: 5px 5px 10px rgb(0, 0, 0);
    font-size: 33px;
    text-align: center;
    border: 10px solid rgb(255, 189, 102);
    color:rgb(255, 255, 255);
    box-shadow: inset 0 0 30px 30px rgb(255, 169, 40);
}
.create-proj-button:hover{
    background: rgb(255, 220, 133);
    text-shadow: 10px 10px 20px rgb(0, 0, 0);
    border: 10px solid rgb(255, 191, 71);
    color:rgb(255, 255, 255);
    cursor: pointer;
    font-size: 30px;
}
.extra-proj-button-border{
    position: relative;
    display: block;
    margin: 0 auto;
    background: goldenrod;
    padding: 40px;
    width: calc(100% - 100px);
    height:50px;
    font-family: fantasy;
    font-weight: bold;
    text-shadow: 5px 5px 10px rgb(0, 0, 0);
    font-size: 30px;
    text-align: center;
    border: 10px solid rgb(255, 145, 0);
    color:white;
    box-shadow: inset 0 0 20px 20px rgb(192, 109, 0);
    transition: all 0.3s ease;
}
.create-proj-button{
  background: rgb(255, 201, 63);
    text-shadow: 10px 10px 20px rgb(0, 0, 0);
    border: 10px solid rgb(255, 175, 25);
    color:rgb(255, 255, 255);
    cursor: pointer;
}
.prefacing-block-text{
    margin-bottom: 50px;
}
.category-title{
    text-align: center;
    font-weight: bold;
    margin: auto;
    font-size: 20px;
    margin-bottom: 30px;
    font-family: fantasy;
    color:white;
    text-shadow: 2px 2px 5px rgba(255, 255, 255, 0.627);
}
.project-list{
    margin:auto;
    width:calc(100% -0px);
    background-color: #ae000000;
}

.container{
    position: absolute;
    top:0;
    padding-top:50px;
    right:0;
    width: calc(100vw);
    height: calc(100vh - 50px);
    z-index: -1;
    overflow: auto;
}

.job-card-image-backdrop-project-card{
    width:calc(100% - 20px);
    height:calc(100% - 40px);
    background-size: cover;
    background-repeat: no-repeat;
    background-color: rgba(0, 0, 0, 0.384);
    box-shadow: inset 0px 0px 15px 5px #00000099;
    padding:10px;
    overflow: hidden;
    margin-top: -40px;
    transform: rotate(-2deg)
}
.explore-job-card{
    display:inline-block;
    padding: 10px;
    width:210px;
    margin-left:50px;
    margin-right:50px;
    height:200px;
    filter:contrast(100%);
    background-image: linear-gradient(45deg, rgb(255, 255, 255),rgb(255, 255, 255));
    box-shadow: inset 0px 0px 25px 15px rgba(75, 75, 75, 0.663);
    transform: rotate(2deg);
    position: relative;
    top:-5px;
    margin-top:10px;
    margin-bottom:10px;
}
.explore-job-card:hover{
    background-image: linear-gradient(45deg, rgb(255, 255, 255),rgb(255, 255, 255));
    box-shadow: inset 0px 0px 25px 15px rgba(75, 75, 75, 0.663);
    cursor: pointer;
    transition: all 0.3s ease;
    transform: scale(1.05);
}
.explore-job-card:hover .project-top-container{
    position: relative;
    width: calc(100%);
    height: 77%;
    background: rgba(0, 0, 0, 0.405);
    padding:0px;
    box-shadow: 0px -15px 15px 100px rgba(0, 0, 0, 0.405);
    transition: all 0.3s ease;
}
.person-card{
    display:inline-block;
    padding: 10px;
    margin: 10px;
    margin-left:30px;
    margin-right: 30px;
    border-radius: 15px;
    width:290px;
    height:200px;
    overflow: hidden;
}
.person-card:hover{
    cursor: pointer;
    transition: all 0.3s ease;
    transform: scale(1.05);
}

.project-card{
    display:inline-block;
    background-image: linear-gradient(45deg, rgb(255, 255, 255),rgb(255, 255, 255));
    box-shadow: inset 0px 0px 15px 5px rgba(0, 0, 0, 0.463);
    padding: 10px;
    margin: 10px;
    border-radius: 15px;
    width:330px;
    height:200px;
    overflow: hidden;
}
.project-card:hover{
    background-image: linear-gradient(45deg, rgb(255, 255, 255),rgb(255, 255, 255));
    box-shadow: inset 0px 0px 25px 15px rgba(12, 12, 12, 0.76);
    cursor: pointer;
    transition: all 0.3s ease;
    cursor: pointer;
    transition: all 0.3s ease;
    transform: scale(1.01);
}

.project-card:hover .project-top-container{
    background-color: rgba(0, 0, 0, 0.405);
    box-shadow: 0px 0px 15px 100px rgba(0, 0, 0, 0.405);
    cursor: pointer;
    transition: all 0.3s ease;
}


.left {
    display: inline-block;
    width: 50%;
    max-width: 1200px;

}
.right {
    display: inline-block;
    width: 50%;
    max-width: 1200px;
    background-color: rgba(240, 248, 255, 0);
}






.switch-toggle {
   float: left;
   background: black;
   border-radius: 2px;
   width: 90px;
}
.switch-toggle input {
  position: absolute;
  opacity: 0;
  width: 30%;
}
.switch-toggle input + label {
  padding: 10px;
  float:left;
  color: black;
  cursor: pointer;
}
.switch-toggle input:checked + label {
  background: red;
  border-radius: 50%;
}

.numberDiv {
  width: 90px;
  display: flex;
  padding-left: 10px;
  }
 
 .numberDiv p {
   width: 30%;
   }

</style>


