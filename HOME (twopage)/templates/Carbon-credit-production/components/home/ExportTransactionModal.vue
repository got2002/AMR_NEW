<template>
	<div class="fixed z-50 bottom-0 left-0 w-full h-screen bg-black bg-opacity-60 flex items-center justify-center overflow-hidden">
		<div class="mx-auto container bg-white rounded shadow-sm p-4 w-3/12 space-y-4">
			<div class="flex justify-between items-center">
				<p class="text-xl font-bold">{{ $t("home.modal.request_statement_title") }}</p>
				<button @click="$emit('close')" class="bg-white px-3 py-1 border border-gray-300 hover:bg-gray-50 rounded">{{ $t("button.close") }}</button>
			</div>
			<div class="border-b border-gray-300"></div>
			<div class="space-y-4">
				<div>
					<div class="w-full h-10 border-2 border-gray-300 rounded flex items-center">
						<div class="w-4/12 px-2 bg-gray-300 h-full text-sm flex items-center justify-center">{{ $t("home.modal.filter.month") }}</div>
						<DatePicker :placeholder="$t('home.modal.filter.placeholder')" type="month" v-model="date" :formatter="monthFormat" value-type="date" :lang="$i18n.locale" input-class="text-center text-sm px-2 py-1 w-full outline-none"></DatePicker>
					</div>
					<p class="text-xs text-right text-red-500" v-if="!$v.date.required">{{ $t("home.form_validation.date") }}</p>
				</div>

				<div>
					<div class="w-full h-10 border-2 border-gray-300 rounded flex items-center">
						<div class="w-4/12 px-2 bg-gray-300 h-full text-sm flex items-center justify-center">{{ $t("home.modal.filter.language") }}</div>
						<select v-model="language" class="w-full outline-none text-center text-sm">
							<option value="th">{{ $t("thai") }}</option>
							<option value="en">{{ $t("eng") }}</option>
						</select>
					</div>
					<p class="text-xs text-right text-red-500" v-if="!$v.language.required">{{ $t("home.form_validation.lang") }}</p>
				</div>

				<div  v-if="admin">
					<div class="w-full h-10 border-2 border-gray-300 rounded flex items-center">
						<div class="w-4/12 px-2 bg-gray-300 h-full text-sm flex items-center justify-center">{{ $t("home.modal.filter.email") }}</div>

						<input type="email" v-model="email" class="w-full outline-none text-center text-sm" />
					</div>
					<p class="text-xs text-right text-red-500" v-if="!$v.email.requiredAdmin">{{ $t("home.form_validation.email") }}</p>
				</div>

				<button @click="sendRequest" class="w-full py-2 rounded shadow-sm text-white bg-tgo-teal-500 hover:bg-tgo-teal-600 border border-gray-400">{{ $t("button.send_request") }}</button>
			</div>
		</div>
	</div>
</template>

<script>
	import { required } from "vuelidate/lib/validators";
	import thaiformatter from "../../mixins/thaiformatter";
	export default {
		mixins: [thaiformatter],
		props: {
			admin: {
				type: Boolean,
				default: () => false,
			},
		},
		data() {
			return {
				date: new Date(),
				language: this.$i18n.locale,
				email: this.$auth.user?.email,
				item: [],
			};
		},
		validations() {
			return {
				date: {
					required,
				},
				language: {
					required,
				},
				email: {
					requiredAdmin: (value) => {
						if (this.admin) {
							if (value) return true;
							else return false;
						} else return true;
					},
				},
			};
		},
		methods: {
			projectName(data) {
				if (this.$i18n.locale === "th") {
					return data.thai;
				} else {
					return data.english;
				}
			},
			datetime(date) {
				if (this.$i18n.locale === "th") {
					return this.$dayjs(date).locale("th").format("DD MMM BBBB (HH:mm)");
				}
				return this.$dayjs(date).locale("en").format("DD MMM YYYY (HH:mm)");
			},
			sendRequest() {
				const app = this;
				this.$v.$touch();
				if (this.$v.$invalid) {
					app.$swal.fire({
						icon: "warning",
						title: app.$t('home.swal.statement.title.invalid'),
						text: app.$t('home.swal.statement.text.invalid'),
					});
					return;
				}
				let dateInput = this.$dayjs(new Date()).format("YYYY-MM-DD");
				if (this.date) {
					dateInput = this.$dayjs(this.date).format("YYYY-MM-DD");
				}
				let url = `/api/v1/credit/transactionmail?lang=${this.language}&date=${dateInput}`;
				if (this.admin) {
					url = `/api/v1/account/credits/${this.$route.params.id}/request-transaction?email=${this.email}&lang=${this.language}&date=${dateInput}`;
				}
				this.$axios
					.$get(url)
					.then(() => {
						app.$swal.fire({
							icon: "success",
							iconColor:'#059669',
							confirmButtonColor: "#059669",
							title: app.$t('home.swal.statement.title.success'),
							html: `<div class="text-sm">${app.$t('home.swal.statement.text.success')} <p>${app.$t('home.swal.statement.text.check_email',{email:this.email})}</p></div>`,
							
						});
						setTimeout(app.$emit("close"), 3000);
					})
					.catch((err) => {
						console.log(err);
						app.$swal.fire({
							icon: "error",
							title: app.$t('home.swal.statement.title.error'),
							text: app.$t('home.swal.statement.text.error'),
						});
					});
			},
		},
	};
</script>

<style></style>
