<script setup>
import { useRoute, useRouter } from 'vue-router';
import Header from '@/components/header.vue';
import ToolBar from '@/components/founder-space/tool-bar.vue';
import SecreteInterface from '@/components/founder-space/interfaces/secret-interface.vue';

const router = useRouter()
const route = useRoute()

</script>
<template>
  <Header />
  <ToolBar />
  <SecreteInterface />
  <footer>
    LaunchPad 2026
  </footer>
</template>
<style scoped>
footer{
    font-family: fantasy;
    font-size: 13px;
    position: absolute;
    bottom: 0;
    left: 0;
    width: calc(100vw - 40px);
    height: 20px;
    color: rgb(232, 232, 232);
    padding: 20px;
    padding-bottom:20px;
    padding-top:20px;
    background-color: rgb(0, 0, 0);
    font-size: 10px;
}
</style>
    