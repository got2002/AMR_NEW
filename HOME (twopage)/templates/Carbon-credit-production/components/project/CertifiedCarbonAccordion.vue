<template>
	<div class="w-full bg-white shadow-sm border rounded divide-y">
		<div :class="{ 'rounded-t': drop, rounded: !drop }" class="flex flex-wrap justify-between cursor-pointer hover:bg-gray-50" @click="drop = !drop">
			<div class="flex items-center gap-4 text-sm">
				<div class="flex items-center gap-2 h-full">
					<div
						:class="{
							'bg-yellow-500 ': item.status == 0,
							'bg-purple-500': item.status == 1,
							'bg-green-500': item.status == 2,
							'rounded-tl': drop,
							'rounded-l': !drop,
						}"
						class="w-1 text-sm text-white h-full"
					></div>
					<div class="py-3 text-sm w-52">{{ dateLocale(item.start_date) }} - {{ dateLocale(item.end_date) }}</div>
				</div>
				<projectCertificateCarbonIssuedBadge :item="item" />
				<projectCertificateCarbonBufferBadge :item="item" />
			</div>

			<div class="flex items-center justify-center px-4">
				<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" :class="{ 'rotate-180': drop }" class="w-5 h-5 transform delay-75 duration-100">
					<path stroke-linecap="round" stroke-linejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" />
				</svg>
			</div>
		</div>
		<div v-if="drop" class="p-4 grid grid-cols-4 gap-4 text-sm">
			<div class="col-span-2">
				<label>{{ $t("project.view_page.credit_period") }}</label>
				<div class="w-full border border-gray-400 rounded">
					<DatePicker range-separator=" - " :lang="$i18n.locale" :placeholder="$t('project.view_page.start_date') + ' - ' + $t('project.view_page.end_date')" :formatter="thaiformatter" @change="periodChange()" v-model="creditPeriod" range format="DD MMM YYYY" value-type="date" input-class="px-3 py-2 text-left w-full bg-transparent outline-none focus:border-tgo-teal-500"> </DatePicker>
				</div>
			</div>
			<div class="col-span-2" v-if="item.status !== 2">
				<label>{{ $t("project.view_page.certicate_carbon.quantity") }} (tCO<sub>2</sub>eq)</label>

				<input type="number" v-model.number="item.amount" :disabled="item.status === 2" :min="0" class="py-2 px-3 border border-gray-400 w-full outline-none rounded" />
				<!-- <p class="text-xs text-red-500" v-if="!$v.item.amount.minAmount && submitted">{{ $t("form_validation.min_max", { min: 0, max: 100000 }) }}</p> -->
			</div>
			<div class="col-span-2">
				<label>{{ $t("project.view_page.certicate_carbon.issuance_date") }}</label>
				<div class="w-full border border-gray-400 rounded">
					<DatePicker :lang="$i18n.locale" :formatter="thaiformatter" @change="issuedDateChange()" v-model="issued_date" format="DD MMM YYYY" value-type="date" input-class="px-3 py-2 text-left w-full bg-transparent outline-none focus:border-tgo-teal-500"> </DatePicker>
				</div>
			</div>
			<div class="col-span-2" v-if="item.status !== 2 && ['Premium T-VER'].includes(projectStandard) && ['การลด ดูดซับ และกักเก็บก๊าซเรือนกระจกจากภาคป่าไม้และการเกษตร'].includes(projectTypeByExtens)">
				<label>{{ $t("project.view_page.certicate_carbon.percent_buffer") }} (%)</label>
				<div class="flex items-center gap-2 rounded border border-gray-400 pl-3">
					<input type="range" v-model.number="percentBuffer" min="0" max="20" class="w-8/12" />
					<input type="number" v-on:keyup="checkMaxPercent($event.target.value)" v-model.number="percentBuffer" :min="0" :max="20" class="text-center border-l border-gray-400 py-2 w-4/12 outline-none bg-transparent" />
				</div>
				<div v-if="percentBuffer > 0" class="text-xs">
					<div>
						<span>Buffer</span>
						<span class="text-blue-500">{{ percentBuffer }}%</span>
						<span>--></span>
						<span class="text-green-500">{{ Math.ceil(item.amount * (percentBuffer / 100)).toLocaleString() }}</span> tCO2eq
					</div>
					<div>
						<span>Total</span>
						<span class="text-blue-500">{{ 100 - percentBuffer }}%</span>
						<span>--></span>
						<span class="text-green-500">{{ (item.amount - Math.ceil(item.amount * (percentBuffer / 100))).toLocaleString() }}</span> tCO2eq
					</div>
				</div>
			</div>

			<div class="col-span-4 border border-gray-400 rounded">
				<table v-if="item.status === 2" class="w-full text-xs">
					<tr class="divide-x divide-gray-400 border-b border-gray-400 bg-gray-100 rounded">
						<th class="p-2">type</th>
						<th>total</th>
						<th>Issued Date</th>
						<th>serial number</th>
					</tr>
					<tr class="divide-x divide-gray-400 border-b border-gray-400">
						<td class="text-center p-2">{{ bufferStatusText(0) }}</td>
						<td class="text-center p-2">{{ item.amount?.toLocaleString() }}</td>
						<td class="text-center p-2">{{ dateLocale(item.issued_date) }}</td>
						<td class="text-center p-2">{{ getSerial }}</td>
					</tr>
					<tr v-for="(buffer, i) in item.buffers" :key="i" class="divide-x divide-gray-400 border-b border-gray-400">
						<td class="text-center p-2">{{ bufferStatusText(buffer.buffer_type) }}</td>
						<td class="text-center p-2">{{ buffer.amount?.toLocaleString() }}</td>
						<td class="text-center p-2">{{ dateLocale(buffer.issued_date) }}</td>

						<td class="text-center p-2">{{ buffer.serial_number }}</td>
					</tr>
					<tr class="divide-x divide-gray-400">
						<td class="text-center p-2 bg-gray-100">Total</td>
						<td colspan="3" class="text-center p-2">{{ (item.amount + item.buffer_amount)?.toLocaleString() }}</td>
					</tr>
				</table>
				<!-- <UILabel :text="$t('Serial Number')" />
				<div v-if="item.status === 2" class="text-gray-500">
					{{ getSerial }}
				</div>
				<div v-else>-</div> -->
			</div>
			<div class="col-span-4">
				<label>{{ $t("project.view_page.certicate_carbon.document") }}</label>

				<div class="space-y-2">
					<template v-for="(doc, i) in item.certified_files">
						<div :key="i" class="w-full cursor-pointer flex items-center">
							<div class="w-full bg-gray-200 py-2 px-2" @click="openPDF(doc.src)">
								<p class="text-xs font-thin text-left break-words">{{ doc.name }}</p>
							</div>
							<div class="" @click="removeFile(i)">
								<IconXMark />
							</div>
						</div>
					</template>

					<div class="w-full">
						<dropzone id="dropDocument3" ref="dropDocument3" :options="dropzoneOptions" :useCustomSlot="true" @vdropzone-success="uploadSuccess" class="cursor-pointer border-dashed border-1 border-primary-dark">
							<label for="dropDocument3" class="">
								<div class="flex justify-center items-center w-full border-2 border-dashed py-1 cursor-pointer hover:bg-gray-50">
									<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
										<path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
									</svg>

									<p class="text-sm text-gray-500 dark:text-gray-400">PDF</p>
								</div>
							</label>
						</dropzone>
					</div>
					<PDFModal v-if="pdfModal" @close="pdfModal = false" :pdfURL="pdfURL"></PDFModal>
				</div>
			</div>
			<div class="col-span-4 flex items-center justify-start gap-4">
				<button @click="$emit('deleteIssueCredit')" v-if="item.status == 0" class="w-20 py-2 shadow-sm text-white bg-red-500 hover:bg-red-600 rounded">{{ $t("button.delete") }}</button>
				<button @click="IssueCredit(item._id)" v-if="item.status == 0 && [1, 99].includes($auth.user.role)" class="w-40 py-2 shadow-sm text-white bg-green-500 hover:bg-green-600 rounded">{{ $t("button.issued") }}</button>
			</div>
		</div>
	</div>
</template>

<script>
// import { required } from "vuelidate/lib/validators";
import Dropzone from "nuxt-dropzone";
import "nuxt-dropzone/dropzone.css";
import thaiformatter from "../../mixins/thaiformatter";

export default {
	props: ["item", "programID", "project_id", "vintageYear", "authorizedUse", "additionalCertificationCode", "projectStandard", "projectTypeByExtens"],
	mixins: [thaiformatter],
	components: {
		Dropzone,
	},
	data() {
		return {
			drop: false,
			submitted: false,
			creditPeriod: [],
			issued_date: this.$dayjs(new Date()).toDate(),
			dropzoneOptions: {
				url: process.env.baseUrl + "/api/v1/form/upload",
				disablePreviews: true,
				parallelUploads: 10,
				previewsContainer: false,
				maxFiles: 10,
			},
			pdfURL: "",
			pdfModal: false,
			percentBuffer: 20,
		};
	},
	watch: {
		creditPeriod: {
			handler: function () {
				this.periodChange();
			},
			deep: true,
		},
	},
	// validations() {
	// 	return {
	// 		item: {
	// 			amount: { minAmount: (value) => value > 0 && value <= 100000 },
	// 		},
	// 	};
	// },
	computed: {
		getSerial() {
			// console.log(this.authorizedUse);
			return `TH1-${this.programID}-${this.project_id}-${this.item.day_batch_number}-${this.vintageYear}-${this.item.block_start}-${this.item.block_end}-${this.authorizedUse}-${this.additionalCertificationCode}`;
		},

		
	},

	mounted() {
		if (this.item.issued_date) this.issued_date = this.$dayjs(this.item.issued_date).toDate();
		else this.issuedDateChange();

		if (this.item.percentBuffer) this.percentBuffer = this.item.percentBuffer;
		else {
			if(this.item.status !== 2 && ['Premium T-VER'].includes(this.projectStandard) && ['การลด ดูดซับ และกักเก็บก๊าซเรือนกระจกจากภาคป่าไม้และการเกษตร'].includes(this.projectTypeByExtens)){
				this.percentBuffer = 20
			}
			else this.percentBuffer = 0;
			
		}
		
		this.mapDateValue();
		// this.issuedDateChange()
	},
	methods: {
		checkMaxPercent(value) {
			if (value > 20) {
				this.percentBuffer = 20;
			} else if (value < 0) {
				this.percentBuffer = 20;
			} else {
				this.percentBuffer = value;
			}
		},
		removeFile(i) {
			this.item.certified_files.splice(i, 1);
		},
		openPDF(src) {
			this.pdfURL = process.env.baseUrl + src;
			this.pdfModal = true;
		},
		periodChange() {
			[this.item.start_date, this.item.end_date] = this.creditPeriod;
			if (this.creditPeriod.length === 2 && !this.creditPeriod.includes(null)) {
				this.item.valid_start = this.$dayjs(this.item.valid_start).format("YYYY-MM-DD");
				this.item.valid_end = this.$dayjs(this.item.valid_end).format("YYYY-MM-DD");

				this.item.start_date = this.$dayjs(this.creditPeriod[0]).format("YYYY-MM-DD");
				this.item.end_date = this.$dayjs(this.creditPeriod[1]).format("YYYY-MM-DD");

				console.log(this.item.start_date, this.item.end_date);
			} else {
				this.item.valid_start = null;
				this.item.valid_end = null;
			}

			// console.log(this.form.carbon_credit_cert[idx]);
		},
		issuedDateChange() {
			this.item.issued_date = this.$dayjs(this.issued_date).format("YYYY-MM-DD");

			// console.log(this.form.carbon_credit_cert[idx]);
		},
		dateLocale(date) {
			if (this.$i18n.locale === "th") {
				return this.$dayjs(date).locale("th").format("DD MMM BBBB");
			}
			return this.$dayjs(date).locale("en").format("DD MMM YYYY");
		},
		statusText(val) {
			switch (val) {
				case 0:
					if (this.$i18n.locale === "th") return "รอ";
					else return "waiting";
				case 1:
					if (this.$i18n.locale === "th") return "issued";
					else return "issued";
			}
		},
		bufferStatusText(val) {
			switch (val) {
				case 0:
					if (this.$i18n.locale === "th") return "Carbon Issued";
					else return "Carbon Issued";
				case 1:
					if (this.$i18n.locale === "th") return "Carbon Buffer";
					else return "Carbon Buffer";
				case 2:
					if (this.$i18n.locale === "th") return "Buffer Issued";
					else return "Buffer Issued";
				case 3:
					if (this.$i18n.locale === "th") return "Reversal Retirement";
					else return "Reversal Retirement";
			}
		},
		uploadSuccess(file, response) {
			// this.$emit("uploadSuccess", response);
			this.item.certified_files.push(response);
			this.$refs.dropDocument3.removeAllFiles();
		},
		mapDateValue() {
			const converseStartDate = this.$dayjs(this.item.start_date).toDate();
			const converseEndDate = this.$dayjs(this.item.end_date).toDate();
			this.creditPeriod = [converseStartDate, converseEndDate];
		},
		IssueCredit(certId) {
			const app = this;
			this.submitted = true;
			// this.$v.$touch();

			// if (this.$v.$invalid) {
			// 	this.$swal.fire({
			// 		icon: "error",
			// 		title: this.$t("sweetalert.invalid"),
			// 		text: this.$t("sweetalert.complete_information_text"),
			// 		confirmButtonColor: "#ef4444",
			// 	});

			// 	return;
			// }
			app.$swal
				.fire({
					icon: "info",
					iconColor: "#059669",
					iconHtml: `
								<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-10 h-10">
									<path stroke-linecap="round" stroke-linejoin="round" d="M10.125 2.25h-4.5c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125v-9M10.125 2.25h.375a9 9 0 019 9v.375M10.125 2.25A3.375 3.375 0 0113.5 5.625v1.5c0 .621.504 1.125 1.125 1.125h1.5a3.375 3.375 0 013.375 3.375M9 15l2.25 2.25L15 12" />
								</svg>
								`,
					title: this.$t("sweetalert.project.certifiedCredit.confirm.title"),
					text: this.$t("sweetalert.project.certifiedCredit.confirm.sub_title"),
					showCancelButton: true,

					confirmButtonColor: "#059669",
					confirmButtonText: this.$t("sweetalert.confirm"),
					cancelButtonText: this.$t("sweetalert.cancel"),
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
						app.item.start_date = app.$dayjs(app.item.start_date).format("YYYY-MM-DD");
						app.item.end_date = app.$dayjs(app.item.end_date).format("YYYY-MM-DD");
						if(!(/^\d{4}-\d{2}-\d{2}$/.test(app.item.issued_date))) app.item.issued_date = app.$dayjs(app.item.issued_date).format("YYYY-MM-DD");
						app.item.buffer_amount = Math.ceil(app.item.amount * (app.percentBuffer / 100));
						app.$axios
							.$put(`/api/v1/project/issued/${app.$route.params.id}/credit/${certId}`, app.item)
							.then((resp) => {
								app.$swal.close();
								app.$swal
									.fire({
										icon: "success",
										iconColor: "#059669",
										title: this.$t("sweetalert.project.certifiedCredit.success.title"),
										text: this.$t("sweetalert.project.certifiedCredit.success.sub_title", { amount: app.item.amount }),
										confirmButtonColor: "#059669",
									})
									.then(() => {
										this.$emit("reload");
									});
							})
							.catch((err) => {
								app.$swal.close();
								app.$swal.fire({
									icon: "error",
									title: this.$t("sweetalert.project.certifiedCredit.error.title"),
									text: this.$t("sweetalert.project.certifiedCredit.error.sub_title"),
									confirmButtonColor: "#ef4444",
								});
								console.log(err.response);
							});
					}
				});
		},
	},
};
</script>

<style>
</style>