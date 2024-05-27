<template>
	<div class="w-full grid grid-cols-1 xl:grid-cols-1 2xl:grid-cols-1 mt-4">
		<table class="items-center w-full space-y-6 border border-theme-black-300">
			<thead>
				<!-- <tr>
					<th class="px-3 bg-theme-black-50 bg-opacity-50 text-sm font-bold text-theme-black-300 align-middle py-3 border border-theme-black-300 text-center">
						{{ $t("project.view_page.credit_period") }}
					</th>
					<th v-html="$t('project.view_page.approved_carbon_credits')" class="px-3 bg-theme-black-50 bg-opacity-50 text-sm font-bold text-theme-black-300 align-middle py-3 border border-theme-black-300 text-center"></th>
					<th class="px-3 bg-theme-black-50 bg-opacity-50 text-sm font-bold text-theme-black-300 align-middle py-3 border border-theme-black-300 text-center">
						{{ $t("project.view_page.greenhouse_gases_amount_approve") }}
					</th>
				</tr> -->

				<tr class="bg-theme-black-50 bg-opacity-50 divide-x divide-black text-sm">
					<th colspan="1" rowspan="2" class="px-3 font-bold text-theme-black-300 align-middle py-3 text-center">
						{{ $t("project.view_page.credit_period") }}
					</th>
					<th colspan="2" class="px-3 font-bold text-theme-black-300 align-middle py-3 text-center border-b border-black">
						{{ $t("project.view_page.certicate_carbon.certified_carbon_credit") }}
					</th>

					<th rowspan="2" colspan="1" class="px-3 font-bold text-theme-black-300 align-middle py-3 text-center">
						{{ $t("project.view_page.status_certificate_carbon") }}
					</th>
				</tr>
				<tr class="divide-x divide-black text-sm">
					<th colspan="1" class="border-l border-black py-2">
						{{ $t("project.view_page.certicate_carbon.quantity") }}
						<p class="text-xs">(tCO<sub>2</sub>eq)</p>
					</th>
					<th colspan="1" class="py-2">{{ $t("project.view_page.certicate_carbon.document") }}</th>
				</tr>
			</thead>
			<tbody class="bg-white border border-theme-black-300">
				<template v-for="(data, index) in form.carbon_credit_cert">
					<tr :key="index" tabindex="0" class="text-xs h-12 hover:bg-theme-green-100 align-middle border border-black divide-x divide-black">
						<td width="30%" class="">
							<!-- <span class="font-medium text-sm text-theme-black-300 leading-6 ml-2 uppercase">{{ dateLocale(data.start_date) }} - {{ dateLocale(data.end_date) }}</span> -->
							<div class="w-full h-full">
								<DatePicker range-separator=" - " :lang="$i18n.locale" :placeholder="$t('project.view_page.start_date') + ' - ' + $t('project.view_page.end_date')" :formatter="thaiformatter" @change="periodChange(index)" v-model="creditPeriod[index]" range format="DD MMM YYYY" value-type="date" input-class="px-2 text-left w-full h-12 bg-bg-transparent"> </DatePicker>
							</div>

							<!-- <input type="date" class="border-2" v-model="data.start_date" /> - <input type="date" class="border-2 xl:w-1/3 2xl:w-auto" v-model="data.end_date" /> -->
						</td>
						<td width="35%" class="">
							<input v-model.number="data.amount" class="w-full bg-transparent text-center outline-none h-12 border focus:border-tgo-teal-500" />
						</td>
						<td width="35%" class="">
							<div class="flex justify-center gap-2">
								<button @click="seePdf(data, index)" target="_blank" class="">
									<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
										<path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
									</svg>
								</button>
								<button @click="deletePDF(index)" target="_blank" class="">
									<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
										<path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
									</svg>
								</button>
							</div>
						</td>
						<td class="text-center px-2">
							<p class="rounded-full text-white py-1" :class="{ 'bg-yellow-500 ': data.status == 0, 'bg-green-500': data.status == 1 }">{{ statusText(data.status) }}</p>
						</td>
					</tr>
					<tr v-if="index == form.carbon_credit_cert.length - 1" tabindex="0" class="focus:outline-none text-xs h-12 rounded rounded-t-none hover:bg-theme-green-100 align-middle border border-theme-black-300" :key="index + 'sum'">
						<td width="40%" class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center border border-theme-black-300">
							<span class="font-medium text-sm text-theme-black-300 leading-6 ml-2 uppercase">{{ $t("project.view_page.sum") }}</span>
						</td>
						<td width="35%" class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center border border-theme-black-300">
							<span class="font-medium text-sm text-theme-black-300 leading-6 ml-2 uppercase">{{ sumCarbon() }}</span>
						</td>
						<td></td>
					</tr>
				</template>
			</tbody>
		</table>
		<ProjectModal v-show="showModal" @close-modal="showModal = false" :number="number" :form="dataModal" :edit="edit" />
	</div>
</template>

<script>
import thaiformatter from "../../mixins/thaiformatter";
export default {
	props: ["form", "edit"],
	mixins: [thaiformatter],
	data() {
		return {
			showModal: false,
			index: 0,
			creditPeriod: [],
			dataModal: {},
			number: 0,
			table: {
				head: [
					{
						name: this.$t("project.view_page.credit_period"),
						align: "center",
						filterable: false,
					},
					{
						name: this.$t("project.view_page.approved_carbon_credits"),
						align: "center",
						filterable: false,
					},
					{
						name: this.$t("project.view_page.greenhouse_gases_amount_approve"),
						align: "center",
						filterable: false,
					},
				],
			},
		};
	},
	watch: {
		"form.carbon_credit_cert.length"() {
			this.mapDateValue();
		},
	},
	computed: {
		// fullName() {
		// 	return `${this.loggedInUser.firstname} ${this.loggedInUser.lastname}`;
		// },
	},
	mounted() {
		// console.log(this.loggedInUser, this.isAuthenticated)
		this.mapDateValue();
		// console.log(this.creditPeriod);
	},
	// updated() {
	// 	// console.log(this.loggedInUser, this.isAuthenticated)
	// 	this.creditPeriod = this._.map(this.form.carbon_credit_cert, (data, idx) => {
	// 		return [data.start_date, data.end_date];
	// 	});
	// 	// console.log(this.creditPeriod);
	// },
	methods: {
		mapDateValue() {
			const app = this;
			this.creditPeriod = this._.map(this.form.carbon_credit_cert, (data, idx) => {
				const converseStartDate = app.$dayjs(data.start_date).toDate();
				const converseEndDate = app.$dayjs(data.end_date).toDate();
				return [converseStartDate, converseEndDate];
			});
		},
		periodChange(idx) {
			[this.form.carbon_credit_cert[idx].start_date, this.form.carbon_credit_cert[idx].end_date] = this.creditPeriod[idx];
			if (this.creditPeriod[idx].length === 2 && !this.creditPeriod[idx].includes(null)) {
				this.form.carbon_credit_cert[idx].valid_start = this.$dayjs(this.form.carbon_credit_cert[idx].valid_start).format("YYYY-MM-DD");
				this.form.carbon_credit_cert[idx].valid_end = this.$dayjs(this.form.carbon_credit_cert[idx].valid_end).format("YYYY-MM-DD");
			} else {
				this.form.carbon_credit_cert[idx].valid_start = null;
				this.form.carbon_credit_cert[idx].valid_end = null;
			}

			// console.log(this.form.carbon_credit_cert[idx]);
		},
		deletePDF(index) {
			this.form.carbon_credit_cert.splice(index, 1);
		},
		seePdf(value, index) {
			// console.log(value);
			this.index = index;
			this.dataModal = value;
			this.showModal = true;
		},
		dateToString(date) {
			const result = new Date(date).toLocaleDateString("th-TH", {
				year: "numeric",
				month: "long",
				day: "numeric",
			});
			return result;
		},
		dateLocale(date) {
			if (this.$i18n.locale === "th") {
				return this.$dayjs(date).locale("th").format("DD MMM BBBB");
			}
			return this.$dayjs(date).locale("en").format("DD MMM YYYY");
		},
		datetime(date) {
			if (this.$i18n.locale === "th") {
				return this.$dayjs(date).locale("th").format("DD MMM BBBB (HH:mm)");
			}
			return this.$dayjs(date).locale("en").format("DD MMM YYYY (HH:mm)");
		},
		sumCarbon() {
			let sum = 0;
			// console.log(this.form);
			this.form.carbon_credit_cert.forEach((element) => {
				sum += element.amount;
			});
			return sum.toLocaleString();
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
	},
};
</script>
