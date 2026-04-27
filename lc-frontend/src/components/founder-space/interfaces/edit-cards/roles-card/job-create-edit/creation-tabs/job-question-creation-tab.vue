<script setup>
let props = defineProps({
    jobInformation: Object,
    tab: Array
});

import defaultJobDescriptionText from '@/components/founder-space/interfaces/edit-cards/roles-card/job-create-edit/creation-tabs/job-description-creation-tab-default-description-text/text.vue';
import { onMounted, nextTick } from 'vue';



onMounted(() => {
    for (let i = 0; i < props.jobInformation.jobQuestions.contacts.length; i++) {
        const contact = props.jobInformation.jobQuestions.contacts[i];
        const checkbox = document.getElementById(contact[0] + '-checkbox-contact');
        console.log(contact);
        if (contact[1] === 1) {
            checkbox.innerHTML = "✓";
            checkbox.style.backgroundColor = "green";
        } else if (contact[1] === 2) {
            checkbox.innerHTML = "o";
            checkbox.style.backgroundColor = "blue";
        } else {
            checkbox.innerHTML = "";
            checkbox.style.backgroundColor = "white";
        }
    }
    document.addEventListener('click', syncContent);
    
});

function showHTML() {
    const editor = document.getElementById('editor');
    console.log(editor.innerHTML);
}

async function addNewContactType(){
    console.log(props.jobInformation.jobQuestions.contacts);
    props.jobInformation.jobQuestions.contacts.push(["",1,"custom"]);
    let index = props.jobInformation.jobQuestions.contacts.length -1;
    await nextTick();
    document.querySelectorAll('.alt-checkbox')[document.querySelectorAll('.alt-checkbox').length -1].innerHTML = "✓";
    document.querySelectorAll('.alt-checkbox')[document.querySelectorAll('.alt-checkbox').length -1].style.backgroundColor = "green";
    document.querySelectorAll('.custom-contact-input')[document.querySelectorAll('.custom-contact-input').length -1].id = "current-custom-contact-edit";
    let input = document.getElementById("current-custom-contact-edit");
    input.style.minWidth = "100px";
    input.style.color = "black";
    input.classList.add('editable-label-contact');
    input.focus();
    input.select();
    await nextTick();
    document.addEventListener('mousedown', clickOutOfCustomInput);
}

function clickOutOfCustomInput(e){
    let event = e;
    if (event.target.id != "current-custom-contact-edit") {
        let index = props.jobInformation.jobQuestions.contacts.length -1;
        console.log(props.jobInformation.jobQuestions.contacts);
        let text = document.getElementById('current-custom-contact-edit').value;
        props.jobInformation.jobQuestions.contacts[index][2] = "additional";
        props.jobInformation.jobQuestions.contacts[index][0] = text;
        document.getElementById('current-custom-contact-edit').id = props.jobInformation.jobQuestions.contacts[index][0] + '-label-contact';
        if(text === ""){
            props.jobInformation.jobQuestions.contacts.pop();
        }
        document.removeEventListener('mousedown', clickOutOfCustomInput);
    }
}

function resumeSelect(event) {
    const yesRadio = document.getElementById('resume-yes');
    const noRadio = document.getElementById('resume-no');
    const optionalRadio = document.getElementById('resume-optional');
    
    if (event.target.id === 'resume-yes') {
        props.jobInformation.jobQuestions.resume[0] = "yes";
    } else if (event.target.id === 'resume-no') {
        props.jobInformation.jobQuestions.resume[0] = "no";
    }else if (event.target.id === 'resume-optional') {
        props.jobInformation.jobQuestions.resume[0] = "optional";
    }
}

function setElemOnNum(elem, number){
    if(number === 0){
        elem.innerHTML = "";
        elem.style.backgroundColor = "white";
    }else if(number === 1){
        elem.innerHTML = "✓";
        elem.style.backgroundColor = "green";
    }else if(number === 2){
        elem.innerHTML = "o";
        elem.style.backgroundColor = "blue";
    }
}

async function optionalQuestionSelect(event) {
    console.log(event.target);
    if(event.target.innerHTML === "o"){ 
        event.target.innerHTML = "";
        for(let i = 0; i < props.jobInformation.jobQuestions.contacts.length; i++){
            if(props.jobInformation.jobQuestions.contacts[i][0] === event.target.id.replace('-checkbox-contact','')){
                if(props.jobInformation.jobQuestions.contacts[i][2] === 'additional'){
                    console.log(i);
                    console.log(props.jobInformation.jobQuestions.contacts[i]);
                    props.jobInformation.jobQuestions.contacts.splice(i, 1);
                    await nextTick();
                    let checkboxes = document.querySelectorAll('.alt-checkbox');
                    for(let j = 0; j < props.jobInformation.jobQuestions.contacts.length; j++){
                        setElemOnNum(checkboxes[j], props.jobInformation.jobQuestions.contacts[j][1]);
                    }
                    return;
                }else{
                    props.jobInformation.jobQuestions.contacts[i][1] = 0;
                    event.target.style.backgroundColor = "white";
                }
            }
        }
    }
    else if(event.target.innerHTML === "✓"){
        event.target.innerHTML = "o";
        for(let i = 0; i < props.jobInformation.jobQuestions.contacts.length; i++){
            if(props.jobInformation.jobQuestions.contacts[i][0] === event.target.id.replace('-checkbox-contact','')){
                props.jobInformation.jobQuestions.contacts[i][1] = 2;
                break;
            }
        }
        event.target.style.backgroundColor = "blue";
    }else{
        event.target.innerHTML = "✓";
        for(let i = 0; i < props.jobInformation.jobQuestions.contacts.length; i++){
            if(props.jobInformation.jobQuestions.contacts[i][0] === event.target.id.replace('-checkbox-contact','')){
                props.jobInformation.jobQuestions.contacts[i][1] = 1;
                break;
            }
        }
        event.target.style.backgroundColor = "green";
    }
}

async function AddNewQuestion(){
    const selectElement = document.getElementById('question-type');
    const selectedValue = selectElement.value;
    if(selectedValue === "Null"){
        document.getElementById('default-selection-new-question').innerHTML = "Please select a valid question type";
        document.getElementById('question-type').classList.add('shake-animation');
        await new Promise(resolve => setTimeout(resolve, 500));
        document.getElementById('question-type').classList.remove('shake-animation');
        return;
    }else if(selectedValue === "Free"){
        document.getElementById('default-selection-new-question').innerHTML = "Select the next type of question you'd like to add, then click the plus";
        props.jobInformation.jobQuestions.extraQuestion.push({
            type: "free-form",
            questionHTML: [""],
            options: [],
            isOptional: [false],
            minWord: [null, false],
            maxWord: [null, false]
        });
    }else if(selectedValue === "Multi"){
        document.getElementById('default-selection-new-question').innerHTML = "Select the next type of question you'd like to add, then click the plus";
        props.jobInformation.jobQuestions.extraQuestion.push({
            type:"multi-select",
            questionHTML:[""],
            options: [""],
            isOptional: [false]
        });
    }else if(selectedValue === "Single"){
        document.getElementById('default-selection-new-question').innerHTML = "Select the next type of question you'd like to add, then click the plus";
        props.jobInformation.jobQuestions.extraQuestion.push({
            type:"single-select",
            questionHTML:[""],
            options: [""],
            isOptional: [false]
        });
    }
    await nextTick();
}

async function removeAddedQuestion(event){
    let index = parseInt(event.target.id.replace('remove-question-',''));
    props.jobInformation.jobQuestions.extraQuestion.splice(index, 1);
    await nextTick();
    for(let i = 0; i < props.jobInformation.jobQuestions.extraQuestion.length; i++){
        let removeButton = document.getElementById('remove-question-' + i);
        removeButton.id = 'remove-question-' + i;
    }
}

function updateQuestionOption(questionIndex, optionIndex, event){
    props.jobInformation.jobQuestions.extraQuestion[questionIndex].options[optionIndex] = event.target.value;
}
async function addNewOption(index){
    let length = props.jobInformation.jobQuestions.extraQuestion[index].options.length;
    if(props.jobInformation.jobQuestions.extraQuestion[index].options[length-1].trim() === ""){
        return;
    }
    props.jobInformation.jobQuestions.extraQuestion[index].options.push("");
    console.log(props.jobInformation.jobQuestions.extraQuestion[index].options);
    await nextTick();
}

async function removeQuestionOption(questionIndex, optionIndex){
    console.log(questionIndex, optionIndex);
    props.jobInformation.jobQuestions.extraQuestion[questionIndex].options.splice(optionIndex, 1);
    await nextTick();
}

function updateOptionalQuestionRequired(index, value){
    props.jobInformation.jobQuestions.extraQuestion[index].isOptional[0] = value;
}

function syncContent(event){
    if(!event.target.id.startsWith('editor-')){
        for(let i = 0; i < props.jobInformation.jobQuestions.extraQuestion.length; i++){
            props.jobInformation.jobQuestions.extraQuestion[i].questionHTML[0] = document.getElementById('editor-'+i).innerHTML;
        }
    }
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
function anonymousClick(){
    if (event.target.id === 'anonymous-yes') {
        props.jobInformation.jobQuestions.anonymous[0] = true;
    } else if (event.target.id === 'anonymous-no') {
        props.jobInformation.jobQuestions.anonymous[0] = false;
    }
}
</script>
<template>
    <div class="text-container">
        <div class="question">
            <div class="text">Would you like to request a resume?</div>
            <div class="input-entry">
                <input @click="resumeSelect" id="resume-yes" type="radio"  :checked="props.jobInformation.jobQuestions.resume[0] === 'yes'">
                <label class="text">Yes</label>
            </div>
            <div class="input-entry">
                <input @click="resumeSelect" id="resume-no" type="radio" :checked="props.jobInformation.jobQuestions.resume[0] === 'no'">
                <label class="text">No</label>
            </div>
            <div class="input-entry">
                <input @click="resumeSelect" id="resume-optional" type="radio" :checked="props.jobInformation.jobQuestions.resume[0] === 'optional'">
                <label class="text">Optional</label>
            </div>
        </div>

        <div class="question">
            <div class="text">Select the forms of contact info you'd like to request</div>
            <div class="help-text">Double click to make contact optional</div>
            <div v-for="(contact, index) in jobInformation.jobQuestions.contacts" :key="index" class="input-entry">
                <div :id="contact[0]+'-checkbox-contact'" class="alt-checkbox" @click="optionalQuestionSelect"></div>
                <input v-if="contact[2] === 'custom'" :id="contact[0]+'-label-contact'" class="custom-contact-input" placeholder="replace..."/>
                <label v-else :id="contact[0]+'-label-contact'" class="contact-text">{{ contact[0] }}</label>
            </div>

            <div class="input-entry">
                <div @click="addNewContactType" id="add-contact-button" class="checkAdd" type="checkbox"> + </div>
                <label class="text">Other</label>
            </div>
        </div>

        <!-- <div class="question">
            <div class="text">Would you like to let people apply anonymously? (This will make sumbitting a name optional and will mask the applicant's profile with an alias if accepted onto the project. This can be undone later at the applicant's choice)</div>
            <div class="input-entry">
                <input @click="anonymousClick" id="anonymous-yes" type="radio" value="required" :checked="jobInformation.jobQuestions.anonymous[0] === true">
                <label class="text">Yes</label>
            </div>
            <div class="input-entry">
                <input @click="anonymousClick" id="anonymous-no" type="radio" value="optional" :checked="jobInformation.jobQuestions.anonymous[0] === false">
                <label class="text">No</label>
            </div>
        </div> -->

        <div v-for="(question, index) in jobInformation.jobQuestions.extraQuestion" :key="index">
            <div class="added-question">
                <div class="text">Write the text for the free-form text question you'd like to ask here</div>
                <div class="freeform-input">
                    <div class="toolbar">
                        <img src="@/assets/founder-space/edit/job-edit/freeform-text-editor/bold.png" class="button" onclick="document.execCommand('bold', false, null)" />
                        <img src="@/assets/founder-space/edit/job-edit/freeform-text-editor/italics.webp" class="button" onclick="document.execCommand('italic', false, null)" />
                        <img src="@/assets/founder-space/edit/job-edit/freeform-text-editor/underline.png" class="button" onclick="document.execCommand('underline', false, null)" />
                    </div>
                    <div class="editor" :id="'editor-'+index" contenteditable="true" @click="syncContent(index, $event)" v-html="question.questionHTML[0]"></div>
                </div>

                <div v-if="question.type=='free-form'" class="question" style="margin-top: -10px;">
                    <div class="text"></div>
                    <div class="input-entry">
                        <div class="text">
                            Select min or max to create character limits for the applicant's response
                        </div>
                    </div>
                    <br/>
                    <div class="number-limit">
                        <input type="checkbox" value="required" v-model="question.minWord[1]">
                        <label v-bind:style="[question.minWord[1] ? 'opacity: 1' : 'opacity: .5']" class="number-label">Min:</label>
                        <input v-bind:style="[question.minWord[1] ? 'opacity: 1' : 'opacity: .5']" class="character-count-input" v-model="question.minWord[0]">
                    </div>

                    <div class="number-limit">
                        <input type="checkbox" value="required" v-model="question.maxWord[1]">
                        <label v-bind:style="[question.maxWord[1] ? 'opacity: 1' : 'opacity: .5']" class="number-label">Max:</label>
                        <input v-bind:style="[question.maxWord[1] ? 'opacity: 1' : 'opacity: .5']" class="character-count-input" v-model="question.maxWord[0]">
                    </div>
                </div>
                <div v-else>
                    <div class="text">
                        Click the plus to add options for this question
                    </div>
                    <div class="check-entries-editable">
                        <div v-for="(option, optionIndex) in question.options" :key="optionIndex" class="question-option-entry">
                            <input class="question-option-input" :value="option" @input="updateQuestionOption(index, optionIndex, $event)"/>
                            <div @click="removeQuestionOption(index, optionIndex)" class="remove-option"></div>
                        </div>
                        <!-- modifyt this so that the outer border spins 90 degrees when hovered, but the + in the middle stays the same -->
                        <div @click="addNewOption(index)" :id="'add-optional-'+index" class="add-option"></div>
                    </div>
                </div>

                <div class="question">
                    <div class="text">Would you like to make this question optional?</div>
                    <div class="input-entry">
                        <input @click="updateOptionalQuestionRequired(index, 'required')" type="radio" value="required" v-model="question.isOptional[0]">
                        <label class="text">Yes</label>
                    </div>
                    <div class="input-entry">
                        <input @click="updateOptionalQuestionRequired(index, 'optional')" type="radio" value="optional" v-model="question.isOptional[0]">
                        <label class="text">No</label>
                    </div>
                </div>
                <div class="remove-question-block">
                    <div @click="removeAddedQuestion" :id="'remove-question-' + index" class="remove-question"></div>
                </div>
            </div>
        </div>

        <div class="add-question-section">
            <div class="drop-down-container">
                <div class="drop-down-custom">
                    <div @click="AddNewQuestion" class="sumbit-added-contact-button"></div>
                </div>
                <select id="question-type" required  class="drop-down"> 
                    <option id="default-selection-new-question" value="Null">Select the next type of question you'd like to add, then click the plus</option>
                    <option value="Free">Free form text</option>
                    <option value="Multi">Multi option (check list)</option>
                    <option value="Single">Single option (choose one of many, ex. yes/no)</option>
                </select>
                <div class="drop-down-sign">
                    <span style="color:black">></span>
                </div>
            </div>
        </div>
        <div class="next-button" @click="nextTab">
            Next
        </div>
    </div>
</template> 

<style scoped>
.add-question-section:hover .drop-down-sign{
    transform: rotate(90deg) translate(-15px,-0px);

}
.drop-down-sign{
    transition: transform 0.3s ease;
    position: absolute;
    right: 110px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 16px;
    background:rgb(255, 255, 255);
    padding:2px;
    padding-left:10px;
    padding-right:10px;
    border-radius: 50%;
}
.shake-animation{
    animation: shake 0.5s;
}
@keyframes shake {
  0% { transform: translate(1px, 0); }
  20% { transform: translate(-1px, 0); }
  40% { transform: translate(1px, 0); }
  60% { transform: translate(-1px, 0); }
  80% { transform: translate(1px, 0); }
  100% { transform: translate(0, 0); }
}
input,textarea{
    background-color: #00000000;
    box-shadow: inset 0 0 2px #00000070;
    color: v-bind(jobInformation.color.textColor[0]);
}
.editable-label-contact{
    color: v-bind(jobInformation.color.textColor[0]);
    width: 300px;
}
input[type="text"] {
  color: v-bind(jobInformation.color.textColor[0]);
}
.alt-checkbox{
    display: inline-block;
    background-color: #ffffff;
    font-size: 14px;
    width:5px;
    height:6px;
    color: white;
    border:#949494 solid 1px;
    vertical-align: middle;
    line-height: 8.5px;
    padding:5px;
    padding-left: 2.5px;
    padding-top: 1.5px;
    padding-top: 1.5px;
    border-radius: 3px;
    margin-right: 3px;
    cursor: pointer;
    user-select: none;
    margin-bottom: 2px;
}
.resume-optional-question{
    margin-bottom: 30px;
    width: calc(100% - 100px);
    margin-top: 30px;
    font-size: 12px;
}
.optional-contact-info{
    margin-bottom: 30px;
    width: calc(100% - 60px);
    margin-top: 30px;
    font-size: 12px;
}
.help-text{
    font-size: 12px;
    color: v-bind(jobInformation.color.textColor[0]);
    filter: invert(.3);
    margin-top: -5px;
    margin-bottom: 5px;
}
.fade-left{
    animation: fadeLeft .25s ease-in;
}

.number-label{
    display: inline-block;
    font-size: 16px;
    margin-left:5px;
}
.number-limit{
    display: inline-block;
    margin-right: 20px;
    
}
.character-count-input{
    display: inline-block;
    width:70px;
    height:15px;
    margin-top: 10px;
    margin-left: 5px;
    border-radius: 5px;

}
.remove-question-text{
    margin: auto;
    text-align: center;
    cursor: pointer;
    user-select: none;
    font-size: 15px;
}
.remove-question-block{
    background-color: #00000028;
    width: calc(100% + 25px);
    margin-right: -30px;
    height: 40px;
    border-radius: 10px;
    float:right;
    text-align: center;
    cursor: pointer;
    user-select: none;
    font-size: 18px;
    padding: 5px;
    padding-right: 30px;
    margin-bottom: -20px;
}
.remove-question{
    display: inline-block;
    width:20px;
    height:20px;
    padding:10px;
    background-color: #c7c7c75b;
    filter: invert(1);
    color: rgb(0, 0, 0);
    text-align: center;
    cursor: pointer;
    user-select: none;
    position: relative;
    background-image: url('@/assets/founder-space/edit/job-edit/file-remove-icon.webp');
    margin-top: 0px;
    font-size: 6px;
    float:right;
    background-size: 25px 25px;
    background-repeat: no-repeat;
    background-position: center;
    border-radius: 15px;
    box-shadow: 0 0 5px #ffffff;
    z-index: 0;
}
.add-option:hover{
    transform: scale(1.1);
    z-index: 10;
    color: black;
}
.add-option{
    display: inline-block;
    width:27px;
    height:27px;
    background-color: white;
    border: #ffffff solid 1px;
    color: white;
    box-shadow: 0px 0px 5px #000000a1;
    cursor: pointer;
    user-select: none;
    position: relative;
    font-size: 16px;
    background-image: url('@/assets/founder-space/edit/job-edit/add-plus.png');
    background-size: 130% auto;
    background-repeat: no-repeat;
    background-position: center;
    margin-left: 10px;
    border-radius: 10px;
    margin-bottom: 8px;
    margin-top: 8px;
    transition: all 0.2s ease-in-out;
    border-bottom: solid black 1.5px; 
    border-left: solid black 1.5px; 
    border-radius: 20px;
}
.remove-option{
    display: inline-block;
    width:30px;
    height:30px;
    background-color: #ffffff;
    color: white;
    cursor: pointer;
    user-select: none;
    position: relative;
    font-size: 16px;
    filter: invert(1);
    background-image: url('@/assets/founder-space/edit/job-edit/trash-bin.png');        
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;
    margin-left: 10px;
    margin-bottom: -10px;
    border-radius: 10px;
}
.question-option-input{
    display: inline-block;
    width:calc(100% - 60px);
    resize: none;
    font-size: 16px;
    padding:5px;
    margin-top:10px;
    border: solid #0000005b 1px;
    box-sizing: border-box;
    font-family: fantasy;
    margin-bottom: 10px;
    height:30px;
    box-shadow: inset 0 0 5px #00000070;
    color: v-bind(jobInformation.color.textColor[0]);
}
.added-question{
    
    padding:20px;
    width: calc(100% - 100px);
    margin-top: 30px;
    margin-left: -20px;
    border-left:#0000003d solid 3px;
    border-radius: 20px;
    overflow: hidden;
}
.add-question-section{
    font-size: 12px;
    position: relative;
}
.sumbit-added-contact-button:hover{
    background-color: #0000008e;
    z-index: 10;
}
.drop-down-custom:hover .drop-down-contents{
    display: block;
    background-color: white;
    box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
    position: absolute;
    margin-top: -40px;
    z-index: 0;
}

.drop-down-contents{
    display: none;
}
.drop-down-prev{
    display: inline-block;
    padding-left: 10px;
    width:calc(100% - 52px);
    padding-bottom:6px;
    font-size: 16px;
    cursor: pointer;
    user-select: none;
}
.drop-down-entry{
    padding:10px;
    padding-left: 50px;;
    font-size: 16px;
    box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.062);
    cursor: pointer;
    user-select: none;
}
.sumbit-added-contact-button{
    display: inline-block;
    width:38px;
    height: 38px;
    background-color: #2e2e2e27;
    border:#5f5f5f solid 1px;
    color: white;
    cursor: pointer;
    user-select: none;
    position: relative;
    font-size: 16px;
    background-image: url('@/assets/founder-space/edit/job-edit/add-plus.png');
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;
    margin-bottom: -50px;
    border-radius: 10px;
    z-index: 0;
}

.drop-down{
    width:calc(100% - 100px);
    height:42px;
    font-size: 15px;
    margin-bottom: 28px;
    padding-left: 50px;
    border: solid #00000080 2px;
    border-radius: 10px;
    box-sizing: border-box;
    font-family: Arial, sans-serif;
    background-color: rgba(255, 44, 44, 0);
    overflow:hidden;
    color: v-bind(jobInformation.color.textColor[0]);
}
.drop-down-custom{
    position: relative;
    height:fit-content;
    font-size: 16px;
    width:300px;
    border: solid #00000000 1px;
    font-family: Arial, sans-serif;
}
.custom-contact-input{
    width:105px;
    font-size: 16px;
    padding:5px;
    margin-top:0px;
    height: 23px;
    border: solid #0000005b 1px;
    box-sizing: border-box;
    font-family: Arial, sans-serif;
    color: v-bind(jobInformation.color.textColor[0]);
}
.checkAdd{
    display: inline-block;
    background-color: #000000;
    font-size: 14px;
    width:5px;
    height:6px;
    color: white;
    border:#949494 solid 1px;
    vertical-align: middle;
    line-height: 8.5px;
    padding:5px;
    padding-left: 2.5px;
    padding-top: 1.5px;
    padding-top: 1.5px;
    border-radius: 3px;
    margin-right: 3px;
    cursor: pointer;
    user-select: none;
    margin-bottom: 2px;
}
.added-input{
    width:calc(100% - 100px);
    resize: none;
    font-size: 16px;
    padding:5px;
    margin-top:10px;
    border: solid #0000005b 1px;
    box-sizing: border-box;
    font-family: Arial, sans-serif;
    margin-bottom: 10px;
}
.question{
    margin-bottom: 30px;
    width: calc(100% - 60px);
}
.input-entry{
    display: inline-block;
    margin-right:20px;
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
    margin-top: 100px;
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
    resize: vertical;
    height:80px;

}
.freeform-input{
    width:calc(100%);
    resize: none;
    font-size: 16px;
    margin-top:10px;
    border: solid #696969 1px;
    box-sizing: border-box;
    border-radius: 10px;
    margin-bottom: 40px;
    font-family: Arial, sans-serif;
    word-break: break-all;
    box-shadow: inset 0 0 10px #00000073; 
}

.input{
    width:calc(100% - 60px);
    resize: none;
    font-size: 16px;
    padding:10px;
    margin-top:10px;
    border: solid #696969 1px;
    box-sizing: border-box;
    border-radius: 10px;
    margin-bottom: 40px;
    font-family: Arial, sans-serif;
}
.text-container{
    text-align: left;
    padding: 30px;
    font-family: Arial, sans-serif;
    padding-bottom: 100px;
    font-family: Arial, sans-serif;
    color:#000000;
    color:v-bind(jobInformation.color.textColor[0]);
}

.text{
    width:calc(100%);
    font-size: 16px;
    margin-bottom: 10px;
}
.contact-text{
    width:calc(100%);
    font-size: 16px;
    margin-bottom: 10px;
}

@keyframes fadeLeft {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes fadeIn {
  from {
    /*height:0;*/
    opacity: 0;
  }
  to {
   /* height:60px;*/
    opacity: 1;
  }
}
</style>


        <!-- <div class="added-question">
            <div class="text">
                Write the text for the question you'd like to ask here
            </div>
            <div class="freeform-input">
                <div class="toolbar">
                    <img src="@/assets/founder-space/edit/job-edit/freeform-text-editor/bold.png" class="button" onclick="document.execCommand('bold', false, null)" />
                    <img src="@/assets/founder-space/edit/job-edit/freeform-text-editor/italics.webp" class="button" onclick="document.execCommand('italic', false, null)" />
                    <img src="@/assets/founder-space/edit/job-edit/freeform-text-editor/underline.png" class="button" onclick="document.execCommand('underline', false, null)" />
                </div>
                <div class="editor" id="editor" contenteditable="true" style="" @input="syncContent">
                </div>
            </div>
            <div class="text">
                Click the plus to add options for this question
            </div>
            <div class="check-entries-editable">
                <div class="question-option-entry">
                    <input class="question-option-input"/>
                    <div class="remove-option"></div>
                </div>
                <div class="add-option"></div>
            </div>

            <div class="question">
                <div class="text">Would you like to make this question optional?</div>
                <div class="input-entry">
                    <input type="radio" value="required" v-model="jobInformation.resumesRequired">
                    <label class="text">Yes</label>
                </div>
                <div class="input-entry">
                    <input type="radio" value="optional" v-model="jobInformation.resumesRequired">
                    <label class="text">No</label>
                </div>
            </div>
            <div class="remove-question-block">
                <div class="remove-question">
                </div>
            </div>
        </div> -->

        <!-- Multi / select -->
        
        <!-- <div class="added-question">
            <div class="text">
                Write the text for the question you'd like to ask here
            </div>
            <div class="freeform-input">
                <div class="toolbar">
                    <img src="@/assets/founder-space/edit/job-edit/freeform-text-editor/bold.png" class="button" onclick="document.execCommand('bold', false, null)" />
                    <img src="@/assets/founder-space/edit/job-edit/freeform-text-editor/italics.webp" class="button" onclick="document.execCommand('italic', false, null)" />
                    <img src="@/assets/founder-space/edit/job-edit/freeform-text-editor/underline.png" class="button" onclick="document.execCommand('underline', false, null)" />
                </div>
                <div class="editor" id="editor" contenteditable="true" style="" @input="syncContent">
                </div>
            </div>
            <div class="text">
                Click the plus to add options for this question
            </div>
            <div class="check-entries-editable">
                <div class="question-option-entry">
                    <input class="question-option-input"/>
                    <div class="remove-option"></div>
                </div>
                <div class="add-option"></div>
            </div>

            <div class="question">
                <div class="text">Would you like to make this question optional?</div>
                <div class="input-entry">
                    <input type="radio" value="required" v-model="jobInformation.resumesRequired">
                    <label class="text">Yes</label>
                </div>
                <div class="input-entry">
                    <input type="radio" value="optional" v-model="jobInformation.resumesRequired">
                    <label class="text">No</label>
                </div>
            </div>
            <div class="remove-question-block">
                <div class="remove-question">
                    
                </div>
            </div>
            

        </div> -->

        <!-- free form -->

<!---   <div class="added-question">
            <div class="text">
                Write the text for the free-form text question you'd like to ask here
            </div>
            <div class="freeform-input">
                <div class="toolbar">
                    <img src="@/assets/founder-space/edit/job-edit/freeform-text-editor/bold.png" class="button" onclick="document.execCommand('bold', false, null)" />
                    <img src="@/assets/founder-space/edit/job-edit/freeform-text-editor/italics.webp" class="button" onclick="document.execCommand('italic', false, null)" />
                    <img src="@/assets/founder-space/edit/job-edit/freeform-text-editor/underline.png" class="button" onclick="document.execCommand('underline', false, null)" />
                </div>
                <div class="editor" id="editor" contenteditable="true" style="" @input="syncContent">
                </div>
            </div>

            <div class="question" style="margin-top: -10px;">
                <div class="text"></div>
                <div class="input-entry">
                    <div class="text">
                        Select min or max to create word limits for the applicant's response
                    </div>
                </div>
                <br/>
                <div class="number-limit">
                    <input type="checkbox" value="required" v-model="jobInformation.resumesRequired">
                    <label class="number-label">Min:</label>
                    <input class="character-count-input" v-model="jobInformation.resumesRequired">
                </div>

                <div class="number-limit">
                    <input type="checkbox" value="required" v-model="jobInformation.resumesRequired">
                    <label class="number-label">Max:</label>
                    <input class="character-count-input" v-model="jobInformation.resumesRequired">
                </div>
                
            </div>

            <div class="question">
                <div class="text">Would you like to make this question optional?</div>
                <div class="input-entry">
                    <input type="radio" value="required" v-model="jobInformation.resumesRequired">
                    <label class="text">Yes</label>
                </div>
                <div class="input-entry">
                    <input type="radio" value="optional" v-model="jobInformation.resumesRequired">
                    <label class="text">No</label>
                </div>
            </div>

            <div class="remove-question-block">
                <div class="remove-question">
                    
                </div>
            </div>
        </div> -->


        <!-- check -->