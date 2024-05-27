<template>
	<div class="w-full h-full">
		<div class="space-y-8">
			<button @click="$router.push(localePath('/cart'))" class="px-4 py-2 flex items-center gap-2 bg-gray-300 rounded shadow-md text-sm">
				<ShowroomBackIcon />
				{{ $t("button.back") }}
			</button>
		</div>
		<div class="grid grid-cols-12 gap-4 mt-4">
			<div class="col-span-9">
				<div class="bg-white p-8 shadow-sm rounded">
					<div class="grid grid-cols-2 gap-4">
						<div class="grid grid-cols-4 gap-4">
							<div class="col-span-4">
								<UITitle class="text-tgo-teal-700 font-semibold text-base">{{$t('cart.payment.personal_detail_label')}}</UITitle>
							</div>

							<div class="col-span-4">
								<UILabel :text="$t('cart.payment.firstname')"></UILabel>
								<UITextInput v-model="form.personal_detail.firstname" />
							</div>
							<div class="col-span-4">
								<UILabel :text="$t('cart.payment.lastname')"></UILabel>
								<UITextInput v-model="form.personal_detail.lastname" />
							</div>
							<div class="col-span-4">
								<UILabel :text="$t('cart.payment.email')"></UILabel>
								<UITextInput type="email" v-model="form.personal_detail.email" />
							</div>
							<div class="col-span-4"></div>
							<div class="col-span-4">
								<UITitle class="text-tgo-teal-700 font-semibold text-base">{{$t('cart.payment.payment_methods_label')}}</UITitle>
							</div>

							<div class="col-span-2">
								<input id="creditcard" type="radio" class="w-5 h-5" hidden :value="0" name="payment" v-model="form.payment.payment_type" />
								<label for="creditcard">
									<div class="w-full rounded border py-4 flex items-center justify-center cursor-pointer flex-col gap-4">
										<svg v-if="form.payment.payment_type != 0" width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
											<circle cx="8" cy="8" r="7.5" stroke="#00B2D9" />
										</svg>
										<svg v-else width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
											<circle cx="8" cy="8" r="7.5" stroke="#00B2D9" />
											<circle cx="8" cy="8" r="5" fill="#00B2D9" />
										</svg>

										<p class="font-light">{{ $t("cart.payment.credit_card") }}</p>
									</div>
								</label>
							</div>
							<div class="col-span-2">
								<input id="DirectPayment" type="radio" class="w-5 h-5" hidden :value="1" name="payment" v-model="form.payment.payment_type" />
								<label for="DirectPayment">
									<div class="w-full rounded border py-4 flex items-center justify-center cursor-pointer flex-col gap-4">
										<svg v-if="form.payment.payment_type != 1" width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
											<circle cx="8" cy="8" r="7.5" stroke="#00B2D9" />
										</svg>
										<svg v-else width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
											<circle cx="8" cy="8" r="7.5" stroke="#00B2D9" />
											<circle cx="8" cy="8" r="5" fill="#00B2D9" />
										</svg>

										<p class="font-light">{{ $t("cart.payment.direct_payment") }}</p>
									</div>
								</label>
							</div>
							<div class="col-span-4">
								<UILabel :text="$t('cart.payment.card_number')"></UILabel>
								<UITextInput />
							</div>
							<div class="col-span-4">
								<UILabel :text="$t('cart.payment.card_holder_name')"></UILabel>
								<UITextInput />
							</div>
							<div class="col-span-2">
								<UILabel :text="$t('cart.payment.expire_date')"></UILabel>
								<UITextInput />
							</div>
							<div class="col-span-2">
								<UILabel :text="$t('cart.payment.cvv_code')"></UILabel>
								<UITextInput />
							</div>
						</div>
						<div class="">
							<UITitle class="text-tgo-teal-700 font-semibold text-base">{{ $t("cart.payment.order_label") }}</UITitle>
							<div class="grid grid-cols-1 divide-y">
								<div class="col-span-1 py-4" v-for="(cart,i) in getCart" :key="i">
									<CartItem2 :data="cart"/>
								</div>
								
							</div>
						</div>
					</div>
				</div>
			</div>
			<div class="col-span-3">
				<div class="bg-white rounded shadow-sm p-4">
					<div class="grid grid-cols-2 gap-4">
						<div class="text-sm font-light">{{ $t("cart.checkout_card.sub_total") }}:</div>
						<div class="text-sm font-light text-right">{{ _.sumBy(getCart, (item) => item.quantity * item.price)?.toLocaleString() }} ฿</div>

						<div class="text-sm font-light">{{ $t("cart.checkout_card.vat") }}:</div>
						<div class="text-sm font-light text-right">{{ (_.sumBy(getCart, (item) => item.quantity * item.price)*7/100)?.toLocaleString() }} ฿</div>

						<div class="text-sm font-light">{{ $t("cart.checkout_card.total") }}:</div>
						<div class="text-sm font-semibold text-right">{{ _.sumBy(getCart, (item) => item.quantity * item.price)?.toLocaleString() }} ฿</div>
					</div>
					<button @click="checkout" class="w-full py-4 text-center bg-tgo-teal-500 shadow-md rounded my-4 text-white">{{$t('button.purchase')}}</button>

					<p class="text-gray-600">* {{$t('cart.checkout_card.msg')}}</p>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import { mapActions,mapGetters } from "vuex";
export default {
	name: "MyCart",
	layout: "MainLayout",
	data() {
		return {
			cart: [],
			form: {
				personal_detail: {
					firstname: "",
					lastname: "",
					email: "",
				},
				payment: {
					payment_type: 0,
					card_number: "",
					card_holdername: "",
					expire_date: "",
					cvv_code: "",
				},
			},
		};
	},
	computed:{
		...mapGetters(['getCart'])
	},
	mounted() {
		this.cart = this.$auth.$storage.getLocalStorage("cart");
	},
	methods: {
		...mapActions({
			clearCart: "clearCart",
		}),
		deleteItem(i) {
			this.cart.splice(i, 1);

			this.$auth.$storage.setLocalStorage("cart", this.cart);
		},
		checkout() {
			const app = this;
			this.$swal.fire({
				title: this.$t("sweetalert.waiting"),
				text: this.$t("loading"),
				allowOutsideClick: false,
				showCloseButton: false,
			});
			this.$swal.showLoading();
			this.$axios
				.$post(`/api/v1/cart/checkout`)
				.then((resp) => {
					app.clearCart();
					app.$swal.close();
					app.$swal.fire({
						icon: "success",
						iconColor: "#059669",
						title: app.$t("sweetalert.checkout.success.title"),
						confirmButtonColor: "#059669",
					}).then(()=>app.$router.push(app.localePath('/cart')));
				})
				.catch((err) => {
					app.$swal.close();
					console.log(err);
				});
		},
	},
};
</script>

<style>
</style>