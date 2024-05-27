<template>
	<section class="pt-2 pb-4 bg-theme-black-50 space-y-10">
		<section>
			<h2 class="mb-4 text-3xl font-bold">{{ $t("project.page_title") }}</h2>
			<div class="w-full grid lg:grid-cols-4 grid-cols-2 gap-4">
				<div class="col-span-1">
					<ProjectCarbonCreditAmount :title="$t('project.statCO2VolumeTitle.allProject')" :value="stat.total" :icon="1"></ProjectCarbonCreditAmount>
				</div>
				<div class="col-span-1">
					<ProjectCarbonCreditAmount :title="$t('project.statCO2VolumeTitle.verify')" :value="stat.verified" :icon="2"></ProjectCarbonCreditAmount>
				</div>
				<div class="col-span-1">
					<ProjectCarbonCreditAmount :title="$t('project.statCO2VolumeTitle.pending')" :value="stat.pending" :icon="3"></ProjectCarbonCreditAmount>
				</div>
				<div class="col-span-1">
					<ProjectCarbonCreditAmount :title="$t('project.statCO2VolumeTitle.concluded')" :value="stat.finish" :icon="4"></ProjectCarbonCreditAmount>
				</div>
			</div>

			<div class="w-full grid grid-cols-12 mt-8 border-b">
				<div class="col-span-2 p-2 cursor-pointer text-center" :class="{ 'border-b-2 border-tgo-teal-500': tab == 1 }" @click="tab = 1">
					{{ $t("project_inventory") }}
				</div>
				<div class="col-span-2 p-2 cursor-pointer text-center" :class="{ 'border-b-2 border-tgo-teal-500': tab == 2 }" @click="tab = 2;">
					{{ $t("cancellation_record") }}
				</div>
				<div class="col-span-2 p-2 cursor-pointer text-center" :class="{ 'border-b-2 border-tgo-teal-500': tab == 3 }" @click="tab = 3;">
					{{ $t("itmos_transfer_records") }}
				</div>
			</div>

			<div class="mt-8 w-full" v-if="tab == 1">
				<!-- <h2 class="mb-1 text-3xl font-bold">{{ $t("project.page_title") }}</h2> -->
				<div class="flex items-center gap-2 mb-2">
					<div class="flex shadow-sm">
						<select v-model="limit" @change="getDatatableProject(sort, 1)" class="text-sm text-center py-1 bg-white hover:bg-white cursor-pointer rounded focus:shadow-sm focus:outline-none">
							<option :value="10">10</option>
							<option :value="50">50</option>
							<option :value="100">100</option>
							<option :value="200">200</option>
						</select>
					</div>

					<div class="flex">
						<button @click="openFilter = !openFilter" class="bg-white flex items-center justify-center p-1 shadow-sm rounded" :class="{ 'bg-tgo-teal-500 text-white': openFilter }">
							<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
								<path stroke-linecap="round" stroke-linejoin="round" d="M12 3c2.755 0 5.455.232 8.083.678.533.09.917.556.917 1.096v1.044a2.25 2.25 0 01-.659 1.591l-5.432 5.432a2.25 2.25 0 00-.659 1.591v2.927a2.25 2.25 0 01-1.244 2.013L9.75 21v-6.568a2.25 2.25 0 00-.659-1.591L3.659 7.409A2.25 2.25 0 013 5.818V4.774c0-.54.384-1.006.917-1.096A48.32 48.32 0 0112 3z" />
							</svg>
						</button>
					</div>
				</div>

				<div v-if="openFilter" class="mb-2 w-full bg-white shadow-sm rounded">
					<ProjectFilter :filter="filter" :limit="meta.limit" @resetFilter="resetFilter" @getProject="getDatatableProject(sort, 1)" />
				</div>

				<Table class="w-full shadow-sm" :project="project" @sort="getDatatableProject($event, 1)" />
				<PaginationBar :meta="meta" @loadRequestByPage="loadRequestByPage" />
				<!-- <ProjectTable :project="project" @sort="getDatatableProject($event.field, $event.value, 1)" /> -->
			</div>
			<div class="mt-8 w-full" v-if="tab == 2">
				<div class="flex items-center gap-2 mb-2">
					<div class="flex shadow-sm">
						<select v-model="limit" @change="getCancellationProject(cancellation.sort, 1)" class="text-sm text-center py-1 bg-white hover:bg-white cursor-pointer rounded focus:shadow-sm focus:outline-none">
							<option :value="10">10</option>
							<option :value="50">50</option>
							<option :value="100">100</option>
							<option :value="200">200</option>
						</select>
					</div>

					<div class="flex">
						<button @click="cancellation.openFilter = !cancellation.openFilter" class="bg-white flex items-center justify-center p-1 shadow-sm rounded" :class="{ 'bg-tgo-teal-500 text-white': cancellation.openFilter }">
							<IconFilter />
						</button>
					</div>
				</div>
				<div v-if="cancellation.openFilter" class="mb-2 w-full bg-white shadow-sm rounded">
					<HomeFilter :filter="cancellation.filter" :limit="cancellation.meta?.limit" @resetFilter="resetCancellationFilter" @getProject="getCancellationProject(cancellation.sort, 1)" />
				</div>
				<HomeCancellationTable :project="cancellation.data" @sort="getCancellationProject($event, 1)" />
				<PaginationBar :meta="cancellation.meta" @loadRequestByPage="getCancellationProject({ key: 'transaction_date,project_id', value: '-1,-1' }, $event)" />
			</div>
			<div class="mt-8 w-full" v-if="tab == 3">
				<div class="flex items-center gap-2 mb-2">
					<div class="flex shadow-sm">
						<select v-model="limit" @change="getITMOsTransfer(transfer_records.sort, 1)" class="text-sm text-center py-1 bg-white hover:bg-white cursor-pointer rounded focus:shadow-sm focus:outline-none">
							<option :value="10">10</option>
							<option :value="50">50</option>
							<option :value="100">100</option>
							<option :value="200">200</option>
						</select>
					</div>

					<div class="flex">
						<button @click="transfer_records.openFilter = !transfer_records.openFilter" class="bg-white flex items-center justify-center p-1 shadow-sm rounded" :class="{ 'bg-tgo-teal-500 text-white': transfer_records.openFilter }">
							<IconFilter />
						</button>
					</div>
				</div>
				<div v-if="transfer_records.openFilter" class="mb-2 w-full bg-white shadow-sm rounded">
					<ITMOsFilter :filter="transfer_records.filter" :limit="transfer_records.meta?.limit" @resetFilter="resetCancellationFilter" @getProject="getITMOsTransfer(transfer_records.sort, 1)" />
				</div>
				<ITMOsTable :project="transfer_records.data" @sort="getITMOsTransfer($event, 1)" />
				<PaginationBar :meta="transfer_records.meta" @loadRequestByPage="getITMOsTransfer({ key: 'transaction_date,project_id', value: '-1,-1' }, $event)" />
			</div>
		</section>

		<section class="space-y-4">
			<h2 class="mb-4 text-3xl font-bold">{{ $t("statistics.page_title") }}</h2>
			<div class="w-full grid lg:grid-cols-3 grid-cols-1 gap-4">
				<StatCarbonCreditAmount :title="$t('statistics.statCO2VolumeTitle.approved_carbon_credits')" :value="carbon_summary.verifiedCredits"></StatCarbonCreditAmount>
				<StatCarbonCreditAmount :title="$t('statistics.statCO2VolumeTitle.compensated_carbon_credits')" :value="carbon_summary.tradedCredits"></StatCarbonCreditAmount>
				<StatCarbonCreditAmount :title="$t('statistics.statCO2VolumeTitle.carbon_credits_available')" :value="carbon_summary.remainCredits"></StatCarbonCreditAmount>
			</div>
			<div class="grid lg:grid-cols-2 grid-cols-1 gap-4">
				<div class="col-span-1 bg-theme-white shadow-sm rounded p-4">
					<!-- <span class="font-semibold text-theme-black-300 pt-4">{{$t('statistics.chart.title.verify_carbon_credit')}}</span> -->
					<HomeChart1></HomeChart1>
				</div>
				<div class="col-span-1 bg-theme-white shadow-sm rounded p-4">
					<!-- <span class="font-semibold text-theme-black-300 pt-4">{{$t('statistics.chart.title.yearly_verified_carbon_credit')}}</span> -->
					<HomeChart2></HomeChart2>
				</div>
				
			</div>
		</section>
		<section>
			<h2 class="mb-4 text-3xl font-bold">{{ $t("statistics.chart.title.transfer_stat") }}</h2>
			<div class="w-full p-4 bg-white rounded shadow-md">
				<StatTransferChart></StatTransferChart>
			</div>
		</section>
		
		<loadingCarbon v-if="isLoading"></loadingCarbon>
	</section>
</template>

<script>
export default {
	name: "HomePage",
	layout: "MainLayout",

	// middleware:['auth'],
	// mounted(){
	// 	this.$router.push('/dashboard')
	// }
	data() {
		return {
			tab: 1,
			filter: {
				searchText: "",
				type: "",
				status: "",
				sub_status: "",
				standard: "",
				min: null,
				max: null,
				vintage: [null, null],
				authUse: "",
			},

			current_page: 1,

			province: "",

			isLoading: true,

			limit: 10,

			sort: {
				key: "registration_date,project_id",
				value: "-1,-1",
			},

			openFilter: false,
			meta: {
				pages: 1,
				current_page: 1,
				total: 0,
			},
			stat: {
				total: 0,
				verified: 0,
				pending: 0,
				finish: 0,
			},
			// loading: true,
			carbon_summary: {
				verifiedCredits: 0,
				tradedCredits: 0,
				remainCredits: 0,
			},
			project: [],
			provinces: [],
			project_types: [],
			cancellation: {
				current_page: 1,
				data: [],
				meta: {
					pages: 1,
					current_page: 1,
					total: 0,
				},
				openFilter: false,
				sort: {
					key: "transaction_date,project_id",
					value: "-1,-1",
				},
				filter: {
					searchText: "",
					type: "",
					status: "",
					sub_status: "",
					standard: "",
					min: null,
					max: null,
					transaction_date: [null, null],
					vintage_year: [null, null],
					authUse: "",
					cancellation_reason_id: "",
				},
			},
			transfer_records: {
				current_page: 1,
				data: [],
				meta: {
					pages: 1,
					current_page: 1,
					total: 0,
				},
				openFilter: false,
				sort: {
					key: "transaction_date,project_id",
					value: "-1,-1",
				},
				filter: {
					searchText: "",
					type: "",
					status: "",
					sub_status: "",
					standard: "",
					min: null,
					max: null,
					transaction_date: [null, null],
					vintage_year: [null, null],
					authUse: "",
					cancellation_reason_id: "",
				},
			},
		};
	},
	watch: {
		status() {
			this.sub_status = "";
		},
		// limit() {
		// 	this.current_page = 1;
		// }
	},
	async mounted() {
		await this.getProvinces();

		await this.getStatPoject();
		await this.getCarbonCreditSummary();

		await this.getDatatableProject(this.sort, 1);
		await this.getCancellationProject(this.cancellation.sort, 1);
		await this.getITMOsTransfer(this.cancellation.sort, 1);
		this.isLoading = false;
	},
	methods: {
		resetFilter() {
			this.filter = {
				searchText: "",
				type: "",
				status: "",
				sub_status: "",
				standard: "",
				min: null,
				max: null,
				vintage: [null, null],
				authUse: "",
			};
			this.openFilter = false;
			this.getDatatableProject(this.sort, 1);
		},
		resetCancellationFilter() {
			this.cancellation.filter = {
				searchText: "",
				type: "",
				status: "",
				sub_status: "",
				standard: "",
				min: null,
				max: null,
				transaction_date: [null, null],
				vintage_year: [null, null],
				authUse: "",
				cancellation_reason_id: "",
			};
			this.cancellation.openFilter = false;
			this.getCancellationProject({ key: "transaction_date,project_id", value: "-1,-1" }, 1);
		},
		resetTransferRecordsFilter() {
			this.transfer_records.filter = {
				searchText: "",
				type: "",
				status: "",
				sub_status: "",
				standard: "",
				min: null,
				max: null,
				transaction_date: [null, null],
				vintage_year: [null, null],
				authUse: "",
				cancellation_reason_id: "",
			};
			this.transfer_records.openFilter = false;
			this.getITMOsTransfer({ key: "transaction_date,project_id", value: "-1,-1" }, 1);
		},

		async getProvinces() {
			const app = this;
			app.isLoading = true;
			await this.$axios
				.$get(`/api/v1/dropdown/provinces`)
				.then((resp) => {
					// console.log(resp);
					app.provinces = resp;
				})
				.catch((errors) => {
					console.log(errors);
					app.isLoading = false;
				});
		},

		async getCarbonCreditSummary() {
			const app = this;
			await this.$axios.$get(`/api/v1/home/statistics/carbon-credits-summary`).then((resp) => {
				// console.log(resp);
				app.carbon_summary = resp;
			}).catch(err=>{
				console.log(err);
			});
		},
		getStatPoject() {
			const app = this;
			this.$axios.$get(`/api/v1/home/projects`).then((resp) => {
				// console.log(resp);
				app.stat = resp;
			}).catch(err=>{
				console.log(err);
			});
		},
		async getCancellationProject(sort = { key: "transaction_date,project_id", value: "-1,-1" }, page = 1) {
			const app = this;
			this.cancellation.current_page = page;
			this.isLoading = true;
			let filter = `sort=${sort.value}&sort_by=${sort.key}`;
			if (this.cancellation.filter.searchText !== null && this.cancellation.filter.searchText !== "") filter += `&search=${this.cancellation.filter.searchText}`;
			if (this.cancellation.filter.type !== null && this.cancellation.filter.type !== "") filter += `&type=${this.cancellation.filter.type}`;
			if (this.cancellation.filter.min !== null && this.cancellation.filter.min !== "") filter += `&min=${this.cancellation.filter.min}`;
			if (this.cancellation.filter.max !== null && this.cancellation.filter.max !== "") filter += `&max=${this.cancellation.filter.max}`;
			if (this.cancellation.filter.authUse !== null && this.cancellation.filter.authUse !== "") filter += `&authorize_use=${this.cancellation.filter.authUse}`;
			if (this.cancellation.filter.cancellation_reason_id !== null && this.cancellation.filter.cancellation_reason_id !== "") filter += `&cancellation_reason_id=${this.cancellation.filter.cancellation_reason_id}`;
			if (this.cancellation.filter.transaction_date.length > 1 && !this.cancellation.filter.transaction_date.includes(null)) 
			filter += `&transaction_date_start=${this.$dayjs(this.cancellation.filter.transaction_date[0]).format("YYYY-MM-DD")}
				&transaction_date_end=${this.$dayjs(this.cancellation.filter.transaction_date[1]).format("YYYY-MM-DD")}`;
			if (this.cancellation.filter.vintage_year.length > 1 && !this.cancellation.filter.vintage_year.includes(null)) 
			filter += `&vintage_year_start=${this.$dayjs(this.cancellation.filter.vintage_year[0]).startOf('year').format("YYYY-MM-DD")}
				&vintage_year_end=${this.$dayjs(this.cancellation.filter.vintage_year[1]).endOf('year').format("YYYY-MM-DD")}`;
			if (this.limit !== null && this.limit !== "") filter += `&limit=${this.limit}`;
			await this.$axios
				.$get(`/api/v1/home/cancellation?page=${this.cancellation.current_page}&${filter}`)
				.then((resp) => {
					app.cancellation.data = resp.data;
					app.cancellation.meta = resp.meta;
					app.isLoading = false;
				})
				.catch((err) => {
					console.log(err);
				});
		},
		async getITMOsTransfer(sort = { key: "transaction_date,project_id", value: "-1,-1" }, page = 1) {
			const app = this;
			this.transfer_records.current_page = page;
			this.isLoading = true;
			let filter = `sort=${sort.value}&sort_by=${sort.key}`;
			if (this.transfer_records.filter.searchText !== null && this.transfer_records.filter.searchText !== "") filter += `&search=${this.transfer_records.filter.searchText}`;
			if (this.transfer_records.filter.type !== null && this.transfer_records.filter.type !== "") filter += `&type=${this.transfer_records.filter.type}`;
			if (this.transfer_records.filter.min !== null && this.transfer_records.filter.min !== "") filter += `&min=${this.transfer_records.filter.min}`;
			if (this.transfer_records.filter.max !== null && this.transfer_records.filter.max !== "") filter += `&max=${this.transfer_records.filter.max}`;
			if (this.transfer_records.filter.authUse !== null && this.transfer_records.filter.authUse !== "") filter += `&authorize_use=${this.transfer_records.filter.authUse}`;
			if (this.transfer_records.filter.cancellation_reason_id !== null && this.transfer_records.filter.cancellation_reason_id !== "") filter += `&cancellation_reason_id=${this.transfer_records.filter.cancellation_reason_id}`;
			if (this.transfer_records.filter.transaction_date.length > 1 && !this.transfer_records.filter.transaction_date.includes(null)) 
			filter += `&transaction_date_start=${this.$dayjs(this.transfer_records.filter.transaction_date[0]).format("YYYY-MM-DD")}
				&transaction_date_end=${this.$dayjs(this.transfer_records.filter.transaction_date[1]).format("YYYY-MM-DD")}`;
			if (this.transfer_records.filter.vintage_year.length > 1 && !this.transfer_records.filter.vintage_year.includes(null)) 
			filter += `&vintage_year_start=${this.$dayjs(this.transfer_records.filter.vintage_year[0]).startOf('year').format("YYYY-MM-DD")}
				&vintage_year_end=${this.$dayjs(this.transfer_records.filter.vintage_year[1]).endOf('year').format("YYYY-MM-DD")}`;
			if (this.limit !== null && this.limit !== "") filter += `&limit=${this.limit}`;
			await this.$axios
				.$get(`/api/v1/home/itmos_cancellation?page=${this.transfer_records.current_page}&${filter}`)
				.then((resp) => {
					app.transfer_records.data = resp.data;
					app.transfer_records.meta = resp.meta;
					app.isLoading = false;
				})
				.catch((err) => {
					console.log(err);
				});
		},
		async getDatatableProject(sort = { key: "registration_date,project_id", value: "-1,-1" }, page = 1) {
			const app = this;
			// console.log(page);
			this.sort = sort;
			this.current_page = page;

			// let filter = `&sort=${sort.value}&sort_by=${sort.key}`;
			let dateVintage = "";
			// if (this.filter.vintage.length === 2 && !this.filter.vintage.includes(null)) dateVintage += `&vintage_start=${this.$dayjs(this.filter.vintage[0]).format("YYYY-MM-DD")}&vintage_end=${this.$dayjs(this.filter.vintage[1]).format("YYYY-MM-DD")}`;
			app.isLoading = true;

			let filter = `&sort=${sort.value}&sort_by=${sort.key}`;
			if (this.filter.searchText !== null && this.filter.searchText !== "") filter += `&search=${this.filter.searchText}`;
			if (this.filter.type !== null && this.filter.type !== "") filter += `&type=${this.filter.type}`;
			if (this.filter.status !== null && this.filter.status !== "") filter += `&status=${this.filter.status}`;
			if (this.filter.standard !== null && this.filter.standard !== "") filter += `&standard=${this.filter.standard}`;
			if (this.filter.sub_status !== null && this.filter.sub_status !== "") filter += `&sub_status=${this.filter.sub_status}`;
			if (this.province !== null && this.province !== "") filter += `&province=${this.province}`;
			if (this.filter.min !== null && this.filter.min !== "") filter += `&min=${this.filter.min}`;
			if (this.filter.max !== null && this.filter.max !== "") filter += `&max=${this.filter.max}`;
			if (this.filter.authUse !== null && this.filter.authUse !== "") filter += `&authorize_use=${this.filter.authUse}`;
			if (this.limit !== null && this.limit !== "") filter += `&limit=${this.limit}`;
			if (this.filter.vintage.length > 1 && !this.filter.vintage.includes(null)) filter += `&vintage_start=${this.$dayjs(this.filter.vintage[0]).format("YYYY-MM-DD")}&vintage_end=${this.$dayjs(this.filter.vintage[1]).format("YYYY-MM-DD")}`;

			await this.$axios
				.$get(`/api/v1/home?page=${this.current_page}` + filter)
				.then((resp) => {
					// console.log(resp);
					app.project = resp.data;
					app.meta = resp.meta;
					app.isLoading = false;

					// this.$toast.success("เพิ่มข้อมูลสำเร็จ");
					// this.$router.push("/users/userManagement");
					// setTimeout(this.$toast.clear, 3000);
				})
				.catch((errors) => {
					console.log(errors);
					// this.$toast.error(errors.response.data.errors);
					// setTimeout(this.$toast.clear, 3000);
					app.isLoading = false;
				});
		},

		loadRequestByPage(pageNumber) {
			this.getDatatableProject(this.sort, pageNumber);
		},
	},
};
</script>
<style>
.border-gradient {
	border: 2px solid;
	border-image: linear-gradient(to right, #4da366, #1d73c9) 1;
}
.mx-datepicker.mx-datepicker-range {
	width: 100% !important;
}
[tooltip] {
	animation: 1s;
	animation-delay: 1s;
	animation-duration: 3s;
	display: none;
}
.projectname:hover [tooltip] {
	display: block;
}
.ccmgm:hover [tooltip] {
	display: block;
}
</style>
