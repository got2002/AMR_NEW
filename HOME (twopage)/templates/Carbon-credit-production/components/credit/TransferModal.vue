<template>
	<div class="fixed z-50 top-0 left-0 bg-black bg-opacity-60 w-full h-full flex items-center justify-center overflow-hidden">
		<div data-aos="fade-down" data-aos-anchor-placement="top-center" class="2xl:w-4/12 lg:w-6/12 md:w-9/12 w-10/12 bg-white p-10 rounded shadow-sm">
			<p class="text-2xl font-bold">{{ $t("credit.modal.title") }}</p>
			<div class="my-4">
				<p class="text-sm">{{ projectName(info.project_name) }}</p>
				<p class="text-sm">{{ $t("credit.modal.subtitle", { amount: info.total_blocks?.toLocaleString() }) }}</p>
			</div>
			<div id="transfer" class="grid grid-cols-2 gap-4 text-sm">
				<div class="col-span-2">
					<UILabel :text="$t('credit.modal.transaction_type')" :required="true" />

					<!-- <v-select @input="getAccountReceiverDropdowns" :options="dropdowns.transactions" :reduce="(text) => text.value" :label="$i18n.locale" v-model="form.transaction_type"> </v-select> -->
					<div class="border border-gray-300">
						<UIDropdownSearch v-model="form.transaction_type" @input="getAccountReceiverDropdowns" :searchable="false" :options="dropdowns.transactions" valueAttr="value" :textAttr="$i18n.locale" />
					</div>
					<p class="text-xs text-red-500" v-if="!$v.form.transaction_type.required && isSubmitted">{{ $t("credit.modal.validation.transaction_type") }}</p>
				</div>

				<div v-if="form.transaction_type === 1" class="col-span-2 border-l-4 border-tgo-teal-500 pl-4">
					<UILabel :text="$t('credit.modal.add_reason')" :required="true" />
					<div class="border border-gray-300">
						<UIDropdownSearch v-model="form.cancellationReasonId" :options="dropdowns.cancellationReasons" valueAttr="reason_id" :textAttr="$i18n.locale" />
					</div>
					<!-- <v-select v-model="form.cancellationReasonId" :options="dropdowns.cancellationReasons" :reduce="(text) => text.reason_id" :label="$i18n.locale"> </v-select> -->
					<div v-if="[1, 2, 3, 4, 5, 6].includes(form.cancellationReasonId)" class="mt-2">
						<div class="p-2 border border-gray-300 rounded space-y-2">
							<div class="flex items-center gap-4">
								<label for="in-roll" class="flex items-center gap-1">
									<input v-model="onbehalofOption" :value="1" type="radio" name="onbehalfof" id="in-roll" />
									<span class="text-sm">{{ $t("credit.modal.registered") }}</span>
								</label>
								<label for="out-roll" class="flex items-center gap-1">
									<input v-model="onbehalofOption" :value="2" type="radio" name="onbehalfof" id="out-roll" />
									<span class="text-sm">{{ $t("credit.modal.non_registered") }}</span>
								</label>
							</div>
							<div v-if="onbehalofOption === 2" class="space-y-2">
								<div>
									<UILabel :text="$t('credit.modal.on_behalf_of')" :required="true" />
									<UITextInput v-model="form.onBehalfOfName" />
									<UIErrorMsg v-if="!$v.form.onBehalfOfName.required && isSubmitted">{{ $t("credit.modal.validation.required") }}</UIErrorMsg>
								</div>
								<div>
									<UILabel :text="$t('credit.modal.email')" :required="true" />
									<UITextInput v-model="form.onBehalfOfEmail" type="email" />
									<UIErrorMsg v-if="!$v.form.onBehalfOfEmail.required && isSubmitted">{{ $t("credit.modal.validation.required") }}</UIErrorMsg>
									<UIErrorMsg v-if="!$v.form.onBehalfOfEmail.email && isSubmitted">{{ $t("credit.modal.validation.invalid_email") }}</UIErrorMsg>
								</div>
							</div>

							<div v-if="onbehalofOption === 1">
								<UILabel :text="$t('credit.modal.on_behalf_of')" :required="true" />
								<div class="border border-gray-300">
									<UIDropdownSearch v-model="form.byAccountNumber" :options="dropdowns.usersOnbehalfOf" valueAttr="value" textAttr="accountName" />
								</div>
								<UIErrorMsg v-if="!$v.form.byAccountNumber.required && isSubmitted">{{ $t("credit.modal.validation.required") }}</UIErrorMsg>
							</div>
						</div>
					</div>
					<div v-if="form.cancellationReasonId === 7" class="space-y-2 mt-2">
						<div>
							<UILabel :text="$t('credit.modal.specify_further')" :required="true" />
							<UITextInput v-model="form.cancellationReasonOther" />
							<UIErrorMsg v-if="!$v.form.cancellationReasonOther.required && isSubmitted">{{ $t("credit.modal.validation.required") }}</UIErrorMsg>
						</div>
						<div>
							<UILabel :text="$t('credit.modal.on_behalf_of')" :required="false" />
							<div class="p-2 border border-gray-300 rounded space-y-2">
								<div class="flex items-center gap-4">
									<label for="in-roll" class="flex items-center gap-1">
										<input v-model="onbehalofOption" :value="1" type="radio" name="onbehalfof" id="in-roll" />
										<span class="text-sm">{{ $t("credit.modal.registered") }}</span>
									</label>
									<label for="out-roll" class="flex items-center gap-1">
										<input v-model="onbehalofOption" :value="2" type="radio" name="onbehalfof" id="out-roll" />
										<span class="text-sm">{{ $t("credit.modal.non_registered") }}</span>
									</label>
								</div>
								<div v-if="onbehalofOption === 2" class="space-y-2">
									<div>
										<UITextInput v-model="form.onBehalfOfName" />
										<UIErrorMsg v-if="!$v.form.onBehalfOfName.required && isSubmitted">{{ $t("credit.modal.validation.required") }}</UIErrorMsg>
									</div>
									<div>
										<UILabel :text="$t('credit.modal.email')" :required="true" />
										<UITextInput v-model="form.onBehalfOfEmail" type="email" />
										<UIErrorMsg v-if="!$v.form.onBehalfOfEmail.required && isSubmitted">{{ $t("credit.modal.validation.required") }}</UIErrorMsg>
										<UIErrorMsg v-if="!$v.form.onBehalfOfEmail.email && isSubmitted">{{ $t("credit.modal.validation.invalid_email") }}</UIErrorMsg>
									</div>
								</div>

								<div v-if="onbehalofOption === 1" class="border border-gray-300">
									<UIDropdownSearch v-model="form.byAccountNumber" :options="dropdowns.usersOnbehalfOf" valueAttr="value" textAttr="accountName" />
								</div>
								<UIErrorMsg v-if="!$v.form.byAccountNumber.required && isSubmitted">{{ $t("credit.modal.validation.required") }}</UIErrorMsg>
							</div>
						</div>
					</div>
					<UIErrorMsg v-if="!$v.form.cancellationReasonId.required && isSubmitted">{{ $t("credit.modal.validation.required") }}</UIErrorMsg>
				</div>

				<div v-if="form.transaction_type === 3" class="col-span-2 border-l-4 border-tgo-teal-500 pl-4">
					<UILabel class="text-sm font-bold" :text="$t('credit.modal.specification')" :required="true" />
					<CreditRetirePurpose :form="form">
						<template v-slot:onbehalfof
							><UIErrorMsg v-if="!$v.form.retirementOnBehalfOf.required && isSubmitted">{{ $t("credit.modal.validation.required") }}</UIErrorMsg></template
						>
						<template v-slot:otherpurpose
							><UIErrorMsg v-if="!$v.form.retirementOtherPurpose.required && isSubmitted">{{ $t("credit.modal.validation.required") }}</UIErrorMsg></template
						>
					</CreditRetirePurpose>
					<UIErrorMsg v-if="!$v.form.retirementPurposeOption.required && isSubmitted">{{ $t("credit.modal.validation.required") }}</UIErrorMsg>
				</div>

				<div v-if="form.transaction_type === 5" class="col-span-2 border-l-4 border-tgo-teal-500 pl-4">
					<UILabel :text="$t('credit.modal.add_reason')" :required="true" />
					<div class="border border-gray-300">
						<UIDropdownSearch v-model="form.cancellationReasonId" :options="dropdowns.ITMOsCancellationReasons" valueAttr="reason_id" :textAttr="$i18n.locale" />
					</div>
					<!-- <v-select v-model="form.cancellationReasonId" :options="dropdowns.cancellationReasons" :reduce="(text) => text.reason_id" :label="$i18n.locale"> </v-select> -->
					<div v-if="[1].includes(form.cancellationReasonId)" class="mt-2">
						<div class="p-2 border border-gray-300 rounded space-y-2">
							<div class="flex items-center gap-4">
								<label for="in-roll" class="flex items-center gap-1">
									<input v-model="onbehalofOption" :value="1" type="radio" name="onbehalfof" id="in-roll" />
									<span class="text-sm">{{ $t("credit.modal.registered") }}</span>
								</label>
								<label for="out-roll" class="flex items-center gap-1">
									<input v-model="onbehalofOption" :value="2" type="radio" name="onbehalfof" id="out-roll" />
									<span class="text-sm">{{ $t("credit.modal.non_registered") }}</span>
								</label>
							</div>
							<div v-if="onbehalofOption === 2" class="space-y-2">
								<div>
									<UILabel :text="$t('credit.modal.on_behalf_of')" :required="true" />
									<UITextInput v-model="form.onBehalfOfName" />
									<UIErrorMsg v-if="!$v.form.onBehalfOfName.required && isSubmitted">{{ $t("credit.modal.validation.required") }}</UIErrorMsg>
								</div>
								<div>
									<UILabel :text="$t('credit.modal.email')" :required="true" />
									<UITextInput v-model="form.onBehalfOfEmail" type="email" />
									<UIErrorMsg v-if="!$v.form.onBehalfOfEmail.required && isSubmitted">{{ $t("credit.modal.validation.required") }}</UIErrorMsg>
									<UIErrorMsg v-if="!$v.form.onBehalfOfEmail.email && isSubmitted">{{ $t("credit.modal.validation.invalid_email") }}</UIErrorMsg>
								</div>
							</div>

							<div v-if="onbehalofOption === 1">
								<UILabel :text="$t('credit.modal.on_behalf_of')" :required="true" />
								<div class="border border-gray-300">
									<UIDropdownSearch v-model="form.byAccountNumber" :options="dropdowns.usersOnbehalfOf" valueAttr="value" textAttr="accountName" />
								</div>
								<UIErrorMsg v-if="!$v.form.byAccountNumber.required && isSubmitted">{{ $t("credit.modal.validation.required") }}</UIErrorMsg>
							</div>
						</div>
					</div>
					<UIErrorMsg v-if="!$v.form.cancellationReasonId.required && isSubmitted">{{ $t("credit.modal.validation.required") }}</UIErrorMsg>
				</div>

				<div class="col-span-2">
					<label>{{ $t("credit.modal.receiver_account") }} <span class="text-red-500 text-sm">*</span></label>
					<div class="border border-gray-300">
						<UIDropdownSearch v-model="form.receiver_account" :disabled="form.transaction_type === ''" :options="dropdowns.accounts" valueAttr="value" textAttr="accountName" />
					</div>
					<!-- <v-select :disabled="form.transaction_type === ''" :options="dropdowns.accounts" :reduce="(text) => text.value" label="accountName" v-model="form.receiver_account" /> -->
					<p class="text-xs text-red-500" v-if="!$v.form.receiver_account.required && isSubmitted">{{ $t("credit.modal.validation.receiver_account") }}</p>
				</div>

				<div class="col-span-2">
					<label>{{ $t("credit.modal.remark") }}</label>
					<textarea :placeholder="`${$t('credit.modal.placeholder_remark')}`" v-model="form.remark" class="h-16 p-2 w-full border border-gray-300 outline-none" />
				</div>
				<div class="col-span-2">
					<!-- <input type="range" min="1" max="100" value="50" class="slider" id="myRange"> -->
					<div class="w-full grid" :class="{ 'grid-cols-2': form.transaction_type !== 4, 'grid-cols-3': form.transaction_type === 4 }">
						<div class="col-span-1">
							<label>{{ $t("credit.modal.amount") }} (tCO<sub>2</sub>e)</label>
							<input v-model.number="form.credit_amount" type="number" class="px-3 py-2 bg-gray-50 border w-3/4 h-full text-center text-3xl outline-none" :class="{ 'border-red-500': !$v.form.credit_amount.limit }" />
							<p class="text-xs text-red-500" v-if="!$v.form.credit_amount.required && isSubmitted">{{ $t("credit.modal.validation.invalid_credit") }}</p>
							<p class="text-xs text-red-500" v-if="!$v.form.credit_amount.limit && isSubmitted">{{ $t("credit.modal.validation.invalid_credit") }}</p>
							<p class="text-xs text-red-500" v-if="!$v.form.credit_amount.isNumber">{{ $t("credit.modal.validation.invalid_credit") }}</p>
						</div>

						<div class="col-span-1" v-if="form.transaction_type === 4">
							<label>{{ $t("credit.modal.price") }} {{ $t("unit.baht") }}/tCO<sub>2</sub>e</label>
							<input v-model.number="form.showroomPrice" type="number" class="px-3 py-2 bg-gray-50 border w-3/4 h-full text-center text-3xl outline-none" :class="{ 'border-red-500': !$v.form.credit_amount.limit }" />

							<p class="text-xs text-red-500" v-if="!$v.form.showroomPrice.isNumber">{{ $t("credit.modal.validation.invalid_price") }}</p>
						</div>

						<div class="col-span-1 space-y-2 flex flex-col items-end justify-start">
							<button @click="submitForm()" class="w-40 py-2 text-sm bg-blue-400 hover:bg-blue-500 border border-blue-500 text-white">{{ $t("button.confirm") }}</button>
							<button @click="$emit('close')" class="w-40 py-2 text-sm bg-gray-50 hover:bg-gray-100 border border-gray-400">{{ $t("button.cancel") }}</button>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import { required, max, requiredIf,email } from "vuelidate/lib/validators";
import AOS from "aos";
import "aos/dist/aos.css";
import dropdowns from "../../mixins/dropdowns";

export default {
	name: "TransactionModal",
	props: ["info", "accountNumber"],
	mixins: [dropdowns],
	validations() {
		return {
			form: {
				transaction_type: { required },
				receiver_account: { required },

				credit_amount: {
					required,
					limit: (value) => value <= this.info.total_blocks && value > 0,
					isNumber: (value) => value % 1 === 0,
				},
				showroomPrice: {
					isNumber: (value) => value % 1 === 0,
				},
				retirementPurposeOption: {
					required: requiredIf((value) => value.transaction_type === 3),
				},
				retirementOnBehalfOf: {
					required: requiredIf((value) => value.transaction_type === 3 && value.retirementPurposeOption === 2),
					// requireIfSelect: (value) => value.transaction_type === 3 && value.retirementPurposeOption === 2 && value !== null,
				},
				retirementOtherPurpose: {
					required: requiredIf((value) => value.transaction_type === 3 && value.retirementPurposeOption === 3),

					// requireIfSelect: (value) => value.transaction_type === 3 && value.retirementPurposeOption === 3 && value !== null,
				},

				cancellationReasonId: {
					required: requiredIf((value) => value.transaction_type === 1 || value.transaction_type === 5),
				},
				cancellationReasonOther: {
					required: requiredIf((value) => value.transaction_type === 1 && value.cancellationReasonId === 7),
				},
				onBehalfOfName: {
					required: requiredIf((value) => (value.transaction_type === 1 || value.transaction_type === 5) && this.onbehalofOption === 2),
				},
				onBehalfOfEmail: {
					required: requiredIf((value) => (value.transaction_type === 1 || value.transaction_type === 5) && this.onbehalofOption === 2),
					email
				},
				byAccountNumber: {
					required: requiredIf((value) => (value.transaction_type === 1 || value.transaction_type === 5) && this.onbehalofOption === 1),
				},
			},
		};
	},
	data() {
		return {
			dropdowns: {
				transactions: [],
				accounts: [],
				cancellationReasons: [],
				ITMOsCancellationReasons: [],
				usersOnbehalfOf: [],
			},
			onbehalofOption: 1,
			form: {
				transaction_type: "",
				receiver_account: "",
				credit_amount: this.info.total_blocks,
				remark: "",
				year: this.info.vintage_year,
				project_id: this.info.project_id,
				option: null,
				other_purpose: "",
				on_behalf_of: null,

				retirementPurposeOption: null,
				retirementOtherPurpose: null,
				retirementOnBehalfOf: "",

				cancellationReason: "",
				showroomPrice: 0,
				cancellationReasonId: null,
				cancellationReasonOther: "",
				onBehalfOfName: "",
				onBehalfOfEmail: "",
				byAccountNumber: "",
			},
			isSubmitted: false,
		};
	},
	async mounted() {
		AOS.init();
		this.dropdowns.cancellationReasons = await this.getCancellationReason();
		this.dropdowns.ITMOsCancellationReasons = await this.getITMOsCancellationReason();
		await this.getTransactionTypeDropdowns();
		await this.loadAccountDropdown();
		
	},
	methods: {
		async loadAccountDropdown() {
			this.dropdowns.usersOnbehalfOf = await this.getAccountDropdowns(0);
		},
		async getTransactionTypeDropdowns() {
			this.dropdowns.transactions = await this.$axios
				.$get(`/api/v1/dropdown/transaction-types`)
				.then((resp) => resp)
				.catch((err) => console.log(err));
		},
		async getAccountReceiverDropdowns() {
			// console.log("sds");
			this.form.receiver_account = "";
			this.dropdowns.accounts = await this.$axios
				.$get(`/api/v1/dropdown/account-numbers?transaction_type=${this.form.transaction_type}`)
				.then((resp) => resp)
				.catch((err) => console.log(err));
		},
		projectName(data) {
			if (this.$i18n.locale === "th") {
				return data?.thai;
			} else {
				return data?.english;
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
									<path stroke-linecap="round" stroke-linejoin="round" d="M7.5 21L3 16.5m0 0L7.5 12M3 16.5h13.5m0-13.5L21 7.5m0 0L16.5 12M21 7.5H7.5" />
								</svg>



								`,
					title: this.$t("sweetalert.transferModal.title.confirm"),
					text: this.$t("sweetalert.transferModal.text.confirm"),
					showCancelButton: true,

					confirmButtonColor: "#60a5fa",
					confirmButtonText: `${app.$t("button.confirm")}`,
					cancelButtonText: `${app.$t("button.cancel")}`,
					reverseButtons: true,
				})
				.then((result) => {
					if (result.isConfirmed) {
						app.form.transfer_account = app.accountNumber;
						app.$swal.fire({
							title: this.$t("sweetalert.waiting"),
							text: this.$t("saving"),
							allowOutsideClick: false,
							showCloseButton: false,
						});
						app.$swal.showLoading();
						app.$axios
							.$post(`/api/v1/credit/${app.info._id}/transfer`, app.form)
							.then((resp) => {
								// console.log(resp);
								app.$swal.close();

								app.$swal
									.fire({
										icon: "success",
										iconColor: "#059669",
										confirmButtonColor: "#059669",
										title: app.$t("sweetalert.transferModal.title.success"),
										text: app.$t("sweetalert.transferModal.text.success"),
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
									title: app.$t("sweetalert.transferModal.title.error"),
									text: app.$t("sweetalert.transferModal.text.error"),
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
#transfer .v-select .vs__dropdown-toggle {
	-webkit-appearance: none;
	-moz-appearance: none;
	appearance: none;
	background: #fff;

	border: 1px solid #e8e8e8 !important;

	border-radius: 0px !important;

	display: flex;
	align-items: center;
	padding: 6px 1px 6px 1px !important;
	white-space: normal;
}
</style>
