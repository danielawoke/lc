<script setup>
    import { useRoute, useRouter } from 'vue-router'
    import { onMounted } from 'vue';
    import { ref, nextTick, watch } from 'vue';
    import MainCardView from '@/components/founder-space/interfaces/edit-cards/main-card/main-card-view.vue';
    import MainCardEdit from '@/components/founder-space/interfaces/edit-cards/main-card/main-card-edit.vue';
    import router from '@/router';


    let props = defineProps({
        mainCardData: Object,
        viewMode: Boolean
    });

    let SetToEdit = ref([false]);

    // watch(SetToEdit, async (newValue) => {
    //     if(newValue[0] === true) {
    //         await nextTick();
    //         console.log("SetToEdit changed:", newValue);
    //     }else{
    //         await nextTick();
    //         console.log("SetToEdit changed to view mode:", newValue);
    //     }
    // }, { deep: true });

</script>

<template>
    <MainCardView v-if="!SetToEdit[0]" :SetToEdit="SetToEdit" :mainCardData="props.mainCardData" :viewMode="props.viewMode"/>
    <MainCardEdit v-else :SetToEdit="SetToEdit" :mainCardData="props.mainCardData" />
</template>

<style scoped>

</style>