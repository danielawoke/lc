<script setup>
import { useRoute, useRouter } from 'vue-router'
import { onMounted, nextTick } from 'vue';
import { ref } from 'vue';
const rawHtmlContent = ref('<p>This is a sample card content with <em>italic text</em> and <strong>bold text</strong>.</p>');
let props = defineProps({
    currentCards: Array,
    jobColor: String
});

useRouter(); 
useRoute();

onMounted(async () => {
    
    console.log(props.jobColor);
    await nextTick();
    let editButton = document.getElementById('edit-button'); 
    editButton.addEventListener("click", function () {
        console.log("Edit button clicked");
        props.SetToEdit[0] = true;
    });
});

async function addNewCard() {
    let newId = 1;
    for (let i = 0; i < props.currentCards.length; i++){
        if(props.currentCards[i].id >= newId){
            newId = props.currentCards[i].id + 1;
        }
    }

    let backgroundColor = props.currentCards.length == 0 ? props.jobColor : props.currentCards[props.currentCards.length -1].backgroundColor[0];
    props.currentCards.push({
        conditions:{
            header:[true],
            paragraph:[true],
            image:[true],
            leftRightRelation:[false]
        },
        header: ["New Card Header"],
        paragraph: ["New card content goes here."],
        image: [""],
        leftRightRelation: [false],
        backgroundColor: [backgroundColor],
        textColor: ["#000000"],
        headerColor: ["#000000"],
        markedForDeletion: [false],
        id: newId,
        recentlySpawned: [true]
    });
    await nextTick();
}

</script>

<template>
    <div class="black-background">
        <div class="card-color-surround">
            <div class="card">
            <div>
                <div class="add-button-text">
                    ADD CARD
                </div>
                <img @click="addNewCard" id="paint" src="@/assets/founder-space/edit/plus-image.png" />
            </div>
            </div>
        </div>
    </div>
</template>

<style scoped>

.black-background{
    background: linear-gradient(to left, rgb(255, 255, 255) ,rgb(255, 255, 255), rgb(255, 255, 255));
    width: 100%;
    height:100px;
}
.add-button-text{
    font-family: fantasy;
    color: #000000;
    font-size: 16px;
    letter-spacing: 10px;
    margin-bottom: 10px;
    text-align: center;
}
#paint{
    margin:auto;
    width:15px;
    height:15px;
    padding: 10px;
    border: rgb(0, 0, 0) solid 4px;
    box-shadow: 0px 0px 10px rgba(255, 255, 255, 0.671);
    border-radius: 50%;
    margin-left:-20px;
    cursor:pointer;
}
.edit-button{
    position: relative;
    width: 60px;
    height: 60px;
    float: right;
    margin-top: -80px;
    border-radius: 50%;
    border: black solid 2px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.671);
    cursor: pointer;
    z-index: 10;
    position: absolute;
    margin-left:-20px;
}
.location-text {
    display: inline-block;
    width: calc(100% - 40px);
    font-family: Arial, sans-serif;
    color: #666;
    font-size: 20px;
    vertical-align: text-top;
    margin-left:5.5px;
}
.inline-correction {
    display: inline-block;
    
    vertical-align: top;
    
}
.card-color-surround{
    background-color: rgba(255, 255, 255, 0);
    box-shadow: 0px 20px 10px rgba(0, 0, 0, 0.671);
}
.card{
    width: calc( (100% - 180px) );
    height: 65px;
    max-width: 1600px;
    border-radius: 10px;
    padding: 20px;
    margin: auto;
}
img{
    max-height:100%;
    max-width: fit-content;
    max-width:100%;
    vertical-align: middle;
}
.image-space {
    display: flex;
    justify-content: center; 
    align-items: center; 
    width: 25vw;
    max-width: 500px;
    height: 400px;
    background-color: rgba(153, 43, 24, 0);
}
.description {
    display: inline-block;
    font-family: Arial, sans-serif;
    color: #444;
    font-size: 18px;
    line-height: 1.6;
    width: calc(100% - min(25vw, 500px) - 180px);
}
#desc-text{
    font-family: fantasy;
    color: #444;
    font-size: 18px;
    line-height: 1.6;
    background-color: transparent;
    margin-left: 40px;
}
.details {
    margin-top: 85px;
    height:auto;
    text-align: left;
    margin-left: 60px;
    overflow: hidden;
    padding-bottom:70px;
}
.title {
    font-weight: bold;
    font-family: fantasy;
    color: #333;
    font-size: 50px;
    margin-left: 60px;
    padding-top:60px;
    width: calc(100% - 60px);
    height:auto;
    overflow-wrap: break-word;
    text-align: left;
    
}
.location {
    font-family: Arial, sans-serif;
    color: #666;
    font-size: 20px;
    text-align: left;
    margin-left: 60px;
    margin-top: 10px;
}
.location-icon {
    width: 21px;
    height: 20px;
    vertical-align: middle;
    margin-right: 10px;
    margin-top: -5px;
}
</style>

<style>
#desc-text{
    font-family: fantasy;
    color: #444;
    font-size: 18px;
    line-height: 1.6;
    background-color: transparent;
    margin-left: 40px;
    white-space: pre-wrap;
    word-wrap: break-word;
}
</style>