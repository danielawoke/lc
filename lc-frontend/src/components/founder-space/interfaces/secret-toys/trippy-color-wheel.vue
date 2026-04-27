<script setup>
import { ref, nextTick} from 'vue';
import { onMounted } from 'vue';

let props = defineProps({
    color: Array,
    backDropClickColor: Array
});


function colorWheelEventListener(event){

    let selector = document.getElementsByClassName("color-wheel-selector-1")[0];
    let x = event.offsetX / event.target.offsetWidth;
    let y = event.offsetY / event.target.offsetHeight;
    if(Math.abs(event.movementX) > Math.abs(event.movementY)){
        let circularX = elipseCenteredAltX(x*100,y*100);
        selector.style.left = (circularX) + "%";
        let circularY = elipseCenteredAltY(circularX,y*100);
        selector.style.top = (circularY) + "%";
    }else{
        let circularY = elipseCenteredAltY(x*100,y*100);
        selector.style.top = (circularY) + "%";
        let circularX = elipseCenteredAltX(x*100,circularY);
        selector.style.left = (circularX) + "%";

    }

    
    // let selector = document.getElementsByClassName("color-wheel-selector-1")[0];
    // let x = event.offsetX / event.target.offsetWidth;
    // let y = event.offsetY / event.target.offsetHeight;
    // let circularX = elipseCenteredAltX(x*100,y*100);
    // selector.style.left = (circularX) + "%";
    // let circularY = elipseCenteredAltY(circularX,y*100);
    // selector.style.top = (circularY) + "%";
    
}

function elipseCenteredAltX(x,y){
    return x < 50 ? -1*Math.sqrt(zeroBarrier(2025-((y-50)*(y-50)))) + 51 : Math.sqrt(zeroBarrier(2025-((y-50)*(y-50)))) + 51;   
}
function elipseCenteredAltY(x,y){
    return y < 50 ? -1*Math.sqrt(zeroBarrier(2025-((x-51)*(x-51)))) + 50 : Math.sqrt(zeroBarrier(2025-((x-51)*(x-51)))) + 50;   
}

function equidistantCircleAlgoXBased(x,y,r){
    // I decided against this algorithim since moving up and down also impacts the position some is on the color circle, or at least it should, and this doesnt account that.
    return (y <= 0.5 ? -1*Math.sqrt(zeroBarrier(r*r-((x*100-r))*((x*100-r)))) + r : Math.sqrt(zeroBarrier(r*r-((x*100-r))*((x*100-r)))) + r ) + "%";

}

function equidistantCircleAlgoYBased(x,y,r){
    // I decided against this algorithim since moving up and down also impacts the position some is on the color circle, or at least it should, and this doesnt account that.
    return (x <= 0.5 ? -1*Math.sqrt(zeroBarrier(r*r-((y*100-r))*((y*100-r)))) + r : Math.sqrt(zeroBarrier(r*r-((y*100-r))*((y*100-r)))) + r ) + "%";
}

function zeroBarrier(number){
    return number < 0 ? 0 : number;
}


onMounted (async () => {
    await nextTick();
    
    // Top
    
    // firstSelector.style.left = (50) + "%";
    // firstSelector.style.top = (5)+"%";

    // Bottom
    
    // firstSelector.style.left = (50) + "%";
    // firstSelector.style.top = (95)+"%";

    // Left
    
    // firstSelector.style.left = (4) + "%";
    // firstSelector.style.top = (50)+"%";

    // Right

    // firstSelector.style.left = (96) + "%";
    // firstSelector.style.top = (50)+"%";

    document.getElementById("color-wheel-container-1").addEventListener("mousedown", (event) => {
        let selector = document.getElementsByClassName("color-wheel-selector-1")[0];
        let x = event.offsetX / event.target.offsetWidth;
        let y = event.offsetY / event.target.offsetHeight;
        let circularX = elipseCenteredAltX(x*100,y*100);
        selector.style.left = (circularX) + "%";
        let circularY = elipseCenteredAltY(circularX,y*100);
        selector.style.top = (circularY) + "%";
        document.getElementById("color-wheel-container-1").addEventListener("mousemove", colorWheelEventListener);
    });

    document.getElementById("color-wheel-container-1").addEventListener("mouseup", (event) => {
        document.getElementById("color-wheel-container-1").removeEventListener("mousemove", colorWheelEventListener);
    });
});

function save() {
    let mainCardImage = document.getElementById("main-card-image");
    mainCardImage.style.backgroundColor = props.color[0];
    props.color[0] = "#fffff2";
    closePopup();
}

function closePopup() {
    props.backDropClickColor[0] = true;
}

</script>


<template>
    
    <div class="contained">
        <div id="color-wheel-container-1" class="color-wheel-container-1">
                <img id="color-wheel-1" class="color-wheel-1" src="@/assets/founder-space/edit/color-pop-up/color-wheel.png" />
                <div class="color-wheel-selector-1"></div>
                <!-- <img class="BW-wheel" src="@/assets/founder-space/edit/color-pop-up/BW-wheel.png" /> -->
            </div>
        </div>
</template>

<style scoped>
.color-wheel-selector-1{
    width: 15%;
    height: auto;
    aspect-ratio: 1 / 1;
    border: 3px solid white;
    background-color: rgba(250, 235, 215, 0);
    border-radius: 50%;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.575);
    pointer-events: none;
    user-select: none;
}
.color-wheel-container-1{
    background-color: rgba(170, 99, 12, 0);
    height: calc(80%);
    aspect-ratio: 1 / 1;
    border-radius: 50%;
    margin:auto;
    z-index: auto;
    position: relative;
    user-select: none;
}
.color-wheel-1{
    background-color: rgba(17, 135, 238, 0);
    border-radius: 50%;
    height:100%;
    width: auto;
    position: relative;
    z-index: -10;
    user-select: none;
}
.BW-wheel{
    width: 80%;
    height: auto;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 5;
    opacity: 1;
}
.contained{
    height:calc(100% - 150px);
    margin:auto;
    border-radius: 50px;
    margin-top: 40px;
    margin-bottom: 40px;
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
