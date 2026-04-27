<script setup>
import { ref, nextTick} from 'vue';
import { onMounted } from 'vue';

let props = defineProps({
    color: Array,
    backDropClickColor: Array
});

onMounted (async () => {
    await nextTick();
    let pos = colorToPosition(props.color[0]);
    document.getElementsByClassName("color-wheel-selector")[0].style.left = (pos.x) + "%";
    document.getElementsByClassName("color-wheel-selector")[0].style.top = (pos.y) + "%";
    document.getElementsByClassName("color-wheel-selector")[0].style.border = "5px solid " + props.color[0];

    document.getElementById("color-wheel-container").addEventListener("mousedown", (event) => {
        let selector = document.getElementsByClassName("color-wheel-selector")[0];
        let x = event.offsetX / event.target.offsetWidth;
        let y = event.offsetY / event.target.offsetHeight;
        let circularX = elipseCenteredAltX(x*100,y*100);
        selector.style.left = (circularX) + "%";
        let circularY = elipseCenteredAltY(circularX,y*100);
        selector.style.top = (circularY) + "%";
        let color = positionToColor(circularX,circularY);
        document.getElementsByClassName("color-wheel-selector")[0].style.border = "5px solid " + color;
        document.getElementById("color-wheel-container").addEventListener("mousemove", colorWheelEventListener);
    });

    document.getElementById("color-wheel-container").addEventListener("mouseup", (event) => {
        document.getElementById("color-wheel-container").removeEventListener("mousemove", colorWheelEventListener);
    });
});

function save() {
    let mainCardImage = document.getElementById("main-card-image");
    mainCardImage.style.backgroundColor = props.color[0];
    closePopup();
}

function closePopup() {
    props.backDropClickColor[0] = true;
}



function colorWheelEventListener(event){
    let selector = document.getElementsByClassName("color-wheel-selector")[0];
    let x = event.offsetX / event.target.offsetWidth;
    let y = event.offsetY / event.target.offsetHeight;
    x = xAdjust(x,y);
    y = yAdjust(x,y);
    let circularX = elipseCenteredAltX(x*100,y*100);
    selector.style.left = (circularX) + "%";
    let circularY = elipseCenteredAltY(circularX,y*100);
    selector.style.top = (circularY) + "%";
    let color = positionToColor(circularX,circularY);
    let BW = ", 0%, 0%";
    let rgbColor = w3color(color+BW).toRgbString();
    document.getElementsByClassName("color-wheel-selector")[0].style.border = "5px solid " + rgbColor;
    document.getElementsByClassName("color-wheel")[0].style.backgroundColor = rgbColor;
    document.getElementsByClassName("preview")[0].style.backgroundColor = rgbColor;
    props.color[0] = rgbColor;
}

function colorToPosition(color){
    const ncolOfColor = w3color(color).toNcolString();
    console.log(ncolOfColor);
    if(ncolOfColor.indexOf("R") === 0){
        let proportion = parseInt(ncolOfColor.substring(1)) / 100;
        let angleDegrees = proportion * 60;
        let angleRadians = angleDegrees * (Math.PI/180);
        let x = 0.51 + -1*0.45 * Math.cos(angleRadians - (Math.PI/2));
        let y = 0.50 + 0.45 * Math.sin(angleRadians - (Math.PI/2));
        return {x: x*100, y: y*100};
    }else if(ncolOfColor.indexOf("Y") === 0){
        let proportion = parseInt(ncolOfColor.substring(1)) / 100;
        let angleDegrees = (proportion * 60) + 60;
        let angleRadians = angleDegrees * (Math.PI/180);
        let x = 0.51 + -1*0.45 * Math.cos(angleRadians - (Math.PI/2));
        let y = 0.50 + 0.45 * Math.sin(angleRadians - (Math.PI/2));
        return {x: x*100, y: y*100};
    }else if(ncolOfColor.indexOf("G") === 0){
        let proportion = parseInt(ncolOfColor.substring(1)) / 100;
        let angleDegrees = (proportion * 60) + 120;
        let angleRadians = angleDegrees * (Math.PI/180);
        let x = 0.51 + -1*0.45 * Math.cos(angleRadians - (Math.PI/2));
        let y = 0.50 + 0.45 * Math.sin(angleRadians - (Math.PI/2));
        return {x: x*100, y: y*100};
    }else if(ncolOfColor.indexOf("C") === 0){
        let proportion = parseInt(ncolOfColor.substring(1)) / 100;
        let angleDegrees = (proportion * 60) + 180;
        let angleRadians = angleDegrees * (Math.PI/180);
        let x = 0.51 + -1*0.45 * Math.cos(angleRadians - (Math.PI/2));
        let y = 0.50 + 0.45 * Math.sin(angleRadians - (Math.PI/2));
        return {x: x*100, y: y*100};
    }else if(ncolOfColor.indexOf("B") === 0){
        let proportion = parseInt(ncolOfColor.substring(1)) / 100;
        let angleDegrees = (proportion * 60) + 240;
        let angleRadians = angleDegrees * (Math.PI/180);
        let x = 0.51 + -1*0.45 * Math.cos(angleRadians - (Math.PI/2));
        let y = 0.50 + 0.45 * Math.sin(angleRadians - (Math.PI/2));
        return {x: x*100, y: y*100};
    }else if(ncolOfColor.indexOf("M") === 0){
        let proportion = parseInt(ncolOfColor.substring(1)) / 100;
        let angleDegrees = (proportion * 60) + 300;
        let angleRadians = angleDegrees * (Math.PI/180);
        let x = 0.51 + -1*0.45 * Math.cos(angleRadians - (Math.PI/2));
        let y = 0.50 + 0.45 * Math.sin(angleRadians - (Math.PI/2));
        return {x: x*100, y: y*100};
    }
}

function positionToColor(x,y){
    y = -1*(y - 50);
    x = x - 51;
    let angleRadians = y>0? Math.acos((x*45)/(45*Math.sqrt(x*x + y*y))) : Math.acos(-1*(x*45)/(45*Math.sqrt(x*x + y*y))) + Math.PI;
    angleRadians = rotate(angleRadians, -90);
    let angleDegrees = angleRadians * (180/Math.PI);
    let proportion = angleDegrees / 360;
    let col = "";
    if(proportion < 1/6){
        proportion = proportion/(1/6);
        col = "R"+Math.round(proportion*100);
    }else if(proportion < 2/6){
        proportion = proportion - 1/6;
        proportion = proportion/(1/6);
        col = "Y"+Math.round(proportion*100);
    }else if(proportion < 3/6){
        proportion = proportion - 2/6;
        proportion = proportion/(1/6);
        col = "G"+Math.round(proportion*100);
    }else if(proportion < 4/6){
        proportion = proportion - 3/6;
        proportion = proportion/(1/6);
        col = "C"+Math.round(proportion*100);
    }else if(proportion < 5/6){
        proportion = proportion - 4/6;
        proportion = proportion/(1/6);
        col = "B"+Math.round(proportion*100);
    }else{
        proportion = proportion - 5/6;
        proportion = proportion/(1/6);
        col = "M"+Math.round(proportion*100);
    }
    return col;
}

function rotate(angleRadians, degree){
    return angleRadians + (degree * (Math.PI/180)) < 0 ? angleRadians + (degree * (Math.PI/180)) + 2*Math.PI : angleRadians + (degree * (Math.PI/180)) > 2*Math.PI ? angleRadians + (degree * (Math.PI/180)) - 2*Math.PI : angleRadians + (degree * (Math.PI/180));
    
}

function xAdjust(x,y){
    let centerX = 0.51;
    let centerY = 0.50;
    let radiusX = Math.abs(x - centerX);
    let radiusY = Math.abs(y - centerY);
    let radius = Math.sqrt((radiusX*radiusX) + (radiusY*radiusY));
    if(radius > 0.05){
        let angle = Math.atan2(y - centerY, x - centerX);
        return centerX + 0.45 * Math.cos(angle);
    }
    return x;
}

function yAdjust(x,y){
    let centerX = 0.51;
    let centerY = 0.50;
    let radiusX = Math.abs(x - centerX);
    let radiusY = Math.abs(y - centerY);
    let radius = Math.sqrt((radiusX*radiusX) + (radiusY*radiusY));
    if(radius > 0.05){
        let angle = Math.atan2(y - centerY, x - centerX);
        return centerY + 0.45 * Math.sin(angle);
    }
    return y;
}

function elipseCenteredAltX(x,y){
    return x < 50 ? -1*Math.sqrt(zeroBarrier(2025-((y-50)*(y-50)))) + 50 : Math.sqrt(zeroBarrier(2025-((y-50)*(y-50)))) + 50;   
}
function elipseCenteredAltY(x,y){
    return y < 50 ? -1*Math.sqrt(zeroBarrier(2025-((x-50)*(x-50)))) + 50 : Math.sqrt(zeroBarrier(2025-((x-50)*(x-50)))) + 50;   
}

function zeroBarrier(number){
    return number < 0 ? 0 : number;
}

</script>


<template>
    <div @click.self="closePopup" id="popup-backdrop" class="popup-backdrop">
        <div class="popup">
            <div class="header"></div>
            <div class="container">
                <div class="BW-wheel-container">
                        <img class="BW-wheel" src="@/assets/founder-space/edit/color-pop-up/BW-wheel.png" />
                        <div class="BW-wheel-selector"></div>
                        <div id="color-wheel-container" class="color-wheel-container">
                            <img id="color-wheel" class="color-wheel" src="@/assets/founder-space/edit/color-pop-up/color-wheel.png" />
                            <div class="color-wheel-selector"></div>
                            <div class="preview"></div>
                        </div>
                </div>
                    
            </div>
            <div class="footer">
            <div class="buttons"> 
                <div @click="save" class="save-button">save</div>
                <div @click="closePopup" id="close-button" class="close-button">close</div>
            </div>
        </div>   
    </div>    
</div> 
</template>

<style scoped>
.BW-wheel-container{
    background-color: rgba(170, 99, 12, 0);
    height: calc(80%);
    aspect-ratio: 1 / 1;
    border-radius: 50%;
    margin:auto;
    z-index: auto;
    user-select: none;
    margin-top: 20px;
    border: solid white 5px;
    background-color: beige;
}
.BW-wheel{
    height: 80%;
    width: auto;
    aspect-ratio: 1 / 1;
    position: absolute;
    top: 50%;
    left: 50%;
    border-radius: 50%;
    transform: translate(-50%, -50%);
    z-index: 5;
    opacity: 1;
    user-select: none;
    z-index: -2;
    border: white solid 2.5px;
    background-color: rgb(0, 0, 0);
}
.BW-wheel-selector{
    width: 10%;
    height: auto;
    aspect-ratio: 1 / 1;
    background-color: rgb(255, 255, 255);
    border-radius: 50%;
    position: absolute;
    transform: translate(-50%, -50%);
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.575);
    pointer-events: none;
    user-select: none;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}
.preview{
    height: 80%;
    border:solid rgb(255, 255, 255) 5px;
    width: auto;
    aspect-ratio: 1 / 1;
    position: absolute;
    top: 50%;
    left: 50%;
    border-radius: 50%;
    transform: translate(-50%, -50%);
    z-index: 5;
    opacity: 1;
    user-select: none;
    z-index: -2;
    background-color: rgba(12, 12, 0, 0);
}
.color-wheel-selector{
    width: 15%;
    height: auto;
    aspect-ratio: 1 / 1;
    border: 5px solid white;
    background-color: rgba(255, 255, 255, 0.5);
    border-radius: 50%;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.575);
    pointer-events: none;
    user-select: none;
}
.color-wheel-container{
    background-color: rgba(170, 99, 12, 0);
    height: calc(70%);
    aspect-ratio: 1 / 1;
    border-radius: 50%;
    margin:auto;
    z-index: auto;
    position: relative;
    user-select: none;
    margin-top: 100px;
    border: solid white 5px;
}
.color-wheel{
    background-color: rgba(17, 135, 238, 0);
    border-radius: 50%;
    height:100%;
    width: auto;
    position: relative;
    z-index: -10;
}
.container{
    height:calc(100% - 150px);
    margin:auto;
    border-radius: 50px;
    margin-top: 40px;
    text-align: center;
    font-family: fantasy;
    color: white;
    font-size: 20px;
    background-color: rgba(255, 255, 255, 0);
}
.buttons{
    float: right;
    width:300px;
    margin-right: 80px;
}
.close-button {
    font-size: 16px;
    padding:30px;
    border-radius: 30px;
    display: inline-block;
    padding: 10px;
    background-color:rgb(48, 48, 48);
    color: white;
    font-family: fantasy;
    letter-spacing: 1.5px;
    box-shadow: 0 0 10px rgba(68, 68, 68, 0.575);
    margin-top: -10px;
    float: right;
    transition: box-shadow 0.3s ease;
}

.close-button:hover{
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.575);
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
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.911);
    position: fixed;
    top: 0;
    left: 0;
    z-index: 10;
    opacity: 1;
    animation: fadeIn 0.3s;
    transition: opacity 0.3s ease-out;
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
    background-image: linear-gradient(45deg, rgb(12, 12, 12), rgb(39, 39, 39));
    color: rgb(0, 0, 0);
    width:  calc( (100% - 180px) * .9);
    height: calc( (100% - 180px) * .7);
    max-width: 800px;
    max-height: 600px;
    border-radius: 90px;
    padding: 20px;
    position: absolute;
    top: 50%;
    left: calc((100vw - 180px) / 2 + 180px);
    transform: translate(-50%, -50%);
    box-shadow: rgba(0, 0, 0, 0.87) 0px 5px 15px 10px;
    overflow:hidden;
}

.header {
    text-align: left;
    background-image: linear-gradient(to top, rgb(22, 22, 22), black);
    box-shadow: rgb(20, 20, 20) 0px 4px 6px -1px, rgb(0, 0, 0) 0px 2px 4px -1px;
    width:100%;
    height:40px;
    padding: 20px;
    margin:-20px;
}
.footer{
    background-color: rgba(0, 0, 0, 0.212);
    box-shadow: rgb(10, 10, 10) 4px 4px 8px 4px;
    width:100%;
    height:40px;
    padding: 20px;
    margin: -20px;
    position: absolute;
    bottom: 0;
    margin-top: -20px;
}


</style>
