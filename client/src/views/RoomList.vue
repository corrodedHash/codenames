<script setup lang="ts">
import OfflineRoomList from "../components/OfflineRoomList.vue";
import OnlineRoomList from "../components/OnlineRoomList.vue";
</script>
<template>
  <v-app id="inspire">
    <v-main class="bg-grey-lighten-3">
      <v-container>
        <v-sheet
          min-height="70vh"
          rounded="lg"
          class="align-center d-flex flex-column justify-center"
        >
          <RouterLink to="/create">
            <VBtn :icon="true" color="secondary" size="x-large" class="mb-4">
              <i-mdi-plus style="font-size: 200%" />
            </VBtn>
          </RouterLink>
          <OfflineRoomList />

          <OnlineRoomList />
        </v-sheet>
      </v-container>
    </v-main>
  </v-app>
</template>
<style scoped>
.listBox {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
</style>
