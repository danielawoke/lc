<script setup>
import { onMounted, ref } from "vue";
import { AccountLocal } from "@/lib/appwrite";

const user = ref(null);
const loading = ref(true);

onMounted(async () => {
  try {
    user.value = await AccountLocal.get();
  } catch (err) {
    console.log("Not logged in", err);
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <div v-if="loading">Loading...</div>

  <div v-else-if="user">
    <h2>Welcome {{ user }}</h2>
    <p>{{ user.email }}</p>
  </div>

  <div v-else>
    Not logged in, this is likely a result of cookies being disabled on this site. Please allow cookies and try to sign in again
  </div>
</template>