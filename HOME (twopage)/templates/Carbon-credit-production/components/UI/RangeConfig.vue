<template>
	<div class="bg-white p-4 rounded shadow-md w-96 border space-y-4">
		<div class="flex items-center gap-2">
			<div class="text-center">
				<UILabel :text="$t('Min')" />
				<UITextInput v-model.number="min" type="number" class="text-center"/>
			</div>
			<span>-</span>
			<div class="text-center">
				<UILabel :text="$t('Max')" />
				<UITextInput v-model.number="max" type="number" class="text-center"/>
			</div>
		</div>
		<!-- <div class="w-full">
			
			<UIRangeSlider/>
		</div> -->

		<div class="grid grid-cols-6 gap-2">
			<div class="col-span-2">
				<button @click="$emit('close')" class="px-4 py-2 bg-gray-300 text-gray-600 shadow-md rounded w-full">close</button>
			</div>
            <div class="col-span-4">
				<button @click="$emit('apply',{min:min,max:max})" class="px-4 py-2 bg-tgo-teal-500 text-white shadow-md rounded w-full">Apply</button>
			</div>
		</div>
	</div>
</template>

<script>
export default {
    props:{
        value:Object

    },
    data(){
        return{
            min:this.value.min,
            max:this.value.max
        }
    },
	methods:{
		updatePrice(dd){
			console.log(dd);
		}
	}
};
</script>

<style>
</style>