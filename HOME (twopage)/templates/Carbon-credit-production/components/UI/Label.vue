<template>
  <label class="text-sm font-thin">{{text}} <span v-if="required" class="text-red-500">*</span></label>
</template>

<script>
export default {
    props:['text','required']
}
</script>

<style>

</style>