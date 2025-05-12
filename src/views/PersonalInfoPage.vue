<template>
  <div class="p-8 max-w-xl mx-auto bg-white rounded shadow">
    <h2 class="text-2xl font-bold mb-4">Personal Information</h2>
    <div class="grid gap-4">
      <div>
        <label class="block font-medium">Name</label>
        <input type="text" value="John Doe" class="input" />
      </div>
      <div>
        <label class="block font-medium">Email</label>
        <input type="email" value="john@example.com" class="input" />
      </div>
      <div>
        <label class="block font-medium">Phone</label>
        <input type="text" value="123-456-7890" class="input" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.input {
  @apply w-full px-3 py-2 border rounded;
}
</style>
