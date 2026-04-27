<script setup>
import { ref, onMounted, nextTick } from 'vue';
import { loadGoogleMaps } from "@/lib/google";

const autocompleteInput = ref(null);
let autocomplete = null;
let interval = null;
defineProps({
    location: String,
    color: String
});


console.log(autocompleteInput.value);

onMounted(async () => {
  // Check if the google object is available (it should be if loaded via index.html)
    await loadGoogleMaps();
    if (window.google) {
          autocomplete = new window.google.maps.places.Autocomplete(
              autocompleteInput.value,
              {
                  bounds: new window.google.maps.LatLngBounds(
                    new window.google.maps.LatLng(-33.8902, 151.1759),
                    new window.google.maps.LatLng(-33.8474, 151.2631)
                  ),
                  componentRestrictions: { country: ["us"] }, 
                  fields: ["address_components", "geometry", "place_id", "name"] 
              }
              
      );
      autocomplete.addListener('place_changed', onPlaceChanged);
    }
    interval = setInterval(adjustMargin, 10);
    adjustHeight(autocompleteInput.value);
});

function adjustMargin(){
  let pacContainer = document.querySelector(".pac-container");
  if (pacContainer) {
    pacContainer.style = "width:inherit !important; margin-top: -25px !important;";

    console.log(pacContainer.style);
    clearInterval(interval); 
  }
}

const onPlaceChanged = () => {
  const place = autocomplete.getPlace();
  if (!place.geometry) {
    console.log("Returned place contains no geometry");
    return;
  }
  adjustHeight(autocompleteInput.value);
};

function adjustHeight(element) {
  element.value = element.value.replace(/\n/g, '');
  element.style.height = "1px";
  // let height = Math.max((element.scrollHeight),150);
  let height = ((element.scrollHeight));
  document.getElementsByClassName("loc")[0].style.height = (height)+"px";
  element.style.height = (25+height)+"px";
}



</script>

<template>
  <div class="loc">
    <textarea :style="`color: ${color};`" class="location-text" id="location-text" @keypress='adjustHeight($event.target)' @keyup='adjustHeight($event.target)' @keydown='adjustHeight($event.target)' ref="autocompleteInput" type="search" :value=location />
  </div>
</template>

<style scoped>
.custom-pac-container{
  margin-top: -25px !important;
}
.loc {
    width:calc(100% - 33px);
    display: inline-block;
    align-items: center;
    outline:auto;
    margin-left:13.5px;
    resize: vertical; 


    
}
input {
    font-family: Arial, sans-serif;
    font-size: 20px;
    text-align: left;

    border: none;
    background-color: transparent;
    max-width:calc(100%);
    min-width: 145px;;
    overflow-x: hidden;
    overflow-y: auto;
    overflow-wrap: break-word;
    box-sizing:border-box;

}
.location-text {
    

}
textarea{
    font-family: Arial, sans-serif;
    font-size: 20px;
    text-align: left;
    border: none;
    outline:none;
    background-color: transparent;
    max-width:calc(100%);
    width:calc(100% - 5px);
    vertical-align: top;
    resize: none;
}


</style>