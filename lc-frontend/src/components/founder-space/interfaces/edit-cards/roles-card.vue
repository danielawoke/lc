<script setup>
import { useRoute, useRouter } from 'vue-router'
import { onMounted } from 'vue';
import { ref, nextTick, watch } from 'vue';
import RolesView from '@/components/founder-space/interfaces/edit-cards/roles-card/roles-view.vue';
import RolesEdit from '@/components/founder-space/interfaces/edit-cards/roles-card/roles-edit.vue';
let props = defineProps({
    jobsCardData: Object,
    viewMode: Boolean,
    projectTitle: String,
    preLoadPayload: Object,
});

let color = ref({backgroundColor: ["white"], jobCardColor: ["black"], textColor: ["white"]});

let SetToEdit = ref([false]);

watch(SetToEdit, async (newValue) => {
    if(newValue[0] === true) {
        await nextTick();
        console.log("SetToEdit changed:", newValue);
    }else{
        await nextTick();
        console.log("SetToEdit changed to view mode:", newValue);
    }
}, { deep: true });

</script>

<template>
    <RolesView v-if="!SetToEdit[0]" :SetToEdit="SetToEdit" :jobsCardData="jobsCardData" :viewMode="props.viewMode" :projectTitle="projectTitle" :preLoadPayload="preLoadPayload"/>
    <RolesEdit v-if="SetToEdit[0]" :SetToEdit="SetToEdit" :jobsCardData="jobsCardData"/>
</template>

<style scoped>

</style>