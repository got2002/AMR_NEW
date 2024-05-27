<template>
	<div class="fixed z-50 top-0 left-0 bg-black bg-opacity-60 w-full h-full flex items-center justify-center overflow-hidden">
		<div data-aos="fade-down" data-aos-anchor-placement="top-center" class="2xl:w-3/12 lg:w-6/12 md:w-8/12 w-10/12 bg-white p-10 rounded shadow-sm">
			<p class="text-2xl font-bold">{{ $t("buffer.modal.title") }}</p>
			<div class="my-2 space-y-2">
				<p class="text-sm text-gray-500">{{ projectName(info.project_name) }}</p>
				<p class="text-sm text-gray-500">{{ $t("buffer.modal.subtitle", { amount: info.amount?.toLocaleString() }) }}</p>
			</div>
			<div id="transfer" class="grid grid-cols-2 gap-4 text-sm">
				<div class="col-span-2">
					<label>{{ $t("buffer.modal.buffer") }} (%)</label>
					<div class="flex items-center gap-2 border border-gray-300 pl-3">
						<input type="range" v-model.number="percentBuffer" min="0" max="100" class="w-8/12" />
						<input type="number" v-on:keyup="checkMaxPercent($event.target.value)" v-model.number="percentBuffer" :min="0" :max="100" class="text-center border-l border-gray-300 py-2 w-4/12 outline-none bg-transparent" />
					</div>
					<p class="text-xs text-red-500" v-if="!$v.percentBuffer.min && isSubmitted">{{ $t("buffer.modal.validation.specification") }}</p>
					<div class="w-full flex items-center justify-between mt-2 text-sm">
						<div class="text-sm text-gray-500">{{ $t(`buffer.modal.issue`) }} (tCO<sub>2</sub>eq)</div>
						<div class="font-medium text-green-500">{{ Math.floor(info.amount * (percentBuffer / 100)) }}</div>
					</div>
					<div class="w-full flex items-center justify-between text-sm">
						<div class="text-sm text-gray-500">{{ $t(`buffer.modal.total`) }} (tCO<sub>2</sub>eq)</div>
						<div class="font-medium text-blue-500">{{ info.amount - Math.floor(info.amount * (percentBuffer / 100)) }}</div>
					</div>
					<!-- <input type="number" v-model="form.remark" class="h-16 p-2 w-full border border-gray-300 outline-none" /> -->
				</div>
				<div class="col-span-2">
					<label>{{ $t("buffer.modal.remark") }}</label>
					<textarea :placeholder="`${$t('credit.modal.placeholder_remark')}`" v-model="remark" class="h-16 p-2 w-full border border-gray-300 outline-none" />
				</div>
				<div class="col-span-2 flex items-center gap-4">
					<button @click="$emit('close')" class="w-4/12 py-2 text-sm bg-gray-50 hover:bg-gray-100 border border-gray-400">{{ $t("button.cancel") }}</button>
					<button @click="submitForm()" class="w-8/12 py-2 text-sm bg-blue-400 hover:bg-blue-500 border border-blue-500 text-white">{{ $t("button.confirm") }}</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import { required, min, requiredIf, email } from "vuelidate/lib/validators";
import AOS from "aos";
import "aos/dist/aos.css";
import dropdowns from "../../mixins/dropdowns";

export default {
	name: "TransactionModal",
	props: ["info"],
	mixins: [dropdowns],
	validations() {
		return {
			percentBuffer: { min: (value) => value > 0 },
		};
	},
	data() {
		return {
			percentBuffer: 0,
			remark: "",
			isSubmitted: false,
		};
	},
	mounted() {
		AOS.init();
	},
	methods: {
		checkMaxPercent(value) {
			if (value > 100) {
				this.percentBuffer = 100;
			} else if (value < 0) {
				this.percentBuffer = 0;
			} else {
				this.percentBuffer = value;
			}
		},

		projectName(data) {
			if (this.$i18n.locale === "th") {
				return data?.th;
			} else {
				return data?.en;
			}
		},
		submitForm() {
			// console.log(this.form);
			const app = this;
			this.isSubmitted = true;
			this.$v.$touch();

			if (this.$v.$invalid) {
				// console.log(this.$v);
				this.$swal.fire({
					icon: "error",
					title: this.$t("sweetalert.transferModal.title.invalid"),
					text: this.$t("sweetalert.transferModal.text.invalid"),
				});
				return;
			}
			app.$swal
				.fire({
					icon: "info",
					iconColor: "#60a5fa",
					iconHtml: `
								<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-10 h-10">
									<path stroke-linecap="round" stroke-linejoin="round" d="M10.125 2.25h-4.5c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125v-9M10.125 2.25h.375a9 9 0 019 9v.375M10.125 2.25A3.375 3.375 0 0113.5 5.625v1.5c0 .621.504 1.125 1.125 1.125h1.5a3.375 3.375 0 013.375 3.375M9 15l2.25 2.25L15 12" />
								</svg>
								`,
					title: this.$t("sweetalert.buffer.confirm.title"),
					text: this.$t("sweetalert.buffer.confirm.sub_title"),
					showCancelButton: true,

					confirmButtonColor: "#60a5fa",
					confirmButtonText: `${app.$t("button.confirm")}`,
					cancelButtonText: `${app.$t("button.cancel")}`,
					reverseButtons: true,
				})
				.then((result) => {
					if (result.isConfirmed) {
						app.$swal.fire({
							title: this.$t("sweetalert.waiting"),
							text: this.$t("saving"),
							allowOutsideClick: false,
							showCloseButton: false,
						});
						app.$swal.showLoading();
						app.$axios
							.$post(`/api/v1/buffercarbons/issues/${app.info._id}`, {
								amount: Math.floor(app.info.amount * (app.percentBuffer / 100)),
								remark: app.remark,
							})
							.then((resp) => {
								// console.log(resp);
								app.$swal.close();

								app.$swal
									.fire({
										icon: "success",
										iconColor: "#059669",
										confirmButtonColor: "#059669",
										title: app.$t("sweetalert.buffer.success.title"),

										timer: 2000,
										timerProgressBar: true,
									})
									.then(() => {
										app.$emit("submit");
									});

								// app.form = resp;
							})
							.catch((err) => {
								app.$swal.close();
								app.$swal.fire({
									icon: "error",
									title: app.$t("sweetalert.buffer.fail.title"),
									text: app.$t("sweetalert.buffer.fail.sub_title"),
								});

								console.log(err);
							});
					}
				});
		},
	},
};
</script>

<style>

</style>
