<template>
	<div class="w-full h-full">
		<div class="space-y-8">
			<button @click="$router.push(localePath('/showroom'))" class="px-4 py-2 flex items-center gap-2 bg-gray-300 rounded shadow-md text-sm">
				<ShowroomBackIcon />
				{{ $t("button.back") }}
			</button>
			<p class="text-xl font-semibold">{{ $t("cart.page_title") }}</p>
		</div>
		<div class="grid grid-cols-12 gap-4 mt-4">
			<div class="col-span-9" :class="{ 'col-span-12': getCart?.length == 0 }">
				<div class="space-y-4">
					<CartItem v-for="(item, i) in getCart" :key="i" :data="item" @deleteItem="removeCart(i)" @setQuantity="setQuantity($event, i)" />
				</div>
				<div v-if="getCart?.length == 0" class="w-full py-8 text-center bg-gray-100">
					{{ $t("cart_empty") }}
				</div>
			</div>
			<div class="col-span-3" v-if="getCart?.length != 0">
				<div class="bg-white rounded shadow-sm p-4">
					<div class="grid grid-cols-2 gap-4">
						<div class="text-sm font-light">{{ $t("cart.checkout_card.sub_total") }}:</div>
						<div class="text-sm font-light text-right">{{ subTotal?.toLocaleString() }} ฿</div>

						<div class="text-sm font-light">{{ $t("cart.checkout_card.vat") }}:</div>
						<div class="text-sm font-light text-right">{{ vat?.toLocaleString() }} ฿</div>

						<div class="text-sm font-light">{{ $t("cart.checkout_card.total") }}:</div>
						<div class="text-sm font-semibold text-right">{{ total?.toLocaleString() }} ฿</div>
					</div>
					<button @click="$router.push(localePath('/cart/checkout'))" class="w-full py-4 text-center bg-tgo-teal-500 shadow-md rounded my-4 text-white">{{ $t("button.proceed_to_checkout") }}</button>

					<p class="text-gray-600">* {{ $t("cart.checkout_card.msg") }}</p>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
export default {
	name: "MyCart",
	layout: "MainLayout",
	data() {
		return {
			cart: [],
		};
	},
	computed: {
		...mapGetters(["getCart", "isAuthenticated", "getCartErr"]),
		vat() {
			return (this._.sumBy(this.getCart, (item) => item.quantity * item.price) * 7) / 100
		},
		subTotal() {
			return this._.sumBy(this.getCart, (item) => item.quantity * item.price);
		},
		total() {
			return this.subTotal + this.vat
		},
	},

	mounted() {
		if (!this.isAuthenticated) {
			this.$router.push(this.localePath({ name: "auth-signin" }));
		}
	},
	methods: {
		...mapActions({
			removeCart: "removeCart",
			setCart: "setCart",
		}),
		
		

		setQuantity(quantity, i) {
			// console.log(i, "kkk");
			
			this.setCart({
				index: i,
				data: quantity,
			});
			
		},
	},
};
</script>

<style>
</style>