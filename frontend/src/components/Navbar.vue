<script setup>
</script>

<template>
  <div class="fixed top-0 left-0 w-full bg-white z-10 flex">
    <div class="container px-4 py-3 flex items-center">
      <!-- Search Bar -->
      <div class="relative flex-1 ml-20">
        <i class="absolute top-4 left-4 pi pi-search text-gray-400"></i>
        <input type="text" placeholder="Поиск"
          class="w-full px-10 py-3 text bg-gray-100 hover:bg-gray-200 rounded-xl" />
      </div>

      <!-- Profile Image -->
      <div class="flex items-center space-x-3 ml-5">
        <img src="https://via.placeholder.com/40" alt="Profile"
          class="w-9 h-9 rounded-full" />
      </div>
    </div>
  </div>
</template>