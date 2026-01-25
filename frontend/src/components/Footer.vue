<script setup>

const onTop = () =>{
  window.scrollTo(0,0);
}

</script>

<template>
  <div class="h-full bg-[#00001b] p-3 text-white">
    <div class="w- border-1 border-white/60 font-bold p-15">
      <div class="flex gap-30 items-center justify-between pb-2 px-50 border-b-1 border-white/40">
        <p class="cursor-pointer">FAQs</p>
        <p class="cursor-pointer">Privacy & Cookies</p>
        <p class="cursor-pointer">Cookie Settings</p>
        <div class="cursor-pointer">
          <span class="text-5xl text-white cursor-pointer font-bold"><span class="text-[#0052ff]">Deri</span>Track</span>
        </div>
      </div>
      <div class="flex gap-3 justify-end mt-10">
        <a target="_blank" href="https://t.me/emirmaqalov">
          <img class="w-7 cursor-pointer" src="/telegram-svgrepo-com.svg" alt=""
        /></a>
        <a target="_blank" href="https://github.com/EmirMagalov"
          ><img class="w-7 cursor-pointer" src="/github-svgrepo-com.svg" alt=""
        /></a>
        <div class="flex gap-1">
          <img class="w-7" src="/whatsapp-svgrepo-com.svg" alt="" />
          <p>+994506661369</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
