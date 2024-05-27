<template>
  <td class="text-xs py-2 px-2" :class="{'text-left':align=='left','text-center':align=='center','text-right':align=='right'}">
    <slot>{{text}}</slot>
  </td>
</template>

<script>
export default {
    props:{
        text:{
          default:()=>''
        },
        align:{
            type:String,
            default:()=>'left'
        }
    }
}
</script>

<style>

</style>