<script setup>
import { useRoute, useRouter } from 'vue-router'
import Header from '@/components/main-page/header.vue';
import jobDescription from '@/components/job-page/description.vue';

const router = useRouter()
const route = useRoute()

</script>
<template>
    <Header />
    <jobDescription />
    
</template>
    