<template>
	<div class="w-full grid grid-cols-1 xl:grid-cols-1 2xl:grid-cols-1 mt-4">
		<table class="items-center w-full space-y-6 border border-theme-black-300">
			<thead>
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
					<th colspan="1" class="border-l border-black py-2">{{ $t("project.view_page.certicate_carbon.quantity") }} (tCO<sub>2</sub>eq)</th>
					<th colspan="1" class="py-2">{{ $t("project.view_page.certicate_carbon.document") }}</th>
				</tr>
			</thead>
			<tbody class="bg-white border border-theme-black-300">
				<template v-for="(data, index) in form.carbon_credit_cert">
					<tr tabindex="0" class="focus:outline-none text-xs h-12 rounded hover:bg-theme-green-100 align-middle border border-theme-black-300" :key="index">
						<td width="40%" class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center border border-theme-black-300">
							<span class="font-medium text-xs text-theme-black-300 leading-6 ml-2">{{ dateLocale(data.start_date) }} - {{ dateLocale(data.end_date) }}</span>
						</td>
						<td width="35%" class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center border border-theme-black-300">
							<span class="font-medium text-xs text-theme-black-300 leading-6 ml-2 uppercase">{{ data.amount.toLocaleString() }}</span>
						</td>
						<td v-if="data.certified_files.length != 0" width="20%" @click="seePdf(data)" class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center border border-theme-black-300">
							<div class="flex justify-center">
								<button>
									<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
										<path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
									</svg>
								</button>
							</div>
						</td>
						<td v-else width="25%" class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center border border-theme-black-300">
							<div class="flex justify-center">
								<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
									<path stroke-linecap="round" stroke-linejoin="round" d="M19.5 12h-15" />
								</svg>
							</div>
						</td>
						<td class="text-center px-2"><p class="rounded-full text-white py-1" :class="{'bg-yellow-500 ':data.status == 0,'bg-green-500':data.status == 1}">{{statusText(data.status)}}</p></td>
					</tr>
					<tr v-if="index == form.carbon_credit_cert.length - 1" tabindex="0" class="bg-theme-black-50 bg-opacity-50 text-xs h-12 rounded hover:bg-theme-green-100 align-middle divide-x divide-black" :key="index + 'sum'">
						<td width="40%" class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center">
							<span class="font-medium text-xs text-theme-black-300 leading-6 ml-2 uppercase">{{ $t("project.view_page.sum") }}</span>
						</td>
						<td width="20%" class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center">
							<span class="font-medium text-xs text-theme-black-300 leading-6 ml-2 uppercase">{{ sumCarbon() }}</span>
						</td>
						<td colspan="2"></td>
					</tr>
				</template>
			</tbody>
		</table>
		<ProjectModal v-show="showModal" @close-modal="showModal = false" :number="number" :form="dataModal" />
	</div>
</template>

<script>
export default {
	props: ["form"],
	data() {
		return {
			showModal: false,
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
	computed: {
		// fullName() {
		// 	return `${this.loggedInUser.firstname} ${this.loggedInUser.lastname}`;
		// },
	},
	mounted() {
		// console.log(this.loggedInUser, this.isAuthenticated)
	},
	methods: {
		seePdf(value) {
			// console.log(value);
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
	
		sumCarbon() {
			let sum = 0;
			// console.log(this.form);
			this.form.carbon_credit_cert.forEach((element) => {
				sum += element.amount;
			});
			return sum.toLocaleString();
		},

		statusText(val){
			switch(val){
				case 0:
					if(this.$i18n.locale === 'th') return 'รอ'
					else return 'waiting'
				case 1:
					if(this.$i18n.locale === 'th') return 'issued'
					else return 'issued'
					
			}
		}	
	},
};
</script>