<script setup>
import Calendar from "@/components/Calendar.vue";
import {computed, onMounted, ref, watch} from 'vue'
import axios from "axios";
import {API_URL} from "@/config.js";
import {WS_URL} from "@/config.js";

const activeTicker = ref('BTC')
const priceLatest = ref()
const active = ref(false)
const tickers = ['BTC', 'ETH']
const dateTs = ref()
const BtcUsd = ref([])
const EthUsd = ref([])


onMounted(async () => {
  await getPriceLatest()
  await getInitialPrices()
})

const formatDate = (ts) => {
  if (!ts) return ''
  const date = new Date(ts * 1000)

  const day = String(date.getDate()).padStart(2, '0')
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const year = date.getFullYear()

  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  const seconds = String(date.getSeconds()).padStart(2, '0')

  return `${hours}:${minutes}`
}
const getInitialPrices = async () => {
  try {
    const btc = await axios.get(`${API_URL}prices/limit/`, {
      params: {ticker: 'btc_usd'}
    })
    BtcUsd.value = btc.data

    const eth = await axios.get(`${API_URL}prices/limit/`, {
      params: {ticker: 'eth_usd'}
    })
    EthUsd.value = eth.data
  } catch (err) {
    console.error(err)
  }
}


const otherTickers = computed(() => {
  return tickers.filter(t => t !== activeTicker.value)
})


const filterPrice = async () => {

  const {data} = await axios.get(`${API_URL}prices/filter/`, {
    params: {
      ticker: activeTicker.value.toLowerCase() + '_usd',
      date_ts: dateTs.value

    }

  })
  return data
}

const getPriceLatest = async () => {
  if (dateTs.value) {
    const data = await filterPrice()
    priceLatest.value = data
  } else {
    const {data} = await axios.get(`${API_URL}prices/latest/`, {
      params: {
        ticker: activeTicker.value.toLowerCase() + '_usd',

      }

    })
    priceLatest.value = data
    console.log(priceLatest.value)
  }


  {

  }
}
watch(dateTs, async () => {
  const data = await filterPrice()
  priceLatest.value = data

  {

  }
})

watch(
    [BtcUsd, EthUsd],
    ([newBtc, newEth], [oldBtc, oldEth]) => {
      if (!dateTs.value) {
        if (activeTicker.value == 'BTC') {
          priceLatest.value = newBtc[0]
        } else if (activeTicker.value == 'ETH') {
          priceLatest.value = newEth[0]
        }
      }

      // console.log('BTC:', newBtc[0])
      // console.log('ETH:', newEth[0])
    }
)

onMounted(() => {
  const socket = new WebSocket(`${WS_URL}prices/`)
  socket.onopen = () => console.log("Connected to WebSocket")
  socket.onmessage = (event) => {
    const data = JSON.parse(event.data)

    if (data.ticker === 'btc_usd') {
      BtcUsd.value = [data, ...BtcUsd.value].slice(0, 5) // новые сверху
    } else if (data.ticker === 'eth_usd') {
      EthUsd.value = [data, ...EthUsd.value].slice(0, 5)
    }
  }

})


</script>

<template>

  <div class="bg-linear-to-r from-[#011232]  via-[#011232] to-black min-h-130">
    <div class="pt-30 px-10 flex gap-20 justify-center items-center">
      <div class="flex flex-col">
        <h1 class="text-white font-bold text-3xl">Последняя цена валюты</h1>
        <div class="text-white mt-2  font-bold text-2xl mb-2">
          <p>{{ priceLatest?.price }} USD</p>

        </div>
        <div class="min-h-30">

          <div class=" w-32 text-white font-bold text-xl">
          <div class="bg-[#eecf3c] flex gap-5 items-center justify-center " @click="active = !active;getPriceLatest()">
            <p
                class="cursor-pointer  p-2 text-2xl text-center rounded"

            >
              {{ activeTicker }}
            </p>
            <p v-show="!active">▼</p>
            <p v-show="active">▲</p>
          </div>
            <div
                v-show="active"
                class=" mt-1 bg-[#eecf3c] text-black rounded shadow-lg z-10"
            >
              <p
                  v-for="(ticker, index) in otherTickers"
                  :key="index"
                  @click="activeTicker = ticker; active = false;getPriceLatest()"
                  class="p-2 cursor-pointer text-2xl hover:opacity-40"
              >
                {{ ticker }}
              </p>

            </div>

          </div>

        </div>


      </div>
      <div class="top-30 left-1/2">
        <h1 class="text-white font-bold text-2xl mb-2">Фильтр по дате</h1>
        <Calendar v-model:dateTs="dateTs"/>
      </div>
    </div>
  </div>
  <div class="flex gap-50 mt-10 bg-black/10 text-white p-5 justify-center items-start">
    <!-- Блок BTC -->
    <div class="">
      <div class="flex justify-center items-center bg-[#0052ff]">
        <h1 class="text-center px-2 py-1  text-2xl  mb-3">BTC</h1>
        <img class="w-8 object-contain " src="/bitcoin-svgrepo-com.png" alt="">

      </div>
      <div class="grid grid-cols-2 gap-20 text-black font-bold">

        <p>Цена</p>
        <p>Время</p>
      </div>
      <div v-for="(data, index) in BtcUsd" :key="index"
           class="py-3 grid grid-cols-2 font-bold text-2xl border-b-1 border-black/10 text-black gap-20">


        <p>{{ data.price }} USD</p>


        <p>{{ formatDate(data.timestamp) }}</p>
      </div>
    </div>

    <!-- Блок ETH -->
    <div class="flex flex-col">
      <div class="flex justify-center items-center bg-[#0052ff]">
        <h1 class="text-center px-2 py-1  text-2xl  mb-3">ETH</h1>
        <img class="w-8 object-contain " src="/eth-svgrepo-com.svg" alt="">

      </div>
      <div class="grid grid-cols-2  gap-20 text-black font-bold">

        <p>Цена</p>
        <p>Время</p>
      </div>
      <div v-for="(data, index) in EthUsd" :key="index"
           class="py-3 grid grid-cols-2 font-bold text-2xl border-b-1 border-black/10 text-black gap-20">

        <p>{{ data.price }} USD</p>
        <p>{{ formatDate(data.timestamp) }}</p>
      </div>
    </div>
  </div>


</template>

<style scoped>

</style>
