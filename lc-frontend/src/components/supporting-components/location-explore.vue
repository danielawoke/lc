<script setup>
import { ref, onMounted, nextTick } from 'vue';
import { loadGoogleMaps } from "@/lib/google";

const autocompleteInput = ref(null);
let margin = ref("0px");
let autocomplete = null;
let interval = null;

defineProps({
    location: String,
    color: String,
    remote: Array
});

onMounted(async () => {
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
});

function adjustMargin(){
  let pacContainer = document.querySelector(".pac-container");
  if (pacContainer) {
    pacContainer.setAttribute("style", "width:fit-content !important;");
  }
}

const onPlaceChanged = () => {
  const place = autocomplete.getPlace();
  if (!place.geometry) {
    console.log("Returned place contains no geometry");
    return;
  }
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
    <input @click="adjustMargin"  ref="autocompleteInput" type="search" id="location-input-val" :value=location />
  </div>
</template>

<style scoped>
.loc {
  display:block;
  width:100%;
}

.location-text {

}
input{
  
  width:100%;
  min-width:250px;
}


</style>