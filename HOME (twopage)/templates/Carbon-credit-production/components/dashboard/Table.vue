<template>
	<div v-if="!isLoading" class="w-full grid grid-cols-1 xl:grid-cols-1 2xl:grid-cols-1 mt-4">
		<section class="pt-6 pb-4">
			<div class="flex flex-wrap -mx-3 items-center">
				<div class="w-full lg:w-1/2 flex items-center mb-5 lg:mb-0 px-3">
					<div>
						<h2 class="mb-1 text-2xl text-theme-black-300 font-bold">{{ $t("dashboard.table.title") }}</h2>
					</div>
				</div>
				<div class="relative w-full lg:w-auto ml-auto px-3">
					<div class="relative inline-flex flex-wrap items-stretch mb-1">
						<button type="button" @click="generatePDF()" class="py-2 px-3 mr-2 mb-2 text-sm font-medium   focus:z-10 shadow-sm rounded bg-tgo-yellow-500 hover:bg-tgo-yellow-600">{{ $t("dashboard.table.filter.export") }}</button>
						<button type="button" @click="filterTran(1, 'day')" class="py-2 px-3 mr-2 mb-2 text-sm font-medium text-theme-white hover:text-gray-100 focus:z-10 shadow-sm rounded" :class="{ 'bg-tgo-teal-700': unit == 'day', 'bg-tgo-teal-500 hover:from-tgo-teal-500': unit != 'day' }">{{ $t("dashboard.table.filter._24Hour") }}</button>
						<button type="button" @click="filterTran(1, 'week')" class="py-2 px-3 mr-2 mb-2 text-sm font-medium text-theme-white hover:text-gray-100 focus:z-10 shadow-sm rounded" :class="{ 'bg-tgo-teal-700': unit == 'week', 'bg-tgo-teal-500 hover:from-tgo-teal-500': unit != 'week' }">{{ $t("dashboard.table.filter.week") }}</button>
						<button type="button" @click="filterTran(1, 'month')" class="py-2 px-3 mr-2 mb-2 text-sm font-medium text-theme-white hover:text-gray-100 focus:z-10 shadow-sm rounded" :class="{ 'bg-tgo-teal-700': unit == 'month', 'bg-tgo-teal-500 hover:from-tgo-teal-500': unit != 'month' }">{{ $t("dashboard.table.filter.month") }}</button>
					</div>
				</div>
			</div>
		</section>
		<table class="items-center w-full space-y-6 shadow-sm rounded-sm">
			<thead>
				<tr>
					<template v-for="(item, idx) in table.head">
						<ApiHeadSlotDark :text="item.name" :key="idx" :align="item.align" />
					</template>
				</tr>
			</thead>
			<tbody class="bg-white">
				<template v-for="(data, index) in dataList">
					<tr tabindex="0" class="focus:outline-none text-xs h-16 rounded hover:bg-theme-green-100 align-middle" :key="index">
						<td class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center">
							<span class="font-medium text-xs text-theme-black-300 leading-6 ml-2 uppercase">#{{ data.project_id }}</span>
						</td>
						<td class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center">
							<div class="w-128 h-auto break-all relative">
								<p class="font-medium text-xs text-theme-black-300 leading-6 ml-2 truncate">{{ data.from_project_name }}</p>
							</div>
						</td>
						<td class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center">
							<span class="font-medium text-xs text-theme-black-300 leading-6 ml-2 uppercase">{{ data.project_type }}</span>
						</td>
						<td class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center">
							<span class="font-medium text-xs text-theme-black-300 leading-6 ml-2 uppercase">{{ data.project_developer }}</span>
						</td>
						<td class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center">
							<span class="font-medium text-xs text-theme-black-300 leading-6 ml-2 uppercase">{{ data.from }}</span>
						</td>
						<td class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center">
							<span class="font-medium text-xs text-theme-black-300 leading-6 ml-2 uppercase">{{ data.to }}</span>
						</td>
						<td class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center">
							<span class="font-medium text-xs text-theme-black-300 leading-6 ml-2 uppercase">{{ data.status }}</span>
						</td>
						<td class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center">
							<span class="font-medium text-xs text-theme-black-300 leading-6 ml-2 uppercase">{{ data.created_at | dateFormat }}</span>
						</td>
					</tr>
				</template>
			</tbody>
		</table>
		<vue-html2pdf :show-layout="false" :float-layout="true" :enable-download="true" :preview-modal="true" :paginate-elements-by-height="1400" :filename="'transaction_statement_'+dateNow()" :pdf-quality="2" :manual-pagination="false" pdf-format="a3" :pdf-margin="10" pdf-orientation="landscape" pdf-content-width="100%" ref="html2Pdf">
			<section slot="pdf-content">
				<table class="items-center w-full space-y-6 shadow-sm rounded-sm">
					<thead>
						<tr>
							<template v-for="(item, idx) in table.head">
								<ApiHeadSlotDark :text="item.name" :key="idx" :align="item.align" />
							</template>
						</tr>
					</thead>
					<tbody class="bg-white">
						<template v-for="(data, index) in dataList">
							<tr tabindex="0" class="focus:outline-none text-xs h-16 rounded hover:bg-theme-green-100 align-middle border" :key="index">
								<td class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center border">
									<span class="font-medium text-xs text-theme-black-300 leading-6 ml-2 uppercase">#{{ data.project_id }}</span>
								</td>
								<td class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center border">
									<div class="w-128 h-auto break-all relative">
										<p class="font-medium text-xs text-theme-black-300 leading-6 ml-2 truncate">{{ data.from_project_name }}</p>
									</div>
								</td>
								<td class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center border">
									<span class="font-medium text-xs text-theme-black-300 leading-6 ml-2 uppercase">{{ data.project_type }}</span>
								</td>
								<td class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center border">
									<span class="font-medium text-xs text-theme-black-300 leading-6 ml-2 uppercase">{{ data.project_developer }}</span>
								</td>
								<td class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center border">
									<span class="font-medium text-xs text-theme-black-300 leading-6 ml-2 uppercase">{{ data.from }}</span>
								</td>
								<td class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center border">
									<span class="font-medium text-xs text-theme-black-300 leading-6 ml-2 uppercase">{{ data.to }}</span>
								</td>
								<td class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center border">
									<span class="font-medium text-xs text-theme-black-300 leading-6 ml-2 uppercase">{{ data.status }}</span>
								</td>
								<td class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center border">
									<span class="font-medium text-xs text-theme-black-300 leading-6 ml-2 uppercase">{{ data.created_at | dateFormat }}</span>
								</td>
							</tr>
						</template>
					</tbody>
				</table>
			</section>
		</vue-html2pdf>
		<div v-if="dataList.length == 0" tabindex="0" colspan="9" class="focus:outline-none text-xs h-16 bg-white rounded hover:bg-theme-green-100 align-middle cursor-pointer">
			<div class="flex justify-center items-center">
				<span class="font-medium text-xs text-theme-black-300 mt-5">{{ $t("alert.no_data") }}</span>
			</div>
		</div>
		<PaginationBar :meta="meta" @loadRequestByPage="loadRequestByPage" />
	</div>
</template>

<script>
import moment from "moment";
export default {
	data() {
		return {
			table: {
				head: [
					{
						name: this.$t("dashboard.table.header.project_id"),
						align: "center",
						filterable: false,
					},
					{
						name: this.$t("dashboard.table.header.project_title"),
						align: "center",
						filterable: false,
					},
					{
						name: this.$t("dashboard.table.header.project_type"),
						align: "center",
						filterable: false,
					},

					{
						name: this.$t("dashboard.table.header.project_developer"),
						align: "center",
						filterable: false,
					},

					{
						name: this.$t("dashboard.table.header.carbon_credit_provider"),
						align: "center",
						filterable: false,
					},

					{
						name: this.$t("dashboard.table.header.carbon_credit_receiver"),
						align: "center",
						filterable: false,
					},

					{
						name: this.$t("dashboard.table.header.status"),
						align: "center",
						filterable: false,
					},

					{
						name: this.$t("dashboard.table.header.time_of_procedure"),
						align: "center",
						filterable: false,
					},
				],
			},
			searchText: "",
			filter: null,
			current_page: 1,
			dataList: [],
			isLoading: true,
			meta: [],
			duration: "",
			unit: "",
			toggle: false,
		};
	},
	computed: {
		// fullName() {
		// 	return `${this.loggedInUser.firstname} ${this.loggedInUser.lastname}`;
		// },
	},
	filters:{
		dateFormat(date){
			return moment(date).format("DD MMM YYYY (HH:mm)");
		}
	},
	mounted() {
		// console.log(this.loggedInUser, this.isAuthenticated)
		this.getTransactions();
	},
	methods: {
		generatePDF() {
			this.$refs.html2Pdf.generatePdf();
		},
		filterTran(duration, unit) {
			if (unit === this.unit) {
				this.duration = "";
				this.unit = "";
				this.toggle = false;
			} else {
				this.duration = duration;
				this.unit = unit;
				this.toggle = true;
			}
			// console.log(this.unit)
			this.getTransactions();
		},
		async loadRequestByPage(pageNumber = 1) {
			this.current_page = pageNumber;
			console.log(`[Info] - Request Page Number ${pageNumber}`);
			await this.getTransactions();
		},
		async getTransactions() {
			const app = this;
			app.isLoading = true;
			let filter = "";
			if (this.duration !== "") filter += `&duration=${this.duration}`;
			if (this.unit !== "") filter += `&unit=${this.unit}`;
			await this.$axios
				.$get(`/api/v1/credit?page=${this.current_page}` + filter)
				.then((resp) => {
					// console.log(resp);
					app.dataList = resp.data;
					app.meta = resp.meta;
					// this.$toast.success("เพิ่มข้อมูลสำเร็จ");
					// this.$router.push("/users/userManagement");
					// setTimeout(this.$toast.clear, 3000);
					app.isLoading = false;
				})
				.catch((errors) => {
					console.log(errors);
					// this.$toast.error(errors.response.data.errors);
					// setTimeout(this.$toast.clear, 3000);
					app.isLoading = false;
				});
		},
		dateToString(data) {
			console.log(moment(data).format("DD MMM YYYY (HH:mm)"));

			return moment(data).format("DD MMM YYYY (HH:mm)");
		},
		dateNow() {
			var today = new Date();
			return moment(today).format("YYYY-MM-DD");
		},
		fullname(data) {
			return data.firstname + " " + data.lastname;
		},
		sumCarbon(data) {
			let sum = 0;
			data.forEach((element) => {
				sum += element.amount;
			});
			return sum;
		},
	},
};
</script>