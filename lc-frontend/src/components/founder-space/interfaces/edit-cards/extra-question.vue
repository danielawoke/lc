<script setup>
import { useRoute, useRouter } from 'vue-router'
import { onMounted } from 'vue';
import { ref, nextTick, watch } from 'vue';
import ExtraCardView from '@/components/founder-space/interfaces/edit-cards/extra-question-card/extra-question-card-view.vue';
import ExtraCardEdit from '@/components/founder-space/interfaces/edit-cards/extra-question-card/extra-question-card-edit.vue';
import router from '@/router';

let props = defineProps({
  cardInfo: Object,
  SetToEdit: Array,
  extraCards: Array,
  key: Number,
  viewMode: Boolean
});

onMounted(() => {

  console.log(props.cardInfo.id);
});

let SetToEdit = ref([false]);

</script>

<template>
  <ExtraCardEdit v-if="SetToEdit[0]" :cardInfo="props.cardInfo" :SetToEdit="SetToEdit" :extraCards="props.extraCards" :key="props.key"/>
  <ExtraCardView v-if="!(SetToEdit[0])" :cardInfo="props.cardInfo" :SetToEdit="SetToEdit" :extraCards="props.extraCards" :key="props.key" :viewMode="props.viewMode"/>
</template>

<style scoped>

</style>