<script setup>
import { useRoute, useRouter } from 'vue-router'
import { onMounted } from 'vue';
import TrippyColorWheel from '@/components/founder-space/interfaces/secret-toys/trippy-color-wheel.vue';
import EsotericColorWheel from '@/components/founder-space/interfaces/secret-toys/esoteric-color-wheel.vue';
const router = useRouter();
onMounted(() => {
  
});

</script>

<template>

<div class="cont">
    Suprise! You found this secret.
    <div class="image">
        <img src="https://media1.tenor.com/m/TLf896LW9vkAAAAd/squirtle-eating.gif" />
        <div id="main-card-image" class="main-card-image">
            Wacky physics color wheel!
            <TrippyColorWheel />
            Heres a mistique looking one
            <EsotericColorWheel :color="['#ff0000']" />
        </div>
    </div>

</div>

</template> 

<style scoped>
.main-card-image{
    width: 600px;
    height: auto;
    border-radius: 75px;
    margin:auto;
    margin-top: 20px;
    background-color: #a2ecff3d;
    padding: 50px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
    position: relative;

}
.image{
    text-align: center;
    margin-top: 20px;
    position: relative;
}
.cont{
    height: calc(100vh - 280px);
    position: absolute;
    margin-top: 120px;
    left: 0;
    background-color: rgb(255, 255, 255);
    width: calc(100vw - 180px);
    padding-bottom: 80px;
    margin-left: 180px;
    text-align: center;
    overflow: auto;
    z-index: -12;
    
}
</style>