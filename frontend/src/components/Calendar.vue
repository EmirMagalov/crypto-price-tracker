<script setup>
import {ref, watch} from 'vue'
import {VueDatePicker} from '@vuepic/vue-datepicker'
import '@vuepic/vue-datepicker/dist/main.css'
import ru from 'date-fns/locale/ru'
import {format} from 'date-fns'

const selectedDate = ref(null)

const props = defineProps(
    {
      dateTs: Number
    }
)

const emit = defineEmits(['update:dateTs'])

watch(selectedDate, (date) => {
  if (!date) return
  const timestamp = Math.floor(date.getTime() / 1000)
  emit('update:dateTs', timestamp)
  console.log('Выбранная дата для API (Unix timestamp):', timestamp)
})
</script>

<template>
  <VueDatePicker
      v-model="selectedDate"
      mode="date"
      auto-apply
      format="dd.MM.yyyy"
      inline
      :locale="ru"
      :time-config="{ enableTimePicker: false }"


  />
</template>

