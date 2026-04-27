<script setup>
import { ref } from 'vue';
import { onMounted } from 'vue';

defineProps({
    src: {
        type: String,
        default: null
    }
});


</script>

<template>
    <div style="filter:brightness(70%);">
        <input id="linkInput" type="text" :value="src" placeholder="Enter image URL here...">
        <img class="preview-image" :src="src" style="margin-top:30px;"/>
    </div>
</template>

<style scoped>
input {
    width: 90%;
    padding: 5px;
    height:auto;
    font-size: 16px;
    border: 5px solid #ffffff;
    border-radius: 4px;
    margin-top: 40px;
    cursor: pointer;
    position: relative;
    background-color: transparent;
    color: white;
    z-index: 10;
    
}
.preview-image {
    max-width: 500px;
    max-height: 300px;
    width: auto;
    height: calc(100% / 2 - 60px);
    display: block;
    margin: auto;
    margin-top: calc(100% / 2 - 370px);
    border-radius: 20px;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.856);
    background-color: white;
}
</style>
