<script setup>
import { defineProps, defineEmits, ref } from "vue";

defineProps({
  users: Object
})

const emits = defineEmits(['success', 'error'])

const formData = ref({
  "source": null,
  "target": null,
  "relation_type": null
})

const relationship = [
  "GRANDPARENT",
  "PARENT",
  "PARTNER",
  "CHILD",
  "FRIEND"
]

async function addRelation() {
  const requestOptions = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(formData.value)
  };
  fetch("http://localhost:8000/relation/", requestOptions)
    .then(async response => {
      const data = await response.json();
      if (!response.ok) {
        const error = data;
        return Promise.reject(error);
      }
      emits('success')
      resetFormValues()
    }).catch((error) => {
      emits('error', error)
    })
}

</script>
<template>
  <div class="columns is-12 is-vcentered">
    <div class="field is-fullwidth column is-3">
      <label class="label">Source</label>
      <div class="control">
        <div class="select is-fullwidth">
          <select v-model="formData.source">
            <option v-for="(user, val, index) in users" :key="`source_` + index" :value="user.id">{{ user.name }}</option>
          </select>
        </div>
      </div>
    </div>
    <div class="field column is-3">
      <label class="label">Target</label>
      <div class="control">
        <div class="select is-fullwidth">
          <select v-model="formData.target">
            <option v-for="(user, val, index) in users" :key="`target_` + index" :value="user.id">{{ user.name }}</option>
          </select>
        </div>
      </div>
    </div>
    <div class="field column is-3">
      <label class="label">Relationship</label>
      <div class="control">
        <div class="select is-fullwidth">
          <select v-model="formData.relation_type">
            <option v-for="(relation, index) in relationship" :key="`relation_` + index" :value="relation">{{ relation }}
            </option>
          </select>
        </div>
      </div>
    </div>
    <div class="field column is-3 mt-4">
      <button class="button is-success" @click="addRelation">Submit</button>
    </div>
  </div>
</template>
