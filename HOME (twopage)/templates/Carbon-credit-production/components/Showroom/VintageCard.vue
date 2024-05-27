<template>
	<div class="bg-white rounded shadow-sm p-4 col-span-12">
		<div class="grid grid-cols-12 gap-4">
			<div class="xl:col-span-1 lg:col-span-5 md:col-span-4 col-span-8 space-y-2 text-center">
				<span class="px-2 bg-tgo-yellow-500 shadow rounded text-sm">{{ info.vintageYear }}</span>
			</div>
			<div class="xl:col-span-7 lg:col-span-5 md:col-span-4 col-span-8 space-y-2 flex items-center">
				<div class="w-1/4 text-sm font-thin text-gray-600 space-y-2">
					<p>{{ $t("showroom.vintage_card.block_number") }}:</p>
					<p>{{ $t("showroom.vintage_card.availability") }}:</p>
					<p>{{ $t("showroom.vintage_card.price") }}:</p>
					<p>{{ $t("showroom.vintage_card.update") }}:</p>
				</div>
				<div class="w-1/3 text-sm font-thin space-y-2 text-right">
					<p>{{ info.blockStart }} - {{ info.blockEnd }}</p>
					<p>{{ info.available }} <span class="text-gray-500 text-xs">tCO<sub>2</sub>e</span></p>
					<p>{{ info.price }}<span class="text-gray-500 text-xs"> {{$t('unit.baht')}}/tCO<sub>2</sub>e</span></p>
					<p>{{ dateLocale(info.updatedAt) }}</p>
				</div>
			</div>
			<div class="xl:col-span-4 lg:col-span-3 md:col-span-4 col-span-8 space-y-2">
				<div class="grid grid-cols-12 gap-2">
					<div class="col-span-10 space-y-2">
						<div>
							<UILabel :text="$t('unit.tco2e')" />
							<UINumberInput :min="1" :max="info.available" v-model.number="quantity" class="text-center" />
							<UIErrorMsg v-if="!$v.quantity.max">{{ $t("Not enough") }}</UIErrorMsg>
							<UIErrorMsg v-if="!$v.quantity.min">{{ $t("invalid") }}</UIErrorMsg>
							<UIErrorMsg v-if="!$v.quantity.required">{{ $t("required") }}</UIErrorMsg>
							<UIErrorMsg v-if="getCartErr?.data.data === info.blockId">{{ $t("Not enough") }}</UIErrorMsg>
						</div>
						<div class="flex justify-between items-center">
							<p class="text-sm font-light">{{ $t("showroom.vintage_card.total") }}</p>
							<p class="text-sm font-semibold">{{ sum() }} ฿</p>
						</div>
					</div>
					<div class="col-span-2 flex items-center">
						<button @click="addToCart" class="w-full flex justify-center text-white text-sm py-2 bg-tgo-teal-500 hover:bg-tgo-teal-600 rounded shadow-md">
							<IconCart customClass="w-6 h-6 text-white"/>
						</button>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import { required } from "vuelidate/lib/validators";
export default {
	props: ["info", "projectInfo"],
	data() {
		return {
			quantity: 1,
			cartItem: [],
		};
	},
	computed: {
		...mapGetters(["getCart", "isAuthenticated", "getCartErr"]),
	},
	validations() {
		return {
			quantity: {
				required,
				max: (value) => value <= this.info.available,
				min: (value) => value > 0,
			},
		};
	},
	mounted() {
		this.cartItem = [...this.getCart] ?? [];
	},
	methods: {
		...mapActions({
			addCart: "addCart",
			removeCart: "removeCart",
		}),
		sum() {
			return this.info.price * this.quantity;
		},
		dateLocale(date) {
			if (this.$i18n.locale === "th") {
				return this.$dayjs(date).locale("th").format("DD MMM BBBB");
			}
			return this.$dayjs(date).locale("en").format("DD MMM YYYY");
		},
		async addToCart() {
			if (this.isAuthenticated) {
				// this.info.total = this.sum();
				this.$v.$touch();
				if (this.$v.$invalid) {
					this.$toast.error(this.$t('toast.cart.error'));

					setTimeout(this.$toast.clear, 3000);
					return;
				}
				this.info.quantity = this.quantity;

				this.info.project_picture = this.projectInfo.project_picture;

				await this.addCart(this.info);
				if (this.getCartErr === null) {
					this.$toast.success(this.$t('toast.cart.success'));

					setTimeout(this.$toast.clear, 3000);
				}
			} else {
				// console.log(document.referrer);
				this.$router.push(this.localePath({ name: "auth-signin" }));
			}
		},
	},
};
</script>

<style>
</style>