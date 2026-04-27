<script setup>
let props = defineProps({
    jobInformation: Object,
    jobID: String,
    tab: Array,
    jobs: Array,
    renderVar: Array,
    newJob: Boolean,
    viewMode: Boolean,
    userID: String,
    projectTitle: String
});

import defaultJobDescriptionText from '@/components/founder-space/interfaces/edit-cards/roles-card/job-create-edit/creation-tabs/job-description-creation-tab-default-description-text/text.vue';
import { nextTick } from 'vue';
import { onMounted } from 'vue';
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios';
const apiURL = import.meta.env.VITE_APP_API_URL;
let route = useRoute();
let responses = ref([]);
import { supabase } from "@/lib/supabase.js";
let resumeFile = null;

onMounted(async () => {
    document.getElementById("questions-block").style.height = "auto";
    let heightAuto = document.getElementById("questions-block").offsetHeight;
    document.getElementById("questions-block").style.height = "100%";
    let heightPercent = document.getElementById("questions-block").offsetHeight;
    if (heightAuto > heightPercent) {
        document.getElementById("questions-block").style.height = heightAuto + "px";
    }
    window.addEventListener("resize", () => {
        console.log("resized");
        document.getElementById("questions-block").style.height = "auto";
        let heightAuto = document.getElementById("questions-block").offsetHeight;
        document.getElementById("questions-block").style.height = "100%";
        let heightPercent = document.getElementById("questions-block").offsetHeight;
        if (heightAuto > heightPercent) {
            document.getElementById("questions-block").style.height = heightAuto + "px";
            document.getElementById("questions-block").style.marginBottom = "0vh";
        }else {
            document.getElementById("questions-block").style.marginBottom = "-8vh";
        }
    });
    responses.value = [];
    for(let question of props.jobInformation.jobQuestions.extraQuestion){
        if(question.type === "free-form"){
            responses.value.push({type: "free-form", response: ""});
        } else if (question.type === "single-select"){
            responses.value.push({type: "single-select", response: null});
        } else if (question.type === "multi-select"){
            responses.value.push({type: "multi-select", response: []});
        }
    }
    console.log("Initial responses state:", responses.value);
});

function showHTML() {
    const editor = document.getElementById('editor');
    console.log(editor.innerHTML);
}

function addRedAsterisk(html) {
    let indents = html.split('</div>');
    if(indents[indents.length-1] == ''){
        indents[indents.length-2] += '<div style="display:inline-block;color:red;">*</div>';
    } else {
        indents[indents.length-1] += '<div style="display:inline-block;color:red;">*</div>';
    }
    return indents.join('</div>');
}

function updateCount(index){
    let input = document.getElementsByClassName("free-form-input")[index];
    let characterCount = input.value.length;
    if(input.value.trim() === ''){
        characterCount = 0;
    }
    document.getElementsByClassName("word-count")[index].innerText = characterCount + "/" + props.jobInformation.jobQuestions.extraQuestion[index].maxWord[0];
    if(props.jobInformation.jobQuestions.extraQuestion[index].maxWord[1]){
        if(characterCount > props.jobInformation.jobQuestions.extraQuestion[index].maxWord[0]){
            input.value = input.value.substring(0, props.jobInformation.jobQuestions.extraQuestion[index].maxWord[0]);
            characterCount = props.jobInformation.jobQuestions.extraQuestion[index].maxWord[0];
            document.getElementsByClassName("word-count")[index].innerText = characterCount + "/" + props.jobInformation.jobQuestions.extraQuestion[index].maxWord[0];
        }
    }
    if(props.jobInformation.jobQuestions.extraQuestion[index].minWord[1]){
        if(characterCount < props.jobInformation.jobQuestions.extraQuestion[index].minWord[0]){
            document.getElementsByClassName("min-word-count")[index].style.display = "block";
        } else {
            document.getElementsByClassName("min-word-count")[index].style.display = "none";
        }
    }
}


async function uploadDocument(blob, job_id,user_id, type){

    const filePath = `${job_id}_${user_id}.${type}`;
    await supabase.auth.signInWithPassword({
        email: import.meta.env.VITE_ADMIN_USERNAME,
        password: import.meta.env.VITE_ADMIN_PASSWORD
    });

    try{
        await supabase.storage.from("resumes").upload(filePath, blob);
    }catch(err){
        console.error("Error uploading resume:", err);
    }
    
    const { data, error } = supabase.storage.from("resumes").getPublicUrl(filePath);
    
    if (error) {
        console.error(error);
    } else {
        console.log("URL:", data.publicUrl);
    }

    return data.publicUrl;

}


async function submitApplication() {
    let contactInfo = [];
    for (let i = 0; i < props.jobInformation.jobQuestions.contacts.length; i++){
        let contactType = props.jobInformation.jobQuestions.contacts[i][0];
        let contactRequired = props.jobInformation.jobQuestions.contacts[i][1];
        let inputElement = document.getElementById(`contact-${i}`);
        if(!inputElement){
            continue;
        }
        let val = inputElement.value? inputElement.value.trim() : "";
        if(contactRequired == 1 && (val === "" || val.length === 0)){
            alert("Please fill out the required contact information: " + contactType);
            return;
        }
        contactInfo.push([contactType, val.trim()]);
    }

    let resumeNameBlock = document.querySelector('.resume-box').files[0];
    if((props.jobInformation.jobQuestions.resume[0] === 'yes') && !resumeNameBlock){
        alert("Please attach a resume to apply for this position.");
        return;
    }

    for(let responsesIndex in responses.value){
        if(responses.value[responsesIndex].type === "free-form"){
            responses.value[responsesIndex].response = document.getElementById("free-form-" + responsesIndex).value;
        }
    }

    let resumeLink = null;

    try{
        if(!resumeNameBlock && props.jobInformation.jobQuestions.resume[0] === 'optional'){
            resumeLink = "None given";
        } else if(resumeNameBlock){
            resumeLink = await uploadDocument(resumeFile, props.jobID, props.userID, resumeFile.name.split('.').pop());
        }
    }catch(error){
        console.error("Error uploading resume:", error);
        alert("There was an error uploading your resume. Please try again.");
        return;
    }

    let selfStatementElement = document.getElementById("self-statement");   

    let requestObject = {
        jobInfo: props.jobInformation,
        contactInfo: contactInfo,
        responses: responses.value,
        resume: resumeLink,
        jobID: props.jobID,
        userID: props.userID,
        projectID: route.params.projectId,
        projectName: props.projectTitle,
        selfStatement: selfStatementElement ? selfStatementElement.value : ""
    }

    try{
        await axios.post(`${apiURL}projects/apply`, requestObject);
        applicationSumbited.value = true;
    }catch(error){
        console.log(error);
        return;
    }
}

let applicationSumbited = ref(false);


function updateMultiSelect(questionIndex, optionIndex){
    let selectedOption = props.jobInformation.jobQuestions.extraQuestion[questionIndex].options[optionIndex];
    let selectedOptions = responses.value[questionIndex].response || [];
    const optionExists = selectedOptions.includes(selectedOption);
    if(optionExists){
        responses.value[questionIndex].response = selectedOptions.filter(opt => opt !== selectedOption);
    } else {
        responses.value[questionIndex].response = [...selectedOptions, selectedOption];
    }
}

function updateSingleSelect(questionIndex, optionIndex){
    responses.value[questionIndex].response = props.jobInformation.jobQuestions.extraQuestion[questionIndex].options[optionIndex];
    console.log(responses.value);
}



function updateResume(event){
    let file = event.target.files[0];
    if(file.size > 5 * 1024 * 1024){
        alert("File size exceeds 5MB limit. Please choose a smaller file.");
        event.target.value = "";
    }else if(file.type !== "application/pdf" && file.type !== "application/msword" && file.type !== "application/vnd.openxmlformats-officedocument.wordprocessingml.document"){
        alert("Invalid file type. Please upload a PDF or Word document.");
        event.target.value = "";
    }else{
        resumeFile = file;
        fileName.value = file.name;
        resumeAccepted.value = true;
    }
}
let fileName = ref("ads");
let resumeAccepted = ref(false);


function capStatementCount(){
    let input = document.getElementById("self-statement");
    if(input.value.length > 100){
        input.value = input.value.substring(0, 100);
    }
    document.getElementById("self-statement-word-count").innerText = input.value.length + "/100";
}

</script>
<template>
    <div id="text-block" class="text-container">
        <div v-if="applicationSumbited" style="max-width:750px; margin:auto; padding: 20px;">
            <img style="width:100px; display:block; margin:auto;"/>
            Application Submitted! Can view application status/info in profile > applications tab.
        </div>
        <div v-else>
            <div style="max-width:750px; margin:auto; padding: 20px;">
                <h1>
                    {{ jobInformation.jobDescription.title[0] }}
                </h1>
                <div class="text" v-html="jobInformation.jobDescription.description[0]"></div>

            </div>
            <div :style="{backgroundColor: 'rgba(0, 0, 0, 0.116)', padding: '20px', paddingBottom: '300px', marginBottom: '-300px'}">
                <div v-if="props.userID==null && viewMode" style="text-align:left; color:red; max-width:750px; margin:auto; padding: 20px; font-size: 14px; font-weight: normal;">
                    * You cannot apply unless you have an account. please login to apply. *
                </div>
                <div id="questions-block" class="questions">
                    <div v-if="jobInformation.jobQuestions.anonymous[0]" class="question">
                        <div class="text">The creators of this project have allowed anonymous applications, would you like to apply anonymously?</div>
                        <div class="input-entry">
                            <input type="radio" value="required" v-model="jobInformation.resumesRequired">
                            <label class="text">Yes</label>
                        </div>
                        <div class="input-entry">
                            <input type="radio" value="optional" v-model="jobInformation.resumesRequired">
                            <label class="text">No</label>
                        </div>
                    </div>

                    <div class="question">
                        <!-- <div class="text">
                            First Name
                            <div style="display:inline-block;color:red;" v-if="!jobInformation.jobQuestions.anonymous[0]">*</div>
                            <input class="input" />
                        </div>
                        <div class="text">
                            Last Name
                            <div style="display:inline-block;color:red;" v-if="!jobInformation.jobQuestions.anonymous[0]" >*</div>
                            <input class="input" />
                        </div> -->
                        <div v-for="(contactType, contactIndex) in jobInformation.jobQuestions.contacts" :key="contactType" class="text">
                            <div v-if="contactType[1]>0">
                                {{ contactType[0] }}
                                <div style="display:inline-block;color:red;" v-if="contactType[1]==1">*</div>
                                <input class="input" :id="`contact-${contactIndex}`"/>
                            </div>
                        </div>
                    </div>

                    <div v-if="(jobInformation.jobQuestions.resume[0] =='yes' || jobInformation.jobQuestions.resume[0] =='optional') && resumeAccepted==false" class="question">
                        <div class="text">Attach a resume <div v-if="jobInformation.jobQuestions.resume[0] =='yes'" style="display:inline-block;color:red;">*</div> </div> 

                        <div class="resume-container-styling">
                            <input class="resume-box" type="file" @change="updateResume" accept=".pdf,.doc,.docx"/>
                        </div>
                        <div class="resume-text"><div>+</div>Upload Resume Here</div>
                        <div class="sub-resume-text">File must be less than 5MB.</div>

                    </div>
                    <div v-if="(jobInformation.jobQuestions.resume[0] =='yes' || jobInformation.jobQuestions.resume[0] =='optional') && resumeAccepted==true" class="question">
                        <div class="text">Attach a resume <div v-if="jobInformation.jobQuestions.resume[0] =='yes'" style="display:inline-block;color:red;">*</div> </div> 

                        <div class="resume-container-styling-accpeted">
                            <input class="resume-box" type="file" @change="updateResume" accept=".pdf,.doc,.docx"/>
                        </div>
                        <div class="resume-text">{{fileName}}</div>
                        <div class="sub-resume-text">File must be less than 5MB.</div>

                    </div>
                    
                    <div v-for="(extraQuestion, index) in jobInformation.jobQuestions.extraQuestion" :key="index" class="question">
                        <div class="text" v-html="extraQuestion.isOptional[0] ? addRedAsterisk(extraQuestion.questionHTML[0]) : extraQuestion.questionHTML[0]"></div>
                        <div v-if="extraQuestion.type === 'free-form'">
                            <textarea @input="updateCount(index)" class="free-form-input" :id="`free-form-${index}`" :style="{ height: '100px' }"></textarea>
                            <div v-if="extraQuestion.maxWord[1]" class="word-count">0/{{ extraQuestion.maxWord[0] }}</div>
                            <div v-if="extraQuestion.minWord[1]">
                                <div class="min-word-count">Minimum word count of {{ extraQuestion.minWord[0] }} not met</div>
                            </div>
                        </div>
                        <div v-else-if="extraQuestion.type === 'single-select'">
                            <div v-for="(option, optIndex) in extraQuestion.options" :key="optIndex" class="input-entry">
                                <label class="text">{{ option }}</label>
                                <input type="radio" @click="updateSingleSelect(index, optIndex)" :checked="responses[index]?.response === option"/>
                            </div>
                        </div>
                        <div v-else-if="extraQuestion.type === 'multi-select'">
                            <div v-for="(option, optIndex) in extraQuestion.options" :key="optIndex" class="input-entry">
                                <label class="text">{{ option }}</label>
                                <input type="checkbox" @click="updateMultiSelect(index, optIndex)" :checked="responses[index]?.response.includes(option)"/>
                            </div>
                        </div>
                    </div>
                    <div class="text" style="margin-bottom:50px">
                        <div>
                            Give a brief self-statement to present yourself for this position with less than 100 characters
                            <div style="display:inline-block;color:red;">*</div>
                            <div style="margin-top:10px"></div>
                            <textarea id="self-statement" @input="capStatementCount" class="free-form-input" :style="{ height: '100px' }"></textarea>
                            <div id="self-statement-word-count" class="word-count">0/{{ 100}}</div>
                        </div>
                    </div>

                    <div class="next-button" @click="tab[0] += 1" v-if="!viewMode">
                        Next
                    </div>
                    <div class="next-button" @click="submitApplication" v-else-if="viewMode && props.userID!=null">
                        Submit
                    </div>
                </div>
            </div>
        </div>
    </div>


    <!-- 
    
    
jobDescription: {
        title: ["SWE"],
        description: ["This is a job description"],
        summary: ["This is a job summary"]
    },
    jobQuestions: {
        resume:[true],
        contacts: ["email", "phone"],
        anonymous: [false],
        extraQuestion: [
            {
                type:"free-form",
                questionText: "What is your favorite color?",
                questionType: "freeform",
                maxWord: null,
                minWord: null,
                required: true
            },
            {
                type:"select",
                questionText: "Select your skills",
                options: ["JavaScript", "Python", "C++"],
                required: false
            }
        ]
    },
    color: {
        backgroundColor: ["white"],
        textColor: ["black"]
    }

    -->
</template> 

<style scoped>
.description{
    background-color: rgba(255, 255, 255, 0.116);
    padding-left: 300px;
    margin-left: -300px;
    width:100%;
    padding-right: 300px;
    padding-top: 400px;
    margin-top: -400px;
}
.bottom-cover{   
    width: 100%;
    background-color: #0000001c;
    display: flex;
    flex-flow: column;
    flex: 0 1 auto;
    height: 100%;
}
.free-form-input{
    width:calc(100%);
    resize: none;
    font-size: 16px;
    padding:10px;
    padding-bottom: 30px;
    border: solid #696969 1px;
    box-sizing: border-box;
    height:15px;
    font-family: Arial, sans-serif;
    z-index: -10;
}
.word-count{
    font-size: 12px;
    color:v-bind(jobInformation.color.textColor[0]);
    filter: invert(.2);
    margin-top: -30px;
    margin-bottom: 20px;
    margin-right: 10px;
    float:right;
    width:fit-content;  
    position: relative;
    z-index: 10;

}
.input, textarea{
    background-color: #00000000;
    box-shadow: inset 0 0 5px #00000070;
}
.min-word-count{
    font-size: 12px;
    color:v-bind(jobInformation.color.textColor[0]);
    filter: invert(.2);
    margin-top: -30px;
    margin-left: 10px;
    position: relative;
    z-index: 10;
    animation: dropIn 0.3s ease-in-out;

}
@keyframes dropIn {
    0% {
        opacity: .7;
        transform: scale(1.05) translateX(10px);;
    }
    100% {
        opacity: 1;
        transform: scale(1) translateX(0px);;
    }
}
.resume-text{
    font-size: 12px;
    color: rgb(0, 0, 0);
    width:100%;
    line-height: 16px;
    margin-bottom: 30px;
    margin-top: -45px;
    opacity: 1;
    text-align: center;
    font-weight: bold;
    overflow-x: auto;
    white-space: nowrap;
    z-index: -1;
  /* Primary method for supporting browsers */
    
}
.sub-resume-text{

    font-size: 16px;
    color: rgb(0, 0, 0);
    width:100%;
    margin-top: 5px;
    opacity: .6;
    
}

.resume-container-styling-accpeted{
    background-image: url("@/assets/green-check.png");
    background-position: center;
    background-repeat: no-repeat;
    background-position: 50% 20px;
    background-size: auto 70px;
    width:100%;
    height:140px;
    box-shadow: inset 0 0 10px #000000b2;
    background-color: #00000000;
    border: dashed #696969 2px;
    box-sizing: border-box;
    border-radius: 5px;
    margin-top:30px;
    display: flex;
    justify-content: center;
    align-items: center;
    padding-bottom: 20px;
}
.resume-container-styling{
    background-image: url("@/assets/founder-space/edit/job-edit/file-icon.png");
    background-position: center;
    background-repeat: no-repeat;
    background-position: 50% 20px;
    background-size: auto 70px;
    width:100%;
    height:140px;
    box-shadow: inset 0 0 10px #000000b2;
    background-color: #00000000;
    border: dashed #696969 2px;
    box-sizing: border-box;
    border-radius: 5px;
    margin-top:30px;
    display: flex;
    justify-content: center;
    align-items: center;
    padding-bottom: 20px;
}
.resume-box{
    width:100%;
    height: 130px;
    opacity: 0;
    margin-top: 20px;
    border: solid #696969 1px;
    box-sizing: border-box;
    border-radius: 5px;
    position: relative;
    z-index: 20;
    background-color: #f80a0ac9;
}
.optional{
    display: inline-block;
    margin-left:10px;
    color: gray;
    font-size: 14px;
}
.input-entry{
    display: inline-block;
    margin-right:20px;
}
.questions{
    max-width:750px;
    margin:auto;
}
.question{
    margin-bottom: 30px;
    width: calc(100% - 60px);
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
    background-color: #f0f0f0;
}
.toolbar{
    background-color: #e0e0e0;
    height:fit-content;
    height:40px;
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
    width:calc(100% );
    resize: none;
    font-size: 16px;
    padding:10px;
    border: solid #696969 1px;
    box-sizing: border-box;
    height:15px;
    font-family: Arial, sans-serif;
    z-index: -10;
}
.text-container{
    text-align: left;
    font-family: Arial, sans-serif;
    font-family: Arial, sans-serif;
    color:v-bind(jobInformation.color.textColor[0]);
    margin-bottom:-260px;
    height: 100%;
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