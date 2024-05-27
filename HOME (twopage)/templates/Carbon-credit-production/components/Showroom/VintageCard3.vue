<template>
	<div class="xl:col-span-4 bg-white rounded shadow-md relative">
		<div class="h-40 flex items-center justify-center">
			<div class="relative">
				<p class="text-6xl text-center text-gray-600 font-semibold">500฿</p>
				<p class="text-sm text-center text-gray-500">Per Tonne</p>
			</div>
		</div>
		<div class="px-8 pb-8 space-y-6">
			<div class="flex justify-between items-center">
				<div>
					<p class="text-gray-500 text-sm">Serial number</p>
					<p class="text-base font-semibold text-gray-600">12643618-12644617</p>
				</div>
				<div>
					<p class="text-gray-500 text-sm">Vintage Year</p>
					<p class="text-base font-semibold text-gray-600">2020</p>
				</div>
			</div>
			<div>
				<UITextInput v-model="tonne" type="number" class="text-center" />
				<p class="text-xs text-gray-500">Availability: 20,000 tonne</p>
			</div>

			<div>
				<p class="text-center text-2xl font-bold text-tgo-teal-600">1,000</p>
				<p class="text-center text-gray-400 text-sm">Total Price</p>
			</div>
		</div>
		<!-- <div class="h-28 rounded-t-full blur-sm bg-tgo-teal-300 w-full absolute z-40 bottom-0 left-0"></div>
		<div class="h-28 rounded-t-full bg-tgo-teal-200 w-full absolute z-30 bottom-2 left-0"></div>
		<div class="h-28 rounded-t-full bg-tgo-teal-100 w-full absolute z-20 bottom-4 left-0"></div> -->
		<div class="relative h-32">
			<div class="flex items-center justify-center absolute z-50 bottom-8 left-0 w-full">
				<button @click="addToCart()" class="px-8 py-2 rounded-full bg-white hover:bg-gray-100 shadow-md text-gray-600 font-medium flex items-center justify-center gap-2">
					<ShowroomCartIcon />
					<span>ADD TO CART</span>
				</button>
			</div>
			<ShowroomWave class="w-full h-full absolute z-40 bottom-0 left-0 rounded" color="#66d0e8" />
			<ShowroomWave class="w-full h-full absolute z-30 bottom-2 left-0" color="#99dfef" />
			<ShowroomWave class="w-full h-full absolute z-20 bottom-4 left-0" color="#cceff7" />
		</div>
	</div>
</template>

<script>
// this.$auth.$storage.setLocalStorage(key, val)
// this.$auth.$storage.getLocalStorage(key)
// this.$auth.$storage.removeLocalStorage(key)
export default {
	props:['cart'],
	data(){
		return{
			cartItem:this.cart,
			tonne:1
		}
	},
	methods:{
		addToCart(){
			this.cartItem.push({
				img:'/images/TGO_logo.png',
				project_name:'โครงการโรงไฟฟ้าชีวมวลขนาด 4.9 เมกะวัตต์ ของบริษัท โคลเวอร์ พิษณุโลก จํากัด จังหวัดพิษณุโลก',
				project_owner:'บริษัท โคลเวอร์พิษณุโลก จํากัด',
				serial_number:'12643618-12644617',
				project_id:'149',
				vintage_year:'2020',
				tonne:this.tonne,
				total_price:this.tonne*1000
			})
			this.$auth.$storage.setLocalStorage('cart',this.cartItem)
		}
	}
};
</script>

<style>
/* Rectangle 38 */
</style>