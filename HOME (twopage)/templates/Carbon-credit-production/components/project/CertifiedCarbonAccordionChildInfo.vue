<template>
	<div class="w-full bg-white rounded">
		<div class="flex flex-wrap justify-between cursor-pointer hover:bg-gray-200 border bg-white rounded" @click="drop = !drop">
			<div class="flex items-center gap-4 text-sm">
				<div class="flex items-center gap-2 h-full">
					<div
						:class="{
							'rounded-tl': drop,
							'rounded-l': !drop,
						}"
						class="w-1 text-sm text-white h-full bg-red-500"
					></div>
					<!-- project.view_page.certicate_carbon.cancellation_carbon -->
					<div class="py-3 text-sm w-52">{{ $t("project.view_page.certicate_carbon.cancellation") }}</div>
				</div>
				<div class="text-center px-4 py-1 bg-red-500 bg-opacity-10 rounded-full text-red-500 border border-red-500">{{ cancellationSum() }} tCO<sub>2</sub>eq</div>
			</div>

			<div class="flex items-center justify-center px-4">
				<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" :class="{ 'rotate-180': drop }" class="w-5 h-5 transform delay-75 duration-100">
					<path stroke-linecap="round" stroke-linejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" />
				</svg>
			</div>
		</div>
		<div v-if="drop" class="pl-8 pr-4 space-y-2 text-sm">
			<template v-for="(data, idx) in item.cancellation">
				<div class="relative" :key="idx + 'cancelled'">
					<div class="absolute z-10 top-0 -left-4 border-l-2 border-b-2 h-6 w-6"></div>
					<div v-if="idx + 1 !== item.cancellation.length" class="absolute z-10 top-6 -left-4 border-l-2 h-full w-6"></div>
					<ProjectCancelCreditTab :data="data" :vintageYear="vintageYear" :programID="programID" :project_id="project_id" :authorizedUse="authorizedUse" :additionalCertificationCode="additionalCertificationCode" />
				</div>
			</template>
		</div>
		<!-- <div v-if="drop" class="p-4 grid grid-cols-4 gap-4 text-sm">
			<div class="col-span-2">
				<label>{{ $t("project.view_page.credit_period") }}</label>
				<div class="w-full border border-gray-200 rounded py-2 px-4 bg-gray-200">{{ dateLocale(item.start_date) }} - {{ dateLocale(item.end_date) }}</div>
			</div>
			<div class="col-span-2">
				<label>{{ $t("project.view_page.certicate_carbon.quantity") }} (tCO<sub>2</sub>eq)</label>
				<div class="w-full border border-gray-200 rounded py-2 px-4 bg-gray-200">
					{{ item.amount?.toLocaleString() }}
				</div>
			</div>
			<div class="col-span-2">
				<label>{{ $t("project.view_page.certicate_carbon.issuance_date") }}</label>
				<div class="w-full border border-gray-200 rounded py-2 px-4 bg-gray-200">{{ dateLocale(item?.issued_date)}}</div>
			</div>
			<div class="col-span-4">
				<UILabel :text="$t('Serial Number')" />
				<div v-if="item.status === 2">
					{{ getSerial }}
				</div>
				<div v-else>
					-
				</div>
			</div>
			<div class="col-span-4">
				<label>{{ $t("project.view_page.certicate_carbon.document") }}</label>
				<ul class="list-disc pl-8">
					<template v-for="(doc, i) in item.certified_files">
						<li :key="i" class="w-full cursor-pointer text-sm font-thin hover:text-tgo-teal-500 hover:underline" @click="openPDF(doc.src)">
							{{ doc.name }}
						</li>
					</template>
					<PDFModal v-if="pdfModal" @close="pdfModal = false" :pdfURL="pdfURL"></PDFModal>
					<div v-if="item.certified_files.length == 0" class="p-4 w-full text-center bg-gray-200 rounded">{{ $t("no_data") }}</div>
				</ul>
			</div>
		</div> -->
	</div>
</template>

<script>
import thaiformatter from "../../mixins/thaiformatter";

export default {
	props: ["item", "programID", "project_id", "vintageYear", "authorizedUse", "additionalCertificationCode"],
	mixins: [thaiformatter],

	data() {
		return {
			drop: false,
			creditPeriod: [],
			dropzoneOptions: {
				url: process.env.baseUrl + "/api/v1/form/upload",
				disablePreviews: true,
				parallelUploads: 10,
				previewsContainer: false,
				maxFiles: 10,
			},
			pdfURL: "",
			pdfModal: false,
		};
	},
	computed: {
		getSerial() {
			// console.log(this.authorizedUse);
			return `TH1-${this.programID}-${this.project_id}-${this.item.day_batch_number}-${this.vintageYear}-${this.item.block_start}-${this.item.block_end}-${this.authorizedUse}-${this.additionalCertificationCode}`;
		},
	},

	mounted() {
		this.mapDateValue();
	},
	methods: {
		openPDF(src) {
			this.pdfURL = process.env.baseUrl + src;
			this.pdfModal = true;
		},
		periodChange() {
			[this.item.start_date, this.item.end_date] = this.creditPeriod;
			if (this.creditPeriod.length === 2 && !this.creditPeriod.includes(null)) {
				this.item.valid_start = this.$dayjs(this.item.valid_start).format("YYYY-MM-DD");
				this.item.valid_end = this.$dayjs(this.item.valid_end).format("YYYY-MM-DD");
			} else {
				this.item.valid_start = null;
				this.item.valid_end = null;
			}

			// console.log(this.form.carbon_credit_cert[idx]);
		},
		dateLocale(date) {
			if (!date) return this.$t("undefined");
			else if (this.$i18n.locale === "th") {
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
		uploadSuccess(file, response) {
			this.$emit("uploadSuccess", response);
			this.$refs.dropDocument3.removeAllFiles();
		},
		mapDateValue() {
			const converseStartDate = this.$dayjs(this.item.start_date).toDate();
			const converseEndDate = this.$dayjs(this.item.end_date).toDate();
			this.creditPeriod = [converseStartDate, converseEndDate];
		},
		cancellationSum() {
			const sumValue = this._.sumBy(this.item.cancellation, (item) => item.amount);
			return sumValue?.toLocaleString();
		},
	},
};
</script>

<style>
</style>