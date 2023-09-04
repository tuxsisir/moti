<script setup>
import { ref, defineEmits, defineProps, onMounted } from "vue";

const props = defineProps({
  activeUser: {
    type: Object,
    required: false,
    default: {}
  }
})

const emits = defineEmits(['success', 'error'])

const formData = ref({
  username: "",
  name: "",
  age: "",
  source: null,
  target: null,
  relation_type: "",
  new_source: false,
  new_target: false
});

async function formSubmit() {
  let apiUrl = "http://localhost:8000/users/"

  let requestOptions = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(formData.value)
  };

  if (Object.keys(props.activeUser).length > 0) {
    requestOptions['method'] = "PUT"
    apiUrl += `${props.activeUser.id}/`
  }
  fetch(apiUrl, requestOptions)
    .then(async response => {
      const data = await response.json();
      if (!response.ok) {
        const error = data;
        return Promise.reject(error);
      }
      resetFormValues()
      emits('success')
      resetFormValues()
    }).catch((error) => {
      emits('error', error)
    })
}

function resetFormValues() {
  formData.value.username = ""
  formData.value.name = ""
  formData.value.age = ""
}

onMounted(() => {
  if (Object.keys(props.activeUser).length > 0) {
    formData.value.username = props.activeUser.username
    formData.value.name = props.activeUser.name
    formData.value.age = props.activeUser.age
  }
})

</script>
<template>
  <div class="columns is-12 is-vcentered">
    <div class="field column is-3">
      <label class="label">Username</label>
      <div class="control">
        <input v-model="formData.username" class="input" type="text" placeholder="Username">
      </div>
    </div>
    <div class="field column is-3">
      <label class="label">Name</label>
      <div class="control">
        <input v-model="formData.name" class="input" type="text" placeholder="Name">
      </div>
    </div>
    <div class="field column is-3">
      <label class="label">Age</label>
      <div class="control">
        <input v-model="formData.age" class="input" type="number" placeholder="Age">
      </div>
    </div>

    <div class="field column is-3 mt-4">
      <button class="button is-success" @click="formSubmit">Submit</button>
    </div>
  </div>
</template>
