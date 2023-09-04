<script setup>
import { defineProps } from "vue";
defineProps({
  errorResponse: {
    type: Object,
    required: true
  }
})
</script>
<template>
  <div v-if="Object.keys(errorResponse).length > 0" class="notification is-danger m-5">
    <button class="delete" @click="errorResponse = {}"></button>
    <ul>
      <li v-for="(err, val, index) in errorResponse" :key="`err_` + index">
        <strong v-if="val !== 'non_field_errors'" class="is-capitalized">{{ val }}:</strong> {{ err[0] }}</li>
    </ul>
  </div>
</template>
