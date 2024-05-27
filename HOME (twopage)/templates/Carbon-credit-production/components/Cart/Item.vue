<template>
	<div class="col-span-1 p-4 bg-white rounded shadow-sm">
		<div class="grid grid-cols-12 gap-8">
			<div class="col-span-2 bg-gray-100">
				<img :src="imgUrl(data.project_picture)" class="w-full h-full object-cover rounded" />
			</div>
			<div class="col-span-5 space-y-2">
				<p class="font-semibold break-words">{{projectName(data.project_name)}}</p>
				<div class="flex items-center gap-2">
					<div class="font-light text-sm w-28 text-gray-600 ">{{$t('cart.vintage_card.project_code')}}:</div>
					<a :href="localePath(`/showroom/${data.project_id}/info`)" target="_blank" class="font-medium text-sm text-tgo-teal-500 hover:underline">{{data.project_code}}</a>
				</div>
				<div class="flex items-center gap-2">
					<div class="font-light text-sm w-28 text-gray-600 ">{{$t('cart.vintage_card.project_owner')}}:</div>
					<div class="font-medium text-sm">{{data.project_owner[$i18n.locale]}}</div>
				</div>
				<div class="flex items-center gap-2">
					<div class="font-light text-sm w-28 text-gray-600 ">{{$t('cart.vintage_card.vintage_year')}}:</div>
					<div class="font-medium text-sm">{{data.vintageYear}}</div>
				</div>
				<div class="flex items-center gap-2">
					<div class="font-light text-sm w-28 text-gray-600 ">{{$t('cart.vintage_card.block_number')}}:</div>
					<div class="font-medium text-sm">{{data.blockStart}} - {{data.blockEnd}}</div>
				</div>
			</div>
			<div class="col-span-4 px-4">
                <div>
                    <UILabel text="tCO2e"/>
                    <UINumberInput type="number" :min="1" :max="data.available" :disabled="getCartLoading" class="text-center" v-model.number="quantity" @change="$emit('setQuantity',quantity)"/>
                    <p class="text-gray-500 text-sm mt-2">{{data.price}} {{$t('unit.baht')}}/{{$t('unit.tco2e')}}</p>
                </div>
                <div class="w-full my-4 h-0.5 bg-gray-100"></div>
                <div class="grid grid-cols-2 ">
                    <div class="font-light text-sm text-left">{{$t('cart.vintage_card.total')}}</div>
					<div class="font-semibold text-sm text-right">{{sum()?.toLocaleString()}}</div>
                </div>
            </div>
			<div class="col-span-1 py-8">
				<button @click="$emit('deleteItem')" class="w-8 h-8 bg-red-400 hover:bg-red-500 rounded shadow-md flex items-center justify-center">
					<CartTrashIcon customClass="w-5 h-5 text-white"/>
				</button>
			</div>
		</div>
	</div>
</template>

<script>
import { mapGetters } from "vuex";
export default {
    props:['data'],
	data(){
		return{
			quantity:this.data.quantity
		}
	},
	watch:{
		'data.quantity'(value){
			this.quantity = Math.floor(value)
		},
		quantity(value){
			this.quantity = Math.floor(value)
		}
	},
	computed: {
		...mapGetters(['getCartLoading']),
	},
	methods:{
		imgUrl(url) {
			if (url?.length>0) {
				return process.env.baseUrl + url[0].src;
			} else return "https://images.unsplash.com/photo-1516937941344-00b4e0337589?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=870&q=80";
		},
		projectOwnertext(data) {
			if (this.$i18n.locale === "th") return data.project_owner;
			else return data.project_owner_en;
		},
		projectName(name) {
			if (this.$i18n.locale === "th") return name?.th;
			else return name?.en;
		},
		sum() {
			return this.data.price * this.data.quantity;
		},
		
		
	}
};
</script>

<style>
</style>