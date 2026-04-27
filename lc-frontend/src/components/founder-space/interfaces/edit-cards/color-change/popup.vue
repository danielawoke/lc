<script setup>
import { ref, nextTick} from 'vue';
import { onMounted } from 'vue';
import MainCardMiniView from '@/components/founder-space/interfaces/edit-cards/color-change/mini-views/alt-main-card-mini-view.vue';

let props = defineProps({
    colorInfo: Object,
    backDropClickColor: Array,
    originCard: Array
}); 

let currentColor = ["R0","0%","100%", "background"];

onMounted (async () => {
    await nextTick();
    colorToPosition(props.colorInfo.backgroundColor[0]);
    document.getElementById("job-background-color").className = "tab";
    document.getElementById("job-card-color").className = "dark-tab";
    document.getElementById("job-text-color").className = "dark-tab";
    document.getElementById("job-location-color").className = "dark-tab";
    document.getElementsByClassName("color-wheel-selector")[0].style.border = "5px solid " + w3color(currentColor[0]+", 0%, 0%").toRgbString();
    document.getElementById("color-wheel").style.backgroundColor = props.colorInfo.backgroundColor[0];
    document.getElementById("hex-input").value = props.colorInfo.backgroundColor[0];
    document.getElementById("color-wheel-container").addEventListener("mousedown", (event) => {
        let selector = document.getElementsByClassName("color-wheel-selector")[0];
        let x = event.offsetX / event.target.offsetWidth;
        let y = event.offsetY / event.target.offsetHeight;
        let circularX = elipseCenteredAltX(x*100,y*100);
        selector.style.left = (circularX) + "%";
        let circularY = elipseCenteredAltY(circularX,y*100);
        selector.style.top = (circularY) + "%";
        let color = positionToColor(circularX,circularY);
        currentColor[0] = color;
        let rgbColor = w3color(currentColor[0]+","+currentColor[1]+", "+currentColor[2]).toRgbString(); 
        document.getElementById("color-wheel").style.backgroundColor = rgbColor;
        document.getElementsByClassName("preview")[0].style.backgroundColor = rgbColor;
        if(currentColor[3] === "background"){
            props.colorInfo.backgroundColor[0] = rgbColor;
        }else if(currentColor[3] === "title"){
            props.colorInfo.titleColor[0] = rgbColor;
        }else if(currentColor[3] === "content"){
            props.colorInfo.contentColor[0] = rgbColor;
        }else if(currentColor[3] === "location"){
            props.colorInfo.locationColor[0] = rgbColor;
        }
        document.getElementsByClassName("color-wheel-selector")[0].style.border = "5px solid " + w3color(currentColor[0]+", 0%, 0%").toRgbString();
        document.getElementById("color-wheel-container").addEventListener("mousemove", colorWheelEventListener);
        document.getElementById("hex-input").value = rgbColor;
    });

    document.getElementById("BW-wheel-container").addEventListener("mouseup", (event) => {
        document.getElementById("color-wheel-container").removeEventListener("mousemove", colorWheelEventListener);
    });

    document.getElementById("BW-wheel-container").addEventListener("mousedown", (event) => {
        if(event.target.className !== "BW-wheel"){
            return;
        }
        let selector = document.getElementById("BW-wheel-selector");
        let x = event.offsetX / event.target.offsetWidth;
        let y = event.offsetY / event.target.offsetHeight;
        let xPack = BWXAdjust(x,y);
        let yPack = BWYAdjust(x,y);
        x = xPack[0];
        y = yPack[0];
        let circularX = BWelipseCenteredAltX(x*100,y*100);
        let circularY = BWelipseCenteredAltY(circularX,y*100);
        positionToBW(circularX,circularY);
        selector.style.left = (circularX) + "%";
        selector.style.top = (circularY) + "%";
        document.getElementById("BW-wheel-selector").style.top = (circularY) + "%";
        document.getElementById("BW-wheel-selector").style.left = (circularX) + "%";
        let color = w3color(currentColor[0] + "," + currentColor[1] + ", " + currentColor[2]).toRgbString();
        document.getElementsByClassName("preview")[0].style.backgroundColor = color;
        document.getElementById("color-wheel").style.backgroundColor = color;
        if(currentColor[3] === "background"){
            props.colorInfo.backgroundColor[0] = color;
        }else if(currentColor[3] === "title"){
            props.colorInfo.titleColor[0] = color;
        }else if(currentColor[3] === "content"){
            props.colorInfo.contentColor[0] = color;
        }else if(currentColor[3] === "location"){
            props.colorInfo.locationColor[0] = color;
        }
        document.getElementById("BW-wheel-container").addEventListener("mousemove", BWWheelEventListener);
        document.getElementById("hex-input").value = color;
    });
    document.getElementById("BW-wheel-container").addEventListener("mouseup", (event) => {
        document.getElementById("BW-wheel-container").removeEventListener("mousemove", BWWheelEventListener);
    });

    document.getElementById("W-wheel-container").addEventListener("mousedown", (event) => {
        if(event.target.className !== "W-wheel"){
            return;
        }
        let selector = document.getElementById("W-wheel-selector");
        let x = event.offsetX / event.target.offsetWidth;
        let y = event.offsetY / event.target.offsetHeight;
        let xPack = BWXAdjust(x,y);
        let yPack = BWYAdjust(x,y);
        x = xPack[0];
        y = yPack[0];
        let circularX = BWelipseCenteredAltX(x*100,y*100);
        let circularY = BWelipseCenteredAltY(circularX,y*100);
        positionToW(circularX,circularY);
        selector.style.left = (circularX) + "%";
        selector.style.top = (circularY) + "%";
        document.getElementById("W-wheel-selector").style.top = (circularY) + "%";
        document.getElementById("W-wheel-selector").style.left = (circularX) + "%";
        let color = w3color(currentColor[0] + "," + currentColor[1] + ", " + currentColor[2]).toRgbString();
        document.getElementById("color-wheel").style.backgroundColor = color;
        document.getElementsByClassName("preview")[0].style.backgroundColor = color;
        if(currentColor[3] === "background"){
            props.colorInfo.backgroundColor[0] = color;
        }else if(currentColor[3] === "title"){
            props.colorInfo.titleColor[0] = color;
        }else if(currentColor[3] === "content"){
            props.colorInfo.contentColor[0] = color;
        }else if(currentColor[3] === "location"){
            props.colorInfo.locationColor[0] = color;
        }
        document.getElementById("hex-input").value = color;
        document.getElementById("W-wheel-container").addEventListener("mousemove", WWheelEventListener);
    });
    document.getElementById("W-wheel-container").addEventListener("mouseup", (event) => {
        document.getElementById("W-wheel-container").removeEventListener("mousemove", WWheelEventListener);
    });

    window.addEventListener("resize", () => {
        const width = document.getElementsByClassName("preview")[0].offsetWidth;
        document.getElementsByClassName("preview-text")[0].style.fontSize = (width * 0.08) + "px";
    });

    document.getElementsByClassName("preview-text")[0].style.fontSize = (document.getElementsByClassName("preview")[0].offsetWidth * 0.08) + "px";

    document.getElementById("hex-input").addEventListener("input", (event) => {
        let color = event.target.value;
        colorToPosition(color);
        document.getElementsByClassName("color-wheel-selector")[0].style.border = "5px solid " + w3color(currentColor[0]+", 0%, 0%").toRgbString();
        let rgbColor = w3color(currentColor[0]+","+currentColor[1]+", "+currentColor[2]).toRgbString();
        document.getElementById("color-wheel").style.backgroundColor = rgbColor;
        document.getElementsByClassName("preview")[0].style.backgroundColor = rgbColor;
        if(currentColor[3] === "background"){
            props.colorInfo.backgroundColor[0] = color;
        }else if(currentColor[3] === "title"){
            props.colorInfo.titleColor[0] = color;
        }else if(currentColor[3] === "content"){
            props.colorInfo.contentColor[0] = color;
        }else if(currentColor[3] === "location"){
            props.colorInfo.locationColor[0] = color;
        }
    });

});

function closePopup() {
    props.backDropClickColor[0] = true;
}

function WWheelEventListener(event){
    let selector = document.getElementsByClassName("W-wheel-selector")[0];
    let x = event.offsetX / event.target.offsetWidth;
    let y = event.offsetY / event.target.offsetHeight;
    let xPack = BWXAdjust(x,y);
    let yPack = BWYAdjust(x,y);
    x = xPack[0];
    y = yPack[0];
    let circularX = BWelipseCenteredAltX(x*100,y*100);
    let circularY = BWelipseCenteredAltY(circularX,y*100);
    positionToW(circularX,circularY);
    selector.style.left = (circularX) + "%";
    selector.style.top = (circularY) + "%";
    document.getElementById("W-wheel-selector").style.top = (circularY) + "%";
    document.getElementById("W-wheel-selector").style.left = (circularX) + "%";
    let color = w3color(currentColor[0] + "," + currentColor[1] + ", " + currentColor[2]).toRgbString();
    document.getElementById("color-wheel").style.backgroundColor = color;
    document.getElementsByClassName("preview")[0].style.backgroundColor = color;
    document.getElementById("hex-input").value = color;
    if(currentColor[3] === "background"){
        props.colorInfo.backgroundColor[0] = color;
    }else if(currentColor[3] === "title"){
        props.colorInfo.titleColor[0] = color;
    }else if(currentColor[3] === "content"){
        props.colorInfo.contentColor[0] = color;
    }else if(currentColor[3] === "location"){
        props.colorInfo.locationColor[0] = color;
    }
}


function BWWheelEventListener(event){
    let selector = document.getElementsByClassName("BW-wheel-selector")[0];
    let x = event.offsetX / event.target.offsetWidth;
    let y = event.offsetY / event.target.offsetHeight;
    let xPack = BWXAdjust(x,y);
    let yPack = BWYAdjust(x,y);
    x = xPack[0];
    y = yPack[0];
    let circularX = BWelipseCenteredAltX(x*100,y*100);
    let circularY = BWelipseCenteredAltY(circularX,y*100);
    positionToBW(circularX,circularY);
    selector.style.left = (circularX) + "%";
    selector.style.top = (circularY) + "%";
    document.getElementById("BW-wheel-selector").style.top = (circularY) + "%";
    document.getElementById("BW-wheel-selector").style.left = (circularX) + "%";
    let color = w3color(currentColor[0] + "," + currentColor[1] + ", " + currentColor[2]).toRgbString();
    document.getElementById("color-wheel").style.backgroundColor = color;
    document.getElementsByClassName("preview")[0].style.backgroundColor = color;
    document.getElementById("hex-input").value = color;
    if(currentColor[3] === "background"){
        props.colorInfo.backgroundColor[0] = color;
    }else if(currentColor[3] === "title"){
        props.colorInfo.titleColor[0] = color;
    }else if(currentColor[3] === "content"){
        props.colorInfo.contentColor[0] = color;
    }else if(currentColor[3] === "location"){
        props.colorInfo.locationColor[0] = color;
    }
}

function positionToW(x,y){
    y = -1*(y - 50);
    x = x - 51;
    let angleRadians = y>0? Math.acos((x*45)/(45*Math.sqrt(x*x + y*y))) : Math.acos(-1*(x*45)/(45*Math.sqrt(x*x + y*y))) + Math.PI;
    angleRadians = rotate(angleRadians, -90);
    let angleDegrees = angleRadians * (180/Math.PI);
    let proportion = angleDegrees / 360;
    let W = "";
    if(proportion < 0.5){
        proportion = proportion/0.5;
        W = Math.round(100-proportion*100)+"%";
    }else{
        proportion = proportion - 0.5;
        proportion = proportion/0.5;
        W = Math.round(proportion*100)+"%";
    }
    if(parseInt(currentColor[1]) + parseInt(currentColor[2]) > 100){
        currentColor[2] = 100 - parseInt(currentColor[1]) + "%";
        setBPosition(currentColor[2]);
    }
    console.log(currentColor);

    currentColor[1] = W;
    return W;
}


function setBPosition(percentage){
    let selector = document.getElementById("BW-wheel-selector");
    let proportion = parseInt(percentage) / 100;
    let angleDegrees = proportion * 180;
    let angleRadians = angleDegrees * (Math.PI/180);
    let x = 0.5 + 0.49 * Math.cos(angleRadians - (Math.PI/2));
    if(parseInt(selector.style.left) < 50){
        x-=0.5;
    }
    let y = 0.5 + 0.49 * Math.sin(-1*(angleRadians - (Math.PI/2)));
    let circularX = BWelipseCenteredAltX(x*100,y*100);
    selector.style.left = (circularX) + "%";
    let circularY = BWelipseCenteredAltY(circularX,y*100);
    selector.style.top = (circularY) + "%";

}

function setWPosition(percentage){
    let selector = document.getElementById("W-wheel-selector");
    let proportion = parseInt(percentage) / 100;
    let angleDegrees = proportion * 180;
    let angleRadians = angleDegrees * (Math.PI/180);
    let x = 0.5 + 0.49 * Math.cos(angleRadians - (Math.PI/2));
    if(parseInt(selector.style.left) < 50){
        x-=0.5;
    }
    let y = 0.5 + 0.49 * Math.sin(-1*(angleRadians - (Math.PI/2)));
    let circularX = BWelipseCenteredAltX(x*100,y*100);
    selector.style.left = (circularX) + "%";
    let circularY = BWelipseCenteredAltY(circularX,y*100);
    selector.style.top = (circularY) + "%";

}

function positionToBW(x,y){
    y = -1*(y - 50);
    x = x - 51;
    let angleRadians = y>0? Math.acos((x*45)/(45*Math.sqrt(x*x + y*y))) : Math.acos(-1*(x*45)/(45*Math.sqrt(x*x + y*y))) + Math.PI;
    angleRadians = rotate(angleRadians, -90);
    let angleDegrees = angleRadians * (180/Math.PI);
    let proportion = angleDegrees / 360;
    let B = "";
    if(proportion < 0.5){
        proportion = proportion/0.5;
        B = Math.round(100-proportion*100)+"%";
    }else{
        proportion = proportion - 0.5;
        proportion = proportion/0.5;
        B = Math.round(proportion*100)+"%";
    }
    currentColor[2] = B;

    if(parseInt(currentColor[1]) + parseInt(currentColor[2]) > 100){
        currentColor[1] = 100 - parseInt(currentColor[2]) + "%";
        setWPosition(currentColor[1]);
    }

    return B;
}

function BWelipseCenteredAltX(x,y){
    return x < 50 ? -1*Math.sqrt(zeroBarrier(2400-((y-50)*(y-50)))) + 50 : Math.sqrt(zeroBarrier(2400-((y-50)*(y-50)))) + 50;   
}
function BWelipseCenteredAltY(x,y){
    return y < 50 ? -1*Math.sqrt(zeroBarrier(2400-((x-50)*(x-50)))) + 50 : Math.sqrt(zeroBarrier(2400-((x-50)*(x-50)))) + 50;   
}

function elipseCenteredAltX(x,y){
    return x < 50 ? -1*Math.sqrt(zeroBarrier(2025-((y-50)*(y-50)))) + 50 : Math.sqrt(zeroBarrier(2025-((y-50)*(y-50)))) + 50;   
}
function elipseCenteredAltY(x,y){
    return y < 50 ? -1*Math.sqrt(zeroBarrier(2025-((x-50)*(x-50)))) + 50 : Math.sqrt(zeroBarrier(2025-((x-50)*(x-50)))) + 50;   
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
    let nColColor = positionToColor(circularX,circularY);
    currentColor[0] = nColColor;
    let color = w3color(currentColor[0]+", "+currentColor[1]+", "+currentColor[2]).toRgbString();
    document.getElementsByClassName("color-wheel-selector")[0].style.border = "5px solid " + w3color(currentColor[0]+", 0%, 0%").toRgbString();
    document.getElementsByClassName("color-wheel")[0].style.backgroundColor = color;
    document.getElementsByClassName("preview")[0].style.backgroundColor = color;
    document.getElementById("hex-input").value = color;
    if(currentColor[3] === "background"){
        props.colorInfo.backgroundColor[0] = color;
    }else if(currentColor[3] === "title"){
        props.colorInfo.titleColor[0] = color;
    }else if(currentColor[3] === "content"){
        props.colorInfo.contentColor[0] = color;
    }else if(currentColor[3] === "location"){
        props.colorInfo.locationColor[0] = color;
    }
}

function setColorPosition(ncolOfColor){
    if(ncolOfColor.indexOf("R") === 0){
        let proportion = parseInt(ncolOfColor.substring(1)) / 100;
        let angleDegrees = proportion * 60;
        let angleRadians = angleDegrees * (Math.PI/180);
        let x = 0.51 + -1*0.45 * Math.cos(angleRadians - (Math.PI/2));
        let y = 0.50 + 0.45 * Math.sin(angleRadians - (Math.PI/2));
        document.getElementsByClassName("color-wheel-selector")[0].style.left = (x*100) + "%";
        document.getElementsByClassName("color-wheel-selector")[0].style.top = (y*100) + "%";
    }else if(ncolOfColor.indexOf("Y") === 0){
        let proportion = parseInt(ncolOfColor.substring(1)) / 100;
        let angleDegrees = (proportion * 60) + 60;
        let angleRadians = angleDegrees * (Math.PI/180);
        let x = 0.51 + -1*0.45 * Math.cos(angleRadians - (Math.PI/2));
        let y = 0.50 + 0.45 * Math.sin(angleRadians - (Math.PI/2));
        document.getElementsByClassName("color-wheel-selector")[0].style.left = (x*100) + "%";
        document.getElementsByClassName("color-wheel-selector")[0].style.top = (y*100) + "%";
    }else if(ncolOfColor.indexOf("G") === 0){
        let proportion = parseInt(ncolOfColor.substring(1)) / 100;
        let angleDegrees = (proportion * 60) + 120;
        let angleRadians = angleDegrees * (Math.PI/180);
        let x = 0.51 + -1*0.45 * Math.cos(angleRadians - (Math.PI/2));
        let y = 0.50 + 0.45 * Math.sin(angleRadians - (Math.PI/2));
        document.getElementsByClassName("color-wheel-selector")[0].style.left = (x*100) + "%";
        document.getElementsByClassName("color-wheel-selector")[0].style.top = (y*100) + "%";
    }else if(ncolOfColor.indexOf("C") === 0){
        let proportion = parseInt(ncolOfColor.substring(1)) / 100;
        let angleDegrees = (proportion * 60) + 180;
        let angleRadians = angleDegrees * (Math.PI/180);
        let x = 0.51 + -1*0.45 * Math.cos(angleRadians - (Math.PI/2));
        let y = 0.50 + 0.45 * Math.sin(angleRadians - (Math.PI/2));
        document.getElementsByClassName("color-wheel-selector")[0].style.left = (x*100) + "%";
        document.getElementsByClassName("color-wheel-selector")[0].style.top = (y*100) + "%";
    }else if(ncolOfColor.indexOf("B") === 0){
        let proportion = parseInt(ncolOfColor.substring(1)) / 100;
        let angleDegrees = (proportion * 60) + 240;
        let angleRadians = angleDegrees * (Math.PI/180);
        let x = 0.51 + -1*0.45 * Math.cos(angleRadians - (Math.PI/2));
        let y = 0.50 + 0.45 * Math.sin(angleRadians - (Math.PI/2));
        document.getElementsByClassName("color-wheel-selector")[0].style.left = (x*100) + "%";
        document.getElementsByClassName("color-wheel-selector")[0].style.top = (y*100) + "%";
    }else if(ncolOfColor.indexOf("M") === 0){
        let proportion = parseInt(ncolOfColor.substring(1)) / 100;
        let angleDegrees = (proportion * 60) + 300;
        let angleRadians = angleDegrees * (Math.PI/180);
        let x = 0.51 + -1*0.45 * Math.cos(angleRadians - (Math.PI/2));
        let y = 0.50 + 0.45 * Math.sin(angleRadians - (Math.PI/2));
        document.getElementsByClassName("color-wheel-selector")[0].style.left = (x*100) + "%";
        document.getElementsByClassName("color-wheel-selector")[0].style.top = (y*100) + "%";
    }
}

function colorToPosition(color){
    const ncolOfColor = w3color(color).toNcolString();
    let colorProperties = ncolOfColor.split(",");
    document.getElementById("BW-wheel-selector").style.left = "0%";
    setBPosition(parseInt(colorProperties[2]));
    document.getElementById("W-wheel-selector").style.left = "100%";
    setWPosition(parseInt(colorProperties[1]));
    setColorPosition(colorProperties[0]);
    currentColor[0] = colorProperties[0];
    currentColor[1] = colorProperties[1];
    currentColor[2] = colorProperties[2];
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
function BWXAdjust(x,y){
    let centerX = 0.5;
    let centerY = 0.5;
    let radiusX = Math.abs(x - centerX);
    let radiusY = Math.abs(y - centerY);
    let radius = Math.sqrt((radiusX*radiusX) + (radiusY*radiusY));
    if(radius > 0){
        let angle = Math.atan2(y - centerY, x - centerX);
        return [centerX + 0.49 * Math.cos(angle), radius];
    }
    return [x,radius];
}

function BWYAdjust(x,y){
    let centerX = 0.5;
    let centerY = 0.5;
    let radiusX = Math.abs(x - centerX);
    let radiusY = Math.abs(y - centerY);
    let radius = Math.sqrt((radiusX*radiusX) + (radiusY*radiusY));
    if(radius > 0){
        let angle = Math.atan2(y - centerY, x - centerX);
        return [centerY + 0.49 * Math.sin(angle), radius];
    }
    return [y,radius];
}


function zeroBarrier(number){
    return number < 0 ? 0 : number;
}

function showHTML() {
    const editor = document.getElementById('editor');
    console.log(editor.innerHTML);
}

function switchTab(event){

    let tab = event.target.id;
    document.getElementById("job-background-color").className = "dark-tab";
    document.getElementById("job-card-color").className = "dark-tab";
    document.getElementById("job-text-color").className = "dark-tab";
    document.getElementById("job-location-color").className = "dark-tab";
    document.getElementById(tab).className = "tab";

    if(event.target.id === "job-background-color"){
        currentColor[3] = "background";
        colorToPosition(props.colorInfo.backgroundColor[0]);
        document.getElementsByClassName("preview")[0].style.backgroundColor = props.colorInfo.backgroundColor[0];
        document.getElementsByClassName("color-wheel-selector")[0].style.border = "5px solid " + w3color(currentColor[0]+", 0%, 0%").toRgbString();
        document.getElementById("color-wheel").style.backgroundColor = props.colorInfo.backgroundColor[0];
        document.getElementById("hex-input").value = props.colorInfo.backgroundColor[0];
    }else if(event.target.id === "job-card-color"){
        currentColor[3] = "title";
        colorToPosition(props.colorInfo.titleColor[0]);
        document.getElementsByClassName("preview")[0].style.backgroundColor = props.colorInfo.titleColor[0];
        document.getElementsByClassName("color-wheel-selector")[0].style.border = "5px solid " + w3color(currentColor[0]+", 0%, 0%").toRgbString();
        document.getElementById("color-wheel").style.backgroundColor = props.colorInfo.titleColor[0];
        document.getElementById("hex-input").value = props.colorInfo.titleColor[0];
    }else if(event.target.id === "job-text-color"){
        currentColor[3] = "content";
        colorToPosition(props.colorInfo.textColor[0]);
        document.getElementsByClassName("preview")[0].style.backgroundColor = props.colorInfo.textColor[0];
        document.getElementsByClassName("color-wheel-selector")[0].style.border = "5px solid " + w3color(currentColor[0]+", 0%, 0%").toRgbString();
        document.getElementById("color-wheel").style.backgroundColor = props.colorInfo.textColor[0];
        document.getElementById("hex-input").value = props.colorInfo.textColor[0];

    }else if(event.target.id === "job-location-color"){
        currentColor[3] = "location";
        colorToPosition(props.colorInfo.locationColor[0]);
        document.getElementsByClassName("preview")[0].style.backgroundColor = props.colorInfo.locationColor[0];
        document.getElementsByClassName("color-wheel-selector")[0].style.border = "5px solid " + w3color(currentColor[0]+", 0%, 0%").toRgbString();
        document.getElementById("color-wheel").style.backgroundColor = props.colorInfo.locationColor[0];
        document.getElementById("hex-input").value = props.colorInfo.locationColor[0];
    }

}   

function save(){
    props.backDropClickColor[0] = true;
}

</script>


<template>
    <div @click.self="closePopup" id="popup-backdrop" class="popup-backdrop">
        <div class="popup" :style="{left:'50%', width:'85%'}">
            <div class="header" style="overflow:auto; height:50px">
                <div class="tab-container" style="width:500px">
                    <div @click="switchTab" id="job-background-color" class="tab">
                        Background
                    </div>
                    <div @click="switchTab" id="job-card-color" class="tab">
                        Header
                    </div>
                    <div @click="switchTab" id="job-text-color" class="tab">
                        Content
                    </div>
                    <div @click="switchTab" id="job-location-color" class="tab">
                        Location
                    </div>
                </div>
            </div>
            <div class="container">
                <div id="BW-wheel-container" draggable="false" class="BW-wheel-container">
                    <img draggable="false" class="BW-wheel" src="@/assets/founder-space/edit/color-pop-up/B-wheel.png" />
                    <div id="BW-wheel-selector" class="BW-wheel-selector"></div>
                    <div class="W-wheel-container" id="W-wheel-container">
                        <img draggable="false" class="W-wheel" src="@/assets/founder-space/edit/color-pop-up/W-wheel.png" />
                        <div class="W-wheel-selector" id="W-wheel-selector"></div>
                        <div id="color-wheel-container" class="color-wheel-container">
                            <img id="color-wheel" class="color-wheel" src="@/assets/founder-space/edit/color-pop-up/color-wheel.png" />
                            <div class="color-wheel-selector"></div>
                            <div class="preview">
                                <div class="preview-container">
                                    <MainCardMiniView v-if="originCard[0] == 'MainCard'" :title="originCard[1].title" :content="originCard[1].content" :location="originCard[1].location" :image="originCard[1].image" :color="colorInfo"/>
                                </div>
                                <div class="preview-text">
                                    Preview
                                </div>
                            </div>
                        </div>
                    </div>
                    <input type="text" id="hex-input" class="hex-input" placeholder="Hex Color Code"/>    
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
.tab {
    display: inline-block;
    font-variant: small-caps;
    padding:5px;
    margin-left: -30px;
    font-size: 17px;
    margin-top: 28px;
    margin-left: 20px;
    margin-right:10px;
    cursor: pointer;
    border-bottom: 2px solid rgba(255, 255, 255, 0.986);
    font-family: fantasy;
    color:rgb(255, 255, 255);
}
.dark-tab {

    display: inline-block;
    font-variant: small-caps;
    padding:5px;
    margin-left: -30px;
    font-size: 17px;
    margin-top: 28px;
    margin-left: 20px;
    margin-right:10px;
    cursor: pointer;
    font-family: fantasy;
    color:rgba(53, 53, 53, 0.432);
    border-bottom: 2px solid rgba(255, 255, 255, 0);
}
.hex-input{
    height: 10%;
    aspect-ratio: 1 / 100;
    min-width: 100%;
    margin-top: 20px;
    border: solid rgb(34, 34, 34) 2px;
    background-color: rgba(0, 0, 0, 0);
    color:rgba(255, 255, 255, 0.658);
    border-radius: 5px;
    text-align: center;
    font-size: 16px;
    margin-left: -5%;
    box-shadow: 0 0 10px rgba(104, 104, 104, 0.575);
    
}

.container{
    height:calc(100% - 140px);
    margin:auto;
    border-radius: 50px;
    margin-top: 40px;
    text-align: center;
    font-family: fantasy;
    color: white;
    font-size: 20px;
    background-color: rgba(255, 255, 255, 0);
    overflow: hidden;
}

.BW-wheel-container{
    height: calc(55%);
    aspect-ratio: 1 / 1;
    border-radius: 50%;
    margin:auto;
    z-index: auto;
    user-select: none;
    position: absolute;
    background-color: rgba(158, 158, 158, 0.082);
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    margin-top: -20px;
}
.preview-container{
    width: 100%;
    height: 100%;
    border-radius: 50%;
    margin: auto;
    position: relative;
    background-color: rgba(255, 255, 255, 0);
    overflow: auto;
    padding-left: 10%;
    margin-left: -10%;
    padding-right: 10%;
}
.preview-text{
    position: absolute;
    bottom: 0;
    width: 100%;
    text-align: center;
    height: 10%;
    font-size: 60%;
    padding-bottom: 6%;
    font-weight: bold;
    color: white;
    background-color: rgba(0, 0, 0, 0.103);
    text-shadow: 0 0 5px black;
    user-select: none;
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
    pointer-events: none;
    z-index: -2;
    background-color: rgba(12, 12, 0, 0);
    overflow: hidden;
}
.W-wheel-selector{
    width: 6%;
    height: auto;
    aspect-ratio: 1 / 1;
    background-color: rgb(0, 0, 0);
    border-radius: 50%;
    border: black solid 2px;
    position: absolute;
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.575);
    pointer-events: none;
    user-select: none;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}
.W-wheel{
    height: calc(100%);
    aspect-ratio: 1 / 1;
    border-radius: 50%;
    margin:auto;
    z-index: auto;
    user-select: none;
    position: absolute;
    border: solid rgba(255, 255, 255, 0) 5px;
    background-color: rgba(109, 109, 109, 0.062);
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}
.W-wheel-container{
    height: calc(80%);
    aspect-ratio: 1 / 1;
    border-radius: 50%;
    margin:auto;
    z-index: auto;
    user-select: none;
    position: absolute;
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.575);
    border: solid rgb(0, 0, 0) 5px;
    background-color: rgba(0, 0, 0, 0.541);
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}
.BW-wheel{
    height: 100%;
    aspect-ratio: 1 / 1;
    width:auto;
    position: relative;
    border-radius: 50%;
    opacity: 1;
    user-select: none;
    z-index: -2;
    border: rgba(255, 255, 255, 0) solid 2.5px;
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.774);
    background-color: rgba(0, 0, 0, 0.76);
}
.BW-wheel-selector{
    width: 6%;
    height: auto;
    aspect-ratio: 1 / 1;
    background-color: rgb(255, 255, 255);
    border-radius: 50%;
    border: black solid 2px;
    position: absolute;
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.575);
    pointer-events: none;
    user-select: none;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
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
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    margin-top:20px;
    margin:auto;
    z-index: auto;
    position: absolute;
    user-select: none;
    border: solid white 5px;
    z-index: 1;
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.575);
    
}
.color-wheel{
    background-color: rgba(17, 135, 238, 0);
    border-radius: 50%;
    height:100%;
    width: auto;
    position: relative;
    z-index: -10;
    pointer-events: none;
    user-select: none;
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