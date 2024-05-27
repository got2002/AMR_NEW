<template>
  <p class=" text-red-500 text-xs mt-2" :class="{
    'text-left':align=='left',
    'text-center':align=='center',
    'text-right':align=='right',
    }"><slot></slot></p>
</template>

<script>
export default {
  props:{
    align:{
      type:String,
      default:()=>'left'
    }
  }
}
</script>

<style>

</style>