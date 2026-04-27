<script setup>
import { onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { AccountLocal } from "@/lib/appwrite";
import dayjs from "dayjs";
import axios from "axios";
const apiUrl = import.meta.env.VITE_APP_API_URL

const router = useRouter()
const route = useRoute();

async function handleRedirect() {
  try {
    const user = await AccountLocal.get();
    const createdAt = new Date(user.$createdAt);
    const now = new dayjs();
    console.log(now);
    console.log(createdAt);
    const diffInSeconds = now.diff(createdAt, "second");

    console.log(`User created ${diffInSeconds} seconds ago`);

    if (diffInSeconds < 10) {
      router.push("/account-setup");
    } else {
      try {
        let hasBeenSetup = await axios.get(`${apiUrl}users/search/account_setup/${user.$id}`);
        console.log("HAS BEEN SETUP:", hasBeenSetup.data.account_configured);
        if(!hasBeenSetup.data.account_configured){
          router.push("/account-setup");
        } else {
          const redirectPath = route.query.redirect || "/home";
          console.log("Redirecting to:", redirectPath);
          router.push(redirectPath);
        }
      } catch (err) {
        console.error("Error occurred while checking account setup:", err);
        router.push("/account-setup");
      }
    }
  } catch (error) {
    router.push("/login");
  }
}

onMounted(async () => {
    await handleRedirect();
});

</script>

<template>
    <div>processing request...</div>
</template>