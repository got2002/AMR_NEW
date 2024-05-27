<template>
  <div class="w-full flex items-center border-b border-gray-200 text-sm">
    <div v-for="(item,idx) in items" :key="idx" @click="changeTab(idx)" class="text-center px-2 py-1 cursor-pointer " :class="{'border-tgo-teal-500 border-b-2 ':tab === idx}">
        {{ item }}
    </div>
  </div>
</template>

<script>
export default {
    props:{
        items:Array
    },
    data(){
        return{
            tab:0
        }
    },
    methods:{
        changeTab(idx){
            this.tab = idx
            this.$emit('tab',this.tab)
        }
    }
}
</script>

<style>

</style>