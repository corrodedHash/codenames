<script setup lang="ts">
import { VTextField } from "vuetify/components";
import { ref } from "vue";

const props = defineProps<{ text: string }>();
const field = ref(undefined as undefined | VTextField);
function copyText() {
  if (field.value === undefined) return;
  field.value.select();
  navigator.clipboard.writeText(props.text);
}
</script>
<template>
  <v-text-field
    ref="field"
    :value="text"
    @click="copyText"
    @touchstart="copyText"
    readonly
  />
</template>
