<script setup>
import logo from '@/assets/img/logo.png'
</script>

<template>
  <div class="fixed top-0 left-0 h-screen w-20 flex flex-col items-center space-y-6 py-4 z-20 justify-between border-r">
    <div class="flex flex-col items-center gap-12 mt-3">
      <img :src="logo" class="w-5 h-5" alt="logo" />
      <i class="pi pi-home text-xl"></i>
      <i class="pi pi-plus text-xl"></i>
      <i class="pi pi-bell text-xl"></i>
      <i class="pi pi-inbox text-xl"></i>
    </div>
    <i class="pi pi-cog text-xl"></i>
  </div>
</template>