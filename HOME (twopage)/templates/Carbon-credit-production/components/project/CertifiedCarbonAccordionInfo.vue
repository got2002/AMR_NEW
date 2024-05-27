<template>
	<div class="w-full bg-white shadow-sm border rounded divide-y">
		<div :class="{ 'rounded-t': drop, rounded: !drop }" class="flex flex-wrap justify-between cursor-pointer hover:bg-gray-200" @click="drop = !drop">
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
				<div class="w-full border border-gray-200 rounded py-2 px-4 bg-gray-200">{{ dateLocale(item?.issued_date) }}</div>
			</div>
			<div class="col-span-2" v-if="item.status !== 2 && ['Premium T-VER'].includes(projectStandard) && ['การลด ดูดซับ และกักเก็บก๊าซเรือนกระจกจากภาคป่าไม้และการเกษตร'].includes(projectTypeByExtens)">
				<label>{{ $t("project.view_page.certicate_carbon.percent_buffer") }} (%)</label>

				<div class="w-full border border-gray-200 rounded px-4 bg-gray-200" :class="{ 'h-9': percentBuffer === 0, 'py-0.5': percentBuffer > 0 }">
					<div v-if="percentBuffer > 0" class="text-xs">
						<div>
							<span class="text-blue-500">{{ percentBuffer }}%</span>
							<span>--></span>
							<span class="text-green-500">{{ (item.amount * (percentBuffer / 100)).toLocaleString() }}</span> tCO2eq
						</div>
						<div>
							<span class="text-blue-500">{{ 100 - percentBuffer }}%</span>
							<span>--></span>
							<span class="text-green-500">{{ (item.amount * ((100 - percentBuffer) / 100)).toLocaleString() }}</span> tCO2eq
						</div>
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
			</div>
			<!-- <div class="col-span-4">
				<UILabel :text="$t('Serial Number')" />
				<div v-if="item.status === 2">
					{{ getSerial }}
				</div>
				<div v-else>-</div>
			</div> -->
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
		</div>
	</div>
</template>

<script>
import thaiformatter from "../../mixins/thaiformatter";

export default {
	props: ["item", "programID", "project_id", "vintageYear", "authorizedUse", "additionalCertificationCode", "projectStandard", "projectTypeByExtens"],
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
			percentBuffer: 0,
		};
	},
	computed: {
		getSerial() {
			// console.log(this.authorizedUse);
			return `TH1-${this.programID}-${this.project_id}-${this.item.day_batch_number}-${this.vintageYear}-${this.item.block_start}-${this.item.block_end}-${this.authorizedUse}-${this.additionalCertificationCode}`;
		},
	},

	mounted() {
		if (this.item.percentBuffer) this.percentBuffer = this.item.percentBuffer;
		else this.percentBuffer = 0;
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
			this.$emit("uploadSuccess", response);
			this.$refs.dropDocument3.removeAllFiles();
		},
		mapDateValue() {
			const converseStartDate = this.$dayjs(this.item.start_date).toDate();
			const converseEndDate = this.$dayjs(this.item.end_date).toDate();
			this.creditPeriod = [converseStartDate, converseEndDate];
		},
	},
};
</script>

<style>
</style>