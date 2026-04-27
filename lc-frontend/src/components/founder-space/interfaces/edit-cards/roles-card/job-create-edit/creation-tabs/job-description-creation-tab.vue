<script setup>
import { onMounted } from 'vue';
let props = defineProps({
    jobInformation: Object,
    tab: Array
});

import defaultJobDescriptionText from '@/components/founder-space/interfaces/edit-cards/roles-card/job-create-edit/creation-tabs/job-description-creation-tab-default-description-text/text.vue';

onMounted(() => {
    console.log(props.jobInformation);
    document.getElementById('role-title-input').addEventListener('input', (event) => {
        props.jobInformation.jobDescription.title[0] = event.target.value;
    });
    document.getElementById('role-title-input').addEventListener('input', (event) => {
        props.jobInformation.jobDescription.title[0] = event.target.value;
    });
    document.getElementById('role-summary').addEventListener('input', (event) => {
        props.jobInformation.jobDescription.summary[0] = event.target.value;
    });
    updateCharacterCountAndFilter();
});
function showHTML() {
    const editor = document.getElementById('editor');
    console.log(editor.innerHTML);
}

function nextTab(){
    if(document.getElementById('editor')){
        props.jobInformation.jobDescription.description[0] = document.getElementById('editor').innerHTML;
    }
    if(document.getElementById('editor-1')){
        for(let i = 0; i < props.jobInformation.jobQuestions.extraQuestion.length; i++){
            props.jobInformation.jobQuestions.extraQuestion[i].questionHTML[0] = document.getElementById('editor-'+i).innerHTML;
        }
    }
    props.tab[0] += 1;
}

function updateCharacterCountAndFilter(){
    const summaryInput = document.getElementById('role-summary');
    const wordCountElement = document.getElementById('summary-word-count');
    summaryInput.value = summaryInput.value.replace(/\n/g, '');
    const currentLength = summaryInput.value.length;
    if(currentLength > 100){
        summaryInput.value = summaryInput.value.substring(0, 100);
        props.jobInformation.jobDescription.summary[0] = summaryInput.value;
        wordCountElement.innerHTML = '100/100';
    } else {
        props.jobInformation.jobDescription.summary[0] = summaryInput.value;
        wordCountElement.innerHTML = `${currentLength}/100`;
    }
}

</script>
<template>
    <div class="text-container">
        <div class="text">Enter the title of the role</div>
        <input :value="jobInformation.jobDescription.title[0]" class="input" id="role-title-input"/>
        <div class="text">Create a detailed overview of the role. Make sure to mention what the person will be doing and what abilities you're expecting from them. This will be shown to people who select the job to apply to the role, and is meant to provide them with a complete description what it will be.</div>

        <div class="freeform-input">
            <div class="toolbar">
                <img src="@/assets/founder-space/edit/job-edit/freeform-text-editor/bold.png" class="button" onclick="document.execCommand('bold', false, null)" />
                <img src="@/assets/founder-space/edit/job-edit/freeform-text-editor/italics.webp" class="button" onclick="document.execCommand('italic', false, null)" />
                <img src="@/assets/founder-space/edit/job-edit/freeform-text-editor/underline.png" class="button" onclick="document.execCommand('underline', false, null)" />
                <img src="@/assets/founder-space/edit/job-edit/freeform-text-editor/bullet-list.svg" class="button" onclick="document.execCommand('insertUnorderedList', false, null)" />
                <img src="@/assets/founder-space/edit/job-edit/freeform-text-editor/number-list.png" class="button" onclick="document.execCommand('insertOrderedList', false, null)"/>
            </div>
            <div @click="showHTML" class="editor" id="editor" contenteditable="true" style="height:250px" @input="syncContent">
                <div v-if="!jobInformation.jobDescription.description || jobInformation.jobDescription.description.length==0">
                    <defaultJobDescriptionText />
                </div>
                <div id="editor" v-else v-html="jobInformation.jobDescription.description[0]"></div>
            </div>
        </div>
        <div  class="text">Create a brief summary of the role. This will be the first thing shown to potential project partners as a preview of the role through the homepage / search results</div>
        <div style="width:calc(100% - 60px); position:relative;">
            <textarea @input="updateCharacterCountAndFilter" id="role-summary" class="input" style="height:90px" >{{jobInformation.jobDescription.summary[0]}}</textarea>
            <div id="summary-word-count" class="word-count">0/100</div>
        </div>

        <div class="next-button" @click="nextTab">
            Next
        </div>
    </div>
</template> 

<style scoped>
.word-count{
    font-size: 12px;
    color:v-bind(jobInformation.color.textColor[0]);
    filter: invert(.2);
    width:fit-content;  
    float:right;
    margin-top:-68px;
    margin-right:10px;
    z-index: 10;
}
.next-button{
    width:fit-content;
    padding:5px 20px 5px 20px;
    background-color: #36ff09;
    color: white;
    border: white solid 2px;
    border-radius: 10px;
    cursor: pointer;
    user-select: none;
    float:right;
    position: relative;
    margin-top: -10px;
    margin-bottom: 20px;
    margin-right: 60px;
    font-size: 16px;
}
.button:active{
    transform: scale(90%);
    background-color: #aaaaaa;
    box-shadow: 0 0 0 0 rgba(102, 102, 102, 0.24); /* Example of shadow change */

}
.button:hover{
    background-color: #bbbbbb;
}
.button{
    width: 18px;
    height: 18px;
    padding:10px;
    border-radius: 5px;
    border: solid #b0b0b0 1px;
    margin:0;
    background-color: #ffffff8c;
    border: white solid 3px;
    filter: invert(1);
}
.toolbar{
    background-color: #00000036;
    border-radius: 10px;
    overflow: hidden;
    height:fit-content;
    height:45px;
}
.editor{
    border-radius: 10px;
    padding:10px;
    overflow-y:auto;
    white-space: pre-wrap;
    resize: vertical

}
.freeform-input{
    width:calc(100% - 60px);
    resize: none;
    font-size: 16px;
    margin-top:10px;
    border: solid #696969 1px;
    box-sizing: border-box;
    border-radius: 10px;
    margin-bottom: 40px;
    font-family: Arial, sans-serif;
    word-break: break-all; 
    
}

.input{
    width:100%;
    resize: none;
    font-size: 16px;
    padding:10px;
    margin-top:10px;
    color:v-bind(jobInformation.color.textColor[0]);
    box-sizing: border-box;
    border-radius: 10px;
    margin-bottom: 40px;
    font-family: Arial, sans-serif;
    background-color: rgba(0, 0, 0, 0);
}
input,textarea, select, .freeform-input{
    background-color: #00000000;
    box-shadow: inset 0 0 5px #00000070;
}
.text-container{
    text-align: left;
    padding: 30px;
    font-family: Arial, sans-serif;
    padding-bottom: 100px;
    color:v-bind(jobInformation.color.textColor[0]);
}

.text{
    width:calc(100% - 60px);
    font-size: 16px;
    margin-bottom: 10px;
    
}


@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
</style>