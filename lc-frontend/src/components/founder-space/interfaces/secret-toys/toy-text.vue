<script setup>
let props = defineProps({
    jobInformation: Object
});

import defaultJobDescriptionText from '@/components/founder-space/interfaces/edit-cards/roles-card/job-create-edit/creation-tabs/job-description-creation-tab-default-description-text/text.vue';



function showHTML() {
    const editor = document.getElementById('editor');
    console.log(editor.innerHTML);
}
</script>
<template>
    
                    <input class="checkAdd" />

        <!-- free form -->

        <!-- <div class="added-question">
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
        </div> -->


        <!-- check -->

        <div class="add-question-section">

            <div class="drop-down-custom">
                <div class="sumbit-added-contact-button"></div>
            </div>

            <select required  class="drop-down"> 
                <option value="apple">Select the next type of question you'd like to add, then click the plus</option>
                <option value="apple">Free form text</option>
                <option value="banana">Check box</option>
                <option value="cherry">Circle selection</option>
            </select>
        </div>

        <div class="next-button" @click="nextTab">
            Next
        </div>
    </div>
</template> 

<style scoped>
.added-question{
    
    padding:20px;
    width: calc(100% - 60px);
    margin-top: 30px;
    margin-left: -20px;
    border-left:#0000003d solid 3px;
    border-radius: 20px;
}
.add-question-section{
    
    font-size: 12px;
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
    width:40px;
    height: 40px;
    background-color: #00000011;
    color: white;
    cursor: pointer;
    user-select: none;
    position: relative;
    font-size: 16px;
    background-image: url('@/assets/founder-space/edit/job-edit/add-plus.png');
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;
    margin-bottom: -49px;
    z-index: 10;
}
.drop-down{
    width:calc(100% - 200px);
    height:42px;
    font-size: 15px;
    margin-bottom: 28px;
    padding-left: 50px;
    border: solid #00000080 3px;
    border-radius: 10px;
    box-sizing: border-box;
    font-family: fantasy;
    background-color: rgb(255, 255, 255);
}
.drop-down-custom{
    position: relative;
    height:fit-content;
    font-size: 16px;
    width:300px;
    border: solid #00000000 1px;
    font-family: fantasy;
}
.custom-contact-input{
    width:150px;
    font-size: 16px;
    padding:5px;
    margin-top:0px;
    height: 23px;
    border: solid #0000005b 1px;
    box-sizing: border-box;
    font-family: fantasy;
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
    font-family: fantasy;
    margin-bottom: 10px;
}
.question{
    margin-bottom: 30px;
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
    resize: vertical;
    height:80px;

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
    font-family: fantasy;
    word-break: break-all; 
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
    font-family: fantasy;
}
.text-container{
    text-align: left;
    padding: 30px;
    font-family: Arial, sans-serif;
    animation: fadeIn 1s ease-in;
    padding-bottom: 100px;
    font-family: fantasy;
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