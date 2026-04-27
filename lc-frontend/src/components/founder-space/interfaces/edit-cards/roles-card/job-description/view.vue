<script setup>
import { ref, nextTick} from 'vue';
import { onMounted } from 'vue';
import MainCardMiniView from '@/components/founder-space/interfaces/edit-cards/color-change/mini-views/main-card-mini-view.vue';
import description from '@/components/job-page/description.vue';
import JobPreview from '@/components/founder-space/interfaces/edit-cards/roles-card/job-description/job-view.vue';
let props = defineProps({
    color: Array,
    renderVar: Array,
    jobInformation: Object
});

const closePopup = async () => {
    props.renderVar[0] = false;
}

</script>

<template>
    <div @click.self="closePopup" id="popup-backdrop" class="popup-backdrop">
        <div class="popup">
            <div class="header">
                <div class="buttons">
                    <img  @click="closePopup" class="close-button" value="Close" src="@/assets/user-tools/job-view/x-icon.png" />
                </div>
            </div>
            <div class="container">
                <!-- <div class="left"><</div> -->
                    <JobPreview :jobInformation="props.jobInformation" :color="props.color"/>
                <!-- <div class="right">></div> -->
            </div>
        </div>    
    </div> 
</template>

<style scoped>
.left{
    position: absolute;
    top: 50%;
    left: 0;
    color: rgb(0, 0, 0);
    font-weight: bold;
    user-select: none;
    cursor: default;
    transform: translateY(calc(-50% + 110px - 50px));
    font-size: 30px;
    line-height: 50px;
    height: 50px;
    width: 50px;
    margin-left:10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.767);
    background-image: linear-gradient(45deg, rgb(255, 255, 255), rgba(255, 255, 255, 0.479));
    border: solid black 5px;
    border-radius: 50%;
    
}
.right{
    position: absolute;
    top: 50%;
    right: 0;
    font-size: 50px;
    color: rgb(0, 0, 0);
    font-weight: bold;
    user-select: none;
    cursor: default;
    transform: translateY(calc(-50% + 110px - 50px));
    font-size: 30px;
    line-height: 50px;
    height: 50px;
    width: 50px;
    margin-right:10px;
    background-image: linear-gradient(45deg, rgb(255, 255, 255), rgba(255, 255, 255, 0.479));
    border: solid black 5px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.767);
    border-radius: 50%;
}
.header {
    text-align: left;
    background-color: v-bind(props.jobInformation.color.backgroundColor[0]);
    opacity: .9;
    box-shadow: rgba(0, 0, 0, 0.329) 0px 4px 6px -1px;
    width:100%;
    max-width: 1050px;
    padding-bottom:20px;
    padding-top:30px;
    position: absolute;
    height:60px;
    left: 50%;
    transform: translateX(-50%);
}
.container{
    font-family: sans-serif;
    margin-top: 200px;
    font-size: 18px;
    padding: 150px;
    line-height: 1.6;
    max-width: 750px;
    margin: auto;
    background-color: v-bind(props.jobInformation.color.backgroundColor[0]);
    color: v-bind(props.jobInformation.color.textColor[0]);
    height: calc(100vh - 500px);
    padding-bottom: 300px;
    transition: all 0.5s ease;
    overflow-y:auto;
    overflow-x:hidden;
}
.buttons{
    float: right;
    width:300px;
    margin-right: 80px;
}
.close-button {
    font-size: 16px;
    padding:30px;
    display: block;
    padding: 10px;
    background-color:rgba(48, 48, 48, 0);
    color: white;
    font-family: fantasy;
    letter-spacing: 1.5px;
    box-shadow: 0 0 15px rgba(255, 255, 255, 0.726);
    margin-top: -10px;
    transition: box-shadow 0.3s ease;
    height: 20px;
    margin-top: -30px;
    width: 20px;
    padding: 45px;
    float: right;
    margin-right: -20px;
    filter: invert(70%);
}

.close-button:hover{
    box-shadow: 0 0 15px rgb(99, 99, 99);
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
    width: calc(100% - 55px);
    height: 100%;
    background-color: rgba(0, 0, 0, 0.301);
    position: fixed;
    top: 0;
    left: 55px;

    z-index: 10;
    opacity: 1;
    animation: fadeIn 0.3s;
    transition: opacity 0.3s ease-out;
    padding-bottom: 100px;
    z-index: 1000;
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
    background-color: rgba(207, 207, 207, 0.308);
    color: rgb(0, 0, 0);
    width:  calc( (100% - 0px ));
    max-width: 1300px;
    height: calc( (100% - 110px));
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    box-shadow: rgba(0, 0, 0, 0.171) 0px 5px 15px 15px;
    overflow:hidden;
}

.footer{
    background-color: rgb(255, 255, 255);
    box-shadow: rgb(138, 137, 137) 0px 4px 6px -1px;
    width:100%;
    height:40px;
    padding: 20px;
    margin: -20px;
    position: absolute;
    bottom: 0;
    margin-top: -20px;
}


</style>