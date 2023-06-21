<script setup lang="ts">
import OfflineRoomList from "../components/OfflineRoomList.vue";
import OnlineRoomList from "../components/OnlineRoomList.vue";
import { useRouter } from "vue-router";

const router = useRouter();
console.log(
  router.resolve({ name: "shareReceiveOffline", params: { shareinfo: "abc" } })
);
</script>
<template>
  <div class="listBox">
    <RouterLink to="/create">
      <i-mdi-plus-box style="font-size: 200%" />
    </RouterLink>
    <OfflineRoomList />

    <OnlineRoomList />
  </div>
</template>
<style scoped>
.listBox {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
</style>
